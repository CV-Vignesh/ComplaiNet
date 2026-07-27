import { configureStore } from '@reduxjs/toolkit';
import complaintReducer from './store/complaintSlice';
import chatReducer from './store/chatSlice';

export const store = configureStore({
  reducer: {
    complaint: complaintReducer,
    chat: chatReducer,
  },
});
