// ── [FRONTEND] Componente · ConfirmModal ──────────────────────────────────────
export default function ConfirmModal({ title, message, onConfirm, onCancel, loading }) {
  return (
    <div className="modal-overlay" onClick={onCancel}>
      <div className="modal" onClick={e => e.stopPropagation()}>
        <div className="modal-title">{title}</div>
        <div className="modal-body">{message}</div>
        <div className="modal-actions">
          <button className="btn btn-outline" onClick={onCancel} disabled={loading}>
            Cancelar
          </button>
          <button className="btn btn-danger" onClick={onConfirm} disabled={loading}>
            {loading ? 'Eliminando…' : 'Eliminar'}
          </button>
        </div>
      </div>
    </div>
  )
}
