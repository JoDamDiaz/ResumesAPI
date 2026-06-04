// ── [FRONTEND] Componente · ExperienceModal (crear / editar experiencia) ──────
import { useState } from 'react'

const empty = { cargo: '', empresa: '', tiempo_inicio: '', tiempo_final: '' }

export default function ExperienceModal({ experiencia, userId, onSave, onCancel }) {
  const isEdit = Boolean(experiencia)
  const [form, setForm] = useState(
    isEdit
      ? { cargo: experiencia.cargo, empresa: experiencia.empresa,
          tiempo_inicio: experiencia.tiempo_inicio, tiempo_final: experiencia.tiempo_final ?? '' }
      : { ...empty }
  )
  const [funciones, setFunciones] = useState(
    isEdit ? experiencia.funciones.map(f => f.descripcion) : ['']
  )
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const setField = (k, v) => setForm(prev => ({ ...prev, [k]: v }))
  const setFuncion = (i, v) => setFunciones(prev => prev.map((f, idx) => idx === i ? v : f))
  const addFuncion = () => setFunciones(prev => [...prev, ''])
  const removeFuncion = (i) => setFunciones(prev => prev.filter((_, idx) => idx !== i))

  async function handleSubmit(e) {
    e.preventDefault()
    setError('')
    if (!form.cargo || !form.empresa || !form.tiempo_inicio) {
      setError('Cargo, empresa y fecha de inicio son obligatorios')
      return
    }
    setLoading(true)
    try {
      const payload = {
        ...form,
        tiempo_final: form.tiempo_final || null,
        user_id: userId,
        funciones: funciones.filter(f => f.trim()).map((desc, i) => ({ descripcion: desc, orden: i + 1 })),
      }
      await onSave(payload, experiencia?.id)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="modal-overlay" onClick={onCancel}>
      <div className="modal" style={{ maxWidth: 560 }} onClick={e => e.stopPropagation()}>
        <div className="modal-title">{isEdit ? 'Editar experiencia' : 'Nueva experiencia'}</div>

        <form className="exp-form" onSubmit={handleSubmit}>
          <div className="exp-form-grid">
            <div className="form-group">
              <label>Cargo *</label>
              <input value={form.cargo} onChange={e => setField('cargo', e.target.value)} placeholder="Ej. Backend Developer" />
            </div>
            <div className="form-group">
              <label>Empresa *</label>
              <input value={form.empresa} onChange={e => setField('empresa', e.target.value)} placeholder="Ej. TechCorp" />
            </div>
            <div className="form-group">
              <label>Inicio *</label>
              <input type="date" value={form.tiempo_inicio} onChange={e => setField('tiempo_inicio', e.target.value)} />
            </div>
            <div className="form-group">
              <label>Fin <span className="text-muted">(vacío = actual)</span></label>
              <input type="date" value={form.tiempo_final} onChange={e => setField('tiempo_final', e.target.value)} />
            </div>
          </div>

          {!isEdit && (
            <div className="funciones-builder">
              <label>Funciones / Responsabilidades</label>
              {funciones.map((f, i) => (
                <div className="funcion-input-row" key={i}>
                  <input
                    value={f}
                    onChange={e => setFuncion(i, e.target.value)}
                    placeholder={`Función ${i + 1}`}
                  />
                  {funciones.length > 1 && (
                    <button type="button" className="btn-icon" onClick={() => removeFuncion(i)} title="Eliminar">✕</button>
                  )}
                </div>
              ))}
              <button type="button" className="btn btn-outline btn-sm add-funcion-btn" onClick={addFuncion}>
                + Añadir función
              </button>
            </div>
          )}

          {error && <div className="form-error">⚠ {error}</div>}

          <div className="modal-actions">
            <button type="button" className="btn btn-outline" onClick={onCancel} disabled={loading}>Cancelar</button>
            <button type="submit" className="btn btn-primary" disabled={loading}>
              {loading ? 'Guardando…' : isEdit ? 'Guardar cambios' : 'Crear'}
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}
