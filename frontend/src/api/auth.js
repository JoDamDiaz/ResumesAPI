// ── [FRONTEND] API · autenticación ───────────────────────────────────────────
import { post, get } from './client'

export const login    = (correo, password) => post('/auth/login',    { correo, password })
export const register = (data)             => post('/auth/register',  data)
export const me       = ()                 => get('/auth/me')
