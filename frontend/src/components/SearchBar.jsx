export default function SearchBar({ filters, onChange, onSearch, onClear }) {
  function handleChange(event) {
    const { name, value } = event.target
    onChange({ ...filters, [name]: value })
  }

  return (
    <form
      className="mt-6 grid gap-4 rounded-xl bg-white p-4 shadow-sm ring-1 ring-slate-200 md:grid-cols-3"
      onSubmit={onSearch}
    >
      <label className="text-sm font-medium text-slate-700">
        Make
        <input
          name="make"
          value={filters.make}
          onChange={handleChange}
          className="mt-1 w-full rounded-md border border-slate-300 px-3 py-2 outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-100"
        />
      </label>
      <label className="text-sm font-medium text-slate-700">
        Model
        <input
          name="model"
          value={filters.model}
          onChange={handleChange}
          className="mt-1 w-full rounded-md border border-slate-300 px-3 py-2 outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-100"
        />
      </label>
      <label className="text-sm font-medium text-slate-700">
        Category
        <input
          name="category"
          value={filters.category}
          onChange={handleChange}
          className="mt-1 w-full rounded-md border border-slate-300 px-3 py-2 outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-100"
        />
      </label>
      <label className="text-sm font-medium text-slate-700">
        Minimum Price
        <input
          name="minPrice"
          type="number"
          min="0"
          step="0.01"
          value={filters.minPrice}
          onChange={handleChange}
          className="mt-1 w-full rounded-md border border-slate-300 px-3 py-2 outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-100"
        />
      </label>
      <label className="text-sm font-medium text-slate-700">
        Maximum Price
        <input
          name="maxPrice"
          type="number"
          min="0"
          step="0.01"
          value={filters.maxPrice}
          onChange={handleChange}
          className="mt-1 w-full rounded-md border border-slate-300 px-3 py-2 outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-100"
        />
      </label>
      <div className="flex items-end gap-3">
        <button
          type="submit"
          className="rounded-md bg-blue-600 px-4 py-2 text-sm font-medium text-white transition hover:bg-blue-700"
        >
          Search
        </button>
        <button
          type="button"
          onClick={onClear}
          className="rounded-md border border-slate-300 px-4 py-2 text-sm font-medium text-slate-700 transition hover:bg-slate-50"
        >
          Clear filters
        </button>
      </div>
    </form>
  )
}
