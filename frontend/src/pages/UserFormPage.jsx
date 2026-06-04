// ── [FRONTEND] Página · Crear / Editar usuario ────────────────────────────────
import { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { getUserById, createUser, updateUser } from '../api/users'

const emptyForm = { nombre: '', telefono: '', correo: '', linkedin: '', github: '', ubicacion: '' }

export default function UserFormPage() {
  const { id } = useParams()
  const navigate = useNavigate()
  const isEdit = Boolean(id)

  const [form, setForm]       = useState(emptyForm)
  const [loading, setLoading] = useState(isEdit)
  const [saving, setSaving]   = useState(false)
  const [error, setError]     = useState('')

  useEffect(() => {
    if (!isEdit) return
    getUserById(id)
      .then(u => setForm({
        nombre: u.nombre, telefono: u.telefono ?? '', correo: u.correo,
        linkedin: u.linkedin ?? '', github: u.github ?? '', ubicacion: u.ubicacion ?? '',
      }))
      .catch(() => navigate('/'))
      .finally(() => setLoading(false))
  }, [id, isEdit, navigate])

  const setField = (k, v) => setForm(prev => ({ ...prev, [k]: v }))

  async function handleSubmit(e) {
    e.preventDefault()
    setError('')
    if (!form.nombre || !form.correo) { setError('Nombre y correo son obligatorios'); return }
    setSaving(true)
    try {
      const payload = Object.fromEntries(
        Object.entries(form).map(([k, v]) => [k, v || null])
      )
      if (isEdit) {
        await updateUser(id, payload)
      } else {
        const created = await createUser(payload)
        navigate(`/usuarios/${created.user_id}`)
        return
      }
      navigate(`/usuarios/${id}`)
    } catch (err) {
      setError(err.message)
    } finally {
      setSaving(false)
    }
  }

  if (loading) return <div className="spinner" />

  return (
    <>
      <button className="btn btn-outline btn-sm back-btn" onClick={() => navigate(isEdit ? `/usuarios/${id}` : '/')}>
        ← Volver
      </button>

      <div className="form-card">
        <h1 className="form-title">{isEdit ? 'Editar usuario' : 'Nuevo usuario'}</h1>

        <form onSubmit={handleSubmit}>
          <div className="form-grid">
            <div className="form-group full">
              <label>Nombre completo *</label>
              <input value={form.nombre} onChange={e => setField('nombre', e.target.value)} placeholder="Ej. Ana García López" />
            </div>
            <div className="form-group">
              <label>Correo electrónico *</label>
              <input type="email" value={form.correo} onChange={e => setField('correo', e.target.value)} placeholder="correo@ejemplo.com" />
            </div>
            <div className="form-group">
              <label>Teléfono</label>
              <input type="tel" value={form.telefono} onChange={e => setField('telefono', e.target.value)} placeholder="+52 55 1234 5678" />
            </div>
            <div className="form-group full">
              <label>Ubicación</label>
              <input value={form.ubicacion} onChange={e => setField('ubicacion', e.target.value)} placeholder="Ciudad de México, MX" />
            </div>
            <div className="form-group">
              <label>LinkedIn</label>
              <input value={form.linkedin} onChange={e => setField('linkedin', e.target.value)} placeholder="linkedin.com/in/usuario" />
            </div>
            <div className="form-group">
              <label>GitHub</label>
              <input value={form.github} onChange={e => setField('github', e.target.value)} placeholder="github.com/usuario" />
            </div>
          </div>

          {error && <div className="form-error mt-16">⚠ {error}</div>}

          <div className="form-actions">
            <button type="button" className="btn btn-outline" onClick={() => navigate(isEdit ? `/usuarios/${id}` : '/')} disabled={saving}>
              Cancelar
            </button>
            <button type="submit" className="btn btn-primary" disabled={saving}>
              {saving ? 'Guardando…' : isEdit ? 'Guardar cambios' : 'Crear usuario'}
            </button>
          </div>
        </form>
      </div>
    </>
  )
}
