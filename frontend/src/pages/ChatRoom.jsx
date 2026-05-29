import React, {useEffect, useState, useRef} from 'react'
import {useParams} from 'react-router-dom'
import api from '../api'
import Loading from '../components/Loading'

export default function ChatRoom(){
  const {roomName} = useParams()
  const [messages, setMessages] = useState([])
  const [text, setText] = useState('')
  const [loading, setLoading] = useState(true)
  const wsRef = useRef(null)

  useEffect(()=>{
    let mounted = true
    const fetchMessages = async ()=>{
      try{
        const res = await api.get('/chat/messages/', {params: {room: roomName}})
        if(mounted) setMessages(res.data)
      }catch(err){
        console.error(err)
      }finally{ if(mounted) setLoading(false) }
    }
    fetchMessages()

    // setup WebSocket
    const wsUrlBase = import.meta.env.VITE_WS_URL || 'ws://localhost:8000/ws'
    const ws = new WebSocket(`${wsUrlBase}/chat/${roomName}/`)
    wsRef.current = ws
    ws.onopen = ()=> console.log('ws open')
    ws.onmessage = (e)=>{
      const data = JSON.parse(e.data)
      // event could be chat.message
      setMessages(prev => [...prev, {text: data.message, sender: {username: data.user}, created_at: new Date().toISOString()}])
    }
    ws.onclose = ()=> console.log('ws closed')
    return ()=>{ mounted=false; ws.close() }
  }, [roomName])

  const send = ()=>{
    if(!text) return
    const payload = {message: text}
    wsRef.current.send(JSON.stringify(payload))
    setText('')
  }

  return (
    <div className="p-4">
      <h2 className="text-xl font-semibold mb-4">Room: {roomName}</h2>
      {loading ? <Loading /> : (
        <div className="bg-white rounded shadow p-4 h-[60vh] overflow-auto">
          {messages.map((m,i)=> (
            <div key={i} className="mb-2">
              <div className="text-sm text-gray-500">{m.sender?.username || m.sender?.full_name || 'system'} <span className="text-xs">{new Date(m.created_at).toLocaleString()}</span></div>
              <div className="p-2 bg-slate-100 rounded">{m.text}</div>
            </div>
          ))}
        </div>
      )}

      <div className="mt-3 flex gap-2">
        <input value={text} onChange={e=>setText(e.target.value)} className="flex-1 p-2 border rounded"/>
        <button onClick={send} className="bg-sky-600 text-white p-2 rounded">Send</button>
      </div>
    </div>
  )
}
