import { useState } from 'react'

import api from '../api/axios.js'
import { getApiErrorMessage } from '../utils/apiError.js'

export default function PurchaseModal({ vehicle, onClose, onSuccess }) {
  const [quantity, setQuantity] = useState('1')
  const [error, setError] = useState('')
  const [isSubmitting, setIsSubmitting] = useState(false)

  async function handleSubmit(event) {
    event.preventDefault()
    const purchaseQuantity = Number(quantity)
    setError('')

    if (!Number.isInteger(purchaseQuantity) || purchaseQuantity <= 0) {
      setError('Purchase quantity must be a whole number greater than zero.')
      return
    }

    setIsSubmitting(true)
    try {
      await api.post(`/vehicles/${vehicle.id}/purchase`, { quantity: purchaseQuantity })
      await onSuccess()
      onClose()
    } catch (requestError) {
      setError(getApiErrorMessage(requestError, 'Unable to complete the purchase.'))
    } finally {
      setIsSubmitting(false)
    }
  }

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center bg-slate-950/40 p-4"
      role="presentation"
    >
      <section
        className="w-full max-w-sm rounded-xl bg-white p-6 shadow-xl"
        role="dialog"
        aria-modal="true"
        aria-labelledby="purchase-title"
      >
        <h2 id="purchase-title" className="text-xl font-semibold text-slate-900">
          Purchase {vehicle.make} {vehicle.model}
        </h2>
        <p className="mt-2 text-sm text-slate-600">
          {vehicle.quantity_in_stock} vehicle(s) currently in stock.
        </p>

        {error && (
          <p className="mt-4 rounded-md bg-red-50 px-3 py-2 text-sm text-red-700" role="alert">
            {error}
          </p>
        )}

        <form className="mt-5 space-y-5" onSubmit={handleSubmit} noValidate>
          <label className="block text-sm font-medium text-slate-700">
            Quantity
            <input
              type="number"
              min="1"
              step="1"
              value={quantity}
              onChange={(event) => setQuantity(event.target.value)}
              className="mt-1 w-full rounded-md border border-slate-300 px-3 py-2 outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-100"
              autoFocus
            />
          </label>
          <div className="flex justify-end gap-3">
            <button
              type="button"
              onClick={onClose}
              disabled={isSubmitting}
              className="rounded-md border border-slate-300 px-4 py-2 text-sm font-medium text-slate-700 disabled:cursor-not-allowed"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={isSubmitting}
              className="rounded-md bg-blue-600 px-4 py-2 text-sm font-medium text-white transition hover:bg-blue-700 disabled:cursor-not-allowed disabled:bg-blue-400"
            >
              {isSubmitting ? 'Purchasing…' : 'Purchase'}
            </button>
          </div>
        </form>
      </section>
    </div>
  )
}
