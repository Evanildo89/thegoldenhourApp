import React from "react";
import { useNavigate, useParams } from "react-router-dom";
import { FaArrowLeft } from "react-icons/fa";
import BookingForm from "./BookingForm";
import "./ServiceDetail.css";

export default function ServiceDetail() {
  const navigate = useNavigate();
  const { id } = useParams(); // id do serviço vindo da URL
  const [service, setService] = React.useState(null);

  React.useEffect(() => {
    fetch(`http://localhost:8000/api/services/${id}/`)
      .then(r => r.json())
      .then(data => setService(data))
      .catch(err => console.error(err));
  }, [id]);

  if (!service) return <p>Carregando...</p>;

  return (
    <div className="service-detail-container">
      {/* Header com seta e nome */}
      <div className="service-detail-header">
        <div className="back-circle" onClick={() => navigate(-1)}>
          <FaArrowLeft className="back-arrow" />
        </div>
        <h2>{service.title}</h2>
      </div>

      {/* Conteúdo */}
      <div className="service-detail-content">
        <p>{service.description}</p>
        <p>Duração: {service.duration_minutes} min</p>
        {service.price && <p>Preço: €{service.price}</p>}

        {/* Botão para reservar / abrir BookingForm */}
        <BookingForm service={service} />
      </div>
    </div>
  );
}