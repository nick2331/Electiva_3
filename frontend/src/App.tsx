import { BrowserRouter, Routes, Route, NavLink } from 'react-router-dom'
import { Eye, History, LayoutDashboard } from 'lucide-react'
import HomePage from './pages/HomePage'
import ResultPage from './pages/ResultPage'
import HistoryPage from './pages/HistoryPage'
import AdminPage from './pages/AdminPage'

function NavBar() {
  const base = 'flex items-center gap-1.5 px-3 py-2 rounded-lg text-sm font-medium transition-all duration-200'
  const active = 'bg-white/20 text-white shadow-sm'
  const inactive = 'text-blue-100 hover:bg-white/10 hover:text-white'

  return (
    <header className="bg-gradient-to-r from-primary-dark via-primary to-primary-light sticky top-0 z-50 shadow-lg">
      <div className="max-w-5xl mx-auto px-4 h-14 flex items-center justify-between">
        <NavLink to="/" className="flex items-center gap-2 group">
          <div className="bg-white/20 rounded-lg p-1.5 group-hover:bg-white/30 transition-colors duration-200">
            <Eye className="text-white" size={20} />
          </div>
          <span className="font-bold text-white text-lg tracking-tight">
            Vehicl<span className="text-blue-200">Eye</span>
          </span>
        </NavLink>
        <nav className="flex items-center gap-1">
          <NavLink to="/" end className={({ isActive }) => `${base} ${isActive ? active : inactive}`}>
            <Eye size={15} /> Analizar
          </NavLink>
          <NavLink to="/historial" className={({ isActive }) => `${base} ${isActive ? active : inactive}`}>
            <History size={15} /> Historial
          </NavLink>
          <NavLink to="/admin" className={({ isActive }) => `${base} ${isActive ? active : inactive}`}>
            <LayoutDashboard size={15} /> Admin
          </NavLink>
        </nav>
      </div>
    </header>
  )
}

export default function App() {
  return (
    <BrowserRouter>
      <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50/30 to-slate-100">
        <NavBar />
        <main className="max-w-5xl mx-auto px-4 py-8">
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/resultado/:id" element={<ResultPage />} />
            <Route path="/historial" element={<HistoryPage />} />
            <Route path="/admin" element={<AdminPage />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  )
}
