from typing import Optional
from . import schemas


def row_to_dict(row):
    if row is None:
        return None
    return {k: row[k] for k in row.keys()}


def get_interaction(db, interaction_id: int):
    cursor = db.cursor()
    cursor.execute('SELECT * FROM hcp_interactions WHERE id = ?', (interaction_id,))
    interaction = row_to_dict(cursor.fetchone())
    if not interaction:
        return None
    cursor.execute('SELECT id, name FROM materials WHERE interaction_id = ?', (interaction_id,))
    interaction['materials'] = [row_to_dict(row) for row in cursor.fetchall()]
    cursor.execute('SELECT id, name, quantity FROM samples WHERE interaction_id = ?', (interaction_id,))
    interaction['samples'] = [row_to_dict(row) for row in cursor.fetchall()]
    return interaction


def get_interactions(db, skip: int = 0, limit: int = 100):
    cursor = db.cursor()
    cursor.execute('SELECT * FROM hcp_interactions ORDER BY id DESC LIMIT ? OFFSET ?', (limit, skip))
    rows = cursor.fetchall()
    interactions = [row_to_dict(row) for row in rows]
    for interaction in interactions:
        interaction_id = interaction['id']
        cursor.execute('SELECT id, name FROM materials WHERE interaction_id = ?', (interaction_id,))
        interaction['materials'] = [row_to_dict(row) for row in cursor.fetchall()]
        cursor.execute('SELECT id, name, quantity FROM samples WHERE interaction_id = ?', (interaction_id,))
        interaction['samples'] = [row_to_dict(row) for row in cursor.fetchall()]
    return interactions


def create_interaction(db, interaction: schemas.HCPInteractionCreate):
    cursor = db.cursor()
    cursor.execute(
        '''INSERT INTO hcp_interactions
           (hcp_name, interaction_type, date, time, attendees, topics, sentiment, outcomes, follow_up, notes, ai_summary)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''',
        (
            interaction.hcp_name,
            interaction.interaction_type,
            interaction.date,
            interaction.time,
            interaction.attendees,
            interaction.topics,
            interaction.sentiment,
            interaction.outcomes,
            interaction.follow_up,
            interaction.notes,
            None,
        ),
    )
    interaction_id = cursor.lastrowid
    for material in interaction.materials or []:
        cursor.execute('INSERT INTO materials (interaction_id, name) VALUES (?, ?)', (interaction_id, material.name))
    for sample in interaction.samples or []:
        cursor.execute('INSERT INTO samples (interaction_id, name, quantity) VALUES (?, ?, ?)', (interaction_id, sample.name, sample.quantity))
    db.commit()
    return get_interaction(db, interaction_id)


def update_interaction(db, interaction_id: int, update: schemas.HCPInteractionUpdate):
    existing = get_interaction(db, interaction_id)
    if not existing:
        return None
    fields = update.model_dump(exclude_unset=True)
    set_values = []
    updates = []
    for key in ['hcp_name', 'interaction_type', 'date', 'time', 'attendees', 'topics', 'sentiment', 'outcomes', 'follow_up', 'notes']:
        if key in fields:
            set_values.append(fields[key])
            updates.append(f"{key} = ?")
    if updates:
        cursor = db.cursor()
        cursor.execute(f"UPDATE hcp_interactions SET {', '.join(updates)} WHERE id = ?", (*set_values, interaction_id))
    if update.materials is not None:
        cursor = db.cursor()
        cursor.execute('DELETE FROM materials WHERE interaction_id = ?', (interaction_id,))
        for material in update.materials:
            cursor.execute('INSERT INTO materials (interaction_id, name) VALUES (?, ?)', (interaction_id, material.name))
    if update.samples is not None:
        cursor = db.cursor()
        cursor.execute('DELETE FROM samples WHERE interaction_id = ?', (interaction_id,))
        for sample in update.samples:
            cursor.execute('INSERT INTO samples (interaction_id, name, quantity) VALUES (?, ?, ?)', (interaction_id, sample.name, sample.quantity))
    db.commit()
    return get_interaction(db, interaction_id)


def delete_interaction(db, interaction_id: int):
    cursor = db.cursor()
    interaction = get_interaction(db, interaction_id)
    if not interaction:
        return None
    cursor.execute('DELETE FROM materials WHERE interaction_id = ?', (interaction_id,))
    cursor.execute('DELETE FROM samples WHERE interaction_id = ?', (interaction_id,))
    cursor.execute('DELETE FROM hcp_interactions WHERE id = ?', (interaction_id,))
    db.commit()
    return interaction
