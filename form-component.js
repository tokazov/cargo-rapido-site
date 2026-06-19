// Cargo Rapido — Form Component v2
// Backend: /api/submit → MailChannels → cargorapido.ge@gmail.com

(function() {
  'use strict';

  const TG_URL = 'https://t.me/CARGORAPIDO';
  const WA_URL = 'https://wa.me/995568644615';

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

  function directLinks() {
    return `
      <div class="cr-direct-links">
        <a href="${TG_URL}" target="_blank" class="cr-direct-btn cr-tg">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M12 0C5.373 0 0 5.373 0 12s5.373 12 12 12 12-5.373 12-12S18.627 0 12 0zm5.562 8.248l-2.04 9.613c-.15.678-.546.843-1.107.524l-3.07-2.262-1.482 1.426c-.164.164-.302.302-.618.302l.22-3.12 5.678-5.127c.247-.22-.054-.342-.383-.122L7.12 14.35 4.1 13.41c-.666-.208-.68-.666.14-.987l10.88-4.194c.554-.2 1.04.136.443.02z"/></svg>
          Написать в Telegram
        </a>
        <a href="${WA_URL}" target="_blank" class="cr-direct-btn cr-wa">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z"/></svg>
          WhatsApp
        </a>
      </div>`;
  }

  function createFormHTML(formId) {
    return `
      <form class="cr-form" id="${formId}" novalidate>
        <!-- Honeypot -->
        <input type="text" name="website" style="display:none;position:absolute;left:-9999px" tabindex="-1" autocomplete="off" aria-hidden="true">

        <div class="cr-form-grid">
          <div class="cr-field">
            <label for="${formId}-name">Ваше имя <span class="req">*</span></label>
            <input type="text" id="${formId}-name" name="name" placeholder="Александр" autocomplete="name">
            <span class="cr-err" id="${formId}-name-err"></span>
          </div>

          <div class="cr-field">
            <label for="${formId}-phone">Телефон <span class="req">*</span></label>
            <input type="tel" id="${formId}-phone" name="phone" placeholder="+995 XX XXX XX XX" autocomplete="tel">
            <span class="cr-err" id="${formId}-phone-err"></span>
          </div>

          <div class="cr-field">
            <label for="${formId}-from">Откуда</label>
            <input type="text" id="${formId}-from" name="from_city" placeholder="Тбилиси, Батуми, Кутаиси...">
          </div>

          <div class="cr-field">
            <label for="${formId}-to">Куда</label>
            <input type="text" id="${formId}-to" name="to_city" placeholder="Москва, СПб, Алматы...">
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
            <label for="${formId}-contact">Удобный способ связи</label>
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
              <input type="checkbox" name="consent" id="${formId}-consent">
              <span>Я согласен(а) с <a href="/politika-konfidencialnosti/" target="_blank">Политикой конфиденциальности</a></span>
            </label>
            <span class="cr-err" id="${formId}-consent-err"></span>
          </div>
        </div>

        <div class="cr-form-actions" style="display:flex;gap:10px;flex-wrap:wrap;align-items:center;margin-top:20px">
          <button type="button" class="cr-submit-btn" id="${formId}-btn" onclick="CRForm.submit(event, '${formId}')">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor" style="flex-shrink:0"><path d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z"/></svg>
            Отправить заявку
          </button>
          <a href="${TG_URL}" target="_blank" class="cr-direct-btn cr-tg" id="${formId}-tg-btn"
             onclick="CRForm.openWith('tg','${formId}',event)">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M12 0C5.373 0 0 5.373 0 12s5.373 12 12 12 12-5.373 12-12S18.627 0 12 0zm5.562 8.248l-2.04 9.613c-.15.678-.546.843-1.107.524l-3.07-2.262-1.482 1.426c-.164.164-.302.302-.618.302l.22-3.12 5.678-5.127c.247-.22-.054-.342-.383-.122L7.12 14.35 4.1 13.41c-.666-.208-.68-.666.14-.987l10.88-4.194c.554-.2 1.04.136.443.02z"/></svg>
            Telegram
          </a>
          <a href="${WA_URL}" target="_blank" class="cr-direct-btn cr-wa" id="${formId}-wa-btn"
             onclick="CRForm.openWith('wa','${formId}',event)">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z"/></svg>
            WhatsApp
          </a>
        </div>

        <!-- Success state -->
        <div class="cr-success" id="${formId}-success" style="display:none">
          <div class="cr-success-icon">✅</div>
          <h3>Заявка отправлена!</h3>
          <p>Менеджер свяжется с вами в течение <strong>15 минут</strong>.</p>
          <p style="margin-top:6px;color:#888;font-size:13px">Пн–Сб 10:00–17:00. Вне рабочего времени — ответим утром.</p>
          ${directLinks()}
        </div>

        <!-- Error state -->
        <div class="cr-error-block" id="${formId}-error" style="display:none">
          <div class="cr-error-icon">⚠️</div>
          <p><strong>Не удалось отправить через форму.</strong><br>Напишите нам напрямую — ответим быстро:</p>
          ${directLinks()}
        </div>
      </form>`;
  }

  function initPhoneMask(input) {
    input.addEventListener('input', function(e) {
      let val = e.target.value.replace(/\D/g, '');
      if (val.length === 0) return;
      if (val.startsWith('995')) {
        val = '+' + val.slice(0, 12);
      } else if (val.startsWith('7') || val.startsWith('8')) {
        val = '+' + val.slice(0, 11);
      } else {
        val = '+' + val.slice(0, 15);
      }
      e.target.value = val;
    });
  }

  function showFieldError(fieldId, message) {
    const errEl = document.getElementById(fieldId);
    if (errEl) errEl.textContent = message;
    const input = document.getElementById(fieldId.replace('-err', ''));
    if (input) input.style.borderColor = '#e53935';
  }

  function clearFieldError(fieldId) {
    const errEl = document.getElementById(fieldId);
    if (errEl) errEl.textContent = '';
    const input = document.getElementById(fieldId.replace('-err', ''));
    if (input) input.style.borderColor = '';
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
        </div>`;
      const phoneInput = container.querySelector('input[name="phone"]');
      if (phoneInput) initPhoneMask(phoneInput);
    },

    openWith: function(channel, formId, e) {
      const form = document.getElementById(formId);
      if (!form) return;
      const val = (name) => form.querySelector('[name="'+name+'"]')?.value?.trim() || '';
      const name     = val('name');
      const phone    = val('phone');
      const from_c   = val('from_city');
      const to_c     = val('to_city');
      const cargo    = val('cargo_type');
      const weight   = val('weight');
      const contact  = val('contact_pref');
      const comment  = val('comment');

      const parts = ['Здравствуйте! Хочу узнать стоимость доставки.'];
      if (name)    parts.push('Меня зовут: ' + name);
      if (phone)   parts.push('Телефон: ' + phone);
      if (from_c)  parts.push('Откуда: ' + from_c);
      if (to_c)    parts.push('Куда: ' + to_c);
      if (cargo)   parts.push('Тип груза: ' + cargo);
      if (weight)  parts.push('Вес: ' + weight + ' кг');
      if (contact) parts.push('Удобная связь: ' + contact);
      if (comment) parts.push('Комментарий: ' + comment);

      const text = parts.join('\n');
      if (channel === 'tg') {
        e.currentTarget.href = 'https://t.me/CARGORAPIDO?text=' + encodeURIComponent(text);
      } else {
        e.currentTarget.href = 'https://wa.me/995568644615?text=' + encodeURIComponent(text);
      }
    },

    submit: async function(e, formId) {
      e.preventDefault();
      const form = document.getElementById(formId);
      if (!form) return;

      // Clear previous errors
      ['name', 'phone', 'consent'].forEach(f => clearFieldError(`${formId}-${f}-err`));

      // Honeypot
      const honeypot = form.querySelector('input[name="website"]');
      if (honeypot && honeypot.value.trim() !== '') return;

      const btn = document.getElementById(`${formId}-btn`);

      // Collect data
      const data = {
        name: form.querySelector('[name="name"]')?.value?.trim() || '',
        phone: form.querySelector('[name="phone"]')?.value?.trim() || '',
        from_city: form.querySelector('[name="from_city"]')?.value || '',
        to_city: form.querySelector('[name="to_city"]')?.value || '',
        cargo_type: form.querySelector('[name="cargo_type"]')?.value || '',
        weight: form.querySelector('[name="weight"]')?.value || '',
        contact_pref: form.querySelector('[name="contact_pref"]')?.value || '',
        comment: form.querySelector('[name="comment"]')?.value?.trim() || '',
        consent: form.querySelector('[name="consent"]')?.checked ? 'true' : 'false',
        website: honeypot?.value || '',
      };

      // Client-side validation
      let hasErrors = false;
      if (!data.name || data.name.length < 2) {
        showFieldError(`${formId}-name-err`, 'Введите ваше имя (минимум 2 символа)');
        hasErrors = true;
      }
      const phoneDigits = data.phone.replace(/\D/g, '');
      if (!phoneDigits || phoneDigits.length < 9) {
        showFieldError(`${formId}-phone-err`, 'Введите корректный номер телефона');
        hasErrors = true;
      }
      if (data.consent !== 'true') {
        showFieldError(`${formId}-consent-err`, 'Необходимо согласие с политикой');
        hasErrors = true;
      }
      if (hasErrors) return;

      // Loading state
      if (btn) {
        btn.disabled = true;
        btn.innerHTML = '<svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor" class="cr-spin"><path d="M12 4V1L8 5l4 4V6c3.31 0 6 2.69 6 6 0 1.01-.25 1.97-.7 2.8l1.46 1.46A7.93 7.93 0 0020 12c0-4.42-3.58-8-8-8zm0 14c-3.31 0-6-2.69-6-6 0-1.01.25-1.97.7-2.8L5.24 7.74A7.93 7.93 0 004 12c0 4.42 3.58 8 8 8v3l4-4-4-4v3z"/></svg> Отправляем...';
      }

      try {
        const resp = await fetch('/api/submit', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(data),
        });

        const result = await resp.json();

        if (resp.ok && result.ok) {
          // Success
          form.querySelector('.cr-form-grid').style.display = 'none';
          form.querySelector('.cr-form-actions').style.display = 'none';
          form.querySelector('.cr-direct-links').style.display = 'none';
          document.getElementById(`${formId}-success`).style.display = 'block';
        } else if (resp.status === 429) {
          // Rate limit
          if (btn) { btn.disabled = false; btn.innerHTML = '<svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z"/></svg> Отправить заявку'; }
          showFieldError(`${formId}-name-err`, 'Слишком много попыток. Подождите минуту.');
        } else {
          throw new Error('Server error: ' + resp.status);
        }
      } catch (err) {
        console.error('Form submit error:', err);
        // Show fallback error with direct contact buttons
        form.querySelector('.cr-form-grid').style.display = 'none';
        form.querySelector('.cr-form-actions').style.display = 'none';
        form.querySelector('.cr-direct-links').style.display = 'none';
        document.getElementById(`${formId}-error`).style.display = 'block';
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
