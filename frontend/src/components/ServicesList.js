import React, {useEffect, useState} from 'react';
import { useNavigate } from "react-router-dom";

export default function ServicesList(){
  const [services, setServices] = useState([]);
  const navigate = useNavigate();

  useEffect(()=>{
    fetch('http://localhost:8000/api/services/')
      .then(r => r.json())
      .then(data => setServices(data))
      .catch(err => console.error(err));
  },[]);

  return (
    <div>
      <h2>Serviços</h2>
      <div className="services-grid">
        {services.map(s => (
          <div key={s.id} className="service-card">
            <h3>{s.title}</h3>
            <p>{s.description}</p>
            <p>Duração: {s.duration_minutes} min</p>
            {s.price && <p>Preço: €{s.price}</p>}
            <button onClick={()=>navigate(`/service/${s.id}`)}>Detalhes / Marcar</button>
          </div>
        ))}
      </div>
    </div>
  );
}