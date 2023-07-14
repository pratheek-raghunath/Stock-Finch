import {useState,useEffect} from 'react'
import {useSearchParams} from 'react-router-dom'

const Company = () => {
    const [searchParams, setSearchParams] = useSearchParams();
    const cid = searchParams.get("cid")
    const token=sessionStorage.getItem('token')
    const [company,setCompany]=useState('')

    useEffect(()=>{
        const getCompany=async()=>{
          const companyFromServer=await fetchCompany()
          setCompany(companyFromServer)
        }
        getCompany()
      },[])
    
      //fetch
      const fetchCompany= async()=>{
        const opts = {
          headers: {
              'Authorization': 'Bearer '+token
          }
      };
        const res =await fetch(
          `${process.env.REACT_APP_API}/company/${cid}`,opts)
          const company =await res.json()
          return company     
    }
 
    return (
        company && (
            <div className='newspage'>
                <h1 className='headline'>{company.name}</h1>
                <div>
                    <h4>SECTOR: {company.sector}</h4>
                    <br/>
                    <h4>NSE: {company.details.nse}</h4>
                    <h4>BSE: {company.details.bse}</h4>
                    <h4>ISIN: {company.details.isin}</h4>
                    <h4>SERIES: {company.details.series}</h4>
                </div>
                <br/>
                <div>
                    <h2>Company Management</h2>
                    <table className="table">
                        <thead className="thead-dark">
                            <tr>
                            <th scope="col">Name</th>
                            <th scope="col">Designation</th>
                            </tr>
                        </thead>
                        <tbody>
                            {company.management.map(manager =>
                                <tr>
                                    <th scope="row">{manager.name}</th>
                                    <td>{manager.designation}</td>
                                </tr>
                            )}
                        </tbody>
                    </table>
                </div>
                <br/>
                <div>
                    <h2>Company Overview</h2>
                    <table className="table">
                        <thead className="thead-dark">
                            <tr>
                            <th scope="col">Parameter</th>
                            <th scope="col">Value</th>
                            </tr>
                        </thead>
                        <tbody>
                            {Object.keys(company.overview).map((keyName, i) => (
                                <tr>
                                    <th scope="row">{keyName}</th>
                                    <td>{company.overview[keyName]}</td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            </div>    
        )
    )
}

export default Company

{/* <div className='newspage'>
                <h1 className='headline'>{company.name}</h1>
                <div>
                    <h4>NSE: {company.details.nse}</h4>
                    <h4>BSE: {company.details.bse}</h4>
                    <h4>ISIN: {company.details.isin}</h4>
                    <h4>SERIES: {company.details.series}</h4>
                </div>
                <p>{company.name}</p>
                <p className='news-para'>{company.name}</p>
            </div>  */}