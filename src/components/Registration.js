import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom'


const Registration = () => {
  const [email ,setEmail] =useState("");
  const [password ,setPassword] =useState("");
  const [phonenumber,setPhone] =useState("");
  const [firstname ,setFname] =useState("");
  const [lastname ,setLname] =useState("");
  let navigate=useNavigate();


  const handleclick = (e)=>{
    e.preventDefault();
  const opts = {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({
        first_name: firstname,
        last_name: lastname, 
        email: email,
        password: password,
        phone: phonenumber
    })
     
};
fetch("https://stockfinch.herokuapp.com/api/register", opts)
      .then(resp =>{
        if(resp.status === 200)
        {
          alert('Successfully Registered'); 
          navigate('/login') 
          return resp.json();
          
          
        }
        if(resp.status === 400)
        {
          alert('User already exists'); 
          return resp.json();
          
        }
        else alert('Error');
      })
    }

  return <section >
  <div className="mask d-flex align-items-center h-100 gradient-custom-3">
    <div className="container h-100">
      <div className="row d-flex justify-content-center align-items-center h-100">
        <div className="col-12 col-md-9 col-lg-7 col-xl-6">
          <div className="card" >
            <div className="card-body p-5">
              <h2 className="text-uppercase text-center mb-5">Create an account</h2>

              <form>

                <div className="form-outline mb-4">
                  <input type="text" id="form3Example1cg" className="form-control form-control-lg" value={firstname} onChange={(e)=>setFname(e.target.value)}/>
                  <label className="form-label" htmlFor="form3Example1cg">First Name</label>
                </div>
                <div className="form-outline mb-4">
                  <input type="text" id="form3Example1cg" className="form-control form-control-lg" value={lastname} onChange={(e)=>setLname(e.target.value)}/>
                  <label className="form-label" htmlFor="form3Example1cg">Last Name</label>
                </div>

                <div className="form-outline mb-4">
                  <input type="text" id="form3Example1cg" className="form-control form-control-lg" value={phonenumber} onChange={(e)=>setPhone(e.target.value)}/>
                  <label className="form-label" htmlFor="form3Example1cg">Phone Number</label>
                </div>

                <div className="form-outline mb-4">
                  <input type="email" id="form3Example3cg" className="form-control form-control-lg" value={email} onChange={(e)=>setEmail(e.target.value)}/>
                  <label className="form-label" htmlFor="form3Example3cg">Your Email</label>
                </div>

                <div className="form-outline mb-4">
                  <input type="password" id="form3Example4cg" className="form-control form-control-lg" value={password} onChange={(e)=>setPassword(e.target.value)}/>
                  <label className="form-label" htmlFor="form3Example4cg">Password</label>
                </div>

                

                <div className="form-check d-flex justify-content-center mb-5">
                  <input
                    className="form-check-input me-2"
                    type="checkbox"
                    value=""
                    id="form2Example3cg"
                  />
                  <label className="form-check-label" htmlFor="form2Example3g">
                    I agree all statements in <a href="#!" className="text-body"><u>Terms of service</u></a>
                  </label>
                </div>

                <div className="d-flex justify-content-center">
                <input className="btn btn-primary btn-lg" type="submit" value="Submit" onClick={handleclick}/>
                </div>

                

              </form>

            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</section>
};

export default Registration;
