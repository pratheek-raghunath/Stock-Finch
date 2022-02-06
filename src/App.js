import { BrowserRouter as Router,Route,Routes } from 'react-router-dom'
import Newsfeed from './components/Newsfeed'
import Newspage from './components/Newspage'
import Nav from './components/Nav'
import Footer from './components/Footer'
import LoginPage from './components/LoginPage'
import Registartion from './components/Registration'
import Archive from './components/Archive'
import {LoginContext} from './components/Context'
import { useEffect, useState } from 'react'

function App() {
  const [loggedIn,setloggedIn] =useState(false)
  
  useEffect(() => {
    const storedLoggedIn = (sessionStorage.getItem('storedLoggedIn'))
    setloggedIn(storedLoggedIn)
  }, [])

  return (
   
    <LoginContext.Provider value={{loggedIn,setloggedIn}}>
        <Router>
          <Nav/>
          <Routes>
            <Route path='/' element={<Newsfeed/>}/>
            <Route path='/news/:id' element={<Newspage/>}/>
            <Route path='/login' element={<LoginPage/>}/>
            <Route path='/Sign-up' element={<Registartion/>}/>
            <Route path='/archive' element={<Archive/>}/>
          </Routes>
          <Footer/>
        </Router>
    </LoginContext.Provider>
    
  )


}
export default App;
 


