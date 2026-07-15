import { useEffect, useState } from 'react'
import { useDispatch, useSelector } from 'react-redux'
import { fetchInteractions, createInteraction, updateInteraction, deleteInteraction, aiChat, addChatMessage, clearChat } from './features/interactionsSlice'
import InteractionForm from './components/InteractionForm'
import AIChatPanel from './components/AIChatPanel'
import InteractionList from './components/InteractionList'

function App() {
  const dispatch = useDispatch()
  const interactions = useSelector((state) => state.interactions.list)
  const status = useSelector((state) => state.interactions.status)
  const chat = useSelector((state) => state.interactions.chat)
  const [activeInteraction, setActiveInteraction] = useState(null)

  useEffect(() => {
    dispatch(fetchInteractions())
  }, [dispatch])

  const handleSubmit = async (payload) => {
    if (activeInteraction) {
      await dispatch(updateInteraction({ id: activeInteraction.id, payload }))
      setActiveInteraction(null)
    } else {
      await dispatch(createInteraction(payload))
    }
    dispatch(clearChat())
  }

  const handleEdit = (interaction) => {
    setActiveInteraction(interaction)
    dispatch(clearChat())
  }

  const handleDelete = (id) => {
    dispatch(deleteInteraction(id))
    if (activeInteraction?.id === id) {
      setActiveInteraction(null)
    }
  }

  const handleAssistantSend = async (message, interactionId) => {
    dispatch(addChatMessage({ sender: 'user', text: message }))
    try {
      console.log('[DEBUG] Sending AI chat request:', { message, interactionId })
      const res = await dispatch(aiChat({ prompt: message, interaction_id: interactionId, force_log: true })).unwrap()
      console.log('[DEBUG] AI chat response:', res)
      if (res?.interaction) {
        console.log('[DEBUG] Setting active interaction:', res.interaction)
        setActiveInteraction(res.interaction)
      } else {
        console.log('[DEBUG] No interaction in response')
      }
    } catch (err) {
      console.error('[DEBUG] AI chat error', err)
    }
  }

  return (
    <div className="app-shell">
      <header className="app-header">
        <div>
          <p className="eyebrow">AI-First CRM | HCP Interaction</p>
          <h1>Log Interaction Screen</h1>
          <p>Capture HCP interaction notes with structured capture and AI assistance.</p>
        </div>
      </header>

      <main className="layout-grid">
        <section className="panel panel-form">
          <InteractionForm
            onSubmit={handleSubmit}
            interaction={activeInteraction}
            onCancel={() => setActiveInteraction(null)}
          />
          <InteractionList
            interactions={interactions}
            status={status}
            onEdit={handleEdit}
            onDelete={handleDelete}
          />
        </section>

        <section className="panel panel-side">
          <AIChatPanel
            messages={chat.messages}
            onSend={(message) => handleAssistantSend(message, activeInteraction?.id)}
            activeInteraction={activeInteraction}
          />
        </section>
      </main>
    </div>
  )
}

export default App
