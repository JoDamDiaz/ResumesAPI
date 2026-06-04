// ── [FRONTEND] Componente · ExperienceCard ────────────────────────────────────
import { useState } from 'react'
import { createFuncion, deleteFuncion } from '../api/funciones'

function formatDate(d) {
  if (!d) return 'Actual'
  const [y, m] = d.split('-')
  const months = ['Ene','Feb','Mar','Abr','May','Jun','Jul','Ago','Sep','Oct','Nov','Dic']
  return `${months[+m - 1]} ${y}`
}

export default function ExperienceCard({ experiencia, onEdit, onDelete, onRefresh }) {
  const [newFuncion, setNewFuncion] = useState('')
  const [addingFn, setAddingFn] = useState(false)
  const [showAddFn, setShowAddFn] = useState(false)

  async function handleAddFuncion() {
    if (!newFuncion.trim()) return
    setAddingFn(true)
    try {
      await createFuncion({
        experiencia_id: experiencia.id,
        descripcion: newFuncion.trim(),
        orden: (experiencia.funciones?.length ?? 0) + 1,
      })
      setNewFuncion('')
      setShowAddFn(false)
      onRefresh()
    } finally {
      setAddingFn(false)
    }
  }

  async function handleDeleteFuncion(id) {
    await deleteFuncion(id)
    onRefresh()
  }

  return (
    <div className="experience-card">
      <div className="experience-card-header">
        <div>
          <div className="experience-title">{experiencia.cargo}</div>
          <div className="experience-company">{experiencia.empresa}</div>
          <div className="experience-dates">
            🗓 {formatDate(experiencia.tiempo_inicio)} — {formatDate(experiencia.tiempo_final)}
            {!experiencia.tiempo_final && <span className="badge badge-green">Actual</span>}
          </div>
        </div>
        <div className="experience-actions">
          <button className="btn btn-outline btn-sm" onClick={() => onEdit(experiencia)}>✏️ Editar</button>
          <button className="btn btn-danger btn-sm" onClick={() => onDelete(experiencia)}>🗑</button>
        </div>
      </div>

      {experiencia.funciones?.length > 0 && (
        <ul className="funciones-list">
          {experiencia.funciones.map(fn => (
            <li key={fn.id} className="funcion-item">
              <span>{fn.descripcion}</span>
              <div className="funcion-item-actions">
                <button className="btn-icon btn-sm" title="Eliminar función" onClick={() => handleDeleteFuncion(fn.id)}>✕</button>
              </div>
            </li>
          ))}
        </ul>
      )}

      {showAddFn ? (
        <div className="add-funcion-row">
          <input
            autoFocus
            value={newFuncion}
            onChange={e => setNewFuncion(e.target.value)}
            placeholder="Descripción de la función"
            onKeyDown={e => { if (e.key === 'Enter') handleAddFuncion(); if (e.key === 'Escape') setShowAddFn(false) }}
          />
          <button className="btn btn-primary btn-sm" onClick={handleAddFuncion} disabled={addingFn}>
            {addingFn ? '…' : 'Añadir'}
          </button>
          <button className="btn btn-ghost btn-sm" onClick={() => setShowAddFn(false)}>Cancelar</button>
        </div>
      ) : (
        <button className="btn btn-ghost btn-sm mt-8" onClick={() => setShowAddFn(true)}>
          + Añadir función
        </button>
      )}
    </div>
  )
}
