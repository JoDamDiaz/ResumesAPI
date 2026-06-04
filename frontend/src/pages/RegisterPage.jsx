// ── [FRONTEND] Página · Registro ─────────────────────────────────────────────
import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { register as apiRegister } from '../api/auth'
import { useAuth } from '../context/AuthContext'

export default function RegisterPage() {
  const { login } = useAuth()
  const navigate  = useNavigate()

  const [form, setForm]    = useState({ nombre: '', correo: '', password: '', confirm: '' })
  const [showPwd, setShow] = useState(false)
  const [loading, setLoad] = useState(false)
  const [error, setError]  = useState('')

  const set = (k, v) => setForm(p => ({ ...p, [k]: v }))

  async function handleSubmit(e) {
    e.preventDefault()
    setError('')
    if (!form.nombre || !form.correo || !form.password) { setError('Todos los campos son obligatorios'); return }
    if (form.password.length < 6) { setError('La contraseña debe tener al menos 6 caracteres'); return }
    if (form.password !== form.confirm) { setError('Las contraseñas no coinciden'); return }
    setLoad(true)
    try {
      const data = await apiRegister({ nombre: form.nombre, correo: form.correo, password: form.password })
      login(data)
      navigate('/')
    } catch (err) {
      setError(err.message)
    } finally {
      setLoad(false)
    }
  }

  return (
    <div className="auth-page">
      <div className="auth-card">

        <div className="auth-brand">
          <span className="auth-brand-icon">📄</span>
          <span className="auth-brand-name">Resumes API</span>
        </div>

        <h1 className="auth-title">Crear cuenta</h1>
        <p className="auth-subtitle">Únete para gestionar currículums</p>

        <form onSubmit={handleSubmit} className="auth-form">
          <div className="form-group">
            <label>Nombre completo</label>
            <input
              type="text"
              placeholder="Ana García López"
              value={form.nombre}
              onChange={e => set('nombre', e.target.value)}
              autoFocus
            />
          </div>

          <div className="form-group">
            <label>Correo electrónico</label>
            <input
              type="email"
              placeholder="correo@ejemplo.com"
              value={form.correo}
              onChange={e => set('correo', e.target.value)}
            />
          </div>

          <div className="form-group">
            <label>Contraseña</label>
            <div className="pwd-wrap">
              <input
                type={showPwd ? 'text' : 'password'}
                placeholder="Mínimo 6 caracteres"
                value={form.password}
                onChange={e => set('password', e.target.value)}
              />
              <button type="button" className="pwd-toggle" onClick={() => setShow(s => !s)}>
                {showPwd ? '🙈' : '👁'}
              </button>
            </div>
          </div>

          <div className="form-group">
            <label>Confirmar contraseña</label>
            <input
              type={showPwd ? 'text' : 'password'}
              placeholder="Repite la contraseña"
              value={form.confirm}
              onChange={e => set('confirm', e.target.value)}
            />
          </div>

          {error && <div className="auth-error">⚠ {error}</div>}

          <button type="submit" className="btn btn-primary auth-submit" disabled={loading}>
            {loading ? 'Creando cuenta…' : 'Crear cuenta'}
          </button>
        </form>

        <p className="auth-footer">
          ¿Ya tienes cuenta?{' '}
          <Link to="/login">Inicia sesión</Link>
        </p>
      </div>
    </div>
  )
}
