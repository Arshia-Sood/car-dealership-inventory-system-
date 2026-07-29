export default function AdminDashboard() {
  return (
    <section className="flex flex-col gap-6">
      <div className="card-surface overflow-hidden p-6 sm:p-8">
        <p className="text-sm font-semibold uppercase tracking-[0.3em] text-blue-600">Admin panel</p>
        <h1 className="mt-2 text-3xl font-bold tracking-tight text-slate-900 sm:text-4xl">
          Manage the dealership inventory with confidence
        </h1>
        <p className="mt-3 max-w-2xl text-sm text-slate-600 sm:text-base">
          Use the main dashboard to review vehicles, update stock, and keep the catalog polished for buyers.
        </p>
      </div>
      <div className="grid gap-4 md:grid-cols-3">
        {[
          ['Inventory overview', 'Track live stock levels and pricing at a glance.'],
          ['Restock controls', 'Add inventory quickly without interrupting the flow.'],
          ['Customer ready', 'Every interaction now feels clearer and more responsive.'],
        ].map(([title, description]) => (
          <div key={title} className="card-surface p-5 transition duration-200 hover:-translate-y-1">
            <h2 className="text-lg font-semibold text-slate-900">{title}</h2>
            <p className="mt-2 text-sm text-slate-600">{description}</p>
          </div>
        ))}
      </div>
    </section>
  )
}
