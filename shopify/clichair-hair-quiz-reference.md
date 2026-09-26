# cliCHair Hair Quiz: documento fonte

Memoria tecnica dell'Hair Quiz della homepage di clichair.ch. Va letto prima di ogni modifica al quiz e aggiornato alla fine (versioni, errori risolti, idee aperte).

Aggiornato al 26.09.2026, versione v5 (blocco unico).

## 1. Cosa fa

- Blocco pieghevole in homepage: titolo "HAIR QUIZ", sottotitolo "In 1 minuto prepari il tuo profilo per clichAIr", pulsante a pillola con bordo rosso "INIZIA IL QUIZ" (pulsa leggermente). Il pulsante è solo bordato perché uno tutto rosso competeva con un altro pulsante della home.
- Aperto mostra un percorso in 3 passi: "Rispondi a 7 domande", "Copia la richiesta nella chat", "clichAIr ti consiglia la routine". Il quiz non dice mai che la routine è pronta: la routine la consiglia clichAIr in chat.
- 7 domande, poi una schermata finale con: riepilogo a chip, testo introduttivo, box "Come continuare" in 3 passi, due pulsanti ("Copia e apri clichAIr" rosso pieno, "Ricomincia" bordato), link "Mostra il messaggio per clichAIr" con la richiesta completa e "Copia di nuovo".
- "Copia e apri clichAIr" copia la richiesta negli appunti e clicca l'icona di Zipchat. La chat NON si precompila (vedi sezione 6): il cliente incolla e invia.
- Lingue: EN, IT, DE, FR (lingua da `request.locale.iso_code`, altrimenti inglese). Anche la richiesta per clichAIr è nella lingua del cliente.

## 2. Principio fondamentale: il quiz raccoglie, clichAIr sceglie

Deciso da Francesco: il quiz NON nomina prodotti, gamme o marchi e non contiene regole che possono diventare obsolete. Raccoglie e formatta i dati, più istruzioni di metodo (analizza gli INCI del catalogo cliCHair, costruisci una routine di N prodotti). La scelta dei prodotti spetta solo a clichAIr, guidato dal paragrafo HAIR QUIZ BRIEF del suo core prompt (sezione 7).

## 3. Dove vive

- Tema Horizon, template `templates/index.json`, blocco Custom Liquid chiamato "Liquid Quiz", impostazione `custom_liquid`. Percorso al 26.09.2026: `sections.section_THkzdp.blocks.group_mjBGHr.blocks.custom_liquid_aUwCDP.settings.custom_liquid`. Gli id dei blocchi possono cambiare: per ritrovarlo cerca il blocco il cui `custom_liquid` contiene `cq2-root`.
- Temi al 26.09.2026: Horizon 4.2.0.05 (gid://shopify/OnlineStoreTheme/189161374077) è ora MAIN, pubblicato da Francesco con il quiz v5 dentro (verificato: contenuto identico al file consegnato, 34.144 caratteri). Per modifiche future serve un nuovo tema bozza (UNPUBLISHED).
- Il codice sta dentro il blocco, non in uno snippet: le impostazioni dei template sopravvivono agli aggiornamenti di Horizon, i file aggiunti no.
- Sfondo: Francesco imposta lo sfondo sulla sezione, non sul blocco. Il quiz usa `--color-foreground` e `--color-background` di Horizon, quindi segue lo schema colori della sezione (testato anche su sfondo scuro).
- Repository GitHub `fralati/main`, cartella `shopify/`:
  - `snippets/clichair-hair-quiz.liquid`: il blocco pronto da incollare (compresso).
  - `src/clichair-hair-quiz.src.liquid`: sorgente leggibile. Si modifica sempre questa.
  - `src/build.js`: comprime il sorgente nel file da incollare.

## 4. Limite di dimensione (importante)

Il limite documentato di un'impostazione Liquid è 50 KB, ma l'editor di Shopify ha rifiutato la v5 da 43 KB (43.060 byte) e accettato la v4 da 34,9 KB (34.886 byte). Il limite reale è quindi fra i due, non noto con precisione.

Regola: il file da incollare deve restare sotto circa 34.000 byte. La v5 compressa pesa 34.319 byte ed è stata accettata (sotto la v4 per caratteri, byte e JSON).

Come si è arrivati a 34 KB senza togliere funzioni: CSS con variabili corte e regole condivise, testi delle opzioni in array nell'ordine di QS (non oggetti con chiavi), messaggi composti da pezzi (es. "Richiesta copiata." + testo), minificazione con terser (anche delle chiavi dei testi) e csso.

Due blocchi Custom Liquid (stile in uno, script nell'altro) funzionano tecnicamente, ma Francesco non si fida di questa soluzione: preferire sempre il blocco unico.

## 5. Struttura del codice

- `<style>` con tutte le classi prefissate `cq2`. Variabili sul contenitore `.cq2`.
- Markup minimo: `#cq2-root` (con `data-lang`), `#cq2-toggle`, `#cq2-body`, `#cq2-path`, `#cq2-stage`. Tutto il resto è generato dallo script.
- Script autonomo `(function init(){...})()`: se `#cq2-root` non c'è ancora, aspetta DOMContentLoaded.
- Stato in localStorage, chiave `cq_state_v3` (risposte + `_step`). Non cambiarla senza motivo: chi torna riprende da dove era.

### Le 7 domande (chiavi fisse, usate nello stato salvato)

| # | Chiave | Tipo | Opzioni |
|---|---|---|---|
| 1 | tex | una risposta | straight, wavy, curly, coily |
| 2 | hair | una risposta | fineflat, average, thickfull |
| 3 | colhist | più risposte, `natural` esclusiva | natural, colored, greycover, lightened, bleached, keratin, perm, heat |
| 4 | cond | più risposte, `healthy` esclusiva | healthy, dry, frizz, damaged, split, dull |
| 5 | scalp | più risposte, `normal` esclusiva, oily e dryscalp si escludono | normal, oily, dryscalp, dandruff, sensitive, thin |
| 6 | goal | massimo 2, smooth e curl si escludono | repair, hydrate, smooth, curl, colorprotect, antiyellow, volume, scalpbal, loss, shine |
| 7 | budget | una risposta | essential (2 prodotti), complete (3-4), full (5 o più) |

Nel sorgente, per ogni lingua: `q` è un array di [titolo, domanda] nell'ordine delle domande; `o` è un array piatto delle 40 etichette nell'ordine di QS; `p.L` sono le 7 etichette della richiesta. Aggiungendo o spostando un'opzione vanno aggiornati QS e gli array `o` in tutte e 4 le lingue.

### La richiesta per clichAIr (esempio IT)

```
Ciao clichAIr! Ho appena completato il quiz capelli su cliCHair.ch. Ecco il mio profilo: analizzalo e consigliami la routine giusta per me.

IL MIO PROFILO CAPELLI
- Texture naturale: ...
- Tipo di capello: ...
- Colore e trattamenti: ...
- Stato dei capelli: ...
- Cute: ...

OBIETTIVO PRINCIPALE: ...
AMPIEZZA DELLA ROUTINE: Minima (2 prodotti)

COSA TI CHIEDO
1. Analizza gli INCI dei prodotti del catalogo cliCHair e scegli solo quelli davvero adatti al mio profilo e al mio obiettivo.
2. Costruisci una routine di esattamente 2 prodotti: scegli prima gli step più importanti ... Se altri prodotti potrebbero aiutare, citali dopo la routine solo come extra facoltativi, senza contarli nella routine.
3. Dimmi cosa evitare e proponi un'alternativa per lo step principale.
4. Rispondi in italiano, in modo chiaro e sintetico, con i link ai prodotti.
```

"esattamente 2 prodotti" / "3 o 4 prodotti" / "almeno 5 prodotti" viene da `p.n`. La frase sugli extra facoltativi serve a far rispettare il numero scelto (clichAIr tendeva ad aggiungere prodotti). In francese è "avec [N]" (non "de exactement").

## 6. Passaggio alla chat (Zipchat)

- Zipchat è installato come app embed. L'icona: `<img id="bubble-icon" data-zipchat="bubble-icon">`. Selettore usato: `[data-zipchat="bubble-icon"],#bubble-icon` (cerca anche negli shadow root).
- Il campo del messaggio di Zipchat è in un iframe di app.zipchat.ai (altro dominio): il sito non può scriverci. Non esiste un'API ufficiale nota per precompilare il messaggio. Per questo: copia + apertura chat + istruzioni chiare prima (box "Come continuare"), non un avviso che la chat coprirebbe.
- Indicazioni per piattaforma: Windows "Ctrl+V", Mac "⌘ Cmd+V", touch "Tieni premuto il campo del messaggio e scegli Incolla".
- Casi di errore, detti in modo onesto:
  - copia non riuscita: si apre "Mostra il messaggio", il testo viene selezionato, messaggio con il tasto per copiare e pulsante "Apri clichAIr";
  - chat non trovata: "La chat non si è aperta da sola: aprila dall'icona di clichAIr in basso sullo schermo."
- Zipchat è agganciato anche alla barra di ricerca della home (`#clichair-home-search`, blocco ai_gen_block_ff365c3): non riguarda il quiz, ma non va toccato.

## 7. Paragrafo HAIR QUIZ BRIEF nel core prompt di clichAIr

Il core prompt di clichAIr (nel pannello Zipchat) è al limite di circa 10.000 caratteri (9.976 con questo paragrafo). Francesco ha adottato questo paragrafo; il resto del prompt non è stato toccato. Modificarlo solo su richiesta, mostrando il testo prima e dopo.

```
## HAIR QUIZ BRIEF
A message headed "MY HAIR PROFILE" (any language) comes from the site
quiz: the diagnosis is done, ask nothing. Answer its numbered requests
in order, all of them. ROUTINE SIZE is the customer's choice: honour
it exactly, it overrides the minimum routine and the two-options
rule. Cover every problem listed, scalp answer first: sensitive or
itchy is not dandruff or oily, use the soothing line. Check the INCI
on each product page before naming it; say whether it meets each
PREFERENCE, flag any that does not. Actives they asked for are not a
lecture. Close: add to cart.
```

Nota: la v5 del quiz non invia più una sezione PREFERENCE; la frase è innocua ma, se serve spazio nel prompt, è la prima da togliere. Il riconoscimento si basa sull'intestazione "MY HAIR PROFILE" "in qualsiasi lingua": clichAIr la riconosce anche come "IL MIO PROFILO CAPELLI", "MEIN HAARPROFIL", "MON PROFIL CAPILLAIRE".

Motivo del paragrafo: in un test clichAIr aveva consigliato Clear Tonic (per cute grassa/forfora) a una cute sensibile, invece di Gentle Relief Treatment.

## 8. Design approvato (v5)

- Contenitore centrale largo 720 px; tutte le domande usano la stessa griglia.
- Colonne: 2 per 4, 8 o 10 opzioni; 3 per 3 o 6 opzioni; 1 colonna su mobile (sotto 640 px). Stessa altezza per tutte le opzioni della domanda, testi allineati a sinistra, altezza minima 56 px.
- Spazi 12 px, raggio 14 px, pulsante "Avanti" sempre nella stessa posizione (bordo destro costante).
- Vetro leggero come la barra di ricerca: sfumatura chiara, riflesso interno in alto, blur 6 px (senza blur resta la sfumatura). Selezione: bordo scuro + leggera tinta rossa, pallino o spunta rossa con piccola animazione.
- Barra di avanzamento con breve transizione. Pressione su mobile: leggera riduzione (scale .985).
- Accessibilità: focus visibile da tastiera (contorno rosso), `aria-pressed` sulle opzioni, focus che resta sull'opzione premuta, titolo della domanda focalizzato al cambio, `prefers-reduced-motion` rispettato.
- Schermata finale: i due pulsanti affiancati e di pari larghezza su desktop, uno sotto l'altro a tutta larghezza su mobile.
- "Ricomincia" chiede conferma se ci sono risposte ("Vuoi ricominciare? Le risposte date finora verranno cancellate.", con "Annulla" e "Sì, ricomincia"; il focus va su Annulla).
- Titolo: da chiuso a metà quiz mostra "Riprendi il tuo Hair Quiz / Domanda 3 di 7"; da aperto sempre "Hair Quiz" + sottotitolo.

## 9. Test (ambiente locale)

Il negozio, Zipchat e il web esterno non sono raggiungibili dall'ambiente di lavoro: si testa con pagine simulate e Playwright (Chromium già installato).

Script nella skill `clichair-hair-quiz` (cartella `scripts/`): `make_pages.py` crea le pagine di prova (IT/EN/DE/FR, sfondo scuro, senza chat) dal file compresso; `t.js` esegue il giro completo. Controlli:

- tutte le 7 domande in IT/FR/EN desktop e IT/DE mobile 390 px; colonne, larghezze e altezze uguali, nessuno scroll orizzontale;
- riga "esattamente 2 prodotti" nella richiesta; appunti = richiesta; icona chat cliccata; percorso passato al passo 3;
- copia non riuscita, chat assente, Indietro, ripresa dopo ricarica, conferma Ricomincia (annulla e sì), tastiera, movimento ridotto, sfondo scuro;
- nessun errore JavaScript; controllo visivo degli screenshot.

Se si cambia solo la forma del codice, confrontare la richiesta generata con la versione precedente nelle 4 lingue (deve essere identica).

Non testabile in locale: sito reale, chat nuova rispetto a chat già aperta, Safari su iPhone.

## 10. Consegna a Francesco

- Codice lungo: consegnarlo come file (.txt) da aprire, selezionare tutto e copiare; non incollarlo in chat (34 KB compressi, rischio di perdere pezzi).
- Istruzioni: tema bozza, blocco "Liquid Quiz", campo "Codice Liquid", sostituire tutto, Salva. La pubblicazione la fa lui.
- Dopo che ha incollato: rileggere `templates/index.json` del tema e confrontare il `custom_liquid` con il file (identico a meno dell'a capo finale).

## 11. Cronologia versioni

| Versione | Commit | Dimensione | Note |
|---|---|---|---|
| v1-v2 | | circa 47 KB | avatar SVG e ciocca ingrandita che cambiavano con le risposte; poi semplificato |
| v3 | 78f8273 | | pulsante "Inizia il quiz" al posto della freccia poco visibile; versione con solo bordo rosso scelta |
| v4 | d1d0afc | 34.886 byte | copia + apertura Zipchat, richiesta senza prodotti, regola dei 2 prodotti; accettata dall'editor |
| v5 | 2798d72 | 43.060 byte | rifinitura completa (percorso 3 passi, box "Come continuare", griglia, vetro, conferma); RIFIUTATA dall'editor |
| v5 in 2 parti | b440c03 | 13,7 + 29,6 KB | scartata |
| v5 blocco unico | 7f406c1 | 34.319 byte | stessa v5 compressa; incollata e pubblicata con Horizon 4.2.0.05 |

## 12. Errori già risolti

- Titolo "Riprendi il tuo Hair Quiz" anche a quiz aperto: da aperto mostra sempre "Hair Quiz".
- Passo attivo del percorso in grassetto andava a capo e disallineava gli altri: niente grassetto, allineamento in alto.
- Riepilogo troppo attaccato al titolo: margine sopra i chip.
- Conferma con role="alertdialog" (sbagliato, non è modale): role="group".
- Conferma dentro la griglia di navigazione occupava una sola colonna: `grid-column:1/-1`.
- Francese "de exactement": "avec exactement".
- Upload del template via API non praticabile (template di circa 100-170 KB): modifiche del template sempre dall'editor, da Francesco.
- Codice da 43 KB rifiutato dall'editor: compressione sotto 34 KB.

## 13. Idee aperte (proposte, non approvate)

1. Eventi analytics (quiz aperto, completato, "Copia e apri" cliccato).
2. Chiedere a Zipchat un'API ufficiale per precompilare il messaggio.
3. Test reale su iPhone Safari; eventualmente aprire la chat prima di copiare.
4. Margine in basso su mobile se l'icona Zipchat copre i pulsanti.
5. Invio del profilo per email (funzione nuova, strategica).
