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
    if 'summarize' in request.prompt.lower():
        text = agent.summarize_interaction(interaction if interaction else {'topics': request.prompt})
        tool = 'Summarize Interaction'
    elif 'follow-up' in request.prompt.lower() or 'follow up' in request.prompt.lower():
        text = agent.extract_action_items(request.prompt)
        tool = 'Follow-up Planner'
    elif 'sentiment' in request.prompt.lower():
        text = agent.classify_sentiment(request.prompt)
        tool = 'Sentiment Classifier'
    else:
        text = agent.help_describe(request.prompt)
        tool = 'AI Assistant'
    return schemas.AIResponse(text=text, tool=tool)
