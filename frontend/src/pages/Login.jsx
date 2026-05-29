import React, {useState} from 'react'
import api from '../api'
import {useNavigate} from 'react-router-dom'
import Loading from '../components/Loading'

export default function Login(){
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const navigate = useNavigate()

  const submit = async (e) =>{
    e.preventDefault()
    setLoading(true)
    setError(null)
    try{
      const res = await api.post('/accounts/login/', {username, password})
      // redirect to chat
      navigate('/chat/Umum')
    }catch(err){
      setError(err?.response?.data?.detail || 'Login failed')
    }finally{setLoading(false)}
  }

  return (
    <div className="max-w-md mx-auto mt-12 bg-white p-6 rounded shadow">
      <h2 className="text-xl font-semibold mb-4">Login</h2>
      <form onSubmit={submit}>
        <label className="block">Username</label>
        <input className="w-full p-2 border rounded mb-3" value={username} onChange={e=>setUsername(e.target.value)} />
        <label className="block">Password</label>
        <input type="password" className="w-full p-2 border rounded mb-3" value={password} onChange={e=>setPassword(e.target.value)} />
        {error && <div className="text-red-600 mb-2">{error}</div>}
        <button className="w-full bg-sky-600 text-white p-2 rounded" disabled={loading}>
          {loading ? <Loading size={18}/> : 'Login'}
        </button>
      </form>
    </div>
  )
}
