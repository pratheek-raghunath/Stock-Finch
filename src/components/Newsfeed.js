import Newscard from './Newscard'
import {useState,useEffect} from 'react'

const Newsfeed = ( ) => {

    const [news,setNews]=useState({has_prev:false,has_next:false,prev:null,next:null})

  useEffect(()=>{
    const getNews=async()=>{
      const newsFromServer=await fetchNews()
      setNews(newsFromServer)
    }
    getNews()
  },[])

  //fetch
  const fetchNews= async()=>{
    const res =await fetch(
        'https://stockfinch.herokuapp.com/api/stock_news')
      const news =await res.json()
      return news 
    
    }
const prevPage =()=>{
    fetch(news.prev)
    .then(res => res.json())
    .then(data => {
        setNews(data)
        window.scrollTo(0, 0)
    })
}

const nextPage =()=>{
    fetch(news.next)
    .then(res => res.json())
    .then(data => {
        setNews(data)
    window.scrollTo(0, 0)
    })
}

    



    return (
        <div>
            <div className='vector-top-bg'>
                <p className='para-top'>Stocks in News Today</p>
                <p>{todaysdate}</p>
            </div>
          
             <div>
             {
                 <Newscard news={news.data}/>
                }
            </div>
            <div className='d-flex justify-content-center'>
            {news.has_prev &&<button className="btn btn-primary pagebtn"onClick={prevPage}>prev</button>}
            {news.has_next &&<button className="btn btn-primary pagebtn"onClick={nextPage}>next</button>}
            </div>
        </div>
    )
    
}



export default Newsfeed

var showdate= new Date();
var todaysdate=showdate.toDateString()

