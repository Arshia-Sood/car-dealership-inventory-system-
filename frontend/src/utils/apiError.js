export function getApiErrorMessage(error, fallbackMessage) {
  const detail = error.response?.data?.detail

  if (Array.isArray(detail)) {
    return detail.map((issue) => issue.msg).join(' ')
  }

  return detail || fallbackMessage
}
