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
  
  initCookieBanner();
  initWhatsAppWidget();
});

// ===== COOKIE BANNER =====
function initCookieBanner() {
  // Метрика и GTM грузятся сразу независимо от выбора
  if (localStorage.getItem('cookie_consent')) return;
  
  const banner = document.createElement('div');
  banner.id = 'cookie-banner';
  banner.innerHTML = `
    <div class="cookie-banner-inner">
      <p>Мы используем cookies для аналитики. Подробнее в 
        <a href="/politika-konfidencialnosti/">Политике конфиденциальности</a>
      </p>
      <div class="cookie-banner-btns">
        <button class="cookie-btn-accept" onclick="acceptCookies()">Принять</button>
        <a href="/politika-konfidencialnosti/" class="cookie-btn-more">Подробнее</a>
      </div>
    </div>
  `;
  document.body.appendChild(banner);
  
  // Show with animation
  setTimeout(() => banner.classList.add('visible'), 300);
}

function acceptCookies() {
  localStorage.setItem('cookie_consent', '1');
  const banner = document.getElementById('cookie-banner');
  if (banner) {
    banner.classList.remove('visible');
    setTimeout(() => banner.remove(), 400);
  }
}

// ===== WHATSAPP + TELEGRAM WIDGET (3 round buttons) =====
function initWhatsAppWidget() {
  const widget = document.createElement('div');
  widget.id = 'wa-widget';
  widget.innerHTML = `
    <div class="wa-bubble" id="wa-bubble">
      <div class="wa-bubble-avatar">👩</div>
      <div class="wa-bubble-text">Здравствуйте! Готова рассчитать стоимость доставки 😊<span style="display:block;font-size:12px;color:#888;margin-top:4px;">— Наталья</span></div>
      <button class="wa-bubble-close" onclick="closeBubble()">×</button>
    </div>
    <div class="wa-buttons">
      <a href="https://t.me/CARGORAPIDO" target="_blank" class="wa-btn wa-btn-tg" aria-label="Telegram">
        <svg width="26" height="26" viewBox="0 0 24 24" fill="white"><path d="M11.944 0A12 12 0 0 0 0 12a12 12 0 0 0 12 12 12 12 0 0 0 12-12A12 12 0 0 0 12 0a12 12 0 0 0-.056 0zm4.962 7.224c.1-.002.321.023.465.14a.506.506 0 0 1 .171.325c.016.093.036.306.02.472-.18 1.898-.962 6.502-1.36 8.627-.168.9-.499 1.201-.82 1.23-.696.065-1.225-.46-1.9-.902-1.056-.693-1.653-1.124-2.678-1.8-1.185-.78-.417-1.21.258-1.91.177-.184 3.247-2.977 3.307-3.23.007-.032.014-.15-.056-.212s-.174-.041-.249-.024c-.106.024-1.793 1.14-5.061 3.345-.48.33-.913.49-1.302.48-.428-.008-1.252-.241-1.865-.44-.752-.245-1.349-.374-1.297-.789.027-.216.325-.437.893-.663 3.498-1.524 5.83-2.529 6.998-3.014 3.332-1.386 4.025-1.627 4.476-1.635z"/></svg>
      </a>
      <a href="https://wa.me/995568644615" target="_blank" class="wa-btn wa-btn-wa" aria-label="WhatsApp">
        <svg width="26" height="26" viewBox="0 0 24 24" fill="white"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413Z"/></svg>
      </a>
      <a href="tel:+995568644615" class="wa-btn wa-btn-call" aria-label="Позвонить">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="white"><path d="M6.62 10.79c1.44 2.83 3.76 5.14 6.59 6.59l2.2-2.2c.27-.27.67-.36 1.02-.24 1.12.37 2.33.57 3.57.57.55 0 1 .45 1 1V20c0 .55-.45 1-1 1-9.39 0-17-7.61-17-17 0-.55.45-1 1-1h3.5c.55 0 1 .45 1 1 0 1.25.2 2.45.57 3.57.11.35.03.74-.25 1.02l-2.2 2.2z"/></svg>
      </a>
    </div>
  `;
  document.body.appendChild(widget);

  // Show bubble after 30 seconds if not shown this session
  if (!sessionStorage.getItem('wa_bubble_shown')) {
    setTimeout(() => {
      const bubble = document.getElementById('wa-bubble');
      if (bubble) {
        bubble.classList.add('visible');
        sessionStorage.setItem('wa_bubble_shown', '1');
      }
    }, 30000);
  }
}

function closeBubble() {
  const bubble = document.getElementById('wa-bubble');
  if (bubble) bubble.classList.remove('visible');
}

// ===== CALCULATOR: Build Telegram link with form data =====
function buildTgLink(e) {
  var from = (document.getElementById('calc-from')?.value || '').trim();
  var to   = (document.getElementById('calc-to')?.value || '').trim();
  var type = (document.getElementById('calc-type')?.value || '').trim();
  var w    = (document.getElementById('calc-weight')?.value || '').trim();

  var parts = [];
  if (from) parts.push('Откуда: ' + from);
  if (to)   parts.push('Куда: ' + to);
  if (type) parts.push('Груз: ' + type);
  if (w)    parts.push('Вес: ' + w + ' кг');

  if (parts.length > 0) {
    var text = 'Хочу рассчитать стоимость доставки\n' + parts.join('\n');
    e.currentTarget.href = 'https://t.me/CARGORAPIDO?text=' + encodeURIComponent(text);
  } else {
    e.currentTarget.href = 'https://t.me/CARGORAPIDO';
  }
}
