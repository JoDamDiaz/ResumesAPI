// ── [FRONTEND] Componente · Navbar ────────────────────────────────────────────
import { NavLink } from 'react-router-dom'

export default function Navbar() {
  return (
    <nav className="navbar">
      <div className="navbar-inner">
        <NavLink to="/" className="navbar-brand">
          <span>📄</span> Resumes API
        </NavLink>
        <div className="navbar-links">
          <NavLink to="/" end>Usuarios</NavLink>
          <NavLink to="/usuarios/nuevo">+ Nuevo</NavLink>
        </div>
      </div>
    </nav>
  )
}
