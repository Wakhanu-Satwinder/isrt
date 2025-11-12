import React,{ useEffect, useState } from 'react';
import {BrowserRouter as Router,Routes,Route, Navigate}from 'react-router-dom';
import  Navbar  from './components/Navbar';
import Home from './components/Home';
import Login from './components/Login';
import Register from './components/Register';
import Request from './components/Request';
import About from './components/About';
import Logout from './components/Logout';
import EmailForm from './components/EmailForm';
import './App.css'
import './index.css'
import './navbar.css'





function App() {
  const[isAuthenticated,setIsAuthenticated]=useState(!!localStorage.getItem('accessToken'));
  const handleLoginSuccess=()=>{
    setIsAuthenticated(true);
  }

  return (
    <>
      <Navbar/>

        <Routes>
          <Route path="/home" element={<Home/>}/>
          <Route path="/Request" element={isAuthenticated?<Request/>:<Navigate to="/login"/>  }/> 
          <Route path="/About" element={<About/>}/>
          <Route path="/login" element={<Login onLoginSuccess={handleLoginSuccess}/>}/>
          <Route path="/register" element={<Register/>}/>
          <Route path="/EmailForm" element={isAuthenticated?<EmailForm/>:<Navigate to="/login"/>}/>
          <Route path="/logout" element={<Logout/>}/>
          <Route path="/" element={<Navigate to={isAuthenticated?"/Request":"/login"}/>}/>

        </Routes>
        
        

    </>
  )
}

export default App;
