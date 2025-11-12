import React from 'react'
import axios from 'axios';


const Profile = () => {

    const logout =async () => {

    try{
        const response=await axios.post(' http://localhost:8000/logout/',{
            refresh:localStorage.getItem('refreshToken'),
        });
        localStorage.removeItem('accessToken');
        localStorage.removeItem('refreshToken');
    }catch(error){
        console.error(error);
    }
};


    const handleLogout=()=>{
        logout();
    };
  return (
    <div>
        <button onClick={handleLogout}>Logout</button>
    </div>
  )
}

export default Profile;