export default function ConfirmDialog({ title, message, confirmLabel, onConfirm, onCancel, isSubmitting }) {
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-950/45 p-4 backdrop-blur-sm">
      <section
        className="card-surface w-full max-w-sm p-6"
        role="dialog"
        aria-modal="true"
        aria-labelledby="confirm-title"
      >
        <h2 id="confirm-title" className="text-xl font-semibold text-slate-900">
          {title}
        </h2>
        <p className="mt-3 text-sm text-slate-600">{message}</p>
        <div className="mt-6 flex justify-end gap-3">
          <button
            type="button"
            onClick={onCancel}
            disabled={isSubmitting}
            className="rounded-full border border-slate-300 px-4 py-2 text-sm font-semibold text-slate-700 transition duration-200 hover:bg-slate-50 disabled:cursor-not-allowed"
          >
            Cancel
          </button>
          <button
            type="button"
            onClick={onConfirm}
            disabled={isSubmitting}
            className="rounded-full bg-red-600 px-4 py-2 text-sm font-semibold text-white transition duration-200 hover:-translate-y-0.5 hover:bg-red-700 disabled:cursor-not-allowed disabled:bg-red-400"
          >
            {isSubmitting ? 'Deleting...' : confirmLabel}
          </button>
        </div>
      </section>
    </div>
  )
}
