import { useEffect, useState } from 'react'

import api from '../api/axios.js'
import PurchaseModal from '../components/PurchaseModal.jsx'
import SearchBar from '../components/SearchBar.jsx'
import VehicleCard from '../components/VehicleCard.jsx'
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
  const [notice, setNotice] = useState('')
  const [isLoading, setIsLoading] = useState(true)
  const [selectedVehicle, setSelectedVehicle] = useState(null)

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
    setNotice('')

    if (
      filters.minPrice !== '' &&
      filters.maxPrice !== '' &&
      Number(filters.minPrice) > Number(filters.maxPrice)
    ) {
      setError('Minimum price cannot be greater than maximum price.')
      return
    }

    setActiveFilters({ ...filters })
  }

  function handleClear() {
    setFilters(emptyFilters)
    setActiveFilters(emptyFilters)
    setNotice('')
  }

  async function handlePurchaseSuccess() {
    setNotice('Purchase completed successfully.')
    await loadVehicles(activeFilters)
  }

  return (
    <section>
      <div>
        <h1 className="text-3xl font-bold text-slate-900">Vehicle Dashboard</h1>
        <p className="mt-2 text-slate-600">Browse the current dealership inventory.</p>
      </div>

      <SearchBar
        filters={filters}
        onChange={setFilters}
        onSearch={handleSearch}
        onClear={handleClear}
      />

      {notice && (
        <p className="mt-6 rounded-md bg-emerald-50 px-4 py-3 text-sm text-emerald-700" role="status">
          {notice}
        </p>
      )}

      {isLoading && (
        <div className="flex min-h-52 items-center justify-center" role="status">
          <span className="size-8 animate-spin rounded-full border-4 border-slate-200 border-t-blue-600" />
          <span className="sr-only">Loading vehicles</span>
        </div>
      )}

      {!isLoading && error && (
        <p className="mt-6 rounded-md bg-red-50 px-4 py-3 text-sm text-red-700" role="alert">
          {error}
        </p>
      )}

      {!isLoading && !error && vehicles.length === 0 && (
        <p className="mt-6 rounded-md bg-white px-4 py-8 text-center text-slate-600 shadow-sm ring-1 ring-slate-200">
          No vehicles available.
        </p>
      )}

      {!isLoading && !error && vehicles.length > 0 && (
        <div className="mt-6 grid gap-5 sm:grid-cols-2 lg:grid-cols-3">
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
