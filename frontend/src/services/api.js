import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

export const aiProcessPrompt = async (prompt, currentData) => {
  const formData = new FormData();
  formData.append('prompt', prompt);
  if (currentData && Object.keys(currentData).length > 0) {
    formData.append('current_data', JSON.stringify(currentData));
  }
  const response = await axios.post(`${API_URL}/ai/process_prompt`, formData);
  return response.data;
};

export const aiProcessDocument = async (file, currentData) => {
  const formData = new FormData();
  formData.append('file', file);
  if (currentData && Object.keys(currentData).length > 0) {
    formData.append('current_data', JSON.stringify(currentData));
  }
  const response = await axios.post(`${API_URL}/ai/process_document`, formData);
  return response.data;
};
