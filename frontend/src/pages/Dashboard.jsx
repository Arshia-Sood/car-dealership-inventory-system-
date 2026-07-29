import { useEffect, useState } from 'react'

import api from '../api/axios.js'
import VehicleCard from '../components/VehicleCard.jsx'
import { getApiErrorMessage } from '../utils/apiError.js'

export default function Dashboard() {
  const [vehicles, setVehicles] = useState([])
  const [error, setError] = useState('')
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    async function loadVehicles() {
      try {
        const response = await api.get('/vehicles')
        setVehicles(response.data)
      } catch (requestError) {
        setError(getApiErrorMessage(requestError, 'Unable to load vehicles. Please try again.'))
      } finally {
        setIsLoading(false)
      }
    }

    loadVehicles()
  }, [])

  return (
    <section>
      <div className="flex flex-col gap-1 sm:flex-row sm:items-end sm:justify-between">
        <div>
          <h1 className="text-3xl font-bold text-slate-900">Vehicle Dashboard</h1>
          <p className="mt-2 text-slate-600">Browse the current dealership inventory.</p>
        </div>
      </div>

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
            <VehicleCard key={vehicle.id} vehicle={vehicle} />
          ))}
        </div>
      )}
    </section>
  )
}
