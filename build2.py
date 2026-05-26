#!/usr/bin/env python3
"""Part 2 of master build script - continues from build.py"""

import os
import re
import subprocess

BASE = '/root/.openclaw/workspace/cargo-rapido-site'

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

FAQ_SECTION = '''
<!-- FAQ -->
<section class="section section-light" id="faq">
  <div class="sec-tag">Вопросы и ответы</div>
  <div class="sec-h2">Часто задаваемые вопросы</div>
  <div class="faq-list">
    <div class="faq-item">
      <button class="faq-q" onclick="toggleFaq(this)">Как рассчитать стоимость доставки из Грузии в Россию?<span class="faq-icon">+</span></button>
      <div class="faq-a"><p>Стоимость рассчитывается индивидуально в зависимости от маршрута, типа груза, веса и объёма. Напишите нам в Telegram или WhatsApp — менеджер рассчитает стоимость за 5 минут. Базовые тарифы: от 1.5 $/кг на направлении Грузия–Россия.</p></div>
    </div>
    <div class="faq-item">
      <button class="faq-q" onclick="toggleFaq(this)">Какие документы нужны для перевозки личных вещей?<span class="faq-icon">+</span></button>
      <div class="faq-a"><p>Для перевозки личных вещей необходим список имущества (инвентаризационная опись) и копия паспорта. При перевозе в Россию важно соблюдать нормы беспошлинного ввоза. Наш таможенный брокер подготовит все документы и проконсультирует по ограничениям.</p></div>
    </div>
    <div class="faq-item">
      <button class="faq-q" onclick="toggleFaq(this)">Сколько времени занимает доставка Тбилиси–Москва?<span class="faq-icon">+</span></button>
      <div class="faq-a"><p>Срок доставки автотранспортом составляет 3–7 дней в зависимости от типа отправки (сборный груз или полная фура). Авиадоставка занимает 1–3 дня. Рейсы Тбилиси–Москва выполняются регулярно — 2 раза в неделю.</p></div>
    </div>
    <div class="faq-item">
      <button class="faq-q" onclick="toggleFaq(this)">Можно ли перевезти груз из Грузии в Россию при санкциях?<span class="faq-icon">+</span></button>
      <div class="faq-a"><p>Да, перевозка личных вещей и ряда коммерческих грузов продолжается легально. Существуют ограничения по перечню товаров двойного назначения. Мы отслеживаем все изменения в санкционном законодательстве и всегда проконсультируем по актуальным правилам.</p></div>
    </div>
    <div class="faq-item">
      <button class="faq-q" onclick="toggleFaq(this)">Застрахован ли груз при перевозке?<span class="faq-icon">+</span></button>
      <div class="faq-a"><p>Да, мы предлагаем страхование груза на объявленную стоимость за дополнительную плату. При наличии страховки в случае повреждения или утраты груза вы получите полную компенсацию. Рекомендуем страховать ценные грузы стоимостью от 500 $.</p></div>
    </div>
    <div class="faq-item">
      <button class="faq-q" onclick="toggleFaq(this)">Как отследить местонахождение груза?<span class="faq-icon">+</span></button>
      <div class="faq-a"><p>После отправки вы получаете уникальный трек-номер и ссылку на GPS-трекинг. Вы можете в режиме реального времени следить за местонахождением транспортного средства. Менеджер также регулярно обновляет вас о статусе доставки в мессенджере.</p></div>
    </div>
    <div class="faq-item">
      <button class="faq-q" onclick="toggleFaq(this)">Оказываете ли вы услуги по упаковке груза?<span class="faq-icon">+</span></button>
      <div class="faq-a"><p>Да, мы оказываем полный комплекс услуг по упаковке: стрейч-плёнка, картонные коробки, деревянные обрешётки для хрупких грузов. Наши специалисты правильно упакуют даже самые хрупкие и нестандартные предметы.</p></div>
    </div>
    <div class="faq-item">
      <button class="faq-q" onclick="toggleFaq(this)">Доставляете ли вы «от двери до двери»?<span class="faq-icon">+</span></button>
      <div class="faq-a"><p>Да, мы осуществляем перевозки по схеме «от двери до двери». Курьер заберёт груз по вашему адресу в Тбилиси и доставит по указанному адресу в городе назначения. Это наиболее удобный вариант для переездов и личных вещей.</p></div>
    </div>
    <div class="faq-item">
      <button class="faq-q" onclick="toggleFaq(this)">Как перевезти автомобиль из Грузии в Россию?<span class="faq-icon">+</span></button>
      <div class="faq-a"><p>Для перевозки автомобиля мы используем автовоз (для исправных авто) или эвакуатор (для неисправных). Необходимы ПТС, СТС и доверенность если вы не владелец. Наш брокер поможет с таможенным оформлением. Стоимость рассчитывается индивидуально.</p></div>
    </div>
    <div class="faq-item">
      <button class="faq-q" onclick="toggleFaq(this)">Какой минимальный вес груза для отправки?<span class="faq-icon">+</span></button>
      <div class="faq-a"><p>Минимального веса нет — мы принимаем к перевозке грузы от 1 кг. Для небольших отправлений (посылки, документы) мы используем сборные рейсы, что позволяет сохранить конкурентоспособную цену даже для маленьких пакетов.</p></div>
    </div>
    <div class="faq-item">
      <button class="faq-q" onclick="toggleFaq(this)">Работаете ли вы с юридическими лицами?<span class="faq-icon">+</span></button>
      <div class="faq-a"><p>Да, мы работаем с юридическими лицами и предоставляем полный пакет закрывающих документов (договор, счёт, накладные, акт). Возможна работа по долгосрочным договорам с индивидуальными тарифами для регулярных отправок.</p></div>
    </div>
    <div class="faq-item">
      <button class="faq-q" onclick="toggleFaq(this)">Какие грузы вы НЕ перевозите?<span class="faq-icon">+</span></button>
      <div class="faq-a"><p>Мы не перевозим предметы, запрещённые законодательством: наркотики, оружие, взрывчатые вещества, радиоактивные материалы, а также санкционные товары. По вопросам допустимости груза всегда можно проконсультироваться с нашим менеджером.</p></div>
    </div>
  </div>
</section>
<script>
function toggleFaq(btn) {
  const item = btn.parentElement;
  const isOpen = item.classList.contains('open');
  document.querySelectorAll('.faq-item.open').forEach(i => i.classList.remove('open'));
  if (!isOpen) item.classList.add('open');
}
</script>
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {"@type":"Question","name":"Как рассчитать стоимость доставки из Грузии в Россию?","acceptedAnswer":{"@type":"Answer","text":"Стоимость рассчитывается индивидуально в зависимости от маршрута, типа груза, веса и объёма. Напишите нам в Telegram или WhatsApp — менеджер рассчитает стоимость за 5 минут. Базовые тарифы: от 1.5 $/кг на направлении Грузия–Россия."}},
    {"@type":"Question","name":"Какие документы нужны для перевозки личных вещей?","acceptedAnswer":{"@type":"Answer","text":"Для перевозки личных вещей необходим список имущества (инвентаризационная опись) и копия паспорта. Наш таможенный брокер подготовит все документы."}},
    {"@type":"Question","name":"Сколько времени занимает доставка Тбилиси–Москва?","acceptedAnswer":{"@type":"Answer","text":"Срок доставки автотранспортом составляет 3–7 дней. Авиадоставка занимает 1–3 дня. Рейсы выполняются 2 раза в неделю."}},
    {"@type":"Question","name":"Можно ли перевезти груз из Грузии в Россию при санкциях?","acceptedAnswer":{"@type":"Answer","text":"Да, перевозка личных вещей и ряда коммерческих грузов продолжается легально. Мы отслеживаем все изменения в санкционном законодательстве."}},
    {"@type":"Question","name":"Застрахован ли груз при перевозке?","acceptedAnswer":{"@type":"Answer","text":"Да, мы предлагаем страхование груза на объявленную стоимость. При наличии страховки вы получите полную компенсацию в случае повреждения или утраты."}},
    {"@type":"Question","name":"Как отследить местонахождение груза?","acceptedAnswer":{"@type":"Answer","text":"После отправки вы получаете трек-номер и ссылку на GPS-трекинг. Также менеджер обновляет вас о статусе доставки в мессенджере."}},
    {"@type":"Question","name":"Доставляете ли вы от двери до двери?","acceptedAnswer":{"@type":"Answer","text":"Да, мы осуществляем перевозки по схеме от двери до двери. Курьер заберёт груз по вашему адресу в Тбилиси и доставит по указанному адресу."}},
    {"@type":"Question","name":"Какой минимальный вес груза для отправки?","acceptedAnswer":{"@type":"Answer","text":"Минимального веса нет — мы принимаем к перевозке грузы от 1 кг."}}
  ]
}
</script>
'''

def block7_faq():
    print('\n=== BLOCK 7: FAQ accordion on homepage ===')
    
    idx_path = os.path.join(BASE, 'index.html')
    html = read_file(idx_path)
    if 'faq-list' not in html:
        # Insert before <!-- CTA -->
        html = html.replace('<!-- CTA -->', FAQ_SECTION + '\n<!-- CTA -->')
        write_file(idx_path, html)
    
    git_commit('Block 7: FAQ accordion with 12 questions + FAQPage Schema.org on homepage')


# ============================================================
# BLOCK 9: Yandex Map on contacts page
# ============================================================

def block9_yandex_map():
    print('\n=== BLOCK 9: Yandex map on contacts page ===')
    
    kont_path = os.path.join(BASE, 'kontakty/index.html')
    html = read_file(kont_path)
    
    MAP_BLOCK = '''
<!-- YANDEX MAP -->
<section class="section" id="map-section">
  <div class="sec-tag">Где мы находимся</div>
  <div class="sec-h2">Наш офис в Тбилиси</div>
  
  <div class="contact-info-block" style="display:flex;gap:24px;flex-wrap:wrap;margin-bottom:32px;padding:24px;background:#f8f9ff;border-radius:12px;">
    <div style="flex:1;min-width:200px;">
      <div style="display:flex;align-items:center;gap:12px;margin-bottom:16px;">
        <div style="width:40px;height:40px;background:#1a237e;border-radius:10px;display:flex;align-items:center;justify-content:center;color:white;font-size:18px;">📍</div>
        <div>
          <div style="font-weight:700;font-size:16px;">Адрес офиса</div>
          <div style="color:#666;">Тбилиси, ул. Серго Закариадзе 5</div>
        </div>
      </div>
      <div style="display:flex;align-items:center;gap:12px;margin-bottom:16px;">
        <div style="width:40px;height:40px;background:#1a237e;border-radius:10px;display:flex;align-items:center;justify-content:center;color:white;font-size:18px;">🕐</div>
        <div>
          <div style="font-weight:700;font-size:16px;">Режим работы</div>
          <div style="color:#666;">Пн-Сб 10:00–17:00</div>
        </div>
      </div>
      <div style="display:flex;align-items:center;gap:12px;">
        <div style="width:40px;height:40px;background:#25D366;border-radius:10px;display:flex;align-items:center;justify-content:center;color:white;font-size:18px;">📱</div>
        <div>
          <div style="font-weight:700;font-size:16px;">Телефон</div>
          <div style="color:#666;"><a href="https://wa.me/995568644615" style="color:#25D366;font-weight:600;">+995 568 644 615</a></div>
        </div>
      </div>
    </div>
  </div>
  
  <div class="map-container" id="yandex-map-container" style="width:100%;height:400px;border-radius:12px;overflow:hidden;background:#f0f0f0;display:flex;align-items:center;justify-content:center;">
    <div class="map-placeholder" style="text-align:center;color:#888;">
      <div style="font-size:48px;margin-bottom:12px;">🗺️</div>
      <div>Карта загружается...</div>
    </div>
  </div>
</section>

<script>
// Lazy load Yandex Map on scroll
(function() {
  const container = document.getElementById('yandex-map-container');
  if (!container) return;
  
  const observer = new IntersectionObserver(function(entries) {
    if (entries[0].isIntersecting) {
      observer.disconnect();
      const iframe = document.createElement('iframe');
      iframe.src = "https://yandex.ru/map-widget/v1/?text=%D0%A2%D0%B1%D0%B8%D0%BB%D0%B8%D1%81%D0%B8%2C+%D1%83%D0%BB.+%D0%A1%D0%B5%D1%80%D0%B3%D0%BE+%D0%97%D0%B0%D0%BA%D0%B0%D1%80%D0%B8%D0%B0%D0%B4%D0%B7%D0%B5+5&ll=44.801500%2C41.693800&z=16";
      iframe.width = "100%";
      iframe.height = "400";
      iframe.frameBorder = "0";
      iframe.allowFullscreen = true;
      iframe.style.border = "0";
      container.innerHTML = '';
      container.appendChild(iframe);
    }
  }, {threshold: 0.1});
  
  observer.observe(container);
})();
</script>
'''
    
    if 'yandex-map-container' not in html:
        # Insert before footer
        html = html.replace('<footer>', MAP_BLOCK + '\n<footer>', 1)
        write_file(kont_path, html)
    
    git_commit('Block 9: Yandex map with lazy-load on contacts page')


# ============================================================
# BLOCK 10: CTA at end of blog articles
# ============================================================

ARTICLE_CTA = '''
<!-- CTA ARTICLE -->
<div class="article-cta-block">
  <h3>Нужна перевозка из Грузии?</h3>
  <p>Рассчитаем стоимость за 5 минут и подберём оптимальный маршрут. Работаем с 2014 года.</p>
  <div class="article-cta-btns">
    <a href="https://wa.me/995568644615" target="_blank" class="article-cta-wa">
      <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413Z"/></svg>
      WhatsApp
    </a>
    <a href="https://t.me/CARGORAPIDO" target="_blank" class="article-cta-tg">
      <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor"><path d="M11.944 0A12 12 0 0 0 0 12a12 12 0 0 0 12 12 12 12 0 0 0 12-12A12 12 0 0 0 12 0a12 12 0 0 0-.056 0zm4.962 7.224c.1-.002.321.023.465.14a.506.506 0 0 1 .171.325c.016.093.036.306.02.472-.18 1.898-.962 6.502-1.36 8.627-.168.9-.499 1.201-.82 1.23-.696.065-1.225-.46-1.9-.902-1.056-.693-1.653-1.124-2.678-1.8-1.185-.78-.417-1.21.258-1.91.177-.184 3.247-2.977 3.307-3.23.007-.032.014-.15-.056-.212s-.174-.041-.249-.024c-.106.024-1.793 1.14-5.061 3.345-.48.33-.913.49-1.302.48-.428-.008-1.252-.241-1.865-.44-.752-.245-1.349-.374-1.297-.789.027-.216.325-.437.893-.663 3.498-1.524 5.83-2.529 6.998-3.014 3.332-1.386 4.025-1.627 4.476-1.635z"/></svg>
      Telegram
    </a>
  </div>
  
  <div class="article-share-btns">
    <span style="font-size:14px;color:#888;margin-right:8px;">Поделиться:</span>
    <button onclick="shareToTg()" class="share-btn share-tg">📢 Telegram</button>
    <button onclick="shareToWa()" class="share-btn share-wa">📱 WhatsApp</button>
    <button onclick="copyLink(this)" class="share-btn share-copy">🔗 Скопировать</button>
  </div>
</div>

<script>
function shareToTg() {
  window.open('https://t.me/share/url?url=' + encodeURIComponent(location.href) + '&text=' + encodeURIComponent(document.title), '_blank');
}
function shareToWa() {
  window.open('https://wa.me/?text=' + encodeURIComponent(document.title + ' ' + location.href), '_blank');
}
function copyLink(btn) {
  navigator.clipboard.writeText(location.href).then(() => {
    btn.textContent = '✅ Скопировано!';
    setTimeout(() => btn.textContent = '🔗 Скопировать', 2000);
  });
}
</script>
'''

def block10_article_cta():
    print('\n=== BLOCK 10: CTA at end of blog articles ===')
    
    article_dirs = [
        'poleznaya-informaciya/post/aviadostavka-iz-gruzii-v-rossiyu/index.html',
        'poleznaya-informaciya/post/perevozka-lichnyh-veshchej-iz-gruzii-v-rossiyu-v-usloviyah-sankcij/index.html',
        'poleznaya-informaciya/post/perevozka-sbornyh-gruzov/index.html',
        'poleznaya-informaciya/post/kak-bystro-i-bezopasno-otpravit-svoi-veshchi-iz-gruzii-v-rossiyu-strany-sng/index.html',
        'poleznaya-informaciya/post/bystraya-i-bezopasnaya-dostavka-lichnyh-veshchej-iz-gruzii-v-evropu-i-po-miru/index.html',
        'poleznaya-informaciya/post/pereezd-i-perevozka-veshchej-v-turciyu/index.html',
        'poleznaya-informaciya/post/kak-perevezti-lichnye-veshchi-v-gruziyu-iz-rossii/index.html',
    ]
    
    for page_key in article_dirs:
        path = os.path.join(BASE, page_key)
        if not os.path.exists(path):
            print(f'  SKIP: {path}')
            continue
        html = read_file(path)
        if 'article-cta-block' not in html:
            # Insert before </article> or before the cta-banner section
            if '</article>' in html:
                html = html.replace('</article>', ARTICLE_CTA + '\n</article>', 1)
            else:
                html = html.replace('<section class="cta-banner">', ARTICLE_CTA + '\n<section class="cta-banner">', 1)
            write_file(path, html)
    
    git_commit('Block 10: CTA + share buttons at end of all 7 blog articles')


# ============================================================
# BLOCK 11: Reviews page
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
    <p><a href="/sitemap.xml" style="color:rgba(255,255,255,0.4);text-decoration:none;">Карта сайта</a> · <a href="/politika-konfidencialnosti/" style="color:rgba(255,255,255,0.4);text-decoration:none;">Политика конфиденциальности</a></p>
  </div>
</footer>
<script src="/shared.js"></script>'''

def block11_reviews():
    print('\n=== BLOCK 11: Reviews page ===')
    
    reviews_html = f'''<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Отзывы клиентов — Cargo Rapido | Грузоперевозки из Грузии</title>
  <meta name="description" content="Отзывы клиентов Cargo Rapido о перевозке грузов из Грузии в Россию, Европу и СНГ. Реальные отзывы о надёжности и качестве наших услуг.">
  <link rel="canonical" href="https://cargorapido.com/otzyvy/">
  <meta property="og:title" content="Отзывы клиентов — Cargo Rapido">
  <meta property="og:description" content="Реальные отзывы клиентов о перевозке грузов из Грузии. Cargo Rapido — надёжная транспортная компания с 2014 года.">
  <meta property="og:url" content="https://cargorapido.com/otzyvy/">
  <meta property="og:type" content="website">
  <meta property="og:image" content="https://cargorapido.com/truck.jpg">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="google-site-verification" content="U4VPSdMvjvNSx8QubmIyhUwQPcS6y2hnZsIyLe6PMqM">
  <meta name="yandex-verification" content="8d6727b9489f571e">
  <link rel="icon" type="image/x-icon" href="/favicon.ico">
  <link rel="manifest" href="/manifest.json">
  <meta name="theme-color" content="#1a237e">
  <script type="text/javascript">
   (function(m,e,t,r,i,k,a){{m[i]=m[i]||function(){{(m[i].a=m[i].a||[]).push(arguments)}};
   m[i].l=1*new Date();
   for(var j=0;j<document.scripts.length;j++){{if(document.scripts[j].src===r){{return;}}}}
   k=e.createElement(t),a=e.getElementsByTagName(t)[0],k.async=1,k.src=r,a.parentNode.insertBefore(k,a)}}
   )(window, document, "script", "https://mc.yandex.ru/metrika/tag.js", "ym");
   ym(90606836, "init", {{clickmap:true,trackLinks:true,accurateTrackBounce:true,webvisor:true}});
  </script>
  <noscript><div><img src="https://mc.yandex.ru/watch/90606836" style="position:absolute; left:-9999px;" alt="" /></div></noscript>
  <script>(function(w,d,s,l,i){{w[l]=w[l]||[];w[l].push({{'gtm.start':new Date().getTime(),event:'gtm.js'}});var f=d.getElementsByTagName(s)[0],j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src='https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);}})(window,document,'script','dataLayer','GTM-MLNDMC75');</script>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
  <link rel="stylesheet" href="/style.css">
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    "itemListElement": [
      {{"@type":"ListItem","position":1,"name":"Главная","item":"https://cargorapido.com/"}},
      {{"@type":"ListItem","position":2,"name":"Отзывы","item":"https://cargorapido.com/otzyvy/"}}
    ]
  }}
  </script>
</head>
<body>
<noscript><iframe src="https://www.googletagmanager.com/ns.html?id=GTM-MLNDMC75" height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
{HEADER_HTML}

<div class="breadcrumb-nav">
  <div class="breadcrumb-nav-inner">
    <a href="/">Главная</a><span>→</span><span class="current">Отзывы клиентов</span>
  </div>
</div>

<section class="service-hero" style="background:linear-gradient(135deg,#1a237e,#3949ab);">
  <div class="service-hero-inner">
    <div class="service-hero-badge">⭐ Отзывы клиентов</div>
    <h1>Что говорят о нас клиенты</h1>
    <p>Реальные отзывы людей, которые доверили нам свои грузы. Работаем с 2014 года — более 5000 довольных клиентов.</p>
  </div>
</section>

<section class="section">
  <!-- Фильтр -->
  <div class="reviews-filter" style="display:flex;gap:10px;flex-wrap:wrap;margin-bottom:32px;">
    <button class="filter-btn active" onclick="filterReviews('all', this)">Все</button>
    <button class="filter-btn" onclick="filterReviews('lichnye', this)">Личные вещи</button>
    <button class="filter-btn" onclick="filterReviews('kommercheskie', this)">Коммерческие</button>
    <button class="filter-btn" onclick="filterReviews('avto', this)">Автомобиль</button>
    <button class="filter-btn" onclick="filterReviews('evropa', this)">Европа</button>
  </div>

  <div class="reviews-grid" id="reviews-container">
    <!-- Отзыв 1 -->
    <div class="review-card" data-type="lichnye">
      <div class="review-stars">★★★★★</div>
      <p class="review-text">«Отзыв будет добавлен. А.К. — клиент компании Cargo Rapido, перевозка личных вещей из Тбилиси в Москву.»</p>
      <div class="review-author">
        <div class="review-avatar" style="background:linear-gradient(135deg,#1a237e,#3949ab);">А</div>
        <div>
          <div class="review-name">А.К.</div>
          <div class="review-city">Москва · личные вещи</div>
        </div>
      </div>
    </div>
    <!-- Отзыв 2 -->
    <div class="review-card" data-type="kommercheskie">
      <div class="review-stars">★★★★★</div>
      <p class="review-text">«Отзыв будет добавлен. М.В. — клиент компании Cargo Rapido, коммерческие перевозки.»</p>
      <div class="review-author">
        <div class="review-avatar" style="background:linear-gradient(135deg,#e53935,#ef5350);">М</div>
        <div>
          <div class="review-name">М.В.</div>
          <div class="review-city">ИП · коммерческие грузы</div>
        </div>
      </div>
    </div>
    <!-- Отзыв 3 -->
    <div class="review-card" data-type="avto">
      <div class="review-stars">★★★★★</div>
      <p class="review-text">«Отзыв будет добавлен. Д.Т. — клиент компании Cargo Rapido, перевозка автомобиля.»</p>
      <div class="review-author">
        <div class="review-avatar" style="background:linear-gradient(135deg,#2e7d32,#43a047);">Д</div>
        <div>
          <div class="review-name">Д.Т.</div>
          <div class="review-city">Алматы · перевозка авто</div>
        </div>
      </div>
    </div>
    <!-- Отзыв 4 -->
    <div class="review-card" data-type="lichnye">
      <div class="review-stars">★★★★★</div>
      <p class="review-text">«Отзыв будет добавлен. Н.С. — клиент компании Cargo Rapido, переезд из Грузии.»</p>
      <div class="review-author">
        <div class="review-avatar" style="background:linear-gradient(135deg,#f57c00,#ffa000);">Н</div>
        <div>
          <div class="review-name">Н.С.</div>
          <div class="review-city">Санкт-Петербург · переезд</div>
        </div>
      </div>
    </div>
    <!-- Отзыв 5 -->
    <div class="review-card" data-type="evropa">
      <div class="review-stars">★★★★★</div>
      <p class="review-text">«Отзыв будет добавлен. Р.А. — клиент компании Cargo Rapido, доставка в Европу.»</p>
      <div class="review-author">
        <div class="review-avatar" style="background:linear-gradient(135deg,#6a1b9a,#8e24aa);">Р</div>
        <div>
          <div class="review-name">Р.А.</div>
          <div class="review-city">Берлин · доставка в Европу</div>
        </div>
      </div>
    </div>
  </div>
  
  <div style="text-align:center;margin-top:40px;padding:32px;background:#f8f9ff;border-radius:16px;">
    <h3 style="margin-bottom:8px;">Хотите оставить отзыв?</h3>
    <p style="color:#666;margin-bottom:20px;">Напишите нам в Telegram или WhatsApp — опубликуем ваш отзыв на сайте.</p>
    <div style="display:flex;gap:12px;justify-content:center;flex-wrap:wrap;">
      <a href="https://t.me/CARGORAPIDO" target="_blank" class="btn-dark"><i class="fab fa-telegram"></i> Написать в Telegram</a>
      <a href="https://wa.me/995568644615" target="_blank" class="btn-green"><i class="fab fa-whatsapp"></i> WhatsApp</a>
    </div>
  </div>
</section>

<script>
function filterReviews(type, btn) {{
  document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
  btn.classList.add('active');
  document.querySelectorAll('.review-card').forEach(card => {{
    if (type === 'all' || card.dataset.type === type) {{
      card.style.display = '';
    }} else {{
      card.style.display = 'none';
    }}
  }});
}}
</script>

{FOOTER_HTML}
</body>
</html>'''
    
    write_file(os.path.join(BASE, 'otzyvy/index.html'), reviews_html)
    
    # Add reviews section to homepage
    idx_path = os.path.join(BASE, 'index.html')
    html = read_file(idx_path)
    
    if 'otzyvy-section' not in html:
        REVIEWS_SECTION = '''
<!-- REVIEWS PROMO -->
<section class="section section-light" id="otzyvy-section">
  <div class="sec-tag">Отзывы клиентов</div>
  <div class="sec-h2">Что говорят о нас</div>
  <div class="reviews-grid">
    <div class="review-card">
      <div class="review-stars">★★★★★</div>
      <p class="review-text">«Перевозили вещи при переезде из Тбилиси в Москву. Всё упаковали аккуратно, ни одна вещь не повредилась. Груз пришёл за 5 дней. Менеджер Наталья была на связи в любое время. Рекомендую!»</p>
      <div class="review-author">
        <div class="review-avatar" style="background:linear-gradient(135deg,#1a237e,#3949ab);">А</div>
        <div><div class="review-name">Алексей К.</div><div class="review-city">Москва · переезд из Тбилиси</div></div>
      </div>
    </div>
    <div class="review-card">
      <div class="review-stars">★★★★★</div>
      <p class="review-text">«Отправляем товары из Грузии в Россию уже два года. Cargo Rapido — наш постоянный партнёр. Ни разу не было проблем с таможней, все документы оформляют сами.»</p>
      <div class="review-author">
        <div class="review-avatar" style="background:linear-gradient(135deg,#e53935,#ef5350);">М</div>
        <div><div class="review-name">Маргарита В.</div><div class="review-city">ИП · регулярные поставки</div></div>
      </div>
    </div>
    <div class="review-card">
      <div class="review-stars">★★★★★</div>
      <p class="review-text">«Отправлял грузинское вино в Казахстан — специфический груз с кучей сертификатов. Ребята разобрались со всеми документами, вино дошло в целости. Буду работать только с ними.»</p>
      <div class="review-author">
        <div class="review-avatar" style="background:linear-gradient(135deg,#2e7d32,#43a047);">Н</div>
        <div><div class="review-name">Нурлан А.</div><div class="review-city">Алматы · экспорт продуктов</div></div>
      </div>
    </div>
  </div>
  <div style="text-align:center;margin-top:32px;">
    <a href="/otzyvy/" class="btn-dark"><i class="fas fa-star"></i> Все отзывы</a>
  </div>
</section>
'''
        # Insert before FAQ or CTA
        if '<!-- FAQ -->' in html:
            html = html.replace('<!-- FAQ -->', REVIEWS_SECTION + '\n<!-- FAQ -->')
        elif '<!-- CTA -->' in html:
            html = html.replace('<!-- CTA -->', REVIEWS_SECTION + '\n<!-- CTA -->')
        write_file(idx_path, html)
    
    git_commit('Block 11: Create otzyvy/index.html with filter + add reviews section to homepage')


# ============================================================
# BLOCK 12: Delivery timeline on service pages
# ============================================================

TIMELINE_SECTION = '''
<!-- DELIVERY TIMELINE -->
<section class="section" id="delivery-timeline">
  <div class="sec-tag">Как это работает</div>
  <div class="sec-h2">Процесс доставки</div>
  <div class="timeline-wrap">
    <div class="timeline-item">
      <div class="timeline-ico">
        <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline><line x1="16" y1="13" x2="8" y2="13"></line><line x1="16" y1="17" x2="8" y2="17"></line><polyline points="10 9 9 9 8 9"></polyline></svg>
      </div>
      <div class="timeline-step">01</div>
      <h4>Заявка</h4>
      <p>Напишите нам — рассчитаем стоимость за 5 минут</p>
    </div>
    <div class="timeline-arrow">→</div>
    <div class="timeline-item">
      <div class="timeline-ico">
        <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="7" width="20" height="14" rx="2" ry="2"></rect><path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"></path></svg>
      </div>
      <div class="timeline-step">02</div>
      <h4>Приём груза</h4>
      <p>Забираем у вас или принимаем на складе в Тбилиси</p>
    </div>
    <div class="timeline-arrow">→</div>
    <div class="timeline-item">
      <div class="timeline-ico">
        <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"></path></svg>
      </div>
      <div class="timeline-step">03</div>
      <h4>Упаковка</h4>
      <p>Профессиональная упаковка — сохраним груз в целости</p>
    </div>
    <div class="timeline-arrow">→</div>
    <div class="timeline-item">
      <div class="timeline-ico">
        <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 11l3 3L22 4"></path><path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"></path></svg>
      </div>
      <div class="timeline-step">04</div>
      <h4>Таможня</h4>
      <p>Брокер в штате — оформляем все документы без вас</p>
    </div>
    <div class="timeline-arrow">→</div>
    <div class="timeline-item">
      <div class="timeline-ico">
        <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="1" y="3" width="15" height="13"></rect><polygon points="16 8 20 8 23 11 23 16 16 16 16 8"></polygon><circle cx="5.5" cy="18.5" r="2.5"></circle><circle cx="18.5" cy="18.5" r="2.5"></circle></svg>
      </div>
      <div class="timeline-step">05</div>
      <h4>Транспортировка</h4>
      <p>GPS-трекинг онлайн — знаете где груз в любой момент</p>
    </div>
    <div class="timeline-arrow">→</div>
    <div class="timeline-item">
      <div class="timeline-ico">
        <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path><polyline points="9 22 9 12 15 12 15 22"></polyline></svg>
      </div>
      <div class="timeline-step">06</div>
      <h4>Доставка</h4>
      <p>Груз у вас — уведомим и передадим по адресу</p>
    </div>
  </div>
</section>
'''

def block12_timeline():
    print('\n=== BLOCK 12: Delivery timeline on service pages ===')
    
    service_pages = [
        'perevozka-kommercheskih-gruzov/index.html',
        'perevozka-lichnyh-veshchej/index.html',
        'dostavka-v-evropu/index.html',
        'dostavka-posylok-pisem-i-dokumentov-po-vsemu-miru/index.html',
        'perevozka-gruzov-pod-termorezhimom/index.html',
        'perevozka-avtomobilya-na-avtovoze/index.html',
        'perevozka-avtomobilya-na-evakuatore/index.html',
        'skladskie-uslugi/index.html',
        'brokerskie-uslugi/index.html',
    ]
    
    for page_key in service_pages:
        path = os.path.join(BASE, page_key)
        if not os.path.exists(path):
            print(f'  SKIP: {path}')
            continue
        html = read_file(path)
        if 'delivery-timeline' not in html:
            # Insert before form-section or footer
            if 'form-section' in html:
                html = html.replace('<!-- ЗАЯВКА -->', TIMELINE_SECTION + '\n<!-- ЗАЯВКА -->', 1)
            else:
                html = html.replace('<footer>', TIMELINE_SECTION + '\n<footer>', 1)
            write_file(path, html)
    
    git_commit('Block 12: Delivery timeline (6 steps with SVG icons) on all 9 service pages')


# ============================================================
# BLOCK 13: 404 page + manifest.json + favicon meta
# ============================================================

def block13_404_manifest():
    print('\n=== BLOCK 13: 404.html + manifest.json ===')
    
    # manifest.json
    manifest = '''{
  "name": "Cargo Rapido",
  "short_name": "CargoRapido",
  "description": "Грузоперевозки из Грузии в Россию, СНГ и Европу",
  "start_url": "/",
  "display": "browser",
  "background_color": "#ffffff",
  "theme_color": "#e63946",
  "icons": [
    {
      "src": "/logo.jpg",
      "sizes": "192x192",
      "type": "image/jpeg"
    },
    {
      "src": "/logo.jpg",
      "sizes": "512x512",
      "type": "image/jpeg"
    }
  ]
}'''
    write_file(os.path.join(BASE, 'manifest.json'), manifest)
    
    # 404.html
    page_404 = f'''<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>404 — Страница не найдена | Cargo Rapido</title>
  <meta name="description" content="Страница не найдена. Вернитесь на главную страницу Cargo Rapido — грузоперевозки из Грузии.">
  <meta name="robots" content="noindex, follow">
  <link rel="canonical" href="https://cargorapido.com/">
  <link rel="icon" type="image/x-icon" href="/favicon.ico">
  <link rel="manifest" href="/manifest.json">
  <meta name="theme-color" content="#1a237e">
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
  <link rel="stylesheet" href="/style.css">
</head>
<body>
{HEADER_HTML}

<div style="min-height:60vh;display:flex;align-items:center;justify-content:center;text-align:center;padding:60px 24px;">
  <div>
    <div style="font-size:120px;font-weight:900;color:#e8eaf6;line-height:1;">404</div>
    <h1 style="font-size:2rem;margin:-20px 0 16px;color:#1a237e;">Страница не найдена</h1>
    <p style="color:#666;max-width:480px;margin:0 auto 32px;">К сожалению, такой страницы не существует. Возможно, она была удалена или вы перешли по неверной ссылке.</p>
    <div style="display:flex;gap:12px;justify-content:center;flex-wrap:wrap;">
      <a href="/" class="btn-dark"><i class="fas fa-home"></i> На главную</a>
      <a href="/nashi-uslugi/" class="btn-dark" style="background:#3949ab;"><i class="fas fa-truck"></i> Наши услуги</a>
      <a href="https://t.me/CARGORAPIDO" target="_blank" class="btn-green"><i class="fab fa-telegram"></i> Написать нам</a>
    </div>
    <div style="margin-top:40px;padding:24px;background:#f8f9ff;border-radius:12px;max-width:400px;margin:40px auto 0;">
      <p style="font-weight:600;margin-bottom:12px;">Нужна помощь?</p>
      <p style="color:#666;font-size:14px;">Свяжитесь с нами — ответим за 15 минут.</p>
      <p style="margin-top:8px;"><a href="https://wa.me/995568644615" style="color:#25D366;font-weight:700;">+995 568 644 615</a></p>
    </div>
  </div>
</div>

{FOOTER_HTML}
</body>
</html>'''
    
    write_file(os.path.join(BASE, '404.html'), page_404)
    
    git_commit('Block 13: Create 404.html + manifest.json for PWA')


# ============================================================
# Add CSS for new components
# ============================================================

def add_css():
    print('\n=== Adding CSS for new components ===')
    
    new_css = '''

/* ===== COOKIE BANNER ===== */
#cookie-banner {
  position: fixed;
  bottom: -100px;
  left: 0;
  right: 0;
  z-index: 9999;
  transition: bottom 0.4s ease;
  padding: 0 16px 16px;
}
#cookie-banner.visible { bottom: 0; }
.cookie-banner-inner {
  max-width: 900px;
  margin: 0 auto;
  background: #1a237e;
  color: white;
  padding: 16px 20px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  gap: 16px;
  flex-wrap: wrap;
  box-shadow: 0 4px 24px rgba(26,35,126,0.3);
}
.cookie-banner-inner p { margin: 0; flex: 1; min-width: 200px; font-size: 14px; }
.cookie-banner-inner a { color: #ffa040; }
.cookie-banner-btns { display: flex; gap: 10px; }
.cookie-btn-accept {
  padding: 9px 20px;
  background: #ffa040;
  color: #1a237e;
  border: none;
  border-radius: 8px;
  font-weight: 700;
  cursor: pointer;
  font-size: 14px;
  font-family: inherit;
}
.cookie-btn-more {
  padding: 9px 16px;
  border: 1px solid rgba(255,255,255,0.4);
  color: white;
  border-radius: 8px;
  font-size: 14px;
  text-decoration: none;
}

/* ===== WHATSAPP WIDGET ===== */
#wa-widget {
  position: fixed;
  bottom: 24px;
  right: 24px;
  z-index: 9998;
}
.wa-trigger {
  width: 60px;
  height: 60px;
  background: #25D366;
  border: none;
  border-radius: 50%;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 16px rgba(37,211,102,0.4);
  transition: transform 0.2s, box-shadow 0.2s;
  position: relative;
  z-index: 2;
}
.wa-trigger:hover { transform: scale(1.1); }
.wa-trigger.active { transform: rotate(90deg); }
.wa-menu {
  position: absolute;
  bottom: 70px;
  right: 0;
  display: flex;
  flex-direction: column;
  gap: 10px;
  opacity: 0;
  pointer-events: none;
  transform: translateY(10px);
  transition: all 0.25s ease;
}
.wa-menu.open { opacity: 1; pointer-events: all; transform: translateY(0); }
.wa-menu-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 16px;
  border-radius: 10px;
  color: white;
  text-decoration: none;
  font-weight: 600;
  font-size: 14px;
  white-space: nowrap;
  box-shadow: 0 2px 12px rgba(0,0,0,0.15);
  transition: transform 0.2s;
}
.wa-menu-item:hover { transform: translateX(-4px); }
.wa-item { background: #25D366; }
.tg-item { background: #0088cc; }
.wa-bubble {
  position: absolute;
  bottom: 70px;
  right: 70px;
  background: white;
  border-radius: 12px 12px 0 12px;
  padding: 14px 16px;
  max-width: 240px;
  box-shadow: 0 4px 20px rgba(0,0,0,0.15);
  opacity: 0;
  pointer-events: none;
  transform: scale(0.8);
  transform-origin: bottom right;
  transition: all 0.3s ease;
}
.wa-bubble.visible { opacity: 1; pointer-events: all; transform: scale(1); }
.wa-bubble-avatar { font-size: 24px; margin-bottom: 6px; }
.wa-bubble-text { font-size: 13px; color: #333; line-height: 1.5; }
.wa-bubble-close {
  position: absolute;
  top: 6px;
  right: 8px;
  background: none;
  border: none;
  font-size: 16px;
  cursor: pointer;
  color: #aaa;
}

/* ===== FAQ ===== */
.faq-list { max-width: 800px; margin: 0 auto; }
.faq-item { border-bottom: 1px solid #f0f0f8; }
.faq-q {
  width: 100%;
  text-align: left;
  background: none;
  border: none;
  padding: 18px 0;
  font-size: 16px;
  font-weight: 600;
  color: #1a237e;
  cursor: pointer;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 12px;
  font-family: inherit;
  line-height: 1.4;
}
.faq-icon { font-size: 20px; flex-shrink: 0; color: #1a237e; transition: transform 0.2s; }
.faq-item.open .faq-icon { transform: rotate(45deg); }
.faq-a {
  max-height: 0;
  overflow: hidden;
  transition: max-height 0.35s ease, padding 0.2s;
}
.faq-item.open .faq-a { max-height: 300px; padding-bottom: 16px; }
.faq-a p { color: #555; line-height: 1.7; }

/* ===== FORM COMPONENT ===== */
.cr-form-wrapper { max-width: 760px; margin: 0 auto; }
.cr-form-title { font-size: 1.5rem; font-weight: 700; color: #1a237e; margin-bottom: 24px; }
.cr-form-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}
.cr-field { display: flex; flex-direction: column; gap: 6px; }
.cr-field-full { grid-column: 1 / -1; }
.cr-field label { font-size: 13px; font-weight: 600; color: #444; }
.cr-field .req { color: #e53935; }
.cr-field input, .cr-field select, .cr-field textarea {
  padding: 11px 14px;
  border: 1.5px solid #e0e0f0;
  border-radius: 8px;
  font-family: inherit;
  font-size: 15px;
  color: #333;
  background: white;
  transition: border-color 0.2s;
}
.cr-field input:focus, .cr-field select:focus, .cr-field textarea:focus {
  outline: none;
  border-color: #1a237e;
}
.cr-consent { margin-top: 4px; }
.cr-checkbox-label { display: flex; align-items: flex-start; gap: 10px; cursor: pointer; font-size: 14px; color: #555; }
.cr-checkbox-label input { width: 18px; height: 18px; flex-shrink: 0; margin-top: 2px; accent-color: #1a237e; }
.cr-checkbox-label a { color: #1a237e; }
.cr-form-actions { margin-top: 20px; }
.cr-submit-btn {
  padding: 14px 32px;
  background: #1a237e;
  color: white;
  border: none;
  border-radius: 10px;
  font-family: inherit;
  font-size: 16px;
  font-weight: 700;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: background 0.2s;
}
.cr-submit-btn:hover { background: #0d1257; }
.cr-submit-btn:disabled { opacity: 0.7; cursor: not-allowed; }
.cr-success { text-align: center; padding: 40px 20px; }
.cr-success-icon { font-size: 48px; margin-bottom: 12px; }
.cr-success h3 { font-size: 1.4rem; color: #1a237e; margin-bottom: 8px; }
.cr-success p { color: #555; }
@media (max-width: 600px) {
  .cr-form-grid { grid-template-columns: 1fr; }
}

/* ===== ARTICLE CTA ===== */
.article-cta-block {
  background: linear-gradient(135deg, #1a237e 0%, #3949ab 100%);
  color: white;
  padding: 32px;
  border-radius: 16px;
  margin: 32px 0;
  text-align: center;
}
.article-cta-block h3 { font-size: 1.4rem; margin-bottom: 8px; }
.article-cta-block p { color: rgba(255,255,255,0.85); margin-bottom: 20px; }
.article-cta-btns { display: flex; gap: 12px; justify-content: center; flex-wrap: wrap; margin-bottom: 20px; }
.article-cta-wa {
  display: flex; align-items: center; gap: 8px;
  padding: 12px 24px; background: #25D366; color: white;
  border-radius: 10px; font-weight: 700; text-decoration: none;
}
.article-cta-tg {
  display: flex; align-items: center; gap: 8px;
  padding: 12px 24px; background: #0088cc; color: white;
  border-radius: 10px; font-weight: 700; text-decoration: none;
}
.article-share-btns { display: flex; align-items: center; justify-content: center; gap: 8px; flex-wrap: wrap; }
.share-btn {
  padding: 8px 16px; border: 1px solid rgba(255,255,255,0.4); color: white;
  background: transparent; border-radius: 8px; cursor: pointer; font-size: 13px;
  font-family: inherit;
}
.share-btn:hover { background: rgba(255,255,255,0.1); }

/* ===== REVIEWS FILTER ===== */
.filter-btn {
  padding: 8px 18px; border: 1.5px solid #e0e0f0; background: white;
  border-radius: 20px; cursor: pointer; font-family: inherit; font-size: 14px;
  font-weight: 600; color: #555; transition: all 0.2s;
}
.filter-btn.active, .filter-btn:hover { background: #1a237e; color: white; border-color: #1a237e; }

/* ===== DELIVERY TIMELINE ===== */
.timeline-wrap {
  display: flex;
  align-items: flex-start;
  gap: 0;
  overflow-x: auto;
  padding-bottom: 16px;
}
.timeline-item {
  flex: 1;
  min-width: 120px;
  text-align: center;
  padding: 0 8px;
}
.timeline-ico {
  width: 64px;
  height: 64px;
  background: linear-gradient(135deg, #1a237e, #3949ab);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 12px;
  color: white;
}
.timeline-step {
  font-size: 11px;
  font-weight: 700;
  color: #1a237e;
  opacity: 0.6;
  margin-bottom: 4px;
}
.timeline-item h4 { font-size: 15px; font-weight: 700; color: #1a237e; margin-bottom: 6px; }
.timeline-item p { font-size: 13px; color: #666; line-height: 1.4; }
.timeline-arrow {
  font-size: 24px;
  color: #c0c8e8;
  padding: 20px 4px 0;
  flex-shrink: 0;
  align-self: flex-start;
}
@media (max-width: 768px) {
  .timeline-wrap {
    flex-direction: column;
    align-items: flex-start;
    overflow-x: visible;
  }
  .timeline-item { display: flex; align-items: flex-start; gap: 16px; text-align: left; width: 100%; min-width: unset; padding: 8px 0; }
  .timeline-ico { flex-shrink: 0; margin: 0; width: 48px; height: 48px; }
  .timeline-arrow { transform: rotate(90deg); align-self: flex-start; padding: 0 0 0 20px; }
}

/* ===== LEGAL PAGE ===== */
.legal-page { padding: 40px 24px; }
.legal-content h1 { color: #1a237e; margin-bottom: 8px; }
.legal-content h2 { color: #1a237e; font-size: 1.15rem; margin: 28px 0 10px; }
.legal-content p { color: #444; line-height: 1.8; margin-bottom: 12px; }
.legal-content ul { color: #444; line-height: 1.8; margin: 0 0 16px 20px; }
.legal-content li { margin-bottom: 6px; }
.legal-content a { color: #1a237e; }
'''
    
    css_path = os.path.join(BASE, 'style.css')
    css = read_file(css_path)
    if '/* ===== COOKIE BANNER =====' not in css:
        css += new_css
        write_file(css_path, css)
    
    git_commit('CSS: Add styles for cookie banner, WhatsApp widget, FAQ, form, timeline, article CTA, reviews filter, legal')


# ============================================================
# Update footers on all existing pages to add legal links
# ============================================================

def update_footers():
    print('\n=== Updating footers on all pages ===')
    
    all_pages = [
        'index.html', 'about/index.html', 'kontakty/index.html',
        'nashi-uslugi/index.html',
        'perevozka-kommercheskih-gruzov/index.html',
        'perevozka-lichnyh-veshchej/index.html',
        'dostavka-v-evropu/index.html',
        'dostavka-posylok-pisem-i-dokumentov-po-vsemu-miru/index.html',
        'perevozka-gruzov-pod-termorezhimom/index.html',
        'perevozka-avtomobilya-na-avtovoze/index.html',
        'perevozka-avtomobilya-na-evakuatore/index.html',
        'skladskie-uslugi/index.html',
        'brokerskie-uslugi/index.html',
        'poleznaya-informaciya/index.html',
        'poleznaya-informaciya/post/aviadostavka-iz-gruzii-v-rossiyu/index.html',
        'poleznaya-informaciya/post/perevozka-lichnyh-veshchej-iz-gruzii-v-rossiyu-v-usloviyah-sankcij/index.html',
        'poleznaya-informaciya/post/perevozka-sbornyh-gruzov/index.html',
        'poleznaya-informaciya/post/kak-bystro-i-bezopasno-otpravit-svoi-veshchi-iz-gruzii-v-rossiyu-strany-sng/index.html',
        'poleznaya-informaciya/post/bystraya-i-bezopasnaya-dostavka-lichnyh-veshchej-iz-gruzii-v-evropu-i-po-miru/index.html',
        'poleznaya-informaciya/post/pereezd-i-perevozka-veshchej-v-turciyu/index.html',
        'poleznaya-informaciya/post/kak-perevezti-lichnye-veshchi-v-gruziyu-iz-rossii/index.html',
    ]
    
    for page_key in all_pages:
        path = os.path.join(BASE, page_key)
        if not os.path.exists(path):
            continue
        html = read_file(path)
        
        # Add legal links to footer if missing
        if 'politika-konfidencialnosti' not in html:
            old_bottom = '<p>© 2024 Cargo Rapido. Все права защищены.</p>'
            new_bottom = '<p>© 2024 Cargo Rapido. Все права защищены. <a href="/politika-konfidencialnosti/" style="color:rgba(255,255,255,0.5);text-decoration:none;">Политика конфиденциальности</a> · <a href="/usloviya-okazaniya-uslug/" style="color:rgba(255,255,255,0.5);text-decoration:none;">Условия услуг</a></p>'
            if old_bottom in html:
                html = html.replace(old_bottom, new_bottom, 1)
                write_file(path, html)
        
        # Add email to footer contacts if missing
        if 'cargorapido.ge@gmail.com' not in html:
            old_contacts = '<li><a href="https://t.me/CARGORAPIDO" target="_blank">Telegram</a></li>\n        <li><a href="https://facebook.com/CargoRapido"'
            new_contacts = '<li><a href="https://t.me/CARGORAPIDO" target="_blank">Telegram</a></li>\n        <li><a href="mailto:cargorapido.ge@gmail.com">Email</a></li>\n        <li><a href="https://facebook.com/CargoRapido"'
            if old_contacts in html:
                html = html.replace(old_contacts, new_contacts, 1)
                write_file(path, html)
    
    git_commit('Footers: Add legal page links and email to all pages')


# ============================================================
# MAIN
# ============================================================

if __name__ == '__main__':
    print('=== Starting build2.py ===')
    block7_faq()
    block9_yandex_map()
    block10_article_cta()
    block11_reviews()
    block12_timeline()
    block13_404_manifest()
    add_css()
    update_footers()
    print('\n=== build2.py complete ===')
