import React from 'react'
import { useState } from 'react'
import axios from 'axios'
import {useNavigate} from 'react-router-dom'



const Register = () => {

    const [formData,setFormData]=useState({
          full_name:'',
          email:'',
          password1:'',
          password2:'',
    })

    const[successMessage,setSuccessMessage]=useState('')
    const[errorMessage,setErrorMessage]=useState('')

    const handleChange=(e)=>{
      const {name,value}=e.target;
      setFormData({...formData,[name]:value,})
    }

    const navigate=useNavigate();

    const handleSubmit=(e)=>{
      e.preventDefault();
      
      axios.post('http://127.0.0.1:8000/trial/register/',formData)
        .then((res)=>{
        console.log(res.data)
        navigate('/Login');
        }).catch((error)=>{
        console.error(error)
      });

      if(formData.password1!==formData.password2){
        setSuccessMessage('');
        setErrorMessage('please enter matching passwords');
        alert('Passwords do not match');
      }else{
        setSuccessMessage('Form subitted successfully');
        setErrorMessage('');
        alert('Registration successful');
      }
    };



  return (
    <div className='form-container'>
      <form onSubmit={handleSubmit}>
        <h2>REGISTER</h2>
        
        <div className='form-group'>
          <label htmlFor='full_name'>Full Name:</label>
          <input type='text' id='full_name' name='full_name' value={formData.full_name} onChange={handleChange} required/> 
        </div>
        <div className='form-group'>
          <label htmlFor='email'>Email:</label>
          <input type='email' id='email' name='email' value={formData.email} onChange={handleChange} required/> 
        </div>
        <div className='form-group'>
          <label htmlFor='password1'>Password:</label>
          <input type='password' id='password1' name='password1' value={formData.password1} onChange={handleChange} required/> 
        </div>
        
        <div className='form-group'>
          <label htmlFor='password2'>Confirm Password:</label>
          <input type='password' id='password2' name='password2' value={formData.password2} onChange={handleChange} required/> 
        </div>

        {errorMessage && <p className='error-message'>{errorMessage}</p>}
        {successMessage &&<p className='success-message'>{successMessage}</p>}
        <button type='submit' className='submit-button'>Register</button>
       <p>Already have an account?<a href='/Login'>Login</a></p>


      </form>
       
    </div>
  )
}

export default Register;