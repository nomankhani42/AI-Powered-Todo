import api from "./api";
import { Task, TaskStatus, TaskPriority } from "@/redux/slices/taskSlice";

export interface TaskCreateRequest {
  title: string;
  description?: string;
  deadline?: string;
}

export interface TaskUpdateRequest {
  title?: string;
  description?: string;
  status?: TaskStatus;
  priority?: TaskPriority;
  deadline?: string;
}

export interface PaginatedTasksResponse {
  status: string;
  data: {
    items: Task[];
    total: number;
    skip: number;
    limit: number;
  };
}

export interface TaskResponse {
  status: string;
  data: Task;
}

/**
 * Normalize task response from backend
 * Converts any timestamp strings to ISO format
 */
function normalizeTask(task: any): Task {
  return {
    id: typeof task.id === 'string' ? task.id : String(task.id),
    owner_id: typeof task.owner_id === 'string' ? task.owner_id : String(task.owner_id),
    title: task.title || '',
    description: task.description || undefined,
    status: task.status || 'pending',
    priority: task.priority || 'medium',
    deadline: task.deadline ? new Date(task.deadline).toISOString() : undefined,
    estimated_duration: task.estimated_duration || undefined,
    ai_estimated_duration: task.ai_estimated_duration || undefined,
    ai_priority: task.ai_priority || undefined,
    created_at: task.created_at ? new Date(task.created_at).toISOString() : new Date().toISOString(),
    updated_at: task.updated_at ? new Date(task.updated_at).toISOString() : new Date().toISOString(),
    completed_at: task.completed_at ? new Date(task.completed_at).toISOString() : undefined,
  };
}

export const tasksService = {
  getTasks: async (
    status?: TaskStatus,
    priority?: TaskPriority,
    skip: number = 0,
    limit: number = 20
  ): Promise<{ tasks: Task[]; total: number; skip: number; limit: number }> => {
    const params: Record<string, any> = { skip, limit };
    if (status) params.status = status;
    if (priority) params.priority = priority;

    const response = await api.get<any>("tasks", { params });

    // Handle different response formats from backend
    const data = response.data;
    let items = [];
    let total = 0;

    if (data.items && Array.isArray(data.items)) {
      // Format: { items: [...], total: N, skip: N, limit: N }
      items = data.items.map(normalizeTask);
      total = data.total || items.length;
    } else if (Array.isArray(data)) {
      // Format: just an array of tasks
      items = data.map(normalizeTask);
      total = items.length;
    } else if (data.data && Array.isArray(data.data.items)) {
      // Format: { data: { items: [...], total: N, skip: N, limit: N } }
      items = data.data.items.map(normalizeTask);
      total = data.data.total || items.length;
    }

    return {
      tasks: items,
      total,
      skip: skip || 0,
      limit: limit || 20,
    };
  },

  getTask: async (taskId: string): Promise<Task> => {
    const response = await api.get<any>(`tasks/${taskId}`);
    // Handle different response formats
    const task = response.data.data || response.data;
    return normalizeTask(task);
  },

  createTask: async (data: TaskCreateRequest): Promise<Task> => {
    const response = await api.post<any>("tasks", data);
    // Handle different response formats
    const task = response.data.data || response.data;
    return normalizeTask(task);
  },

  updateTask: async (
    taskId: string,
    data: TaskUpdateRequest
  ): Promise<Task> => {
    const response = await api.put<any>(`tasks/${taskId}`, data);
    // Handle different response formats
    const task = response.data.data || response.data;
    return normalizeTask(task);
  },

  deleteTask: async (taskId: string): Promise<void> => {
    await api.delete(`tasks/${taskId}`);
  },

  completeTask: async (taskId: string): Promise<Task> => {
    // Note: Backend may not have a /complete endpoint, use updateTask instead
    try {
      const response = await api.patch<any>(
        `tasks/${taskId}/complete`
      );
      const task = response.data.data || response.data;
      return normalizeTask(task);
    } catch (error) {
      // Fallback: use updateTask with status=completed
      return tasksService.updateTask(taskId, { status: 'completed' });
    }
  },
};
