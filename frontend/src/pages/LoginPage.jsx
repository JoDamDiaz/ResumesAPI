// ── [FRONTEND] Página · Login ─────────────────────────────────────────────────
import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { login as apiLogin } from '../api/auth'
import { useAuth } from '../context/AuthContext'

export default function LoginPage() {
  const { login } = useAuth()
  const navigate  = useNavigate()

  const [form, setForm]     = useState({ correo: '', password: '' })
  const [showPwd, setShow]  = useState(false)
  const [loading, setLoad]  = useState(false)
  const [error, setError]   = useState('')

  const set = (k, v) => setForm(p => ({ ...p, [k]: v }))

  async function handleSubmit(e) {
    e.preventDefault()
    setError('')
    if (!form.correo || !form.password) { setError('Completa todos los campos'); return }
    setLoad(true)
    try {
      const data = await apiLogin(form.correo, form.password)
      login(data)
      navigate('/')
    } catch (err) {
      setError(err.message)
    } finally {
      setLoad(false)
    }
  }

  function fillDemo() {
    setForm({ correo: 'demo@resumes.com', password: 'Demo1234!' })
  }

  return (
    <div className="auth-page">
      <div className="auth-card">

        {/* Branding */}
        <div className="auth-brand">
          <span className="auth-brand-icon">📄</span>
          <span className="auth-brand-name">Resumes API</span>
        </div>

        <h1 className="auth-title">Iniciar sesión</h1>
        <p className="auth-subtitle">Ingresa tus credenciales para continuar</p>

        {/* Demo hint */}
        <button type="button" className="demo-hint" onClick={fillDemo}>
          <span>🔑</span>
          <span>Usar cuenta demo — <strong>demo@resumes.com</strong> / <strong>Demo1234!</strong></span>
        </button>

        <form onSubmit={handleSubmit} className="auth-form">
          <div className="form-group">
            <label>Correo electrónico</label>
            <input
              type="email"
              placeholder="correo@ejemplo.com"
              value={form.correo}
              onChange={e => set('correo', e.target.value)}
              autoComplete="email"
              autoFocus
            />
          </div>

          <div className="form-group">
            <label>Contraseña</label>
            <div className="pwd-wrap">
              <input
                type={showPwd ? 'text' : 'password'}
                placeholder="••••••••"
                value={form.password}
                onChange={e => set('password', e.target.value)}
                autoComplete="current-password"
              />
              <button type="button" className="pwd-toggle" onClick={() => setShow(s => !s)}>
                {showPwd ? '🙈' : '👁'}
              </button>
            </div>
          </div>

          {error && <div className="auth-error">⚠ {error}</div>}

          <button type="submit" className="btn btn-primary auth-submit" disabled={loading}>
            {loading ? 'Iniciando sesión…' : 'Iniciar sesión'}
          </button>
        </form>

        <p className="auth-footer">
          ¿No tienes cuenta?{' '}
          <Link to="/registro">Regístrate aquí</Link>
        </p>
      </div>
    </div>
  )
}
