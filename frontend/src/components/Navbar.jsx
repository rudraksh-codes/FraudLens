import { NavLink } from 'react-router-dom'
import './Navbar.css'

export default function Navbar() {
  return (
    <header className="navbar">
      <div className="app-shell navbar-inner">
        <NavLink to="/" className="navbar-brand">
          <span className="navbar-brand-mark" aria-hidden="true" />
          <span>
            FraudLens<span className="navbar-brand-dot">.</span>
          </span>
        </NavLink>

        <nav className="navbar-links" aria-label="Primary">
          <NavLink
            to="/"
            end
            className={({ isActive }) => `navbar-link${isActive ? ' is-active' : ''}`}
          >
            Checker
          </NavLink>
          <NavLink
            to="/dashboard"
            className={({ isActive }) => `navbar-link${isActive ? ' is-active' : ''}`}
          >
            Dashboard
          </NavLink>
          <NavLink
            to="/about"
            className={({ isActive }) => `navbar-link${isActive ? ' is-active' : ''}`}
          >
            About
          </NavLink>
        </nav>
      </div>
    </header>
  )
}
