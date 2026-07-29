import { Navigate, useLocation, useNavigate } from 'react-router-dom'
import { useState } from 'react'

import api from '../api/axios.js'
import { useAuth } from '../context/AuthContext.jsx'
import { useToast } from '../context/ToastContext.jsx'
import { getApiErrorMessage } from '../utils/apiError.js'

const initialForm = { email: '', password: '' }

export default function Login() {
  const [form, setForm] = useState(initialForm)
  const [error, setError] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const { isAuthenticated, login } = useAuth()
  const location = useLocation()
  const navigate = useNavigate()
  const { pushToast } = useToast()

  if (isAuthenticated) {
    return <Navigate to="/" replace />
  }

  function handleChange(event) {
    const { name, value } = event.target
    setForm((currentForm) => ({ ...currentForm, [name]: value }))
  }

  async function handleSubmit(event) {
    event.preventDefault()
    setError('')

    if (!form.email.trim() || !form.password) {
      setError('Email and password are required.')
      return
    }

    setIsLoading(true)
    try {
      const response = await api.post('/auth/login', form)
      login(response.data.access_token)
      pushToast('Welcome back! You are signed in.', 'success')
      navigate('/', { replace: true })
    } catch (requestError) {
      setError(getApiErrorMessage(requestError, 'Unable to sign in. Please try again.'))
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <section className="card-surface mx-auto w-full max-w-md p-6 sm:p-8">
      <div className="flex items-center gap-3">
        <span className="flex size-10 items-center justify-center rounded-full bg-blue-600 text-sm font-semibold text-white shadow-sm">
          CD
        </span>
        <div>
          <h1 className="text-2xl font-bold text-slate-900">Login</h1>
          <p className="mt-1 text-sm text-slate-600">Sign in to access the dealership dashboard.</p>
        </div>
      </div>

      {location.state?.message && (
        <p className="mt-4 rounded-md bg-emerald-50 px-3 py-2 text-sm text-emerald-700" role="status">
          {location.state.message}
        </p>
      )}
      {error && (
        <p className="mt-4 rounded-md bg-red-50 px-3 py-2 text-sm text-red-700" role="alert">
          {error}
        </p>
      )}

      <form className="mt-6 space-y-4" onSubmit={handleSubmit} noValidate>
        <label className="block text-sm font-medium text-slate-700">
          Email
          <input
            name="email"
            type="email"
            value={form.email}
            onChange={handleChange}
            className="mt-1 w-full rounded-md border border-slate-300 px-3 py-2 outline-none transition focus:border-blue-500 focus:ring-2 focus:ring-blue-100"
            autoComplete="email"
          />
        </label>
        <label className="block text-sm font-medium text-slate-700">
          Password
          <input
            name="password"
            type="password"
            value={form.password}
            onChange={handleChange}
            className="mt-1 w-full rounded-md border border-slate-300 px-3 py-2 outline-none transition focus:border-blue-500 focus:ring-2 focus:ring-blue-100"
            autoComplete="current-password"
          />
        </label>
        <button
          type="submit"
          disabled={isLoading}
          className="w-full rounded-full bg-blue-600 px-4 py-2.5 font-semibold text-white transition duration-200 hover:-translate-y-0.5 hover:bg-blue-700 disabled:cursor-not-allowed disabled:bg-blue-400"
        >
          {isLoading ? 'Signing in…' : 'Login'}
        </button>
      </form>
    </section>
  )
}
