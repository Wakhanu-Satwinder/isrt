import React, { useState } from 'react'

const Navbar = () => {
    const [isOpen,setIsOpen]=useState(false);
    const toggleMenu =()=>{
        setIsOpen(!isOpen)
    }

  return (

        <nav className='navbar'>
            <div className='navbar-logo'><i>ISRTS</i></div>

            <div className={`navbar-links ${isOpen?"active":""}`}>
               <a href='/Home'>Home</a>
               <a href='/Request'>Request</a>
               <a href='/About'>About</a>
               <a href='/Login'>Login</a>
               <a href='/Logout'>Logout</a>
               <a href='/EmailForm'>Contact</a>
               
               
               
            </div>

            <div className='navbar-toggle' onClick={toggleMenu}>
                <span></span>
                <span></span>
                <span></span>
            </div>
        </nav>
    
  );

}

export default Navbar;
