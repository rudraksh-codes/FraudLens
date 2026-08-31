import { Routes, Route } from 'react-router-dom'
import Navbar from './components/Navbar'
import Checker from './pages/Checker'
import Dashboard from './pages/Dashboard'
import About from './pages/About'

export default function App() {
  return (
    <>
      <Navbar />
      <main className="app-shell">
        <Routes>
          <Route path="/" element={<Checker />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/about" element={<About />} />
        </Routes>
      </main>
    </>
  )
}
