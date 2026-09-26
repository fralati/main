// Uso: node t.js <cartella con le pagine di make_pages.py>  (screenshot salvati nella stessa cartella)
let PW;try{PW=require('playwright')}catch(e){PW=require('/opt/node22/lib/node_modules/playwright')}const { chromium } = PW;
const D=require('path').resolve(process.argv[2]||__dirname);const out=[];const errs=[];const log=(...a)=>out.push(a.join(' '));
const A=[['wavy'],['fineflat'],['colored','heat'],['split'],['sensitive'],['volume','repair'],['essential']];
(async()=>{const b=await chromium.launch();
async function ctxFor(mobile,opts={}){const c=await b.newContext(mobile?{viewport:{width:390,height:844},hasTouch:true,isMobile:true,deviceScaleFactor:2}:{viewport:{width:1440,height:1000}});if(!opts.noclip)await c.grantPermissions(['clipboard-read','clipboard-write']);const p=await c.newPage();p.on('pageerror',e=>errs.push((opts.tag||'')+': '+e.message));p.on('console',m=>{if(m.type()==='error')errs.push((opts.tag||'')+' console: '+m.text())});if(opts.noclip)await p.addInitScript(()=>{Object.defineProperty(navigator,'clipboard',{value:undefined});document.execCommand=()=>false;});return [c,p];}
const shot=async(p,name,full)=>p.screenshot({path:D+'/'+name+'.png',fullPage:!!full});
async function geom(p){return p.evaluate(()=>{const o=[...document.querySelectorAll('.cq2-opt')].map(e=>e.getBoundingClientRect());const cols=new Set(o.map(r=>Math.round(r.left))).size;const w=new Set(o.map(r=>Math.round(r.width))).size;const h=new Set(o.map(r=>Math.round(r.height))).size;const s=document.getElementById('cq2-stage').getBoundingClientRect();const n=document.getElementById('cq2-next').getBoundingClientRect();return {n:o.length,cols,widths:w,heights:h,minH:Math.round(Math.min(...o.map(r=>r.height))),stageL:Math.round(s.left),stageW:Math.round(s.width),nextRight:Math.round(n.right),hscroll:document.documentElement.scrollWidth>innerWidth}});}
async function flow(lang,mobile,tag,full){
 const [c,p]=await ctxFor(mobile,{tag});await p.goto('file://'+D+'/'+lang+'.html');
 const tap=s=>mobile?p.tap(s):p.click(s);
 if(full)await shot(p,tag+'_0closed');
 await tap('#cq2-toggle');await p.waitForTimeout(600);
 for(let i=0;i<7;i++){
  const g=await geom(p);log(tag,'Q'+(i+1),JSON.stringify(g));
  for(const v of A[i])await tap('.cq2-opt[data-v="'+v+'"]');
  await p.waitForTimeout(300);
  if(full&&(i===0||i===2||i===5||i===6))await shot(p,tag+'_q'+(i+1));
  await tap('#cq2-next');await p.waitForTimeout(450);
 }
 await p.waitForTimeout(500);
 const txt=await p.$eval('#cq2-txt',e=>e.value);
 log(tag,'minimal routine line:',(txt.split('\n').find(l=>/^2\. /.test(l))||'').slice(0,70));
 if(full)await shot(p,tag+'_summary',true);
 const acts=await p.evaluate(()=>[...document.querySelectorAll('.cq2-acts .cq2-btn')].map(b=>{const r=b.getBoundingClientRect();return Math.round(r.left)+','+Math.round(r.top)+' '+Math.round(r.width)+'x'+Math.round(r.height)}));
 log(tag,'summary buttons:',acts.join(' | '),'hscroll',await p.evaluate(()=>document.documentElement.scrollWidth>innerWidth));
 await tap('#cq2-open');await p.waitForTimeout(500);
 log(tag,'after open: chat clicks',await p.evaluate(()=>window.__zc||0),'| status:',await p.$eval('#cq2-status',e=>e.innerText),'| clipboard==prompt',await p.evaluate(t=>navigator.clipboard.readText().then(x=>x===t),txt),'| path:',await p.$eval('#cq2-path',e=>[...e.children].map(li=>li.className||'-').join('/')));
 if(full)await shot(p,tag+'_afteropen');
 await c.close();}
await flow('it',false,'it_desk',true);
await flow('it',true,'it_mob',true);
await flow('fr',false,'fr_desk',false);
await flow('de',true,'de_mob',false);
await flow('en',false,'en_desk',false);
// back, resume, keyboard, confirm
{const [c,p]=await ctxFor(false,{tag:'nav'});await p.goto('file://'+D+'/it.html');
 await p.click('#cq2-toggle');await p.waitForTimeout(500);
 await p.click('.cq2-opt[data-v="curly"]');await p.click('#cq2-next');await p.waitForTimeout(300);
 await p.click('.cq2-opt[data-v="thickfull"]');await p.click('#cq2-next');await p.waitForTimeout(300);
 await p.click('#cq2-back');await p.waitForTimeout(300);
 log('back: shows',await p.$eval('#cq2-q',e=>e.textContent),'selected',await p.$eval('.cq2-opt[aria-pressed=true]',e=>e.dataset.v));
 // keyboard: tab to an option and press space
 await p.focus('.cq2-opt[data-v="fineflat"]');await p.keyboard.press('Space');await p.waitForTimeout(200);
 log('keyboard: pressed',await p.$eval('.cq2-opt[data-v="fineflat"]',e=>e.getAttribute('aria-pressed')),'focus kept',await p.evaluate(()=>document.activeElement.dataset.v));
 await p.keyboard.press('Tab');await shot(p,'kbd_focus');
 await p.click('#cq2-next');await p.waitForTimeout(300);
 await p.reload();await p.waitForTimeout(300);
 log('resume after reload: header',await p.$eval('[data-t=ask]',e=>e.textContent),'/',await p.$eval('[data-t=ask2]',e=>e.textContent),'/ cta',await p.$eval('[data-t=cta]',e=>e.textContent));
 await shot(p,'resume_closed');
 await p.click('#cq2-toggle');await p.waitForTimeout(500);
 log('resume opens at:',await p.$eval('#cq2-q',e=>e.textContent));
 await p.click('#cq2-reset');await p.waitForTimeout(200);await shot(p,'confirm_mid');
 log('confirm mid shown',await p.$$eval('.cq2-confirm',e=>e.length),'focus on',await p.evaluate(()=>document.activeElement.id));
 await p.click('#cq2-no');await p.waitForTimeout(200);log('cancel keeps step:',await p.$eval('#cq2-q',e=>e.textContent));
 await p.click('#cq2-reset');await p.click('#cq2-yes');await p.waitForTimeout(300);
 log('after yes: ',await p.$eval('#cq2-q',e=>e.textContent),'answers left',await p.$$eval('.cq2-opt[aria-pressed=true]',e=>e.length),'header cta',await p.$eval('[data-t=cta]',e=>e.textContent));
 await c.close();}
// summary restart confirm + clipboard failure + no chat
{const [c,p]=await ctxFor(false,{tag:'noclip',noclip:true});await p.goto('file://'+D+'/it.html');
 await p.click('#cq2-toggle');await p.waitForTimeout(400);
 for(let i=0;i<7;i++){for(const v of A[i])await p.click('.cq2-opt[data-v="'+v+'"]');await p.click('#cq2-next');await p.waitForTimeout(200);}
 await p.click('#cq2-open');await p.waitForTimeout(300);
 log('copy fail: chat clicks',await p.evaluate(()=>window.__zc||0),'| details open',await p.$eval('#cq2-det',e=>e.open),'| selected chars',await p.evaluate(()=>{const t=document.getElementById('cq2-txt');return t.selectionEnd-t.selectionStart}),'| status:',await p.$eval('#cq2-status',e=>e.innerText.replace(/\n/g,' / ')));
 await shot(p,'copyfail',true);
 await p.click('#cq2-go');await p.waitForTimeout(200);log('open from fail box: chat clicks',await p.evaluate(()=>window.__zc||0));
 await p.click('#cq2-restart');await p.waitForTimeout(200);await shot(p,'confirm_summary');
 log('summary confirm shown',await p.$$eval('.cq2-confirm',e=>e.length));
 await p.click('#cq2-no');await p.waitForTimeout(200);log('cancel keeps summary',await p.$$eval('#cq2-open',e=>e.length));
 await c.close();}
{const [c,p]=await ctxFor(false,{tag:'nobubble'});await p.goto('file://'+D+'/nobubble.html');
 await p.click('#cq2-toggle');await p.waitForTimeout(400);
 for(let i=0;i<7;i++){for(const v of A[i])await p.click('.cq2-opt[data-v="'+v+'"]');await p.click('#cq2-next');await p.waitForTimeout(200);}
 await p.click('#cq2-open');await p.waitForTimeout(300);log('no chat widget: status:',await p.$eval('#cq2-status',e=>e.innerText));
 await c.close();}
{const [c,p]=await ctxFor(false,{tag:'dark'});await p.goto('file://'+D+'/dark.html');await p.click('#cq2-toggle');await p.waitForTimeout(500);await p.click('.cq2-opt[data-v="wavy"]');await p.hover('.cq2-opt[data-v="curly"]');await p.waitForTimeout(300);await shot(p,'dark_q1');await c.close();}
{const c=await b.newContext({viewport:{width:1440,height:1000},reducedMotion:'reduce'});const p=await c.newPage();p.on('pageerror',e=>errs.push('rm: '+e.message));await p.goto('file://'+D+'/it.html');await p.click('#cq2-toggle');await p.click('.cq2-opt[data-v="wavy"]');await p.click('#cq2-next');log('reduced motion bar width',await p.$eval('.cq2-bar i',e=>e.style.width));await c.close();}
{const [c,p]=await ctxFor(false,{tag:'hover'});await p.goto('file://'+D+'/it.html');await p.click('#cq2-toggle');await p.waitForTimeout(500);await p.click('.cq2-opt[data-v="wavy"]');await p.hover('.cq2-opt[data-v="curly"]');await p.waitForTimeout(300);await shot(p,'hover_desk');await c.close();}
console.log(out.join('\n'));console.log('ERRORS',JSON.stringify(errs));await b.close();})();
