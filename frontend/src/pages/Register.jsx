import { Navigate, useNavigate } from 'react-router-dom'
import { useState } from 'react'

import api from '../api/axios.js'
import { useAuth } from '../context/AuthContext.jsx'
import { getApiErrorMessage } from '../utils/apiError.js'

const initialForm = { email: '', username: '', password: '' }

export default function Register() {
  const [form, setForm] = useState(initialForm)
  const [error, setError] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const { isAuthenticated } = useAuth()
  const navigate = useNavigate()

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

    if (!form.email.trim() || !form.username.trim() || !form.password) {
      setError('Email, username, and password are required.')
      return
    }

    setIsLoading(true)
    try {
      await api.post('/auth/register', form)
      navigate('/login', {
        replace: true,
        state: { message: 'Registration successful. Please log in.' },
      })
    } catch (requestError) {
      setError(getApiErrorMessage(requestError, 'Unable to register. Please try again.'))
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <section className="mx-auto w-full max-w-md rounded-xl bg-white p-6 shadow-sm ring-1 ring-slate-200 sm:p-8">
      <h1 className="text-2xl font-bold text-slate-900">Register</h1>
      <p className="mt-2 text-sm text-slate-600">Create an account for the dealership system.</p>

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
          Username
          <input
            name="username"
            type="text"
            value={form.username}
            onChange={handleChange}
            className="mt-1 w-full rounded-md border border-slate-300 px-3 py-2 outline-none transition focus:border-blue-500 focus:ring-2 focus:ring-blue-100"
            autoComplete="username"
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
            autoComplete="new-password"
          />
        </label>
        <button
          type="submit"
          disabled={isLoading}
          className="w-full rounded-md bg-blue-600 px-4 py-2 font-medium text-white transition hover:bg-blue-700 disabled:cursor-not-allowed disabled:bg-blue-400"
        >
          {isLoading ? 'Creating account…' : 'Register'}
        </button>
      </form>
    </section>
  )
}
