export const AUTH_TOKEN_KEY = 'car_dealership_access_token'

export function isAdminToken(token) {
  try {
    const payload = token.split('.')[1]
    return JSON.parse(atob(payload.replace(/-/g, '+').replace(/_/g, '/'))).role === 'admin'
  } catch {
    return false
  }
}
