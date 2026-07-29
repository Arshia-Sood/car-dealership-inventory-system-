import { NavLink, useNavigate } from 'react-router-dom'

import { useAuth } from '../context/AuthContext.jsx'

export default function Navbar() {
  const { isAuthenticated, logout } = useAuth()
  const navigate = useNavigate()
  const navigationLinks = isAuthenticated
    ? [{ label: 'Dashboard', to: '/' }]
    : [
        { label: 'Login', to: '/login' },
        { label: 'Register', to: '/register' },
      ]

  function handleLogout() {
    logout()
    navigate('/login')
  }

  return (
    <nav className="border-b border-slate-200 bg-white" aria-label="Main navigation">
      <div className="mx-auto flex max-w-6xl flex-col gap-3 px-4 py-4 sm:flex-row sm:items-center sm:justify-between sm:px-6">
        <NavLink to="/" className="text-lg font-semibold text-slate-900">
          Car Dealership
        </NavLink>
        <div className="flex flex-wrap gap-x-4 gap-y-2 text-sm font-medium text-slate-600">
          {navigationLinks.map(({ label, to }) => (
            <NavLink
              key={to}
              to={to}
              className={({ isActive }) =>
                isActive ? 'text-blue-600' : 'transition hover:text-blue-600'
              }
            >
              {label}
            </NavLink>
          ))}
          {isAuthenticated && (
            <button
              type="button"
              onClick={handleLogout}
              className="cursor-pointer transition hover:text-blue-600"
            >
              Logout
            </button>
          )}
        </div>
      </div>
    </nav>
  )
}
