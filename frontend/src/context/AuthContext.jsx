// ── [FRONTEND] Contexto · Autenticación ──────────────────────────────────────
import { createContext, useContext, useState, useEffect } from 'react'
import { me } from '../api/auth'

const AuthContext = createContext(null)

export function AuthProvider({ children }) {
  // undefined = verificando token, null = sin sesión, objeto = usuario autenticado
  const [user, setUser] = useState(undefined)

  useEffect(() => {
    const token = localStorage.getItem('token')
    if (!token) { setUser(null); return }
    me()
      .then(data => setUser(data))
      .catch(() => { localStorage.removeItem('token'); setUser(null) })
  }, [])

  function login(tokenData) {
    localStorage.setItem('token', tokenData.access_token)
    setUser(tokenData)
  }

  function logout() {
    localStorage.removeItem('token')
    setUser(null)
  }

  return (
    <AuthContext.Provider value={{ user, login, logout, loading: user === undefined }}>
      {children}
    </AuthContext.Provider>
  )
}

export const useAuth = () => useContext(AuthContext)
