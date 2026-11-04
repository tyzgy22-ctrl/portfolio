# Генератор демо-набросков сайтов для реальных компаний (для холодных предложений).
# Только настоящие данные из 2ГИС (адрес, рейтинг, число отзывов); цены помечены как примерные;
# на каждой странице плашка «демо-набросок» и запрет индексации.
# Запуск: python build.py  ->  demo/<slug>/index.html
import os, html

HERE = os.path.dirname(os.path.abspath(__file__))
PORTFOLIO = "https://tyzgy22-ctrl.github.io/portfolio/"

ART = {
 "barber": '''<svg viewBox="0 0 300 300" class="art"><defs><linearGradient id="g1" x1="0" x2="1"><stop offset="0" stop-color="var(--acc)"/><stop offset="1" stop-color="var(--acc2)"/></linearGradient></defs>
  <circle cx="150" cy="150" r="130" fill="none" stroke="var(--line)" stroke-width="2"/>
  <g transform="rotate(-35 150 150)"><rect x="135" y="40" width="30" height="150" rx="6" fill="url(#g1)"/><rect x="128" y="185" width="44" height="70" rx="10" fill="var(--text)"/>
  <rect x="139" y="50" width="22" height="130" rx="4" fill="none" stroke="var(--bg)" stroke-width="2" opacity=".35"/></g>
  <g transform="rotate(35 150 150)" opacity=".9"><rect x="141" y="30" width="18" height="170" rx="9" fill="var(--text)"/><g fill="var(--bg)"><rect x="141" y="60" width="18" height="3"/><rect x="141" y="72" width="18" height="3"/><rect x="141" y="84" width="18" height="3"/><rect x="141" y="96" width="18" height="3"/><rect x="141" y="108" width="18" height="3"/><rect x="141" y="120" width="18" height="3"/></g></g></svg>''',
 "vinyl": '''<svg viewBox="0 0 300 300" class="art spin"><circle cx="150" cy="150" r="140" fill="#111"/>
  <g fill="none" stroke="#2a2a2a" stroke-width="1.5"><circle cx="150" cy="150" r="125"/><circle cx="150" cy="150" r="112"/><circle cx="150" cy="150" r="99"/><circle cx="150" cy="150" r="86"/><circle cx="150" cy="150" r="73"/></g>
  <path d="M60 80 A110 110 0 0 1 150 40" stroke="rgba(255,255,255,.18)" stroke-width="6" fill="none" stroke-linecap="round"/>
  <circle cx="150" cy="150" r="52" fill="var(--acc)"/><circle cx="150" cy="150" r="6" fill="#111"/>
  <text x="150" y="137" text-anchor="middle" font-size="11" fill="var(--bg)" font-family="Manrope" font-weight="700" letter-spacing="2">ВИНИЛ</text>
  <text x="150" y="172" text-anchor="middle" font-size="11" fill="var(--bg)" font-family="Manrope" font-weight="700" letter-spacing="2">&amp; КОФЕ</text></svg>''',
 "tattoo": '''<svg viewBox="0 0 300 300" class="art"><defs><radialGradient id="gl"><stop offset="0" stop-color="var(--acc)" stop-opacity=".55"/><stop offset="1" stop-color="var(--acc)" stop-opacity="0"/></radialGradient></defs>
  <circle cx="150" cy="150" r="140" fill="url(#gl)"/>
  <g fill="none" stroke="var(--text)" stroke-width="3" stroke-linecap="round" stroke-linejoin="round">
  <path d="M150 70c-30 40-45 62-45 85a45 45 0 0 0 90 0c0-23-15-45-45-85z"/><path d="M150 112c-14 20-21 31-21 43a21 21 0 0 0 42 0c0-12-7-23-21-43z" stroke="var(--acc)"/>
  <path d="M95 235h110M115 250h70" opacity=".5"/></g></svg>''',
 "nails": '''<svg viewBox="0 0 300 300" class="art"><g><circle cx="110" cy="120" r="70" fill="var(--acc)" opacity=".85"/><circle cx="185" cy="105" r="55" fill="var(--acc2)" opacity=".8"/><circle cx="170" cy="190" r="65" fill="var(--acc3)" opacity=".75"/></g>
  <g fill="#fff" opacity=".95"><rect x="96" y="150" width="26" height="46" rx="13"/><rect x="130" y="138" width="26" height="54" rx="13"/><rect x="164" y="142" width="26" height="50" rx="13"/><rect x="198" y="156" width="24" height="40" rx="12"/></g></svg>''',
 "flowers": '''<svg viewBox="0 0 300 300" class="art"><g stroke="var(--leaf)" stroke-width="4" fill="none" stroke-linecap="round"><path d="M150 280C150 200 140 150 110 100"/><path d="M150 280C152 200 170 150 200 110"/><path d="M150 280c0-60 0-110 0-160"/></g>
  <g fill="var(--leaf)" opacity=".85"><ellipse cx="125" cy="190" rx="26" ry="10" transform="rotate(-35 125 190)"/><ellipse cx="178" cy="200" rx="26" ry="10" transform="rotate(30 178 200)"/><ellipse cx="135" cy="150" rx="20" ry="8" transform="rotate(-50 135 150)"/></g>
  <g fill="var(--acc)"><circle cx="105" cy="92" r="11"/><circle cx="122" cy="84" r="11"/><circle cx="112" cy="74" r="10"/><circle cx="96" cy="78" r="9"/><circle cx="150" cy="112" r="12"/><circle cx="138" cy="100" r="10"/><circle cx="162" cy="98" r="11"/><circle cx="150" cy="88" r="10"/><circle cx="200" cy="100" r="11"/><circle cx="214" cy="90" r="10"/><circle cx="192" cy="86" r="9"/><circle cx="206" cy="76" r="9"/></g>
  <g fill="#fff" opacity=".5"><circle cx="102" cy="88" r="3"/><circle cx="146" cy="108" r="3"/><circle cx="197" cy="96" r="3"/></g></svg>''',
}

SITES = [
 dict(slug="tj-haircuts", name="Tj Haircuts", kind="Барбершоп", art="barber",
      addr="Звенигородская улица, 26", rating="5,0", reviews=362, link="https://2gis.ru/spb/firm/70000001032416557",
      fonts="Oswald:wght@500;700&family=Inter:wght@400;500;700", hfont="Oswald", bfont="Inter", upper=True,
      c=dict(bg="#121212", card="#1b1b1b", text="#f2efe9", muted="#9b968d", acc="#ff7a1a", acc2="#ffb066", acc3="#ff7a1a", line="#2a2a2a", leaf="#000"),
      title="Стрижка, после которой хочется в зеркало", sub="Мужские стрижки, фейды и борода у Звенигородской. Записывайтесь онлайн в пару касаний, без звонков и ожидания.",
      cta="Записаться онлайн",
      feats=[("Онлайн-запись 24/7", "Клиент выбирает мастера и время сам, даже ночью"), ("Прайс на виду", "Цены на все услуги до записи, без сюрпризов"), ("Работы мастеров", "Галерея стрижек, по которой легко выбрать свою")],
      services=[("Мужская стрижка", "1 500 ₽"), ("Стрижка + борода", "2 300 ₽"), ("Фейд", "1 700 ₽"), ("Оформление бороды", "1 000 ₽"), ("Детская стрижка", "1 100 ₽"), ("Камуфляж седины", "900 ₽")]),
 dict(slug="vinil-i-kofe", name="Винил & кофе", kind="Кофейня", art="vinyl",
      addr="улица Малая Садовая, 4 (во дворе)", rating="5,0", reviews=284, link="https://2gis.ru/spb/firm/70000001064803008",
      fonts="Playfair+Display:ital,wght@0,600;1,600&family=Manrope:wght@400;500;700", hfont="Playfair Display", bfont="Manrope", upper=False,
      c=dict(bg="#16110e", card="#211a15", text="#f4ebdd", muted="#b3a28c", acc="#e2553b", acc2="#f0a35e", acc3="#e2553b", line="#33291f", leaf="#000"),
      title="Кофе, вафли и пластинки во дворе у Невского", sub="Спрятанная кофейня с плющом на входе: внизу варим кофе и печём вафли, наверху мансарда с проигрывателем и винилом.",
      cta="Как нас найти",
      feats=[("Меню онлайн", "Кофе, вафли, сезонные напитки и сидр с ценами"), ("Как найти вход", "Карта и фото входа во двор, чтобы гости не блуждали"), ("Пластинка дня", "Что сегодня играет на втором этаже")],
      services=[("Капучино", "250 ₽"), ("Авторский кофе", "от 320 ₽"), ("Вафли сладкие", "от 290 ₽"), ("Вафли сытные", "от 390 ₽"), ("Сезонный напиток", "от 330 ₽"), ("Сидр", "от 350 ₽")]),
 dict(slug="teplo-tattoo", name="Teplo Tattoo", kind="Студия татуировки и пирсинга", art="tattoo",
      addr="набережная реки Мойки, 81", rating="5,0", reviews=217, link="https://2gis.ru/spb/firm/70000001055212022",
      fonts="Unbounded:wght@500;700&family=Inter:wght@400;500;700", hfont="Unbounded", bfont="Inter", upper=False,
      c=dict(bg="#0f0c0a", card="#1a1512", text="#f3e9df", muted="#a8988a", acc="#ff9d3c", acc2="#ffcf8a", acc3="#ff9d3c", line="#2b231d", leaf="#000"),
      title="Тату и пирсинг в тёплой атмосфере", sub="Художественная татуировка, перекрытие старых работ и пирсинг на Мойке. Портфолио мастеров и запись на консультацию на одной странице.",
      cta="Записаться на консультацию",
      feats=[("Портфолио по стилям", "Графика, реализм, минимализм: клиент сразу видит, к кому идти"), ("Запись на эскиз", "Форма с описанием идеи и референсами"), ("Уход после сеанса", "Памятка, которую не нужно пересылать каждому")],
      services=[("Мини-тату", "от 4 000 ₽"), ("Тату среднего размера", "от 8 000 ₽"), ("Перекрытие", "по эскизу"), ("Пирсинг", "от 2 500 ₽"), ("Консультация и эскиз", "бесплатно"), ("Час работы мастера", "от 5 000 ₽")]),
 dict(slug="guash", name="Guash", kind="Студия маникюра", art="nails",
      addr="Петровский бульвар, 6 к2", rating="4,8", reviews=304, link="https://2gis.ru/spb/firm/70000001081145000",
      fonts="Fraunces:ital,wght@0,600;1,600&family=Manrope:wght@400;500;700", hfont="Fraunces", bfont="Manrope", upper=False,
      c=dict(bg="#faf6f2", card="#ffffff", text="#2c2430", muted="#7d7180", acc="#e98aa4", acc2="#8fb3ff", acc3="#ffc66d", line="#eee4e6", leaf="#000"),
      title="Маникюр яркий, как гуашь", sub="Аккуратный маникюр, покрытие и дизайн на Петровском бульваре. Прайс, работы мастеров и запись онлайн в одном месте.",
      cta="Записаться онлайн",
      feats=[("Онлайн-запись", "Мастер, услуга и время за минуту"), ("Галерея дизайнов", "Клиентки выбирают дизайн заранее"), ("Прозрачный прайс", "Все услуги и доплаты списком")],
      services=[("Маникюр", "1 000 ₽"), ("Маникюр + покрытие", "2 000 ₽"), ("Дизайн", "от 100 ₽ / ноготь"), ("Френч", "+ 400 ₽"), ("Педикюр с покрытием", "2 400 ₽"), ("Снятие покрытия", "300 ₽")]),
 dict(slug="ryabina", name="Рябина", kind="Цветочная мастерская", art="flowers",
      addr="Пулковская улица, 10 к2", rating="4,7", reviews=219, link="https://2gis.ru/spb/firm/5348552839674110",
      fonts="Cormorant+Garamond:ital,wght@0,600;1,600&family=Manrope:wght@400;500;700", hfont="Cormorant Garamond", bfont="Manrope", upper=False,
      c=dict(bg="#f7f2ea", card="#fffdf9", text="#2e2a24", muted="#7f7568", acc="#c8442f", acc2="#e98a5b", acc3="#c8442f", line="#e8ddcc", leaf="#5e7b4f"),
      title="Букеты, которые хочется подарить", sub="Цветочная мастерская на Пулковской: авторские букеты, композиции в коробках и доставка по городу. Выбирайте на сайте и заказывайте в мессенджере.",
      cta="Выбрать букет",
      feats=[("Витрина букетов", "Фото и цены, заказ одной кнопкой в WhatsApp"), ("Доставка по городу", "Зоны и стоимость доставки сразу видны"), ("Букет к дате", "Предзаказ к праздникам и напоминания")],
      services=[("Букет комплимент", "от 1 500 ₽"), ("Авторский букет", "от 3 500 ₽"), ("Композиция в коробке", "от 3 000 ₽"), ("Свадебный букет", "от 6 000 ₽"), ("Моно-букет роз", "от 4 000 ₽"), ("Доставка", "от 400 ₽")]),
]

def page(s):
    e = html.escape
    c = s["c"]
    up = "text-transform:uppercase;letter-spacing:.02em;" if s["upper"] else ""
    light = c["bg"].lower() in ("#faf6f2", "#f7f2ea")
    feats = "".join(f'<div class="f"><span>{i+1:02d}</span><h3>{e(t)}</h3><p>{e(d)}</p></div>' for i, (t, d) in enumerate(s["feats"]))
    svc = "".join(f'<div class="row"><b>{e(n)}</b><i></i><span>{e(p)}</span></div>' for n, p in s["services"])
    return f'''<!doctype html>
<html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>{e(s["name"])} · демо-набросок сайта</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family={s["fonts"]}&display=swap" rel="stylesheet">
<style>
:root{{--bg:{c["bg"]};--card:{c["card"]};--text:{c["text"]};--muted:{c["muted"]};--acc:{c["acc"]};--acc2:{c["acc2"]};--acc3:{c["acc3"]};--line:{c["line"]};--leaf:{c["leaf"]}}}
*{{box-sizing:border-box;margin:0;padding:0}}html{{scroll-behavior:smooth}}
body{{background:var(--bg);color:var(--text);font:17px/1.6 "{s["bfont"]}",system-ui,sans-serif}}
a{{color:inherit;text-decoration:none}}.wrap{{max-width:1120px;margin:0 auto;padding:0 20px}}
h1,h2,h3{{font-family:"{s["hfont"]}",serif;line-height:1.1;{up}}}
.demo{{background:var(--acc);color:{"#fff" if light else "#111"};font-size:13px;font-weight:700;text-align:center;padding:9px 16px}}
.demo a{{text-decoration:underline}}
header .wrap{{display:flex;justify-content:space-between;align-items:center;height:76px}}
.logo{{font-family:"{s["hfont"]}";font-size:24px;font-weight:700;{up}}}.logo small{{display:block;font-family:"{s["bfont"]}";font-size:11px;color:var(--muted);text-transform:uppercase;letter-spacing:.2em;font-weight:500}}
nav{{display:flex;gap:26px;color:var(--muted);font-size:15px}}nav a:hover{{color:var(--acc)}}
.btn{{display:inline-block;background:var(--acc);color:{"#fff" if light else "#111"};font-weight:700;padding:15px 28px;border-radius:999px;transition:.2s}}
.btn:hover{{transform:translateY(-2px);box-shadow:0 12px 30px color-mix(in srgb,var(--acc) 40%,transparent)}}
.btn.ghost{{background:transparent;color:var(--text);box-shadow:inset 0 0 0 1.5px var(--line)}}
.hero .wrap{{display:grid;grid-template-columns:1.15fr .85fr;gap:40px;align-items:center;padding-top:40px;padding-bottom:90px}}
.kind{{color:var(--acc);font-weight:700;font-size:13px;letter-spacing:.2em;text-transform:uppercase;margin-bottom:16px}}
.hero h1{{font-size:clamp(40px,6.4vw,78px)}}
.hero p{{color:var(--muted);font-size:19px;max-width:520px;margin:22px 0 32px}}
.btns{{display:flex;gap:12px;flex-wrap:wrap}}
.rate{{display:inline-flex;align-items:center;gap:12px;margin-top:34px;padding:10px 16px;border:1px solid var(--line);border-radius:16px;background:var(--card)}}
.rate b{{font-size:26px;font-family:"{s["hfont"]}"}}.rate span{{color:var(--muted);font-size:14px;line-height:1.3}}.stars{{color:#f5b301;letter-spacing:2px}}
.art{{width:100%;max-width:420px;justify-self:center;filter:drop-shadow(0 30px 60px rgba(0,0,0,.25))}}
.spin{{animation:spin 14s linear infinite}}@keyframes spin{{to{{transform:rotate(360deg)}}}}
section{{padding:90px 0}}.sh{{margin-bottom:40px}}.sh h2{{font-size:clamp(32px,4.6vw,52px)}}.sh p{{color:var(--muted);margin-top:10px;max-width:560px}}
.feats{{display:grid;grid-template-columns:repeat(3,1fr);gap:20px}}
.f{{background:var(--card);border:1px solid var(--line);border-radius:24px;padding:30px;transition:.25s}}.f:hover{{border-color:var(--acc);transform:translateY(-4px)}}
.f span{{font-family:"{s["hfont"]}";font-size:34px;color:var(--acc)}}.f h3{{font-size:21px;margin:12px 0 6px}}.f p{{color:var(--muted);font-size:15px}}
.price{{background:var(--card);border-block:1px solid var(--line)}}
.rows{{display:grid;grid-template-columns:1fr 1fr;gap:0 60px}}
.row{{display:flex;align-items:baseline;gap:12px;padding:18px 0;border-bottom:1px solid var(--line)}}.row b{{font-weight:500}}
.row i{{flex:1;border-bottom:1px dotted var(--muted);opacity:.5;transform:translateY(-5px)}}.row span{{font-weight:700;color:var(--acc);white-space:nowrap}}
.note{{color:var(--muted);font-size:14px;margin-top:22px}}
.find .wrap{{display:grid;grid-template-columns:1fr 1fr;gap:28px}}
.card{{background:var(--card);border:1px solid var(--line);border-radius:28px;padding:40px}}
.card h2{{font-size:clamp(28px,4vw,42px);margin-bottom:18px}}.card p{{color:var(--muted);margin-bottom:10px}}.card p b{{color:var(--text)}}
.big{{display:flex;flex-direction:column;justify-content:center;align-items:flex-start;background:linear-gradient(135deg,var(--acc),var(--acc2));color:{"#fff" if light else "#111"};border:0}}
.big .n{{font-family:"{s["hfont"]}";font-size:84px;line-height:1}}.big p{{color:inherit;opacity:.85}}.big a{{margin-top:20px;font-weight:700;text-decoration:underline}}
footer{{padding:36px 0;color:var(--muted);font-size:14px}}footer .wrap{{display:flex;justify-content:space-between;gap:12px;flex-wrap:wrap}}footer a{{color:var(--acc);font-weight:700}}
@media(max-width:860px){{nav{{display:none}}.hero .wrap,.find .wrap{{grid-template-columns:1fr}}.art{{max-width:280px;order:-1}}.feats,.rows{{grid-template-columns:1fr}}section{{padding:64px 0}}.card{{padding:28px}}}}
</style></head><body>
<div class="demo">Демо-набросок сайта для «{e(s["name"])}». Это не официальный сайт: пример того, как он может выглядеть. Автор: <a href="{PORTFOLIO}">Александр</a></div>
<header><div class="wrap"><a href="#" class="logo">{e(s["name"])}<small>{e(s["kind"])}</small></a>
<nav><a href="#about">О нас</a><a href="#price">Цены</a><a href="#find">Контакты</a></nav>
<a href="#find" class="btn" style="padding:10px 20px;font-size:14px">{e(s["cta"])}</a></div></header>
<section class="hero" style="padding:0"><div class="wrap"><div>
<div class="kind">{e(s["kind"])} · Санкт-Петербург</div>
<h1>{e(s["title"])}</h1><p>{e(s["sub"])}</p>
<div class="btns"><a href="#find" class="btn">{e(s["cta"])}</a><a href="#price" class="btn ghost">Смотреть цены</a></div>
<div class="rate"><b>{s["rating"]}</b><span><span class="stars">★★★★★</span><br>{s["reviews"]} отзывов в 2ГИС</span></div>
</div>{ART[s["art"]]}</div></section>
<section id="about"><div class="wrap"><div class="sh"><h2>Что будет на сайте</h2><p>Всё, чтобы новый клиент нашёл вас в поиске, понял цены и сразу записался.</p></div>
<div class="feats">{feats}</div></div></section>
<section class="price" id="price"><div class="wrap"><div class="sh"><h2>Цены</h2></div><div class="rows">{svc}</div>
<p class="note">Цены здесь для примера. На настоящем сайте будут ваши услуги и ваш прайс.</p></div></section>
<section class="find" id="find"><div class="wrap">
<div class="card"><h2>Как нас найти</h2><p><b>Адрес:</b> {e(s["addr"])}</p><p><b>Телефон и мессенджеры:</b> кнопки WhatsApp, Telegram и звонка</p><p><b>Часы работы:</b> из вашей карточки</p>
<a href="{s["link"]}" class="btn" style="margin-top:14px" target="_blank" rel="noopener">Открыть в 2ГИС</a></div>
<div class="card big"><div class="n">{s["rating"]}</div><p>средняя оценка по {s["reviews"]} отзывам в 2ГИС</p><p>На сайте покажем ваши настоящие отзывы и обновим их автоматически.</p></div>
</div></section>
<footer><div class="wrap"><span>Демо-набросок для «{e(s["name"])}». Не является официальным сайтом.</span><span>Сделал <a href="{PORTFOLIO}">Александр</a> · сайты за 3-5 дней</span></div></footer>
</body></html>'''

if __name__ == "__main__":
    for s in SITES:
        d = os.path.join(HERE, s["slug"]); os.makedirs(d, exist_ok=True)
        open(os.path.join(d, "index.html"), "w", encoding="utf-8").write(page(s))
        print("ok", s["slug"])
