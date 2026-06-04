// ── [FRONTEND] Página · Detalle de usuario ────────────────────────────────────
import { useState, useEffect, useCallback } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { getUserById, deleteUser } from '../api/users'
import { createExperiencia, updateExperiencia, deleteExperiencia } from '../api/experiencias'
import ExperienceCard from '../components/ExperienceCard'
import ExperienceModal from '../components/ExperienceModal'
import ConfirmModal from '../components/ConfirmModal'

const AVATAR_COLORS = ['#3b82f6','#10b981','#f59e0b','#8b5cf6','#ef4444','#06b6d4','#ec4899','#14b8a6','#f97316','#6366f1']
const getColor = name => AVATAR_COLORS[name.charCodeAt(0) % AVATAR_COLORS.length]
const getInitials = name => name.split(' ').slice(0, 2).map(n => n[0]).join('').toUpperCase()

export default function UserDetailPage() {
  const { id } = useParams()
  const navigate = useNavigate()
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)

  // modales
  const [expModal, setExpModal]         = useState(null)   // null | 'create' | experiencia-obj
  const [deleteExpModal, setDeleteExpModal] = useState(null)
  const [deleteUserModal, setDeleteUserModal] = useState(false)
  const [deleting, setDeleting] = useState(false)

  // toast
  const [toast, setToast] = useState(null)
  const showToast = (msg, type = 'success') => {
    setToast({ msg, type })
    setTimeout(() => setToast(null), 3000)
  }

  const load = useCallback(() => {
    setLoading(true)
    getUserById(id)
      .then(setUser)
      .catch(() => navigate('/'))
      .finally(() => setLoading(false))
  }, [id, navigate])

  useEffect(() => { load() }, [load])

  async function handleSaveExp(payload, expId) {
    if (expId) {
      const { funciones: _, user_id: __, ...fields } = payload
      await updateExperiencia(expId, fields)
      showToast('Experiencia actualizada')
    } else {
      await createExperiencia(payload)
      showToast('Experiencia creada')
    }
    setExpModal(null)
    load()
  }

  async function handleDeleteExp() {
    setDeleting(true)
    try {
      await deleteExperiencia(deleteExpModal.id)
      showToast('Experiencia eliminada')
      setDeleteExpModal(null)
      load()
    } finally {
      setDeleting(false)
    }
  }

  async function handleDeleteUser() {
    setDeleting(true)
    try {
      await deleteUser(id)
      navigate('/')
    } finally {
      setDeleting(false)
    }
  }

  if (loading) return <div className="spinner" />
  if (!user)   return null

  return (
    <>
      <button className="btn btn-outline btn-sm back-btn" onClick={() => navigate('/')}>
        ← Volver
      </button>

      {/* Tarjeta de perfil */}
      <div className="profile-card">
        <div className="profile-avatar" style={{ background: getColor(user.nombre) }}>
          {getInitials(user.nombre)}
        </div>
        <div className="profile-info">
          <div className="profile-name">{user.nombre}</div>
          <div className="profile-email">{user.correo}</div>
          <div className="profile-meta">
            {user.telefono  && <span>📞 {user.telefono}</span>}
            {user.ubicacion && <span>📍 {user.ubicacion}</span>}
            {user.linkedin  && <span>🔗 <a href={`https://${user.linkedin.replace(/^https?:\/\//,'')}`} target="_blank" rel="noreferrer">LinkedIn</a></span>}
            {user.github    && <span>🐙 <a href={`https://${user.github.replace(/^https?:\/\//,'')}`} target="_blank" rel="noreferrer">GitHub</a></span>}
          </div>
        </div>
        <div className="profile-actions">
          <button className="btn btn-outline btn-sm" onClick={() => navigate(`/usuarios/${id}/editar`)}>✏️ Editar</button>
          <button className="btn btn-danger  btn-sm" onClick={() => setDeleteUserModal(true)}>🗑 Eliminar</button>
        </div>
      </div>

      {/* Experiencias */}
      <div className="section-header">
        <h2 className="section-title">
          Experiencia laboral <span className="badge badge-gray">{user.experiencias.length}</span>
        </h2>
        <button className="btn btn-primary btn-sm" onClick={() => setExpModal('create')}>+ Añadir</button>
      </div>

      {user.experiencias.length === 0 && (
        <div className="empty-state">
          <div className="empty-icon">💼</div>
          Sin experiencia registrada. ¡Añade la primera!
        </div>
      )}

      <div className="experience-list">
        {user.experiencias.map(exp => (
          <ExperienceCard
            key={exp.id}
            experiencia={exp}
            onEdit={e => setExpModal(e)}
            onDelete={e => setDeleteExpModal(e)}
            onRefresh={load}
          />
        ))}
      </div>

      {/* Modales */}
      {expModal && (
        <ExperienceModal
          experiencia={expModal === 'create' ? null : expModal}
          userId={Number(id)}
          onSave={handleSaveExp}
          onCancel={() => setExpModal(null)}
        />
      )}

      {deleteExpModal && (
        <ConfirmModal
          title="¿Eliminar experiencia?"
          message={`Se eliminará "${deleteExpModal.cargo} @ ${deleteExpModal.empresa}" y todas sus funciones.`}
          onConfirm={handleDeleteExp}
          onCancel={() => setDeleteExpModal(null)}
          loading={deleting}
        />
      )}

      {deleteUserModal && (
        <ConfirmModal
          title="¿Eliminar usuario?"
          message={`Se eliminará a "${user.nombre}" junto con toda su experiencia laboral. Esta acción no se puede deshacer.`}
          onConfirm={handleDeleteUser}
          onCancel={() => setDeleteUserModal(false)}
          loading={deleting}
        />
      )}

      {/* Toast */}
      {toast && (
        <div className="toast-container">
          <div className={`toast toast-${toast.type}`}>{toast.msg}</div>
        </div>
      )}
    </>
  )
}
