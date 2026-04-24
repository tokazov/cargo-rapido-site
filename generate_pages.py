#!/usr/bin/env python3
"""Generate all HTML pages for Cargo Rapido site."""

import os

BASE = "/root/.openclaw/workspace/cargo-rapido-site"

HEADER = """<header>
  <a href="/" class="logo"><div class="logo-box">🚛</div> Cargo Rapido</a>
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
      </div>
    </div>
    <a href="/poleznaya-informaciya/">Блог</a>
    <a href="/kontakty/">Контакты</a>
    <a href="https://wa.me/995568644615" class="nav-phone"><i class="fab fa-whatsapp" style="color:#25D366"></i> +995 568 644 615</a>
    <a href="https://t.me/CARGORAPIDO" target="_blank" class="nav-phone nav-cta">Заявка</a>
  </nav>
</header>"""

FOOTER = """<footer>
  <div class="footer-grid">
    <div class="footer-brand">
      <a href="/" class="logo"><div class="logo-box">🚛</div> Cargo Rapido</a>
      <p style="margin-top:16px;">Транспортно-логистическая компания. Грузоперевозки из Грузии в Россию, СНГ и Европу с 2014 года.</p>
      <p style="margin-top:12px;">Грузия, г. Тбилиси,<br>ул. Серго Закариадзе 5</p>
      <p style="margin-top:8px;">Пн-Сб 10:00–17:00</p>
    </div>
    <div class="footer-col">
      <h4>Услуги</h4>
      <ul>
        <li><a href="/perevozka-kommercheskih-gruzov/">Коммерческие грузы</a></li>
        <li><a href="/perevozka-lichnyh-veshchej/">Личные вещи</a></li>
        <li><a href="/dostavka-v-evropu/">Доставка в Европу</a></li>
        <li><a href="/dostavka-posylok-pisem-i-dokumentov-po-vsemu-miru/">Посылки и документы</a></li>
        <li><a href="/perevozka-gruzov-pod-termorezhimom/">Термо-режим</a></li>
        <li><a href="/skladskie-uslugi/">Склад</a></li>
        <li><a href="/brokerskie-uslugi/">Брокерские услуги</a></li>
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
        <li><a href="https://facebook.com/CargoRapido" target="_blank">Facebook</a></li>
      </ul>
    </div>
  </div>
  <div class="footer-bottom">
    <p>© 2024 Cargo Rapido. Все права защищены.</p>
    <p><a href="/sitemap.xml" style="color:rgba(255,255,255,0.4);text-decoration:none;">Карта сайта</a></p>
  </div>
</footer>"""

CHAT = """<div class="chat-widget">
  <div class="chat-bubble">
    <div class="cb-header">
      <div class="cb-avatar">👩</div>
      <div>
        <div class="cb-name">Наталья</div>
        <div class="cb-status">Онлайн сейчас</div>
      </div>
    </div>
    <div class="cb-text">Здравствуйте! Готова рассчитать стоимость доставки. Напишите маршрут и вес груза 😊</div>
    <a href="https://t.me/CARGORAPIDO" target="_blank" class="cb-btn">✈️ Написать в Telegram</a>
  </div>
  <a href="https://t.me/CARGORAPIDO" target="_blank" class="chat-trigger">
    💬
    <div class="chat-badge"></div>
  </a>
</div>"""

CTA = """<section class="cta-banner">
  <h2>Нужна перевозка из Грузии?</h2>
  <p>Напишите нам — рассчитаем стоимость за 5 минут и подберём оптимальный маршрут.</p>
  <div style="display:flex;gap:12px;justify-content:center;flex-wrap:wrap;">
    <a href="https://t.me/CARGORAPIDO" target="_blank" class="btn-dark"><i class="fab fa-telegram"></i> Написать в Telegram</a>
    <a href="https://wa.me/995568644615" target="_blank" class="btn-green"><i class="fab fa-whatsapp"></i> WhatsApp</a>
  </div>
</section>"""

def page(title, desc, canonical, og_img="https://cargorapido.com/truck.jpg", body=""):
    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <meta name="description" content="{desc}">
  <link rel="canonical" href="{canonical}">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{desc}">
  <meta property="og:url" content="{canonical}">
  <meta property="og:type" content="website">
  <meta property="og:image" content="{og_img}">
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
  <link rel="stylesheet" href="/style.css">
</head>
<body>
{HEADER}
{body}
{CTA}
{FOOTER}
{CHAT}
<script src="/shared.js"></script>
</body>
</html>"""

def article_page(title, desc, canonical, date, h1, content, breadcrumb_text):
    body = f"""<div class="page-hero">
  <div class="breadcrumb"><a href="/">Главная</a> → <a href="/poleznaya-informaciya/">Блог</a> → {breadcrumb_text}</div>
  <h1>{h1}</h1>
</div>
<div class="layout-two">
  <article class="article">
    <div class="content-body" style="padding:0">
      <p style="color:#888;font-size:14px;margin-bottom:24px;">📅 {date} · Cargo Rapido</p>
      {content}
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
    <div class="sidebar-card">
      <h4>Последние статьи</h4>
      <ul>
        <li><a href="/poleznaya-informaciya/post/perevozka-lichnyh-veshchej-iz-gruzii-v-rossiyu-v-usloviyah-sankcij/">Перевозка вещей из Грузии</a></li>
        <li><a href="/poleznaya-informaciya/post/aviadostavka-iz-gruzii-v-rossiyu/">Авиадоставка из Грузии</a></li>
        <li><a href="/poleznaya-informaciya/post/perevozka-sbornyh-gruzov/">Сборные грузы</a></li>
        <li><a href="/poleznaya-informaciya/post/pereezd-i-perevozka-veshchej-v-turciyu/">Переезд в Турцию</a></li>
        <li><a href="/poleznaya-informaciya/post/kak-perevezti-lichnye-veshchi-v-gruziyu-iz-rossii/">Переезд в Грузию из России</a></li>
      </ul>
    </div>
  </aside>
</div>"""
    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <meta name="description" content="{desc}">
  <link rel="canonical" href="{canonical}">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{desc}">
  <meta property="og:url" content="{canonical}">
  <meta property="og:type" content="article">
  <meta property="og:image" content="https://cargorapido.com/truck.jpg">
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
  <link rel="stylesheet" href="/style.css">
</head>
<body>
{HEADER}
{body}
{CTA}
{FOOTER}
{CHAT}
<script src="/shared.js"></script>
</body>
</html>"""

def write(path, content):
    full_path = os.path.join(BASE, path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✓ {path}")

# ===== ABOUT =====
write("about/index.html", page(
    "О компании | Cargo Rapido",
    "Cargo Rapido — транспортно-логистическая компания из Тбилиси. Более 10 лет на рынке. Грузоперевозки из Грузии в Россию и СНГ.",
    "https://cargorapido.com/about/",
    body="""<div class="page-hero">
  <div class="breadcrumb"><a href="/">Главная</a> → О компании</div>
  <h1>О компании Cargo Rapido</h1>
  <p>Мы — надёжный транспортный партнёр для бизнеса и частных лиц с 2014 года.</p>
</div>
<section class="section">
  <div class="stats-row" style="margin-bottom:60px;">
    <div class="stat-card"><div class="stat-val">10<span class="stat-unit">+</span></div><div class="stat-label">лет на рынке</div></div>
    <div class="stat-card"><div class="stat-val">5000<span class="stat-unit">+</span></div><div class="stat-label">доставленных грузов</div></div>
    <div class="stat-card"><div class="stat-val">15<span class="stat-unit">+</span></div><div class="stat-label">стран назначения</div></div>
    <div class="stat-card"><div class="stat-val">98<span class="stat-unit">%</span></div><div class="stat-label">довольных клиентов</div></div>
  </div>
  <div class="sec-tag">Наша история</div>
  <div class="sec-h2-sm">Кто мы</div>
  <div class="content-body" style="padding:0;max-width:800px;">
    <p>Cargo Rapido основана в 2014 году в Тбилиси. За более чем 10 лет работы мы стали одним из ведущих транспортных операторов на маршрутах Грузия–Россия–СНГ.</p>
    <p>Наша команда — это профессионалы с многолетним опытом в логистике, таможенном оформлении и организации международных перевозок. Мы знаем все нюансы работы на постсоветском пространстве.</p>
    <h2>Наши возможности</h2>
    <ul>
      <li>Собственный автопарк из 20+ единиц техники</li>
      <li>Склад в Тбилиси площадью 3000 м²</li>
      <li>Таможенный брокер в штате</li>
      <li>Партнёрские склады в Москве и Санкт-Петербурге</li>
      <li>GPS-трекинг каждого груза</li>
      <li>Круглосуточная поддержка клиентов</li>
    </ul>
    <h2>Наша миссия</h2>
    <p>Мы создаём прозрачную и надёжную логистику между Грузией и странами СНГ. Ваш груз — наша ответственность.</p>
  </div>
</section>
<section class="section section-light">
  <div class="sec-tag">Наша команда</div>
  <div class="sec-h2">Профессионалы своего дела</div>
  <div class="why-grid">
    <div class="why-item"><div class="why-ico">🚛</div><h3>Водители и логисты</h3><p>Опытные водители с международными лицензиями и знанием всех маршрутов.</p></div>
    <div class="why-item"><div class="why-ico">📋</div><h3>Таможенные брокеры</h3><p>Сертифицированные специалисты по таможенному оформлению Грузии и России.</p></div>
    <div class="why-item"><div class="why-ico">💬</div><h3>Менеджеры поддержки</h3><p>Персональные менеджеры ведут ваш груз от момента заявки до доставки.</p></div>
  </div>
</section>"""
))

# ===== NASHI-USLUGI =====
write("nashi-uslugi/index.html", page(
    "Наши услуги — Грузоперевозки из Грузии | Cargo Rapido",
    "Полный перечень услуг Cargo Rapido: коммерческие грузы, личные вещи, доставка в Европу, таможенный брокер, склад. Тбилиси.",
    "https://cargorapido.com/nashi-uslugi/",
    body="""<div class="page-hero">
  <div class="breadcrumb"><a href="/">Главная</a> → Услуги</div>
  <h1>Наши услуги</h1>
  <p>Полный спектр транспортно-логистических услуг из Грузии в Россию, СНГ и Европу.</p>
</div>
<section class="section">
  <div class="svc-grid">
    <a href="/perevozka-kommercheskih-gruzov/" class="svc">
      <div class="svc-num">01</div><div class="svc-ico">🚛</div>
      <h3>Коммерческие грузы</h3>
      <p>Перевозка товаров Грузия–Россия–Казахстан–Беларусь. GPS, страховка, таможня.</p>
      <div class="svc-link">Подробнее <i class="fas fa-arrow-right"></i></div>
    </a>
    <a href="/perevozka-lichnyh-veshchej/" class="svc">
      <div class="svc-num">02</div><div class="svc-ico">📦</div>
      <h3>Личные вещи</h3>
      <p>Переезды и перевозка личного имущества. Бережная упаковка, страховка.</p>
      <div class="svc-link">Подробнее <i class="fas fa-arrow-right"></i></div>
    </a>
    <a href="/dostavka-v-evropu/" class="svc">
      <div class="svc-num">03</div><div class="svc-ico">✈️</div>
      <h3>Доставка в Европу</h3>
      <p>Авиа и авто доставка в любую страну Европейского союза.</p>
      <div class="svc-link">Подробнее <i class="fas fa-arrow-right"></i></div>
    </a>
    <a href="/dostavka-posylok-pisem-i-dokumentov-po-vsemu-miru/" class="svc">
      <div class="svc-num">04</div><div class="svc-ico">📮</div>
      <h3>Посылки и документы</h3>
      <p>Доставка посылок, писем и документов по всему миру. Быстро и безопасно.</p>
      <div class="svc-link">Подробнее <i class="fas fa-arrow-right"></i></div>
    </a>
    <a href="/perevozka-gruzov-pod-termorezhimom/" class="svc">
      <div class="svc-num">05</div><div class="svc-ico">❄️</div>
      <h3>Термо-режим</h3>
      <p>Перевозка грузов, требующих контроля температуры. Фармацевтика, продукты.</p>
      <div class="svc-link">Подробнее <i class="fas fa-arrow-right"></i></div>
    </a>
    <a href="/skladskie-uslugi/" class="svc">
      <div class="svc-num">06</div><div class="svc-ico">🏭</div>
      <h3>Складские услуги</h3>
      <p>Собственный склад в Тбилиси. Хранение, сортировка, маркировка грузов.</p>
      <div class="svc-link">Подробнее <i class="fas fa-arrow-right"></i></div>
    </a>
    <a href="/brokerskie-uslugi/" class="svc">
      <div class="svc-num">07</div><div class="svc-ico">📋</div>
      <h3>Брокерские услуги</h3>
      <p>Полное таможенное оформление. Коды ТН ВЭД, расчёт платежей.</p>
      <div class="svc-link">Подробнее <i class="fas fa-arrow-right"></i></div>
    </a>
  </div>
</section>"""
))

# ===== SERVICE PAGES =====
def service_page(slug, num, ico, title_full, title_short, desc, canonical, h1, content):
    body = f"""<div class="page-hero">
  <div class="breadcrumb"><a href="/">Главная</a> → <a href="/nashi-uslugi/">Услуги</a> → {title_short}</div>
  <h1>{h1}</h1>
</div>
<section class="section">
  <div style="max-width:900px;">
    {content}
  </div>
</section>"""
    return page(title_full, desc, canonical, body=body)

write("perevozka-kommercheskih-gruzov/index.html", service_page(
    "perevozka-kommercheskih-gruzov", "01", "🚛",
    "Перевозка коммерческих грузов из Грузии | Cargo Rapido",
    "Коммерческие грузы",
    "Перевозка коммерческих грузов из Грузии в Россию, Казахстан, Беларусь. Собственный автопарк, GPS, страховка, таможня.",
    "https://cargorapido.com/perevozka-kommercheskih-gruzov/",
    "Перевозка коммерческих грузов из Грузии",
    """<p>Cargo Rapido специализируется на перевозке коммерческих грузов из Грузии в Россию, Казахстан, Беларусь и другие страны СНГ. Мы обеспечиваем полный цикл логистики — от забора груза на складе до доставки конечному получателю.</p>
    <h2>Что мы перевозим</h2>
    <ul>
      <li>Промышленные товары и оборудование</li>
      <li>Продукты питания (в рефрижераторах)</li>
      <li>Строительные материалы</li>
      <li>Одежда и текстиль</li>
      <li>Электроника и бытовая техника</li>
      <li>Автозапчасти и комплектующие</li>
    </ul>
    <h2>Наши преимущества</h2>
    <ul>
      <li>Собственный автопарк 20+ единиц</li>
      <li>GPS-трекинг каждого рейса</li>
      <li>Страховка груза включена в стоимость</li>
      <li>Таможенный брокер в штате</li>
      <li>Регулярные рейсы Тбилиси → Москва</li>
    </ul>
    <div class="info-box"><p>💡 Стоимость перевозки рассчитывается индивидуально в зависимости от веса, объёма и маршрута. Оставьте заявку — ответим в течение 15 минут.</p></div>"""
))

write("perevozka-lichnyh-veshchej/index.html", service_page(
    "perevozka-lichnyh-veshchej", "02", "📦",
    "Перевозка личных вещей из Грузии | Cargo Rapido",
    "Личные вещи",
    "Перевозка личных вещей при переезде из Грузии в Россию и СНГ. Бережная упаковка, страховка, таможенное оформление.",
    "https://cargorapido.com/perevozka-lichnyh-veshchej/",
    "Перевозка личных вещей из Грузии",
    """<p>Переезжаете? Cargo Rapido поможет перевезти все личные вещи из Грузии в Россию или другую страну СНГ. Мы обеспечиваем бережную упаковку, страховку и полное таможенное оформление.</p>
    <h2>Что мы перевозим</h2>
    <ul>
      <li>Мебель и бытовая техника</li>
      <li>Одежда и личные предметы</li>
      <li>Книги, документы, ценности</li>
      <li>Спортивный инвентарь</li>
      <li>Музыкальные инструменты</li>
    </ul>
    <h2>Как это работает</h2>
    <ol>
      <li>Вы оставляете заявку — менеджер связывается в течение 15 минут</li>
      <li>Оцениваем объём и рассчитываем стоимость</li>
      <li>Забираем вещи с вашего адреса</li>
      <li>Упаковываем и оформляем документы</li>
      <li>Доставляем до двери получателя</li>
    </ol>
    <div class="info-box"><p>⚖️ Максимальный вес одной партии для частных лиц: 30 кг / стоимость до $500. Это позволяет избежать таможенных пошлин.</p></div>"""
))

write("dostavka-v-evropu/index.html", service_page(
    "dostavka-v-evropu", "03", "✈️",
    "Доставка грузов в Европу из Грузии | Cargo Rapido",
    "Доставка в Европу",
    "Доставка грузов и посылок из Грузии в Европу. Авиа и автодоставка в любую страну ЕС. Cargo Rapido.",
    "https://cargorapido.com/dostavka-v-evropu/",
    "Доставка грузов в Европу из Грузии",
    """<p>Cargo Rapido организует доставку грузов из Грузии в любую страну Европы — как авиационным, так и автомобильным транспортом.</p>
    <h2>Направления</h2>
    <ul>
      <li>Германия, Австрия, Швейцария</li>
      <li>Франция, Испания, Италия</li>
      <li>Польша, Чехия, Венгрия</li>
      <li>Нидерланды, Бельгия, Скандинавия</li>
      <li>Другие страны ЕС — по запросу</li>
    </ul>
    <h2>Виды доставки</h2>
    <ul>
      <li><strong>Авиадоставка</strong> — от 3 до 7 дней. Для срочных грузов и документов.</li>
      <li><strong>Автодоставка</strong> — от 7 до 14 дней. Для крупных партий и переездов.</li>
    </ul>
    <div class="info-box"><p>🇪🇺 Мы оформляем все необходимые документы для ввоза груза в Европу, включая экспортную декларацию из Грузии.</p></div>"""
))

write("dostavka-posylok-pisem-i-dokumentov-po-vsemu-miru/index.html", service_page(
    "dostavka-posylok", "04", "📮",
    "Доставка посылок, писем и документов по всему миру | Cargo Rapido",
    "Посылки и документы",
    "Доставка посылок, писем и документов по всему миру из Грузии. Быстро, надёжно, с отслеживанием. Cargo Rapido.",
    "https://cargorapido.com/dostavka-posylok-pisem-i-dokumentov-po-vsemu-miru/",
    "Доставка посылок, писем и документов по всему миру",
    """<p>Нужно отправить посылку, важные документы или деловую корреспонденцию? Cargo Rapido доставит в любую точку мира.</p>
    <h2>Что мы доставляем</h2>
    <ul>
      <li>Деловые документы и контракты</li>
      <li>Личные посылки и подарки</li>
      <li>Образцы продукции</li>
      <li>Медицинские документы</li>
      <li>Юридические бумаги</li>
    </ul>
    <h2>Сроки доставки</h2>
    <ul>
      <li>Россия и СНГ: 3–5 дней</li>
      <li>Европа: 5–7 дней</li>
      <li>США и Азия: 7–14 дней</li>
    </ul>
    <div class="info-box"><p>📱 Каждому отправлению присваивается трек-номер для отслеживания в режиме реального времени.</p></div>"""
))

write("perevozka-gruzov-pod-termorezhimom/index.html", service_page(
    "perevozka-gruzov-pod-termorezhimom", "05", "❄️",
    "Перевозка грузов под термо-режимом из Грузии | Cargo Rapido",
    "Термо-режим",
    "Перевозка скоропортящихся грузов и продуктов с поддержанием температурного режима. Рефрижераторы. Cargo Rapido.",
    "https://cargorapido.com/perevozka-gruzov-pod-termorezhimom/",
    "Перевозка грузов под термо-режимом",
    """<p>Cargo Rapido располагает собственным рефрижераторным транспортом для перевозки грузов, требующих строгого контроля температуры.</p>
    <h2>Типы грузов</h2>
    <ul>
      <li>Продукты питания и скоропортящиеся товары</li>
      <li>Фармацевтика и медицинские препараты</li>
      <li>Косметика и химия</li>
      <li>Цветы и растения</li>
    </ul>
    <h2>Условия хранения</h2>
    <ul>
      <li>Охлаждение: от +2°C до +8°C</li>
      <li>Заморозка: от -18°C до -25°C</li>
      <li>Контролируемая температура: от 0°C до +25°C</li>
    </ul>
    <div class="info-box"><p>🌡️ Температурный режим контролируется и документируется на всём протяжении маршрута. Данные доступны клиенту.</p></div>"""
))

write("skladskie-uslugi/index.html", service_page(
    "skladskie-uslugi", "06", "🏭",
    "Складские услуги в Тбилиси | Cargo Rapido",
    "Склад",
    "Складские услуги в Тбилиси. Хранение, сортировка, маркировка, консолидация грузов. Cargo Rapido.",
    "https://cargorapido.com/skladskie-uslugi/",
    "Складские услуги в Тбилиси",
    """<p>Cargo Rapido располагает собственным складом площадью 3000 м² в Тбилиси. Мы предоставляем полный комплекс складских услуг.</p>
    <h2>Услуги склада</h2>
    <ul>
      <li>Ответственное хранение грузов</li>
      <li>Сортировка и маркировка</li>
      <li>Консолидация сборных грузов</li>
      <li>Упаковка и переупаковка</li>
      <li>Складирование крупногабаритных грузов</li>
      <li>Инвентаризация и учёт</li>
    </ul>
    <h2>Параметры склада</h2>
    <ul>
      <li>Площадь: 3000 м²</li>
      <li>Высота потолков: 8 м</li>
      <li>Охрана: 24/7</li>
      <li>Видеонаблюдение</li>
      <li>Современное оборудование</li>
    </ul>"""
))

write("brokerskie-uslugi/index.html", service_page(
    "brokerskie-uslugi", "07", "📋",
    "Брокерские и таможенные услуги | Cargo Rapido",
    "Брокерские услуги",
    "Таможенное оформление грузов в Грузии. Декларирование, коды ТН ВЭД, расчёт пошлин. Cargo Rapido.",
    "https://cargorapido.com/brokerskie-uslugi/",
    "Брокерские и таможенные услуги",
    """<p>В штате Cargo Rapido — сертифицированные таможенные брокеры Грузии и России. Мы берём на себя все вопросы таможенного оформления.</p>
    <h2>Что включает услуга</h2>
    <ul>
      <li>Консультация по таможенному законодательству</li>
      <li>Подбор кодов ТН ВЭД</li>
      <li>Расчёт таможенных пошлин и НДС</li>
      <li>Подготовка пакета документов</li>
      <li>Подача декларации и сопровождение</li>
      <li>Взаимодействие с таможенными органами</li>
    </ul>
    <h2>Наш опыт</h2>
    <ul>
      <li>Более 1000 оформленных деклараций в год</li>
      <li>Работа с товарами любых категорий</li>
      <li>Опыт на таможне Грузии, России, ЕС</li>
    </ul>
    <div class="info-box"><p>⚡ Мы оформляем таможенные документы в кратчайшие сроки, минимизируя время простоя вашего груза.</p></div>"""
))

# ===== BLOG INDEX =====
blog_posts = [
    ("25 ноября 2025", "Перевозка личных вещей из Грузии в Россию в условиях санкций", "Как легально перевезти личные вещи. Ограничения, документы, партии до 30 кг/$500.", "/poleznaya-informaciya/post/perevozka-lichnyh-veshchej-iz-gruzii-v-rossiyu-v-usloviyah-sankcij/"),
    ("5 марта 2025", "Авиадоставка грузов и личных вещей в Россию", "Быстрая авиадоставка из Тбилиси в Москву с таможенным оформлением.", "/poleznaya-informaciya/post/aviadostavka-iz-gruzii-v-rossiyu/"),
    ("23 ноября 2024", "Перевозка сборных грузов из Грузии", "Экономная доставка сборных грузов от одной паллеты в Россию и СНГ.", "/poleznaya-informaciya/post/perevozka-sbornyh-gruzov/"),
    ("18 октября 2024", "Как быстро и безопасно отправить свои вещи из Грузии в Россию, страны СНГ", "Пошаговая инструкция по отправке личных вещей с таможней, страховкой и GPS.", "/poleznaya-informaciya/post/kak-bystro-i-bezopasno-otpravit-svoi-veshchi-iz-gruzii-v-rossiyu-strany-sng/"),
    ("18 октября 2024", "Быстрая и безопасная доставка личных вещей из Грузии в Европу и по миру", "Авиадоставка и автодоставка личных вещей из Тбилиси в Европу.", "/poleznaya-informaciya/post/bystraya-i-bezopasnaya-dostavka-lichnyh-veshchej-iz-gruzii-v-evropu-i-po-miru/"),
    ("22 апреля 2023", "Переезд и перевозка вещей в Турцию", "Организация переезда и перевозки личных вещей из Грузии в Турцию.", "/poleznaya-informaciya/post/pereezd-i-perevozka-veshchej-v-turciyu/"),
    ("27 января 2023", "Как перевезти личные вещи в Грузию из России?", "Организация переезда из России в Грузию: вещи, документы, таможня.", "/poleznaya-informaciya/post/kak-perevezti-lichnye-veshchi-v-gruziyu-iz-rossii/"),
]

blog_cards = "\n".join([f"""    <a href="{url}" class="blog-card">
      <div class="blog-date">{date}</div>
      <h3>{title}</h3>
      <p>{desc}</p>
      <div class="blog-read">Читать <i class="fas fa-arrow-right"></i></div>
    </a>""" for date, title, desc, url in blog_posts])

write("poleznaya-informaciya/index.html", page(
    "Полезная информация — Блог о грузоперевозках | Cargo Rapido",
    "Статьи о грузоперевозках из Грузии в Россию и СНГ. Советы, инструкции, актуальная информация. Cargo Rapido.",
    "https://cargorapido.com/poleznaya-informaciya/",
    body=f"""<div class="page-hero">
  <div class="breadcrumb"><a href="/">Главная</a> → Блог</div>
  <h1>Полезная информация</h1>
  <p>Статьи, советы и актуальная информация о грузоперевозках из Грузии.</p>
</div>
<section class="section">
  <div class="blog-grid">
{blog_cards}
  </div>
</section>"""
))

# ===== BLOG ARTICLES =====
# Article 1
write("poleznaya-informaciya/post/aviadostavka-iz-gruzii-v-rossiyu/index.html",
article_page(
    "Авиадоставка из Грузии в Россию | Cargo Rapido",
    "Авиадоставка грузов и личных вещей из Грузии в Россию. Быстро, надёжно, с таможенным оформлением. Cargo Rapido.",
    "https://cargorapido.com/poleznaya-informaciya/post/aviadostavka-iz-gruzii-v-rossiyu/",
    "5 марта 2025",
    "Авиадоставка грузов и личных вещей в Россию с компанией Cargo Rapido",
    """<p>Авиадоставка — оптимальный выбор, когда важна скорость. Cargo Rapido организует авиационную доставку грузов и личных вещей из Тбилиси в Москву, Санкт-Петербург и другие города России.</p>
    <h2>Когда выбирать авиадоставку?</h2>
    <ul>
      <li>Срочные отправления — документы, медикаменты, запчасти</li>
      <li>Ценные грузы с минимальным временем в пути</li>
      <li>Небольшие партии (до 100 кг)</li>
      <li>Когда наземный маршрут недоступен или задержан</li>
    </ul>
    <h2>Сроки и маршруты</h2>
    <p>Тбилиси → Москва: от 1 до 3 дней. Регулярные рейсы несколько раз в неделю.</p>
    <p>Тбилиси → Санкт-Петербург: от 2 до 4 дней.</p>
    <h2>Таможенное оформление</h2>
    <p>Наши таможенные брокеры оформляют все необходимые документы для ввоза груза в Россию. Вам не нужно разбираться в тонкостях таможенного законодательства — мы берём это на себя.</p>
    <h2>Стоимость авиадоставки</h2>
    <p>Цена рассчитывается индивидуально в зависимости от веса, объёма и срочности. Свяжитесь с нашим менеджером для получения точного расчёта.</p>
    <div class="info-box"><p>✈️ Для срочных отправлений мы можем организовать доставку «день в день» при наличии места на рейсе.</p></div>""",
    "Авиадоставка из Грузии в Россию"
))

# Article 2
write("poleznaya-informaciya/post/perevozka-lichnyh-veshchej-iz-gruzii-v-rossiyu-v-usloviyah-sankcij/index.html",
article_page(
    "Перевозка личных вещей из Грузии в Россию в условиях санкций | Cargo Rapido",
    "Легальная перевозка личных вещей из Грузии в Россию. Партии до 30кг/$500. Cargo Rapido.",
    "https://cargorapido.com/poleznaya-informaciya/post/perevozka-lichnyh-veshchej-iz-gruzii-v-rossiyu-v-usloviyah-sankcij/",
    "25 ноября 2025",
    "Перевозка личных вещей из Грузии в Россию в условиях санкций",
    """<p>В условиях санкций перевозка личных вещей из Грузии в Россию имеет ряд особенностей. Cargo Rapido помогает клиентам легально перевезти имущество в соответствии с действующим законодательством.</p>
    <h2>Ограничения на ввоз</h2>
    <p>Физическое лицо вправе ввезти в Россию личные вещи без уплаты таможенных пошлин при соблюдении следующих условий:</p>
    <ul>
      <li>Суммарный вес не превышает 31 кг на человека</li>
      <li>Стоимость товаров не превышает 1000 евро (при авиадоставке) или 500 евро (при других видах доставки)</li>
      <li>Товары носят личный, а не коммерческий характер</li>
    </ul>
    <h2>Что не разрешено ввозить</h2>
    <ul>
      <li>Санкционные товары (перечень утверждён Правительством РФ)</li>
      <li>Оружие и боеприпасы без разрешения</li>
      <li>Наркотические вещества</li>
    </ul>
    <h2>Как мы помогаем</h2>
    <p>Cargo Rapido консультирует клиентов по актуальным ограничениям и помогает правильно задекларировать товары. Мы работаем только в рамках закона.</p>
    <div class="info-box"><p>📋 Для актуальной информации об ограничениях свяжитесь с нашим менеджером — законодательство регулярно меняется, и мы всегда в курсе последних изменений.</p></div>""",
    "Перевозка вещей из Грузии в Россию"
))

# Article 3
write("poleznaya-informaciya/post/perevozka-sbornyh-gruzov/index.html",
article_page(
    "Перевозка сборных грузов из Грузии | Cargo Rapido",
    "Перевозка сборных грузов из Грузии в Россию и СНГ. От одной паллеты. Cargo Rapido.",
    "https://cargorapido.com/poleznaya-informaciya/post/perevozka-sbornyh-gruzov/",
    "23 ноября 2024",
    "Перевозка сборных грузов",
    """<p>Сборный груз — это экономичный способ доставки, при котором несколько небольших отправлений объединяются в одном транспортном средстве. Вы платите только за фактически занятое место.</p>
    <h2>Преимущества сборной перевозки</h2>
    <ul>
      <li>Экономия до 50% по сравнению с выделенным транспортом</li>
      <li>Отправка грузов от 1 паллеты или 50 кг</li>
      <li>Регулярные отправки по расписанию</li>
      <li>Страховка каждого отправления</li>
    </ul>
    <h2>Как работает сборный груз</h2>
    <ol>
      <li>Вы привозите груз на наш склад в Тбилиси или заказываете забор</li>
      <li>Мы маркируем и консолидируем грузы от разных клиентов</li>
      <li>Машина отправляется по расписанию</li>
      <li>На складе в городе назначения груз сортируется и доставляется</li>
    </ol>
    <h2>Расписание отправок</h2>
    <p>Тбилиси → Москва: каждый вторник и пятница<br>
    Тбилиси → Казахстан: каждые 10 дней<br>
    Тбилиси → Беларусь: еженедельно</p>
    <div class="info-box"><p>📦 Минимальный объём для сборной перевозки: 0,1 м³ или 50 кг. Максимум — без ограничений.</p></div>""",
    "Перевозка сборных грузов"
))

# Article 4
write("poleznaya-informaciya/post/kak-bystro-i-bezopasno-otpravit-svoi-veshchi-iz-gruzii-v-rossiyu-strany-sng/index.html",
article_page(
    "Как быстро отправить вещи из Грузии в Россию и СНГ | Cargo Rapido",
    "Отправка личных вещей из Грузии в Россию и СНГ. Таможня, страховка, GPS. Cargo Rapido.",
    "https://cargorapido.com/poleznaya-informaciya/post/kak-bystro-i-bezopasno-otpravit-svoi-veshchi-iz-gruzii-v-rossiyu-strany-sng/",
    "18 октября 2024",
    "Как быстро и безопасно отправить свои вещи из Грузии в Россию, страны СНГ",
    """<p>Планируете отправить вещи из Грузии в Россию или другие страны СНГ? Рассказываем пошаговый план действий, чтобы всё прошло быстро, безопасно и без лишних расходов.</p>
    <h2>Шаг 1: Подготовьте список вещей</h2>
    <p>Заранее составьте перечень всего, что собираетесь отправить. Это поможет правильно рассчитать объём, стоимость и оценить таможенные риски.</p>
    <h2>Шаг 2: Свяжитесь с Cargo Rapido</h2>
    <p>Напишите нам в Telegram или WhatsApp. Менеджер ответит в течение 15 минут, уточнит детали и предложит оптимальный способ доставки.</p>
    <h2>Шаг 3: Упаковка и забор груза</h2>
    <p>Мы можем забрать вещи с вашего адреса в Тбилиси или принять на нашем складе. Профессионально упакуем хрупкие предметы.</p>
    <h2>Шаг 4: Таможенное оформление</h2>
    <p>Наши брокеры подготовят все необходимые документы для прохождения таможни.</p>
    <h2>Шаг 5: Отслеживание и доставка</h2>
    <p>Вы получаете трек-номер и можете следить за грузом онлайн. По прибытии доставляем до двери.</p>
    <div class="info-box"><p>⏱️ Среднее время доставки Тбилиси → Москва: 4–6 дней при автодоставке, 1–3 дня при авиадоставке.</p></div>""",
    "Отправить вещи из Грузии"
))

# Article 5
write("poleznaya-informaciya/post/bystraya-i-bezopasnaya-dostavka-lichnyh-veshchej-iz-gruzii-v-evropu-i-po-miru/index.html",
article_page(
    "Доставка личных вещей из Грузии в Европу и по миру | Cargo Rapido",
    "Доставка личных вещей из Грузии в Европу и по всему миру. Авиадоставка, страховка. Cargo Rapido.",
    "https://cargorapido.com/poleznaya-informaciya/post/bystraya-i-bezopasnaya-dostavka-lichnyh-veshchej-iz-gruzii-v-evropu-i-po-miru/",
    "18 октября 2024",
    "Быстрая и безопасная доставка личных вещей из Грузии в Европу и по миру",
    """<p>Cargo Rapido организует доставку личных вещей из Грузии в любую страну мира. Авиадоставка или автодоставка — выбирайте оптимальный вариант.</p>
    <h2>Доставка в Европу</h2>
    <p>Авиадоставка в страны ЕС занимает от 3 до 7 дней. Мы оформляем экспортную декларацию из Грузии и все документы для ввоза в европейскую страну назначения.</p>
    <h2>Доставка в США, Канаду, Австралию</h2>
    <p>Международная авиадоставка занимает от 7 до 14 дней. Мы сотрудничаем с ведущими международными перевозчиками.</p>
    <h2>Доставка в Азию</h2>
    <p>Китай, Япония, Корея — от 5 до 10 дней авиадоставкой.</p>
    <h2>Что включено в стоимость</h2>
    <ul>
      <li>Забор груза в Тбилиси</li>
      <li>Упаковка</li>
      <li>Страховка</li>
      <li>Таможенное оформление на вывоз</li>
      <li>Международная доставка</li>
    </ul>""",
    "Доставка вещей из Грузии в Европу"
))

# Article 6
write("poleznaya-informaciya/post/pereezd-i-perevozka-veshchej-v-turciyu/index.html",
article_page(
    "Переезд и перевозка вещей в Турцию | Cargo Rapido",
    "Безопасный переезд в Турцию из Грузии. Перевозка личных вещей с оформлением документов. Cargo Rapido.",
    "https://cargorapido.com/poleznaya-informaciya/post/pereezd-i-perevozka-veshchej-v-turciyu/",
    "22 апреля 2023",
    "Переезд и перевозка вещей в Турцию",
    """<p>Переезд в Турцию — популярное направление среди наших клиентов. Cargo Rapido организует перевозку всего вашего имущества из Тбилиси в любой город Турции.</p>
    <h2>Маршруты</h2>
    <ul>
      <li>Тбилиси → Стамбул</li>
      <li>Тбилиси → Анталья</li>
      <li>Тбилиси → Измир</li>
      <li>Тбилиси → Анкара</li>
    </ul>
    <h2>Особенности переезда в Турцию</h2>
    <p>Турция не является членом Таможенного союза, поэтому для ввоза личных вещей необходимо пройти таможенное оформление на турецкой границе. Наши брокеры имеют опыт работы именно с турецкой таможней.</p>
    <h2>Что разрешено ввозить</h2>
    <p>Личные вещи и предметы домашнего обихода ввозятся беспошлинно при условии, что вы становитесь резидентом Турции. Мы поможем правильно оформить документы.</p>
    <h2>Сроки доставки</h2>
    <p>Тбилиси → Стамбул: 2–4 дня автодоставкой. Маршрут проходит через территорию Грузии, поэтому граница одна.</p>""",
    "Переезд в Турцию из Грузии"
))

# Article 7
write("poleznaya-informaciya/post/kak-perevezti-lichnye-veshchi-v-gruziyu-iz-rossii/index.html",
article_page(
    "Как перевезти личные вещи в Грузию из России | Cargo Rapido",
    "Организация переезда из России в Грузию. Перевозка вещей, документы, таможня. Cargo Rapido.",
    "https://cargorapido.com/poleznaya-informaciya/post/kak-perevezti-lichnye-veshchi-v-gruziyu-iz-rossii/",
    "27 января 2023",
    "Как перевезти личные вещи в Грузию из России?",
    """<p>Переезд из России в Грузию стал одним из самых популярных запросов в 2022–2023 годах. Cargo Rapido помогает тысячам семей организовать этот переезд.</p>
    <h2>Откуда мы забираем грузы в России</h2>
    <ul>
      <li>Москва и Московская область</li>
      <li>Санкт-Петербург</li>
      <li>Краснодар и Сочи</li>
      <li>Другие города — по запросу</li>
    </ul>
    <h2>Таможня Россия → Грузия</h2>
    <p>Вывоз личных вещей из России в Грузию в целом не ограничен. Однако существуют ограничения на вывоз валюты, ювелирных украшений свыше определённой стоимости, предметов культурного наследия.</p>
    <h2>Ввоз в Грузию</h2>
    <p>Грузия — одна из наиболее либеральных стран в части таможенного законодательства. Личные вещи ввозятся без ограничений и пошлин.</p>
    <h2>Сроки</h2>
    <p>Москва → Тбилиси: 5–7 дней автодоставкой. Маршрут через Владикавказ и КПП «Верхний Ларс».</p>
    <div class="info-box"><p>⚠️ КПП «Верхний Ларс» периодически закрывается. Мы всегда информируем клиентов об актуальной ситуации на границе.</p></div>""",
    "Переезд из России в Грузию"
))

# ===== CONTACTS =====
write("kontakty/index.html", page(
    "Контакты | Cargo Rapido — Грузоперевозки из Тбилиси",
    "Контакты Cargo Rapido. Тбилиси, ул. Серго Закариадзе 5. Telegram, WhatsApp, Facebook. Пн-Сб 10:00-17:00.",
    "https://cargorapido.com/kontakty/",
    body="""<div class="page-hero">
  <div class="breadcrumb"><a href="/">Главная</a> → Контакты</div>
  <h1>Контакты</h1>
  <p>Мы на связи в рабочие дни с 10:00 до 17:00 по тбилисскому времени.</p>
</div>
<section class="section">
  <div class="contacts-grid">
    <div class="contact-info">
      <h2>Как с нами связаться</h2>
      <div class="contact-row">
        <div class="contact-ico"><i class="fas fa-map-marker-alt"></i></div>
        <div>
          <h4>Адрес</h4>
          <p>Грузия, г. Тбилиси,<br>ул. Серго Закариадзе 5</p>
        </div>
      </div>
      <div class="contact-row">
        <div class="contact-ico"><i class="fas fa-clock"></i></div>
        <div>
          <h4>График работы</h4>
          <p>Понедельник – Суббота<br>10:00 – 17:00</p>
        </div>
      </div>
      <div class="contact-row">
        <div class="contact-ico"><i class="fab fa-whatsapp"></i></div>
        <div>
          <h4>WhatsApp</h4>
          <a href="https://wa.me/995568644615">+995 568 644 615</a>
        </div>
      </div>
      <div class="contact-row">
        <div class="contact-ico"><i class="fab fa-telegram"></i></div>
        <div>
          <h4>Telegram</h4>
          <a href="https://t.me/CARGORAPIDO" target="_blank">@CARGORAPIDO</a>
        </div>
      </div>
      <div class="contact-row">
        <div class="contact-ico"><i class="fab fa-facebook"></i></div>
        <div>
          <h4>Facebook</h4>
          <a href="https://facebook.com/CargoRapido" target="_blank">CargoRapido</a>
        </div>
      </div>
      <div class="social-row">
        <a href="https://t.me/CARGORAPIDO" target="_blank" class="social-btn tg"><i class="fab fa-telegram"></i> Telegram</a>
        <a href="https://wa.me/995568644615" target="_blank" class="social-btn wa"><i class="fab fa-whatsapp"></i> WhatsApp</a>
        <a href="https://facebook.com/CargoRapido" target="_blank" class="social-btn fb"><i class="fab fa-facebook"></i> Facebook</a>
      </div>
    </div>
    <div>
      <div class="map-placeholder">🗺️</div>
      <p style="text-align:center;color:#888;font-size:14px;margin-top:12px;">г. Тбилиси, ул. Серго Закариадзе 5</p>
    </div>
  </div>
</section>"""
))

print("\n✅ All pages generated!")
