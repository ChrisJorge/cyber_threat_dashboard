import React from 'react'
import '../styling/Overview.css'
const Overview = ({total, critical, high, medium, low}) => {
  return (
    <div className="overViewContainer">
        <div className="statContainer">
            <p>{total}</p>
            <p>Total Threats</p>
        </div>
        <div className="statContainer">
            <p>{critical}</p>
            <p>Critical Threats</p>
        </div>
        <div className="statContainer">
            <p>{high}</p>
            <p>High Threats</p>
        </div>
        <div className="statContainer">
            <p>{medium}</p>
            <p>Medium Threats</p>
        </div>
        <div className="statContainer">
            <p>{low}</p>
            <p>Low Threats</p>
        </div>
    </div>
  )
}

export default Overview