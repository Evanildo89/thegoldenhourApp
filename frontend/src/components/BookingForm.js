import React, {useState} from 'react';


export default function BookingForm({service, onClose}){
    const [form, setForm] = useState({name:'', email:'', phone:'', date:'', time:'', notes:''});
    const [message, setMessage] = useState('');


    function handleChange(e){
    setForm({...form, [e.target.name]: e.target.value});
}


function submit(e){
    e.preventDefault();
    const payload = {...form, service: service.id};
    fetch('http://localhost:8000/api/bookings/',{
    method:'POST',
    headers:{'Content-Type':'application/json'},
    body: JSON.stringify(payload)
    }).then(r=>{
    if(r.ok){
    setMessage('Reserva enviada! Entrarei em contacto em breve.');
    setForm({name:'', email:'', phone:'', date:'', time:'', notes:''});
    setTimeout(()=> onClose(), 1500);
    } else {
    r.json().then(d=> setMessage('Erro: ' + JSON.stringify(d)));
    }
    }).catch(err=> setMessage('Erro: ' + err.message));
}


return (
    <div className="booking-modal">
        <h3>Marcar: {service.title}</h3>
        <form onSubmit={submit}>
        <input name="name" value={form.name} onChange={handleChange} placeholder="Nome" required />
        <input name="email" value={form.email} onChange={handleChange} placeholder="Email" type="email" required />
        <input name="phone" value={form.phone} onChange={handleChange} placeholder="Telemóvel" />
        <input name="date" value={form.date} onChange={handleChange} type="date" required />
        <input name="time" value={form.time} onChange={handleChange} type="time" required />
        <textarea name="notes" value={form.notes} onChange={handleChange} placeholder="Notas (opcional)" />
        <div style={{marginTop:10}}>
        <button type="submit">Enviar</button>
        <button type="button" onClick={onClose}>Fechar</button>
        </div>
        </form>
        {message && <p>{message}</p>}
        </div>
    )
}