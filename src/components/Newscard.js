import {Link} from "react-router-dom"
const Newscard = ({ news}) => {
    return (
        <div>
          
        {news&&news.map((news) => (
         <div style={{ cursor:'pointer'}} key={news.id} className="newssection">
             <Link to={`/news/${news.id}`} >
             <img src={news.image_url}></img>
             <h2 className="headlineout">{news.headline}</h2>
            </Link>
            </div>
            )) 
           }
        
      </div>
      
     
    )
}

export default Newscard
