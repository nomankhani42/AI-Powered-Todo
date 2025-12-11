/**
 * API client for communicating with the backend.
 *
 * Wraps axios for making HTTP requests to the FastAPI backend.
 */

import axios from "axios";

const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";

// Create axios instance with base configuration
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

// Request interceptor (for adding auth tokens if needed)
api.interceptors.request.use(
  (config) => {
    // Add auth token if available
    try {
      const token = localStorage.getItem("accessToken");
      if (token && token.trim()) {
        config.headers.Authorization = `Bearer ${token}`;
      }
    } catch (error) {
      // localStorage might not be available in SSR
      console.warn("Could not access localStorage for token");
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor (for handling common errors)
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Handle unauthorized - clear token and redirect to login
      localStorage.removeItem("accessToken");
      window.location.href = "/auth/login";
    }
    return Promise.reject(error);
  }
);

// Task API endpoints
export const taskApi = {
  /**
   * Get all tasks
   * @returns Promise with tasks list and statistics
   */
  getTasks: () =>
    api.get("tasks", {
      params: {},
    }),

  /**
   * Create a new task
   * @param description Task description
   * @returns Promise with created task
   */
  createTask: (description: string) =>
    api.post("tasks", {
      description,
    }),

  /**
   * Get a single task by ID
   * @param id Task ID
   * @returns Promise with task details
   */
  getTask: (id: number) => api.get(`tasks/${id}`),

  /**
   * Update a task's description
   * @param id Task ID
   * @param description New description
   * @returns Promise with updated task
   */
  updateTask: (id: number, description: string) =>
    api.put(`tasks/${id}`, {
      description,
    }),

  /**
   * Mark a task as complete
   * @param id Task ID
   * @returns Promise with updated task
   */
  completeTask: (id: number) => api.patch(`tasks/${id}/complete`),

  /**
   * Delete a task
   * @param id Task ID
   * @returns Promise with success message
   */
  deleteTask: (id: number) => api.delete(`tasks/${id}`),
};

export default api;
