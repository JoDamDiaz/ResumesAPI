// ── [FRONTEND] Componente · Navbar ────────────────────────────────────────────
import { NavLink, useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'

const AVATAR_COLORS = ['#3b82f6','#10b981','#f59e0b','#8b5cf6','#ef4444','#06b6d4']
const getColor = name => AVATAR_COLORS[name.charCodeAt(0) % AVATAR_COLORS.length]
const getInitials = name => name.split(' ').slice(0, 2).map(n => n[0]).join('').toUpperCase()

export default function Navbar() {
  const { user, logout } = useAuth()
  const navigate = useNavigate()

  function handleLogout() {
    logout()
    navigate('/login')
  }

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

        {user && (
          <div className="navbar-user">
            <div
              className="navbar-avatar"
              style={{ background: getColor(user.nombre) }}
              title={user.nombre}
            >
              {getInitials(user.nombre)}
            </div>
            <span className="navbar-username">{user.nombre.split(' ')[0]}</span>
            <span className={`role-badge role-${user.role}`}>{user.role}</span>
            <button className="btn btn-ghost btn-sm" onClick={handleLogout} title="Cerrar sesión">
              Salir →
            </button>
          </div>
        )}
      </div>
    </nav>
  )
}
