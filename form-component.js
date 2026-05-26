// Cargo Rapido — Form Component
// TODO: подключить /api/submit когда будет BOT_TOKEN и CHAT_ID

(function() {
  'use strict';
  
  const CITIES_FROM = [
    'Тбилиси', 'Батуми', 'Кутаиси', 'Рустави', 'Гори', 'Другой город Грузии'
  ];
  
  const CITIES_TO = [
    'Москва', 'Санкт-Петербург', 'Краснодар', 'Ростов-на-Дону',
    'Алматы', 'Астана', 'Минск', 'Киев', 'Берлин', 'Варшава', 
    'Стамбул', 'Другой город'
  ];
  
  const CARGO_TYPES = [
    'Личные вещи / переезд', 'Коммерческий груз', 'Автомобиль',
    'Посылка / документы', 'Продукты питания (термо)', 'Другое'
  ];
  
  const CONTACT_PREF = ['Telegram', 'WhatsApp', 'Телефон', 'Email'];
  
  function createFormHTML(formId) {
    return `
      <form class="cr-form" id="${formId}" onsubmit="CRForm.submit(event, '${formId}')">
        <!-- Honeypot -->
        <input type="text" name="website" style="display:none" tabindex="-1" autocomplete="off">
        
        <div class="cr-form-grid">
          <div class="cr-field">
            <label for="${formId}-name">Ваше имя <span class="req">*</span></label>
            <input type="text" id="${formId}-name" name="name" placeholder="Александр" required>
          </div>
          
          <div class="cr-field">
            <label for="${formId}-phone">Телефон <span class="req">*</span></label>
            <input type="tel" id="${formId}-phone" name="phone" placeholder="+995 XX XXX XX XX" required>
          </div>
          
          <div class="cr-field">
            <label for="${formId}-from">Откуда</label>
            <select id="${formId}-from" name="from_city">
              <option value="">Выберите город</option>
              ${CITIES_FROM.map(c => `<option value="${c}">${c}</option>`).join('')}
            </select>
          </div>
          
          <div class="cr-field">
            <label for="${formId}-to">Куда</label>
            <select id="${formId}-to" name="to_city">
              <option value="">Выберите город</option>
              ${CITIES_TO.map(c => `<option value="${c}">${c}</option>`).join('')}
            </select>
          </div>
          
          <div class="cr-field">
            <label for="${formId}-cargo">Тип груза</label>
            <select id="${formId}-cargo" name="cargo_type">
              <option value="">Выберите тип</option>
              ${CARGO_TYPES.map(c => `<option value="${c}">${c}</option>`).join('')}
            </select>
          </div>
          
          <div class="cr-field">
            <label for="${formId}-weight">Вес груза (кг)</label>
            <input type="number" id="${formId}-weight" name="weight" placeholder="50" min="0" step="0.1">
          </div>
          
          <div class="cr-field">
            <label for="${formId}-contact">Предпочтительный способ связи</label>
            <select id="${formId}-contact" name="contact_pref">
              <option value="">Выберите</option>
              ${CONTACT_PREF.map(c => `<option value="${c}">${c}</option>`).join('')}
            </select>
          </div>
          
          <div class="cr-field cr-field-full">
            <label for="${formId}-comment">Комментарий</label>
            <textarea id="${formId}-comment" name="comment" placeholder="Дополнительная информация о грузе..." rows="3"></textarea>
          </div>
          
          <div class="cr-field cr-field-full cr-consent">
            <label class="cr-checkbox-label">
              <input type="checkbox" name="consent" required id="${formId}-consent">
              <span>Я согласен(а) с <a href="/politika-konfidencialnosti/" target="_blank">Политикой конфиденциальности</a> и даю согласие на обработку персональных данных</span>
            </label>
          </div>
        </div>
        
        <div class="cr-form-actions">
          <button type="submit" class="cr-submit-btn">
            <i class="fas fa-paper-plane"></i> Отправить заявку
          </button>
        </div>
        
        <div class="cr-success" id="${formId}-success" style="display:none">
          <div class="cr-success-icon">✅</div>
          <h3>Спасибо! Заявка получена.</h3>
          <p>Менеджер свяжется с вами в течение <strong>15 минут</strong>.</p>
          <p style="margin-top:8px;color:#888;font-size:14px;">Пн-Сб 10:00–17:00. Вне рабочего времени — ответим утром следующего дня.</p>
        </div>
      </form>
    `;
  }
  
  function initPhoneMask(input) {
    input.addEventListener('input', function(e) {
      let val = e.target.value.replace(/\D/g, '');
      if (val.startsWith('995')) {
        val = '+' + val.slice(0, 12);
      } else if (val.startsWith('7') || val.startsWith('8')) {
        val = '+' + val.slice(0, 11);
      } else if (val.length > 0) {
        val = '+' + val.slice(0, 15);
      }
      e.target.value = val;
    });
  }
  
  window.CRForm = {
    init: function(containerId, title) {
      const container = document.getElementById(containerId);
      if (!container) return;
      const formId = 'form-' + containerId;
      container.innerHTML = `
        <div class="cr-form-wrapper">
          ${title ? `<h2 class="cr-form-title">${title}</h2>` : ''}
          ${createFormHTML(formId)}
        </div>
      `;
      const phoneInput = container.querySelector('input[name="phone"]');
      if (phoneInput) initPhoneMask(phoneInput);
    },
    
    submit: async function(e, formId) {
      e.preventDefault();
      const form = document.getElementById(formId);
      if (!form) return;
      
      // Honeypot check
      const honeypot = form.querySelector('input[name="website"]');
      if (honeypot && honeypot.value) return;
      
      const btn = form.querySelector('.cr-submit-btn');
      if (btn) {
        btn.disabled = true;
        btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Отправляем...';
      }
      
      const data = {
        name: form.querySelector('[name="name"]')?.value || '',
        phone: form.querySelector('[name="phone"]')?.value || '',
        from_city: form.querySelector('[name="from_city"]')?.value || '',
        to_city: form.querySelector('[name="to_city"]')?.value || '',
        cargo_type: form.querySelector('[name="cargo_type"]')?.value || '',
        weight: form.querySelector('[name="weight"]')?.value || '',
        contact_pref: form.querySelector('[name="contact_pref"]')?.value || '',
        comment: form.querySelector('[name="comment"]')?.value || '',
      };
      
      // TODO: подключить /api/submit когда будет BOT_TOKEN и CHAT_ID
      // try {
      //   const resp = await fetch('/api/submit', {
      //     method: 'POST',
      //     headers: { 'Content-Type': 'application/json' },
      //     body: JSON.stringify(data)
      //   });
      //   if (!resp.ok) throw new Error('Server error');
      // } catch(err) {
      //   console.error('Form submit error:', err);
      // }
      
      // Заглушка — показываем успех
      console.log('Form data (stub):', data);
      
      // Show success message
      const successEl = document.getElementById(formId + '-success');
      if (successEl) {
        form.querySelector('.cr-form-grid').style.display = 'none';
        form.querySelector('.cr-form-actions').style.display = 'none';
        successEl.style.display = 'block';
      }
    }
  };
  
  // Auto-init all [data-cr-form] elements
  document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('[data-cr-form]').forEach(el => {
      CRForm.init(el.id, el.dataset.crFormTitle || 'Оставить заявку');
    });
  });
})();
