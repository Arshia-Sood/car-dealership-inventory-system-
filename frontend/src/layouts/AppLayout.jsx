import { Outlet } from 'react-router-dom'

import Navbar from '../components/Navbar.jsx'

export default function AppLayout() {
  return (
    <div className="min-h-screen bg-transparent">
      <Navbar />
      <main className="mx-auto flex w-full max-w-6xl flex-col px-4 py-6 sm:px-6 sm:py-8 lg:px-8 lg:py-10">
        <Outlet />
      </main>
    </div>
  )
}
