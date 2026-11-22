/* ApexRide Nepal — main.js: nav drawer, reveal, gallery, calculators, filters, wizard, role switch, booking breakdown */
(function(){
"use strict";
const $=(s,c=document)=>c.querySelector(s), $$=(s,c=document)=>[...c.querySelectorAll(s)];
const fmt=n=>"Rs. "+Number(n||0).toLocaleString("en-NP");

/* --- Mobile drawer --- */
const drawer=$("#drawer"), overlay=$("#overlay");
function setDrawer(open){
  if(!drawer) return;
  drawer.classList.toggle("open",open); overlay.classList.toggle("show",open);
  document.body.style.overflow=open?"hidden":"";
}
$("#hamburger")?.addEventListener("click",()=>setDrawer(true));
$("#drawerClose")?.addEventListener("click",()=>setDrawer(false));
overlay?.addEventListener("click",()=>setDrawer(false));
$$("#drawer a").forEach(a=>a.addEventListener("click",()=>setDrawer(false)));

/* --- IntersectionObserver reveal --- */
const io=new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting){e.target.classList.add("visible");io.unobserve(e.target);}}),{threshold:.12});
$$(".reveal").forEach(el=>io.observe(el));

/* --- Hero video fallback: if autoplay blocked, poster image shows --- */
const vid=$(".hero-video");
if(vid){ const p=vid.play(); if(p) p.catch(()=>{ vid.style.display="none"; }); }

/* --- Respect reduced motion / low-power: pause drift animation --- */
if(window.matchMedia("(prefers-reduced-motion: reduce)").matches){ $$(".drift-car,.skid,.smoke,.speed-lines").forEach(e=>e.style.animation="none"); }

/* --- Featured fleet live calculator (days x daily rate) --- */
$$("[data-calc]").forEach(box=>{
  const input=$("input",box), out=$(".calc-total",box), rate=Number(box.dataset.calc);
  const update=()=>{ const d=Math.max(1,parseInt(input.value)||1); out.textContent=fmt(rate*d)+" / "+d+" day"+(d>1?"s":""); };
  input.addEventListener("input",update); update();
});

/* --- Fleet quick-preview modal --- */
const modal=$("#previewModal");
function openPreview(btn){
  if(!modal) return;
  $("#pmImg").src=btn.dataset.img; $("#pmTitle").textContent=btn.dataset.title;
  $("#pmMeta").textContent=btn.dataset.meta||""; $("#pmPrice").textContent=btn.dataset.price||"";
  $("#pmDesc").textContent=btn.dataset.desc||"";
  const link=$("#pmLink"); if(link) link.href=btn.dataset.link||"#";
  modal.classList.add("open"); document.body.style.overflow="hidden";
}
$$("[data-preview]").forEach(b=>b.addEventListener("click",()=>openPreview(b)));
$("#previewClose")?.addEventListener("click",()=>{modal.classList.remove("open");document.body.style.overflow="";});
modal?.addEventListener("click",e=>{if(e.target===modal){modal.classList.remove("open");document.body.style.overflow="";}});
document.addEventListener("keydown",e=>{if(e.key==="Escape"){modal?.classList.remove("open");$("#lightbox")?.classList.remove("open");setDrawer(false);}});

/* --- Mobile filter sidebar toggle --- */
$("#filterToggle")?.addEventListener("click",()=>$("#filterSidebar")?.classList.toggle("open"));

/* --- Vehicle gallery: swipe + lightbox --- */
const mainImg=$("#galMain"), thumbs=$$(".thumbs img");
let cur=0;
function show(i){
  if(!mainImg||!thumbs.length) return;
  cur=(i+thumbs.length)%thumbs.length;
  mainImg.src=thumbs[cur].src; mainImg.alt=thumbs[cur].alt||"Vehicle photo";
  thumbs.forEach((t,j)=>t.classList.toggle("active",j===cur));
  const c=$("#galCount"); if(c) c.textContent=(cur+1)+" / "+thumbs.length;
}
thumbs.forEach((t,i)=>t.addEventListener("click",()=>show(i)));
$("#galPrev")?.addEventListener("click",()=>show(cur-1));
$("#galNext")?.addEventListener("click",()=>show(cur+1));
mainImg?.addEventListener("click",()=>{ const lb=$("#lightbox"); if(lb){ $("#lbImg").src=mainImg.src; lb.classList.add("open"); }});
$("#lbClose")?.addEventListener("click",()=>$("#lightbox").classList.remove("open"));
$("#lightbox")?.addEventListener("click",e=>{if(e.target.id==="lightbox") e.target.classList.remove("open");});
/* touch swipe */
let tx=null;
mainImg?.addEventListener("touchstart",e=>{tx=e.changedTouches[0].clientX;},{passive:true});
mainImg?.addEventListener("touchend",e=>{ if(tx===null) return; const dx=e.changedTouches[0].clientX-tx; if(Math.abs(dx)>40) show(cur+(dx<0?1:-1)); tx=null; },{passive:true});

/* --- Booking price breakdown (date picker) --- */
const startEl=$("#startDate"), endEl=$("#endDate");
function breakdown(){
  const rate=Number($("#bookingWidget")?.dataset.rate||0);
  const cat=$("#bookingWidget")?.dataset.category||"car", tier=$("#bookingWidget")?.dataset.tier||"standard";
  if(!startEl?.value||!endEl?.value) return;
  const d1=new Date(startEl.value), d2=new Date(endEl.value);
  const days=Math.max(1, Math.round((d2-d1)/86400000)+1);
  if(d2<d1){ $("#bdError").textContent="Return date must be after pickup date."; return; }
  $("#bdError").textContent="";
  const sub=rate*days, fee=Math.round(sub*.05), vat=Math.round((sub+fee)*.13);
  const dep=cat==="cycle"?5000:cat==="bike"?15000:30000; const dep2=tier==="luxury"?dep*2:dep;
  const set=(id,v)=>{const el=$(id); if(el) el.textContent=v;};
  set("#bdDays",days+" day"+(days>1?"s":"")); set("#bdRate",fmt(rate));
  set("#bdSub",fmt(sub)); set("#bdFee",fmt(fee)); set("#bdVat",fmt(vat)); set("#bdDep",fmt(dep2));
  set("#bdTotal",fmt(sub+fee+vat)); set("#bdNow",fmt(sub+fee+vat+dep2));
  const sticky=$("#stickyPrice"); if(sticky) sticky.textContent=fmt(sub+fee+vat);
  // live server check (optional, non-blocking)
  const vid2=$("#bookingWidget")?.dataset.vehicle;
  if(vid2){ fetch("/api/calculate",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({vehicle_id:vid2,start_date:startEl.value,end_date:endEl.value})}).then(r=>r.json()).then(j=>{ if(!j.error){ set("#bdTotal",fmt(j.total)); set("#bdNow",fmt(j.payable_now)); } }).catch(()=>{}); }
}
[startEl,endEl].forEach(el=>el?.addEventListener("change",breakdown));
if(startEl){ const t=new Date(); startEl.min=t.toISOString().slice(0,10); }
if(endEl){ const t=new Date(Date.now()+86400000); endEl.min=t.toISOString().slice(0,10); }

/* --- Pricing tier selector (list-vehicle): LOCKS daily price --- */
const PRICE_MAP={"cycle|standard":500,"cycle|luxury":2000,"bike|standard":2000,"bike|luxury":7000,"car|standard":7000,"car|luxury":15000};
function lockPrice(){
  const cat=$("#vehCategory")?.value, tier=$("#vehTier")?.value, price=$("#dailyPrice"), note=$("#priceNote");
  if(!cat||!tier||!price) return;
  const p=PRICE_MAP[cat+"|"+tier];
  price.value=p; price.readOnly=true;
  if(note) note.textContent="Locked by ApexRide policy: "+cat+" / "+tier+" = Rs. "+p.toLocaleString("en-NP")+"/day. This price cannot be changed.";
}
$("#vehCategory")?.addEventListener("change",lockPrice);
$("#vehTier")?.addEventListener("change",lockPrice);
lockPrice();

/* --- Multi-step wizard --- */
let step=0; const steps=$$(".wizard-step"), indicators=$$(".step");
function goStep(n){
  step=Math.max(0,Math.min(steps.length-1,n));
  steps.forEach((s,i)=>s.classList.toggle("active",i===step));
  indicators.forEach((s,i)=>{ s.classList.toggle("active",i===step); s.classList.toggle("done",i<step); });
  window.scrollTo({top:0,behavior:"smooth"});
  if(step===3){ // review summary
    const g=id=>$(id)?.value||"—";
    const el=$("#reviewSummary"); if(el) el.innerHTML=
      "<b>"+g("#vehBrand")+" "+g("#vehModel")+"</b> ("+g("#vehYear")+") · "+g("#vehCategory")+" / "+g("#vehTier")+
      "<br>Daily price: <b>"+fmt($("#dailyPrice")?.value||0)+"</b> · "+g("#vehTransmission")+" · "+g("#vehFuel")+" · "+g("#vehLocation");
  }
}
$$("[data-next]").forEach(b=>b.addEventListener("click",()=>goStep(step+1)));
$$("[data-prev]").forEach(b=>b.addEventListener("click",()=>goStep(step-1)));
goStep(0);

/* --- Register role switch --- */
function setRole(role){
  $$(".role-opt").forEach(o=>o.classList.toggle("selected",o.dataset.role===role));
  const r=$("#roleInput"); if(r) r.value=role;
  const cf=$("#customerFields"), of=$("#ownerFields");
  cf?.style.setProperty("display",role==="customer"?"block":"none");
  of?.style.setProperty("display",role==="owner"?"block":"none");
  // Disable inputs in the hidden section so duplicate field names are not submitted
  $$("input,select,textarea",cf||document.createElement("div")).forEach(i=>i.disabled=(role!=="customer"));
  $$("input,select,textarea",of||document.createElement("div")).forEach(i=>i.disabled=(role!=="owner"));
  $("#roleTitle").textContent=role==="owner"?"List & Earn — Vehicle Owner":"Rent a Vehicle — Customer";
}
$$(".role-opt").forEach(o=>o.addEventListener("click",()=>setRole(o.dataset.role)));
if($("#roleInput")) setRole("customer");
/* Nepal phone helper */
$("#phoneInput")?.addEventListener("input",e=>{ e.target.value=e.target.value.replace(/\D/g,"").slice(0,10); });

/* --- Dashboard tabs --- */
$$(".tab-btn").forEach(b=>b.addEventListener("click",()=>{
  $$(".tab-btn").forEach(x=>x.classList.toggle("active",x===b));
  $$(".tab-panel").forEach(p=>p.classList.toggle("active",p.id==="tab-"+b.dataset.tab));
}));

/* --- FAQ accordion --- */
$$(".faq-q").forEach(q=>q.addEventListener("click",()=>{
  const item=q.closest(".faq-item"); const was=item.classList.contains("open");
  $$(".faq-item").forEach(i=>i.classList.remove("open"));
  if(!was) item.classList.add("open");
}));
})();
