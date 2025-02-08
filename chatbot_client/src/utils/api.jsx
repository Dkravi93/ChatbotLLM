import axios from 'axios';
import { getToken } from './auth';

// Create an instance of axios with the base URL of your FastAPI backend
const api = axios.create({
  baseURL: 'http://localhost:8000/api', // Your FastAPI server URL
});

// Function to send a query (for example, for a chatbot)
export const sendQuery = async (query) => {
  try {
    const response = await api.post('/query', query);
    return response.data;
  } catch (error) {
    console.error("Error:", error);
    throw error;
  }
};

// Function to fetch user data by token
export const fetchUserData = async () => {
  try {

    const token = getToken();

    if (!token) {
      throw new Error("No token found. Please log in.");
    }

    // Make a GET request to the /me endpoint with the token in the Authorization header
    const response = await api.get('/users/me', {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });

    // Return the user data from the response
    return response.data;
  } catch (error) {
    console.error("Error fetching user data:", error);
    throw error;
  }
};
