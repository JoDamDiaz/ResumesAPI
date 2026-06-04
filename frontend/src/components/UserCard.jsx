// ── [FRONTEND] Componente · UserCard ──────────────────────────────────────────
import { useNavigate } from 'react-router-dom'

const AVATAR_COLORS = ['#3b82f6','#10b981','#f59e0b','#8b5cf6','#ef4444','#06b6d4','#ec4899','#14b8a6','#f97316','#6366f1']

function getColor(name) { return AVATAR_COLORS[name.charCodeAt(0) % AVATAR_COLORS.length] }
function getInitials(name) { return name.split(' ').slice(0, 2).map(n => n[0]).join('').toUpperCase() }

export default function UserCard({ user }) {
  const navigate = useNavigate()
  const currentJob = user.experiencias?.[0]

  return (
    <div className="user-card">
      <div className="user-card-header">
        <div className="avatar" style={{ background: getColor(user.nombre) }}>
          {getInitials(user.nombre)}
        </div>
        <div>
          <div className="user-card-name">{user.nombre}</div>
          <div className="user-card-job">
            {currentJob ? `${currentJob.cargo} @ ${currentJob.empresa}` : 'Sin experiencia registrada'}
          </div>
        </div>
      </div>

      <div className="user-card-meta">
        {user.ubicacion && <span>📍 {user.ubicacion}</span>}
        <span>✉️ {user.correo}</span>
        {user.telefono && <span>📞 {user.telefono}</span>}
      </div>

      {(user.linkedin || user.github) && (
        <div className="user-card-links">
          {user.linkedin && (
            <a href={`https://${user.linkedin.replace(/^https?:\/\//, '')}`} target="_blank" rel="noreferrer">
              🔗 LinkedIn
            </a>
          )}
          {user.github && (
            <a href={`https://${user.github.replace(/^https?:\/\//, '')}`} target="_blank" rel="noreferrer">
              🐙 GitHub
            </a>
          )}
        </div>
      )}

      <div className="user-card-footer">
        <button className="btn btn-primary btn-sm" onClick={() => navigate(`/usuarios/${user.user_id}`)}>
          Ver perfil →
        </button>
      </div>
    </div>
  )
}
