import React from 'react'
import { Link } from 'react-router-dom'

export default function Header(){
  return (
    <header className="p-4 bg-white shadow flex items-center justify-between">
      <div className="flex items-center gap-3">
        <img src="/assets/logo.svg" alt="Elshinta" className="h-12" />
        <h1 className="text-lg font-bold">Elshinta Chat Internal</h1>
      </div>
      <nav>
        <Link to="/login" className="mr-3 text-sm text-sky-600">Login</Link>
        <Link to="/register" className="text-sm text-sky-600">Register</Link>
      </nav>
    </header>
  )
}
