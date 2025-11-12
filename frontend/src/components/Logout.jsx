import React from 'react'
import axios from 'axios';
import { useNavigate } from 'react-router-dom';


const Logout =()=> {
    const navigate=useNavigate();
    const handleLogout=()=>{

     localStorage.clear();
     navigate('/Login');
    };

    
return(
    <button onClick={handleLogout}>Logout</button>
);
};
export default Logout;