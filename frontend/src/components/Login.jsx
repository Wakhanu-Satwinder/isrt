import React, { useEffect, useState } from 'react'
import Register from './Register';
import { useNavigate} from 'react-router-dom';
import axios from 'axios';

const Login = () => {

  const[formData,setFormData]=useState({
    email:'',
    password:'',
  });

  
  const[successMessage,setSuccessMessage]=useState('');
  const[errorMessage,setErrorMessage]=useState('');
  const [data,setData]=useState('');

  const handleChange=(e)=>{
    const {name,value}=e.target;
    setFormData({...formData,[name]:value,});
  }



const navigate =useNavigate();
const handleSubmit=(e)=>{
  e.preventDefault();
   axios.post('http://127.0.0.1:8000/trial/token/',formData)
        .then((response)=>{
          localStorage.setItem('accessToken',response.data.access);
          localStorage.setItem('refreshToken',response.data.refresh);
          console.log('login successful',response.data);
             //window.location.href='/Request'
             navigate('/Request');     
         }).catch((error)=>{
              console.error('LoginFailed',error)
        });
    
  };
  
  return (
    <div className='form-container'>
      <form onSubmit={handleSubmit}>
        <h2>LOGIN</h2>
        <div className='form-group'>
          <label htmlFor='email'>Email:</label>
          <input type='email' id='email'name='email' value={formData.email} onChange={handleChange} required/>
        </div>
        <div className='form-group'>
          <label htmlFor='password'>Password:</label>
          <input type='password' name='password' id='password' value={formData.password} onChange={handleChange} required/>
        </div>
         

         {successMessage &&<p className='success-message'>{successMessage}</p>}
         {errorMessage &&<p className='error-message'>{errorMessage }</p>}
        <button type='submit' className='submit-button'>Login</button>
          <p>Don't have an account?<a href='/Register'>Register</a></p>
      </form>

    </div>
  )
}

export default Login;