import React, { useState } from 'react';
import axios from 'axios';

const EmailForm = () => {
    const [subject,setSubject]=useState('');
    const [message,setMessage]=useState('');
    const [fromEmail, setFromEmail] = useState('');
    const [toEmail, setToEmail] = useState('');
    {/*const [recipient_email, setRecipientEmail] = useState(''); // Comma separated emails*/}
    
    const handleSubmit = async (e) => {
        e.preventDefault();
        //const accessToken=localStorage.getItem('accessToken');
        axios.post('http://localhost:8000/trial/send-email/',{
            subject,
            message,
            from_email:fromEmail,
            to_email:toEmail,
        }).then((response)=>{
            console.log(response.data);
        }).catch ((error) =>{
            console.error("Error sending email:", error);
            alert("Failed to send email");
    });
}

    return (
        <div className='form-container'>
        <form onSubmit={handleSubmit}>
            <div className='form-group'>
            <input type="text" name='subject' placeholder="Subject" value={subject} onChange={(e) => setSubject(e.target.value)} required />
             </div>
             <div className='form-group'>
            <textarea name='message' placeholder="Message" value={message} onChange={(e) => setMessage(e.target.value)} required />
             </div>
             <div className='form-group'>
            <input type="email" name='email' placeholder="From Email" value={fromEmail} onChange={(e) => setFromEmail(e.target.value)} required />
             </div>
             <div className='form-group'>
            <input type="email" name='email' placeholder="To Email" value={toEmail} onChange={(e) => setToEmail(e.target.value)} required />
             </div>
            <button type="submit" className='submit-button'>Send Email</button>
            {message&&<p>{message}</p>}
        </form>
        </div>
    );
};

export default EmailForm;