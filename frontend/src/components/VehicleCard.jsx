export default function VehicleCard({ vehicle, onPurchase, children }) {
  const formattedPrice = new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
  }).format(vehicle.price)
  const isOutOfStock = vehicle.quantity_in_stock === 0

  return (
    <article className="card-surface group flex h-full flex-col p-5 transition duration-200 hover:-translate-y-1 hover:shadow-xl">
      <div className="flex items-start justify-between gap-3">
        <div>
          <p className="text-sm font-semibold uppercase tracking-[0.25em] text-blue-600">{vehicle.category}</p>
          <h2 className="mt-1 text-xl font-semibold text-slate-900">
            {vehicle.make} {vehicle.model}
          </h2>
        </div>
        <span className={`rounded-full px-2.5 py-1 text-xs font-semibold ${isOutOfStock ? 'bg-slate-100 text-slate-600' : 'bg-emerald-100 text-emerald-700'}`}>
          {isOutOfStock ? 'Sold out' : 'In stock'}
        </span>
      </div>
      <dl className="mt-5 grid grid-cols-2 gap-4 border-t border-slate-100 pt-4 text-sm">
        <div>
          <dt className="text-slate-500">Price</dt>
          <dd className="mt-1 font-semibold text-slate-900">{formattedPrice}</dd>
        </div>
        <div>
          <dt className="text-slate-500">Quantity</dt>
          <dd className="mt-1 font-semibold text-slate-900">{vehicle.quantity_in_stock}</dd>
        </div>
      </dl>
      {onPurchase && (
        <button
          type="button"
          onClick={() => onPurchase(vehicle)}
          disabled={isOutOfStock}
          className="mt-5 w-full rounded-full bg-blue-600 px-4 py-2.5 text-sm font-semibold text-white transition duration-200 hover:-translate-y-0.5 hover:bg-blue-700 disabled:cursor-not-allowed disabled:bg-slate-300"
        >
          {isOutOfStock ? 'Out of Stock' : 'Purchase'}
        </button>
      )}
      {children}
    </article>
  )
}
