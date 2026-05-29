import React from 'react'
import { Link, useNavigate } from 'react-router-dom'
import api from '../api'

export default function Header(){
  const navigate = useNavigate()
  const handleLogout = async ()=>{
    try{
      await api.post('/accounts/logout/')
    }catch(err){ }
    navigate('/login')
  }

  return (
    <header className="p-4 bg-white shadow flex flex-col md:flex-row md:items-center md:justify-between gap-4">
      <div className="flex items-center gap-3">
        <img src="/assets/logo.svg" alt="Elshinta" className="h-12" />
        <h1 className="text-lg font-bold">Elshinta Chat Internal</h1>
      </div>
      <nav className="flex items-center gap-3">
        <Link to="/chat/Umum" className="text-sm text-sky-600">Umum</Link>
        <Link to="/admin" className="text-sm text-sky-600">Admin</Link>
        <Link to="/login" className="text-sm text-sky-600">Login</Link>
        <Link to="/register" className="text-sm text-sky-600">Register</Link>
        <button onClick={handleLogout} className="text-sm text-red-500">Logout</button>
      </nav>
    </header>
  )
}
