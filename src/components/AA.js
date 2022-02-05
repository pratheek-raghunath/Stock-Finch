import React from 'react';
import { useState, useEffect } from 'react';
import { Navigate, useNavigate } from 'react-router-dom'


const AA = () => {


    const [count, setCount] = useState(0);
    let navigate=useNavigate();

  
    // Similar to componentDidMount and componentDidUpdate:
    useEffect(() => {
      // Update the document title using the browser API
      document.title = `You clicked ${count} times`;
      <Navigate to='/'/>
    });
  
    return (
      <div>
        <p>You clicked {count} times</p>
        <button onClick={() => setCount(count + 1)}>
          Click me
        </button>
      </div>
    );
  }


export default AA;
