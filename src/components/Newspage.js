import {useState,useEffect} from 'react'
import {useParams} from 'react-router-dom'


const Newspage = ({newspage}) => {
    const params=useParams();
    const [news,setNews]=useState([])
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
          `https://stockfinch.herokuapp.com/api/stock_news/${params.id}`)
          const news =await res.json()
    return news     
    }
 
    return (
        <div className='newspage'>
            <p className='headline'>{news.headline}</p>
            <p>{news.publish_date}</p>
            <img className='newspage-img' src={news.image_url}></img>
            <p className='news-para'>{news.description}</p>
        </div>
           
    )
}

export default Newspage
