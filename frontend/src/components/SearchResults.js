import SearchCard from './SearchCard'
import {useState,useEffect, useContext} from 'react'
import { useNavigate, useSearchParams } from 'react-router-dom'

import {LoginContext} from './Context'


const SearchResults = ( ) => {
    const [searchParams, setSearchParams] = useSearchParams();
    const query = searchParams.get("query")

    const [searchResults,setSearchResults]=useState({has_prev:false,has_next:false,prev:null,next:null,results:[]})
    const {loggedIn,setloggedIn}=useContext(LoginContext)

    const token=sessionStorage.getItem('token')
    let navigate=useNavigate();

    //fetch
    const fetchSearchResult= async()=>{
        const opts = {
            headers: {
                'Authorization': 'Bearer '+token
            },
            }
        const res =await fetch(
            process.env.REACT_APP_API + '/search?query=' + query,opts)
        const searchResults =await res.json()
        return searchResults 
        
        }

    useEffect(()=>{
        const getSearchResults=async()=>{
        const searchResultsFromServer=await fetchSearchResult()
        setSearchResults(searchResultsFromServer)
        }
        getSearchResults()
    },[query])

    
    const prevPage =()=>{
        const opts = {
            headers: {
                'Authorization': 'Bearer '+token
            },
        }
        fetch(searchResults.prev,opts)
        .then(res => res.json())
        .then(data => {
            setSearchResults(data)
            window.scrollTo(0, 0)
        })
    }

    const nextPage =()=>{
        const opts = {
            headers: {
                'Authorization': 'Bearer '+token
            },
        }
        fetch(searchResults.next,opts)
        .then(res => res.json())
        .then(data => {
            setSearchResults(data)
        window.scrollTo(0, 0)
        })
    }


    return (
        <div>
             {loggedIn ?(
            <div>
                <div className='vector-top-bg'>
                    <p className='para-top'>Search results</p>
                </div><div>
                {searchResults.results.map((searchResult)=>
                        //<div key={searchResult.cid}>{searchResult.cid}</div>)
                        <SearchCard key={searchResult.id} search={searchResult} />)
                        }

                    </div><div className='d-flex justify-content-center'>
                        {searchResults.has_prev && <button className="btn btn-primary pagebtn" onClick={prevPage}>prev</button>}
                        {searchResults.has_next && <button className="btn btn-primary pagebtn" onClick={nextPage}>next</button>}
                    </div>
                    </div>):
                    (navigate('/login'))}
        </div>
    )
    
}

export default SearchResults



