import {Link} from "react-router-dom"
import { IoBookmark } from 'react-icons/io5';
import { IoBookmarkOutline } from 'react-icons/io5';
import { useContext, useState } from "react";
import {LoginContext} from './Context'



const Newscard = ({ news}) => {
    const [archived ,setArchived] =useState(news.is_archived);
    const token=sessionStorage.getItem('token')
    const {loggedIn,setloggedIn}=useContext(LoginContext)


    
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
          fetch(process.env.REACT_APP_API + '/news_archive',opts)
          .then(()=>setArchived(false))
          .then(resp =>{
            if(resp.status === 400)
            {
              alert('Something went wrong');
            }
            
          })



    }

    
    return (

       
         <div  className="newssection" style={{display: archived ? "block" : "none"}}
         >
             <button className="archivebtn" onClick={()=>removeArchive(news.id)}>
             <IoBookmark  style={{ cursor:'pointer'}}/> </button>
             
             <div style={{ cursor:'pointer'}}>
             <Link to={`/news/${news.id}`} >
             <img src={news.image_url}></img>
             <h2 className="headlineout">{news.headline}</h2>
            </Link>
            </div>
            
           
        
      </div>
      
     
    )
}

export default Newscard
