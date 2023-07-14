import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import {Link} from "react-router-dom"




const SearchBar = () => {
    const [searchelem ,setSearchelem] =useState("");
    let navigate=useNavigate();

    const handleclick = (e)=>{
        e.preventDefault();
        navigate('/search-results?query=' + searchelem)
    }

  return (
    <div className=" nav-search-div">
      <input type="search" id="form1" className=" nav-search-bar" placeholder='search' value={searchelem} onChange={(e) => setSearchelem(e.target.value)} />
      <button type="button" className="btn btn-primary" onClick={handleclick}>
        <i className="fas fa-search"></i>
      </button>
    </div>
  )
}

export default SearchBar