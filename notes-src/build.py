#!/usr/bin/env python3
# builds the patch notes pages from notes.json and roadmap.html from roadmap.json
# add an entry to notes.json (newest first), run: python3 notes-src/build.py
# also sets the version shown on every page and the download links in js/site.js to the newest entry
# (only push once the installers are mirrored, or the download buttons 404)
import json, html, datetime, pathlib, re

ROOT = pathlib.Path(__file__).resolve().parent.parent
D = json.loads((pathlib.Path(__file__).parent / 'notes.json').read_text())
ORDER = ['kue', 'vyz', 'mapp', 'rakk', 'dekk', 'kode', 'lynk', 'konv']
LIVE = {p.stem for p in ROOT.glob('*.html')}  # apps that have a product page

# header + footer straight from an existing page so they stay in step
tpl = (ROOT / 'vyz.html').read_text()
HEAD_END = tpl.index('<main id="main">')
FOOT_START = tpl.index('</main>')
head, foot = tpl[:HEAD_END], tpl[FOOT_START:]

e = html.escape

def prod(app):
    return f'<span class="prod"><span class="kn">KYNETYK</span><span class="pn">{app}</span></span>'

def when(d):
    t = datetime.date.fromisoformat(d)
    return f'<time datetime="{d}">{t.day} {t:%b %Y}</time>'

def tag(t):
    return f'<span class="ntag {t}">{e(D["labels"][t][0])}</span>'

def page(title, desc, body):
    h = re.sub(r'<title>.*?</title>', f'<title>{e(title)}</title>', head, count=1)
    h = re.sub(r'<meta name="description" content=".*?">', f'<meta name="description" content="{e(desc)}">', h, count=1)
    return h + '<main id="main">\n' + body + '\n  ' + foot

def legend():
    return '<dl class="nlegend">' + ''.join(f'<div>{tag(k)}<dd>{e(v[1])}</dd></div>' for k, v in D['labels'].items()) + '</dl>'

def entry(app, x, link=False):
    items = ''.join(f'<li>{e(i)}</li>' for i in x['items'])
    head = f'<div class="nhead"><span class="dot nver">v{e(x["v"])}</span>{tag(x["type"])}{when(x["date"])}</div>'
    if link:
        head = f'<div class="nhead">{prod(app)}<span class="dot nver">v{e(x["v"])}</span>{tag(x["type"])}{when(x["date"])}</div>'
    return f'<article class="note reveal" id="v{e(x["v"])}">{head}<h3>{e(x["title"])}</h3><ul>{items}</ul></article>'

for app in ORDER:
    a = D['apps'][app]
    back = f'<a href="{app}.html">{app} home</a> · ' if app in LIVE else ''
    body = f'''    <section class="wrap nhero">
      <span class="intro">{prod(app)}</span>
      <h1 class="intro">Patch notes</h1>
      <p class="lede intro i2">Every {app} release, newest first. {back}<a href="patch-notes.html">All apps</a></p>
    </section>
    <section class="wrap nlist">
      {''.join(entry(app, x) for x in a['entries'])}
    </section>
    <section class="band"><div class="wrap section-pad stack"><h2 style="font-size: clamp(22px, 2.4vw, 28px)">What the labels mean</h2>{legend()}</div></section>'''
    (ROOT / f'{app}-patch-notes.html').write_text(page(f'KYNETYK {app}: patch notes', f'Every release of KYNETYK {app}, newest first.', body))

latest = sorted(((x['date'], ORDER.index(app), app, x) for app in ORDER for x in D['apps'][app]['entries']), key=lambda r: (r[0], -r[1]), reverse=True)[:6]
cards = ''.join(f'''<a class="ncard" href="{app}-patch-notes.html">{prod(app)}<span class="dim">{e(D["apps"][app]["what"])}</span><span class="nhead"><span class="dot nver">v{e(D["apps"][app]["entries"][0]["v"])}</span>{tag(D["apps"][app]["entries"][0]["type"])}</span><span class="dim small">{when(D["apps"][app]["entries"][0]["date"])}</span></a>''' for app in ORDER)
body = f'''    <section class="wrap nhero">
      <h1 class="intro">Patch notes</h1>
      <p class="lede intro i2">What's new in every KYNETYK app: big updates, small ones, bug fixes and hotfixes.</p>
      {legend()}
    </section>
    <section class="wrap nlist">
      <h2>Latest</h2>
      {''.join(entry(app, x, True) for _, _, app, x in latest)}
    </section>
    <section class="band"><div class="wrap section-pad stack"><h2 style="font-size: clamp(22px, 2.4vw, 28px)">By app</h2><div class="ncards">{cards}</div></div></section>'''
(ROOT / 'patch-notes.html').write_text(page('KYNETYK: patch notes', 'What is new in every KYNETYK app.', body))

# roadmap
R = json.loads((pathlib.Path(__file__).parent / 'roadmap.json').read_text())
def chipicons(apps):
    return ''.join(f'<a class="rapp" href="{a}.html"><img src="media/icons/{a}.png" alt="" width="20" height="20"><span class="dot">{a}</span></a>' for a in apps) or '<span class="dim small">Every app</span>'
cols = ''
for c in R['columns']:
    items = ''.join(f'<article class="ritem"><div class="ricons">{chipicons(i["apps"])}</div><h3>{e(i["title"])}</h3><p>{e(i["text"])}</p></article>' for i in R['items'] if i['col'] == c['id'])
    cols += f'<section class="rcol {c["id"]}"><h2>{e(c["name"])}</h2><p class="dim small">{e(c["note"])}</p><div class="ritems">{items}</div></section>'
body = (
    '    <section class="wrap nhero">\n'
    '      <h1 class="intro">Roadmap</h1>\n'
    '      <p class="lede intro i2">What\'s just landed, what\'s next and what\'s planned for the KYNETYK apps. Plans can change; the <a href="patch-notes.html">patch notes</a> have everything that\'s actually out.</p>\n'
    '    </section>\n'
    f'    <section class="wrap rmap">{cols}</section>\n'
    '    <section class="band"><div class="wrap section-pad stack"><h2 style="font-size: clamp(22px, 2.4vw, 28px)">Something missing?</h2><p class="lede">Requests from people using the apps on real shows shape what gets built next. Leave a message on the <a href="https://ko-fi.com/ritualsyntax" target="_blank" rel="noopener">Ko-fi page</a>.</p></div></section>'
)
(ROOT / 'roadmap.html').write_text(page('KYNETYK: roadmap', 'What is next for the KYNETYK apps.', body))

# versions everywhere = newest entry
newest = {app: D['apps'][app]['entries'][0]['v'] for app in ORDER}
for p in ROOT.glob('*.html'):
    t = p.read_text()
    n = re.sub(r'data-text="(\w+)\.version">[^<]*<', lambda m: f'data-text="{m.group(1)}.version">{newest.get(m.group(1), m.group(0))}<' if m.group(1) in newest else m.group(0), t)
    if n != t: p.write_text(n)
js = ROOT / 'js' / 'site.js'
t = js.read_text()
n = re.sub(r"rel\('(\w+)', '[^']*'\)", lambda m: f"rel('{m.group(1)}', '{newest[m.group(1)]}')" if m.group(1) in newest else m.group(0), t)
if n != t: js.write_text(n)
print('built', len(ORDER) + 1, 'pages, versions:', ' '.join(f'{a} {v}' for a, v in newest.items()))
