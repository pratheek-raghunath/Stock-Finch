import { BrowserRouter as Router,Route,Routes } from 'react-router-dom'
import Newsfeed from './components/Newsfeed'
import Newspage from './components/Newspage'
import Nav from './components/Nav'
import Footer from './components/Footer'
import LoginPage from './components/LoginPage'
import Registartion from './components/Registration'

function App() {

  return (
   

    <Router>
       <Nav/>
      <Routes>
        <Route path='/' element={<Newsfeed/>}/>
        <Route path='/news/:id' element={<Newspage/>}/>
        <Route path='/login' element={<LoginPage/>}/>
        <Route path='/Sign-up' element={<Registartion/>}/>
      </Routes>
      <Footer/>
    </Router>
    
  )


}
export default App;
 


