import { createContext, useContext, useState } from 'react'

import { AUTH_TOKEN_KEY } from '../utils/auth.js'

const AuthContext = createContext(null)

export function AuthProvider({ children }) {
  const [token, setToken] = useState(() => localStorage.getItem(AUTH_TOKEN_KEY))

  function login(accessToken) {
    localStorage.setItem(AUTH_TOKEN_KEY, accessToken)
    setToken(accessToken)
  }

  function logout() {
    localStorage.removeItem(AUTH_TOKEN_KEY)
    setToken(null)
  }

  return (
    <AuthContext.Provider
      value={{ token, login, logout, isAuthenticated: Boolean(token) }}
    >
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const context = useContext(AuthContext)

  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider')
  }

  return context
}
