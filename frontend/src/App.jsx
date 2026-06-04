// ── [FRONTEND] Resumes API · router ───────────────────────────────────────────
import { BrowserRouter, Routes, Route } from 'react-router-dom'
import Navbar from './components/Navbar'
import HomePage from './pages/HomePage'
import UserDetailPage from './pages/UserDetailPage'
import UserFormPage from './pages/UserFormPage'

export default function App() {
  return (
    <BrowserRouter>
      <Navbar />
      <main className="main-content">
        <Routes>
          <Route path="/"                       element={<HomePage />} />
          <Route path="/usuarios/nuevo"         element={<UserFormPage />} />
          <Route path="/usuarios/:id"           element={<UserDetailPage />} />
          <Route path="/usuarios/:id/editar"    element={<UserFormPage />} />
        </Routes>
      </main>
    </BrowserRouter>
  )
}
