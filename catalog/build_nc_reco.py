#!/usr/bin/env python3
"""
Correlati e complementari per i 226 prodotti attivi non colore di cliCHair.

Semantica:
  related       = alternative allo stesso bisogno (si comprano AL POSTO di)
  complementary = si usano INSIEME (step successivo del protocollo, strumento, mantenimento)

Vincoli globali: solo prodotti attivi, mai se stesso, mai materiale marketing
fra i consigli di un prodotto vendibile.
"""
import json, re
from collections import defaultdict

P = {}   # id -> dict
for l in open('catalog/data/nc-products.tsv'):
    pid, handle, ptype, tags = l.rstrip('\n').split('\t')
    P[pid] = {"id": pid, "handle": handle, "type": ptype,
              "tags": set(tags.split(',')) if tags else set()}
SHADE_TITLES = [tuple(l.rstrip('\n').split('\t')) for l in open('catalog/data/shades-active.tsv')]
SHADES = [i for i, _ in SHADE_TITLES]
H = {p["handle"]: pid for pid, p in P.items()}


def h(*names):
    """handle -> id, saltando quelli assenti"""
    return [H[n] for n in names if n in H]


# ---------------------------------------------------------------- ruolo
def role(p):
    t, tags, hd = p["type"], p["tags"], p["handle"]
    if t == "Marketing": return "sample" if "Sample" in tags else "marketing"
    if t == "Oxidizer": return "developer"
    if t == "Bleaching": return "bleach"
    if t == "After Shave": return "aftershave"
    if t == "Beard": return "shaving" if "Shaving" in tags else "beard"
    if t in ("Sanitizing", "Skin Stain Remover"): return "skin"
    if t == "GiftCard": return "giftcard"
    if t == "Clothing" or hd in ("nika-turban", "nika-disposable-cape"): return "wear"
    if t == "Tools" or hd == "flexion-l-brush" or ("brush" in hd and t != "Styling"): return "tool"
    if t == "Bundle": return "kit"
    if t == "Treatment": return "treatment"
    if t == "Care": return "leavein"
    if t == "Styling": return "styling"
    if t == "Wash":
        if "Mask" in tags: return "mask"
        if "Conditioner" in tags: return "conditioner"
        return "shampoo"
    return "other"


# ---------------------------------------------------------------- linea
LINE_BY_PREFIX = [
    ("inej-anti-age", "Inej Anti-Age"), ("inej-anti-dandruff", "Inej Dandruff"),
    ("inej-color-protect", "Inej Color Protect"), ("inej-dry-hair", "Inej Dry"),
    ("inej-loss-control", "Inej Loss"), ("inej-remedy", "Inej Oily"),
    ("inej-smooth", "Inej Smooth"), ("inej-detox", "Inej Detox"),
    ("nika-gentle-relief", "Gentle Relief"), ("nika-new-density", "New Density"),
    ("nika-total-balance", "Total Balance"),
    ("curly-up-", "Curly Up"), ("curly-harmony", "Curly Up"),
    ("no-glow-yellow-", "No Glow Yellow"), ("ngy-", "No Glow Yellow"),
    ("intensive-remedy-", "Intensive Remedy"),
    ("pure-keratin-", "K-perfection"), ("nika-breakless", "K-perfection"),
    ("nika-miracle", "K-perfection"), ("nika-ultimate", "K-perfection"),
    ("liss-komplex", "Liss Komplex"), ("pure-verve", "Pure Verve"),
    ("clichair-pure-verve", "Pure Verve"),
    ("reconstructive-", "Reconstructive"), ("regeneration-", "Regeneration"),
    ("volume-up", "Volume Up"), ("inej-", "Inej"), ("xflex-", "Xflex"),
    ("nika-frozen-blonde", "Frozen Blonde"), ("nika-fairy-silk", "Fairy Silk"),
    ("nika-age-restore", "Age Restore"),
    ("nika-clear-tonic", "Clear Tonic"),
    ("nika-hyalu", "Age Restore"), ("nika-radiance", "Age Restore"),
]
LINE_TAGS = ["Fairy Silk", "K-perfection", "Age Restore", "Frozen Blonde",
             "Healthy Scalp", "Styling Secret", "Riviera Breeze", "Pure Verve",
             "Inej", "Liss Komplex", "Reconstructive", "Regeneration",
             "Volume Up", "Cuticle", "Nanoplastia", "Xflex"]
COLOR_SERVICE = {"colorfixx-1000", "balancer-1000", "stabilizer",
                 "perfect-color-care-duo", "remov-up", "remover"}


def line(p):
    if p["handle"] in COLOR_SERVICE: return "Color Service"
    for pre, ln in LINE_BY_PREFIX:
        if p["handle"].startswith(pre): return ln
    for t in LINE_TAGS:
        if t in p["tags"]: return t
    if "Reconstruction" in p["tags"]: return "Reconstructive"
    return None


# ---------------------------------------------------------------- bisogno
NEED_BY_TAG = [
    ("Anti-Yellow", "blonde"), ("Curly", "curl"),
    ("Frizz Free", "smooth"), ("Smooth", "smooth"),
    ("Split Ends", "repair"), ("Reconstruction", "repair"),
    ("Reconstructive", "repair"), ("Repair", "repair"), ("Regeneration", "repair"),
    ("Keratin", "repair"),
    ("Dandruff", "scalp"), ("Oily", "scalp"), ("Sensitive", "scalp"),
    ("Loss", "scalp"), ("Detox", "scalp"), ("Scalp", "scalp"),
    ("Healthy Scalp", "scalp"),
    ("Anti-Age", "antiage"), ("Age Restore", "antiage"),
    ("Coloured", "colour-care"), ("Hydration", "hydration"),
    ("Volumizing", "volume"), ("Volume Up", "volume"),
    ("Protection", "protection"),
]


def needs(p):
    return [n for t, n in NEED_BY_TAG if t in p["tags"]]


for pid, p in P.items():
    p["role"], p["line"], p["needs"] = role(p), line(p), needs(p)
    p["brand"] = ("Xflex" if "Xflex" in p["tags"] else
                  "Nika" if "Nika" in p["tags"] else
                  "Code Zero" if "Code Zero" in p["tags"] else
                  "Edelstein" if "Edelstein" in p["tags"] else "cliCHair")

VALID = set(P) | set(SHADES)

BY_ROLE = defaultdict(list)
for pid, p in P.items(): BY_ROLE[p["role"]].append(pid)


# ---------------------------------------------------------------- ancore
FINISH = {"Xflex": h("xflex-power-spray"), "Nika": h("nika-hair-spray"),
          "Code Zero": h("finish-up"), "Edelstein": h("beat-up-hold"),
          "cliCHair": h("beat-up-hold")}
HEAT = h("all-brushing-fast")
COLOR_TOOLS = h("bowl-color-code-zero", "brush-color", "nika-color-mixer")
DEVELOPERS = h("oxidizer", "nika-activator")
POST_COLOR = h("colorfixx-1000", "balancer-1000", "remov-up")
DETANGLER = h("argan-native-fluid", "extender", "nika-shimmer")
BLEACH = h("bleach-9-tones", "lightening-cream-black", "blondeness", "nika-extreme-lift")
BOND = h("pure-verve-molecular-kit")
SHAVE = h("xflex-shave-cream", "xflex-shave-gel")
AFTERSHAVES = h("xflex-after-shave-refreshing", "xflex-after-shave-sensitive",
                "xflex-after-shave-classic")
SAMPLE_OF = {"reconstructive-sample": h("reconstructive-treatment", "reconstructive-shampoo-250"),
             "regeneration-therapy-sample": h("regeneration-therapy-treatment",
                                              "regeneration-therapy-shampoo-250"),
             "xflex-lux-fix-sample": h("xflex-lux-fix"),
             "prickly-pear-oil-sample": h("argan-native-fluid")}

# ordine del protocollo per i complementari di una linea di cura
PROTO = {"shampoo":     ["conditioner", "mask", "treatment", "leavein"],
         "conditioner": ["shampoo", "mask", "leavein", "treatment"],
         "mask":        ["shampoo", "conditioner", "leavein", "treatment"],
         "leavein":     ["shampoo", "mask", "conditioner", "treatment"],
         "treatment":   ["shampoo", "mask", "conditioner", "leavein"]}

STYLE_KIND = [("gel", ["gel"]), ("wax", ["wax", "paste"]), ("spray", ["spray", "hold"]),
              ("mousse", ["mousse", "foam"]), ("powder", ["powder", "dust"]),
              ("salt", ["salt", "briny"]), ("oil", ["oil"]), ("fluid", ["fluid"])]


def style_kind(p):
    hd = p["handle"]
    if "Hairspray" in p["tags"]: return "spray"
    if "Wax" in p["tags"]: return "wax"
    if "Gel" in p["tags"]: return "gel"
    if "Mousse" in p["tags"]: return "mousse"
    if "Sea Salt" in p["tags"]: return "salt"
    for k, keys in STYLE_KIND:
        if any(x in hd for x in keys): return k
    return "other"


def cap(seq, n, exclude):
    out = []
    for x in seq:
        if x and x not in out and x not in exclude and x in VALID:
            out.append(x)
        if len(out) >= n: break
    return out


def related_for(pid):
    p, r, ln, ex = P[pid], P[pid]["role"], P[pid]["line"], {pid}
    pool = [q for q in BY_ROLE[r] if q != pid and P[q]["role"] not in ("marketing", "sample")]

    if r in ("marketing", "sample"):
        return cap([q for q in BY_ROLE[r] if P[q]["brand"] == p["brand"] and q != pid], 4, ex)
    if r == "giftcard":
        return []

    if r == "styling":
        k, nd = style_kind(p), set(p["needs"])
        same_kind_brand = [q for q in pool if style_kind(P[q]) == k and P[q]["brand"] == p["brand"]]
        same_kind = [q for q in pool if style_kind(P[q]) == k]
        # un termoprotettore o un fluido leave-in e' una vera alternativa a una crema da brushing
        same_need = [q for q in BY_ROLE["leavein"] + pool
                     if q != pid and nd & set(P[q]["needs"])]
        same_brand = [q for q in pool if P[q]["brand"] == p["brand"]]
        if k in ("other", "fluid"):
            return cap(same_need + same_kind + same_brand, 6, ex)
        return cap(same_kind_brand + same_kind + same_need + same_brand, 6, ex)

    if r in ("tool", "wear"):
        same_brand = [q for q in pool if P[q]["brand"] == p["brand"]]
        return cap(same_brand + pool, 6, ex)

    if r == "aftershave":
        return cap(pool, 6, ex)
    if r in ("beard", "shaving", "skin", "developer", "bleach"):
        return cap(pool, 5, ex)

    # linee di cura e kit. Ordine: altri formati dello stesso prodotto,
    # stesso bisogno in altre linee, resto della linea, stesso brand
    def stem(x):
        return re.sub(r"-\d+$", "", P[x]["handle"])
    my_stem, my_needs = stem(pid), set(p["needs"])

    def score(q):
        if stem(q) == my_stem: return 0
        shared = my_needs & set(P[q]["needs"])
        same_ln = ln and P[q]["line"] == ln
        if shared and same_ln: return 1
        if shared: return 2
        if same_ln: return 3
        if P[q]["brand"] == p["brand"]: return 4
        return 5
    ranked = sorted(pool, key=lambda q: (score(q), P[q]["handle"]))
    ranked = [q for q in ranked if score(q) <= 4] or ranked
    return cap(ranked, 6, ex)


MANUAL_COMP = {
    "dry-ease-dry-shampoo-powder": ("puff-up-root-body-powder", "dry-wash-volume-powder-routine"),
    "sweet-almonds-shampoo": ("regeneration-therapy-mask-175", "argan-native-fluid"),
    "nika-riviera-breeze-kit": ("nika-fairy-silk-shampoo-250", "extender", "nika-massage-scalp"),
}


def complementary_for(pid):
    p, r, ln, ex = P[pid], P[pid]["role"], P[pid]["line"], {pid}
    if p["handle"] in MANUAL_COMP:
        return cap(h(*MANUAL_COMP[p["handle"]]), 3, ex)

    if p["handle"] in SAMPLE_OF:
        return cap(SAMPLE_OF[p["handle"]], 3, ex)
    if r == "marketing" or r == "giftcard":
        return []

    if r == "developer":
        # lo sviluppatore si vende con le tinte della sua linea
        want = "Grace" if p["handle"] == "nika-activator" else "Vibrant"
        shades = [i for i, t in SHADE_TITLES
                  if t.startswith(want) and (" 5.0 " in t or " 7.0 " in t)][:2]
        return cap(shades + COLOR_TOOLS, 4, ex)
    if r == "bleach":
        return cap(DEVELOPERS + BOND + h("no-glow-yellow-shampoo-300") + COLOR_TOOLS, 4, ex)
    if r == "skin":
        if p["handle"] == "sanitising-hand-gel":
            return cap(h("nika-disposable-cape", "necks-cover", "chimono"), 3, ex)
        return cap(COLOR_TOOLS + DEVELOPERS + BLEACH, 4, ex)
    if r == "wear":
        return cap(COLOR_TOOLS + h("nika-protection-cape", "necks-cover"), 4, ex)
    if r == "tool":
        if any(x in p["handle"] for x in ("bowl", "mixer", "brush-color", "application-brush",
                                          "nk-application", "small-brush", "tech-brush")):
            return cap(DEVELOPERS + BLEACH + POST_COLOR, 4, ex)
        if "atomizer" in p["handle"]:
            return cap(AFTERSHAVES + SHAVE, 4, ex)
        if "massage" in p["handle"] or "Scalp" in p["tags"] or "Healthy Scalp" in p["tags"]:
            scalp = [q for q in P if "scalp" in P[q]["needs"]
                     and P[q]["role"] in ("treatment", "leavein") and q != pid]
            scalp.sort(key=lambda q: (P[q]["brand"] != p["brand"], P[q]["handle"]))
            return cap(scalp, 4, ex)
        return cap(DETANGLER + h("nika-clear-tonic"), 4, ex)     # spazzole e pettini
    if r == "aftershave":
        return cap(SHAVE + h("xflex-atomizer", "xflex-beard-oil"), 4, ex)
    if r in ("beard", "shaving"):
        others = [q for q in BY_ROLE["beard"] + BY_ROLE["shaving"] if q != pid]
        return cap(others + AFTERSHAVES, 4, ex)
    if r == "styling":
        k, out, nd = style_kind(p), [], set(p["needs"])
        if k != "spray": out += FINISH[p["brand"]]
        out += HEAT
        if p["brand"] == "Xflex":
            out += h("xflex-ghiaccio-shampoo")
        else:
            wash = [q for q in BY_ROLE["shampoo"] if nd & set(P[q]["needs"])]
            wash.sort(key=lambda q: (P[q]["brand"] != p["brand"], P[q]["handle"]))
            out += wash
        return cap(out, 3, ex)
    if r == "kit":
        singles = [q for q in P if P[q]["line"] == ln and P[q]["role"] in
                   ("shampoo", "mask", "conditioner", "treatment", "leavein") and q != pid]
        return cap(singles, 4, ex)

    # linee di cura: gli altri step della stessa linea, in ordine di protocollo
    out = []
    if ln:
        for want in PROTO.get(r, []):
            out += [q for q in P if P[q]["line"] == ln and P[q]["role"] == want and q != pid]
    if ln:   # il finish della linea: fluido, siero o styling dedicato
        out += [q for q in P if P[q]["line"] == ln and P[q]["role"] == "styling" and q != pid]
    if len(out) < 3:
        fill = [q for q in P if set(p["needs"]) & set(P[q]["needs"])
                and P[q]["role"] in ("leavein", "treatment") and q != pid]
        fill.sort(key=lambda q: (P[q]["brand"] != p["brand"], P[q]["handle"]))
        out += fill
    return cap(out, 4, ex)


def dedupe_formats(ids):
    """nei complementari basta un formato per prodotto"""
    out, seen = [], set()
    for x in ids:
        st = re.sub(r"-\d+$", "", P[x]["handle"]) if x in P else x
        if st in seen: continue
        seen.add(st); out.append(x)
    return out


def main():
    plan = {}
    for pid in P:
        plan[pid] = {"rel": related_for(pid),
                     "comp": dedupe_formats(complementary_for(pid))}
    json.dump(plan, open('catalog/data/nc-reco-plan.json', 'w'), indent=0)

    empty_r = [P[k]["handle"] for k, v in plan.items() if not v["rel"] and P[k]["role"] != "giftcard"]
    empty_c = [P[k]["handle"] for k, v in plan.items() if not v["comp"]
               and P[k]["role"] not in ("marketing", "giftcard")]
    print(f"prodotti: {len(P)}")
    print(f"senza correlati: {len(empty_r)} {empty_r if empty_r else ''}")
    print(f"senza complementari: {len(empty_c)} {empty_c if empty_c else ''}")
    rc = defaultdict(int)
    for pid, p in P.items(): rc[p["role"]] += 1
    print("ruoli:", dict(sorted(rc.items(), key=lambda x: -x[1])))


def show(*handles):
    plan = json.load(open('catalog/data/nc-reco-plan.json'))
    names = {i: P[i]["handle"] for i in P}
    names.update({i: t for i, t in SHADE_TITLES})
    for hd in handles:
        pid = H[hd]
        print(f"\n{hd}  [{P[pid]['role']} / {P[pid]['line']} / {P[pid]['brand']}]")
        print("  correlati:    " + ", ".join(names[x] for x in plan[pid]["rel"]))
        print("  complementari:" + ", ".join(names[x] for x in plan[pid]["comp"]))


if __name__ == "__main__":
    import sys
    main()
    if len(sys.argv) > 1: show(*sys.argv[1:])
