import React, {useEffect, useState} from 'react'
import api from '../api'
import Loading from '../components/Loading'

export default function AdminDashboard(){
  const [divisions, setDivisions] = useState([])
  const [announcements, setAnnouncements] = useState([])
  const [newDivision, setNewDivision] = useState('')
  const [newAnnouncement, setNewAnnouncement] = useState({title:'', body:''})
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(()=>{
    const fetchData = async ()=>{
      try{
        const [divRes, annRes] = await Promise.all([
          api.get('/accounts/divisions/'),
          api.get('/chat/announcements/'),
        ])
        setDivisions(divRes.data)
        setAnnouncements(annRes.data)
      }catch(err){
        setError('Failed to load admin data')
      }finally{setLoading(false)}
    }
    fetchData()
  }, [])

  const addDivision = async () =>{
    if(!newDivision) return
    try{
      const res = await api.post('/accounts/divisions/', {name:newDivision})
      setDivisions(prev => [...prev, res.data])
      setNewDivision('')
    }catch(err){ console.error(err) }
  }

  const toggleDivision = async (division) =>{
    try{
      const res = await api.patch(`/accounts/divisions/${division.id}/`, {is_active: !division.is_active})
      setDivisions(prev => prev.map(d => d.id===division.id ? res.data : d))
    }catch(err){ console.error(err) }
  }

  const addAnnouncement = async () =>{
    if(!newAnnouncement.title || !newAnnouncement.body) return
    try{
      const res = await api.post('/chat/announcements/', newAnnouncement)
      setAnnouncements(prev => [res.data, ...prev])
      setNewAnnouncement({title:'', body:''})
    }catch(err){ console.error(err) }
  }

  return (
    <div className="p-4">
      <h2 className="text-xl font-semibold mb-4">Admin Dashboard</h2>
      {loading ? <Loading /> : error ? <div className="text-red-600">{error}</div> : (
        <div className="grid gap-6 md:grid-cols-2">
          <section className="bg-white p-4 rounded shadow">
            <h3 className="font-semibold mb-3">Master Divisi</h3>
            <div className="flex gap-2 mb-3">
              <input className="flex-1 p-2 border rounded" value={newDivision} onChange={e=>setNewDivision(e.target.value)} placeholder="Nama divisi" />
              <button onClick={addDivision} className="bg-sky-600 text-white px-4 rounded">Tambah</button>
            </div>
            <ul className="space-y-2">
              {divisions.map(div => (
                <li key={div.id} className="flex justify-between items-center p-2 border rounded">
                  <div>
                    <div className="font-medium">{div.name}</div>
                    <div className="text-sm text-slate-500">{div.is_active ? 'Active' : 'Inactive'}</div>
                  </div>
                  <button onClick={()=>toggleDivision(div)} className="text-sm text-sky-600">{div.is_active ? 'Disable' : 'Enable'}</button>
                </li>
              ))}
            </ul>
          </section>

          <section className="bg-white p-4 rounded shadow">
            <h3 className="font-semibold mb-3">Announcement</h3>
            <input className="w-full p-2 border rounded mb-2" placeholder="Judul" value={newAnnouncement.title} onChange={e=>setNewAnnouncement(prev=>({...prev,title:e.target.value}))} />
            <textarea className="w-full p-2 border rounded mb-2" placeholder="Pesan" rows={4} value={newAnnouncement.body} onChange={e=>setNewAnnouncement(prev=>({...prev,body:e.target.value}))} />
            <button onClick={addAnnouncement} className="bg-sky-600 text-white px-4 py-2 rounded">Kirim Pengumuman</button>
            <div className="mt-4 space-y-3">
              {announcements.map(item => (
                <div key={item.id} className="border p-3 rounded">
                  <div className="font-semibold">{item.title}</div>
                  <div className="text-sm text-slate-600">{new Date(item.created_at).toLocaleString()}</div>
                  <div className="mt-2">{item.body}</div>
                </div>
              ))}
            </div>
          </section>
        </div>
      )}
    </div>
  )
}
