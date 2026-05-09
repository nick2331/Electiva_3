import { BrowserRouter, Routes, Route, NavLink } from 'react-router-dom'
import { Eye, History, LayoutDashboard } from 'lucide-react'
import HomePage from './pages/HomePage'
import ResultPage from './pages/ResultPage'
import HistoryPage from './pages/HistoryPage'
import AdminPage from './pages/AdminPage'

function NavBar() {
  const base = 'flex items-center gap-1.5 px-3 py-2 rounded-lg text-sm font-medium transition-colors'
  const active = 'bg-primary text-white'
  const inactive = 'text-gray-600 hover:bg-gray-100'

  return (
    <header className="bg-white border-b border-gray-200 sticky top-0 z-50">
      <div className="max-w-5xl mx-auto px-4 h-14 flex items-center justify-between">
        <NavLink to="/" className="flex items-center gap-2">
          <Eye className="text-primary" size={22} />
          <span className="font-bold text-primary text-lg tracking-tight">VehiclEye</span>
        </NavLink>
        <nav className="flex items-center gap-1">
          <NavLink
            to="/"
            end
            className={({ isActive }) => `${base} ${isActive ? active : inactive}`}
          >
            <Eye size={16} /> Analizar
          </NavLink>
          <NavLink
            to="/historial"
            className={({ isActive }) => `${base} ${isActive ? active : inactive}`}
          >
            <History size={16} /> Historial
          </NavLink>
          <NavLink
            to="/admin"
            className={({ isActive }) => `${base} ${isActive ? active : inactive}`}
          >
            <LayoutDashboard size={16} /> Admin
          </NavLink>
        </nav>
      </div>
    </header>
  )
}

export default function App() {
  return (
    <BrowserRouter>
      <NavBar />
      <main className="max-w-5xl mx-auto px-4 py-8">
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/resultado/:id" element={<ResultPage />} />
          <Route path="/historial" element={<HistoryPage />} />
          <Route path="/admin" element={<AdminPage />} />
        </Routes>
      </main>
    </BrowserRouter>
  )
}
