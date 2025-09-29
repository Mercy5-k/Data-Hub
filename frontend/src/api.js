const API_URL = import.meta.env.VITE_API_URL || "https://data-hub-1-r2qi.onrender.com";

async function request(endpoint, options = {}, isForm = false) {
  try {
    const url = `${API_URL}/api${endpoint}`;
    const config = {
      ...options,
      headers: isForm ? {} : { "Content-Type": "application/json" },
    };
    
    const response = await fetch(url, config);
    
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({ error: 'Network error' }));
      throw new Error(errorData.error || `HTTP error! status: ${response.status}`);
    }
    
    return await response.json();
  } catch (error) {
    console.error('API request failed:', error);
    throw error;
  }
}

const api = {
  // Generic methods
  get: (endpoint) => request(endpoint),
  post: (endpoint, data, isForm = false) =>
    request(endpoint, { 
      method: "POST", 
      body: isForm ? data : JSON.stringify(data) 
    }, isForm),
  patch: (endpoint, data) =>
    request(endpoint, { 
      method: "PATCH", 
      body: JSON.stringify(data) 
    }),
  delete: (endpoint) => request(endpoint, { method: "DELETE" }),
  
  // Specific API methods
  files: {
    getAll: () => api.get('/files'),
    getById: (id) => api.get(`/files/${id}`),
    create: (formData) => api.post('/files', formData, true),
    update: (id, data) => api.patch(`/files/${id}`, data),
    delete: (id) => api.delete(`/files/${id}`),
    addTag: (id, tagData) => api.post(`/files/${id}/tags`, tagData)
  },
  
  collections: {
    getAll: () => api.get('/collections'),
    create: (data) => api.post('/collections', data)
  },
  
  tags: {
    getAll: () => api.get('/tags'),
    create: (data) => api.post('/tags', data)
  },
  
  users: {
    getAll: () => api.get('/users'),
    create: (data) => api.post('/users', data)
  },
  
  health: () => api.get('/health')
};

export default api;
