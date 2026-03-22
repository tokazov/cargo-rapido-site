// Cargo Rapido — Shared JS

function toggleMenu() {
  document.getElementById('main-nav').classList.toggle('open');
}

// Request form → WhatsApp
function submitForm(e) {
  e.preventDefault();
  const form = e.target;
  const name = form.querySelector('[name=name]')?.value || '';
  const phone = form.querySelector('[name=phone]')?.value || '';
  const from = form.querySelector('[name=from]')?.value || '';
  const to = form.querySelector('[name=to]')?.value || '';
  const cargo = form.querySelector('[name=cargo]')?.value || '';
  const weight = form.querySelector('[name=weight]')?.value || '';
  
  const msg = `Заявка с сайта cargorapido.com\n\nИмя: ${name}\nТелефон: ${phone}\nОткуда: ${from}\nКуда: ${to}\nГруз: ${cargo}\nВес: ${weight} кг`;
  const url = `https://wa.me/995568644615?text=${encodeURIComponent(msg)}`;
  window.open(url, '_blank');
}

document.addEventListener('DOMContentLoaded', () => {
  const form = document.querySelector('.request-form form');
  if (form) form.addEventListener('submit', submitForm);
  
  // Smooth scroll
  document.querySelectorAll('a[href^="#"]').forEach(a => {
    a.addEventListener('click', e => {
      e.preventDefault();
      const el = document.querySelector(a.getAttribute('href'));
      if (el) el.scrollIntoView({ behavior: 'smooth' });
    });
  });
});
