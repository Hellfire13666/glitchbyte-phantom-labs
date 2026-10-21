(function(){
'use strict';
const COMMANDS={
  'hexbazaar':'cd "$HOME/PhantomLabsLaunchers/hexbazaar-savage-intel-shop-v0_1_2_rc1_rosie_savage" &&\npython3 -B hexbazaar_savage_intel_shop_v0_1_2_rc1.py --color always demo',
  'phantom-spine':"\"$HOME/.local/bin/phantom-spine-live-v020\" hunt example.com --engine native --providers dns --timeout 8",
  'riftseal':'sha256sum "$HOME/Downloads/your-own-file.zip"',
  'reports':'mkdir -p -m 700 "$HOME/GlitchBytePrivateReports"',
};
function flash(button, message, orig){button.textContent=message;window.setTimeout(()=>button.textContent=orig,1900)}
async function copyToClipboard(str, button, orig){
 try{if(navigator.clipboard?.writeText){await navigator.clipboard.writeText(str);flash(button,'✓ Copied',orig);return}}
 catch(e){}
 const el=document.createElement('textarea');el.value=str;el.style.cssText='position:fixed;left:-9999px;top:0';document.body.appendChild(el);el.focus();el.select();let ok=false;try{ok=document.execCommand('copy')}catch(e){}el.remove();
 flash(button,ok?'✓ Copied':'Select text manually',orig);
}
document.querySelectorAll('.copy').forEach(b=>b.addEventListener('click',()=>{
 const pre=b.closest('.recipe')?.querySelector('pre');if(pre)copyToClipboard(pre.innerText||pre.textContent,b,'Copy command');
}));
document.querySelectorAll('.copy-switch').forEach(b=>b.addEventListener('click',()=>{
 const command=COMMANDS[b.dataset.command];if(command)copyToClipboard(command,b,'Copy easy command');
}));
const rows=Array.isArray(window.GB_CATALOG)?window.GB_CATALOG:[];
const list=document.querySelector('#catalog-list'),input=document.querySelector('#catalog-search'),counter=document.querySelector('#catalog-count');
if(list){
 const render=()=>{
  const q=(input?.value||'').trim().toLowerCase();list.textContent='';
  const filtered=rows.filter(r=>!q||[r.project,r.title,r.type].join(' ').toLowerCase().includes(q));
  if(counter)counter.textContent=filtered.length+' page'+(filtered.length===1?'':'s')+' found';
  if(!filtered.length){const empty=document.createElement('div');empty.className='empty';empty.textContent=rows.length?'No pages match your search.':'No external tool HTML pages found. Your built-in recipes and manuals still work.';list.appendChild(empty);return}
  filtered.forEach(r=>{const card=document.createElement('div');card.className='catalog-item';const a=document.createElement('a');a.textContent=r.title;a.href=r.href;card.appendChild(a);const sub=document.createElement('small');sub.textContent=r.project+' · '+r.type;card.appendChild(sub);list.appendChild(card)});
 };if(input)input.addEventListener('input',render);render();
}
for(const card of document.querySelectorAll('.switch-card[data-tool]')){
 const kind=card.dataset.tool;
 if(!['hexbazaar','phantom-spine','riftseal'].includes(kind))continue;
 const candidates=rows.filter(r=>{const p=(r.project||'').toLowerCase();return p.includes(kind.replace('-', ' '))||p.replaceAll(' ','').includes(kind.replaceAll('-',''))});
 const score=r=>{const href=r.href||'';if(kind==='phantom-spine')return (href.includes('phantom-spine-live-signal-v0_2_0/')?200:0)+(href.includes('phantom-spine-live-signal-v0_2_0_rc2/')?100:0)+(r.title==='Main shop page'?20:0);return (href.includes('rosie_facebook_recipes')?100:0)+(href.includes('v0_1_2')?50:0)+(r.title==='Main shop page'?15:0)+(r.title==='Facebook recipes'?8:0)};
 const home=candidates.slice().sort((a,b)=>score(b)-score(a))[0];
 const link=card.querySelector('.switch-open'), status=card.querySelector('.switch-status');
 if(home){link.href=home.href;link.classList.remove('unavailable');link.removeAttribute('aria-disabled');link.textContent='↗ Open installed page';status.textContent='✓ '+candidates.length+' installed page'+(candidates.length===1?'':'s')+' found';status.classList.add('ready');}
 else{link.removeAttribute('href');link.classList.add('unavailable');link.setAttribute('aria-disabled','true');link.textContent='Not detected';status.textContent='No local HTML page detected · recipes still work';status.classList.add('pending');}
}
})();
