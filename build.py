#!/usr/bin/env python3
"""Master build script for cargo-rapido-site SEO & feature updates."""

import os
import re
import subprocess

BASE = '/root/.openclaw/workspace/cargo-rapido-site'

# ============================================================
# HELPERS
# ============================================================

def read_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'  wrote: {path}')

def git_commit(msg):
    subprocess.run(['git', '-C', BASE, 'add', '-A'], check=True)
    result = subprocess.run(['git', '-C', BASE, 'diff', '--cached', '--quiet'])
    if result.returncode != 0:
        subprocess.run(['git', '-C', BASE, 'commit', '-m', msg], check=True)
        print(f'  git commit: {msg}')
    else:
        print(f'  (nothing to commit for: {msg})')

# ============================================================
# BLOCK 1: sitemap.xml and robots.txt
# ============================================================

def block1_sitemap_robots():
    print('\n=== BLOCK 1: sitemap.xml + robots.txt ===')
    
    sitemap = '''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url><loc>https://cargorapido.com/</loc><lastmod>2026-05-26</lastmod><changefreq>weekly</changefreq><priority>1.0</priority></url>
  <url><loc>https://cargorapido.com/about/</loc><lastmod>2026-05-26</lastmod><changefreq>monthly</changefreq><priority>0.7</priority></url>
  <url><loc>https://cargorapido.com/nashi-uslugi/</loc><lastmod>2026-05-26</lastmod><changefreq>monthly</changefreq><priority>0.8</priority></url>
  <url><loc>https://cargorapido.com/perevozka-kommercheskih-gruzov/</loc><lastmod>2026-05-26</lastmod><changefreq>monthly</changefreq><priority>0.9</priority></url>
  <url><loc>https://cargorapido.com/perevozka-lichnyh-veshchej/</loc><lastmod>2026-05-26</lastmod><changefreq>monthly</changefreq><priority>0.9</priority></url>
  <url><loc>https://cargorapido.com/dostavka-v-evropu/</loc><lastmod>2026-05-26</lastmod><changefreq>monthly</changefreq><priority>0.8</priority></url>
  <url><loc>https://cargorapido.com/dostavka-posylok-pisem-i-dokumentov-po-vsemu-miru/</loc><lastmod>2026-05-26</lastmod><changefreq>monthly</changefreq><priority>0.8</priority></url>
  <url><loc>https://cargorapido.com/perevozka-gruzov-pod-termorezhimom/</loc><lastmod>2026-05-26</lastmod><changefreq>monthly</changefreq><priority>0.8</priority></url>
  <url><loc>https://cargorapido.com/perevozka-avtomobilya-na-avtovoze/</loc><lastmod>2026-05-26</lastmod><changefreq>monthly</changefreq><priority>0.8</priority></url>
  <url><loc>https://cargorapido.com/perevozka-avtomobilya-na-evakuatore/</loc><lastmod>2026-05-26</lastmod><changefreq>monthly</changefreq><priority>0.8</priority></url>
  <url><loc>https://cargorapido.com/skladskie-uslugi/</loc><lastmod>2026-05-26</lastmod><changefreq>monthly</changefreq><priority>0.7</priority></url>
  <url><loc>https://cargorapido.com/brokerskie-uslugi/</loc><lastmod>2026-05-26</lastmod><changefreq>monthly</changefreq><priority>0.7</priority></url>
  <url><loc>https://cargorapido.com/poleznaya-informaciya/</loc><lastmod>2026-05-26</lastmod><changefreq>weekly</changefreq><priority>0.8</priority></url>
  <url><loc>https://cargorapido.com/poleznaya-informaciya/post/aviadostavka-iz-gruzii-v-rossiyu/</loc><lastmod>2025-03-05</lastmod><changefreq>monthly</changefreq><priority>0.7</priority></url>
  <url><loc>https://cargorapido.com/poleznaya-informaciya/post/perevozka-lichnyh-veshchej-iz-gruzii-v-rossiyu-v-usloviyah-sankcij/</loc><lastmod>2025-11-25</lastmod><changefreq>monthly</changefreq><priority>0.7</priority></url>
  <url><loc>https://cargorapido.com/poleznaya-informaciya/post/perevozka-sbornyh-gruzov/</loc><lastmod>2024-11-23</lastmod><changefreq>monthly</changefreq><priority>0.7</priority></url>
  <url><loc>https://cargorapido.com/poleznaya-informaciya/post/kak-bystro-i-bezopasno-otpravit-svoi-veshchi-iz-gruzii-v-rossiyu-strany-sng/</loc><lastmod>2024-10-18</lastmod><changefreq>monthly</changefreq><priority>0.7</priority></url>
  <url><loc>https://cargorapido.com/poleznaya-informaciya/post/bystraya-i-bezopasnaya-dostavka-lichnyh-veshchej-iz-gruzii-v-evropu-i-po-miru/</loc><lastmod>2024-10-18</lastmod><changefreq>monthly</changefreq><priority>0.7</priority></url>
  <url><loc>https://cargorapido.com/poleznaya-informaciya/post/pereezd-i-perevozka-veshchej-v-turciyu/</loc><lastmod>2023-04-22</lastmod><changefreq>monthly</changefreq><priority>0.7</priority></url>
  <url><loc>https://cargorapido.com/poleznaya-informaciya/post/kak-perevezti-lichnye-veshchi-v-gruziyu-iz-rossii/</loc><lastmod>2023-01-27</lastmod><changefreq>monthly</changefreq><priority>0.7</priority></url>
  <url><loc>https://cargorapido.com/kontakty/</loc><lastmod>2026-05-26</lastmod><changefreq>monthly</changefreq><priority>0.7</priority></url>
  <url><loc>https://cargorapido.com/otzyvy/</loc><lastmod>2026-05-26</lastmod><changefreq>monthly</changefreq><priority>0.6</priority></url>
  <url><loc>https://cargorapido.com/politika-konfidencialnosti/</loc><lastmod>2026-05-26</lastmod><changefreq>yearly</changefreq><priority>0.3</priority></url>
  <url><loc>https://cargorapido.com/usloviya-okazaniya-uslug/</loc><lastmod>2026-05-26</lastmod><changefreq>yearly</changefreq><priority>0.3</priority></url>
  <url><loc>https://cargorapido.com/soglasie-na-obrabotku/</loc><lastmod>2026-05-26</lastmod><changefreq>yearly</changefreq><priority>0.3</priority></url>
</urlset>'''
    
    robots = '''User-agent: *
Allow: /
Disallow: /*?*
Disallow: /404
Sitemap: https://cargorapido.com/sitemap.xml'''
    
    write_file(os.path.join(BASE, 'sitemap.xml'), sitemap)
    write_file(os.path.join(BASE, 'robots.txt'), robots)
    git_commit('Block 1: Update sitemap.xml (25 URLs) and robots.txt')

# ============================================================
# BLOCK 2: META tags on all pages
# ============================================================

# Common head additions (verification, analytics, GTM)
COMMON_HEAD_ADDITIONS = '''  <meta name="google-site-verification" content="U4VPSdMvjvNSx8QubmIyhUwQPcS6y2hnZsIyLe6PMqM">
  <meta name="yandex-verification" content="8d6727b9489f571e">
  <meta name="twitter:card" content="summary_large_image">
  <!-- Яндекс.Метрика -->
  <script type="text/javascript">
   (function(m,e,t,r,i,k,a){m[i]=m[i]||function(){(m[i].a=m[i].a||[]).push(arguments)};
   m[i].l=1*new Date();
   for(var j=0;j<document.scripts.length;j++){if(document.scripts[j].src===r){return;}}
   k=e.createElement(t),a=e.getElementsByTagName(t)[0],k.async=1,k.src=r,a.parentNode.insertBefore(k,a)})
   (window, document, "script", "https://mc.yandex.ru/metrika/tag.js", "ym");
   ym(90606836, "init", {
        clickmap:true,
        trackLinks:true,
        accurateTrackBounce:true,
        webvisor:true
   });
  </script>
  <noscript><div><img src="https://mc.yandex.ru/watch/90606836" style="position:absolute; left:-9999px;" alt="" /></div></noscript>
  <!-- End Яндекс.Метрика -->
  <!-- Google Tag Manager -->
  <script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':
  new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],
  j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
  'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
  })(window,document,'script','dataLayer','GTM-MLNDMC75');</script>
  <!-- End Google Tag Manager -->'''

GTM_NOSCRIPT = '''<!-- Google Tag Manager (noscript) -->
<noscript><iframe src="https://www.googletagmanager.com/ns.html?id=GTM-MLNDMC75"
height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
<!-- End Google Tag Manager (noscript) -->'''

# Favicon meta tags
FAVICON_META = '''  <link rel="icon" type="image/x-icon" href="/favicon.ico">
  <link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">
  <link rel="manifest" href="/manifest.json">
  <meta name="theme-color" content="#1a237e">'''

# Page-specific meta data
PAGE_META = {
    'index.html': {
        'title': 'Cargo Rapido — Грузоперевозки из Грузии в Россию и СНГ',
        'desc': 'Надёжные грузоперевозки из Грузии в Россию, Казахстан, Беларусь и Европу. 10+ лет на рынке. Таможня, GPS, страховка. Получите расчёт за 5 минут!',
        'canonical': 'https://cargorapido.com/',
        'og_image': 'https://cargorapido.com/hero-main.jpg',
    },
    'about/index.html': {
        'title': 'О компании Cargo Rapido — Транспортная компания в Тбилиси',
        'desc': 'Cargo Rapido — транспортно-логистическая компания в Тбилиси с 2014 года. Собственный автопарк, склады, таможенный брокер. Узнайте о нас больше!',
        'canonical': 'https://cargorapido.com/about/',
        'og_image': 'https://cargorapido.com/about-team.jpg',
    },
    'kontakty/index.html': {
        'title': 'Контакты Cargo Rapido — Позвоните или напишите нам',
        'desc': 'Cargo Rapido в Тбилиси, ул. Серго Закариадзе 5. Telegram @CARGORAPIDO, WhatsApp +995568644615. Пн-Сб 10:00-17:00. Ответим за 15 минут!',
        'canonical': 'https://cargorapido.com/kontakty/',
        'og_image': 'https://cargorapido.com/truck.jpg',
    },
    'nashi-uslugi/index.html': {
        'title': 'Наши услуги — Cargo Rapido | Грузоперевозки из Грузии',
        'desc': 'Полный спектр транспортно-логистических услуг: коммерческие и личные грузы, Европа, термо-режим, склад, таможенный брокер. Рассчитайте стоимость!',
        'canonical': 'https://cargorapido.com/nashi-uslugi/',
        'og_image': 'https://cargorapido.com/truck.jpg',
    },
    'perevozka-kommercheskih-gruzov/index.html': {
        'title': 'Перевозка коммерческих грузов из Грузии в Россию и СНГ',
        'desc': 'Грузоперевозки Грузия–Россия, Казахстан, Беларусь. Паллеты, сборные грузы, FTL. GPS-трекинг, страховка, таможенный брокер. Узнайте цену!',
        'canonical': 'https://cargorapido.com/perevozka-kommercheskih-gruzov/',
        'og_image': 'https://cargorapido.com/commercial-cargo.jpg',
    },
    'perevozka-lichnyh-veshchej/index.html': {
        'title': 'Перевозка личных вещей из Грузии в Россию и СНГ',
        'desc': 'Перевезём ваши личные вещи из Грузии в Россию, Казахстан, Беларусь и Европу. Бережная упаковка, страховка, доставка от двери до двери.',
        'canonical': 'https://cargorapido.com/perevozka-lichnyh-veshchej/',
        'og_image': 'https://cargorapido.com/blog-personal.jpg',
    },
    'dostavka-v-evropu/index.html': {
        'title': 'Доставка грузов в Европу из Грузии — Cargo Rapido',
        'desc': 'Авиа и автодоставка из Грузии в Германию, Польшу, Италию и другие страны ЕС. Таможенное оформление, страховка. Получите расчёт сегодня!',
        'canonical': 'https://cargorapido.com/dostavka-v-evropu/',
        'og_image': 'https://cargorapido.com/europe-delivery.jpg',
    },
    'dostavka-posylok-pisem-i-dokumentov-po-vsemu-miru/index.html': {
        'title': 'Доставка посылок, писем и документов по всему миру',
        'desc': 'Международная экспресс-доставка посылок, писем, документов из Грузии. Отслеживание отправлений, надёжная упаковка. Отправьте посылку сейчас!',
        'canonical': 'https://cargorapido.com/dostavka-posylok-pisem-i-dokumentov-po-vsemu-miru/',
        'og_image': 'https://cargorapido.com/documents.jpg',
    },
    'perevozka-gruzov-pod-termorezhimom/index.html': {
        'title': 'Перевозка грузов под термо-режимом из Грузии | Cargo Rapido',
        'desc': 'Рефрижераторные перевозки фармацевтики, продуктов питания и термочувствительных грузов из Грузии. Контроль температуры. Заявка онлайн!',
        'canonical': 'https://cargorapido.com/perevozka-gruzov-pod-termorezhimom/',
        'og_image': 'https://cargorapido.com/reefer-fleet.jpg',
    },
    'perevozka-avtomobilya-na-avtovoze/index.html': {
        'title': 'Перевозка автомобиля на автовозе из Грузии | Cargo Rapido',
        'desc': 'Безопасная перевозка автомобилей на автовозе из Грузии в Россию, СНГ и Европу. Страховка, GPS-трекинг. Рассчитайте стоимость за 5 минут!',
        'canonical': 'https://cargorapido.com/perevozka-avtomobilya-na-avtovoze/',
        'og_image': 'https://cargorapido.com/car-transport.jpg',
    },
    'perevozka-avtomobilya-na-evakuatore/index.html': {
        'title': 'Перевозка автомобиля на эвакуаторе из Грузии | Cargo Rapido',
        'desc': 'Транспортировка автомобиля на эвакуаторе из Грузии в Россию и СНГ. Аварийные автомобили, техника, нестандартный транспорт. Звоните!',
        'canonical': 'https://cargorapido.com/perevozka-avtomobilya-na-evakuatore/',
        'og_image': 'https://cargorapido.com/car-transport.jpg',
    },
    'skladskie-uslugi/index.html': {
        'title': 'Складские услуги в Тбилиси — Cargo Rapido | Хранение грузов',
        'desc': 'Собственный склад в Тбилиси: хранение, сортировка, маркировка, упаковка грузов. Гибкие тарифы, видеонаблюдение 24/7. Узнайте стоимость!',
        'canonical': 'https://cargorapido.com/skladskie-uslugi/',
        'og_image': 'https://cargorapido.com/photo-warehouse-big.jpg',
    },
    'brokerskie-uslugi/index.html': {
        'title': 'Таможенный брокер в Тбилиси — Cargo Rapido | Оформление',
        'desc': 'Таможенное оформление грузов в Грузии. Коды ТН ВЭД, расчёт пошлин, декларирование. Брокер в штате — быстро и без переплат. Консультация!',
        'canonical': 'https://cargorapido.com/brokerskie-uslugi/',
        'og_image': 'https://cargorapido.com/broker-handshake.jpg',
    },
    'poleznaya-informaciya/index.html': {
        'title': 'Блог Cargo Rapido — Полезные статьи о грузоперевозках',
        'desc': 'Статьи о грузоперевозках из Грузии: таможня, маршруты, упаковка, документы. Экспертные советы от Cargo Rapido. Читайте и оставайтесь в курсе!',
        'canonical': 'https://cargorapido.com/poleznaya-informaciya/',
        'og_image': 'https://cargorapido.com/truck.jpg',
    },
    # Blog posts
    'poleznaya-informaciya/post/aviadostavka-iz-gruzii-v-rossiyu/index.html': {
        'title': 'Авиадоставка из Грузии в Россию — сроки и стоимость',
        'desc': 'Авиадоставка грузов и личных вещей из Тбилиси в Москву и другие города России. Сроки от 1 дня. Таможенное оформление включено. Cargo Rapido.',
        'canonical': 'https://cargorapido.com/poleznaya-informaciya/post/aviadostavka-iz-gruzii-v-rossiyu/',
        'og_image': 'https://cargorapido.com/blog-avia.jpg',
    },
    'poleznaya-informaciya/post/perevozka-lichnyh-veshchej-iz-gruzii-v-rossiyu-v-usloviyah-sankcij/index.html': {
        'title': 'Перевозка личных вещей из Грузии в Россию при санкциях',
        'desc': 'Как легально перевезти личные вещи из Грузии в Россию в условиях санкций 2024-2025. Ограничения, документы, партии до 30 кг. Cargo Rapido.',
        'canonical': 'https://cargorapido.com/poleznaya-informaciya/post/perevozka-lichnyh-veshchej-iz-gruzii-v-rossiyu-v-usloviyah-sankcij/',
        'og_image': 'https://cargorapido.com/blog-sanctions.jpg',
    },
    'poleznaya-informaciya/post/perevozka-sbornyh-gruzov/index.html': {
        'title': 'Перевозка сборных грузов из Грузии в Россию и СНГ',
        'desc': 'Экономная доставка сборных грузов из Грузии. От 1 паллеты. Регулярные рейсы в Россию, Казахстан, Беларусь. Расчёт стоимости за 5 минут.',
        'canonical': 'https://cargorapido.com/poleznaya-informaciya/post/perevozka-sbornyh-gruzov/',
        'og_image': 'https://cargorapido.com/blog-sborny.jpg',
    },
    'poleznaya-informaciya/post/kak-bystro-i-bezopasno-otpravit-svoi-veshchi-iz-gruzii-v-rossiyu-strany-sng/index.html': {
        'title': 'Как быстро отправить вещи из Грузии в Россию и СНГ',
        'desc': 'Пошаговое руководство по отправке личных вещей из Грузии в Россию и страны СНГ. Документы, упаковка, сроки, стоимость. Советы от Cargo Rapido.',
        'canonical': 'https://cargorapido.com/poleznaya-informaciya/post/kak-bystro-i-bezopasno-otpravit-svoi-veshchi-iz-gruzii-v-rossiyu-strany-sng/',
        'og_image': 'https://cargorapido.com/blog-russia.jpg',
    },
    'poleznaya-informaciya/post/bystraya-i-bezopasnaya-dostavka-lichnyh-veshchej-iz-gruzii-v-evropu-i-po-miru/index.html': {
        'title': 'Доставка личных вещей из Грузии в Европу и по всему миру',
        'desc': 'Международная доставка личных вещей из Грузии в Европу и страны мира. Авиа и автомаршруты, страховка, упаковка. Cargo Rapido — с 2014 года.',
        'canonical': 'https://cargorapido.com/poleznaya-informaciya/post/bystraya-i-bezopasnaya-dostavka-lichnyh-veshchej-iz-gruzii-v-evropu-i-po-miru/',
        'og_image': 'https://cargorapido.com/blog-europe.jpg',
    },
    'poleznaya-informaciya/post/pereezd-i-perevozka-veshchej-v-turciyu/index.html': {
        'title': 'Переезд и перевозка вещей в Турцию из Грузии | Cargo Rapido',
        'desc': 'Переезжаете в Турцию? Cargo Rapido организует перевозку личных вещей из Грузии в Стамбул, Анкару, Трабзон. Сроки 2-4 дня. Узнайте стоимость!',
        'canonical': 'https://cargorapido.com/poleznaya-informaciya/post/pereezd-i-perevozka-veshchej-v-turciyu/',
        'og_image': 'https://cargorapido.com/blog-turkey.jpg',
    },
    'poleznaya-informaciya/post/kak-perevezti-lichnye-veshchi-v-gruziyu-iz-rossii/index.html': {
        'title': 'Как перевезти личные вещи в Грузию из России | Cargo Rapido',
        'desc': 'Переезжаете в Грузию из России? Cargo Rapido поможет перевезти все личные вещи. Документы, таможня, сроки и стоимость. Консультация бесплатно!',
        'canonical': 'https://cargorapido.com/poleznaya-informaciya/post/kak-perevezti-lichnye-veshchi-v-gruziyu-iz-rossii/',
        'og_image': 'https://cargorapido.com/blog-russia.jpg',
    },
}

def inject_head_meta(html, page_key):
    meta = PAGE_META.get(page_key, {})
    title = meta.get('title', '')
    desc = meta.get('desc', '')
    canonical = meta.get('canonical', '')
    og_image = meta.get('og_image', 'https://cargorapido.com/truck.jpg')
    
    # Build new head block
    new_head = f'''<!DOCTYPE html>
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
  <meta property="og:type" content="{'article' if '/post/' in page_key else 'website'}">
  <meta property="og:image" content="{og_image}">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{title}">
  <meta name="twitter:description" content="{desc}">
  <meta name="twitter:image" content="{og_image}">
  <meta name="google-site-verification" content="U4VPSdMvjvNSx8QubmIyhUwQPcS6y2hnZsIyLe6PMqM">
  <meta name="yandex-verification" content="8d6727b9489f571e">
  <link rel="icon" type="image/x-icon" href="/favicon.ico">
  <link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">
  <link rel="manifest" href="/manifest.json">
  <meta name="theme-color" content="#1a237e">
  <!-- Яндекс.Метрика -->
  <script type="text/javascript">
   (function(m,e,t,r,i,k,a){{m[i]=m[i]||function(){{(m[i].a=m[i].a||[]).push(arguments)}};
   m[i].l=1*new Date();
   for(var j=0;j<document.scripts.length;j++){{if(document.scripts[j].src===r){{return;}}}}
   k=e.createElement(t),a=e.getElementsByTagName(t)[0],k.async=1,k.src=r,a.parentNode.insertBefore(k,a)}}
   )(window, document, "script", "https://mc.yandex.ru/metrika/tag.js", "ym");
   ym(90606836, "init", {{
        clickmap:true,
        trackLinks:true,
        accurateTrackBounce:true,
        webvisor:true
   }});
  </script>
  <noscript><div><img src="https://mc.yandex.ru/watch/90606836" style="position:absolute; left:-9999px;" alt="" /></div></noscript>
  <!-- End Яндекс.Метрика -->
  <!-- Google Tag Manager -->
  <script>(function(w,d,s,l,i){{w[l]=w[l]||[];w[l].push({{'gtm.start':
  new Date().getTime(),event:'gtm.js'}});var f=d.getElementsByTagName(s)[0],
  j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
  'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
  }})(window,document,'script','dataLayer','GTM-MLNDMC75');</script>
  <!-- End Google Tag Manager -->
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
  <link rel="stylesheet" href="/style.css">'''
    
    # Replace everything from <!DOCTYPE to end of </head>
    html = re.sub(r'<!DOCTYPE html>.*?</head>', new_head, html, flags=re.DOTALL | re.IGNORECASE)
    
    # Add GTM noscript after <body>
    gtm_noscript = '''
<!-- Google Tag Manager (noscript) -->
<noscript><iframe src="https://www.googletagmanager.com/ns.html?id=GTM-MLNDMC75"
height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
<!-- End Google Tag Manager (noscript) -->'''
    
    html = html.replace('<body>', '<body>' + gtm_noscript, 1)
    
    return html

def block2_meta_tags():
    print('\n=== BLOCK 2: META tags on all pages ===')
    
    for page_key in PAGE_META.keys():
        path = os.path.join(BASE, page_key)
        if not os.path.exists(path):
            print(f'  SKIP (not found): {path}')
            continue
        html = read_file(path)
        html = inject_head_meta(html, page_key)
        write_file(path, html)
    
    git_commit('Block 2: Add/update META tags, verification, Metrika, GTM, favicon on all pages')

# ============================================================
# BLOCK 3: Schema.org
# ============================================================

def get_service_schema(name, url, desc, image):
    return f'''<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "Service",
  "name": "{name}",
  "description": "{desc}",
  "url": "{url}",
  "image": "{image}",
  "provider": {{
    "@type": "LocalBusiness",
    "name": "Cargo Rapido",
    "telephone": "+995568644615",
    "address": {{
      "@type": "PostalAddress",
      "streetAddress": "ул. Серго Закариадзе 5",
      "addressLocality": "Тбилиси",
      "addressCountry": "GE"
    }}
  }},
  "areaServed": ["Georgia", "Russia", "Kazakhstan", "Belarus", "Europe"]
}}
</script>'''

def get_breadcrumb_schema(items):
    # items: list of (name, url) tuples
    item_list = []
    for i, (name, url) in enumerate(items):
        item_list.append(f'''    {{
      "@type": "ListItem",
      "position": {i+1},
      "name": "{name}",
      "item": "{url}"
    }}''')
    return f'''<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
{",\n".join(item_list)}
  ]
}}
</script>'''

def get_article_schema(title, desc, url, image, date):
    return f'''<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "BlogPosting",
  "headline": "{title}",
  "description": "{desc}",
  "url": "{url}",
  "image": "{image}",
  "datePublished": "{date}",
  "dateModified": "{date}",
  "author": {{
    "@type": "Organization",
    "name": "Cargo Rapido"
  }},
  "publisher": {{
    "@type": "Organization",
    "name": "Cargo Rapido",
    "logo": {{
      "@type": "ImageObject",
      "url": "https://cargorapido.com/logo.jpg"
    }}
  }}
}}
</script>'''

SERVICE_PAGES = {
    'perevozka-kommercheskih-gruzov/index.html': (
        'Перевозка коммерческих грузов из Грузии',
        'https://cargorapido.com/perevozka-kommercheskih-gruzov/',
        'Надёжная перевозка коммерческих грузов из Грузии в Россию, Казахстан и Беларусь.',
        'https://cargorapido.com/commercial-cargo.jpg',
        [('Главная', 'https://cargorapido.com/'), ('Услуги', 'https://cargorapido.com/nashi-uslugi/'), ('Коммерческие грузы', 'https://cargorapido.com/perevozka-kommercheskih-gruzov/')]
    ),
    'perevozka-lichnyh-veshchej/index.html': (
        'Перевозка личных вещей из Грузии',
        'https://cargorapido.com/perevozka-lichnyh-veshchej/',
        'Перевозка личных вещей и переезды из Грузии в Россию, СНГ и Европу.',
        'https://cargorapido.com/blog-personal.jpg',
        [('Главная', 'https://cargorapido.com/'), ('Услуги', 'https://cargorapido.com/nashi-uslugi/'), ('Личные вещи', 'https://cargorapido.com/perevozka-lichnyh-veshchej/')]
    ),
    'dostavka-v-evropu/index.html': (
        'Доставка грузов в Европу из Грузии',
        'https://cargorapido.com/dostavka-v-evropu/',
        'Авиа и автодоставка из Грузии в страны Европейского союза.',
        'https://cargorapido.com/europe-delivery.jpg',
        [('Главная', 'https://cargorapido.com/'), ('Услуги', 'https://cargorapido.com/nashi-uslugi/'), ('Доставка в Европу', 'https://cargorapido.com/dostavka-v-evropu/')]
    ),
    'dostavka-posylok-pisem-i-dokumentov-po-vsemu-miru/index.html': (
        'Доставка посылок, писем и документов по всему миру',
        'https://cargorapido.com/dostavka-posylok-pisem-i-dokumentov-po-vsemu-miru/',
        'Международная доставка посылок, писем и документов из Грузии по всему миру.',
        'https://cargorapido.com/documents.jpg',
        [('Главная', 'https://cargorapido.com/'), ('Услуги', 'https://cargorapido.com/nashi-uslugi/'), ('Посылки и документы', 'https://cargorapido.com/dostavka-posylok-pisem-i-dokumentov-po-vsemu-miru/')]
    ),
    'perevozka-gruzov-pod-termorezhimom/index.html': (
        'Перевозка грузов под термо-режимом из Грузии',
        'https://cargorapido.com/perevozka-gruzov-pod-termorezhimom/',
        'Рефрижераторные перевозки и транспортировка термочувствительных грузов из Грузии.',
        'https://cargorapido.com/reefer-fleet.jpg',
        [('Главная', 'https://cargorapido.com/'), ('Услуги', 'https://cargorapido.com/nashi-uslugi/'), ('Термо-режим', 'https://cargorapido.com/perevozka-gruzov-pod-termorezhimom/')]
    ),
    'perevozka-avtomobilya-na-avtovoze/index.html': (
        'Перевозка автомобиля на автовозе из Грузии',
        'https://cargorapido.com/perevozka-avtomobilya-na-avtovoze/',
        'Безопасная транспортировка автомобилей на автовозе из Грузии в Россию и СНГ.',
        'https://cargorapido.com/car-transport.jpg',
        [('Главная', 'https://cargorapido.com/'), ('Услуги', 'https://cargorapido.com/nashi-uslugi/'), ('Перевозка автомобиля на автовозе', 'https://cargorapido.com/perevozka-avtomobilya-na-avtovoze/')]
    ),
    'perevozka-avtomobilya-na-evakuatore/index.html': (
        'Перевозка автомобиля на эвакуаторе из Грузии',
        'https://cargorapido.com/perevozka-avtomobilya-na-evakuatore/',
        'Транспортировка автомобилей на эвакуаторе из Грузии в Россию и СНГ.',
        'https://cargorapido.com/car-transport.jpg',
        [('Главная', 'https://cargorapido.com/'), ('Услуги', 'https://cargorapido.com/nashi-uslugi/'), ('Перевозка автомобиля на эвакуаторе', 'https://cargorapido.com/perevozka-avtomobilya-na-evakuatore/')]
    ),
    'skladskie-uslugi/index.html': (
        'Складские услуги в Тбилиси',
        'https://cargorapido.com/skladskie-uslugi/',
        'Складское хранение, сортировка и маркировка грузов в Тбилиси.',
        'https://cargorapido.com/photo-warehouse-big.jpg',
        [('Главная', 'https://cargorapido.com/'), ('Услуги', 'https://cargorapido.com/nashi-uslugi/'), ('Складские услуги', 'https://cargorapido.com/skladskie-uslugi/')]
    ),
    'brokerskie-uslugi/index.html': (
        'Брокерские и таможенные услуги в Тбилиси',
        'https://cargorapido.com/brokerskie-uslugi/',
        'Профессиональное таможенное оформление грузов в Грузии.',
        'https://cargorapido.com/broker-handshake.jpg',
        [('Главная', 'https://cargorapido.com/'), ('Услуги', 'https://cargorapido.com/nashi-uslugi/'), ('Брокерские услуги', 'https://cargorapido.com/brokerskie-uslugi/')]
    ),
}

ARTICLE_PAGES = {
    'poleznaya-informaciya/post/aviadostavka-iz-gruzii-v-rossiyu/index.html': {
        'title': 'Авиадоставка грузов и личных вещей в Россию с компанией Cargo Rapido',
        'desc': 'Авиадоставка грузов и личных вещей из Тбилиси в Москву и другие города России.',
        'url': 'https://cargorapido.com/poleznaya-informaciya/post/aviadostavka-iz-gruzii-v-rossiyu/',
        'image': 'https://cargorapido.com/blog-avia.jpg',
        'date': '2025-03-05',
        'breadcrumb': [('Главная', 'https://cargorapido.com/'), ('Блог', 'https://cargorapido.com/poleznaya-informaciya/'), ('Авиадоставка из Грузии в Россию', 'https://cargorapido.com/poleznaya-informaciya/post/aviadostavka-iz-gruzii-v-rossiyu/')]
    },
    'poleznaya-informaciya/post/perevozka-lichnyh-veshchej-iz-gruzii-v-rossiyu-v-usloviyah-sankcij/index.html': {
        'title': 'Перевозка личных вещей из Грузии в Россию в условиях санкций',
        'desc': 'Как легально перевезти личные вещи из Грузии в Россию в условиях санкций.',
        'url': 'https://cargorapido.com/poleznaya-informaciya/post/perevozka-lichnyh-veshchej-iz-gruzii-v-rossiyu-v-usloviyah-sankcij/',
        'image': 'https://cargorapido.com/blog-sanctions.jpg',
        'date': '2025-11-25',
        'breadcrumb': [('Главная', 'https://cargorapido.com/'), ('Блог', 'https://cargorapido.com/poleznaya-informaciya/'), ('Перевозка вещей при санкциях', 'https://cargorapido.com/poleznaya-informaciya/post/perevozka-lichnyh-veshchej-iz-gruzii-v-rossiyu-v-usloviyah-sankcij/')]
    },
    'poleznaya-informaciya/post/perevozka-sbornyh-gruzov/index.html': {
        'title': 'Перевозка сборных грузов из Грузии',
        'desc': 'Экономная доставка сборных грузов из Грузии в Россию и СНГ.',
        'url': 'https://cargorapido.com/poleznaya-informaciya/post/perevozka-sbornyh-gruzov/',
        'image': 'https://cargorapido.com/blog-sborny.jpg',
        'date': '2024-11-23',
        'breadcrumb': [('Главная', 'https://cargorapido.com/'), ('Блог', 'https://cargorapido.com/poleznaya-informaciya/'), ('Перевозка сборных грузов', 'https://cargorapido.com/poleznaya-informaciya/post/perevozka-sbornyh-gruzov/')]
    },
    'poleznaya-informaciya/post/kak-bystro-i-bezopasno-otpravit-svoi-veshchi-iz-gruzii-v-rossiyu-strany-sng/index.html': {
        'title': 'Как быстро отправить вещи из Грузии в Россию и СНГ',
        'desc': 'Пошаговое руководство по отправке личных вещей из Грузии в Россию.',
        'url': 'https://cargorapido.com/poleznaya-informaciya/post/kak-bystro-i-bezopasno-otpravit-svoi-veshchi-iz-gruzii-v-rossiyu-strany-sng/',
        'image': 'https://cargorapido.com/blog-russia.jpg',
        'date': '2024-10-18',
        'breadcrumb': [('Главная', 'https://cargorapido.com/'), ('Блог', 'https://cargorapido.com/poleznaya-informaciya/'), ('Как отправить вещи из Грузии', 'https://cargorapido.com/poleznaya-informaciya/post/kak-bystro-i-bezopasno-otpravit-svoi-veshchi-iz-gruzii-v-rossiyu-strany-sng/')]
    },
    'poleznaya-informaciya/post/bystraya-i-bezopasnaya-dostavka-lichnyh-veshchej-iz-gruzii-v-evropu-i-po-miru/index.html': {
        'title': 'Доставка личных вещей из Грузии в Европу и по всему миру',
        'desc': 'Международная доставка личных вещей из Грузии в Европу и страны мира.',
        'url': 'https://cargorapido.com/poleznaya-informaciya/post/bystraya-i-bezopasnaya-dostavka-lichnyh-veshchej-iz-gruzii-v-evropu-i-po-miru/',
        'image': 'https://cargorapido.com/blog-europe.jpg',
        'date': '2024-10-18',
        'breadcrumb': [('Главная', 'https://cargorapido.com/'), ('Блог', 'https://cargorapido.com/poleznaya-informaciya/'), ('Доставка вещей в Европу', 'https://cargorapido.com/poleznaya-informaciya/post/bystraya-i-bezopasnaya-dostavka-lichnyh-veshchej-iz-gruzii-v-evropu-i-po-miru/')]
    },
    'poleznaya-informaciya/post/pereezd-i-perevozka-veshchej-v-turciyu/index.html': {
        'title': 'Переезд и перевозка вещей в Турцию из Грузии',
        'desc': 'Cargo Rapido организует перевозку личных вещей из Грузии в Турцию.',
        'url': 'https://cargorapido.com/poleznaya-informaciya/post/pereezd-i-perevozka-veshchej-v-turciyu/',
        'image': 'https://cargorapido.com/blog-turkey.jpg',
        'date': '2023-04-22',
        'breadcrumb': [('Главная', 'https://cargorapido.com/'), ('Блог', 'https://cargorapido.com/poleznaya-informaciya/'), ('Переезд в Турцию', 'https://cargorapido.com/poleznaya-informaciya/post/pereezd-i-perevozka-veshchej-v-turciyu/')]
    },
    'poleznaya-informaciya/post/kak-perevezti-lichnye-veshchi-v-gruziyu-iz-rossii/index.html': {
        'title': 'Как перевезти личные вещи в Грузию из России | Cargo Rapido',
        'desc': 'Переезд в Грузию из России. Cargo Rapido поможет перевезти все личные вещи.',
        'url': 'https://cargorapido.com/poleznaya-informaciya/post/kak-perevezti-lichnye-veshchi-v-gruziyu-iz-rossii/',
        'image': 'https://cargorapido.com/blog-russia.jpg',
        'date': '2023-01-27',
        'breadcrumb': [('Главная', 'https://cargorapido.com/'), ('Блог', 'https://cargorapido.com/poleznaya-informaciya/'), ('Переезд в Грузию из России', 'https://cargorapido.com/poleznaya-informaciya/post/kak-perevezti-lichnye-veshchi-v-gruziyu-iz-rossii/')]
    },
}

def block3_schema():
    print('\n=== BLOCK 3: Schema.org ===')
    
    # Update index.html - MovingCompany + FAQ schema
    idx_path = os.path.join(BASE, 'index.html')
    html = read_file(idx_path)
    
    moving_company_schema = '''<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "MovingCompany",
  "name": "Cargo Rapido",
  "description": "Транспортно-логистическая компания. Грузоперевозки из Грузии в Россию, СНГ и Европу с 2014 года.",
  "url": "https://cargorapido.com",
  "telephone": "+995568644615",
  "email": "cargorapido.ge@gmail.com",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "ул. Серго Закариадзе 5",
    "addressLocality": "Тбилиси",
    "addressRegion": "Тбилиси",
    "addressCountry": "GE"
  },
  "geo": {
    "@type": "GeoCoordinates",
    "latitude": 41.6938,
    "longitude": 44.8015
  },
  "openingHoursSpecification": [
    {
      "@type": "OpeningHoursSpecification",
      "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"],
      "opens": "10:00",
      "closes": "17:00"
    }
  ],
  "image": "https://cargorapido.com/hero-main.jpg",
  "logo": "https://cargorapido.com/logo.jpg",
  "priceRange": "$$",
  "currenciesAccepted": "USD, EUR, RUB, GEL",
  "areaServed": ["Georgia", "Russia", "Kazakhstan", "Belarus", "Europe"],
  "sameAs": [
    "https://t.me/CARGORAPIDO",
    "https://facebook.com/CargoRapido"
  ],
  "hasMap": "https://yandex.ru/maps/?text=Тбилиси+ул.+Серго+Закариадзе+5"
}
</script>'''
    
    breadcrumb_main = get_breadcrumb_schema([('Главная', 'https://cargorapido.com/')])
    
    # Remove old LD+JSON schema
    html = re.sub(r'<script type="application/ld\+json">.*?</script>', '', html, flags=re.DOTALL)
    
    # Add new schemas before </head>
    schemas = moving_company_schema + '\n' + breadcrumb_main
    html = html.replace('</head>', schemas + '\n</head>', 1)
    
    write_file(idx_path, html)
    
    # Update service pages
    for page_key, (svc_name, svc_url, svc_desc, svc_image, breadcrumb) in SERVICE_PAGES.items():
        path = os.path.join(BASE, page_key)
        if not os.path.exists(path):
            print(f'  SKIP: {path}')
            continue
        html = read_file(path)
        # Remove old schemas
        html = re.sub(r'<script type="application/ld\+json">.*?</script>', '', html, flags=re.DOTALL)
        service_schema = get_service_schema(svc_name, svc_url, svc_desc, svc_image)
        bc_schema = get_breadcrumb_schema(breadcrumb)
        html = html.replace('</head>', service_schema + '\n' + bc_schema + '\n</head>', 1)
        write_file(path, html)
    
    # Update article pages
    for page_key, art in ARTICLE_PAGES.items():
        path = os.path.join(BASE, page_key)
        if not os.path.exists(path):
            print(f'  SKIP: {path}')
            continue
        html = read_file(path)
        html = re.sub(r'<script type="application/ld\+json">.*?</script>', '', html, flags=re.DOTALL)
        article_schema = get_article_schema(art['title'], art['desc'], art['url'], art['image'], art['date'])
        bc_schema = get_breadcrumb_schema(art['breadcrumb'])
        html = html.replace('</head>', article_schema + '\n' + bc_schema + '\n</head>', 1)
        write_file(path, html)
    
    # Other pages (about, kontakty, nashi-uslugi, poleznaya-informaciya)
    other_pages = {
        'about/index.html': [('Главная', 'https://cargorapido.com/'), ('О компании', 'https://cargorapido.com/about/')],
        'kontakty/index.html': [('Главная', 'https://cargorapido.com/'), ('Контакты', 'https://cargorapido.com/kontakty/')],
        'nashi-uslugi/index.html': [('Главная', 'https://cargorapido.com/'), ('Услуги', 'https://cargorapido.com/nashi-uslugi/')],
        'poleznaya-informaciya/index.html': [('Главная', 'https://cargorapido.com/'), ('Блог', 'https://cargorapido.com/poleznaya-informaciya/')],
    }
    for page_key, breadcrumb in other_pages.items():
        path = os.path.join(BASE, page_key)
        if not os.path.exists(path):
            continue
        html = read_file(path)
        html = re.sub(r'<script type="application/ld\+json">.*?</script>', '', html, flags=re.DOTALL)
        bc_schema = get_breadcrumb_schema(breadcrumb)
        html = html.replace('</head>', bc_schema + '\n</head>', 1)
        write_file(path, html)
    
    git_commit('Block 3: Schema.org - MovingCompany, Service, Article, BreadcrumbList on all pages')

# ============================================================
# BLOCK 4: Legal pages
# ============================================================

HEADER_HTML = '''<header>
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
</header>'''

FOOTER_HTML = '''<footer>
  <div class="footer-grid">
    <div class="footer-brand">
      <a href="/" class="logo"><img src="/logo.jpg" alt="Cargo Rapido" style="height:56px;width:auto;display:block;"></a>
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
        <li><a href="/otzyvy/">Отзывы</a></li>
        <li><a href="/politika-konfidencialnosti/">Политика конфиденциальности</a></li>
        <li><a href="/usloviya-okazaniya-uslug/">Условия оказания услуг</a></li>
      </ul>
    </div>
    <div class="footer-col">
      <h4>Контакты</h4>
      <ul>
        <li><a href="https://wa.me/995568644615">+995 568 644 615</a></li>
        <li><a href="https://t.me/CARGORAPIDO" target="_blank">Telegram</a></li>
        <li><a href="mailto:cargorapido.ge@gmail.com">cargorapido.ge@gmail.com</a></li>
        <li><a href="https://facebook.com/CargoRapido" target="_blank">Facebook</a></li>
      </ul>
    </div>
  </div>
  <div class="footer-bottom">
    <p>© 2024 Cargo Rapido. Все права защищены.</p>
    <p><a href="/sitemap.xml" style="color:rgba(255,255,255,0.4);text-decoration:none;">Карта сайта</a> · <a href="/politika-konfidencialnosti/" style="color:rgba(255,255,255,0.4);text-decoration:none;">Политика конфиденциальности</a> · <a href="/usloviya-okazaniya-uslug/" style="color:rgba(255,255,255,0.4);text-decoration:none;">Условия услуг</a></p>
  </div>
</footer>
<script src="/shared.js"></script>'''

def legal_page_template(title, desc, canonical, content_html):
    return f'''<!DOCTYPE html>
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
  <meta property="og:image" content="https://cargorapido.com/truck.jpg">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="robots" content="noindex, follow">
  <meta name="google-site-verification" content="U4VPSdMvjvNSx8QubmIyhUwQPcS6y2hnZsIyLe6PMqM">
  <meta name="yandex-verification" content="8d6727b9489f571e">
  <link rel="icon" type="image/x-icon" href="/favicon.ico">
  <link rel="manifest" href="/manifest.json">
  <meta name="theme-color" content="#1a237e">
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
  <script>(function(w,d,s,l,i){{w[l]=w[l]||[];w[l].push({{'gtm.start':new Date().getTime(),event:'gtm.js'}});var f=d.getElementsByTagName(s)[0],j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src='https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);}})(window,document,'script','dataLayer','GTM-MLNDMC75');</script>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
  <link rel="stylesheet" href="/style.css">
</head>
<body>
<!-- Google Tag Manager (noscript) -->
<noscript><iframe src="https://www.googletagmanager.com/ns.html?id=GTM-MLNDMC75" height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
{HEADER_HTML}

<div class="breadcrumb-nav">
  <div class="breadcrumb-nav-inner">
    <a href="/">Главная</a><span>→</span><span class="current">{title}</span>
  </div>
</div>

<div class="legal-page section">
  <div class="legal-content" style="max-width:860px;margin:0 auto;">
    {content_html}
  </div>
</div>

{FOOTER_HTML}
</body>
</html>'''

def block4_legal_pages():
    print('\n=== BLOCK 4: Legal pages ===')
    
    # Политика конфиденциальности
    privacy_content = '''<h1 style="font-size:2rem;margin-bottom:32px;">Политика конфиденциальности</h1>
<p style="color:#888;margin-bottom:32px;"><em>Последнее обновление: 26 мая 2026 г.</em></p>

<h2>1. Общие положения</h2>
<p>Настоящая Политика конфиденциальности (далее — «Политика») регулирует порядок обработки персональных данных пользователей сайта cargorapido.com (далее — «Сайт»), принадлежащего компании Cargo Rapido (далее — «Компания»). Используя Сайт, вы соглашаетесь с условиями настоящей Политики.</p>

<h2>2. Какие данные мы собираем</h2>
<p>В процессе использования Сайта мы можем собирать следующие данные:</p>
<ul>
  <li>Имя и фамилия (при заполнении формы заявки)</li>
  <li>Номер телефона (при заполнении формы заявки)</li>
  <li>Адрес электронной почты (при добровольном указании)</li>
  <li>Информация о грузе (маршрут, тип, вес — при заполнении форм)</li>
  <li>Технические данные: IP-адрес, тип браузера, страницы посещений, время на сайте</li>
  <li>Данные cookies и аналогичных технологий</li>
</ul>

<h2>3. Цели обработки данных</h2>
<p>Мы обрабатываем ваши данные в следующих целях:</p>
<ul>
  <li>Обработка и исполнение заявок на оказание транспортных услуг</li>
  <li>Связь с вами по вопросам поданных заявок</li>
  <li>Улучшение качества Сайта и услуг Компании</li>
  <li>Аналитика посещаемости (Яндекс.Метрика, Google Analytics через GTM)</li>
  <li>Соблюдение требований законодательства</li>
</ul>

<h2>4. Правовое основание обработки</h2>
<p>Обработка персональных данных осуществляется на основании:</p>
<ul>
  <li>Согласия субъекта персональных данных (ст. 6(1)(а) GDPR)</li>
  <li>Исполнения договора или преддоговорных мероприятий (ст. 6(1)(б) GDPR)</li>
  <li>Законных интересов Компании (ст. 6(1)(е) GDPR)</li>
  <li>Законодательства Грузии об информатике, связи и телекоммуникациях</li>
</ul>

<h2>5. Передача данных третьим лицам</h2>
<p>Мы не продаём и не передаём ваши персональные данные третьим лицам, за исключением:</p>
<ul>
  <li>Сервисов аналитики: Яндекс.Метрика (Россия), Google Analytics (США) — только обезличенные данные</li>
  <li>Мессенджеров Telegram и WhatsApp — при вашем добровольном переходе по нашим ссылкам</li>
  <li>Государственных органов — по законным требованиям</li>
</ul>

<h2>6. Сроки хранения данных</h2>
<p>Персональные данные хранятся не дольше, чем это необходимо для достижения целей обработки:</p>
<ul>
  <li>Данные заявок — 3 года с момента последнего взаимодействия</li>
  <li>Данные аналитики — в соответствии с политиками Яндекс.Метрика и Google</li>
  <li>Cookie-данные — не более 1 года</li>
</ul>

<h2>7. Права субъекта персональных данных</h2>
<p>Вы имеете право:</p>
<ul>
  <li>Получить доступ к своим персональным данным</li>
  <li>Потребовать исправления неточных данных</li>
  <li>Потребовать удаления данных («право на забвение»)</li>
  <li>Отозвать согласие на обработку данных в любое время</li>
  <li>Подать жалобу в надзорный орган</li>
</ul>
<p>Для реализации своих прав обратитесь по адресу: <a href="mailto:cargorapido.ge@gmail.com">cargorapido.ge@gmail.com</a></p>

<h2>8. Использование Cookie</h2>
<p>Сайт использует файлы cookie для:</p>
<ul>
  <li>Обеспечения работы сайта (технические cookie)</li>
  <li>Аналитики посещаемости (аналитические cookie — Яндекс.Метрика, GTM)</li>
</ul>
<p>Вы можете отключить cookie в настройках браузера. Обратите внимание, что отключение cookie может повлиять на работу некоторых функций Сайта.</p>

<h2>9. Контактная информация</h2>
<p>По вопросам, связанным с обработкой персональных данных, обращайтесь:</p>
<ul>
  <li>Email: <a href="mailto:cargorapido.ge@gmail.com">cargorapido.ge@gmail.com</a></li>
  <li>Telegram: <a href="https://t.me/CARGORAPIDO" target="_blank">@CARGORAPIDO</a></li>
  <li>Адрес: Грузия, г. Тбилиси, ул. Серго Закариадзе 5</li>
</ul>

<h2>10. Изменения в Политике</h2>
<p>Компания оставляет за собой право вносить изменения в настоящую Политику. При существенных изменениях мы уведомим пользователей через Сайт. Актуальная версия Политики всегда доступна по адресу <a href="/politika-konfidencialnosti/">cargorapido.com/politika-konfidencialnosti/</a>. Дата последнего обновления указана в начале документа.</p>

<div style="margin-top:40px;padding:24px;background:#f8f9ff;border-radius:12px;">
  <p><strong>Cargo Rapido</strong> · Грузия, г. Тбилиси, ул. Серго Закариадзе 5</p>
  <p>Email: <a href="mailto:cargorapido.ge@gmail.com">cargorapido.ge@gmail.com</a> · Telegram: <a href="https://t.me/CARGORAPIDO">@CARGORAPIDO</a></p>
</div>'''
    
    write_file(
        os.path.join(BASE, 'politika-konfidencialnosti/index.html'),
        legal_page_template(
            'Политика конфиденциальности — Cargo Rapido',
            'Политика конфиденциальности сайта Cargo Rapido. Порядок обработки персональных данных.',
            'https://cargorapido.com/politika-konfidencialnosti/',
            privacy_content
        )
    )
    
    # Условия оказания услуг
    terms_content = '''<h1 style="font-size:2rem;margin-bottom:32px;">Условия оказания услуг (Публичная оферта)</h1>
<p style="color:#888;margin-bottom:32px;"><em>Последнее обновление: 26 мая 2026 г.</em></p>

<p>Настоящий документ является публичной офертой компании Cargo Rapido (далее — «Исполнитель») на оказание транспортно-логистических услуг.</p>

<h2>1. Стороны и предмет договора</h2>
<p>Исполнитель: Cargo Rapido, г. Тбилиси, ул. Серго Закариадзе 5, Грузия. Заказчик: любое физическое или юридическое лицо, принявшее условия настоящей оферты. Предмет: оказание транспортно-логистических услуг по перевозке грузов, таможенному оформлению, складскому хранению.</p>

<h2>2. Порядок принятия оферты</h2>
<p>Оферта считается принятой (акцептованной) с момента отправки заявки через сайт, мессенджер (Telegram, WhatsApp) или иным способом и оплаты аванса. Акцепт означает полное согласие со всеми условиями настоящей оферты.</p>

<h2>3. Услуги и стоимость</h2>
<p>Исполнитель оказывает следующие услуги:</p>
<ul>
  <li>Перевозка коммерческих грузов (паллеты, сборные грузы, FTL)</li>
  <li>Перевозка личных вещей и переезды</li>
  <li>Доставка в Европу, СНГ, по всему миру</li>
  <li>Рефрижераторные перевозки</li>
  <li>Перевозка автомобилей</li>
  <li>Складские услуги</li>
  <li>Таможенное оформление</li>
</ul>
<p>Стоимость услуг определяется индивидуально для каждой заявки и фиксируется в счёте или накладной.</p>

<h2>4. Права и обязанности Исполнителя</h2>
<p>Исполнитель обязуется: принять груз к перевозке, обеспечить сохранность груза, уведомить Заказчика о статусе доставки, оформить необходимые документы. Исполнитель вправе привлекать субподрядчиков для выполнения перевозки.</p>

<h2>5. Права и обязанности Заказчика</h2>
<p>Заказчик обязуется: предоставить достоверные сведения о грузе, обеспечить надлежащую упаковку (при самостоятельной упаковке), своевременно оплатить услуги, не включать в груз запрещённые к перевозке предметы.</p>

<h2>6. Ответственность сторон</h2>
<p>Исполнитель несёт ответственность за утрату или повреждение груза в размере объявленной стоимости или рыночной стоимости, но не более суммы, указанной в накладной. Исполнитель не несёт ответственности за задержки, вызванные форс-мажорными обстоятельствами, действиями таможенных органов или третьих лиц.</p>

<h2>7. Страхование груза</h2>
<p>Страхование груза осуществляется по желанию Заказчика за дополнительную плату. При отсутствии страховки ответственность Исполнителя ограничена условиями п. 6 настоящей оферты.</p>

<h2>8. Порядок расчётов</h2>
<p>Оплата производится в порядке, согласованном с менеджером: полная предоплата или оплата при получении (только для постоянных клиентов). Валюта расчётов: USD, EUR, RUB, GEL по курсу на дату оплаты.</p>

<h2>9. Претензии и споры</h2>
<p>Претензии по качеству услуг принимаются в течение 7 дней с момента получения груза. Споры решаются путём переговоров. При невозможности урегулирования — в судебном порядке по законодательству Грузии.</p>

<h2>10. Прочие условия</h2>
<p>Настоящая оферта действует бессрочно до момента её отзыва Исполнителем. Исполнитель вправе изменять условия оферты, уведомив об этом на Сайте. По всем вопросам: <a href="mailto:cargorapido.ge@gmail.com">cargorapido.ge@gmail.com</a></p>

<div style="margin-top:40px;padding:24px;background:#f8f9ff;border-radius:12px;">
  <p><strong>Cargo Rapido</strong> · Грузия, г. Тбилиси, ул. Серго Закариадзе 5</p>
  <p>Email: <a href="mailto:cargorapido.ge@gmail.com">cargorapido.ge@gmail.com</a> · Telegram: <a href="https://t.me/CARGORAPIDO">@CARGORAPIDO</a></p>
</div>'''
    
    write_file(
        os.path.join(BASE, 'usloviya-okazaniya-uslug/index.html'),
        legal_page_template(
            'Условия оказания услуг — Cargo Rapido',
            'Публичная оферта Cargo Rapido. Условия оказания транспортно-логистических услуг.',
            'https://cargorapido.com/usloviya-okazaniya-uslug/',
            terms_content
        )
    )
    
    # Согласие на обработку данных
    consent_content = '''<h1 style="font-size:2rem;margin-bottom:32px;">Согласие на обработку персональных данных</h1>

<p>Настоящим я, нижеподписавшийся субъект персональных данных, даю согласие компании <strong>Cargo Rapido</strong> (г. Тбилиси, ул. Серго Закариадзе 5, Грузия) на обработку следующих персональных данных:</p>

<ul>
  <li>Имя и фамилия</li>
  <li>Номер телефона</li>
  <li>Адрес электронной почты</li>
  <li>Информация о грузе и маршруте перевозки</li>
</ul>

<h2>Цели обработки</h2>
<ul>
  <li>Обработка заявок на оказание транспортных и логистических услуг</li>
  <li>Связь с клиентом по вопросам оказания услуг</li>
  <li>Оказание услуг согласно публичной оферте</li>
</ul>

<h2>Способы обработки</h2>
<p>Сбор, запись, систематизация, накопление, хранение, уточнение, использование, передача, обезличивание, блокирование, удаление и уничтожение персональных данных.</p>

<h2>Срок действия согласия</h2>
<p>Настоящее согласие действует до его отзыва. Для отзыва согласия направьте соответствующий запрос на адрес <a href="mailto:cargorapido.ge@gmail.com">cargorapido.ge@gmail.com</a>.</p>

<h2>Порядок отзыва согласия</h2>
<p>Вы вправе отозвать согласие в любое время, направив соответствующее уведомление по электронной почте: <a href="mailto:cargorapido.ge@gmail.com">cargorapido.ge@gmail.com</a></p>
<p>После отзыва согласия Cargo Rapido прекратит обработку персональных данных в течение 30 дней.</p>

<p style="margin-top:32px;">Ознакомившись с Политикой конфиденциальности (<a href="/politika-konfidencialnosti/">cargorapido.com/politika-konfidencialnosti/</a>), я подтверждаю своё согласие на обработку персональных данных в указанных целях.</p>

<div style="margin-top:40px;padding:24px;background:#f8f9ff;border-radius:12px;">
  <p><strong>Cargo Rapido</strong> · Грузия, г. Тбилиси, ул. Серго Закариадзе 5</p>
  <p>Email: <a href="mailto:cargorapido.ge@gmail.com">cargorapido.ge@gmail.com</a></p>
</div>'''
    
    write_file(
        os.path.join(BASE, 'soglasie-na-obrabotku/index.html'),
        legal_page_template(
            'Согласие на обработку персональных данных — Cargo Rapido',
            'Текст согласия на обработку персональных данных Cargo Rapido.',
            'https://cargorapido.com/soglasie-na-obrabotku/',
            consent_content
        )
    )
    
    git_commit('Block 4: Create legal pages - privacy policy, terms, consent')

# ============================================================
# BLOCK 5: Cookie banner + WhatsApp/Telegram widget in shared.js
# ============================================================

def block5_cookie_and_widget():
    print('\n=== BLOCK 5+8: Cookie banner + WhatsApp/Telegram widget in shared.js ===')
    
    shared_js = '''// Cargo Rapido — Shared JS
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

// ===== WHATSAPP + TELEGRAM WIDGET =====
function initWhatsAppWidget() {
  const widget = document.createElement('div');
  widget.id = 'wa-widget';
  widget.innerHTML = `
    <div class="wa-menu" id="wa-menu">
      <a href="https://wa.me/995568644615" target="_blank" class="wa-menu-item wa-item">
        <svg width="22" height="22" viewBox="0 0 24 24" fill="currentColor"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413Z"/></svg>
        WhatsApp
      </a>
      <a href="https://t.me/CARGORAPIDO" target="_blank" class="wa-menu-item tg-item">
        <svg width="22" height="22" viewBox="0 0 24 24" fill="currentColor"><path d="M11.944 0A12 12 0 0 0 0 12a12 12 0 0 0 12 12 12 12 0 0 0 12-12A12 12 0 0 0 12 0a12 12 0 0 0-.056 0zm4.962 7.224c.1-.002.321.023.465.14a.506.506 0 0 1 .171.325c.016.093.036.306.02.472-.18 1.898-.962 6.502-1.36 8.627-.168.9-.499 1.201-.82 1.23-.696.065-1.225-.46-1.9-.902-1.056-.693-1.653-1.124-2.678-1.8-1.185-.78-.417-1.21.258-1.91.177-.184 3.247-2.977 3.307-3.23.007-.032.014-.15-.056-.212s-.174-.041-.249-.024c-.106.024-1.793 1.14-5.061 3.345-.48.33-.913.49-1.302.48-.428-.008-1.252-.241-1.865-.44-.752-.245-1.349-.374-1.297-.789.027-.216.325-.437.893-.663 3.498-1.524 5.83-2.529 6.998-3.014 3.332-1.386 4.025-1.627 4.476-1.635z"/></svg>
        Telegram
      </a>
    </div>
    <button class="wa-trigger" id="wa-trigger" onclick="toggleWaMenu()" aria-label="Написать нам">
      <svg width="28" height="28" viewBox="0 0 24 24" fill="white"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413Z"/></svg>
    </button>
    <div class="wa-bubble" id="wa-bubble">
      <div class="wa-bubble-avatar">👩</div>
      <div class="wa-bubble-text">Здравствуйте! Готова рассчитать стоимость. Напишите нам 😊<span style="display:block;font-size:12px;color:#888;margin-top:4px;">— Наталья</span></div>
      <button class="wa-bubble-close" onclick="closeBubble()">×</button>
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

function toggleWaMenu() {
  const menu = document.getElementById('wa-menu');
  const trigger = document.getElementById('wa-trigger');
  if (menu) {
    menu.classList.toggle('open');
    trigger.classList.toggle('active');
  }
  // Close bubble when menu opened
  const bubble = document.getElementById('wa-bubble');
  if (bubble) bubble.classList.remove('visible');
}

function closeBubble() {
  const bubble = document.getElementById('wa-bubble');
  if (bubble) bubble.classList.remove('visible');
}

// Close menu on outside click
document.addEventListener('click', function(e) {
  const widget = document.getElementById('wa-widget');
  if (widget && !widget.contains(e.target)) {
    const menu = document.getElementById('wa-menu');
    const trigger = document.getElementById('wa-trigger');
    if (menu) menu.classList.remove('open');
    if (trigger) trigger.classList.remove('active');
  }
});
'''
    
    write_file(os.path.join(BASE, 'shared.js'), shared_js)
    git_commit('Block 5+8: Cookie banner + WhatsApp/Telegram floating widget in shared.js')

# ============================================================
# BLOCK 6: Form component
# ============================================================

def block6_form():
    print('\n=== BLOCK 6: Form component ===')
    
    form_js = '''// Cargo Rapido — Form Component
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
      let val = e.target.value.replace(/\\D/g, '');
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
''';
    
    write_file(os.path.join(BASE, 'form-component.js'), form_js)
    
    # Form HTML block to insert into pages
    FORM_SECTION = '''
<!-- ЗАЯВКА -->
<section class="section section-light" id="form-section">
  <div class="sec-tag">Быстрая заявка</div>
  <div class="sec-h2">Оставьте заявку — ответим за 15 минут</div>
  <div id="main-order-form" data-cr-form data-cr-form-title=""></div>
</section>
<script src="/form-component.js"></script>
'''
    
    # Add form to index.html - before <!-- BLOG PREVIEW -->
    idx_path = os.path.join(BASE, 'index.html')
    html = read_file(idx_path)
    if 'main-order-form' not in html:
        html = html.replace('<!-- BLOG PREVIEW -->', FORM_SECTION + '\n<!-- BLOG PREVIEW -->')
        write_file(idx_path, html)
    
    # Add form to kontakty/index.html - after contacts section, before footer
    kont_path = os.path.join(BASE, 'kontakty/index.html')
    html = read_file(kont_path)
    if 'main-order-form' not in html:
        KONT_FORM = '''
<!-- ЗАЯВКА -->
<section class="section" id="form-section">
  <div class="sec-tag">Онлайн-заявка</div>
  <div class="sec-h2">Отправьте заявку онлайн</div>
  <div id="main-order-form" data-cr-form data-cr-form-title=""></div>
</section>
<script src="/form-component.js"></script>
'''
        html = html.replace('<footer>', KONT_FORM + '\n<footer>', 1)
        write_file(kont_path, html)
    
    # Add form to all 9 service pages - before footer
    SVC_FORM = '''
<!-- ЗАЯВКА -->
<section class="section section-light" id="form-section">
  <div class="sec-tag">Оставить заявку</div>
  <div class="sec-h2">Получите расчёт стоимости за 5 минут</div>
  <div id="main-order-form" data-cr-form data-cr-form-title=""></div>
</section>
<script src="/form-component.js"></script>
'''
    for page_key in SERVICE_PAGES.keys():
        path = os.path.join(BASE, page_key)
        if not os.path.exists(path):
            continue
        html = read_file(path)
        if 'main-order-form' not in html:
            html = html.replace('<footer>', SVC_FORM + '\n<footer>', 1)
            write_file(path, html)
    
    git_commit('Block 6: Add form-component.js (frontend stub) and forms on index, kontakty, service pages')

# ============================================================
# BLOCK 7: FAQ accordion on homepage
# ============================================================

def block7_faq():
    print('\n=== BLOCK 7: FAQ accordion on homepage ===')
    
    FAQ_SECTION = '''
<!-- FAQ -->
<section class="section section-light" id="faq">
  <div class="sec-tag">Вопросы и ответы</div>
  <div class="sec-h2">Часто задаваемые вопросы</div>
  <div class="faq-list">
    <div class="faq-item">
      <button class="faq-q" onclick="toggleFaq(this)">
        Как рассчитать стоимость доставки из Грузии в Россию?
        <span class="faq-icon">+</span>
      </button>
      <div class="faq-a">
        <p>Стоимость рассчитывается индивидуально в зависимости от маршрута, типа груза, веса и объёма. Напишите нам в Telegram или WhatsApp — менеджер рассчитает стоимость за 5 минут. Базовые тарифы: от 1.5 $/кг на направлении Грузия–Россия.</p>
      </div>
    </div>
    <div class="faq-item">
      <button class="faq-q" onclick="toggleFaq(this)">
        Какие документы нужны для перевозки личных вещей?
        <span class="faq-icon">+</span>
      </button>
      <div class="faq-a">
        <p>Для перевозки личных вещей необходим список имущества (инвентаризационная опись) и копия паспорта. При перевозе в Россию важно соблюдать нормы беспошлинного ввоза. Наш таможенный брокер подготовит все документы и проконсультирует по ограничениям.</p>
      </div>
    </div>
    <div class="faq-item">
      <button class="faq-q" onclick="toggleFaq(this)">
        Сколько времени занимает доставка Тбилиси–Москва?
        <span class="faq-icon">+</span>
      </button>
      <div class="faq-a">
        <p>Срок доставки автотранспортом составляет 3–7 дней в зависимости от типа отправки (сборный груз или полная фура). Авиадоставка занимает 1–3 дня. Рейсы Тбилиси–Москва выполняются регулярно — 2 раза в неделю.</p>
      </div>
    </div>
    <div class="faq-item">
      <button class="faq-q" onclick="toggleFaq(this)">
        Можно ли перевезти груз из Грузии в Россию в условиях санкций?
        <span class="faq-icon">+</span>
      </button>
      <div class="faq-a">
        <p>Да, перевозка личных вещей и ряда коммерческих грузов продолжается легально. Существуют ограничения по перечню товаров двойного назначения. Мы отслеживаем все изменения в санкционном законодательстве и всегда проконсультируем по актуальным правилам.</p>
      </div>
    </div>
    <div class="faq-item">
      <button class="faq-q" onclick="toggleFaq(this)">
        Застрахован ли груз при перевозке?
        <span class="faq-icon">+</span>
      </button>
      <div class="faq-a">
        <p>Да, мы предлагаем страхование груза. Вы можете застраховать груз на объявленную стоимость за дополнительную плату. При наличии страховки в случае повреждения или утраты груза вы получите полную компенсацию.</p>
      </div>
    </div>
    <div class="faq-item">
      <button class="faq-q" onclick="toggleFaq(this)">
        Как отследить местонахождение груза?
        <span class="faq-icon">+</span>
      </button>
      <div class="faq-a">
        <p>После отправки груза вы получаете уникальный трек-номер и ссылку на GPS-трекинг. Вы можете в режиме реального времени следить за местонахождением транспортного средства. Также менеджер регулярно обновляет вас о статусе доставки в мессенджере.</p>
      </div>
    </div>
    <div class="faq-item">
      <button class="faq-q" onclick="toggleFaq(this)">
        Оказываете ли вы услуги по упаковке груза?
        <span class="faq-icon">+</span>
      </button>
      <div class="faq-a">
        <p>Да, мы оказываем полный комплекс услуг по упаковке: стрейч-плёнка, картонные коробки, деревянные обрешётки для хрупких грузов. Наши специалисты правильно упакуют даже самые хрупкие и нестандартные предметы.</p>
      </div>
    </div>
    <div class="faq-item">
      <button class="faq-q" onclick="toggleFaq(this)">
        Доставляете ли вы «от двери до двери»?
        <span class="faq-icon">+</span>
      </button>
      <div class="faq-a">
        <p>Да, мы осуществляем перевозки по схеме «от двери до двери». Курьер заберёт груз по вашему адресу в Тбилиси и доставит по указанному адресу в городе назначения. Это наиболее удобный вариант для переездов и личных вещей.</p>
      </div>
    </div>
    <div class="faq-item">
      <button class="faq-q" onclick="toggleFaq(this)">
        Как перевезти автомобиль из Грузии в Россию?
        <span class="faq-icon">+</span>
      </button>
      <div class="faq-a">
        <p>Для перевозки автомобиля мы используем автовоз (для исправных авто) или эвакуатор (для неисправных). Необходимы ПТС, СТС и доверенность если вы не владелец. Наш брокер поможет с таможенным оформлением. Стоимость рассчитывается индивидуально.</p>
      </div>
    </div>
    <div class="faq-item">
      <button class="faq-q" onclick="toggleFaq(this)">
        Какой минимальный вес груза для отправки?
        <span class="faq-icon">+</span>
      </button>
      <div class="faq-a">
        <p>Минимального веса нет — мы принимаем к перевозке грузы от 1 кг. Для небольших отправлений (посылки, документы) мы используем сборные рейсы, что позволяет сохранить конкурентоспособную цену даже для маленьких пакетов.</p>
      </div>
    </div>
    <div class="faq-item">
      <button class="faq-q" onclick="toggleFaq(this)">
        Работаете ли вы с юридическими лицами?
        <span class="faq-icon">+</span>
      </button>
      <div class="faq-a">
        <p>Да, мы активно работаем с юридическими лицами: предоставляем полный пакет закрывающих документов (договор, счёт, накладные, акт выполненных работ). Возможна работа по долгосрочным договорам с индивидуальными тарифами для регулярных отправок.</p>
      </div>
    </div>
    <div class="faq-item">
      <button class="faq-q" onclick="toggleFaq(this)">
        Какие грузы вы НЕ перевозите?
        <span class="faq-icon">+</span>
      </button>
      <div class="faq-a">
        <p>Мы не перевозим предметы, запрещённые законодательством: наркотики, оружие, взрывчатые вещества, радиоактивные материалы        <span class="faq-icon">+</span>
      </button>
      <div class="faq-a">
        <p>Мы не перевозим предметы, запрещённые законодательством: наркотики, оружие, взрывчатые вещества, радиоактивные материалы, а также санкционные товары. По вопросам допустимости груза проконсультирует наш менеджер.</p>
      </div>
    </div>
  </div>
</section>
<script>
function toggleFaq(btn) {
  var item = btn.parentElement;
  var isOpen = item.classList.contains('open');
  document.querySelectorAll('.faq-item.open').forEach(function(i) { i.classList.remove('open'); });
  if (!isOpen) item.classList.add('open');
}
</script>
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {"@type":"Question","name":"Как рассчитать стоимость?","acceptedAnswer":{"@type":"Answer","text":"Напишите нам в Telegram или WhatsApp — рассчитаем за 5 минут."}},
    {"@type":"Question","name":"Сколько времени доставка Тбилиси–Москва?","acceptedAnswer":{"@type":"Answer","text":"3–7 дней автотранспортом, 1–3 дня авиа."}}
  ]
}
</script>
'''
    
    idx_path = os.path.join(BASE, 'index.html')
    html = read_file(idx_path)
    if 'faq-list' not in html:
        # Insert before CTA
        if '<!-- CTA -->' in html:
            html = html.replace('<!-- CTA -->', FAQ_SECTION + '\n<!-- CTA -->')
        else:
            html = html.replace('<section class="cta-banner">', FAQ_SECTION + '\n<section class="cta-banner">', 1)
        write_file(idx_path, html)
    
    git_commit('Block 7: FAQ accordion with 12 questions + FAQPage Schema.org on homepage')


# ============================================================
# MAIN
# ============================================================

if __name__ == '__main__':
    print('=== Starting build.py ===')
    block1_sitemap_robots()
    block2_meta_tags()
    block3_schema()
    block4_legal_pages()
    block5_cookie_and_widget()
    block6_form()
    block7_faq()
    print('\n=== build.py complete ===')
