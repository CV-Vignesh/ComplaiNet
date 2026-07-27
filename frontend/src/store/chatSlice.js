import { createSlice } from '@reduxjs/toolkit';

const initialState = {
  messages: [
    {
      id: 'system-1',
      sender: 'ai',
      text: 'Hello! I am your QA Assistant. Describe the customer complaint, or upload a document (PDF, DOCX, TXT) and I will automatically extract the details into the form.',
      timestamp: new Date().toISOString()
    }
  ],
  isProcessing: false,
};

export const chatSlice = createSlice({
  name: 'chat',
  initialState,
  reducers: {
    addMessage: (state, action) => {
      state.messages.push(action.payload);
    },
    setProcessing: (state, action) => {
      state.isProcessing = action.payload;
    },
    clearChat: (state) => {
      state.messages = initialState.messages;
    }
  }
});

export const { addMessage, setProcessing, clearChat } = chatSlice.actions;
export default chatSlice.reducer;
