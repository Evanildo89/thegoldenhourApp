const API_BASE_URL =
  window.location.hostname === "localhost" || window.location.hostname === "127.0.0.1"
    ? "http://127.0.0.1:8000"
    : "https://thegoldenhourapp.onrender.com";

export const getServices = async () => {
  const res = await fetch(`${API_BASE_URL}/api/services/`);
  if (!res.ok) throw new Error(`Erro ${res.status}`);
  return res.json();
};

export const getProfessionals = async () => {
  const res = await fetch(`${API_BASE_URL}/api/professionals/`);
  if (!res.ok) throw new Error(`Erro ${res.status}`);
  return res.json();
};

export const postReview = async (data) => {
  const res = await fetch(`${API_BASE_URL}/api/reviews/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });

  const json = await res.json();
  if (!res.ok) throw new Error(json.error || "Erro ao enviar avaliação");
  return json;
};
