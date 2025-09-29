import { createContext, useContext, useEffect, useMemo, useState } from 'react'
import api from '../api'

const AuthContext = createContext(null)

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null)

  useEffect(() => {
    const saved = localStorage.getItem('dh_user')
    if (saved) {
      try { setUser(JSON.parse(saved)) } catch {}
    }
  }, [])

  useEffect(() => {
    if (user) localStorage.setItem('dh_user', JSON.stringify(user))
    else localStorage.removeItem('dh_user')
  }, [user])

  const value = useMemo(() => ({
    user,
    logout: () => setUser(null),
    async register(username, password) {
      const u = await api.post('/register', { username, password })
      setUser(u)
      return u
    },
    async login(username, password) {
      const u = await api.post('/login', { username, password })
      setUser(u)
      return u
    },
  }), [user])

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

export function useAuth() {
  return useContext(AuthContext)
}
