import axios from 'axios';
import React, { useEffect, useState } from 'react'

const Home = () => {
  const[items,setItems]=useState([]);
  const[dataIsLoaded,setDataIsLoaded]=useState(false);
  
  useEffect(()=>{
     axios.get('http://localhost:8000/ims/teacher/')
       .then((res)=>{
        setItems(res.data);
        setDataIsLoaded(true);
       });
  },[]);

  if (!dataIsLoaded){
    return(
      <div>
        <h4><i>Please wait some time..</i></h4>
      </div>
    );
  } else{

  return (
    <div>

      <table>
        <thead>
          <tr>
            <th>Full Name</th>
            <th>Stream</th>
            <th>Subject</th>
            <th>No. of Students</th>
          </tr>
        </thead>
         <tbody>
            {items.map((row)=>(
             <tr key={row.id}>
               <td>{row.fullname}</td>
               <td>{row.stream}</td>
               <td>{row.subject}</td>
               <td>{row.no_of_students}</td>    
             </tr>
        ))}
        </tbody>
      </table>
    </div>
  );
};
};
export default Home;

