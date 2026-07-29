export default function VehicleCard({ vehicle }) {
  const formattedPrice = new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
  }).format(vehicle.price)

  return (
    <article className="rounded-xl bg-white p-5 shadow-sm ring-1 ring-slate-200">
      <p className="text-sm font-medium text-blue-600">{vehicle.category}</p>
      <h2 className="mt-1 text-xl font-semibold text-slate-900">
        {vehicle.make} {vehicle.model}
      </h2>
      <dl className="mt-5 grid grid-cols-2 gap-4 border-t border-slate-100 pt-4 text-sm">
        <div>
          <dt className="text-slate-500">Price</dt>
          <dd className="mt-1 font-semibold text-slate-900">{formattedPrice}</dd>
        </div>
        <div>
          <dt className="text-slate-500">Quantity in Stock</dt>
          <dd className="mt-1 font-semibold text-slate-900">{vehicle.quantity_in_stock}</dd>
        </div>
      </dl>
    </article>
  )
}
