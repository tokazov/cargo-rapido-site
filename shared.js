// Cargo Rapido — Shared JS
function toggleMenu() {
  const nav = document.getElementById('main-nav');
  if (nav) nav.classList.toggle('open');
}

// Highlight active nav item
document.addEventListener('DOMContentLoaded', function() {
  const path = window.location.pathname;
  document.querySelectorAll('header a').forEach(a => {
    if (a.getAttribute('href') && a.getAttribute('href') !== '/' && path.startsWith(a.getAttribute('href'))) {
      a.style.color = '#1a237e';
      a.style.background = '#f4f5ff';
    }
  });
});
