import React from 'react'

export default function Loading({size=40}){
  return (
    <div className="flex items-center justify-center">
      <div className="animate-spin rounded-full h-" style={{width: size, height: size, border: '4px solid rgba(0,0,0,0.1)', borderTop: '4px solid #0ea5e9'}}></div>
    </div>
  )
}
