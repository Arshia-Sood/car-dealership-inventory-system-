import { Navigate, Outlet } from 'react-router-dom'

import { useAuth } from '../context/AuthContext.jsx'
import { isAdminToken } from '../utils/auth.js'

export default function AdminRoute() {
  const { token } = useAuth()

  return isAdminToken(token) ? <Outlet /> : <Navigate to="/" replace />
}
