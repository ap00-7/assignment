from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .database import get_connection, init_db
from . import crud, schemas
from .langgraph_agent import LangGraphAgent

app = FastAPI(title='AI-First CRM HCP Module')

origins = [
    'http://localhost:5173',
    'http://127.0.0.1:5173',
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

agent = LangGraphAgent()


@app.on_event('startup')
def startup_event():
    init_db()


def get_db():
    db = get_connection()
    try:
        yield db
    finally:
        db.close()


@app.get('/health')
def health_check():
    return {'status': 'ok'}


@app.get('/interactions', response_model=list[schemas.HCPInteraction])
def list_interactions(skip: int = 0, limit: int = 100, db=Depends(get_db)):
    return crud.get_interactions(db, skip=skip, limit=limit)


@app.post('/interactions', response_model=schemas.HCPInteraction)
def create_interaction(interaction: schemas.HCPInteractionCreate, db=Depends(get_db)):
    created = crud.create_interaction(db, interaction)
    summary = agent.summarize_interaction(created)
    cursor = db.cursor()
    cursor.execute('UPDATE hcp_interactions SET ai_summary = ? WHERE id = ?', (summary, created['id']))
    db.commit()
    created['ai_summary'] = summary
    return created


@app.put('/interactions/{interaction_id}', response_model=schemas.HCPInteraction)
def update_interaction(interaction_id: int, data: schemas.HCPInteractionUpdate, db=Depends(get_db)):
    updated = crud.update_interaction(db, interaction_id, data)
    if not updated:
        raise HTTPException(status_code=404, detail='Interaction not found')
    summary = agent.summarize_interaction(updated)
    cursor = db.cursor()
    cursor.execute('UPDATE hcp_interactions SET ai_summary = ? WHERE id = ?', (summary, updated['id']))
    db.commit()
    updated['ai_summary'] = summary
    return updated


@app.delete('/interactions/{interaction_id}', response_model=schemas.HCPInteraction)
def delete_interaction(interaction_id: int, db=Depends(get_db)):
    deleted = crud.delete_interaction(db, interaction_id)
    if not deleted:
        raise HTTPException(status_code=404, detail='Interaction not found')
    return deleted


@app.post('/ai/chat', response_model=schemas.AIResponse)
def ai_chat(request: schemas.AIRequest, db=Depends(get_db)):
    interaction = None
    if request.interaction_id:
        interaction = crud.get_interaction(db, request.interaction_id)
    prompt = request.prompt
    if interaction:
        prompt = f"Interaction context: {interaction.get('topics') or ''}. {prompt}"
    tool = 'Log Interaction' if request.force_log else agent.route_tool(prompt)
    created_interaction = None
    if tool == 'Summarize Interaction':
        text = agent.summarize_interaction(interaction if interaction else {'topics': prompt})
    elif tool == 'Follow-up Planner':
        text = agent.extract_action_items(prompt)
    elif tool == 'Sentiment Classifier':
        text = agent.classify_sentiment(prompt)
    elif tool == 'Log Interaction':
        # Parse structured fields and create an interaction record
        parsed = agent.parse_transaction(prompt)
        create_payload = {
            'hcp_name': parsed.get('hcp_name') or '',
            'interaction_type': parsed.get('interaction_type') or 'Meeting',
            'date': parsed.get('date') or '',
            'time': parsed.get('time') or '',
            'attendees': parsed.get('attendees'),
            'topics': parsed.get('topics'),
            'sentiment': parsed.get('sentiment'),
            'outcomes': parsed.get('outcomes'),
            'follow_up': parsed.get('follow_up'),
            'notes': parsed.get('notes'),
            'materials': parsed.get('materials') or [],
            'samples': parsed.get('samples') or [],
        }
        created_interaction = crud.create_interaction(db, schemas.HCPInteractionCreate(**create_payload))
        # generate summary and attach
        summary = agent.summarize_interaction(created_interaction)
        cursor = db.cursor()
        cursor.execute('UPDATE hcp_interactions SET ai_summary = ? WHERE id = ?', (summary, created_interaction['id']))
        db.commit()
        created_interaction['ai_summary'] = summary
        text = summary
    else:
        text = agent.help_describe(prompt)

    return schemas.AIResponse(text=text, tool=tool, interaction=created_interaction)
