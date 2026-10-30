import json, secrets, copy, sys
S=sys.argv[1]
p=json.load(open(S+'/payload.json')); d=p['data']
def W(wt,**s): return {"id":"x","elType":"widget","widgetType":wt,"settings":s}
def C(settings,els): return {"id":"x","elType":"container","settings":settings,"elements":els}
def L(url,ext=False): return {"url":url,"is_external":"on" if ext else "","nofollow":""}
def FA(v,lib="fa-solid"): return {"value":v,"library":lib}
PAD={"padding":{"unit":"px","top":72,"right":20,"bottom":72,"left":20,"isLinked":False},"padding_mobile":{"unit":"px","top":44,"right":16,"bottom":44,"left":16,"isLinked":False}}
def section(els,cls="",gap=20):
    return C({"flex_direction":"column","flex_gap":{"size":gap,"unit":"px","column":str(gap),"row":str(gap),"isLinked":True},**copy.deepcopy(PAD),"css_classes":cls},els)
def KICK(t): return W("text-editor",editor=f"<p>{t}</p>",align="center",_css_classes="sodc-kicker")
def H2(t,align="center"): return W("heading",title=t,header_size="h2",align=align,_css_classes="sodc-h2")
def SUB(t,align="center"): return W("text-editor",editor=f"<p>{t}</p>",align=align,_css_classes="sodc-sub")
TEL="tel:+971558961826"; U="https://smileondc.com"
CALL=lambda txt="Call +971 55 896 1826",cls="sodc-btn-grad",align=None: W("button",text=txt,link=L(TEL),size="md",selected_icon=FA("fas fa-phone-alt"),_css_classes=cls,**({"align":align} if align else {}))

css_holder,hero,stats,services,offers,why,team,reviews,steps,blog,find,faq,cta=d

# --- move page CSS into the hero (no separate top-level block) and add new rules ---
style=css_holder['elements'][0]
extra="""
/* v2: logged-in admin bar gap (preview only), swipe sliders on mobile, new sections */
body.admin-bar .sodc-sat-hero{margin-top:-32px}
@media (max-width:782px){body.admin-bar .sodc-sat-hero{margin-top:-46px}}
body .sodc-sat-hero>.sodc-css,body .sodc-sat-hero .elementor-widget-html.sodc-css{display:none!important}
body .sodc-swipe-hint{display:none}
@media (max-width:767px){
body .sodc-swipe{display:flex!important;flex-wrap:nowrap!important;overflow-x:auto;scroll-snap-type:x mandatory;gap:14px!important;margin-right:-16px;padding:4px 16px 12px 0;scrollbar-width:none;-webkit-overflow-scrolling:touch}
body .sodc-swipe::-webkit-scrollbar{display:none}
body .sodc-swipe>.elementor-element{flex:0 0 78%!important;max-width:78%;scroll-snap-align:start}
body .sodc-docs.sodc-swipe>.elementor-element{flex-basis:58%!important;max-width:58%}
body .sodc-swipe-hint{display:block}
body .sodc-swipe-hint p{font-size:13px;color:var(--sodc-muted);margin:0;text-align:right}
}
body .sodc-emergency{background:linear-gradient(90deg,#1f7c87 0%,#4f43a8 100%)}
body .sodc-emergency .elementor-icon-box-title{color:#fff!important;font-family:Rubik,sans-serif;font-size:20px;font-weight:600;margin:0 0 2px}
body .sodc-emergency .elementor-icon-box-description{color:rgba(255,255,255,.9)!important;font-size:15px}
body .sodc-emergency .elementor-icon{background:rgba(255,255,255,.16)!important;color:#fff!important;fill:#fff!important}
body .sodc-about-img img{width:100%;aspect-ratio:4/3;object-fit:cover;border-radius:22px;box-shadow:0 18px 40px rgba(29,39,51,.14)}
body .sodc-about .sodc-h2 .elementor-heading-title{text-align:left}
body .sodc-ba .elementor-image-box-img{width:100%!important;margin:0 0 12px!important}
body .sodc-ba img{width:100%;aspect-ratio:4/3;object-fit:cover;border-radius:16px}
body .sodc-ba .elementor-image-box-title{font-family:Rubik,sans-serif;font-size:17px;font-weight:600;color:var(--sodc-ink)}
body .sodc-ba .elementor-image-box-description{font-size:14px;color:var(--sodc-muted)}
body .sodc-ins{background:#fff;border:1px solid var(--sodc-line);border-radius:22px;max-width:1140px;margin:0 auto}
body .sodc-ins .elementor-icon-box-title{font-family:Rubik,sans-serif;font-size:22px;font-weight:700;color:var(--sodc-ink)}
body .sodc-ins .elementor-icon-box-description{color:var(--sodc-muted);font-size:15px}
"""
style['settings']['html']=style['settings']['html'].replace('\n</style>',extra+'\n</style>')
style['settings']['_css_classes']="sodc-css"
hero['elements'].insert(0,style)

# --- HERO: Call is the main action ---
btnrow=hero['elements'][1]['elements'][3]
btnrow['elements']=[CALL(),W("button",text="Book Online",link=L(U+"/make-appointment/"),size="md",selected_icon=FA("fas fa-calendar-check"),_css_classes="sodc-btn-ghost")]
hero['elements'][1]['elements'][2]['settings']['editor']=("<p>From Invisalign and dental implants to teeth whitening and root canal care, we correct, repair and restore healthier smiles. "
 "Every treatment is carried out by a dentist who specialises in it, in one comfortable clinic on 2nd December Street. Call us today, we're open every day, 9am to 9pm.</p>")

# --- STATS: stronger set ---
for c,(n,suf,t) in zip(stats['elements'],[(5,'.0 ★','Google rating, 333 reviews'),(6,'','In-house specialists'),(8,'','Dental specialties'),(12,' hrs','Open every day, 9am to 9pm')]):
    c['settings'].update(starting_number=0,ending_number=n,suffix=suf,title=t)

# --- EMERGENCY STRIP ---
emergency=C({"flex_direction":"row","flex_wrap":"wrap","flex_align_items":"center","flex_justify_content":"space-between","flex_gap":{"size":20,"unit":"px","column":"20","row":"16","isLinked":False},
  "padding":{"unit":"px","top":28,"right":20,"bottom":28,"left":20,"isLinked":False},"css_classes":"sodc-emergency"},[
  W("icon-box",selected_icon=FA("fas fa-tooth"),view="stacked",position="inline-start",primary_color="#ffffff",secondary_color="#2D9CA9",
    title_text="Dental pain or a broken tooth?",description_text="We keep same-day urgent slots open every day, 9am to 9pm. Call and tell us it's urgent.",title_size="h3"),
  CALL("Call Now: +971 55 896 1826","sodc-btn-white")])

# --- ABOUT / OUR STORY ---
about=C({"flex_direction":"row","flex_wrap":"wrap","flex_align_items":"center","flex_gap":{"size":48,"unit":"px","column":"48","row":"28","isLinked":False},**copy.deepcopy(PAD),"css_classes":"sodc-about"},[
  C({"content_width":"full","width":{"unit":"%","size":46},"width_mobile":{"unit":"%","size":100}},[
    W("image",image={"url":U+"/wp-content/uploads/2026/01/meet-the-team.jpg","id":4602,"alt":"The Smile On Dental Clinic team at the clinic in Al Satwa, Dubai","source":"library"},image_size="large",_css_classes="sodc-about-img")]),
  C({"content_width":"full","width":{"unit":"%","size":48},"width_mobile":{"unit":"%","size":100},"flex_direction":"column","flex_gap":{"size":16,"unit":"px","column":"16","row":"16","isLinked":True}},[
    W("text-editor",editor="<p>About us</p>",_css_classes="sodc-kicker"),
    W("heading",title="A One-Stop Dental Clinic for the Whole Family",header_size="h2",_css_classes="sodc-h2"),
    W("text-editor",editor=("<p>Smile On Dental Clinic LLC is a one-stop place for all your dental concerns. Established in 2021 by Dr. Arun Devarajan and Dr. Jeffrey Manuel, "
      "we offer a wide range of dental care in a well-equipped clinic, with a team of experienced doctors who truly care about your dental health.</p>"
      "<p>We combine the latest cosmetic techniques with proven treatment plans to correct and restore your smile. Every plan is personalised, "
      "from preventive and pediatric care to cosmetic and specialist treatment, so you get the right care from the right dentist.</p>"),_css_classes="sodc-lead"),
    C({"content_width":"full","flex_direction":"row","flex_wrap":"wrap","flex_gap":{"size":12,"unit":"px","column":"12","row":"12","isLinked":True}},[
      CALL("Call Us"),W("button",text="Know More About Us",link=L(U+"/about-us/"),size="md",_css_classes="sodc-btn-ghost")])])])

# --- SERVICES: swipe on mobile, Call next to view-all ---
grid=services['elements'][3]; grid['settings']['css_classes']+=" sodc-swipe"
services['elements'].insert(3,W("text-editor",editor="<p>Swipe to see all treatments →</p>",_css_classes="sodc-swipe-hint"))
vb=services['elements'].pop()
services['elements'].append(C({"content_width":"full","flex_direction":"row","flex_wrap":"wrap","flex_justify_content":"center","flex_gap":{"size":12,"unit":"px","column":"12","row":"12","isLinked":True}},[
  CALL("Not sure? Call +971 55 896 1826"),vb]))
services['elements'][2]['settings']['editor']="<p>Whatever your smile needs, there's a specialist for it under one roof. Tap a treatment to learn more, or call us and we'll point you to the right dentist.</p>"

# --- OFFERS: call to book ---
offers['elements'][3]=CALL("Call to Book an Offer",align="center")

# --- WHY: avoid repeating the About story ---
cards=why['elements'][3]['elements']
cards[5]['settings'].update(selected_icon=FA("fas fa-hand-holding-heart"),title_text="Clear costs, no pressure",
  description_text="Your options and what each one costs are explained before anything starts. No upselling and no manufactured urgency.")
cards[3]['settings']['description_text']="Digital X-rays and modern equipment for an accurate diagnosis, safe procedures and reliable results."

# --- BEFORE & AFTER ---
def ba(mid,url,alt,title,desc):
    return W("image-box",image={"url":url,"id":mid,"alt":alt,"source":"library"},title_text=title,description_text=desc,title_size="h3",_css_classes="sodc-ba sodc-card")
before_after=section([KICK("Results"),H2("Before & After Smiles"),
  SUB("A few of the smile transformations completed at our clinic. Every result depends on the patient, and your dentist will explain what's realistic for you."),
  C({"content_width":"full","css_classes":"sodc-grid sodc-grid-3 sodc-swipe"},[
    ba(6127,U+"/wp-content/uploads/2026/06/Hollywood-Smile-result-at-Smile-On-Dental-Clinic-Dubai.webp","Hollywood Smile before and after at Smile On Dental Clinic, Dubai","Hollywood Smile","Porcelain veneers to reshape and brighten the smile."),
    ba(5781,U+"/wp-content/uploads/2026/04/before_after_merged.png","Orthodontic treatment before and after at Smile On Dental Clinic, Dubai","Orthodontic Treatment","Crowded teeth straightened with braces."),
    ba(5614,U+"/wp-content/uploads/2026/03/Composite-Bonding-Before-and-After.png","Composite bonding before and after at Smile On Dental Clinic, Dubai","Composite Bonding","Chips and gaps repaired in a single visit.")]),
  W("text-editor",editor="<p>Want to know what's possible for your smile?</p>",align="center",_css_classes="sodc-sub"),
  CALL("Call for a Smile Consultation",align="center")])

# --- TEAM: swipe on mobile ---
team['elements'][3]['settings']['css_classes']+=" sodc-swipe"
team['elements'].insert(3,W("text-editor",editor="<p>Swipe to meet the team →</p>",_css_classes="sodc-swipe-hint"))

# --- INSURANCE STRIP ---
insurance=section([C({"flex_direction":"row","flex_wrap":"wrap","flex_align_items":"center","flex_justify_content":"space-between","flex_gap":{"size":20,"unit":"px","column":"20","row":"16","isLinked":False},
   "padding":{"unit":"px","top":28,"right":28,"bottom":28,"left":28,"isLinked":True},"css_classes":"sodc-ins"},[
  W("icon-box",selected_icon=FA("fas fa-shield-alt"),view="stacked",position="inline-start",primary_color="#E8F6F7",secondary_color="#2D9CA9",title_size="h2",
    title_text="Insurance Accepted",description_text="We work with most major UAE health insurance providers and offer flexible payment options. Call us with your insurance details and we'll confirm your cover before your visit."),
  CALL("Check My Cover")])])
insurance['settings']['padding']={"unit":"px","top":8,"right":20,"bottom":56,"left":20,"isLinked":False}

# --- FIRST VISIT step 1 mentions calling first ---
steps['elements'][2]['elements'][0]['settings']['description_text']="Call us, send a WhatsApp message or book online. If you're in pain, tell us and we'll find the earliest slot."

# --- VISIT card: call button first ---
right=find['elements'][2]['elements'][1]
right['elements'].insert(2,CALL())
right['elements'][-1]['settings']['_css_classes']="sodc-btn-ghost"

# --- CTA: call first ---
row=cta['elements'][2]['elements']
row[0]=CALL("Call +971 55 896 1826","sodc-btn-white"); row[2]=W("button",text="Book Online",link=L(U+"/make-appointment/"),size="md",_css_classes="sodc-btn-outline-white")
cta['elements'][1]['settings']['editor']="<p>Call us now for an appointment or advice. Specialists in-house, same-day urgent slots and a 5.0 Google rating. Open every day, 9am to 9pm.</p>"

# --- FAQ booking answer leads with phone ---
for t in faq['elements'][2]['settings']['tabs']:
    if t['tab_title'].startswith('How do I book'):
        t['tab_content']="<p>The quickest way is to call us on <a href='tel:+971558961826'>+971 55 896 1826</a>, every day from 9am to 9pm. You can also <a href='https://wa.me/971558961826'>send a WhatsApp message</a> or <a href='https://smileondc.com/make-appointment/'>book online</a>, and our team will confirm your appointment and send you a reminder.</p>"

page=[hero,stats,emergency,about,services,offers,why,before_after,team,reviews,insurance,steps,blog,find,faq,cta]
# alternate backgrounds (hero, stats, emergency, cta have their own)
tint=[about,offers,before_after,reviews,steps,find]; plain=[services,why,team,insurance,blog]
for s_ in tint+plain:
    cls=[c for c in s_['settings'].get('css_classes','').split() if c!='sodc-tint']
    if s_ in tint: cls.append('sodc-tint')
    s_['settings']['css_classes']=' '.join(cls)
faq['settings']['css_classes']='sodc-faq'
used=set()
def reid(els):
    for e in els:
        while True:
            x=secrets.token_hex(4)
            if x not in used: used.add(x); break
        e['id']=x; reid(e.get('elements',[]))
reid(page)
body={"id":6845,"data":page}
s=json.dumps(body,ensure_ascii=False,separators=(',',':'))
open(S+'/payload2.json','w').write(s)
print('chars',len(s),'widgets',s.count('"elType":"widget"'),'calls',s.count('tel:+971558961826'))
