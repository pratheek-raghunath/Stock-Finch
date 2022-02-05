import React from 'react'
import { Link } from 'react-router-dom'
import logoimg from '../images/logo.png'
import 'bootstrap/dist/css/bootstrap.min.css';
import {Dropdown}from 'react-bootstrap'

const Nav = () => {
    const first_name=sessionStorage.getItem('first_name')
    const token=sessionStorage.getItem('token')


    return (
        <div>
            <nav className='nav-bar'>
                    <div>
                    <Link to='/'>
                        <img className='logo-image'src={logoimg} alt=' '></img>
                    </Link>
                    

                    {/* <Link to='/login'>
                   
                    <button type="button" className="login-btn btn btn-primary">Login/Sign up</button>
                    </Link> */}
                    <Dropdown className='profile-btn'>
                        <Dropdown.Toggle variant="primary" id="dropdown-basic">
                            Hi,{first_name}
                        </Dropdown.Toggle>

                        <Dropdown.Menu>
                            <Dropdown.Item href="/Archive">Archive</Dropdown.Item>
                            <Dropdown.Item href="#/action-1">Logout</Dropdown.Item>
                        </Dropdown.Menu>
                        </Dropdown>
                       
                        
                    
                    </div>
                
            </nav>
        </div>
    )
}

export default Nav
