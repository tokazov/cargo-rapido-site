// Cargo Rapido — Form Submission Handler
// Cloudflare Pages Function
// POST /api/submit → Telegram group CargoRapidoAi

const BOT_TOKEN = '8627618553:AAEhNoPtiU6D1ADq-y1BrzYxOyxgxnZpoWY';
const CHAT_ID   = '-1003747824934';

const ALLOWED_ORIGINS = [
  'https://cargorapido.com',
  'https://www.cargorapido.com',
  'https://cargo-rapido.pages.dev',
  'https://preview.cargo-rapido.pages.dev',
  'https://77bca61b.cargo-rapido.pages.dev',
];

// In-memory rate limit: 3 req / IP / min
const rateLimitMap = new Map();
function checkRateLimit(ip) {
  const now = Date.now();
  const window = 60_000;
  const max = 3;
  const hits = (rateLimitMap.get(ip) || []).filter(t => now - t < window);
  hits.push(now);
  rateLimitMap.set(ip, hits);
  return hits.length <= max;
}

function validateFields(data) {
  const errors = [];
  if (!data.name || data.name.trim().length < 2 || data.name.trim().length > 50)
    errors.push('Имя: от 2 до 50 символов');
  const digits = (data.phone || '').replace(/\D/g, '');
  if (!digits || digits.length < 9)
    errors.push('Укажите корректный номер телефона');
  if (data.consent !== 'true')
    errors.push('Необходимо согласие с политикой');
  return errors;
}

function buildTgMessage(data, meta) {
  const line = (icon, label, val) => val ? `${icon} <b>${label}:</b> ${escTg(val)}\n` : '';
  return `🚛 <b>Новая заявка с сайта cargorapido.com</b>\n\n` +
    line('👤', 'Имя',       data.name?.trim()) +
    line('📞', 'Телефон',   data.phone) +
    line('💬', 'Контакт',   data.contact_pref) +
    line('📍', 'Откуда',    data.from_city) +
    line('📍', 'Куда',      data.to_city) +
    line('📦', 'Тип груза', data.cargo_type) +
    line('⚖️', 'Вес',       data.weight ? data.weight + ' кг' : '') +
    line('💭', 'Комментарий', data.comment) +
    `\n🌐 IP: ${meta.ip}\n🕐 ${meta.time}\n🔗 ${meta.referer}`;
}

function escTg(str) {
  return String(str || '').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
}

const corsHeaders = (origin) => ({
  'Access-Control-Allow-Origin': origin,
  'Content-Type': 'application/json',
});

export async function onRequestPost(context) {
  const { request } = context;

  const origin = request.headers.get('Origin') || '';
  if (!ALLOWED_ORIGINS.includes(origin)) {
    return new Response(JSON.stringify({ ok: false, error: 'Forbidden' }), {
      status: 403, headers: { 'Content-Type': 'application/json' }
    });
  }

  const headers = corsHeaders(origin);

  // Rate limit
  const ip = request.headers.get('CF-Connecting-IP') || '0.0.0.0';
  if (!checkRateLimit(ip)) {
    return new Response(JSON.stringify({ ok: false, error: 'rate_limit' }), {
      status: 429, headers
    });
  }

  // Parse
  let data;
  try { data = await request.json(); }
  catch {
    return new Response(JSON.stringify({ ok: false, error: 'invalid_json' }), {
      status: 400, headers
    });
  }

  // Honeypot
  if (data.website && data.website.trim() !== '') {
    return new Response(JSON.stringify({ ok: true }), { status: 200, headers });
  }

  // Validate
  const errors = validateFields(data);
  if (errors.length > 0) {
    return new Response(JSON.stringify({ ok: false, error: 'validation', details: errors }), {
      status: 422, headers
    });
  }

  // Build message
  const referer = request.headers.get('Referer') || 'прямой переход';
  const timeStr = new Date().toLocaleString('ru-RU', { timeZone: 'Asia/Tbilisi' }) + ' (Тбилиси)';
  const text = buildTgMessage(data, { ip, time: timeStr, referer });

  // Send to Telegram
  try {
    const tgResp = await fetch(
      `https://api.telegram.org/bot${BOT_TOKEN}/sendMessage`,
      {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          chat_id: CHAT_ID,
          text,
          parse_mode: 'HTML',
          disable_web_page_preview: true,
        }),
      }
    );

    const tgData = await tgResp.json();

    if (tgData.ok) {
      return new Response(JSON.stringify({ ok: true }), { status: 200, headers });
    } else {
      console.error('Telegram error:', JSON.stringify(tgData));
      return new Response(JSON.stringify({ ok: false, error: 'tg_failed', detail: tgData.description }), {
        status: 502, headers
      });
    }
  } catch (err) {
    console.error('Fetch error:', err);
    return new Response(JSON.stringify({ ok: false, error: 'network_error' }), {
      status: 502, headers
    });
  }
}

export async function onRequestOptions(context) {
  const origin = context.request.headers.get('Origin') || '';
  return new Response(null, {
    status: 204,
    headers: {
      'Access-Control-Allow-Origin': ALLOWED_ORIGINS.includes(origin) ? origin : '',
      'Access-Control-Allow-Methods': 'POST, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type',
      'Access-Control-Max-Age': '86400',
    },
  });
}
