import {Link} from "react-router-dom"
import { IoBookmark } from 'react-icons/io5';
import { IoBookmarkOutline } from 'react-icons/io5';
import { useState } from "react";


const Newscard = ({ news}) => {
    const [archived ,setArchived] =useState(news.is_archived);
    const token=sessionStorage.getItem('token')
    console.log(news)

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
          .then(()=>setArchived(false))


    }

    
    return (

       
         <div  className="newssection">

            
             {archived ?(
             <button className="archivebtn" onClick={()=>removeArchive(news.id)}>
             <IoBookmark  style={{ cursor:'pointer'}}/> </button>):
             ( <button className="archivebtn" onClick={()=>addArchive(news.id)}>
             <IoBookmarkOutline  style={{ cursor:'pointer'}}/> </button>)}

             <div style={{ cursor:'pointer'}}>
             <Link to={`/news/${news.id}`} >
             <img src={news.image_url}></img>
             <h2 className="headlineout">{news.headline}</h2>
            </Link>
            </div>
              {/* <IoBookmarkOutline onClick={()=>setNewsid(news.id) && addArchive} style={{ cursor:'pointer'}}/>  */}
            
           
        
      </div>
      
     
    )
}

export default Newscard
