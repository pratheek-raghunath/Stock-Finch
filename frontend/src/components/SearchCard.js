import {Link} from "react-router-dom"
import { IoBookmark } from 'react-icons/io5';
import { IoBookmarkOutline } from 'react-icons/io5';
import { useState } from "react";


const SearchCard = ({ search }) => { 
    return (
         <div  className="newssection">
             <div style={{ cursor:'pointer'}}>
             <Link to={'/company?cid=' + search.cid} >
              <h1 className="headlineout">{search.cname}</h1>
            </Link>
            </div>
            <h2 className="headlineout">NSE: {search.nse}</h2>
            <h2 className="headlineout">Sector: {search.sname}</h2>
            
      </div>
    )
}

export default SearchCard
