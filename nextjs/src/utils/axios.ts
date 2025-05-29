import axios from "axios";

// Configure axios defaults
axios.defaults.xsrfCookieName = "csrftoken";
axios.defaults.xsrfHeaderName = "X-CSRFToken";
axios.defaults.withCredentials = true;

// Create an axios instance with the base URL if needed
export const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL || "/api",
});

// USAGE:
// import { api } from "@/utils/axios";

// Request interceptor
api.interceptors.request.use(
  (config) => {
    // You can add additional logic here if needed
    // For example, adding auth tokens from localStorage
    // const token = localStorage.getItem('token');
    // if (token) {
    //   config.headers.Authorization = `Bearer ${token}`;
    // }

    return config;
  },
  (error) => {
    return Promise.reject(error);
  },
);

// Response interceptor
api.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    // Handle specific error cases
    if (error.response) {
      // The request was made and the server responded with a status code
      // that falls out of the range of 2xx
      if (
        error.response.status === 403 &&
        error.response.data.detail ===
          "CSRF Failed: CSRF token missing or incorrect."
      ) {
        // If CSRF token is missing, try to get a new one and retry the request
        return axios.get("/api/csrf/").then(() => {
          // After getting a new CSRF token, retry the original request
          return api(error.config);
        });
      }
    }

    return Promise.reject(error);
  },
);

// Initial CSRF token fetch
export const initializeCSRF = async () => {
  try {
    await axios.get("/api/csrf/");
  } catch (error) {
    console.error("Failed to initialize CSRF token:", error);
  }
};

export default api;
