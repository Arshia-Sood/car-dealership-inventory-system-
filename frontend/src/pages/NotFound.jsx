export default function NotFound() {
  return (
    <div className="card-surface mx-auto flex max-w-xl flex-col items-center justify-center gap-4 p-10 text-center">
      <div className="rounded-full bg-slate-100 px-3 py-1 text-sm font-semibold uppercase tracking-[0.25em] text-slate-500">
        404
      </div>
      <h1 className="text-3xl font-bold text-slate-900">Page not found</h1>
      <p className="text-sm text-slate-600">
        The route you’re looking for doesn’t exist or may have moved.
      </p>
    </div>
  )
}
