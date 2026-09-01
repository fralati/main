#!/usr/bin/env python3
"""
Genera related_products per le shade colore di cliCHair.

Logica (naturale per un colorista):
  A) stesso riflesso, livelli adiacenti  -> "stessa tonalita', piu' chiara / piu' scura"  (max 3)
  B) stesso livello, riflessi vicini     -> "stessa profondita', tonalita' diverse"       (max 3)
Totale max 6, sempre dentro la stessa linea, solo prodotti ACTIVE, mai charts.

Codice shade: cifra prima del punto = livello, cifre dopo = riflesso
(0 naturale, 1 cenere, 2 viola/iride, 3 dorato, 4 rame, 5 mogano, 6 rosso,
 7 tabacco/marrone, 8 beige/perla, 9 blu/freddo).
"""
import re, json, sys
from collections import defaultdict

SRC = "catalog/data/shades-active.tsv"

# riflesso primario -> famiglia
FAMILY = {"1": "cool", "2": "cool", "9": "cool",
          "3": "warm-light", "8": "warm-light",
          "4": "warm-deep", "5": "warm-deep", "6": "warm-deep",
          "0": "neutral", "7": "neutral"}

# distanza fra famiglie (neutral e' vicino a tutto)
def fam_dist(a, b):
    if a == b: return 0
    if "neutral" in (a, b): return 1
    if {a, b} == {"warm-light", "warm-deep"}: return 1
    return 2

# casi che non seguono la notazione livello.riflesso: mappati sul loro equivalente
SPECIAL = {
    "Grace Color 100 Extra Lift":      (11, "0"),
    "Grace Color Silver":              (11, "1"),
    "Grace Color Pearl Rose":          (11, "2"),
    "Grace Color 1B Blue Black":       (1,  "9"),
    "Vibrant Color 01 Toner Ash":      (11, "1"),
    "Vibrant Color 09 Toner Blue":     (11, "9"),
    "Vibrant Color .COM19 Agate":      (11, "2"),
}

# Gems: shade fashion, non seguono la scala livelli -> famiglie cromatiche esplicite
GEMS_FAMILY = {
    "Gems 01 Platinum": "cool", "Gems 11 Pearl Grey": "cool", "Gems 118 Graphite": "cool",
    "Gems 18 Iron": "cool", "Gems 23 Champagne": "cool",
    "Gems 02 Lavender": "violet", "Gems 22 Intense Violet": "violet", "Gems 12 Dark Mauve": "violet",
    "Gems 036 Peach": "pink", "Gems 060 Coral Pink": "pink", "Gems 52 Magenta": "pink",
    "Gems 62 Fuchsia": "pink",
    "Gems 44 Intense Copper": "warm", "Gems 66 Intense Red": "warm",
    "Gems 3 Very Light Golden Blonde": "warm",
    "Gems 7 Moka": "brown", "Gems 75 Cocoa": "brown",
    "Gems 81 Black": "dark", "Gems 88 Blue": "dark",
    "Gems C Clear": "neutral",
}
GEMS_NEAR = {
    "cool": ["violet", "neutral"], "violet": ["cool", "pink"], "pink": ["violet", "warm"],
    "warm": ["pink", "brown"], "brown": ["warm", "dark"], "dark": ["brown", "cool"],
    "neutral": ["cool", "violet", "pink", "warm", "brown", "dark"],
}

CHART = "Chart"
MAX_A, MAX_B, MAX_TOTAL = 3, 3, 6


def line_of(title):
    if title.startswith("Gems"): return "Gems"
    if title.startswith("Grace"): return "Grace"
    if title.startswith("Vibrant"): return "Vibrant"
    if title.startswith("Pure Pigment"): return "PurePigment"
    if title.startswith("Liquid Pigment"): return "LiquidPigment"
    return "?"


def parse_code(title):
    """-> (livello:int, riflesso_primario:str, riflesso_pieno:str) oppure None"""
    if title in SPECIAL:
        lvl, refl = SPECIAL[title]
        return lvl, refl, refl
    m = re.search(r"\b(\d{1,3})\.(\+|\d{1,2})(?![\d.])", title)
    if not m:
        return None
    lvl = int(m.group(1))
    refl = m.group(2)
    if refl == "+":            # shade "intense": naturale rinforzato
        primary, full = "0", "+"
    else:
        primary, full = refl[0], refl
    if lvl == 90: lvl = 11     # superbleaching: sopra il 10
    if lvl == 100: lvl = 11
    return lvl, primary, full


def load():
    rows = []
    for ln in open(SRC):
        ln = ln.rstrip("\n")
        if not ln: continue
        pid, title = ln.split("\t", 1)
        rows.append({"id": pid, "title": title, "line": line_of(title),
                     "chart": CHART in title, "code": parse_code(title)})
    return rows


def related_for(p, rows):
    line, pid = p["line"], p["id"]

    if p["chart"]:                      # una cartella colore si confronta con le altre cartelle
        return [q["id"] for q in rows if q["chart"] and q["id"] != pid]

    if line == "PurePigment":           # i pigmenti puri sono alternative fra loro
        return [q["id"] for q in rows if q["line"] == "PurePigment" and q["id"] != pid]

    if line == "LiquidPigment":         # toner anti-giallo NIKA -> shade fredde Grace
        want = ["Grace Color Silver", "Grace Color 10.11", "Grace Color 9.11", "Grace Color Pearl Rose"]
        out = []
        for w in want:
            out += [q["id"] for q in rows if q["title"].startswith(w)]
        return out[:MAX_TOTAL]

    if line == "Gems":
        fam = GEMS_FAMILY.get(p["title"])
        if not fam: return []
        same = [q for q in rows if q["line"] == "Gems" and not q["chart"] and q["id"] != pid]
        near = GEMS_NEAR[fam]
        same.sort(key=lambda q: (0 if GEMS_FAMILY.get(q["title"]) == fam
                                 else (1 + near.index(GEMS_FAMILY.get(q["title"], "neutral"))
                                       if GEMS_FAMILY.get(q["title"], "neutral") in near else 9),
                                 q["title"]))
        return [q["id"] for q in same[:MAX_TOTAL]]

    if not p["code"]: return []
    lvl, primary, full = p["code"]
    pool = [q for q in rows if q["line"] == line and not q["chart"]
            and q["id"] != pid and q["code"]]

    # A) stesso riflesso, livello piu' vicino
    a = [q for q in pool if q["code"][1] == primary]
    a.sort(key=lambda q: (abs(q["code"][0] - lvl),
                          0 if q["code"][2] == full else 1,
                          q["code"][0]))
    a = [q for q in a if q["code"][0] != lvl][:MAX_A]

    # B) stesso livello, riflesso vicino
    b = [q for q in pool if q["code"][0] == lvl and q["code"][1] != primary]
    b.sort(key=lambda q: (fam_dist(FAMILY.get(primary, "neutral"),
                                   FAMILY.get(q["code"][1], "neutral")),
                          abs(int(q["code"][1]) - int(primary)) if primary.isdigit()
                          and q["code"][1].isdigit() else 9,
                          q["title"]))
    b = b[:MAX_B]

    out, seen = [], set()
    for q in a + b:
        if q["id"] not in seen:
            seen.add(q["id"]); out.append(q["id"])
    if len(out) < 4:                    # riempi con lo stesso livello, poi livelli vicini
        for q in sorted(pool, key=lambda q: (abs(q["code"][0] - lvl), q["title"])):
            if q["id"] not in seen:
                seen.add(q["id"]); out.append(q["id"])
            if len(out) >= 4: break
    return out[:MAX_TOTAL]


def main():
    rows = load()
    by_id = {r["id"]: r for r in rows}
    plan, empty = {}, []
    for p in rows:
        rel = related_for(p, rows)
        if not rel: empty.append(p["title"])
        plan[p["id"]] = rel
    json.dump(plan, open("catalog/data/shade-related-plan.json", "w"), indent=0)
    print(f"shade elaborate: {len(rows)}  senza correlati: {len(empty)}")
    if empty: print("  ->", empty)
    dist = defaultdict(int)
    for v in plan.values(): dist[len(v)] += 1
    print("distribuzione n. correlati:", dict(sorted(dist.items())))
    for t in sys.argv[1:]:
        for r in rows:
            if r["title"].startswith(t):
                print(f"\n{r['title']}")
                for rid in plan[r["id"]]:
                    print("   -", by_id[rid]["title"])


if __name__ == "__main__":
    main()
