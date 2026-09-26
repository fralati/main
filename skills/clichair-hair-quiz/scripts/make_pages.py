#!/usr/bin/env python3
"""Crea le pagine di prova del quiz. Uso: python3 make_pages.py <file.liquid> <cartella>
Pagine: it/en/de/fr.html (sfondo chiaro, icona Zipchat finta), dark.html, nobubble.html (senza chat)."""
import os, re, sys
src, out = sys.argv[1], sys.argv[2]
os.makedirs(out, exist_ok=True)
s = open(src, encoding='utf-8').read()
body = re.sub(r'\{%-?\s*comment\s*-?%\}.*?\{%-?\s*endcomment\s*-?%\}\n?', '', s, flags=re.S)
body = re.sub(r'\{%-.*?-%\}\n?', '', body)
assert '{%' not in body, 'tag Liquid non gestito'
BUB = ('<img id="bubble-icon" data-zipchat="bubble-icon" alt="" onclick="window.__zc=(window.__zc||0)+1" '
       'style="position:fixed;left:12px;bottom:12px;width:44px;height:44px;background:#333;border-radius:50%">')
def page(lang, sec, bubble=True):
    return ('<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
            '<style>body{margin:0;font-family:Inter,system-ui,sans-serif}header{height:70px;background:#fff;border-bottom:1px solid #ddd}'
            '.sec{' + sec + ';padding:30px 5vw;display:flex;flex-direction:column;align-items:flex-start}</style></head>'
            '<body><header></header><div class="sec"><div>\n' + body.replace('{{ cq_lang }}', lang) +
            '\n</div></div><div style="height:600px"></div>' + (BUB if bubble else '') + '</body></html>')
light = '--color-foreground:#1a1a1a;--color-background:#f4f4f4;background:#f4f4f4;color:#1a1a1a'
dark = '--color-foreground:#f2f2f2;--color-background:#1f1f1f;background:#1f1f1f;color:#f2f2f2'
for l in ['it', 'en', 'de', 'fr']:
    open(os.path.join(out, l + '.html'), 'w', encoding='utf-8').write(page(l, light))
open(os.path.join(out, 'dark.html'), 'w', encoding='utf-8').write(page('it', dark))
open(os.path.join(out, 'nobubble.html'), 'w', encoding='utf-8').write(page('it', light, False))
print('pagine create in', out)
