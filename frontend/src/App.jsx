// ── [FRONTEND] Resumes API · router + auth ────────────────────────────────────
import { BrowserRouter, Routes, Route, Navigate, Outlet } from 'react-router-dom'
import { AuthProvider, useAuth } from './context/AuthContext'
import Navbar from './components/Navbar'
import HomePage from './pages/HomePage'
import UserDetailPage from './pages/UserDetailPage'
import UserFormPage from './pages/UserFormPage'
import LoginPage from './pages/LoginPage'
import RegisterPage from './pages/RegisterPage'

function AuthenticatedLayout() {
  return (
    <>
      <Navbar />
      <main className="main-content">
        <Outlet />
      </main>
    </>
  )
}

function AppRoutes() {
  const { user, loading } = useAuth()

  if (loading) {
    return (
      <div style={{ display: 'flex', justifyContent: 'center', marginTop: 120 }}>
        <div className="spinner" />
      </div>
    )
  }

  return (
    <Routes>
      {/* Rutas públicas */}
      <Route path="/login"    element={user ? <Navigate to="/" replace /> : <LoginPage />} />
      <Route path="/registro" element={user ? <Navigate to="/" replace /> : <RegisterPage />} />

      {/* Rutas protegidas */}
      <Route element={user ? <AuthenticatedLayout /> : <Navigate to="/login" replace />}>
        <Route path="/"                    element={<HomePage />} />
        <Route path="/usuarios/nuevo"      element={<UserFormPage />} />
        <Route path="/usuarios/:id"        element={<UserDetailPage />} />
        <Route path="/usuarios/:id/editar" element={<UserFormPage />} />
      </Route>

      <Route path="*" element={<Navigate to={user ? '/' : '/login'} replace />} />
    </Routes>
  )
}

export default function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <AppRoutes />
      </BrowserRouter>
    </AuthProvider>
  )
}
