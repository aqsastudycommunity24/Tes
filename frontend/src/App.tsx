import React from 'react'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import './App.css'

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<div>Landing Page - Coming Soon</div>} />
      </Routes>
    </Router>
  )
}

export default App
