import React, { useContext } from 'react';
import ArchivedCard from './ArchivedCard';
import {useState,useEffect} from 'react'
import {LoginContext} from './Context'
import { useNavigate } from 'react-router-dom'




const Archive = ( ) => {
    const [news,setNews]=useState({has_prev:false,has_next:false,prev:null,next:null,data:[]})
    const token=sessionStorage.getItem('token')
    const {loggedIn,setloggedIn}=useContext(LoginContext)
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
      }
  };
  
    const res =await fetch(
        'https://stockfinch.herokuapp.com/api/news_archive',opts)
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

  return <div>
    {loggedIn ?
    (<div>
  <div className='vector-top-bg'>
      <p className='para-top'> News You've Archived</p>
  </div>

   <div>
   {news.data.map((news)=>
                        <ArchivedCard key={news.id} news={news} />)}
  </div>
  <div className='d-flex justify-content-center'>
  {news.has_prev &&<button className="btn btn-primary pagebtn"onClick={prevPage}>prev</button>}
  {news.has_next &&<button className="btn btn-primary pagebtn"onClick={nextPage}>next</button>}
  </div>
  </div>):((navigate('/login')))}
  </div>;
};

export default Archive;
