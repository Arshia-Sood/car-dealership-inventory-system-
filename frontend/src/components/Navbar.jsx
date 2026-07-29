import { NavLink, useNavigate } from 'react-router-dom'

import { useAuth } from '../context/AuthContext.jsx'
import { isAdminToken } from '../utils/auth.js'

export default function Navbar() {
  const { isAuthenticated, logout, token } = useAuth()
  const navigate = useNavigate()
  const navigationLinks = isAuthenticated
    ? [
        { label: 'Dashboard', to: '/' },
        ...(isAdminToken(token) ? [{ label: 'Admin', to: '/admin' }] : []),
      ]
    : [
        { label: 'Login', to: '/login' },
        { label: 'Register', to: '/register' },
      ]

  function handleLogout() {
    logout()
    navigate('/login')
  }

  return (
    <nav className="border-b border-slate-200/80 bg-white/80 backdrop-blur" aria-label="Main navigation">
      <div className="mx-auto flex max-w-6xl flex-col gap-3 px-4 py-4 sm:flex-row sm:items-center sm:justify-between sm:px-6 lg:px-8">
        <NavLink to="/" className="flex items-center gap-3 text-lg font-semibold text-slate-900 transition hover:text-blue-600">
          <span className="flex size-9 items-center justify-center rounded-full bg-blue-600 text-sm font-semibold text-white shadow-sm">
            CD
          </span>
          <span>Car Dealership</span>
        </NavLink>
        <div className="flex flex-wrap items-center gap-2 text-sm font-medium text-slate-600">
          {navigationLinks.map(({ label, to }) => (
            <NavLink
              key={to}
              to={to}
              className={({ isActive }) =>
                `rounded-full px-3 py-2 transition ${
                  isActive
                    ? 'bg-blue-600 text-white shadow-sm'
                    : 'hover:bg-slate-100 hover:text-blue-600'
                }`
              }
            >
              {label}
            </NavLink>
          ))}
          {isAuthenticated && (
            <button
              type="button"
              onClick={handleLogout}
              className="rounded-full border border-slate-200 px-3 py-2 transition hover:border-blue-200 hover:bg-blue-50 hover:text-blue-600"
            >
              Logout
            </button>
          )}
        </div>
      </div>
    </nav>
  )
}
