// ── [FRONTEND] Página · Lista de usuarios ─────────────────────────────────────
import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { getUsers } from '../api/users'
import { useAuth } from '../context/AuthContext'
import UserCard from '../components/UserCard'

export default function HomePage() {
  const [users, setUsers] = useState([])
  const [query, setQuery] = useState('')
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const navigate = useNavigate()
  const { user: authUser } = useAuth()
  const canCreate = authUser?.role !== 'auditor'

  useEffect(() => {
    getUsers()
      .then(data => setUsers(data))
      .catch(e => setError(e.message))
      .finally(() => setLoading(false))
  }, [])

  const filtered = users.filter(u =>
    u.nombre.toLowerCase().includes(query.toLowerCase()) ||
    u.correo.toLowerCase().includes(query.toLowerCase()) ||
    (u.ubicacion ?? '').toLowerCase().includes(query.toLowerCase())
  )

  return (
    <>
      <div className="page-header">
        <h1 className="page-title">Usuarios <span className="badge badge-blue">{users.length}</span></h1>
        <div className="search-bar">
          <span className="search-icon">🔍</span>
          <input
            placeholder="Buscar por nombre, correo o ciudad…"
            value={query}
            onChange={e => setQuery(e.target.value)}
          />
        </div>
        {canCreate && (
          <button className="btn btn-primary" onClick={() => navigate('/usuarios/nuevo')}>
            + Nuevo usuario
          </button>
        )}
      </div>

      {loading && <div className="spinner" />}

      {error && <div className="form-error">⚠ {error}</div>}

      {!loading && filtered.length === 0 && (
        <div className="empty-state">
          <div className="empty-icon">🗂</div>
          {query ? 'Sin resultados para tu búsqueda.' : 'No hay usuarios registrados aún.'}
        </div>
      )}

      <div className="users-grid">
        {filtered.map(u => <UserCard key={u.user_id} user={u} />)}
      </div>
    </>
  )
}
