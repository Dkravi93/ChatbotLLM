import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000/api', // Your FastAPI server URL
});

export const sendQuery = async (query) => {
  try {
    const response = await api.post('/query', { query });
    return response.data;
  } catch (error) {
    console.error("Error:", error);
    throw error;
  }
};
