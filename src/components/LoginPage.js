import React, { useContext, useState } from 'react';
import {Link} from "react-router-dom"
import signedinimg from '../images/signedin.png'
import { useNavigate } from 'react-router-dom'



const LoginPage = () => {
  const [email ,setEmail] =useState("");
  const [password ,setPassword] =useState("");
  const token=sessionStorage.getItem('token')
  let navigate=useNavigate();


  const handleclick = (e)=>{
    e.preventDefault();
    const opts = {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json'
      },
      body:JSON.stringify({
          email:email,
          password:password
      })
  };
    fetch('https://stockfinch.herokuapp.com/api/token',opts)
    .then(resp =>{
      if(resp.status === 200) 
      {
        return resp.json();
        
      }
      else alert('errrrrrruuuuurr');
    })
    .then(data =>{
      sessionStorage.setItem('token',data.access_token)
      sessionStorage.setItem('first_name',data.first_name)


    })
    .then(navigate('/'))
    .catch(error => {
      console.error('errrrrrrrooooooorrr',error);
    })

  }


  return <div className='loginpage'>
             
             {token && token !=='' &&token !==undefined ? (
             <div><h3 className='logh3'>You're Logged In</h3>
             <img className='signedinimg' src={signedinimg}></img>
             </div>
             ) :

             (<div>
               <span className='login-header'>Login</span>
               <center>  <form>
             <div className="form-outline mb-4">
                  <input type="email" id="form3Example3cg" className="form-control form-control-lg" placeholder='Your Email' value={email} onChange={(e)=>setEmail(e.target.value)}/>
                  
                </div>

                <div className="form-outline mb-4">
                  <input type="password" id="form3Example4cg" className="form-control form-control-lg" placeholder='Password' value={password} onChange={(e)=>setPassword(e.target.value)}/>
                 
                </div>
                <div className="d-flex justify-content-center">
                <input className="btn btn-primary btn-lg" type="submit" value="Submit" onClick={handleclick} />
                </div>
                </form></center>
                <div>
                    <Link to='/Sign-up'>
                        <p className='signup'>Sign up?</p>
                    </Link>
                </div>
                </div>)}

        </div>;

};

export default LoginPage;



