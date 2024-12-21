// filename: vue_js_project/src/plugins/axios.js
import axios from 'axios';

// Set your backend API base URL
axios.defaults.baseURL = 'http://localhost:8000';

// Function to set or remove the Authorization header
export function setAuthToken(token) {
  if (token) {
    console.log("Setting token in localStorage and Axios headers:", token);
    localStorage.setItem('accessToken', token);
    axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
  } else {
    console.log("Removing token from localStorage and Axios headers");
    localStorage.removeItem('accessToken');
    delete axios.defaults.headers.common['Authorization'];
  }
}

// Initialize the Authorization header if token exists in localStorage
const storedToken = localStorage.getItem('accessToken');
if (storedToken) {
  console.log("Found token in localStorage, setting Axios Authorization header:", storedToken);
  axios.defaults.headers.common['Authorization'] = `Bearer ${storedToken}`;
} else {
  console.log("No token found in localStorage");
}

export default axios;
