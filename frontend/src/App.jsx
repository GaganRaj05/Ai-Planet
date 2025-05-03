import { useState } from 'react'
import {ToastContainer , toast } from 'react-toastify'
import Router from './router/routes'
function App() {
  return (
    <>
      <Router/>
      <ToastContainer position="top-center"/>
    </>
  )
}

export default App
