import { createSlice, createAsyncThunk } from '@reduxjs/toolkit'
import api from '../api'

export const fetchInteractions = createAsyncThunk('interactions/fetch', async () => {
  const response = await api.get('/interactions')
  return response.data
})

export const createInteraction = createAsyncThunk('interactions/create', async (payload) => {
  const response = await api.post('/interactions', payload)
  return response.data
})

export const updateInteraction = createAsyncThunk('interactions/update', async ({ id, payload }) => {
  const response = await api.put(`/interactions/${id}`, payload)
  return response.data
})

export const deleteInteraction = createAsyncThunk('interactions/delete', async (id) => {
  await api.delete(`/interactions/${id}`)
  return id
})

export const aiChat = createAsyncThunk('interactions/aiChat', async (payload) => {
  const response = await api.post('/ai/chat', payload)
  return response.data
})

const interactionsSlice = createSlice({
  name: 'interactions',
  initialState: {
    list: [],
    status: 'idle',
    chat: { messages: [] },
  },
  reducers: {
    addChatMessage(state, action) {
      state.chat.messages.push(action.payload)
    },
    clearChat(state) {
      state.chat.messages = []
    },
  },
  extraReducers(builder) {
    builder
      .addCase(fetchInteractions.fulfilled, (state, action) => {
        state.list = action.payload
        state.status = 'succeeded'
      })
      .addCase(fetchInteractions.pending, (state) => {
        state.status = 'loading'
      })
      .addCase(createInteraction.fulfilled, (state, action) => {
        state.list.unshift(action.payload)
      })
      .addCase(updateInteraction.fulfilled, (state, action) => {
        state.list = state.list.map((item) => (item.id === action.payload.id ? action.payload : item))
      })
      .addCase(deleteInteraction.fulfilled, (state, action) => {
        state.list = state.list.filter((item) => item.id !== action.payload)
      })
      .addCase(aiChat.fulfilled, (state, action) => {
        state.chat.messages.push({ sender: 'assistant', text: action.payload.text, tool: action.payload.tool })
      })
  },
})

export const { addChatMessage, clearChat } = interactionsSlice.actions
export default interactionsSlice.reducer
