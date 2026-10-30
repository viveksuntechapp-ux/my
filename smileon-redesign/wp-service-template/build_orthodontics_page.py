import json, secrets, copy, sys
S=sys.argv[1]
home=json.load(open(S+'/payload2.json'))['data']
base_css=home[0]['elements'][0]['settings']['html']          # homepage style block (design system)
wpr=None
def findw(els):
    global wpr
    for e in els:
        if e.get('widgetType')=='wpr-grid': wpr=copy.deepcopy(e)
        findw(e.get('elements',[]))
findw(home)

def W(wt,**s): return {"id":"x","elType":"widget","widgetType":wt,"settings":s}
def C(settings,els): return {"id":"x","elType":"container","settings":settings,"elements":els}
def L(url,ext=False): return {"url":url,"is_external":"on" if ext else "","nofollow":""}
def FA(v,lib="fa-solid"): return {"value":v,"library":lib}
def GAP(n,row=None): return {"size":n,"unit":"px","column":str(n),"row":str(row if row is not None else n),"isLinked":row is None}
PAD={"padding":{"unit":"px","top":72,"right":20,"bottom":72,"left":20,"isLinked":False},"padding_mobile":{"unit":"px","top":44,"right":16,"bottom":44,"left":16,"isLinked":False}}
def section(els,cls="",gap=20,row=False):
    s={"flex_direction":"row" if row else "column","flex_gap":GAP(gap),**copy.deepcopy(PAD),"css_classes":cls}
    if row: s.update(flex_wrap="wrap",flex_align_items="center")
    return C(s,els)
def col(w,els,gap=16,cls=""):
    return C({"content_width":"full","width":{"unit":"%","size":w},"width_mobile":{"unit":"%","size":100},"flex_direction":"column","flex_gap":GAP(gap),"css_classes":cls},els)
def row(els,justify=None,gap=12):
    s={"content_width":"full","flex_direction":"row","flex_wrap":"wrap","flex_gap":GAP(gap)}
    if justify: s["flex_justify_content"]=justify
    return C(s,els)
def KICK(t,align="center"): return W("text-editor",editor=f"<p>{t}</p>",**({"align":align} if align else {}),_css_classes="sodc-kicker")
def H(t,tag="h2",align="center",cls="sodc-h2"): return W("heading",title=t,header_size=tag,**({"align":align} if align else {}),_css_classes=cls)
def SUB(t,align="center"): return W("text-editor",editor=f"<p>{t}</p>",**({"align":align} if align else {}),_css_classes="sodc-sub")
def TXT(html,cls="sodc-lead"): return W("text-editor",editor=html,_css_classes=cls)
TEL="tel:+971558961826"; U="https://smileondc.com"
def CALL(txt="Call +971 55 896 1826",cls="sodc-btn-grad",align=None,tel=TEL):
    return W("button",text=txt,link=L(tel),size="md",selected_icon=FA("fas fa-phone-alt"),_css_classes=cls,**({"align":align} if align else {}))
def BTN(txt,url,cls="sodc-btn-ghost",icon=None,ext=False,align=None):
    s=dict(text=txt,link=L(url,ext),size="md",_css_classes=cls)
    if icon: s["selected_icon"]=FA(*icon) if isinstance(icon,tuple) else FA(icon)
    if align: s["align"]=align
    return W("button",**s)
def card(icon,t,dsc,teal=True,cls="sodc-card",link=None):
    s=dict(selected_icon=FA(icon),view="stacked",primary_color="#E8F6F7" if teal else "#EEEBFA",secondary_color="#2D9CA9" if teal else "#6656C4",
           text_align="left",title_text=t,description_text=dsc,title_size="h3",_css_classes=cls)
    if link: s["link"]=L(link)
    return W("icon-box",**s)
def grid(cls,els): return C({"content_width":"full","css_classes":cls},els)
def IMG(mid,url,alt,cls,size="large"): return W("image",image={"url":url,"id":mid,"alt":alt,"source":"library"},image_size=size,_css_classes=cls)

extra_css = """
/* Service page template (orthodontics first) */
body .sodc-hero-photo img{width:100%;aspect-ratio:4/5;object-fit:cover;object-position:top;border-radius:26px;box-shadow:0 22px 50px rgba(29,39,51,.18)}
body .sodc-hero-photo{position:relative}
body .sodc-crumbs p{margin:0;font-size:13px;color:var(--sodc-muted)}
body .sodc-crumbs a{color:var(--sodc-teal);text-decoration:none}
body .sodc-formcard{background:#fff;border:1px solid var(--sodc-line);border-radius:22px;padding:26px;box-shadow:0 14px 34px rgba(29,39,51,.08)}
body .sodc-formcard .elementor-heading-title{font-family:Rubik,sans-serif;font-size:22px;font-weight:700;color:var(--sodc-ink)}
body .sodc-prose p{color:var(--sodc-muted);font-size:17px;line-height:1.7;margin:0 0 14px}
body .sodc-prose a{color:var(--sodc-violet);font-weight:600}
body .sodc-sign{background:#fff;border:1px solid var(--sodc-line);border-radius:16px;padding:18px 20px}
body .sodc-sign .elementor-icon-box-title{font-family:Rubik,sans-serif;font-size:17px;font-weight:600;color:var(--sodc-ink);margin:0}
body .sodc-sign .elementor-icon{font-size:18px}
body .sodc-opt{background:#fff;border:1px solid var(--sodc-line);border-radius:20px;padding:26px 24px;transition:transform .25s ease,box-shadow .25s ease,border-color .25s ease;height:100%}
body .sodc-opt:hover{transform:translateY(-4px);border-color:var(--sodc-teal);box-shadow:0 18px 38px rgba(45,156,169,.16)}
body .sodc-opt .elementor-icon-box-title,body .sodc-opt .elementor-icon-box-title a{font-family:Rubik,sans-serif;font-size:19px;font-weight:600;color:var(--sodc-ink)}
body .sodc-opt .elementor-icon-box-description{color:var(--sodc-muted);font-size:15px;line-height:1.6}
body .sodc-opt .elementor-icon-box-description::after{content:"Learn more \\2192";display:block;margin-top:10px;color:var(--sodc-teal);font-weight:600;font-size:14px}
body .sodc-compare{overflow-x:auto;border:1px solid var(--sodc-line);border-radius:18px;background:#fff;max-width:1100px;margin:0 auto;width:100%}
body .sodc-compare table{width:100%;min-width:640px;border-collapse:collapse;font-size:15px;margin:0}
body .sodc-compare th,body .sodc-compare td{padding:14px 18px;border:0;border-bottom:1px solid var(--sodc-line);text-align:left;vertical-align:top;color:var(--sodc-muted)}
body .sodc-compare th{background:linear-gradient(90deg,#2D9CA9,#6656C4);color:#fff;font-family:Rubik,sans-serif;font-weight:600}
body .sodc-compare td:first-child{color:var(--sodc-ink);font-weight:600}
body .sodc-compare tr:last-child td{border-bottom:0}
body .sodc-compare tr:nth-child(even) td{background:#f8fafc}
body .sodc-panel{background:#fff;border:1px solid var(--sodc-line);border-radius:22px;padding:30px}
body .sodc-panel .elementor-heading-title{font-family:Rubik,sans-serif;font-size:24px;font-weight:700;color:var(--sodc-ink)}
body .sodc-panel .elementor-icon-list-text{color:var(--sodc-ink);font-size:16px}
body .sodc-panel p{color:var(--sodc-muted);margin:0}
body .sodc-profile img{width:100%;aspect-ratio:1/1;object-fit:cover;object-position:top;border-radius:24px;box-shadow:0 18px 40px rgba(29,39,51,.14)}
body .sodc-badges .elementor-icon-list-item{background:#fff;border:1px solid var(--sodc-line);border-radius:999px;padding:8px 14px!important;margin:0 8px 8px 0!important}
body .sodc-badges .elementor-icon-list-text{font-size:14px;font-weight:500;color:var(--sodc-ink)}
body .sodc-ba-single img{width:100%;max-width:560px;margin:0 auto;border-radius:22px;box-shadow:0 18px 40px rgba(29,39,51,.14)}
body .sodc-h3c .elementor-heading-title{font-family:Rubik,sans-serif;font-size:22px;font-weight:700;color:var(--sodc-ink);margin-top:10px}
body .sodc-price{background:linear-gradient(135deg,#f1fafb 0%,#f4f2fd 100%);border-radius:24px;padding:34px}
@media (max-width:767px){body .sodc-price,body .sodc-panel{padding:22px}body .sodc-formcard{padding:20px}}
"""
style_html=base_css.replace('\n</style>',extra_css+'\n</style>')
style=W("html",html=style_html,_css_classes="sodc-css")

# ===== 1. HERO =====
hero=C({"flex_direction":"row","flex_wrap":"wrap","flex_align_items":"center","flex_gap":GAP(48,32),
  "padding":{"unit":"px","top":64,"right":20,"bottom":72,"left":20,"isLinked":False},"padding_mobile":{"unit":"px","top":36,"right":16,"bottom":44,"left":16,"isLinked":False},"css_classes":"sodc-sat-hero"},[
  style,
  col(56,[
    TXT('<p><a href="https://smileondc.com/">Home</a> › <a href="https://smileondc.com/dental-services/">Dental Services</a> › Orthodontics</p>',"sodc-crumbs"),
    TXT("<p>Orthodontist in Dubai · Braces &amp; Clear Aligners</p>","sodc-pill"),
    H("Best Orthodontist in Dubai for Braces and Clear Aligners","h1",None,"sodc-h1"),
    TXT("<p>Straighter teeth and a healthier bite, planned by a specialist orthodontist. We treat children, teens and adults with metal, ceramic, lingual and Damon braces, Invisalign and Invisalign First, all in one clinic in Al Satwa, close to Jumeirah.</p>"),
    row([CALL(),BTN("Book a Consultation",U+"/make-appointment/",icon="fas fa-calendar-check")]),
    W("icon-list",view="inline",icon_color="#2D9CA9",text_color="#3a4652",_css_classes="sodc-trust",icon_list=[
      {"_id":"t1","text":"Specialist orthodontist","selected_icon":FA("fas fa-check-circle")},
      {"_id":"t2","text":"Certified Invisalign provider","selected_icon":FA("fas fa-check-circle")},
      {"_id":"t3","text":"Children, teens & adults","selected_icon":FA("fas fa-check-circle")},
      {"_id":"t4","text":"Rated 5.0 on Google","selected_icon":FA("fas fa-star")}])],gap=16),
  col(38,[IMG(3833,U+"/wp-content/uploads/2025/06/Dr.Jeff_-768x1014.jpg","Dr. Jeffrey Manuel, Specialist Orthodontist and Medical Director at Smile On Dental Clinic, Dubai","sodc-hero-photo","full"),
    TXT("<p><strong>Dr. Jeffrey Manuel</strong><br>Specialist Orthodontist &amp; Medical Director. Certified Invisalign provider, in UAE practice since 2008.</p>","sodc-float-card")],gap=0,cls="sodc-collage-wrap")])

# ===== 2. STATS =====
def counter(n,suf,t): return W("counter",starting_number=0,ending_number=n,suffix=suf,title=t,number_color="#ffffff",title_color="#ffffff")
stats=C({"flex_direction":"row","flex_wrap":"wrap","flex_justify_content":"space-around","flex_gap":GAP(24),
  "padding":{"unit":"px","top":36,"right":20,"bottom":36,"left":20,"isLinked":False},"css_classes":"sodc-stats"},[
  counter(6,"","Orthodontic options"),counter(18,"–24","Months, typical treatment"),counter(3,"","Age groups: kids, teens, adults"),counter(5,".0 ★","Google rating")])

# ===== 3. INTRO + FORM =====
intro=section([
  col(56,[KICK("Orthodontics at Smile On",None),H("Orthodontist in Dubai for Braces and Clear Aligners",align=None),
    TXT("<p>Choosing the right orthodontist is an important decision, especially when treatment affects both your appearance and long-term oral health. At Smile On Dental Clinic, we provide orthodontic care that is precise, well-planned and focused on patient comfort.</p>"
        "<p>Our orthodontic team works with adults, teenagers and children who want straighter teeth, better bite alignment and long-lasting results. Every treatment is planned carefully, using modern techniques and clear communication, so you always know what to expect.</p>"
        "<p>We offer a full range of options to suit every case and lifestyle, including traditional <a href=\"https://smileondc.com/metal-ceramic-braces-dubai/\">metal and ceramic braces</a>, fully hidden <a href=\"https://smileondc.com/lingual-braces-dubai/\">lingual braces</a> and comfortable self-ligating <a href=\"https://smileondc.com/damon-braces-dubai/\">Damon braces</a>. For a removable option there's <a href=\"https://smileondc.com/invisalign-dubai/\">Invisalign</a>, and <a href=\"https://smileondc.com/invisalign-first-dubai/\">Invisalign First</a> for younger patients. Every course of treatment finishes with custom <a href=\"https://smileondc.com/teeth-retainers-dubai/\">teeth retainers</a> to protect your results.</p>"
        "<p>Many patients looking for an orthodontist near Jumeirah choose our clinic for its experienced team, modern options and clear, patient-focused approach. We're on 2nd December Street in Al Satwa, a practical choice for families, professionals and expats across central Dubai.</p>","sodc-prose")],gap=14),
  col(38,[H("Request a Call Back","h3",None,""),TXT("<p>Leave your details and our team will call you within 24 hours. Prefer to talk now? Call <a href=\"tel:+971558961826\">+971 55 896 1826</a>.</p>","sodc-sub sodc-small"),
    W("shortcode",shortcode='[gravityform id="2" title="false"]')],gap=12,cls="sodc-formcard")],row=True,gap=40)

# ===== 4. WHAT IS IT + SIGNS =====
def sign(icon,t): return W("icon-box",selected_icon=FA(icon),view="stacked",position="inline-start",primary_color="#EEEBFA",secondary_color="#6656C4",title_text=t,title_size="h3",_css_classes="sodc-sign")
what=section([KICK("The basics"),H("What Is Orthodontic Treatment?"),
  SUB("Orthodontic treatment corrects the position of teeth and jaws. When teeth are crowded, unevenly spaced or the bite doesn't line up, it can affect chewing, speech, oral hygiene and confidence. Braces or clear aligners move teeth gently into healthier positions over time, with a plan tailored to your age, bone structure and dental condition."),
  H("When Is Orthodontic Treatment Recommended?","h3",cls="sodc-h3c"),
  grid("sodc-grid sodc-grid-3",[sign("fas fa-layer-group","Crowded or overlapping teeth"),sign("fas fa-arrows-alt-h","Gaps between teeth"),
     sign("fas fa-tooth","Overbite, underbite or crossbite"),sign("fas fa-head-side-cough","Jaw discomfort related to bite issues"),
     sign("fas fa-pump-soap","Difficulty cleaning teeth due to misalignment"),sign("fas fa-smile","Concerns about how your smile looks")]),
  SUB("Orthodontic care isn't just for teenagers. Many adults in Dubai now choose treatment for both functional and aesthetic reasons."),
  CALL("Not sure if you need braces? Call us",align="center")],cls="sodc-tint")

# ===== 5. OPTIONS =====
def opt(icon,t,dsc,url,teal): 
    return W("icon-box",selected_icon=FA(icon),view="stacked",primary_color="#E8F6F7" if teal else "#EEEBFA",secondary_color="#2D9CA9" if teal else "#6656C4",
      text_align="left",title_text=t,description_text=dsc,title_size="h3",link=L(U+url),_css_classes="sodc-opt")
options=section([KICK("Treatment options"),H("Orthodontic Solutions We Offer"),
  SUB("A full range of options, so your treatment can match your lifestyle, budget and clinical needs."),
  TXT("<p>Swipe to see all options →</p>","sodc-swipe-hint"),
  grid("sodc-grid sodc-grid-3 sodc-swipe",[
    opt("fas fa-teeth","Metal & Ceramic Braces","Metal braces are durable and effective for every level of correction. Ceramic braces work the same way but blend with your tooth colour, so they're less noticeable.","/metal-ceramic-braces-dubai/",True),
    opt("fas fa-eye-slash","Lingual Braces","Placed behind the teeth, so they're hidden from view. Ideal if you want effective treatment without visible braces.","/lingual-braces-dubai/",False),
    opt("fas fa-cog","Damon Braces","A self-ligating system that allows smoother tooth movement. Often fewer adjustments and more comfort during treatment.","/damon-braces-dubai/",True),
    opt("fas fa-smile-beam","Invisalign","Custom-made clear aligners that are removable and comfortable. Eat normally and keep up your oral hygiene easily.","/invisalign-dubai/",False),
    opt("fas fa-child","Invisalign First","Designed for younger patients. Helps guide jaw development while correcting early alignment issues in growing children.","/invisalign-first-dubai/",True),
    opt("fas fa-shield-alt","Teeth Retainers","Custom retainers keep your teeth in their new position, with clear guidance on how to wear and care for them.","/teeth-retainers-dubai/",False)])],)

# ===== 6. COMPARISON =====
table=("<div class=\"sodc-compare\"><table><thead><tr><th>Option</th><th>How visible?</th><th>Removable?</th><th>Good to know</th></tr></thead><tbody>"
 "<tr><td>Metal braces</td><td>Visible</td><td>No</td><td>Durable and effective for every level of correction</td></tr>"
 "<tr><td>Ceramic braces</td><td>Less noticeable, tooth-coloured</td><td>No</td><td>Works like metal braces with a more discreet look</td></tr>"
 "<tr><td>Lingual braces</td><td>Hidden behind the teeth</td><td>No</td><td>For effective treatment without visible braces</td></tr>"
 "<tr><td>Damon braces</td><td>Visible (self-ligating)</td><td>No</td><td>Smoother movement, often fewer adjustments</td></tr>"
 "<tr><td>Invisalign</td><td>Clear, barely noticeable</td><td>Yes</td><td>Eat normally and clean your teeth easily</td></tr>"
 "<tr><td>Invisalign First</td><td>Clear, barely noticeable</td><td>Yes</td><td>For children, guiding jaw development early</td></tr>"
 "</tbody></table></div>")
compare=section([KICK("Compare"),H("Braces or Aligners? Your Options at a Glance"),
  SUB("Your orthodontist will recommend the best option for your teeth and bite. This quick comparison helps you prepare questions for your consultation."),
  W("text-editor",editor=table),
  W("text-editor",editor="<p>Want a deeper comparison? Read our guide: <a href=\"https://smileondc.com/blogs/invisalign-vs-braces-dubai/\">Invisalign vs Braces in Dubai</a>.</p>",align="center",_css_classes="sodc-sub sodc-small")],cls="sodc-tint")

# ===== 7. MEET THE ORTHODONTIST =====
doctor=section([
  col(38,[IMG(617,U+"/wp-content/uploads/2022/09/dr.jeffrey-poster-768x768-1.webp","Dr. Jeffrey Manuel, specialist orthodontist at Smile On Dental Clinic, Dubai","sodc-profile")],gap=0),
  col(56,[KICK("Meet your orthodontist",None),H("Dr. Jeffrey Manuel",align=None),
    TXT("<p><strong>Specialist Orthodontist &amp; Medical Director.</strong> Dr. Jeffrey co-founded Smile On Dental Clinic in 2021 and has practised in the UAE since 2008. He treats children, teens and adults, and plans every case personally, from early treatment for growing children to discreet options for working professionals.</p>"),
    W("icon-list",view="inline",icon_color="#6656C4",_css_classes="sodc-badges",icon_list=[
      {"_id":"b1","text":"Certified Invisalign provider","selected_icon":FA("fas fa-certificate")},
      {"_id":"b2","text":"Damon & self-ligating braces","selected_icon":FA("fas fa-cog")},
      {"_id":"b3","text":"Early treatment for children","selected_icon":FA("fas fa-child")},
      {"_id":"b4","text":"Myobrace","selected_icon":FA("fas fa-tooth")}]),
    row([CALL("Book with Dr. Jeffrey"),BTN("View Full Profile",U+"/doctors/dr-jeffrey-manuel/")])],gap=14)],row=True,gap=48)

# ===== 8. PROCESS =====
def step(icon,t,dsc,teal): return W("icon-box",selected_icon=FA(icon),view="stacked",primary_color="#2D9CA9" if teal else "#6656C4",secondary_color="#ffffff",text_align="left",title_text=t,description_text=dsc,title_size="h3",_css_classes="sodc-card")
process=section([KICK("Your treatment journey"),H("What to Expect During Treatment"),
  SUB("Orthodontic treatment is a structured process designed to deliver safe, predictable results."),
  grid("sodc-grid sodc-grid-4",[
    step("fas fa-search","1. Initial consultation","A detailed assessment, including digital scans, X-rays if needed and a bite analysis.",True),
    step("fas fa-clipboard-list","2. Personalised plan","We explain the recommended option, the estimated duration and how to care for your teeth.",True),
    step("fas fa-sync-alt","3. Active treatment","Braces or aligners are adjusted periodically to guide your teeth gradually into place.",False),
    step("fas fa-shield-alt","4. Retention","Retainers are fitted once alignment goals are reached, to protect your results long term.",False)])],cls="sodc-tint")

# ===== 9. BEFORE / AFTER =====
results=section([
  col(46,[IMG(5781,U+"/wp-content/uploads/2026/04/before_after_merged.png","Orthodontic treatment before and after at Smile On Dental Clinic, Dubai","sodc-ba-single")],gap=0),
  col(48,[KICK("Results",None),H("Straighter Teeth, Healthier Bite",align=None),
    TXT("<p>Orthodontic care offers more than a cosmetic improvement. Here's what a well-planned treatment can do for you:</p>"),
    W("icon-list",icon_color="#2D9CA9",text_color="#2b3440",space_between={"unit":"px","size":10},icon_list=[
      {"_id":"r1","text":"Better bite alignment and jaw function","selected_icon":FA("fas fa-check-circle")},
      {"_id":"r2","text":"Easier cleaning and improved oral hygiene","selected_icon":FA("fas fa-check-circle")},
      {"_id":"r3","text":"Reduced risk of tooth wear and gum problems","selected_icon":FA("fas fa-check-circle")},
      {"_id":"r4","text":"Improved confidence and facial balance","selected_icon":FA("fas fa-check-circle")},
      {"_id":"r5","text":"Long-term dental stability","selected_icon":FA("fas fa-check-circle")}]),
    CALL("Call to Start Your Smile Journey")],gap=14)],row=True,gap=48)

# ===== 10. PRICE + WHY =====
price=section([KICK("Cost & value"),H("Orthodontist Braces Price in Dubai"),
  C({"content_width":"full","flex_direction":"row","flex_wrap":"wrap","flex_gap":GAP(24),"flex_align_items":"stretch"},[
    col(49,[H("What affects the cost","h3",None,""),
      W("icon-list",icon_color="#6656C4",text_color="#2b3440",space_between={"unit":"px","size":10},icon_list=[
        {"_id":"p1","text":"The type of braces or aligners you choose","selected_icon":FA("fas fa-circle")},
        {"_id":"p2","text":"How complex the tooth and bite correction is","selected_icon":FA("fas fa-circle")},
        {"_id":"p3","text":"How long treatment takes","selected_icon":FA("fas fa-circle")},
        {"_id":"p4","text":"The patient's age","selected_icon":FA("fas fa-circle")},
        {"_id":"p5","text":"Follow-up and retention needs","selected_icon":FA("fas fa-circle")}]),
      TXT("<p>At your consultation we give you a transparent treatment plan with clear cost guidance, so you can decide without pressure. We work with a range of insurance providers and offer flexible payment options. For typical Invisalign prices, see our <a href=\"https://smileondc.com/blogs/invisalign-cost-dubai-uae/\">Invisalign cost guide</a>.</p>","sodc-sub sodc-small"),
      CALL("Call for a Cost Estimate")],gap=14,cls="sodc-panel"),
    col(49,[H("Why patients choose Smile On","h3",None,""),
      W("icon-list",icon_color="#2D9CA9",text_color="#2b3440",space_between={"unit":"px","size":10},icon_list=[
        {"_id":"w1","text":"Experienced orthodontic professionals","selected_icon":FA("fas fa-user-md")},
        {"_id":"w2","text":"Modern diagnostic and treatment technology","selected_icon":FA("fas fa-laptop-medical")},
        {"_id":"w3","text":"Strict hygiene and sterilisation standards","selected_icon":FA("fas fa-hand-sparkles")},
        {"_id":"w4","text":"Clear explanations at every stage","selected_icon":FA("fas fa-comments")},
        {"_id":"w5","text":"A calm, patient-focused environment","selected_icon":FA("fas fa-spa")}]),
      TXT("<p>Our approach is centred on long-term oral health, not rushed outcomes.</p>","sodc-sub sodc-small")],gap=14,cls="sodc-panel")])])

# ===== 11. REVIEWS =====
reviews=section([KICK("Patient reviews"),H("What Our Patients Say"),
  SUB("Rated 5.0 on Google by patients from Al Satwa, Jumeirah and across Dubai."),
  W("shortcode",shortcode="[trustindex no-registration=google]",_css_classes="sodc-reviews")],cls="sodc-tint")

# ===== 12. FAQ (answers corrected to match their questions) =====
Q=[("How long does orthodontic treatment usually take?","<p>It depends on how complex the problem is rather than the type of braces, along with factors such as bone density and age. Treatment usually takes 18 to 24 months. Teenagers often see faster results because much of their growth happens at this stage.</p>"),
 ("Is orthodontic treatment painful?","<p>Treatment shouldn't be painful. Most people feel some pressure or soreness for a few days after braces are fitted or adjusted, or when they start a new set of aligners. This usually settles quickly, and soft foods help in the meantime. Your orthodontist will explain what to expect and how to stay comfortable.</p>"),
 ("Can adults get braces or Invisalign?","<p>Yes. Orthodontic care isn't limited to teenagers, and many adults in Dubai choose treatment for both functional and aesthetic reasons. Discreet options such as <a href='https://smileondc.com/invisalign-dubai/'>Invisalign</a>, ceramic braces and <a href='https://smileondc.com/lingual-braces-dubai/'>lingual braces</a> are popular with working professionals.</p>"),
 ("Which type of braces is right for me?","<p>Each option works differently. Traditional braces use brackets and wires, Invisalign uses removable clear trays to move teeth into position, and lingual braces are attached behind the teeth. The right choice depends on how severe the problem is, along with cost, treatment time and how discreet you'd like it to be. Our orthodontist will talk you through the options at your consultation.</p>"),
 ("When should my child see an orthodontist?","<p>An early check helps spot bite and jaw problems while your child is still growing. If treatment is needed, options such as <a href='https://smileondc.com/invisalign-first-dubai/'>Invisalign First</a> and <a href='https://smileondc.com/myobrace-dubai/'>Myobrace</a> can guide jaw development and correct early alignment issues.</p>"),
 ("How much do braces cost in Dubai?","<p>The cost depends on the type of braces or aligners, how complex the correction is, how long treatment takes, your age and your retention needs. You'll get a transparent plan with clear cost guidance at your consultation. Call <a href='tel:+971558961826'>+971 55 896 1826</a> to book.</p>"),
 ("What is the difference between an orthodontist and a general dentist for braces?","<p>An orthodontist is a dentist who has completed additional training focused on tooth alignment and bite correction. For braces and complex orthodontic treatment, seeing an orthodontist means a specialist handles your treatment planning and care.</p>"),
 ("Is Smile On Dental Clinic a good choice for orthodontics near Jumeirah?","<p>Patients from Jumeirah and nearby areas often choose Smile On for its accessible location on 2nd December Street, its range of braces and aligner options and its patient-focused care. Treatment is always based on your individual needs rather than a one-size-fits-all approach.</p>")]
faq=section([KICK("FAQ"),H("Frequently Asked Questions"),
  W("toggle",faq_schema="yes",title_html_tag="h3",selected_icon=FA("fas fa-plus"),selected_active_icon=FA("fas fa-minus"),
    tabs=[{"_id":f"q{n+1}","tab_title":q,"tab_content":a} for n,(q,a) in enumerate(Q)])],cls="sodc-faq")

# ===== 13. BLOG =====
blog_w=copy.deepcopy(wpr)
blog=section([KICK("From our blog"),H("Orthodontic Guides From Our Team"),blog_w,BTN("View All Blogs",U+"/blogs/",align="center")],cls="sodc-tint")

# ===== 14. CTA =====
cta=C({"flex_direction":"column","flex_align_items":"center","flex_gap":GAP(16),
  "padding":{"unit":"px","top":64,"right":20,"bottom":64,"left":20,"isLinked":False},"padding_mobile":{"unit":"px","top":44,"right":16,"bottom":44,"left":16,"isLinked":False},"css_classes":"sodc-cta"},[
  W("heading",title="Book an Orthodontic Consultation in Dubai",align="center",header_size="h2"),
  W("text-editor",editor="<p>Our team will assess your needs, explain suitable options and guide you through the process with clarity and care. Call 04 347 2102 or 055 896 1826, or send a request and we'll get back to you within 24 hours.</p>",align="center"),
  row([CALL("Call 055 896 1826","sodc-btn-white"),CALL("Call 04 347 2102","sodc-btn-outline-white",tel="tel:+97143472102"),
       BTN("WhatsApp Us","https://wa.me/971558961826","sodc-btn-outline-white",icon=("fab fa-whatsapp","fa-brands"),ext=True),
       BTN("Book Online",U+"/make-appointment/","sodc-btn-outline-white")],justify="center")])

page=[hero,stats,intro,what,options,compare,doctor,process,results,price,reviews,faq,blog,cta]
used=set()
def reid(els):
    for e in els:
        while True:
            x=secrets.token_hex(4)
            if x not in used: used.add(x); break
        e['id']=x; reid(e.get('elements',[]))
reid(page)
payload={"title":"Orthodontist Dubai (New Design, Draft)","status":"draft","template_type":"wp-page","page_template":"elementor_header_footer","data":page}
s=json.dumps(payload,ensure_ascii=False,separators=(',',':'))
open(S+'/payload_ortho.json','w').write(s)
print('chars',len(s),'widgets',s.count('"elType":"widget"'),'calls',s.count('tel:+97'))
