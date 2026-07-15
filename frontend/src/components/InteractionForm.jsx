import { useEffect, useState } from 'react'

const initialForm = {
  hcp_name: '',
  interaction_type: 'Meeting',
  date: '',
  time: '',
  attendees: '',
  topics: '',
  sentiment: 'Neutral',
  outcomes: '',
  follow_up: '',
  notes: '',
  materials: [],
  samples: [],
}

function InteractionForm({ onSubmit, interaction, onCancel }) {
  const [form, setForm] = useState(initialForm)
  const [materialInput, setMaterialInput] = useState('')
  const [sampleName, setSampleName] = useState('')
  const [sampleQuantity, setSampleQuantity] = useState('')

  useEffect(() => {
    if (interaction) {
      setForm({
        ...initialForm,
        ...interaction,
        materials: interaction.materials || [],
        samples: interaction.samples || [],
      })
    } else {
      setForm(initialForm)
    }
  }, [interaction])

  const handleChange = (field) => (event) => {
    setForm({ ...form, [field]: event.target.value })
  }

  const addMaterial = () => {
    if (!materialInput.trim()) return
    setForm({ ...form, materials: [...form.materials, { name: materialInput.trim() }] })
    setMaterialInput('')
  }

  const addSample = () => {
    if (!sampleName.trim()) return
    setForm({ ...form, samples: [...form.samples, { name: sampleName.trim(), quantity: sampleQuantity.trim() }] })
    setSampleName('')
    setSampleQuantity('')
  }

  const removeMaterial = (index) => {
    setForm({
      ...form,
      materials: form.materials.filter((_, i) => i !== index),
    })
  }

  const removeSample = (index) => {
    setForm({
      ...form,
      samples: form.samples.filter((_, i) => i !== index),
    })
  }

  const handleSubmit = (event) => {
    event.preventDefault()
    onSubmit(form)
  }

  return (
    <div className="card">
      <div className="card-header">
        <h2>{interaction ? 'Edit Interaction' : 'New Interaction'}</h2>
      </div>
      <form className="form-grid" onSubmit={handleSubmit}>
        <label>
          HCP Name
          <input value={form.hcp_name} onChange={handleChange('hcp_name')} required />
        </label>
        <label>
          Interaction Type
          <select value={form.interaction_type} onChange={handleChange('interaction_type')}>
            <option>Meeting</option>
            <option>Call</option>
            <option>Conference</option>
            <option>Virtual Visit</option>
          </select>
        </label>
        <label>
          Date
          <input type="date" value={form.date} onChange={handleChange('date')} required />
        </label>
        <label>
          Time
          <input type="time" value={form.time} onChange={handleChange('time')} required />
        </label>
        <label>
          Attendees
          <input value={form.attendees} onChange={handleChange('attendees')} placeholder="Enter names or roles" />
        </label>
        <label className="full-width">
          Topics Discussed
          <textarea value={form.topics} onChange={handleChange('topics')} rows={4} placeholder="Enter key discussion points..." />
        </label>

        <div className="section-title full-width">Materials Shared</div>
        <div className="inline-row full-width">
          <input value={materialInput} onChange={(e) => setMaterialInput(e.target.value)} placeholder="Material name" />
          <button type="button" onClick={addMaterial}>Add</button>
        </div>
        <div className="chip-list full-width">
          {form.materials.map((item, index) => (
            <span key={index} className="chip">
              {item.name}
              <button type="button" onClick={() => removeMaterial(index)}>×</button>
            </span>
          ))}
        </div>

        <div className="section-title full-width">Samples Distributed</div>
        <div className="inline-row full-width">
          <input value={sampleName} onChange={(e) => setSampleName(e.target.value)} placeholder="Sample name" />
          <input value={sampleQuantity} onChange={(e) => setSampleQuantity(e.target.value)} placeholder="Quantity" />
          <button type="button" onClick={addSample}>Add</button>
        </div>
        <div className="chip-list full-width">
          {form.samples.map((sample, index) => (
            <span key={index} className="chip">
              {sample.name} {sample.quantity ? `(${sample.quantity})` : ''}
              <button type="button" onClick={() => removeSample(index)}>×</button>
            </span>
          ))}
        </div>

        <label>
          Observed / Inferred HCP Sentiment
          <div className="radio-row">
            {['Positive', 'Neutral', 'Negative'].map((value) => (
              <label key={value} className="radio-inline">
                <input type="radio" name="sentiment" value={value} checked={form.sentiment === value} onChange={handleChange('sentiment')} />
                {value}
              </label>
            ))}
          </div>
        </label>

        <label className="full-width">
          Outcomes
          <textarea value={form.outcomes} onChange={handleChange('outcomes')} rows={3} placeholder="Key outcomes or agreements..." />
        </label>
        <label className="full-width">
          Follow-up Actions
          <textarea value={form.follow_up} onChange={handleChange('follow_up')} rows={3} placeholder="Enter next steps or tasks..." />
        </label>
        <label className="full-width">
          Additional Notes
          <textarea value={form.notes} onChange={handleChange('notes')} rows={3} placeholder="Optional supporting details only; use the AI chatbot to log the transaction." />
        </label>

        <div className="actions full-width">
          <button className="primary" type="submit">{interaction ? 'Save Changes' : 'Log Interaction'}</button>
          {interaction && <button type="button" className="secondary" onClick={onCancel}>Cancel</button>}
        </div>
      </form>
    </div>
  )
}

export default InteractionForm
