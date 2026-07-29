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
      className="fixed inset-0 z-50 flex items-center justify-center bg-slate-950/45 p-4 backdrop-blur-sm"
      role="presentation"
    >
      <section
        className="card-surface w-full max-w-sm p-6"
        role="dialog"
        aria-modal="true"
        aria-labelledby="purchase-title"
      >
        <div className="flex items-start justify-between gap-3">
          <div>
            <p className="text-sm font-semibold uppercase tracking-[0.25em] text-blue-600">Purchase</p>
            <h2 id="purchase-title" className="text-xl font-semibold text-slate-900">
              {vehicle.make} {vehicle.model}
            </h2>
          </div>
          <div className="rounded-full bg-emerald-50 px-2.5 py-1 text-xs font-semibold text-emerald-700">
            {vehicle.quantity_in_stock} in stock
          </div>
        </div>
        <p className="mt-3 text-sm text-slate-600">
          Choose the quantity to purchase and confirm the order instantly.
        </p>

        {error && (
          <p className="mt-4 rounded-xl border border-rose-200 bg-rose-50 px-3 py-2 text-sm text-rose-700" role="alert">
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
              className="mt-1 w-full rounded-xl border border-slate-300 px-3 py-2 outline-none transition focus:border-blue-500 focus:ring-2 focus:ring-blue-100"
              autoFocus
            />
          </label>
          <div className="flex justify-end gap-3">
            <button
              type="button"
              onClick={onClose}
              disabled={isSubmitting}
              className="rounded-full border border-slate-300 px-4 py-2 text-sm font-semibold text-slate-700 transition duration-200 hover:bg-slate-50 disabled:cursor-not-allowed"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={isSubmitting}
              className="rounded-full bg-blue-600 px-4 py-2 text-sm font-semibold text-white transition duration-200 hover:-translate-y-0.5 hover:bg-blue-700 disabled:cursor-not-allowed disabled:bg-blue-400"
            >
              {isSubmitting ? 'Purchasing…' : 'Purchase'}
            </button>
          </div>
        </form>
      </section>
    </div>
  )
}
