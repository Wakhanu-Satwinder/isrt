import React from 'react'
import { useState } from 'react'
import axios from 'axios'
import {useNavigate} from 'react-router-dom'



  const Request = () => {
    const [formData,setFormData]=useState({
          name:'',
          department:'',
          issue_category:'',
          description:'' ,    
    });

    const [error,setError]=useState(null);
    const [successMessage,setSuccessMessage]=useState('')
    const [errorMessage,setErrorMessage]=useState('')
    const [data,setData]=useState('')
    




  const handleChange=(e)=>{
    const {name,value}=e.target;
    setFormData({...formData,[name]:value,})
    }

  const navigate=useNavigate();

  const handleSubmit=async(e)=>{
      e.preventDefault();
    const accessToken=localStorage.getItem('accessToken');

    try{
      await axios.post('http://127.0.0.1:8000/trial/request/',formData,{
        headers:{
          Authorization:`Bearer ${accessToken}`,
        },
      });

      alert('Request posted successfully');
      setData('');
      navigate("/Logout");
    }catch(error){
      if (error.response && error.response.status===401){
        console.log('Access token expired');
      }else{
        console.error('Error posting data',error);
      }
    }
  
   };
     

  return (
    <div className='form-container'>
      <form onSubmit={handleSubmit}>
        <h2>REQUEST</h2>
        
        <div className='form-group'>
          <label htmlFor='name'>Name:</label>
          <input type='text' id='name' name='name' value={formData.name} onChange={handleChange} required/> 
        </div>
        <div className='form-group'>
          <label htmlFor='department'>Department:</label>
          <input type='text' id='department' name='department' value={formData.department} onChange={handleChange} required/> 
        </div>
        <div className='form-group'>
          <label htmlFor='issue_category'>Issue Category</label>
          <input type='text' id='issue_category' name='issue_category' value={formData.issue_category} onChange={handleChange} required/> 
        </div>
        
        <div className='form-group'>
          <label htmlFor='description'>Description:</label>
          <input type='textarea' id='description' name='description' value={formData.description} onChange={handleChange} required/> 
        </div>
        

        {errorMessage && <p className='error-message'>{errorMessage}</p>}
        {successMessage &&<p className='success-message'>{successMessage}</p>}
        <button type='submit' className='submit-button'>Submit</button>
       


      </form>
       
    </div>
  )
}

export default Request;