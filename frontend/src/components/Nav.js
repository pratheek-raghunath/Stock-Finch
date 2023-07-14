import React, { useContext } from 'react'
import { Link } from 'react-router-dom'
import logoimg from '../images/logo.png'
import 'bootstrap/dist/css/bootstrap.min.css';
import {Dropdown}from 'react-bootstrap'
import {LoginContext} from './Context'
import { useNavigate } from 'react-router-dom'
import SearchBar from './SearchBar'

const Nav = () => {
    const {loggedIn,setloggedIn}=useContext(LoginContext)
    const first_name=sessionStorage.getItem('first_name')
    let navigate=useNavigate();
    const logout=()=>{
        sessionStorage.removeItem('token')
        sessionStorage.removeItem('first_name')
        sessionStorage.removeItem('storedLoggedIn')
        setloggedIn(false)
        navigate('/login')

    }
    return (
        <div className='nav-div'>
            <nav className='nav-bar'>
                    <div>
                        <div className='logo-cntr'>
                    <Link to='/'>
                        <img className='logo-image'src={logoimg} alt=' '></img>
                    </Link>
                    </div>



                    {loggedIn ? 
                (<div className='nav-search-drop'>
                     <SearchBar/>
                    <Dropdown className='profile-btn'>
                        <Dropdown.Toggle variant="primary" id="dropdown-basic">
                            Hi,{first_name}
                        </Dropdown.Toggle>
                        <Dropdown.Menu>
                            <Dropdown.Item href="/Archive">Archive</Dropdown.Item>
                            <Dropdown.Item as="button" onClick={logout}>Logout</Dropdown.Item>
                        </Dropdown.Menu>
                        </Dropdown>
                        </div>):(<></>)}

                                         
                    </div>
            </nav>
        </div>
    )
}
export default Nav