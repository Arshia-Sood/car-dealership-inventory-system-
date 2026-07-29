import { createContext, useContext, useMemo, useState } from 'react'

import ToastContainer from '../components/ToastContainer.jsx'

const ToastContext = createContext(null)

let toastId = 0

export function ToastProvider({ children }) {
  const [toasts, setToasts] = useState([])

  function pushToast(message, tone = 'info', duration = 4000) {
    const id = ++toastId
    setToasts((currentToasts) => [...currentToasts, { id, message, tone }])

    window.setTimeout(() => {
      setToasts((currentToasts) => currentToasts.filter((toast) => toast.id !== id))
    }, duration)
  }

  const value = useMemo(() => ({ pushToast }), [])

  return (
    <ToastContext.Provider value={value}>
      {children}
      <ToastContainer toasts={toasts} />
    </ToastContext.Provider>
  )
}

export function useToast() {
  const context = useContext(ToastContext)

  if (!context) {
    throw new Error('useToast must be used within a ToastProvider')
  }

  return context
}
