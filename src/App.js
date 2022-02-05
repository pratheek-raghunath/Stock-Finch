import { BrowserRouter as Router,Route,Routes } from 'react-router-dom'
import Newsfeed from './components/Newsfeed'
import Newspage from './components/Newspage'
import Nav from './components/Nav'
import Footer from './components/Footer'
import LoginPage from './components/LoginPage'
import Registartion from './components/Registration'
import Archive from './components/Archive'
import AA from './components/AA'

function App() {
  

  return (
   

    <Router>
       <Nav/>
      <Routes>
        <Route path='/' element={<Newsfeed/>}/>
        <Route path='/news/:id' element={<Newspage/>}/>
        <Route path='/login' element={<LoginPage/>}/>
        <Route path='/Sign-up' element={<Registartion/>}/>
        <Route path='/archive' element={<Archive/>}/>
        <Route path='/aa' element={<AA/>}/>

      </Routes>
      <Footer/>
    </Router>
    
  )


}
export default App;
 


