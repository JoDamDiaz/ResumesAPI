// ── [FRONTEND] API · cliente base ────────────────────────────────────────────
const BASE = '/api/v1'

async function request(method, path, body) {
  const token = localStorage.getItem('token')
  const options = { method, headers: {} }
  if (token) options.headers['Authorization'] = `Bearer ${token}`
  if (body !== undefined) {
    options.headers['Content-Type'] = 'application/json'
    options.body = JSON.stringify(body)
  }
  const res = await fetch(`${BASE}${path}`, options)
  if (res.status === 204) return null
  const data = await res.json()
  if (!res.ok) throw new Error(data.detail ?? `Error ${res.status}`)
  return data
}

export const get  = (path)       => request('GET',    path)
export const post = (path, body) => request('POST',   path, body)
export const put  = (path, body) => request('PUT',    path, body)
export const del  = (path)       => request('DELETE', path)
