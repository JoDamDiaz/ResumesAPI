import { post, put, del } from './client'

export const createFuncion = (data)       => post('/funciones/', data)
export const updateFuncion = (id, data)   => put(`/funciones/${id}`, data)
export const deleteFuncion = (id)         => del(`/funciones/${id}`)
