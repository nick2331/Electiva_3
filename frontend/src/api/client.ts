import axios from 'axios'

const client = axios.create({
  baseURL: '/api/v1',
  timeout: 120_000,
})

client.interceptors.response.use(
  (res) => res,
  (error) => {
    const msg: string =
      error?.response?.data?.detail ?? error.message ?? 'Error de conexión con el servidor.'
    return Promise.reject(new Error(msg))
  }
)

export default client
