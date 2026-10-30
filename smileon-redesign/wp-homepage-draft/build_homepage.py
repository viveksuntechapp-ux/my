import json, secrets, copy, sys
S=sys.argv[1]
draft=json.load(open(S+'/draft6836.json'))
home=json.load(open(S+'/home4103.json'))
css=open(S+'/sodc.css').read()

JUNKP=('pa_','premium_','eael_','hover_parallax','exad_')
def clean(e):
    e['settings']={k:v for k,v in e['settings'].items() if not k.startswith(JUNKP)}
    for c in e.get('elements',[]): clean(c)
    return e
idx={}
def index(els):
    for e in els: idx[e['id']]=e; index(e.get('elements',[]))
index(draft)
def tpl(i): return clean(copy.deepcopy(idx[i]))
def W(wt,**s): return {"id":"x","elType":"widget","widgetType":wt,"settings":s}
def C(settings,els): return {"id":"x","elType":"container","settings":settings,"elements":els}
SEC_PAD={"padding":{"unit":"px","top":72,"right":20,"bottom":72,"left":20,"isLinked":False},
         "padding_mobile":{"unit":"px","top":44,"right":16,"bottom":44,"left":16,"isLinked":False}}
def section(els,cls=None,gap=20):
    s={"flex_direction":"column","flex_gap":{"size":gap,"unit":"px","column":str(gap),"row":str(gap),"isLinked":True},**copy.deepcopy(SEC_PAD)}
    if cls: s["css_classes"]=cls
    return C(s,els)
def H2(t,align="center",cls="sodc-h2"): return W("heading",title=t,header_size="h2",align=align,_css_classes=cls)
def KICK(t,align="center"): return W("text-editor",editor=f"<p>{t}</p>",align=align,_css_classes="sodc-kicker")
def SUB(t,align="center"): return W("text-editor",editor=f"<p>{t}</p>",align=align,_css_classes="sodc-sub")
def L(url,ext=False): return {"url":url,"is_external":"on" if ext else "","nofollow":""}
def FA(v,lib="fa-solid"): return {"value":v,"library":lib}
U="https://smileondc.com"

# ===== 1. HERO (layout from location page, homepage copy) =====
hero=tpl('5a700001')
hl=hero['elements'][0]; hr=hero['elements'][1]
hl['elements'][0]['settings']['editor']="<p>Crafting Wholesome Smiles · Al Satwa, Dubai</p>"
hl['elements'][1]['settings']['title']="Specialist Dental Clinic in Dubai"
hl['elements'][1]['settings']['header_size']="h1"
hl['elements'][2]['settings']['editor']=("<p>From Invisalign and dental implants to teeth whitening and root canal care, we correct, repair and restore "
 "healthier smiles. Every treatment is carried out by a dentist who specialises in it, in one comfortable clinic on 2nd December Street. "
 "Open every day, 9am to 9pm.</p>")
ok=FA("fas fa-check-circle")
hl['elements'][4]['settings']['icon_list']=[
 {"_id":"t1","text":"Rated 5.0 on Google (333 reviews)","selected_icon":FA("fas fa-star")},
 {"_id":"t2","text":"DHA-licensed clinic","selected_icon":ok},
 {"_id":"t3","text":"Specialists in-house","selected_icon":ok},
 {"_id":"t4","text":"Same-day urgent appointments","selected_icon":ok}]
MEDIA={'Dr.Jeff_':(3833,"Dr. Jeffrey Manuel, Medical Director and Specialist Orthodontist at Smile On Dental Clinic, Dubai"),
 'Dr-Arunu':(3849,"Dr. Arun Devarajan, Specialist Endodontist at Smile On Dental Clinic, Dubai"),
 'Dr-Amit':(3850,"Dr. Amit Gupta, Specialist Oral and Maxillofacial Surgeon at Smile On Dental Clinic, Dubai"),
 'Dr-Rahul':(3851,"Dr. Rahul Patel, Specialist Prosthodontist at Smile On Dental Clinic, Dubai"),
 'Dr-Vineetha':(3852,"Dr. Vineetha Varughese, Specialist Periodontist at Smile On Dental Clinic, Dubai"),
 'Dr-Minu':(6816,"Dr. Minu Mumtaz O.V., Specialist Pediatric Dentist at Smile On Dental Clinic, Dubai")}
def fix_img(img):
    fn=img['url'].rsplit('/',1)[-1]
    for k,(mid,alt) in MEDIA.items():
        if fn.startswith(k): img.update(id=mid,alt=alt,source="library"); return
    raise SystemExit('no media for '+fn)
for im in hr['elements'][0]['elements']: fix_img(im['settings']['image'])
hr['elements'][1]['settings']['editor']="<p><strong>Meet your specialists</strong><br>Braces, root canals, implants, gums and kids, all in one clinic</p>"

# ===== 2. STATS =====
stats=tpl('5a700020')
for c,(n,suf,t) in zip(stats['elements'],[(333,'','Google reviews, rated 5.0'),(10,'+','Dentists and specialists'),(5,'+','Years caring for Dubai smiles'),(7,'','Days a week, 9am to 9pm')]):
    c['settings'].update(starting_number=0,ending_number=n,suffix=suf,title=t)

# ===== 3. SERVICES (16 tiles, live homepage list + cleaning/wisdom) =====
tile=clean(copy.deepcopy(idx['5a700044']))
SV=[("fas fa-teeth","Orthodontic Braces","Metal, ceramic, Damon and lingual braces with a specialist orthodontist.","/metal-ceramic-braces-dubai/","t"),
 ("fas fa-smile","Invisalign","Clear aligners for teens and adults from a certified Invisalign provider.","/invisalign-dubai/","t"),
 ("fas fa-grip-lines","Damon Braces","Self-ligating braces with fewer adjustments.","/damon-braces-dubai/","t"),
 ("fas fa-tooth","Dental Implants","Replace missing teeth, from a single implant to All-on-4.","/dental-implants-dubai/","p"),
 ("fas fa-bolt","Same Day Dental Implants","Leave with a temporary tooth on the day, when the implant is stable.","/same-day-dental-implants-dubai/","p"),
 ("fas fa-heartbeat","Root Canal Treatment","Save an infected tooth with a specialist endodontist.","/root-canal-treatment/","t"),
 ("fas fa-magic","Cosmetic Dentistry","Smile makeovers planned around your face and your bite.","/cosmetic-dentistry-dubai/","p"),
 ("fas fa-sun","Teeth Whitening","In-clinic and Zoom whitening for a brighter smile.","/teeth-whitening-dubai/","p"),
 ("fas fa-gem","Porcelain Veneers (Hollywood Smile)","Natural-looking veneers that reshape and brighten.","/porcelain-veneers-dubai/","p"),
 ("fas fa-crown","Dental Crowns & Bridges","Restore broken or missing teeth with lasting results.","/dental-crowns-bridges-dubai/","t"),
 ("fas fa-hand-holding-medical","Gum Disease Treatment","Periodontist-led care for bleeding or receding gums.","/gum-disease-treatment/","t"),
 ("fas fa-child","Children's Dentistry","Gentle visits with a specialist pediatric dentist.","/pediatric-dentistry-dubai/","p"),
 ("fas fa-stethoscope","Routine Dental Checkup","A full exam, with X-rays only when they're needed.","/dental-checkup-dubai/","t"),
 ("fas fa-spray-can","Teeth Cleaning","Scaling and polishing from AED 150.","/teeth-cleaning-dubai/","t"),
 ("fas fa-procedures","Full Mouth Rehabilitation","A complete plan to restore comfort, function and looks.","/full-mouth-rehabilitation-dubai/","p"),
 ("fas fa-tooth","Wisdom Tooth Extraction","Handled by our oral and maxillofacial surgeon.","/wisdom-tooth-extraction-dubai/","t")]
tiles=[]
for ic,t,dsc,url,col in SV:
    w=copy.deepcopy(tile); s=w['settings']
    s.update(selected_icon=FA(ic),title_text=t,description_text=dsc,link=L(U+url),primary_color="#2D9CA9" if col=="t" else "#6656C4")
    tiles.append(w)
services=section([KICK("Dental services"),H2("Dental Services Provided"),
  SUB("Whatever your smile needs, there's a specialist for it under one roof. Tap a treatment to see how it works and who carries it out."),
  C({"content_width":"full","css_classes":"sodc-grid sodc-grid-4"},tiles),
  W("button",text="View All Dental Services",link=L(U+"/dental-services/"),align="center",size="md",_css_classes="sodc-btn-ghost")],cls="sodc-tint")

# ===== 4. OFFERS (from the live announcement bar) =====
def ibox(icon,title,desc,cls,pc="#EEEBFA",sc="#6656C4"):
    return W("icon-box",selected_icon=FA(icon),view="stacked",primary_color=pc,secondary_color=sc,text_align="left",title_text=title,description_text=desc,_css_classes=cls)
offers=section([KICK("Offers"),H2("Offers Running Now"),
  C({"content_width":"full","css_classes":"sodc-grid sodc-grid-3"},[
    ibox("fas fa-child","Free Pediatric Consultation","Includes an X-ray and scaling for children. Ideal for a first visit.","sodc-card sodc-offer"),
    ibox("fas fa-tooth","Scaling & Polishing: AED 150","A professional clean to remove tartar and surface stains.","sodc-card sodc-offer",pc="#E8F6F7",sc="#2D9CA9"),
    ibox("fas fa-star","Scaling, Polishing & Whitening: AED 499","Clean and brighten your smile in one visit.","sodc-card sodc-offer sodc-offer-hot")]),
  W("button",text="Book an Offer",link=L(U+"/make-appointment/"),align="center",size="md",_css_classes="sodc-btn-grad"),
  W("text-editor",editor="<p>Offers are subject to availability and a dentist's assessment.</p>",align="center",_css_classes="sodc-sub sodc-small")])

# ===== 5. WHY CHOOSE US (live 6 points, rewritten) =====
card=lambda icon,t,dsc,teal: W("icon-box",selected_icon=FA(icon),view="stacked",primary_color="#E8F6F7" if teal else "#EEEBFA",
   secondary_color="#2D9CA9" if teal else "#6656C4",text_align="left",title_text=t,description_text=dsc,_css_classes="sodc-card")
why=section([KICK("Why choose us"),H2("Why Patients Across Dubai Choose Smile On"),
  SUB("Patient comfort and quality care come first. We combine experienced specialists with modern dental technology for an accurate diagnosis, safe procedures and reliable results."),
  C({"content_width":"full","css_classes":"sodc-grid sodc-grid-3"},[
    card("fas fa-user-md","Specialists for every treatment","An orthodontist, endodontist, oral surgeon, prosthodontist, periodontist and pediatric dentist all work here. No referral across town.",True),
    card("fas fa-star","Rated 5.0 by patients","A 5.0 rating on Google from 333 reviews by patients across Dubai.",True),
    card("fas fa-bolt","Same-day urgent care","Severe pain, a broken tooth or swelling? We keep slots open so you can usually be seen the day you call.",True),
    card("fas fa-x-ray","Modern dental technology","Digital X-rays and modern equipment for an accurate diagnosis, with your options and costs explained first.",False),
    card("fas fa-map-marker-alt","Central Al Satwa location","On 2nd December Street, easy to reach from Jumeirah, Bur Dubai, Karama and across Dubai.",False),
    card("fas fa-award","Founded by specialists","Established in 2021 by Dr. Arun Devarajan and Dr. Jeffrey Manuel, with five years of trusted dental care in Dubai.",False)])])

# ===== 6. TEAM (6-across doctor grid from the location page) =====
team=tpl('5a700060')
team['settings'].update(copy.deepcopy(SEC_PAD)); team['settings']['css_classes']="sodc-tint"
team['elements'][0]['settings']['title']="Meet Our Specialist Team"
team['elements'][1]['settings']['editor']="<p>Six specialists work alongside our general dentists, so even complex cases are planned and treated in the same building.</p>"
team['elements'].insert(0,KICK("Our team"))
for dbox in team['elements'][3]['elements']: fix_img(dbox['settings']['image'])
team['elements'][-1]['settings']['text']="Meet the Full Team"

# ===== 7. REVIEWS =====
reviews=section([KICK("Patient reviews"),H2("What Our Patients Say"),
  SUB("Rated 5.0 on Google by patients from Al Satwa, Jumeirah and across Dubai."),
  W("shortcode",shortcode="[grw id=5630]",_css_classes="sodc-reviews")])

# ===== 8. FIRST VISIT =====
steps=tpl('5a700090')
steps['settings'].update(copy.deepcopy(SEC_PAD)); steps['settings']['css_classes']="sodc-tint"
steps['elements'].insert(0,KICK("Your first visit"))
st=steps['elements'][2]['elements']
TX=[("1. Book a time","Book online, call or send a WhatsApp message. If you're in pain, tell us and we'll look for the earliest slot."),
 ("2. Meet your dentist","We listen first, then check your teeth and gums. X-rays are taken only when they're needed for a diagnosis."),
 ("3. Your plan, explained","You hear what we found, your options and what each one costs, with no pressure to decide on the day."),
 ("4. Treatment by the right specialist","When you're ready, the specialist for your treatment takes over, in the same clinic.")]
for b,(t,dsc) in zip(st,TX): b['settings'].update(title_text=t,description_text=dsc)
steps['elements'][3]['settings']['editor']="<p><strong>Insurance and payment.</strong> We work with a range of insurance providers and offer flexible payment options for treatment your plan doesn't cover. Send us your insurance details when you book and we'll confirm your cover before your visit.</p>"

# ===== 9. BLOG (live homepage's Royal Addons grid, trimmed to 3 posts) =====
blog_w=None
def findw(els):
    global blog_w
    for e in els:
        if e.get('widgetType')=='wpr-grid': blog_w=clean(copy.deepcopy(e))
        findw(e.get('elements',[]))
findw(home)
blog_w['settings']['query_posts_per_page']=3
blog=section([KICK("From our blog"),H2("Dental Tips From Our Specialists"),blog_w,
  W("button",text="View All Blogs",link=L(U+"/blogs/"),align="center",size="md",_css_classes="sodc-btn-ghost")])

# ===== 10. LOCATION + CONTACT FORM =====
find=tpl('5a700080')
find['settings'].update(copy.deepcopy(SEC_PAD)); find['settings']['css_classes']="sodc-tint"
find['elements'][0]['settings']['title']="Visit Us or Send a Message"
find['elements'].insert(0,KICK("Location & contact"))
right=find['elements'][2]['elements'][1]
right['elements'][0]['settings']['title']="Smile On Dental Clinic"
il=right['elements'][1]['settings']['icon_list']
il.append({"_id":"v5","text":"info@smileondc.com","selected_icon":FA("fas fa-envelope"),"link":L("mailto:info@smileondc.com")})
right['elements'][2]=W("shortcode",shortcode='[gravityform id="2" title="false"]',_css_classes="sodc-form")
# keep the Get Directions button after the form

# ===== 11. FAQ (live 6 + hours + children) =====
faq=tpl('5a7000a0')
faq['elements'][0]['settings']['title']="Frequently Asked Questions"
faq['elements'].insert(0,KICK("FAQ"))
Q=[("What dental services does Smile On Dental Clinic offer?","<p>We offer a full range of dental care under one roof, including general and preventive dentistry, cosmetic treatments like teeth whitening and veneers, orthodontics including Invisalign and braces, dental implants, root canal treatment, gum treatments and pediatric dentistry for children. <a href='https://smileondc.com/dental-services/'>See all dental services</a>.</p>"),
 ("Where is Smile On Dental Clinic located?","<p>Our clinic is in Al Satwa, Dubai, at Unit 213, AMKM Investment Building, 2nd December Street. We're easy to reach from Jumeirah, Bur Dubai and other nearby areas.</p>"),
 ("What are your opening hours?","<p>We're open every day of the week, from 9am to 9pm.</p>"),
 ("Do you accept insurance or offer payment plans?","<p>We work with a range of insurance providers and also offer flexible payment options for treatments not covered by insurance. Contact our team before your visit and we'll confirm your coverage.</p>"),
 ("Can I get a same-day emergency dental appointment?","<p>Yes. We keep slots open for urgent dental concerns such as severe pain, broken teeth or swelling, so you can usually be seen the same day you call <a href='tel:+971558961826'>+971 55 896 1826</a>.</p>"),
 ("Do you treat children?","<p>Yes. Our specialist pediatric dentist, <a href='https://smileondc.com/doctors/dr-minu-mumtaz/'>Dr. Minu Mumtaz O.V.</a>, sees babies, children and teens. Ask about our free pediatric consultation.</p>"),
 ("How do I book an appointment?","<p>Call us directly at <a href='tel:+971558961826'>+971 55 896 1826</a> or <a href='https://smileondc.com/make-appointment/'>book online</a>. Our team will confirm your appointment time and send you a reminder before your visit.</p>"),
 ("What languages do your doctors speak?","<p>Our team is multilingual and comfortable treating patients in English along with several other languages. Let our front desk know your preference when you book and we'll do our best to accommodate you.</p>")]
faq['elements'][2]['settings']['tabs']=[{"_id":f"q{n+1}","tab_title":q,"tab_content":a} for n,(q,a) in enumerate(Q)]

# ===== 12. CLOSING CTA =====
cta=tpl('5a7000b0')
cta['elements'][0]['settings']['title']="Ready for a Healthier, Brighter Smile?"
cta['elements'][1]['settings']['editor']="<p>Specialists in-house, same-day urgent slots and a 5.0 Google rating. Open every day, 9am to 9pm.</p>"

# ===== page CSS: location-page styles rescoped to this page only, plus new pieces =====
extra = """
/* Homepage additions */
body .sodc-css{display:none!important}
body .sodc-kicker p{display:inline-block;margin:0;padding:6px 14px;border-radius:999px;background:#EEEBFA;color:#6656C4;font-size:13px;font-weight:600;letter-spacing:.06em;text-transform:uppercase}
body .sodc-kicker{margin-bottom:-6px}
body .sodc-offer{border-top:4px solid var(--sodc-violet)}
body .sodc-offer .elementor-icon-box-title{font-size:20px}
body .sodc-offer-hot{background:linear-gradient(135deg,#6656C4 0%,#4f43a8 100%);border-color:transparent;border-top-color:#f5a623}
body .sodc-offer-hot .elementor-icon-box-title,body .sodc-offer-hot .elementor-icon-box-description{color:#fff!important}
body .sodc-offer-hot .elementor-icon{background-color:rgba(255,255,255,.18)!important;color:#fff!important;fill:#fff!important}
body .sodc-small p{font-size:14px}
body .sodc-reviews,body .wpr-grid{max-width:1140px;margin-left:auto;margin-right:auto;width:100%}
body .sodc-form{background:#fff;border:1px solid var(--sodc-line);border-radius:16px;padding:18px}
body .sodc-tile .elementor-icon-box-title,body .sodc-tile .elementor-icon-box-title a{font-size:16px}
@media (max-width:600px){body .sodc-tile{padding:16px}}
"""
scoped=css.replace('.page-id-6836','body')+extra
style_holder=C({"content_width":"full","padding":{"unit":"px","top":0,"right":0,"bottom":0,"left":0,"isLinked":True},"css_classes":"sodc-css"},
  [W("html",html="<style id=\"sodc-home-css\">\n"+scoped+"\n</style>")])

page=[style_holder,hero,stats,services,offers,why,team,reviews,steps,blog,find,faq,cta]
used=set()
def reid(els):
    for e in els:
        while True:
            x=secrets.token_hex(4)
            if x not in used: used.add(x); break
        e['id']=x; reid(e.get('elements',[]))
reid(page)
payload={"title":"Home (New Design, Draft)","status":"draft","template_type":"wp-page","page_template":"elementor_header_footer","data":page}
s=json.dumps(payload,ensure_ascii=False,separators=(',',':'))
open(S+'/payload.json','w').write(s)
print('chars',len(s),'widgets',s.count('"elType":"widget"'))
