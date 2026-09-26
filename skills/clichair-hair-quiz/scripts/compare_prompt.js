// Uso: node compare_prompt.js <cartella pagine versione A> <cartella pagine versione B>
// Confronta richiesta, chip, box 'Come continuare' e percorso nelle 4 lingue con le stesse risposte.
let PW;try{PW=require('playwright')}catch(e){PW=require('/opt/node22/lib/node_modules/playwright')}const { chromium } = PW;
const st=JSON.stringify({tex:'curly',hair:'thickfull',colhist:['colored','heat'],cond:['dry','split'],scalp:['oily','sensitive'],goal:['repair','shine'],budget:'full',_step:7});
(async()=>{const b=await chromium.launch();let same=0,diff=[];
for(const l of ['it','en','de','fr']){const r=[];for(const d of process.argv.slice(2,4)){const p=await b.newPage();await p.goto('file://'+require('path').resolve(d)+'/'+l+'.html');await p.evaluate(s=>localStorage.setItem('cq_state_v3',s),st);await p.reload();await p.click('#cq2-toggle');await p.waitForTimeout(300);r.push(await p.evaluate(()=>[document.getElementById('cq2-txt').value,document.querySelector('.cq2-chips').innerText,document.querySelector('.cq2-how').innerText,document.getElementById('cq2-path').innerText].join('\n###\n')));await p.close();}
if(r[0]===r[1])same++;else diff.push(l+'\n'+r[0]+'\n------\n'+r[1]);}
console.log('identical',same,'\n',diff.join('\n=====\n'));await b.close();})();
