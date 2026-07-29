import { useEffect, useState } from 'react'

import api from '../api/axios.js'
import PurchaseModal from '../components/PurchaseModal.jsx'
import SearchBar from '../components/SearchBar.jsx'
import VehicleCard from '../components/VehicleCard.jsx'
import { useToast } from '../context/ToastContext.jsx'
import { getApiErrorMessage } from '../utils/apiError.js'

const emptyFilters = {
  make: '',
  model: '',
  category: '',
  minPrice: '',
  maxPrice: '',
}

function applyPriceFilters(vehicles, filters) {
  return vehicles.filter((vehicle) => {
    const price = Number(vehicle.price)
    const meetsMinimum = filters.minPrice === '' || price >= Number(filters.minPrice)
    const meetsMaximum = filters.maxPrice === '' || price <= Number(filters.maxPrice)

    return meetsMinimum && meetsMaximum
  })
}

export default function Dashboard() {
  const [vehicles, setVehicles] = useState([])
  const [filters, setFilters] = useState(emptyFilters)
  const [activeFilters, setActiveFilters] = useState(emptyFilters)
  const [error, setError] = useState('')
  const [isLoading, setIsLoading] = useState(true)
  const [selectedVehicle, setSelectedVehicle] = useState(null)
  const { pushToast } = useToast()

  async function loadVehicles(searchFilters) {
    setIsLoading(true)
    setError('')

    const params = Object.fromEntries(
      Object.entries(searchFilters)
        .filter(([key, value]) => ['make', 'model', 'category'].includes(key) && value.trim())
        .map(([key, value]) => [key, value.trim()]),
    )

    try {
      const response = await api.get('/vehicles/search', { params })
      setVehicles(applyPriceFilters(response.data, searchFilters))
    } catch (requestError) {
      setError(getApiErrorMessage(requestError, 'Unable to load vehicles. Please try again.'))
    } finally {
      setIsLoading(false)
    }
  }

  useEffect(() => {
    loadVehicles(activeFilters)
  }, [activeFilters])

  function handleSearch(event) {
    event.preventDefault()

    if (
      filters.minPrice !== '' &&
      filters.maxPrice !== '' &&
      Number(filters.minPrice) > Number(filters.maxPrice)
    ) {
      setError('Minimum price cannot be greater than maximum price.')
      return
    }

    setActiveFilters({ ...filters })
    pushToast('Search filters applied.', 'info', 2500)
  }

  function handleClear() {
    setFilters(emptyFilters)
    setActiveFilters(emptyFilters)
    pushToast('Filters cleared.', 'info', 2500)
  }

  async function handlePurchaseSuccess() {
    pushToast('Purchase completed successfully.', 'success')
    await loadVehicles(activeFilters)
  }

  return (
    <section className="flex flex-col gap-6">
      <div className="card-surface overflow-hidden p-6 sm:p-8">
        <div className="flex flex-col gap-2 sm:flex-row sm:items-end sm:justify-between">
          <div>
            <p className="text-sm font-semibold uppercase tracking-[0.3em] text-blue-600">Inventory</p>
            <h1 className="text-3xl font-bold tracking-tight text-slate-900 sm:text-4xl">
              Vehicle Dashboard
            </h1>
            <p className="mt-2 max-w-2xl text-sm text-slate-600 sm:text-base">
              Browse the current dealership inventory and manage purchases with a polished, responsive experience.
            </p>
          </div>
          <div className="rounded-full border border-slate-200 bg-slate-50 px-3 py-1 text-sm font-medium text-slate-700">
            {vehicles.length} vehicles shown
          </div>
        </div>
      </div>

      <SearchBar
        filters={filters}
        onChange={setFilters}
        onSearch={handleSearch}
        onClear={handleClear}
      />

      {isLoading && (
        <div className="card-surface flex min-h-72 items-center justify-center p-6" role="status">
          <div className="flex flex-col items-center gap-3 text-center">
            <span className="size-10 animate-spin rounded-full border-4 border-slate-200 border-t-blue-600" />
            <p className="text-sm font-medium text-slate-600">Loading vehicles…</p>
          </div>
        </div>
      )}

      {!isLoading && error && (
        <div className="card-surface border-rose-200 bg-rose-50/80 p-6 text-center" role="alert">
          <p className="text-lg font-semibold text-rose-700">We hit a snag</p>
          <p className="mt-2 text-sm text-rose-700/80">{error}</p>
        </div>
      )}

      {!isLoading && !error && vehicles.length === 0 && (
        <div className="card-surface flex flex-col items-center justify-center gap-3 p-10 text-center">
          <div className="rounded-full bg-slate-100 px-3 py-1 text-sm font-semibold uppercase tracking-[0.25em] text-slate-500">
            Empty state
          </div>
          <h2 className="text-xl font-semibold text-slate-900">No vehicles match your search</h2>
          <p className="max-w-md text-sm text-slate-600">
            Try adjusting your filters or clearing them to see the full inventory again.
          </p>
        </div>
      )}

      {!isLoading && !error && vehicles.length > 0 && (
        <div className="grid gap-5 sm:grid-cols-2 xl:grid-cols-3">
          {vehicles.map((vehicle) => (
            <VehicleCard key={vehicle.id} vehicle={vehicle} onPurchase={setSelectedVehicle} />
          ))}
        </div>
      )}

      {selectedVehicle && (
        <PurchaseModal
          vehicle={selectedVehicle}
          onClose={() => setSelectedVehicle(null)}
          onSuccess={handlePurchaseSuccess}
        />
      )}
    </section>
  )
}
