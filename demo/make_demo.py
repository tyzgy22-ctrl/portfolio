"""Демо-наброски сайтов по данным Яндекс Карт (16.11.2026).
Каждой компании свой стиль (палитра, шрифты, раскладка первого экрана),
только реальные фото из карточки, реальные цены и отзывы.
Запуск: python make_demo.py [slug ...]
"""
import os, sys, html, json
from PIL import Image

ROOT = os.path.dirname(os.path.abspath(__file__))
TG = "staryi_kok"

def esc(s): return html.escape(s, quote=True)

def prep_images(slug, hero, gallery, about):
    raw = os.path.join(ROOT, slug, "img", "raw")
    out = os.path.join(ROOT, slug, "img")
    names = {}
    for role, files in (("hero", [hero]), ("about", about), ("g", gallery)):
        for i, f in enumerate(files):
            src = os.path.join(raw, f + ".jpg")
            im = Image.open(src).convert("RGB")
            im.thumbnail((1800 if role == "hero" else 1100,) * 2)
            name = f"{role}{i}.jpg" if role != "hero" else "hero.jpg"
            im.save(os.path.join(out, name), quality=82, optimize=True, progressive=True)
            names.setdefault(role, []).append(name)
    return names

def prep_logo(slug, logo):
    if not logo: return False
    im = Image.open(os.path.join(ROOT, slug, "img", "raw", logo + ".jpg")).convert("RGB")
    w, h = im.size; s = min(w, h)
    im = im.crop(((w - s) // 2, (h - s) // 2, (w + s) // 2, (h + s) // 2)).resize((160, 160))
    im.save(os.path.join(ROOT, slug, "img", "logo.jpg"), quality=88)
    return True

FONTS = {
    "mustache": "family=Marck+Script&family=Manrope:wght@400;500;600;700;800",
    "street": "family=Russo+One&family=Manrope:wght@400;500;600;700",
    "loft": "family=Old+Standard+TT:ital,wght@0,400;0,700;1,400&family=Manrope:wght@400;500;600;700",
    "elegant": "family=Playfair+Display:ital,wght@0,500;0,600;1,500&family=Montserrat:wght@400;500;600",
    "soft": "family=Comfortaa:wght@500;700&family=Nunito:wght@400;600;700;800",
}

def page(d, imgs):
    s = d["style"]
    phone_href = "tel:" + "".join(c for c in d["phone"] if c.isdigit() or c == "+")
    wa = "https://wa.me/" + "".join(c for c in d["phone"] if c.isdigit())
    price_html = ""
    for group, items in d["prices"]:
        rows = "".join(f'<li><span>{esc(n)}</span><i></i><b>{esc(p)}</b></li>' for n, p in items)
        price_html += f'<div class="pg"><h3>{esc(group)}</h3><ul>{rows}</ul></div>'
    gal = "".join(f'<figure class="gi gi{i%5}"><img loading="lazy" src="img/{n}" alt=""></figure>' for i, n in enumerate(imgs["g"]))
    revs = "".join(f'<blockquote><p>{esc(t)}</p><cite>{esc(a)} · Яндекс Карты</cite></blockquote>' for a, t in d["reviews"])
    about_imgs = "".join(f'<img loading="lazy" src="img/{n}" alt="">' for n in imgs.get("about", []))
    perks = "".join(f"<span>{esc(p)}</span>" for p in d["perks"])
    hero_cls = d.get("hero_layout", "full")
    return f"""<!doctype html>
<html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>{esc(d['name'])} · {esc(d['area'])} · демо</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?{FONTS[s]}&display=swap" rel="stylesheet">
<style>
:root{{{d['vars']}}}
*{{box-sizing:border-box;margin:0;padding:0}}html{{scroll-behavior:smooth}}
body{{background:var(--bg);color:var(--text);font:16px/1.65 var(--fb),system-ui,sans-serif;-webkit-font-smoothing:antialiased}}
img{{display:block;max-width:100%}}a{{color:inherit;text-decoration:none}}
.w{{max-width:1180px;margin:0 auto;padding:0 20px}}
.demo{{background:#000;color:#aaa;font:12px/1.4 system-ui,sans-serif;text-align:center;padding:7px 12px}}.demo a{{color:#fff;text-decoration:underline}}
h1,h2,h3,.logo b{{font-family:var(--fh);font-weight:var(--fhw);line-height:1.04;letter-spacing:var(--fhls)}}
header{{position:absolute;left:0;right:0;z-index:5}}
header .w{{display:flex;align-items:center;justify-content:space-between;height:84px;gap:20px}}
.logo{{display:flex;align-items:center;gap:12px;color:var(--htext)}}.logo img{{width:46px;height:46px;border-radius:50%;object-fit:cover;background:#fff}}
.logo b{{font-size:24px}}.logo small{{display:block;font:600 10px/1.2 var(--fb);letter-spacing:.28em;text-transform:uppercase;opacity:.7;margin-top:3px}}
nav{{display:flex;gap:26px;font-size:14px;font-weight:600;color:var(--htext)}}nav a{{opacity:.85}}nav a:hover{{opacity:1;color:var(--acc)}}
.hph{{color:var(--htext);font-weight:700;font-size:15px;white-space:nowrap}}
.btn{{display:inline-flex;align-items:center;justify-content:center;gap:10px;font:700 14px/1 var(--fb);letter-spacing:.08em;text-transform:uppercase;padding:18px 28px;background:var(--acc);color:var(--acctext);border-radius:var(--r);transition:transform .2s,filter .2s}}
.btn:hover{{transform:translateY(-2px);filter:brightness(1.08)}}.btn.ghost{{background:transparent;color:var(--htext);box-shadow:inset 0 0 0 1.5px currentColor}}
.hero{{position:relative;min-height:min(100svh,940px);display:flex;align-items:flex-end;color:var(--htext);overflow:hidden}}
.hero>img{{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:{d.get('hero_pos','center')}}}
.hero:after{{content:"";position:absolute;inset:0;background:var(--shade)}}
.hero .w{{position:relative;z-index:2;padding-top:140px;padding-bottom:70px;width:100%}}
.kicker{{font-weight:700;font-size:12px;letter-spacing:.3em;text-transform:uppercase;color:var(--acc);margin-bottom:18px}}
.hero h1{{font-size:clamp(46px,8.4vw,118px);max-width:960px}}.hero h1 em{{font-style:normal;color:var(--acc)}}
.hero p.lead{{max-width:560px;font-size:18px;margin:22px 0 32px;opacity:.9}}
.btns{{display:flex;gap:12px;flex-wrap:wrap}}
.facts{{display:flex;gap:36px;flex-wrap:wrap;margin-top:44px;padding-top:24px;border-top:1px solid rgba(255,255,255,.22)}}
.facts b{{display:block;font-family:var(--fh);font-size:40px;line-height:1;color:var(--acc)}}.facts span{{font-size:13px;opacity:.8}}
.split .hero{{align-items:center}}
@media(min-width:900px){{.split .hero>img{{left:46%;width:54%}}.split .hero:after{{background:linear-gradient(90deg,var(--bg2) 46%,rgba(0,0,0,0) 46%)}}.split .hero h1{{max-width:560px}}.split .hero .w>div{{max-width:520px}}}}
section{{padding:100px 0}}
.label{{font-weight:700;font-size:12px;letter-spacing:.3em;text-transform:uppercase;color:var(--acc);margin-bottom:14px}}
h2{{font-size:clamp(38px,5.4vw,68px);margin-bottom:18px}}
.sub{{color:var(--muted);max-width:620px;font-size:17px}}
.about .w{{display:grid;grid-template-columns:1fr 1fr;gap:64px;align-items:center}}
.about .pics{{display:grid;grid-template-columns:1fr 1fr;gap:12px}}.about .pics img{{width:100%;aspect-ratio:3/4;object-fit:cover;border-radius:var(--r)}}.about .pics img:nth-child(2){{margin-top:48px}}
.about p{{margin-top:16px;color:var(--muted);font-size:17px}}
.chips{{display:flex;flex-wrap:wrap;gap:8px;margin-top:26px}}.chips span{{border:1px solid var(--line);padding:8px 14px;font-size:13px;font-weight:600;border-radius:999px}}
.prices,.contact{{background:var(--bg2);color:var(--on2,var(--text))}}
.prices .sub,.prices .pnote,.contact dt{{color:var(--on2m,var(--muted))}}.pg{{color:var(--text)}}
.contact .btn.ghost{{color:inherit!important}}
.split .hero h1{{font-size:clamp(44px,5.8vw,86px)}}
.pgrid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(320px,1fr));gap:22px;margin-top:44px}}
.pg{{background:var(--card);border:1px solid var(--line);padding:30px 28px;border-radius:var(--r)}}
.pg h3{{font-size:26px;margin-bottom:18px;color:var(--acc2)}}
.pg li{{list-style:none;display:flex;align-items:baseline;gap:10px;padding:10px 0;border-bottom:1px dashed var(--line)}}.pg li:last-child{{border:0}}
.pg li span{{flex:0 1 auto}}.pg li i{{flex:1}}.pg li b{{white-space:nowrap;font-weight:800}}
.pnote{{margin-top:20px;font-size:14px;color:var(--muted)}}
.gal{{display:grid;grid-template-columns:repeat(4,1fr);grid-auto-rows:240px;gap:10px;margin-top:40px}}
.gi{{overflow:hidden;border-radius:var(--r)}}.gi img{{width:100%;height:100%;object-fit:cover;transition:transform .6s}}.gi:hover img{{transform:scale(1.05)}}
.gi0{{grid-row:span 2}}.gi3{{grid-column:span 2}}
.revs{{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:20px;margin-top:40px}}
blockquote{{background:var(--card);border:1px solid var(--line);border-radius:var(--r);padding:30px 28px;display:flex;flex-direction:column;justify-content:space-between;gap:22px}}
blockquote p{{font-size:16px}}blockquote p:before{{content:"★★★★★";display:block;color:var(--acc);letter-spacing:.2em;margin-bottom:12px;font-size:14px}}
cite{{font-style:normal;font-size:13px;font-weight:700;color:var(--muted)}}
.contact .w{{display:grid;grid-template-columns:.9fr 1.1fr;gap:50px;align-items:stretch}}
.cinfo dl{{margin:28px 0 34px}}.cinfo dt{{font-size:12px;letter-spacing:.2em;text-transform:uppercase;color:var(--muted);margin-top:18px}}.cinfo dd{{font-size:20px;font-weight:700}}
.map{{min-height:420px;border-radius:var(--r);overflow:hidden;border:1px solid var(--line)}}.map iframe{{width:100%;height:100%;min-height:420px;border:0;display:block}}
footer{{padding:34px 0 100px;font-size:13px;color:var(--muted);text-align:center}}
.mcta{{display:none}}
@media(max-width:860px){{nav,.hph{{display:none}}.about .w,.contact .w{{grid-template-columns:1fr}}
.gal{{grid-template-columns:1fr 1fr;grid-auto-rows:180px}}.gi3{{grid-column:span 1}}section{{padding:72px 0}}
.mcta{{display:flex;position:fixed;left:12px;right:12px;bottom:12px;z-index:20;gap:8px}}.mcta a{{flex:1;padding:16px 10px}}
.facts{{gap:22px}}.facts b{{font-size:32px}}}}
</style></head>
<body class="{hero_cls}">
<div class="demo">Демо-набросок сайта для «{esc(d['name'])}» по данным Яндекс Карт · сделал Александр, <a href="https://t.me/{TG}">Telegram</a></div>
<header><div class="w">
<a class="logo" href="#">{'<img src="img/logo.jpg" alt="">' if d.get('logo') else ''}<span><b>{esc(d['name'])}</b><small>{esc(d['tag'])}</small></span></a>
<nav><a href="#about">О нас</a><a href="#prices">Цены</a><a href="#works">Работы</a><a href="#reviews">Отзывы</a><a href="#contacts">Контакты</a></nav>
<a class="hph" href="{phone_href}">{esc(d['phone'])}</a>
</div></header>
<section class="hero" style="padding:0"><img src="img/hero.jpg" alt="">
<div class="w"><div>
<div class="kicker">{esc(d['kicker'])}</div>
<h1>{d['h1']}</h1>
<p class="lead">{esc(d['lead'])}</p>
<div class="btns"><a class="btn" href="{phone_href}">Записаться</a><a class="btn ghost" href="#prices">Цены</a></div>
<div class="facts">{''.join(f'<div><b>{esc(a)}</b><span>{esc(b)}</span></div>' for a,b in d['facts'])}</div>
</div></div></section>
<section class="about" id="about"><div class="w">
<div><div class="label">{esc(d['about_label'])}</div><h2>{d['about_h']}</h2>{''.join(f'<p>{esc(p)}</p>' for p in d['about'])}<div class="chips">{perks}</div></div>
<div class="pics">{about_imgs}</div>
</div></section>
<section class="prices" id="prices"><div class="w">
<div class="label">Прайс</div><h2>Услуги и цены</h2><p class="sub">{esc(d['price_sub'])}</p>
<div class="pgrid">{price_html}</div><p class="pnote">Цены из карточки на Яндекс Картах, точную стоимость уточняйте при записи.</p>
</div></section>
<section id="works"><div class="w">
<div class="label">Работы и интерьер</div><h2>{d['gal_h']}</h2><p class="sub">Фото из карточки на Яндекс Картах.</p>
<div class="gal">{gal}</div>
</div></section>
<section id="reviews" style="padding-top:0"><div class="w">
<div class="label">Отзывы</div><h2>{esc(d['rating'])} на Яндекс Картах</h2><p class="sub">{esc(d['rev_sub'])}</p>
<div class="revs">{revs}</div>
</div></section>
<section class="contact" id="contacts"><div class="w">
<div class="cinfo"><div class="label">Контакты</div><h2>Ждём вас</h2>
<dl><dt>Адрес</dt><dd>{esc(d['address'])}</dd><dt>Телефон</dt><dd><a href="{phone_href}">{esc(d['phone'])}</a></dd>{''.join(f'<dt>{esc(a)}</dt><dd>{esc(b)}</dd>' for a,b in d.get('extra',[]))}</dl>
<div class="btns"><a class="btn" href="{phone_href}">Позвонить</a><a class="btn ghost" style="color:var(--text)" href="{wa}">WhatsApp</a></div></div>
<div class="map"><iframe loading="lazy" src="https://yandex.ru/map-widget/v1/?oid={d['oid']}&z=16" title="Карта"></iframe></div>
</div></section>
<footer>© {esc(d['name'])} · {esc(d['address'])}<br>Демо-набросок, не официальный сайт.</footer>
<div class="mcta"><a class="btn" href="{phone_href}">Записаться</a><a class="btn" style="background:#25D366;color:#fff" href="{wa}">WhatsApp</a></div>
</body></html>"""

DATA = json.load(open(os.path.join(ROOT, "demo_data.json"), encoding="utf-8"))

if __name__ == "__main__":
    for d in DATA:
        if len(sys.argv) > 1 and d["slug"] not in sys.argv[1:]:
            continue
        imgs = prep_images(d["slug"], d["hero"], d["gallery"], d["about_imgs"])
        prep_logo(d["slug"], d.get("logo"))
        open(os.path.join(ROOT, d["slug"], "index.html"), "w", encoding="utf-8").write(page(d, imgs))
        print("ok", d["slug"])
