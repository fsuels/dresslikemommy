(()=>{
  function h(tag, attrs={}, children=[]) {
    const el=document.createElement(tag);
    for(const k in attrs){ if(k==='class') el.className=attrs[k]; else el.setAttribute(k, attrs[k]); }
    (Array.isArray(children)?children:[children]).forEach(c=>{
      if(typeof c==='string') el.appendChild(document.createTextNode(c)); else if(c) el.appendChild(c);
    });
    return el;
  }

  function mount(){
    const root=document.getElementById('dlm-agent-root');
    if(!root) return;
    const btn=h('button',{class:'dlm-agent-button',type:'button'},'Ask our Stylist');
    const panel=h('div',{class:'dlm-agent-panel',hidden:''});
    const log=h('div',{class:'dlm-agent-log'});
    const form=h('form',{class:'dlm-agent-form'});
    const input=h('input',{class:'dlm-agent-input',placeholder:'Ask about size, style, occasion…',type:'text'});
    const send=h('button',{class:'dlm-agent-send',type:'submit'},'Send');
    form.append(input,send);
    panel.append(log,form);
    root.append(btn,panel);

    btn.addEventListener('click',()=>{ panel.hidden=!panel.hidden; if(!panel.hidden) input.focus(); });
    form.addEventListener('submit', async (e)=>{
      e.preventDefault();
      const msg=input.value.trim(); if(!msg) return;
      input.value='';
      log.append(h('div',{class:'dlm-msg dlm-me'},msg));
      try{
        const session=localStorage.getItem('dlm_agent_sess')||null;
        const r=await fetch('/apps/agent/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({message:msg,session})});
        if(!r.ok) throw new Error('Network error');
        const j=await r.json();
        if(j.session) localStorage.setItem('dlm_agent_sess',j.session);
        if(j.reply) log.append(h('div',{class:'dlm-msg dlm-bot'},j.reply));
        if(Array.isArray(j.actions)){
          j.actions.forEach(a=>{
            if(a.type==='recommendations' && Array.isArray(a.items)){
              const wrap=h('div',{class:'dlm-recos'});
              a.items.forEach(it=>{
                const card=h('div',{class:'dlm-card'});
                if(it.image){ const img=h('img',{src:it.image,alt:it.title||'Recommended'}); card.append(img); }
                card.append(h('div',{class:'dlm-title'},it.title||''));
                if(it.price!=null) card.append(h('div',{class:'dlm-price'}, new Intl.NumberFormat(undefined,{style:'currency',currency:(j.currency||'USD')}).format((it.price/100)||0)));
                if(it.variantId){
                  const add=h('button',{type:'button',class:'dlm-add'},'Add to cart');
                  add.addEventListener('click',()=>{
                    fetch('/cart/add.js',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id:it.variantId,quantity:1})})
                      .then(()=>{ if(typeof publish==='function'){ publish('cart-update', {source:'agent'});} })
                      .catch(()=>{});
                  });
                  card.append(add);
                }
                wrap.append(card);
              });
              log.append(wrap);
            }
          });
        }
      }catch(err){ log.append(h('div',{class:'dlm-msg dlm-bot'},'Sorry, I had trouble. Please try again.')); }
      panel.scrollTop=panel.scrollHeight;
    });

    const style=`
    .dlm-agent-button{position:fixed;right:16px;bottom:16px;z-index:50;padding:10px 14px;border:0;border-radius:20px;background:#111;color:#fff;}
    .dlm-agent-panel{position:fixed;right:16px;bottom:64px;width:320px;max-height:60vh;overflow:auto;box-shadow:0 8px 24px rgba(0,0,0,.2);background:#fff;border-radius:12px;padding:10px;z-index:50}
    .dlm-agent-log{display:flex;flex-direction:column;gap:8px;margin-bottom:8px}
    .dlm-msg{padding:8px 10px;border-radius:10px;max-width:80%}
    .dlm-me{align-self:flex-end;background:#1f2937;color:#fff}
    .dlm-bot{align-self:flex-start;background:#f3f4f6}
    .dlm-agent-form{display:flex;gap:6px}
    .dlm-agent-input{flex:1;padding:8px;border:1px solid #ddd;border-radius:8px}
    .dlm-card{border:1px solid #eee;border-radius:8px;padding:8px;margin:6px 0;display:grid;grid-template-columns:56px 1fr;gap:8px;align-items:center}
    .dlm-card img{width:56px;height:56px;object-fit:cover;border-radius:6px}
    .dlm-title{font-size:14px;font-weight:600}
    .dlm-price{font-size:13px;color:#555}
    .dlm-add{justify-self:end;padding:6px 8px;border:0;border-radius:6px;background:#111;color:#fff}
    `;
    const s=document.createElement('style'); s.textContent=style; document.head.appendChild(s);
  }

  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded', mount); else mount();
})();

