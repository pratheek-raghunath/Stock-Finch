import React from 'react';
import {Link} from "react-router-dom"

const LoginPage = () => {
  return <div className='loginpage'>
             <span className='login-header'>Login</span>
             <center>  <form>
             <div class="form-outline mb-4">
                  <input type="email" id="form3Example3cg" class="form-control form-control-lg" placeholder='Your Email'/>
                  
                </div>

                <div className="form-outline mb-4">
                  <input type="password" id="form3Example4cg" className="form-control form-control-lg" placeholder='Password'/>
                 
                </div>
                <div className="d-flex justify-content-center">
                <input className="btn btn-primary btn-lg" type="submit" value="Submit" />
                </div>
                </form></center>
                <div>
                    <Link to='/Sign-up'>
                        <p className='signup'>Sign up?</p>
                    </Link>
                </div>
        </div>;
};

export default LoginPage;
