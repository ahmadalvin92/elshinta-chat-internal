import React, {useState} from 'react'
import api from '../api'
import {useNavigate} from 'react-router-dom'
import Loading from '../components/Loading'

export default function Register(){
  const [full_name, setFullName] = useState('')
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [division, setDivision] = useState('')
  const [internal_code, setInternalCode] = useState('')
  const [avatar, setAvatar] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const navigate = useNavigate()

  const submit = async (e) =>{
    e.preventDefault()
    setLoading(true); setError(null)
    try{
      const fd = new FormData()
      fd.append('full_name', full_name)
      fd.append('username', username)
      fd.append('password', password)
      fd.append('division', division)
      fd.append('internal_code', internal_code)
      if(avatar) fd.append('avatar', avatar)
      await api.post('/accounts/register/', fd, {headers: {'Content-Type': 'multipart/form-data'}})
      navigate('/login')
    }catch(err){
      setError(err?.response?.data || 'Register failed')
    }finally{setLoading(false)}
  }

  return (
    <div className="max-w-md mx-auto mt-8 bg-white p-6 rounded shadow">
      <h2 className="text-xl font-semibold mb-4">Register</h2>
      <form onSubmit={submit}>
        <label>Nama Lengkap</label>
        <input className="w-full p-2 border rounded mb-2" value={full_name} onChange={e=>setFullName(e.target.value)} />
        <label>Username</label>
        <input className="w-full p-2 border rounded mb-2" value={username} onChange={e=>setUsername(e.target.value)} />
        <label>Password</label>
        <input type="password" className="w-full p-2 border rounded mb-2" value={password} onChange={e=>setPassword(e.target.value)} />
        <label>Divisi</label>
        <input className="w-full p-2 border rounded mb-2" value={division} onChange={e=>setDivision(e.target.value)} />
        <label>Kode Akses Internal</label>
        <input className="w-full p-2 border rounded mb-2" value={internal_code} onChange={e=>setInternalCode(e.target.value)} />
        <label>Avatar (optional)</label>
        <input type="file" accept="image/*" onChange={e=>setAvatar(e.target.files[0])} className="mb-3" />
        {error && <div className="text-red-600 mb-2">{JSON.stringify(error)}</div>}
        <button className="w-full bg-sky-600 text-white p-2 rounded" disabled={loading}>
          {loading ? <Loading size={18}/> : 'Register'}
        </button>
      </form>
    </div>
  )
}
