import { useState } from 'react'

function createInitialForm(vehicle) {
  return {
    make: vehicle?.make ?? '',
    model: vehicle?.model ?? '',
    category: vehicle?.category ?? '',
    price: vehicle?.price?.toString() ?? '',
    quantity_in_stock: vehicle?.quantity_in_stock?.toString() ?? '',
  }
}

export default function VehicleForm({ vehicle, onSubmit, onCancel, isSubmitting }) {
  const [form, setForm] = useState(() => createInitialForm(vehicle))
  const [error, setError] = useState('')
  const isEditing = Boolean(vehicle)

  function handleChange(event) {
    const { name, value } = event.target
    setForm((currentForm) => ({ ...currentForm, [name]: value }))
  }

  async function handleSubmit(event) {
    event.preventDefault()
    const price = Number(form.price)
    const quantity = Number(form.quantity_in_stock)
    setError('')

    if (!form.make.trim() || !form.model.trim() || !form.category.trim()) {
      setError('Make, model, and category are required.')
      return
    }
    if (!Number.isFinite(price) || price <= 0) {
      setError('Price must be greater than zero.')
      return
    }
    if (!Number.isInteger(quantity) || quantity < 0) {
      setError('Quantity in stock must be a whole number of zero or more.')
      return
    }

    const succeeded = await onSubmit({
      make: form.make.trim(),
      model: form.model.trim(),
      category: form.category.trim(),
      price,
      quantity_in_stock: quantity,
    })

    if (succeeded && !isEditing) {
      setForm(createInitialForm())
    }
  }

  return (
    <section className="card-surface p-5 sm:p-6">
      <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <p className="text-sm font-semibold uppercase tracking-[0.25em] text-blue-600">
            {isEditing ? 'Update' : 'Create'}
          </p>
          <h2 className="text-xl font-semibold text-slate-900">
            {isEditing ? 'Edit Vehicle' : 'Add Vehicle'}
          </h2>
        </div>
        {isEditing && (
          <button
            type="button"
            onClick={onCancel}
            className="text-sm font-semibold text-slate-600 transition hover:text-slate-900"
          >
            Cancel edit
          </button>
        )}
      </div>

      {error && (
        <p className="mt-4 rounded-xl border border-rose-200 bg-rose-50 px-3 py-2 text-sm text-rose-700" role="alert">
          {error}
        </p>
      )}

      <form className="mt-5 grid gap-4 md:grid-cols-2" onSubmit={handleSubmit} noValidate>
        <label className="text-sm font-medium text-slate-700">
          Make
          <input
            name="make"
            value={form.make}
            onChange={handleChange}
            className="mt-1 w-full rounded-md border border-slate-300 px-3 py-2 outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-100"
          />
        </label>
        <label className="text-sm font-medium text-slate-700">
          Model
          <input
            name="model"
            value={form.model}
            onChange={handleChange}
            className="mt-1 w-full rounded-md border border-slate-300 px-3 py-2 outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-100"
          />
        </label>
        <label className="text-sm font-medium text-slate-700">
          Category
          <input
            name="category"
            value={form.category}
            onChange={handleChange}
            className="mt-1 w-full rounded-md border border-slate-300 px-3 py-2 outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-100"
          />
        </label>
        <label className="text-sm font-medium text-slate-700">
          Price
          <input
            name="price"
            type="number"
            min="0.01"
            step="0.01"
            value={form.price}
            onChange={handleChange}
            className="mt-1 w-full rounded-md border border-slate-300 px-3 py-2 outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-100"
          />
        </label>
        <label className="text-sm font-medium text-slate-700">
          Quantity in Stock
          <input
            name="quantity_in_stock"
            type="number"
            min="0"
            step="1"
            value={form.quantity_in_stock}
            onChange={handleChange}
            className="mt-1 w-full rounded-md border border-slate-300 px-3 py-2 outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-100"
          />
        </label>
        <div className="flex items-end">
          <button
            type="submit"
            disabled={isSubmitting}
            className="w-full rounded-full bg-blue-600 px-4 py-2.5 font-semibold text-white transition duration-200 hover:-translate-y-0.5 hover:bg-blue-700 disabled:cursor-not-allowed disabled:bg-blue-400"
          >
            {isSubmitting ? 'Saving...' : isEditing ? 'Save Changes' : 'Add Vehicle'}
          </button>
        </div>
      </form>
    </section>
  )
}
