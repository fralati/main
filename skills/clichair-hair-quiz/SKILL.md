---
name: clichair-hair-quiz
description: "Use for any work on the cliCHair (clichair.ch) homepage Hair Quiz, the Custom Liquid block \"Liquid Quiz\" that builds a request for clichAIr (the Zipchat AI assistant): changing questions, options, texts in EN/IT/DE/FR, design, the copy-and-open-chat handoff, the request (prompt) the quiz generates, its size limit in the Shopify editor, tests and delivery to Francesco. Also use when clichAIr answers a quiz request badly, when the HAIR QUIZ BRIEF paragraph of the clichAIr core prompt is involved, or when the user mentions hair quiz, quiz capelli, profilo capelli, cq2, cq_state_v3 or 'Copia e apri clichAIr', even without naming the skill."
---

# cliCHair Hair Quiz

L'Hair Quiz della homepage di clichair.ch raccoglie 7 risposte sui capelli e prepara una richiesta che il cliente copia nella chat di clichAIr (Zipchat), che poi consiglia la routine. Vive in un blocco Custom Liquid del tema Horizon.

Lavora e rispondi in italiano. Francesco è il CEO: vuole risultati pronti, testati e spiegati in modo semplice, con codice da copiare e incollare.

## 0. Prima di tutto: il documento fonte

Leggi `references/clichair-hair-quiz-reference.md` (copia anche nel progetto Claude CLICHAIR come `claude/clichair-hair-quiz-reference.md`; se le due copie differiscono, vale la più recente per data in testa). Contiene: dove vive il blocco, le 7 domande e le chiavi, la struttura della richiesta, il paragrafo HAIR QUIZ BRIEF di clichAIr, il design approvato, la cronologia, gli errori già risolti e le idee aperte. Senza questo contesto è facile rifare errori già risolti.

Il sorgente leggibile più recente è nel repository `fralati/main` in `shopify/src/clichair-hair-quiz.src.liquid`; `assets/clichair-hair-quiz.src.liquid` della skill è la copia della v5 (può essere più vecchia).

## Regole fisse

- **Il quiz raccoglie, clichAIr sceglie.** Il quiz non nomina prodotti, gamme o marchi e non contiene regole di catalogo che possono invecchiare. Solo dati del cliente e istruzioni di metodo (analizza gli INCI, routine di N prodotti). Se una risposta di clichAIr è sbagliata, la correzione va di norma nel prompt di clichAIr, non nel quiz.
- **Si lavora solo su un tema bozza (UNPUBLISHED)**, mai sul MAIN: la pubblicazione la fa Francesco. Controlla con `themes { nodes { id name role } }` quale tema è bozza: i ruoli cambiano quando lui pubblica.
- **Blocco unico, niente file separati.** Il codice sta tutto nel blocco Custom Liquid (le impostazioni dei template sopravvivono agli aggiornamenti di Horizon, gli snippet no). Niente divisione in due blocchi: Francesco non se ne fida.
- **Limite di dimensione: sotto circa 34.000 byte** il file da incollare. L'editor ha rifiutato 43 KB e accettato 34,9 KB, anche se il limite documentato è 50 KB.
- **Il template si modifica dall'editor, non via API**: il file è di 100-170 KB. Dai a Francesco il file e le istruzioni per incollarlo.
- **4 lingue** (EN, IT, DE, FR) dentro il blocco, tedesco con il "Sie" nei testi dell'interfaccia (la richiesta a clichAIr in tedesco usa il "du", è il cliente che scrive al bot), niente trattini lunghi nei testi del sito.
- **Non cambiare** la chiave `cq_state_v3` (chi torna perde il progresso) né il selettore di Zipchat senza verificare l'icona reale.
- **Onestà nel passaggio alla chat**: il campo di Zipchat è in un iframe di un altro dominio, non si può precompilare. Non promettere che il messaggio sia già nella chat; spiega prima cosa fare (incolla e invia) e gestisci in modo veritiero copia o apertura non riuscite.
- **Prompt di clichAIr**: il core prompt è al limite di circa 10.000 caratteri. Tocca solo il paragrafo HAIR QUIZ BRIEF, mostra prima e dopo, e conferma a Francesco che il resto è invariato.

## Procedura

### 1. Recupera il codice attuale
- Leggi `templates/index.json` del tema su cui si lavora (GraphQL `theme(id:) { files(filenames:["templates/index.json"]) { nodes { body { ... on OnlineStoreThemeFileBodyText { content } } } } }`). Il risultato è grande e viene salvato su file: analizzalo con Python, togli il commento iniziale `/* ... */`, cerca il blocco il cui `custom_liquid` contiene `cq2-root`.
- Confronta quel codice con `shopify/snippets/clichair-hair-quiz.liquid` del repository (uguale a meno dell'a capo finale). Se è diverso, qualcuno l'ha cambiato nell'editor: capisci cosa prima di partire dal sorgente.

### 2. Modifica il sorgente leggibile
- Lavora su `clichair-hair-quiz.src.liquid`, mai sul file compresso. Modifiche mirate (script Python con `assert s.count(old) == 1` prima di ogni sostituzione).
- Testi: per ogni lingua `q` è un array [titolo, domanda] nell'ordine delle domande, `o` un array piatto delle etichette nell'ordine di QS, `p.L` le 7 etichette della richiesta. Aggiungere o spostare un'opzione richiede di aggiornare QS e gli array in tutte e 4 le lingue.
- Nuove chiavi di testo: se sono lette solo come `L.chiave`, aggiungile alla regex `mangle.properties` in `build.js` per risparmiare byte; non metterci nomi che esistono anche nel DOM (`open`, `close`, ecc.).

### 3. Comprimi e controlla la dimensione
- `npm install terser csso` in una cartella di lavoro, poi `node scripts/build.js <sorgente> <file-da-incollare.liquid>`. Lo script blocca l'uscita se compaiono `{{` o `{%` nel codice compresso (Liquid li interpreterebbe).
- Se supera circa 34.000 byte: prima si accorcia il codice (regole CSS condivise, messaggi composti da pezzi), poi, solo con il consenso di Francesco, i testi. Non togliere funzioni in silenzio.

### 4. Testa (obbligatorio)
Il negozio e Zipchat non sono raggiungibili: si usano pagine simulate e Playwright (Chromium preinstallato).
- `python3 scripts/make_pages.py <file-da-incollare> <cartella>` e poi `node scripts/t.js <cartella>`: 7 domande in più lingue su desktop e mobile, griglia, copia, apertura chat, errori, conferma, tastiera, movimento ridotto, sfondo scuro. Deve finire con `ERRORS []`.
- Se hai cambiato solo la forma del codice: `node scripts/compare_prompt.js <pagine versione vecchia> <pagine versione nuova>` deve dire `identical 4`.
- Guarda gli screenshot (desktop, mobile, schermata finale, conferma, sfondo scuro): il controllo visivo conta quanto i numeri.
- Per modifiche importanti, una revisione indipendente (subagente) del codice e dei testi prima della consegna.

### 5. Consegna
- Manda il file da incollare come `.txt` (SendUserFile) invece di incollarlo in chat: 34 KB compressi copiati dalla chat rischiano di perdere pezzi.
- Istruzioni brevi: tema bozza, blocco "Liquid Quiz", campo "Codice Liquid", sostituire tutto, Salva. Ricorda che la pubblicazione la fa lui.
- Dopo che ha incollato, rileggi il template e verifica che il `custom_liquid` sia identico al file.
- Dì chiaramente cosa non è stato testabile (sito reale, chat già aperta rispetto a nuova, Safari su iPhone).
- Proponi le funzioni nuove prima di costruirle.

### 6. Chiusura
- Repository `fralati/main`: aggiorna `shopify/src/` e `shopify/snippets/clichair-hair-quiz.liquid`, commit e push sul branch di lavoro indicato.
- Aggiorna il documento fonte (cronologia con commit e byte, errori risolti, idee aperte, data in testa) nella skill e dai a Francesco la versione da ricaricare nel progetto CLICHAIR (o scrivila tu se hai accesso ai Projects).

## Quando clichAIr risponde male a una richiesta del quiz
1. Fatti dare la risposta completa e le risposte date al quiz; ricostruisci la richiesta con `compare_prompt.js` o a mano.
2. Verifica i prodotti in Shopify (INCI, destinazione d'uso) prima di giudicare.
3. Se la richiesta era chiara, correggi il paragrafo HAIR QUIZ BRIEF (conteggio caratteri del prompt intero sotto circa 10.000). Cambia il quiz solo se il dato mancava o era ambiguo, e sempre senza nominare prodotti.
