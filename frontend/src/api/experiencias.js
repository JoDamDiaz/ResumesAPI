import { get, post, put, del } from './client'

export const getExperienciasByUser = (userId)     => get(`/experiencias/user/${userId}`)
export const createExperiencia     = (data)       => post('/experiencias/', data)
export const updateExperiencia     = (id, data)   => put(`/experiencias/${id}`, data)
export const deleteExperiencia     = (id)         => del(`/experiencias/${id}`)
