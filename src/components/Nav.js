import React from 'react'
import { Link } from 'react-router-dom'
import logoimg from '../images/logo.png'

const Nav = () => {
    return (
        <div>
            <nav className='nav-bar'>
                    <div>
                    <Link to='/'>
                        <img className='logo-image'src={logoimg} alt=' '></img>
                    </Link>
                    <Link to='/login'>
                   
                    <button type="button" class="login-btn btn btn-primary">Login/Sign up</button>
                    </Link>
                    </div>
                
            </nav>
        </div>
    )
}

export default Nav
