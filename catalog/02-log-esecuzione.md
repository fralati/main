# Log di esecuzione

## Fase A — Correlati delle shade colore (COMPLETATA, 1 settembre 2026)

**Perimetro**: metafield `shopify--discovery--product_recommendation.related_products`
su tutte le 208 shade attive (Vibrant, Grace, Gems, Pure Pigment, Liquid Pigment, cartelle colore).
Nessun tag, nessuna collezione, nessun URL, nessun product type toccato.
I `complementary_products` sono stati lasciati invariati: erano gia' coerenti
(sviluppatore o attivatore della linea, shampoo post-colore, Balancer, strumenti).

### Stato precedente

| Linea | Correlati prima |
|---|---|
| Vibrant (107 shade + 5 Pure Pigment) | sempre gli stessi 4: Bowl Black, Application Brush, Nika Mixer, **Nika Hair Tools Kit (DRAFT)** |
| Gems (20 shade + Clear) | sempre le stesse 5: cartella colore, 81 Black, 11 Pearl Grey, 7 Moka, 62 Fuchsia |
| Grace (72 shade) | cartella colore in prima posizione + alcune shade dello stesso livello |
| Liquid Pigment .21 | un solo prodotto, identico al suo complementare |

Problemi: strumenti presentati come alternative, un prodotto non acquistabile fra i consigli,
nessuna informazione tonale, la cartella colore proposta come "alternativa" su ogni pagina prodotto.

### Regola applicata

Per ogni shade, entro la stessa linea e solo fra prodotti attivi:

1. **Stesso riflesso, livelli adiacenti** (fino a 3) — la stessa tonalita' piu' chiara o piu' scura
2. **Stesso livello, riflessi vicini** (fino a 3) — la stessa profondita' in tonalita' diverse

Livello e riflesso si leggono dal codice shade gia' presente nel titolo (`5.22`, `10.1`, `4.07`).
Le famiglie di riflesso sono: freddi (1 cenere, 2 viola, 9 blu), dorati (3 oro, 8 beige),
caldi (4 rame, 5 mogano, 6 rosso), neutri (0 naturale, 7 tabacco).

Casi particolari:
- shade "intense" (`7.+`) trattate come naturale rinforzato del proprio livello
- serie superbleaching `90.x` e Grace `100`, `11.x`, Silver, Pearl Rose ricondotte al livello 11
- toner Vibrant `01`, `09`, `.COM19` ricondotti al livello 11 con il rispettivo riflesso
- Gems: shade fashion senza scala livelli, raggruppate per famiglia cromatica esplicita
  (freddi, viola, rosa, caldi, marroni, scuri)
- Pure Pigments: alternative fra loro
- Liquid Pigment .21: toner anti-giallo NIKA, ricondotto alle shade fredde Grace
- cartelle colore: alternative fra loro, non piu' proposte come alternativa a una tinta

### Risultato

- 208 shade su 208 aggiornate, 9 batch, **zero errori**
- distribuzione: 171 shade con 6 correlati, 16 con 5, 18 con 4, 3 con 2 (le cartelle colore)
- nessun auto-riferimento, nessun rimando a prodotti DRAFT o ARCHIVED, nessuno strumento fra le alternative

Verifica a campione sul negozio dopo la scrittura:

| Shade | Correlati ora |
|---|---|
| Vibrant 7.0 Blond | 6.0, 8.0, 6.+, 7.7, 7.1, 7.11 |
| Grace 6.44 Dark Deep Copper | 7.44, 7.4, 6.53, 6.6, 6.62 |
| Vibrant 90.2 Superbleaching Violet | 10.28, 9.23, 8.23, 01 Toner Ash, 90.1, 09 Toner Blue |
| Grace Silver | 10.1, 10.11, 9.1, 11.20 Quarzo Rosa, Pearl Rose, 100 Extra Lift |
| Gems 22 Intense Violet | 02 Lavender, 12 Dark Mauve, 01 Platinum, 11 Pearl Grey, 118 Graphite, 18 Iron |

### Rollback

`data/backup-related-before.tsv` contiene lo stato precedente di tutte le 208 shade,
verificato riga per riga prima della scrittura.

## Prossimo passo

Fase B: correlati e complementari dei 226 prodotti attivi non colore, per famiglia
(lavaggio, maschere, leave-in, styling, trattamenti in cabina, kit, strumenti, uomo).
Regola: *related* = alternative allo stesso bisogno, *complementary* = si usano insieme.
Da correggere in particolare i casi con la semantica invertita (Byebact, Chimono, Flexion)
e i rimandi a prodotti archiviati (Defrizzit).
