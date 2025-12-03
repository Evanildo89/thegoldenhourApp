import React, { useState, useRef, useEffect } from 'react';
//import ServicesList from './components/ServicesList';
import './styles.css';
import LogoImg from './assets/3.png';
//import EquipeImg from './assets/vansophie.jpg';
import { FaPhoneAlt, FaInstagram, FaRegCalendarAlt } from "react-icons/fa";
import { X } from "lucide-react"; // npm install lucide-react
import { getServices, getProfessionals, postReview } from './api';


const PHONE_NUMBER = '+351 961 292 916'; // seu número

const pacotePages = {
  1: 'pacote-essencia-gravida.html',
  2: 'pacote-eterno-gravida.html',
  3: 'pacote-essencia-crianca.html',
  4: 'pacote-eterno-crianca.html',
  5: 'pacote-essencia-familia.html',
  6: 'pacote-eterno-familia.html',
};

const operatingHoursDisplay = {
  "domingo": "Fechado",
  "segunda-feira": "Fechado",
  "terça-feira": "Aberto - Fecha às 24:00",
  "quarta-feira": "Aberto - Fecha às 24:00",
  "quinta-feira": "Aberto - Fecha às 24:00",
  "sexta-feira": "Aberto - Fecha às 24:00",
  "sabado": "Aberto - Fecha às 24:00",
};

const operatingHoursFull = {
  "domingo": "Fechado",
  "segunda-feira": "Fechado",
  "terça-feira": "07:00 - 24:00",
  "quarta-feira": "07:00 - 24:00",
  "quinta-feira": "07:00 - 24:00",
  "sexta-feira": "07:00 - 24:00",
  "sabado": "07:00 - 24:00",
};

function App() {

   const [activeNav, setActiveNav] = useState('servicos'); // link ativo inicial
   const [openHours, setOpenHours] = useState(false);
   const [services, setServices] = useState([]);
   const servicesRef = useRef(null);
   const equipaRef = useRef(null);
const avaliacoesRef = useRef(null);
   const [showPolicy, setShowPolicy] = useState(false);
   const [showBox, setShowBox] = useState(false);
   const [rating, setRating] = useState(0)
   const [name, setName] = useState("");
const [email, setEmail] = useState("");
const [comment, setComment] = useState("");
const [errors, setErrors] = useState({})
 const [professionals, setProfessionals] = useState([]);
 const [loading, setLoading] = useState(false);
 const [success, setSuccess] = useState(false);

  const handleNavClick = (id) => {
    setActiveNav(id);
  };

  const toggleHours = () => setOpenHours(!openHours);

  const days = ['domingo', 'segunda-feira', 'terça-feira', 'quarta-feira', 'quinta-feira', 'sexta-feira', 'sabado'];
  const today = days[new Date().getDay()];
  const todayStatus = operatingHoursDisplay[today];

  const scrollToServices = () => {
  if (servicesRef.current) {
    servicesRef.current.scrollIntoView({ behavior: 'smooth' });
  }
};

 const handleSubmit = async () => {
  let newErrors = {};

  if (rating === 0) newErrors.rating = "Selecione uma classificação.";
  if (!name.trim()) newErrors.name = "Por favor, insira seu nome.";
  if (!email.trim()) newErrors.email = "Por favor, insira seu email.";
  if (!comment.trim()) newErrors.comment = "Por favor, insira sua avaliação.";

  setErrors(newErrors);

  if (Object.keys(newErrors).length === 0) {
    setLoading(true); // ativa spinner
    setSuccess(false);

    setTimeout(async () => {
      try {
        await postReview({ name, email, rating, comment });

        // limpa campos
        setRating(0);
        setName("");
        setEmail("");
        setComment("");

        setSuccess(true); // mostra mensagem de sucesso
      } catch (err) {
        console.error(err);
        alert(err.message || "Erro ao enviar avaliação. Tente novamente.");
      } finally {
        setLoading(false); // desativa spinner
      }
    }, 2000);
  }
};


  useEffect(() => {
  getServices()
    .then(setServices)
    .catch(err => console.error('Erro ao buscar serviços:', err));
}, []);

  useEffect(() => {
  getProfessionals()
    .then(setProfessionals)
    .catch(err => console.error('Erro ao buscar profissionais:', err));
}, []);

  useEffect(() => {
    console.log('Professionals:', professionals);
  }, [professionals]);


  useEffect(() => {
  const sections = [
    { id: 'servicos', ref: servicesRef },
    { id: 'equipa', ref: equipaRef },
    { id: 'avaliacoes', ref: avaliacoesRef },
  ];


  const observer = new IntersectionObserver(
  (entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        setActiveNav(entry.target.id);
      }
    });
  },
  {
    root: null,
    threshold: 0.5,
rootMargin: '-20% 0px -20% 0px'

  }
);

  sections.forEach(section => {
    if (section.ref.current) observer.observe(section.ref.current);
  });

  return () => {
    sections.forEach(section => {
      if (section.ref.current) observer.unobserve(section.ref.current);
    });
  };
}, []);

  console.log('Professionals:', professionals);


  return (
    <div className="app-container">
  <div className="top-strip">
    <a href={`tel:${PHONE_NUMBER.replace(/\s+/g, '')}`}>
      <FaPhoneAlt style={{ marginRight: '8px' }} />
      Ligar agora {PHONE_NUMBER}
    </a>
  </div>

  <nav className="nav-bar">
    <ul>
      <li><a href="#servicos" className={activeNav === 'servicos' ? 'active' : ''} onClick={() => handleNavClick('servicos')}>Serviços</a></li>
      <li><a href="#equipa" className={activeNav === 'equipa' ? 'active' : ''} onClick={() => handleNavClick('equipa')}>Equipa</a></li>
      <li><a href="#avaliacoes" className={activeNav === 'avaliacoes' ? 'active' : ''} onClick={() => handleNavClick('avaliacoes')}>Avaliações</a></li>
    </ul>
  </nav>

  {(activeNav === 'servicos' || activeNav === 'equipa') && (
    <div className="logo-text-container">
      <div className="logo-container">
        <img src={LogoImg} alt="Logo" />
      </div>
      <div className="logo-text">
        The Golden Light Photography
      </div>
    </div>
  )}

  {(activeNav === 'servicos' || activeNav === 'equipa') && (
    <div className="hours-container">
  <div className="today-hours" onClick={toggleHours}>
    <span>{todayStatus}</span>
    <span className={`arrow ${openHours ? 'open' : ''}`}>▼</span>
  </div>
  {openHours && (
    <ul className="full-hours">
      {Object.entries(operatingHoursFull).map(([day, hours]) => (
  <li key={day}>
    <span className="day">{day.charAt(0).toUpperCase() + day.slice(1)}</span>
    <span className="status">{hours}</span>
  </li>
))}
    </ul>
  )}
</div>
  )}
    {(activeNav === 'servicos' || activeNav === 'equipa') && (
  <>
    <div className="policy-box">
      <h2>Nossa política de reservas</h2>
      <p className="policy-warning">
        <strong>AVISO!!!</strong><br />
        Após o agendamento, caso queira cancelar, faça-o com antecedência.<br />
        Em caso de <strong>Não COMPARECÊNCIA</strong> será cobrado metade do <strong>VALOR DO SERVIÇO!</strong><br />
        Obrigado.
      </p>
      <div className="policy-button">
        <button onClick={scrollToServices}>OK</button>
      </div>
    </div>

    <h2 className="services-title" ref={servicesRef} id="servicos">
      Serviços
    </h2>
    <p className="services-subtitle">Serviços</p>

    <div className="services-container">
  {services.map((service) => (
    <div className="service-section" key={service.id}>
      <h3 className="service-title">{service.title}</h3>
      <ul className="service-description">
        <li>Tempo de sessão: {service.duration_minutes} minutos</li>
        {service.description.split('\n').map((line, idx) => (
          <li key={idx}>{line}</li>
        ))}
        <li>Valor base: {service.price}€</li>
      </ul>
      <div
  className="service-arrow"
  onClick={() => {
    const serviceData = services.find(s => s.id === service.id);
    const query = new URLSearchParams({
      service_id: service.id,
      title: serviceData.title,
      price: serviceData.price,
      duration: serviceData.duration_minutes
    }).toString();

    window.location.href = `/${pacotePages[service.id]}?${query}`;
  }}
>
  &gt;
</div>
    </div>
  ))}
</div>
  </>
)}



 <hr className="team-separator" />

 <>
  <div className="team-section"> {/* Mantém o container para o layout */}
  <h2 className="team-title" ref={equipaRef} id="equipa">Equipa</h2>
  <p className="team-subtitle">
    Conheça os profissionais que dão vida à The Golden Light Photography.
  </p>

  <div className="team-container">
  {professionals.map(prof => {
    console.log('Photo URL:', prof.photo);
    return (
      <div className="team-box" key={prof.id}>
        <div className="team-image-container">
          <img src={prof.photo} alt={prof.name} />
        </div>
        <div className="team-info">
          <h3 className="team-name">{prof.name}</h3>
          <p className="team-role">{prof.bio}</p>
        </div>
      </div>
    )
  })}

  <div
  className="service-arrow-equipe"
  onClick={() => {
    if (professionals.length === 0) return;

    if (!services || services.length === 0) {
      alert("Os serviços ainda estão carregando. Aguarde um momento.");
      return;
    }

    const lastProf = professionals[professionals.length - 1];
    const profData = {
      id: lastProf.id,
      name: lastProf.name,
      bio: lastProf.bio,
      photo: lastProf.photo,
    };

    const servicesData = encodeURIComponent(JSON.stringify(services));
    const profQuery = encodeURIComponent(JSON.stringify(profData));

    window.location.href = `/servicos.html?data=${servicesData}&prof=${profQuery}`;
  }}
>
  &gt;
</div>
</div>
</div>

  <hr className="team-separator" />

  <div className="contact-container">
    <div className="contact-text">Contactar-nos</div>
    <div className="contact-phone">
      <FaPhoneAlt className="phone-icon" />
      <a href="tel:+351912345678" className="phone-number">
        {PHONE_NUMBER}
      </a>
    </div>

    <a
      href="https://www.instagram.com/thegoldenhour.photography?igsh=MThkMHR0d21pZ2VleQ=="
      target="_blank"
      rel="noopener noreferrer"
      className="instagram-link"
    >
      <FaInstagram className="instagram-icon" />
      <span className="instagram-text">
        https://www.instagram.com/thegoldenhour.photography?igsh=MThkMHR0d21pZ2VleQ==
      </span>
    </a>
  </div>
</>

    <div className="bom-saber-container">
        <div className="bom-saber-title">Bom Saber</div>

        <div className="bom-saber-link" onClick={() => setShowPolicy(true)}>
  <FaRegCalendarAlt className="calendar-icon" />
  <span className="bom-saber-text">Política de Reservas</span>
</div>
      </div>

      {showPolicy && (activeNav === 'servicos' || activeNav === 'avaliacoes') && (
  <div className="policy-box-overlay">
    <div className="policy-box">
      <h2>Nossa política de reservas</h2>
      <p className="policy-warning">
        <strong>AVISO!!!</strong><br />
        Após o agendamento, caso queira cancelar, faça-o com antecedência.<br />
        Em caso de <strong>Não COMPARECÊNCIA</strong> será cobrado metade do <strong>VALOR DO SERVIÇO!</strong><br />
        Obrigado.
      </p>
      <div className="policy-button">
        <button onClick={() => { setShowPolicy(false); scrollToServices(); }}>OK</button>
      </div>
    </div>
  </div>
)}
<hr className="team-separator" />

 <h2 className="Avalicao-title" ref={avaliacoesRef} id="avaliacoes">Avaliações</h2>
 <p className="avaliacao-text">
  Seja o primeiro a nos avaliar e compartilhar suas impressões sobre a sua experiência.
</p>

 <div className="avaliacao-button-container">
  <button className="avaliacao-button" onClick={() => setShowBox(true)}>
    Escrever uma avaliação
  </button>
</div>

<hr className="avaliacao-separator" />

 <div className="reservar-button-container">
  <button
    className="reservar-button"
    onClick={() => {
      if (equipaRef.current) {
        equipaRef.current.scrollIntoView({ behavior: "smooth" });
      }
    }}
  >
    Reservar Agora
  </button>
</div>

 {showBox && (
  <>
    <div className="avaliacao-overlay" onClick={() => setShowBox(false)}></div>
    <div className="avaliacao-box">
      <div className="avaliacao-header">
        <h3>Escrever uma avaliação</h3>
        <button className="fechar-btn" onClick={() => setShowBox(false)}>
          <X size={22} />
        </button>
      </div>

      <div className="avaliacao-conteudo">
        {!success ? (
          <>
            {!loading ? (
              <>
                {/* Avaliação em estrelas */}
                <div className="avaliacao-rating">
                  <label className="avaliacao-label">
                    A sua classificação <span className="obrigatorio">*</span>
                  </label>
                  <div className="stars">
                    {[1,2,3,4,5].map(star => (
                      <span
                        key={star}
                        className={`star ${star <= rating ? "filled" : ""}`}
                        onClick={() => setRating(star)}
                      >
                        ★
                      </span>
                    ))}
                  </div>
                  {errors.rating && <span className="avaliacao-error">{errors.rating}</span>}
                </div>

                {/* Nome */}
                <div className="avaliacao-field">
                  <label className="avaliacao-label">
                    Nome completo <span className="obrigatorio">*</span>
                  </label>
                  <input
                    type="text"
                    className="avaliacao-input"
                    placeholder="Seu nome"
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                  />
                  {errors.name && <span className="avaliacao-error">{errors.name}</span>}
                </div>

                {/* Email */}
                <div className="avaliacao-field">
                  <label className="avaliacao-label">
                    Email <span className="obrigatorio">*</span>
                  </label>
                  <input
                    type="email"
                    className="avaliacao-input"
                    placeholder="seuemail@exemplo.com"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                  />
                  {errors.email && <span className="avaliacao-error">{errors.email}</span>}
                </div>

                {/* Comentário */}
                <div className="avaliacao-field">
                  <label className="avaliacao-label">
                    Avaliação <span className="obrigatorio">*</span>
                  </label>
                  <textarea
                    className="avaliacao-textarea"
                    placeholder="Compartilhe sua experiência..."
                    value={comment}
                    onChange={(e) => setComment(e.target.value)}
                  ></textarea>
                  {errors.comment && <span className="avaliacao-error">{errors.comment}</span>}
                </div>

                <button className="avaliacao-enviar" onClick={handleSubmit}>
                  Enviar Avaliação
                </button>
              </>
            ) : (
              <div className="loading">
                <div className="spinner"></div> Aguarde...
              </div>
            )}
          </>
        ) : (
          <div className="success-message">
            Comentário enviado com sucesso!
          </div>
        )}
      </div>
    </div>
  </>
)}
    </div>
  );
}

export default App;
