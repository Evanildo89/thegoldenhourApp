import React from "react";
import LogoImg from "../assets/3.png"; // logo
import EquipeImg from "../assets/vansophie.jpg"; // imagem da equipe
import { FaArrowLeft } from "react-icons/fa";
import "./Pacote.css"; // CSS específico

export default function PacoteEssenciaGravida() {
  return (
    <div className="pacote-container">
      {/* Topo */}
      <div className="pacote-topo">
        <FaArrowLeft className="back-arrow" onClick={() => window.history.back()} />
        <div className="logo-circle">
          <img src={LogoImg} alt="Logo" />
        </div>
        <div className="empresa-nome">The Golden Light Photography</div>
      </div>

      {/* Equipe */}
      <div className="team-box">
        <div className="team-image-container">
          <img src={EquipeImg} alt="Equipe" />
        </div>
        <div className="team-info">
          <h3 className="team-name">VANESSA "VANSOPHIE"</h3>
          <p className="team-role">Fundadora</p>
        </div>
      </div>

      {/* Box de preço */}
      <div className="preco-box">
        <span>120€</span>
        <span className="arrow-down">▼</span>
      </div>
    </div>
  );
}