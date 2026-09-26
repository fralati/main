// Uso: npm install terser csso ; node build.js <sorgente.src.liquid> <file-da-incollare.liquid>
// Comprime CSS e JS del blocco, blocca l'uscita se compaiono delimitatori Liquid, stampa le dimensioni.
const fs=require('fs'),{minify}=require('terser'),csso=require('csso');
const [src,out]=process.argv.slice(2);
(async()=>{let s=fs.readFileSync(src,'utf8');
const css=s.match(/<style>([\s\S]*?)<\/style>/)[1];
let mc=csso.minify(css,{restructure:false}).css;const V={ink:'i',bg:'b',acc:'a',line:'l',soft:'s',muted:'m',hi:'h',gl:'g',r:'r',g:'p'};mc=mc.replace(/--cq-([a-z]+)/g,(m,k)=>{if(!V[k])throw new Error('var '+k);return '--q'+V[k];});
const js=s.match(/<script>([\s\S]*?)<\/script>/)[1];
const mj=(await minify(js,{compress:{passes:2},mangle:{properties:{regex:/^(ask2|cont|cta|resume|ctaDone|next|back|finish|single|multi|max2|restart|sumProg|sumT|lead|howT|how1|how2|how2t|how3|cp|pst|noChat|copyFail|ct|openChat|showMsg|copyAgain|copied|confirmQ|confirmYes|confirmNo|hi|prof|ask|steps)$/}},format:{ascii_only:false,quote_style:1}})).code;
let o=s.replace(css,()=>mc).replace(js,()=>mj);
o=o.replace(/\n<div class="cq2"/,'<div class="cq2"').replace(/\n<script>/,'<script>');
const bad=(mj+mc).match(/\{\{|\{%/g);if(bad)throw new Error('liquid delimiters in output: '+bad);
fs.writeFileSync(out,o);const b=Buffer.byteLength(o);console.log('chars',o.length,'bytes',b,'json',JSON.stringify(o).length,'css',mc.length,'js',Buffer.byteLength(mj));})();
