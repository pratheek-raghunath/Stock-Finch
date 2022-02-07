import {useState,useEffect} from 'react'
import {useParams} from 'react-router-dom'
import { IoBookmark } from 'react-icons/io5';
import { IoBookmarkOutline } from 'react-icons/io5';



const Newspage = ({newspage}) => {
    const params=useParams();
    const token=sessionStorage.getItem('token')


    const [news,setNews]=useState([])
    const [archived ,setArchived] =useState(false);

    const addArchive =(id)=>{

      const opts = {
          method: 'POST',
          headers: {
              'Authorization': 'Bearer '+token,

              'Content-Type': 'application/json'
          },
          body:JSON.stringify({
              news_id:id
            
          })
          
      };
        fetch('https://stockfinch.herokuapp.com/api/news_archive',opts)
        .then(resp =>{
          if(resp.status === 400)
          {
            alert('Something went wrong');
          }
          
        })
        .then(()=>setArchived(true))
        

  }
  const removeArchive =(id)=>{

      const opts = {
          method: 'DELETE',
          headers: {
              'Authorization': 'Bearer '+token,

              'Content-Type': 'application/json'
          },
          body:JSON.stringify({
              news_id:id
            
          })
      };
        fetch('https://stockfinch.herokuapp.com/api/news_archive',opts)
        .then(resp =>{
          if(resp.status === 400)
          {
            alert('Something went wrong');
          }
          
        })
        .then(()=>setArchived(false))
      }
    useEffect(()=>{
        const getNews=async()=>{
          const newsFromServer=await fetchNews()
          setNews(newsFromServer)
          setArchived(newsFromServer.is_archived)
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
          `https://stockfinch.herokuapp.com/api/stock_news/${params.id}`,opts)
          console.log(res)
          const news =await res.json()
          console.log(news)


          return news     

          
    }
 
    return (
        <div className='newspage'>
            <p className='headline'>{news.headline}</p>
            {archived ?(
             <button className="archivebtn" onClick={()=>removeArchive(news.id)}>
             <IoBookmark  style={{ cursor:'pointer'}}/> </button>):
             ( <button className="archivebtn" onClick={()=>addArchive(news.id)}>
             <IoBookmarkOutline  style={{ cursor:'pointer'}}/> </button>)}
            <p>{news.publish_date}</p>
            <img className='newspage-img' src={news.image_url}></img>
            <p className='news-para'>{news.description}</p>
        </div>
           
    )
}

export default Newspage
