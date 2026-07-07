#!/usr/bin/env python3
"""
Автоматический блог для cargorapido.com
- Генерирует идеи статей на основе новостей + ключевых запросов
- Создаёт полный HTML в формате сайта
- Обновляет sitemap.xml и индекс блога
- Делает git push → Cloudflare Pages деплоит автоматически
"""

import os
import re
import json
import subprocess
import urllib.request
import urllib.parse
from datetime import datetime, date
from pathlib import Path

# ─── CONFIG ───────────────────────────────────────────────────────────────────
BASE = Path('/root/.openclaw/workspace/cargo-rapido-site')
ANTHROPIC_KEY = os.environ.get('ANTHROPIC_API_KEY', '')
GEMINI_KEY = 'AIzaSyBSwXW8HO2J8McwQ9JOsGyPq88tsgoaRig'
GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN', '')
SITE_URL = 'https://cargorapido.com'
TODAY = str(date.today())

# Тематика: только то что касается Cargo Rapido
# ─── ТЕМАТИЧЕСКИЕ ФОТО ───────────────────────────────────────────────────────
# Маппинг тем → список фотографий (рандомно выбирается одна для карточки и несколько для статьи)
PHOTO_THEMES = {
    'таможня': ['customs.jpg', 'broker-docs.jpg', 'documents.jpg', 'broker-calc.jpg', 'broker-handshake.jpg'],
    'broker': ['broker-docs.jpg', 'broker-calc.jpg', 'broker-handshake.jpg', 'broker-meeting.jpg', 'broker-tablet.jpg'],
    'авиа': ['svc-airfreight.jpg', 'blog-avia.jpg', 'photo2-airfreight.jpg'],
    'европа': ['blog-europe.jpg', 'europe-delivery.jpg', 'photo2-highway.jpg', 'photo2-truck-modern.jpg'],
    'россия': ['blog-russia.jpg', 'photo-trucks-winter.jpg', 'photo2-truck-red.jpg', 'hero-truck.jpg'],
    'санкции': ['blog-sanctions.jpg', 'documents.jpg', 'broker-docs.jpg'],
    'личные': ['blog-personal.jpg', 'personal-items.jpg', 'photo2-mover.jpg', 'svc-movers-carry.jpg', 'svc-movers-blue.jpg'],
    'мебель': ['svc-movers-carry.jpg', 'svc-movers-blue.jpg', 'svc-movers-van.jpg', 'photo2-mover.jpg'],
    'переезд': ['svc-movers-carry.jpg', 'svc-movers-blue.jpg', 'photo2-mover.jpg', 'svc-movers-van.jpg'],
    'сборные': ['blog-sborny.jpg', 'commercial-cargo.jpg', 'photo-containers.jpg', 'photo-loading.jpg'],
    'автомобил': ['car-transport.jpg', 'photo-autovoz.jpg', 'photo-evacuator.jpg'],
    'склад': ['warehouse.jpg', 'photo-warehouse-big.jpg', 'photo-warehouse2.jpg', 'photo-loading.jpg'],
    'термо': ['reefer.jpg', 'reefer-truck.jpg', 'reefer-fleet.jpg'],
    'посылк': ['photo-parcel.jpg', 'photo-parcel-hand.jpg', 'svc-courier-box.jpg', 'photo2-courier.jpg'],
    'документ': ['documents.jpg', 'photo2-documents.jpg', 'broker-docs.jpg'],
    'упаковк': ['svc-packing.jpg', 'photo2-unloading.jpg', 'photo-loading.jpg'],
    'ларс': ['hero-truck.jpg', 'photo-trucks-winter.jpg', 'photo2-highway.jpg', 'photo-truck-city.jpg'],
    'турция': ['blog-turkey.jpg', 'photo2-highway.jpg'],
    'доставка': ['photo-delivery-door.jpg', 'photo-delivery-sign.jpg', 'photo2-delivery.jpg', 'svc-delivery-sign.jpg'],
}
PHOTOS_ALL = [
    'truck.jpg', 'hero-truck.jpg', 'hero-main.jpg', 'commercial-cargo.jpg',
    'photo-truck-city.jpg', 'photo2-truck-modern.jpg', 'photo2-highway.jpg',
    'photo-worker.jpg', 'photo-handshake.jpg', 'about-team.jpg',
]

import random as _random

def pick_cover_photo(title: str, keywords: str) -> str:
    """Выбирает тематическую обложку для статьи."""
    text = (title + ' ' + keywords).lower()
    for theme, photos in PHOTO_THEMES.items():
        if theme in text:
            return _random.choice(photos)
    return _random.choice(PHOTOS_ALL)

def pick_inline_photos(title: str, keywords: str, count: int = 2) -> list:
    """Выбирает несколько тематических фото для вставки в текст."""
    text = (title + ' ' + keywords).lower()
    candidates = []
    for theme, photos in PHOTO_THEMES.items():
        if theme in text:
            candidates.extend(photos)
    # Уникальные + рандом
    candidates = list(dict.fromkeys(candidates))
    if len(candidates) < count:
        candidates.extend(PHOTOS_ALL)
    _random.shuffle(candidates)
    return candidates[:count]

TOPIC_CONTEXT = """
Cargo Rapido — транспортно-логистическая компания в Тбилиси (Грузия).
Специализация: грузоперевозки Грузия ↔ Россия ↔ СНГ ↔ Европа.
Услуги: сборные грузы, личные вещи, автовоз, авиадоставка, таможня, брокер, склад, термо-режим.
Маршруты: через Верхний Ларс, авиа, морской путь.

Темы статей должны быть ТОЛЬКО о:
- Грузоперевозках (практика, советы, маршруты)
- Таможенном оформлении (Грузия, Россия, СНГ, Европа)
- Брокерских услугах
- Перевозке автомобилей
- Упаковке и подготовке грузов
- Изменениях в законодательстве по перевозкам
- Актуальных новостях о КПП Верхний Ларс
- Переездах (личные вещи, контейнеры)
- Авиадоставке из/в Грузию

НЕ писать о политике, общих новостях, темах не связанных с грузоперевозками.
"""

# ─── AI API ───────────────────────────────────────────────────────────────────
def call_ai(prompt: str) -> str:
    """Вызов Claude Haiku — быстро и дёшево для генерации контента"""
    key = ANTHROPIC_KEY
    if not key:
        raise ValueError('ANTHROPIC_API_KEY not set')
    payload = json.dumps({
        'model': 'claude-haiku-4-5',
        'max_tokens': 4096,
        'messages': [{'role': 'user', 'content': prompt}]
    }).encode()
    req = urllib.request.Request(
        'https://api.anthropic.com/v1/messages',
        data=payload,
        headers={
            'x-api-key': key,
            'anthropic-version': '2023-06-01',
            'content-type': 'application/json'
        },
        method='POST'
    )
    with urllib.request.urlopen(req, timeout=60) as r:
        data = json.loads(r.read())
    return data['content'][0]['text']

# ─── SLUG ─────────────────────────────────────────────────────────────────────
def make_slug(title: str) -> str:
    ru = {'а':'a','б':'b','в':'v','г':'g','д':'d','е':'e','ё':'yo','ж':'zh','з':'z',
          'и':'i','й':'j','к':'k','л':'l','м':'m','н':'n','о':'o','п':'p','р':'r',
          'с':'s','т':'t','у':'u','ф':'f','х':'kh','ц':'ts','ч':'ch','ш':'sh',
          'щ':'sch','ъ':'','ы':'y','ь':'','э':'e','ю':'yu','я':'ya'}
    slug = title.lower()
    result = ''
    for ch in slug:
        result += ru.get(ch, ch)
    slug = re.sub(r'[^a-z0-9]+', '-', result).strip('-')
    return slug[:60]

# ─── HTML TEMPLATE ─────────────────────────────────────────────────────────────
def build_post_html(title: str, description: str, slug: str, content_html: str,
                    keywords: str, image: str = 'truck.jpg') -> str:
    post_url = f'{SITE_URL}/poleznaya-informaciya/post/{slug}/'
    schema_article = json.dumps({
        "@context": "https://schema.org",
        "@type": "BlogPosting",
        "headline": title,
        "description": description,
        "url": post_url,
        "datePublished": TODAY,
        "dateModified": TODAY,
        "author": {"@type": "Organization", "name": "Cargo Rapido"},
        "publisher": {"@type": "Organization", "name": "Cargo Rapido",
                      "logo": {"@type": "ImageObject", "url": f"{SITE_URL}/logo.jpg"}},
        "image": f"{SITE_URL}/{image}",
        "keywords": keywords
    })
    schema_breadcrumb = json.dumps({
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Главная", "item": f"{SITE_URL}/"},
            {"@type": "ListItem", "position": 2, "name": "Блог", "item": f"{SITE_URL}/poleznaya-informaciya/"},
            {"@type": "ListItem", "position": 3, "name": title[:40], "item": post_url}
        ]
    })

    return f'''<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} | Cargo Rapido</title>
  <meta name="description" content="{description}">
  <link rel="canonical" href="{post_url}">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{description}">
  <meta property="og:url" content="{post_url}">
  <meta property="og:type" content="article">
  <meta property="og:image" content="{SITE_URL}/{image}">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{title}">
  <meta name="twitter:description" content="{description}">
  <meta name="twitter:image" content="{SITE_URL}/{image}">
  <meta name="keywords" content="{keywords}">
  <meta name="google-site-verification" content="U4VPSdMvjvNSx8QubmIyhUwQPcS6y2hnZsIyLe6PMqM">
  <meta name="yandex-verification" content="8d6727b9489f571e">
  <link rel="icon" type="image/x-icon" href="/favicon.ico">
  <link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">
  <link rel="manifest" href="/manifest.json">
  <meta name="theme-color" content="#1a237e">
  <script type="application/ld+json">{schema_article}</script>
  <script type="application/ld+json">{schema_breadcrumb}</script>
  <!-- Яндекс.Метрика -->
  <script type="text/javascript">
   (function(m,e,t,r,i,k,a){{m[i]=m[i]||function(){{(m[i].a=m[i].a||[]).push(arguments)}};
   m[i].l=1*new Date();
   for(var j=0;j<document.scripts.length;j++){{if(document.scripts[j].src===r){{return;}}}}
   k=e.createElement(t),a=e.getElementsByTagName(t)[0],k.async=1,k.src=r,a.parentNode.insertBefore(k,a)}}
   )(window, document, "script", "https://mc.yandex.ru/metrika/tag.js", "ym");
   ym(90606836, "init", {{clickmap:true,trackLinks:true,accurateTrackBounce:true,webvisor:true}});
  </script>
  <noscript><div><img src="https://mc.yandex.ru/watch/90606836" style="position:absolute; left:-9999px;" alt="" /></div></noscript>
  <!-- Google Tag Manager -->
  <script>(function(w,d,s,l,i){{w[l]=w[l]||[];w[l].push({{'gtm.start':
  new Date().getTime(),event:'gtm.js'}});var f=d.getElementsByTagName(s)[0],
  j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
  'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
  }})(window,document,'script','dataLayer','GTM-MLNDMC75');</script>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
  <link rel="stylesheet" href="/style.css">
  <style>
    @media (max-width: 768px) {{
      .post-layout {{ grid-template-columns: 1fr !important; }}
      .sidebar {{ order: 2; }}
      .post-content {{ order: 1; }}
    }}
  </style>
</head>
<body>
<noscript><iframe src="https://www.googletagmanager.com/ns.html?id=GTM-MLNDMC75" height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
<header>
  <a href="/" class="logo"><img src="/logo.jpg" alt="Cargo Rapido" style="height:48px;width:auto;display:block;"></a>
  <button class="burger" onclick="toggleMenu()">☰</button>
  <nav class="header-nav" id="main-nav">
    <a href="/about/">О компании</a>
    <div class="dropdown">
      <a href="/nashi-uslugi/">Услуги ▾</a>
      <div class="dropdown-menu">
        <a href="/perevozka-kommercheskih-gruzov/">Коммерческие грузы</a>
        <a href="/perevozka-lichnyh-veshchej/">Личные вещи</a>
        <a href="/dostavka-v-evropu/">Доставка в Европу</a>
        <a href="/dostavka-posylok-pisem-i-dokumentov-po-vsemu-miru/">Посылки и документы</a>
        <a href="/perevozka-gruzov-pod-termorezhimom/">Термо-режим</a>
        <a href="/skladskie-uslugi/">Складские услуги</a>
        <a href="/brokerskie-uslugi/">Брокерские услуги</a>
        <a href="/perevozka-avtomobilya-na-avtovoze/">Перевозка автомобиля на автовозе</a>
        <a href="/perevozka-avtomobilya-na-evakuatore/">Перевозка автомобиля на эвакуаторе</a>
      </div>
    </div>
    <a href="/poleznaya-informaciya/">Блог</a>
    <a href="/kontakty/">Контакты</a>
    <a href="https://wa.me/995568644615" class="nav-phone"><i class="fab fa-whatsapp" style="color:#25D366"></i> +995 568 644 615</a>
    <a href="https://t.me/CARGORAPIDO" target="_blank" class="nav-phone nav-cta">Заявка</a>
  </nav>
</header>

<div class="breadcrumb-nav" style="padding:12px 24px;font-size:13px;color:#666;max-width:1200px;margin:0 auto;">
  <a href="/" style="color:#1a237e;text-decoration:none;">Главная</a> →
  <a href="/poleznaya-informaciya/" style="color:#1a237e;text-decoration:none;">Блог</a> →
  <span>{title[:50]}</span>
</div>

<div class="post-layout" style="max-width:1200px;margin:0 auto;padding:0 24px 48px;display:grid;grid-template-columns:1fr 320px;gap:40px;">
<article class="post-content">
  <div style="margin-bottom:24px;">
    <span style="background:#e8eaf6;color:#1a237e;padding:4px 12px;border-radius:20px;font-size:13px;font-weight:600;">Грузоперевозки</span>
    <span style="color:#999;font-size:13px;margin-left:12px;">{TODAY}</span>
  </div>

{content_html}

  <div style="margin-top:32px;padding:20px;background:#f8f9ff;border-radius:12px;display:flex;gap:12px;flex-wrap:wrap;align-items:center;">
    <span style="font-size:14px;color:#666;">Поделиться:</span>
    <button onclick="shareToWa()" style="background:#25D366;color:white;border:none;padding:8px 16px;border-radius:8px;cursor:pointer;font-size:13px;">💬 WhatsApp</button>
    <button onclick="copyLink(this)" style="background:#1a237e;color:white;border:none;padding:8px 16px;border-radius:8px;cursor:pointer;font-size:13px;">🔗 Скопировать</button>
  </div>
</article>

<aside class="sidebar">
  <div class="sidebar-cta">
    <h4>Нужна доставка?</h4>
    <p>Рассчитаем стоимость за 5 минут. Работаем Пн-Сб 10:00-17:00.</p>
    <a href="https://t.me/CARGORAPIDO" target="_blank">✈️ Telegram</a>
    <a href="https://wa.me/995568644615" target="_blank" style="background:#25D366">💬 WhatsApp</a>
  </div>
  <div class="sidebar-card">
    <h4>Услуги компании</h4>
    <ul>
      <li><a href="/perevozka-kommercheskih-gruzov/">Коммерческие грузы</a></li>
      <li><a href="/perevozka-lichnyh-veshchej/">Личные вещи</a></li>
      <li><a href="/dostavka-v-evropu/">Доставка в Европу</a></li>
      <li><a href="/dostavka-posylok-pisem-i-dokumentov-po-vsemu-miru/">Посылки и документы</a></li>
      <li><a href="/brokerskie-uslugi/">Брокерские услуги</a></li>
      <li><a href="/skladskie-uslugi/">Складские услуги</a></li>
    </ul>
  </div>
</aside>
</div>

<section class="cta-banner">
  <h2>Нужна перевозка из Грузии?</h2>
  <p>Напишите нам — рассчитаем стоимость за 5 минут и подберём оптимальный маршрут.</p>
  <div style="display:flex;gap:12px;justify-content:center;flex-wrap:wrap;">
    <a href="https://t.me/CARGORAPIDO" target="_blank" class="btn-dark"><i class="fab fa-telegram"></i> Написать в Telegram</a>
    <a href="https://wa.me/995568644615" target="_blank" class="btn-green"><i class="fab fa-whatsapp"></i> WhatsApp</a>
  </div>
</section>

<footer>
  <div class="footer-grid">
    <div class="footer-brand">
      <a href="/" class="logo"><img src="/logo.jpg" alt="Cargo Rapido" style="height:48px;width:auto;display:block;"></a>
      <p style="margin-top:16px;">Транспортно-логистическая компания. Грузоперевозки из Грузии в Россию, СНГ и Европу.</p>
      <p style="margin-top:12px;">Грузия, г. Тбилиси,<br>ул. Серго Закариадзе 5</p>
      <p style="margin-top:8px;">Пн-Сб 10:00–17:00</p>
    </div>
    <div class="footer-col">
      <h4>Услуги</h4>
      <ul>
        <li><a href="/perevozka-kommercheskih-gruzov/">Коммерческие грузы</a></li>
        <li><a href="/perevozka-lichnyh-veshchej/">Личные вещи</a></li>
        <li><a href="/dostavka-v-evropu/">Доставка в Европу</a></li>
        <li><a href="/perevozka-gruzov-pod-termorezhimom/">Термо-режим</a></li>
        <li><a href="/skladskie-uslugi/">Склад</a></li>
        <li><a href="/brokerskie-uslugi/">Брокерские услуги</a></li>
        <li><a href="/perevozka-avtomobilya-na-avtovoze/">Перевозка автомобилей</a></li>
      </ul>
    </div>
    <div class="footer-col">
      <h4>Компания</h4>
      <ul>
        <li><a href="/about/">О компании</a></li>
        <li><a href="/poleznaya-informaciya/">Блог</a></li>
        <li><a href="/kontakty/">Контакты</a></li>
      </ul>
    </div>
    <div class="footer-col">
      <h4>Контакты</h4>
      <ul>
        <li><a href="https://wa.me/995568644615">+995 568 644 615</a></li>
        <li><a href="https://t.me/CARGORAPIDO" target="_blank">Telegram</a></li>
        <li><a href="mailto:cargorapido.ge@gmail.com">Email</a></li>
        <li><a href="https://facebook.com/CargoRapido" target="_blank">Facebook</a></li>
      </ul>
    </div>
  </div>
  <div class="footer-bottom">
    <p>© 2026 Cargo Rapido. Все права защищены.
      <a href="/politika-konfidencialnosti/" style="color:rgba(255,255,255,0.5);text-decoration:none;">Политика конфиденциальности</a> ·
      <a href="/usloviya-okazaniya-uslug/" style="color:rgba(255,255,255,0.5);text-decoration:none;">Условия услуг</a>
    </p>
    <p><a href="/sitemap.xml" style="color:rgba(255,255,255,0.4);text-decoration:none;">Карта сайта</a></p>
  </div>
</footer>
<script src="/shared.js"></script>
<script>
function shareToWa() {{
  window.open('https://wa.me/?text=' + encodeURIComponent(document.title + ' ' + location.href), '_blank');
}}
function copyLink(btn) {{
  navigator.clipboard.writeText(location.href).then(() => {{
    btn.textContent = '✅ Скопировано!';
    setTimeout(() => btn.textContent = '🔗 Скопировать', 2000);
  }});
}}
</script>
</body>
</html>'''

# ─── GENERATE ARTICLE IDEAS ───────────────────────────────────────────────────
def generate_ideas(n: int = 5) -> list:
    prompt = f"""{TOPIC_CONTEXT}

Дата сегодня: {TODAY}

Сгенерируй {n} идей для статей блога cargorapido.com.
Для каждой идеи дай:
- title: заголовок статьи (на русском, SEO-оптимизированный, без года)
- description: meta description 150-160 символов
- keywords: 5-7 ключевых слов через запятую
- why: почему эта тема актуальна сейчас (1 предложение)

Верни JSON массив объектов. Только JSON, без пояснений.
"""
    response = call_ai(prompt)
    # Извлекаем JSON
    start = response.find('[')
    end = response.rfind(']') + 1
    return json.loads(response[start:end])

# ─── GENERATE ARTICLE CONTENT ─────────────────────────────────────────────────
def generate_content(title: str, description: str, keywords: str, inline_photos: list = None) -> str:
    # Формируем блок с инструкцией по фото
    photo_instructions = ''
    if inline_photos:
        photo_list = '\n'.join([f'  - /{p}' for p in inline_photos])
        photo_instructions = f"""
10. ФОТО В ТЕКСТЕ: вставь {len(inline_photos)} изображения в статью — по одному после 1-го и 3-го H2.
    Используй ровно эти файлы (в указанном порядке):
{photo_list}
    Формат вставки:
    <figure style="margin:24px 0;border-radius:12px;overflow:hidden;">
      <img src="/FILENAME.jpg" alt="ОПИСАНИЕ" style="width:100%;height:260px;object-fit:cover;display:block;">
      <figcaption style="padding:8px 12px;font-size:13px;color:#666;background:#f8f9ff;">ПОДПИСЬ</figcaption>
    </figure>
"""

    prompt = f"""{TOPIC_CONTEXT}

Напиши статью для блога cargorapido.com.

Тема: {title}
Meta description: {description}
Ключевые слова: {keywords}

ТРЕБОВАНИЯ:
1. Структура: H1 (уже есть, не добавляй) → лид-абзац → 4-6 H2 с развёрнутыми абзацами → FAQ (H2 + H3 вопросы)
2. Каждый H2 — минимум 2 абзаца по 3-5 предложений. Не буллеты.
3. Конкретные цены и таможенные пороги НЕ указывать — только "уточняйте у менеджера"
4. Внутренние ссылки: используй теги <a href="/brokerskie-uslugi/">, <a href="/perevozka-avtomobilya-na-avtovoze/"> и т.д.
5. SEO: ключевые слова естественно в тексте, не спам
6. FAQ в конце: 3-4 вопроса которые реально задают клиенты
7. Schema FAQPage разметка для FAQ — добавь отдельным <script type="application/ld+json"> в конце
8. Язык: профессиональный, живой, не канцелярский
9. Объём: 700-1000 слов{photo_instructions}

Верни ТОЛЬКО HTML контент (от <h1> до последнего </script>). Без DOCTYPE, head, body.
"""
    return call_ai(prompt)

# ─── UPDATE SITEMAP ────────────────────────────────────────────────────────────
def update_sitemap(slug: str):
    sitemap_path = BASE / 'sitemap.xml'
    sitemap = sitemap_path.read_text()
    new_url = f'''  <url><loc>{SITE_URL}/poleznaya-informaciya/post/{slug}/</loc><lastmod>{TODAY}</lastmod><changefreq>monthly</changefreq><priority>0.7</priority></url>'''
    if slug in sitemap:
        print(f'  sitemap: {slug} already exists')
        return
    sitemap = sitemap.replace('</urlset>', f'{new_url}\n</urlset>')
    sitemap_path.write_text(sitemap)
    print(f'  sitemap updated: {slug}')

# ─── UPDATE BLOG INDEX ─────────────────────────────────────────────────────────
def update_blog_index(title: str, description: str, slug: str, image: str = 'truck.jpg'):
    index_path = BASE / 'poleznaya-informaciya' / 'index.html'
    index = index_path.read_text()

    # Формат карточки совпадает с существующими article.blog-card на сайте
    date_ru = datetime.now().strftime('%-d %B %Y').upper()
    card = f'''    <article class="blog-card">
      <a href="/poleznaya-informaciya/post/{slug}/" class="blog-card-link-wrap">
        <div class="blog-card-img" style="background-image:url('/{image}')"></div>
        <div class="blog-card-body">
          <div class="blog-card-date">{TODAY}</div>
          <h2 class="blog-card-title">{title}</h2>
          <p class="blog-card-desc">{description[:120]}</p>
          <span class="blog-card-link">Читать →</span>
        </div>
      </a>
    </article>\n'''

    # Вставляем первой карточкой внутри blog-grid
    index = index.replace('<div class="blog-grid">\n', '<div class="blog-grid">\n' + card)
    index_path.write_text(index)
    print(f'  blog index updated')

# ─── LINK VALIDATOR ───────────────────────────────────────────────────────────
# Все реально существующие страницы сайта
VALID_PATHS = {
    '/', '/about/', '/nashi-uslugi/', '/kontakty/', '/poleznaya-informaciya/',
    '/politika-konfidencialnosti/', '/usloviya-okazaniya-uslug/', '/sitemap.xml',
    '/perevozka-kommercheskih-gruzov/', '/perevozka-lichnyh-veshchej/',
    '/dostavka-v-evropu/', '/dostavka-posylok-pisem-i-dokumentov-po-vsemu-miru/',
    '/perevozka-gruzov-pod-termorezhimom/', '/perevozka-avtomobilya-na-avtovoze/',
    '/perevozka-avtomobilya-na-evakuatore/', '/skladskie-uslugi/',
    '/brokerskie-uslugi/', '/otzyvy/', '/soglasie-na-obrabotku/',
}

# Карта ближайших замен для несуществующих путей
FALLBACK_MAP = {
    '/tamozhennoe-oformlenie/': '/brokerskie-uslugi/',
    '/tamozhnya/': '/brokerskie-uslugi/',
    '/customs/': '/brokerskie-uslugi/',
    '/tarify/': '/perevozka-kommercheskih-gruzov/',
    '/prices/': '/perevozka-kommercheskih-gruzov/',
    '/avtozov/': '/perevozka-avtomobilya-na-avtovoze/',
    '/avtovoz/': '/perevozka-avtomobilya-na-avtovoze/',
    '/lichnye-veshchi/': '/perevozka-lichnyh-veshchej/',
    '/perevozka-lichnyx-veshhej/': '/perevozka-lichnyh-veshchej/',
    '/sborny-gruz/': '/perevozka-kommercheskih-gruzov/',
    '/sbornyj-gruz/': '/perevozka-kommercheskih-gruzov/',
    '/evropa/': '/dostavka-v-evropu/',
    '/blog/': '/poleznaya-informaciya/',
}

def validate_and_fix_links(html: str) -> tuple[str, list]:
    """Проверяет все внутренние href в HTML и заменяет 404 на валидные."""
    issues = []
    def replace_href(m):
        href = m.group(1)
        # Пропускаем внешние ссылки, якоря, mailto, tel
        if href.startswith(('http', 'mailto:', 'tel:', '#', '//')):
            return m.group(0)
        # Пропускаем статичные файлы
        if any(href.endswith(ext) for ext in ('.css', '.js', '.ico', '.png', '.jpg', '.xml', '.json')):
            return m.group(0)
        # Проверяем путь
        if href in VALID_PATHS:
            return m.group(0)
        # Ищем в карте замен
        if href in FALLBACK_MAP:
            fixed = FALLBACK_MAP[href]
            issues.append(f'  replaced: {href} → {fixed}')
            return f'href="{fixed}"'
        # Проверяем через HTTP (только для неизвестных путей)
        try:
            code = urllib.request.urlopen(
                urllib.request.Request(SITE_URL + href, method='HEAD'),
                timeout=5
            ).getcode()
            if code == 200:
                VALID_PATHS.add(href)
                return m.group(0)
        except Exception:
            pass
        # Не нашли — заменяем на главную блога
        fixed = '/poleznaya-informaciya/'
        issues.append(f'  broken (404): {href} → {fixed}')
        return f'href="{fixed}"'

    html = re.sub(r'href="([^"]*)"', replace_href, html)
    return html, issues

# ─── GIT PUSH ─────────────────────────────────────────────────────────────────
def git_push(message: str):
    env = os.environ.copy()
    env['GIT_ASKPASS'] = 'echo'
    env['GIT_USERNAME'] = 'tokazov'
    env['GIT_PASSWORD'] = GITHUB_TOKEN

    subprocess.run(['git', '-C', str(BASE), 'add', '-A'], check=True, env=env)
    result = subprocess.run(['git', '-C', str(BASE), 'diff', '--cached', '--quiet'], env=env)
    if result.returncode != 0:
        subprocess.run(['git', '-C', str(BASE), 'commit', '-m', message], check=True, env=env)
        remote = f'https://{GITHUB_TOKEN}@github.com/tokazov/cargo-rapido-site.git'
        subprocess.run(['git', '-C', str(BASE), 'push', remote, 'main'], check=True, env=env)
        print(f'  pushed: {message}')
    else:
        print('  nothing to push')

# ─── MAIN: CREATE ONE POST ─────────────────────────────────────────────────────
def create_post(title: str, description: str, keywords: str, image: str = None):
    slug = make_slug(title)
    post_dir = BASE / 'poleznaya-informaciya' / 'post' / slug
    if post_dir.exists():
        print(f'Post already exists: {slug}')
        return slug

    # Подбираем тематические фото
    cover = image or pick_cover_photo(title, keywords)
    inline_photos = pick_inline_photos(title, keywords, count=2)
    # Убираем обложку из inline чтоб не повторялась
    inline_photos = [p for p in inline_photos if p != cover][:2]
    print(f'\nGenerating article: {title}')
    print(f'  cover: {cover} | inline: {inline_photos}')
    content_html = generate_content(title, description, keywords, inline_photos=inline_photos)

    # Убираем markdown-артефакты (```html, ```)
    content_html = re.sub(r'```html\s*', '', content_html)
    content_html = re.sub(r'```\s*', '', content_html)

    # Убираем H1 если Claude добавил его (H1 уже в шаблоне)
    content_html = re.sub(r'<h1[^>]*>.*?</h1>', '', content_html, flags=re.DOTALL)

    # Добавляем H1 в начало контента
    content_html = f'<h1>{title}</h1>\n' + content_html

    html = build_post_html(title, description, slug, content_html, keywords, cover)

    # Валидация ссылок
    html, link_issues = validate_and_fix_links(html)
    if link_issues:
        print('  link fixes:')
        for issue in link_issues:
            print(issue)
    else:
        print('  links: all OK')

    post_dir.mkdir(parents=True, exist_ok=True)
    (post_dir / 'index.html').write_text(html, encoding='utf-8')
    print(f'  written: {post_dir}/index.html')

    update_sitemap(slug)
    update_blog_index(title, description, slug, cover)
    git_push(f'blog: add {slug}')
    print(f'  DONE: {SITE_URL}/poleznaya-informaciya/post/{slug}/')
    return slug

# ─── MAIN: AUTO MODE (идеи + публикация) ──────────────────────────────────────
def auto_run(count: int = 2):
    print(f'Generating {count} article ideas...')
    ideas = generate_ideas(count)
    for idea in ideas:
        print(f'\nIdea: {idea["title"]}')
        print(f'Why: {idea.get("why", "")}')
        create_post(
            title=idea['title'],
            description=idea['description'],
            keywords=idea['keywords'],
            image='truck.jpg'
        )

# ─── ENTRYPOINT ───────────────────────────────────────────────────────────────
if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        # Ручной режим: python3 auto_blog.py "Заголовок статьи"
        title = sys.argv[1]
        desc = sys.argv[2] if len(sys.argv) > 2 else title
        kw = sys.argv[3] if len(sys.argv) > 3 else 'грузоперевозки, Грузия, Россия, таможня'
        create_post(title, desc, kw)
    else:
        # Авто режим: генерирует 2 статьи
        auto_run(count=2)
