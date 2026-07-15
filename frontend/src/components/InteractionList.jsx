function InteractionList({ interactions, status, onEdit, onDelete }) {
  return (
    <div className="card card-list">
      <div className="card-header">
        <h2>Saved Interactions</h2>
      </div>
      {status === 'loading' && <p>Loading saved interactions…</p>}
      {interactions.length === 0 && status !== 'loading' && <p>No interactions logged yet.</p>}
      <div className="interaction-list">
        {interactions.map((item) => (
          <article key={item.id} className="interaction-card">
            <div>
              <strong>{item.hcp_name}</strong>
              <p>{item.date} · {item.interaction_type}</p>
              <p>{item.topics || 'No topics provided'}</p>
            </div>
            <div className="card-actions">
              <button onClick={() => onEdit(item)}>Edit</button>
              <button className="danger" onClick={() => onDelete(item.id)}>Delete</button>
            </div>
          </article>
        ))}
      </div>
    </div>
  )
}

export default InteractionList
