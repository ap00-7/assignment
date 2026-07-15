import { useState } from 'react'

function AIChatPanel({ messages, onSend, activeInteraction }) {
  const [message, setMessage] = useState('')

  const handleSubmit = (event) => {
    event.preventDefault()
    if (!message.trim()) return
    onSend(message.trim())
    setMessage('')
  }

  return (
    <div className="card panel-chat">
      <div className="card-header">
        <h2>AI Assistant</h2>
        <p>Use the chatbot to log the transaction, summarize details, classify sentiment, or plan follow ups.</p>
      </div>
      <div className="chat-window">
        {messages.length === 0 && <p className="empty-chat">Describe interaction or ask the assistant for a summary.</p>}
        {messages.map((item, index) => (
          <div key={index} className={`chat-bubble ${item.sender}`}>
            <strong>{item.sender === 'assistant' ? 'Assistant' : 'You'}</strong>
            <p>{item.text}</p>
            {item.tool && item.sender === 'assistant' && <span className="chat-tool">Tool: {item.tool}</span>}
          </div>
        ))}
      </div>
      <form className="chat-input-row" onSubmit={handleSubmit}>
        <input
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          placeholder={activeInteraction ? 'Log the transaction or ask about this interaction...' : 'Log the transaction or ask for a summary...'}
        />
        <button className="primary" type="submit">Send</button>
      </form>
    </div>
  )
}

export default AIChatPanel
