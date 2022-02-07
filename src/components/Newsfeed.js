import Newscard from './Newscard'
import {useState,useEffect, useContext} from 'react'
import { useNavigate } from 'react-router-dom'

import {LoginContext} from './Context'


const Newsfeed = ( ) => {

    const [news,setNews]=useState({has_prev:false,has_next:false,prev:null,next:null,data:[]})
    const {loggedIn,setloggedIn}=useContext(LoginContext)

    const token=sessionStorage.getItem('token')
    let navigate=useNavigate();

  useEffect(()=>{
    const getNews=async()=>{
      const newsFromServer=await fetchNews()
      setNews(newsFromServer)
    }
    getNews()
  },[])

  //fetch
  const fetchNews= async()=>{
    const opts = {
        headers: {
            'Authorization': 'Bearer '+token
        },
        }
    const res =await fetch(
        'https://stockfinch.herokuapp.com/api/stock_news',opts)
        console.log(res)
      const news =await res.json()
      return news 
    
    }
const prevPage =()=>{
    const opts = {
        headers: {
            'Authorization': 'Bearer '+token
        },
    }
    fetch(news.prev,opts)
    .then(res => res.json())
    .then(data => {
        setNews(data)
        window.scrollTo(0, 0)
    })
}

const nextPage =()=>{
    const opts = {
        headers: {
            'Authorization': 'Bearer '+token
        },
    }
    fetch(news.next,opts)
    .then(res => res.json())
    .then(data => {
        setNews(data)
    window.scrollTo(0, 0)
    })
}

    



    return (
        <div>
             {loggedIn ?(
            <div>
                <div className='vector-top-bg'>
                    <p className='para-top'>Stocks in News Today</p>
                    <p>{todaysdate}</p>
                </div><div>
                {news.data.map((news)=>
                        <Newscard key={news.id} news={news} />)}

                    </div><div className='d-flex justify-content-center'>
                        {news.has_prev && <button className="btn btn-primary pagebtn" onClick={prevPage}>prev</button>}
                        {news.has_next && <button className="btn btn-primary pagebtn" onClick={nextPage}>next</button>}
                    </div>
                    </div>):
                    (navigate('/login'))}
        </div>
    )
    
}



export default Newsfeed

var showdate= new Date();
var todaysdate=showdate.toDateString()

