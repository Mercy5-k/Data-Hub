const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000/api'

async function request(endpoint, options = {}, isForm = false) {
  const res = await fetch(`${API_URL}${endpoint}`, {
    ...options,
    headers: isForm ? {} : { 'Content-Type': 'application/json' },
  })
  if (!res.ok) {
    let message = 'Request failed'
    try {
      const err = await res.json()
      message = err.error || message
    } catch (_) {}
    throw new Error(message)
  }
  return res.status === 204 ? null : res.json()
}

export default {
  get: (endpoint) => request(endpoint),
  post: (endpoint, data, isForm = false) =>
    request(endpoint, { method: 'POST', body: isForm ? data : JSON.stringify(data) }, isForm),
  patch: (endpoint, data) =>
    request(endpoint, { method: 'PATCH', body: JSON.stringify(data) }),
  delete: (endpoint) => request(endpoint, { method: 'DELETE' }),
}
