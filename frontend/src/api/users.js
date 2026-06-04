import { get, post, put, del } from './client'

export const getUsers      = ()         => get('/users/')
export const getUserById   = (id)       => get(`/users/${id}`)
export const createUser    = (data)     => post('/users/', data)
export const updateUser    = (id, data) => put(`/users/${id}`, data)
export const deleteUser    = (id)       => del(`/users/${id}`)
