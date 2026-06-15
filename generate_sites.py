#!/usr/bin/env python3
"""
Generate a polished HTML website for every company in the Amsterdam dataset.
Each page is tailored to the business category with unique colour schemes,
imagery, taglines, services, and USPs. All actual company data
(name, address, phone) is injected into every page.
"""

import openpyxl, re, os, html

# ── OUTPUT DIR ──────────────────────────────────────────────────────────────
OUT = "/home/user/GB123/sites"
os.makedirs(OUT, exist_ok=True)

# ── LOAD DATA ───────────────────────────────────────────────────────────────
wb = openpyxl.load_workbook(
    "/root/.claude/uploads/29439921-ed30-5fc8-aa62-2417c0aef4fa/fe96e0b4-Amsterdam_Data_Set_1.xlsx"
)
ws = wb["Data"]
rows = list(ws.iter_rows(values_only=True))
companies = [r for r in rows[1:] if r[0] and str(r[0]).strip() not in ("", "Z")]

# ── HELPERS ─────────────────────────────────────────────────────────────────
def slug(name):
    s = name.lower().strip()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-")[:80]

def esc(v):
    return html.escape(str(v)) if v else ""

# ── CATEGORY PROFILES ───────────────────────────────────────────────────────
# Each profile: colors, Google Fonts, hero photo, about photo, tagline,
# services (3×name+desc), usps (4×icon+title+desc)

PROFILES = {

    # ── TRADES / CONSTRUCTION ───────────────────────────────────────────────
    "trades": {
        "match": lambda c: c in {
            "Carpenter","Bricklayer","Masonry contractor","Plumber",
            "Electrician","Electrical installation service","Roofing contractor",
            "Plasterer","Stucco contractor","General contractor","Home builder",
            "Custom home builder","Contractor","Construction company",
            "Paving contractor","Interior construction contractor",
            "Handyman/Handywoman/Handyperson","Installation service",
            "Appliance repair service","Modular home builder","Woodworker",
            "Foreman builders association","Cabinet maker","Foundry",
            "Boat builders","Shipyard","Tool store","Home improvement store",
        },
        "font_url": "https://fonts.googleapis.com/css2?family=Barlow:wght@300;400;600;700&family=Barlow+Condensed:wght@400;600;700&display=swap",
        "font_head": "'Barlow Condensed', sans-serif",
        "font_body": "'Barlow', sans-serif",
        "c1": "#1A1F2E",   # deep navy
        "c2": "#2C3347",   # navy mid
        "c3": "#E8760A",   # construction orange
        "c4": "#F5A940",   # amber
        "c5": "#F5F2EE",   # warm off-white
        "c6": "#FDFCFA",   # ivory
        "hero_photo": "photo-1504307651254-35680f356dfd",
        "about_photo": "photo-1590496793929-36417d3117de",
        "tagline": "Vakmanschap dat generaties meegaat",
        "sub": "Betrouwbaar, vakkundig en op tijd. Wij leveren bouwwerk van de hoogste kwaliteit in Amsterdam en omgeving.",
        "services": [
            ("Nieuwbouw & Renovatie", "Van fundering tot dakrand — wij realiseren solide constructies met oog voor detail en duurzaamheid."),
            ("Reparatie & Onderhoud", "Snel en professioneel herstelwerk. Wij lossen elk probleem vakkundig op, groot of klein."),
            ("Advies & Inspectie", "Gratis inspectie en eerlijk advies. Wij denken mee over de beste oplossing voor uw situatie."),
        ],
        "usps": [
            ("🏗️", "Gecertificeerd", "Volledig gecertificeerd en verzekerd voor al onze werkzaamheden."),
            ("⏱️", "Op Tijd", "Wij houden ons altijd aan de afgesproken planning en deadline."),
            ("💰", "Vaste Prijs", "Transparante offertes zonder verborgen kosten of verrassingen achteraf."),
            ("⭐", "Eigen Team", "Vast, ervaren personeel — geen wisselende onderaannemers."),
        ],
    },

    # ── PAINTER ─────────────────────────────────────────────────────────────
    "painter": {
        "match": lambda c: c in {"Painter","Painting"},
        "font_url": "https://fonts.googleapis.com/css2?family=Nunito:wght@300;400;600;700&family=Nunito+Sans:wght@300;400;600&display=swap",
        "font_head": "'Nunito', sans-serif",
        "font_body": "'Nunito Sans', sans-serif",
        "c1": "#2D2416",
        "c2": "#4A3F2F",
        "c3": "#C9823A",
        "c4": "#E8A96A",
        "c5": "#F7F0E6",
        "c6": "#FDFAF4",
        "hero_photo": "photo-1562259949-e8e7689d7828",
        "about_photo": "photo-1589939705384-5185137a7f0f",
        "tagline": "Kleur die uw ruimte tot leven brengt",
        "sub": "Professioneel schilderwerk voor binnen en buiten. Strakke afwerking, mooie kleuren, blijvend resultaat.",
        "services": [
            ("Binnenschilderwerk", "Muren, plafonds, kozijnen en deuren — strakke afwerking met de beste materialen."),
            ("Buitenschilderwerk", "Bescherming én uitstraling. Wij schilderen gevels, kozijnen en houtwerk duurzaam af."),
            ("Behangen & Afwerking", "Behang, spuitwerk, stucwerk en speciale afwerkingen voor een uniek resultaat."),
        ],
        "usps": [
            ("🎨", "Kleuradvies", "Gratis kleuradvies door onze ervaren specialisten."),
            ("✨", "Strakke Afwerking", "Wij staan voor een perfecte, strakke eindresultaat."),
            ("🛡️", "Garantie", "Op al ons werk geven wij garantie."),
            ("🧹", "Schoon Achter", "Wij werken netjes en laten uw woning schoon achter."),
        ],
    },

    # ── PHOTOGRAPHER ────────────────────────────────────────────────────────
    "photographer": {
        "match": lambda c: c in {
            "Photographer","Photography service","Photography studio",
            "Commercial photographer","Wedding photographer",
            "Aerial photographer","Portrait studio","Photo shop",
        },
        "font_url": "https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,500;1,300;1,400&family=Inter:wght@300;400;500&display=swap",
        "font_head": "'Cormorant Garamond', serif",
        "font_body": "'Inter', sans-serif",
        "c1": "#1A1A1A",
        "c2": "#2E2E2E",
        "c3": "#B8996A",
        "c4": "#D4B896",
        "c5": "#F5F3EF",
        "c6": "#FDFCF9",
        "hero_photo": "photo-1452587925148-ce544e77e70d",
        "about_photo": "photo-1542038374597-5e3c0ac69c7d",
        "tagline": "Momenten die eeuwig duren",
        "sub": "Professionele fotografie met oog voor detail, sfeer en emotie. Elk beeld vertelt uw verhaal.",
        "services": [
            ("Portret & Lifestyle", "Natuurlijke, authentieke portretten die karakter en persoonlijkheid uitstralen."),
            ("Bedrijfsfotografie", "Professionele beelden voor uw website, social media en marketing materiaal."),
            ("Evenement & Reportage", "Dynamische verslaglegging van uw event, bruiloft of bijzonder moment."),
        ],
        "usps": [
            ("📸", "Professioneel", "High-end camera-apparatuur en jarenlange expertise."),
            ("🎨", "Eigen Stijl", "Een herkenbare, authentieke beeldtaal die bij u past."),
            ("⚡", "Snelle Levering", "Bewerkte foto's binnen 7 werkdagen in uw mailbox."),
            ("💬", "Persoonlijk", "Intensief contact en een relaxte sfeer tijdens de shoot."),
        ],
    },

    # ── GARDEN / LANDSCAPE ──────────────────────────────────────────────────
    "garden": {
        "match": lambda c: c in {
            "Garden","Gardener","Landscaper","Landscape designer",
            "Landscape architect","Community garden","Garden center",
            "Garden building supplier","Garden furniture shop",
            "Botanical garden","Plant nursery","Interior plant service",
            "Hydroponics equipment supplier","Christmas tree farm",
        },
        "font_url": "https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,500;1,400&family=DM+Sans:wght@300;400;500&display=swap",
        "font_head": "'Playfair Display', serif",
        "font_body": "'DM Sans', sans-serif",
        "c1": "#1B2E1E",
        "c2": "#2E4A30",
        "c3": "#6B9E5E",
        "c4": "#9DC78D",
        "c5": "#EEF4EB",
        "c6": "#F8FBF6",
        "hero_photo": "photo-1416879595882-3373a0480b5b",
        "about_photo": "photo-1500530855697-b586d89ba3ee",
        "tagline": "Natuur die uw leven verrijkt",
        "sub": "Tuinontwerp, aanleg en onderhoud met passie voor groen. Wij creëren buitenruimtes om van te genieten.",
        "services": [
            ("Tuinontwerp", "Van schets tot beplanting — wij ontwerpen een tuin die perfect bij u past."),
            ("Aanleg & Beplanting", "Professionele aanleg van borders, gazon, bestrating en waterpartijen."),
            ("Onderhoud", "Seizoensgebonden tuinonderhoud zodat uw tuin het hele jaar door mooi blijft."),
        ],
        "usps": [
            ("🌿", "Duurzaam", "Wij werken met inheemse planten en duurzame materialen."),
            ("🎨", "Op Maat", "Elk tuinontwerp is uniek en afgestemd op uw wensen."),
            ("📅", "Heel het Jaar", "Onderhoudscontracten voor groen dat altijd er goed uitziet."),
            ("🌱", "Groen Advies", "Gratis adviesgesprek over de mogelijkheden in uw tuin."),
        ],
    },

    # ── YOGA / FITNESS ──────────────────────────────────────────────────────
    "yoga": {
        "match": lambda c: c in {
            "Yoga studio","Yoga instructor","Gym","Personal trainer",
            "Coaching center","Dog trainer","Pet trainer",
        },
        "font_url": "https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,300;0,400;1,300;1,400&family=DM+Sans:wght@300;400;500&display=swap",
        "font_head": "'Playfair Display', serif",
        "font_body": "'DM Sans', sans-serif",
        "c1": "#1E2D2A",
        "c2": "#2A3D38",
        "c3": "#7A9E8E",
        "c4": "#B8CCBF",
        "c5": "#EEF4F1",
        "c6": "#FDFAF6",
        "hero_photo": "photo-1545205597-3d9d02c29597",
        "about_photo": "photo-1599901860904-17e6ed7083a0",
        "tagline": "Vind je balans, voel je kracht",
        "sub": "Professionele begeleiding voor een gezonder, bewuster en sterker leven — in een warme, persoonlijke omgeving.",
        "services": [
            ("Groepslessen", "Dynamische en herstellende groepssessies voor alle niveaus in een hechte community."),
            ("Privébegeleiding", "Één-op-één sessies volledig afgestemd op jouw doelen, tempo en niveau."),
            ("Workshops & Retreats", "Verdiepende workshops en speciale evenementen voor extra inspiratie."),
        ],
        "usps": [
            ("🌿", "Kleine Groepen", "Maximaal 10 personen per sessie voor persoonlijke aandacht."),
            ("🏅", "Gecertificeerd", "Al onze instructeurs zijn gecertificeerd met jarenlange ervaring."),
            ("❤️", "Welkom voor Iedereen", "Van absolute beginner tot gevorderde — iedereen is welkom."),
            ("🕯️", "Sfeervolle Ruimte", "Een zorgvuldig ontworpen, rustgevende omgeving."),
        ],
    },

    # ── MOVER / LOGISTICS ───────────────────────────────────────────────────
    "logistics": {
        "match": lambda c: c in {
            "Mover","Moving and storage service","Trucking company",
            "Shipping company","Courier service","Delivery service",
            "Freight forwarding service","Logistics service",
            "Import export company","Shipping service",
            "Shipping and mailing service","Mailing service",
            "Transportation service","Taxi service","Wholesaler",
        },
        "font_url": "https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;600;700&display=swap",
        "font_head": "'Montserrat', sans-serif",
        "font_body": "'Montserrat', sans-serif",
        "c1": "#0D1B2A",
        "c2": "#1B3A5C",
        "c3": "#E8A020",
        "c4": "#F5C842",
        "c5": "#F0F4F8",
        "c6": "#FAFCFF",
        "hero_photo": "photo-1601584115197-04ecc0da31d7",
        "about_photo": "photo-1586528116311-ad8dd3c8310d",
        "tagline": "Uw lading, onze verantwoordelijkheid",
        "sub": "Betrouwbaar transport en logistiek in Amsterdam en heel Nederland. Op tijd, veilig en tegen een scherpe prijs.",
        "services": [
            ("Verhuizingen", "Complete verhuisservice van inpakken tot uitpakken — stressvrij verhuizen."),
            ("Transport & Bezorging", "Snelle en veilige levering van goederen naar elke bestemming."),
            ("Opslag", "Flexibele opslagruimte voor uw spullen, kort- of langdurig."),
        ],
        "usps": [
            ("🚛", "Eigen Vloot", "Moderne voertuigen en eigen chauffeurs voor betrouwbaar transport."),
            ("📍", "Real-time Tracking", "Altijd inzicht in de locatie van uw zending."),
            ("🛡️", "Verzekerd", "Al uw goederen zijn volledig verzekerd tijdens transport."),
            ("📞", "24/7 Bereikbaar", "Onze dispatch is dag en nacht beschikbaar voor u."),
        ],
    },

    # ── BICYCLE ─────────────────────────────────────────────────────────────
    "bicycle": {
        "match": lambda c: c in {
            "Bicycle Shop","Bicycle repair shop","Bicycle rental service",
            "Used bicycle shop","Parking lot for bicycles",
        },
        "font_url": "https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&display=swap",
        "font_head": "'Space Grotesk', sans-serif",
        "font_body": "'Space Grotesk', sans-serif",
        "c1": "#1A2E1A",
        "c2": "#2C4A2C",
        "c3": "#4CAF50",
        "c4": "#81C784",
        "c5": "#EDF5ED",
        "c6": "#F5FBF5",
        "hero_photo": "photo-1571188654248-7a89213915f7",
        "about_photo": "photo-1558618047-3c8c76ca4624",
        "tagline": "Amsterdam op zijn best — op de fiets",
        "sub": "De beste fietsen, reparaties en accessoires voor de echte Amsterdammer. Persoonlijk advies en vakkundig werk.",
        "services": [
            ("Verkoop", "Breed assortiment kwaliteitsfietsen voor elke rijder en elk budget."),
            ("Reparatie & Onderhoud", "Snelle en vakkundige reparaties — van lekke band tot complete revisie."),
            ("Verhuur & Accessoires", "Huur een fiets per dag of week en compleet je rit met het juiste accessoire."),
        ],
        "usps": [
            ("🚲", "Fietsexperts", "Jarenlange ervaring met alle merken en modellen."),
            ("⚡", "Snel Geholpen", "Kleine reparaties vaak dezelfde dag nog klaar."),
            ("🏙️", "Amsterdams", "Wij kennen de stad en de fietser."),
            ("♻️", "Duurzaam", "Tweedehands fietsen en onderdelen voor een groenere keuze."),
        ],
    },

    # ── PHOTOGRAPHY VIDEO ────────────────────────────────────────────────────
    "video": {
        "match": lambda c: c in {
            "Video production service","Video editing service","Video",
            "Recording studio","Media company","Advertising agency",
            "Digital printer",
        },
        "font_url": "https://fonts.googleapis.com/css2?family=Syne:wght@400;500;600;700&family=Inter:wght@300;400;500&display=swap",
        "font_head": "'Syne', sans-serif",
        "font_body": "'Inter', sans-serif",
        "c1": "#0A0A0A",
        "c2": "#1A1A1A",
        "c3": "#E63946",
        "c4": "#F08080",
        "c5": "#F5F5F5",
        "c6": "#FAFAFA",
        "hero_photo": "photo-1516035069371-29a1b244cc32",
        "about_photo": "photo-1492619375914-88005aa9e8fb",
        "tagline": "Uw verhaal in beeld",
        "sub": "Creatieve video- en mediaproductie die uw boodschap krachtig, helder en onvergetelijk overbrengt.",
        "services": [
            ("Videoproductie", "Van concept tot eindproduct — wij realiseren video's die indruk maken."),
            ("Editing & Post", "Professionele nabewerking, kleurcorrectie en geluidsmix voor een strak resultaat."),
            ("Content Strategie", "Wij denken mee over de inzet van uw content op alle platforms."),
        ],
        "usps": [
            ("🎬", "Professioneel", "Cinema-grade apparatuur en een creatief team."),
            ("🎯", "On Brand", "Uw merkidentiteit staat centraal in elk project."),
            ("🚀", "Snelle Doorlooptijd", "Efficiënt proces van brief tot oplevering."),
            ("🤝", "Partnerschap", "Wij denken met u mee als creatief partner."),
        ],
    },

    # ── ART / GALLERY ───────────────────────────────────────────────────────
    "art": {
        "match": lambda c: c in {
            "Art studio","Art gallery","Sculpture","Painting","Statuary",
            "Exhibit","Cultural center","Cultural landmark","Historical landmark",
            "Auction house","Make-up artist",
        },
        "font_url": "https://fonts.googleapis.com/css2?family=EB+Garamond:ital,wght@0,400;0,500;1,400&family=Inter:wght@300;400;500&display=swap",
        "font_head": "'EB Garamond', serif",
        "font_body": "'Inter', sans-serif",
        "c1": "#1A1410",
        "c2": "#2E2620",
        "c3": "#8B6914",
        "c4": "#C4A44A",
        "c5": "#F5F0E8",
        "c6": "#FDFAF4",
        "hero_photo": "photo-1513364776144-60967b0f800f",
        "about_photo": "photo-1558618666-fcd25c85cd64",
        "tagline": "Kunst die raakt en inspireert",
        "sub": "Een plek waar creativiteit bloeit en kunst toegankelijk is voor iedereen. Welkom in onze wereld.",
        "services": [
            ("Tentoonstellingen", "Wisselende exposities van gevestigde en opkomende kunstenaars."),
            ("Atelierwerk", "Ruimte en begeleiding voor kunstenaars om te creëren en te groeien."),
            ("Events & Openingen", "Inspirerende kunstgebeurtenissen en vernissages in een unieke sfeer."),
        ],
        "usps": [
            ("🎨", "Curatie", "Zorgvuldig geselecteerde kunst van hoge kwaliteit."),
            ("🌍", "Internationaal", "Kunstenaars uit Amsterdam en de rest van de wereld."),
            ("🏛️", "Erfgoed", "Respect voor traditie met oog voor het nieuwe."),
            ("❤️", "Toegankelijk", "Kunst voor iedereen, niet alleen voor kenners."),
        ],
    },

    # ── EDUCATION / TUTORING ────────────────────────────────────────────────
    "education": {
        "match": lambda c: c in {
            "Tutoring service","Private tutor","Language school",
            "Culinary school","Education center","Educational institution",
            "University","Coaching center","Community center",
        },
        "font_url": "https://fonts.googleapis.com/css2?family=Lora:ital,wght@0,400;0,500;1,400&family=Source+Sans+3:wght@300;400;600&display=swap",
        "font_head": "'Lora', serif",
        "font_body": "'Source Sans 3', sans-serif",
        "c1": "#2B1F3A",
        "c2": "#4A3660",
        "c3": "#9B72CF",
        "c4": "#C4A8E8",
        "c5": "#F2EDF8",
        "c6": "#FAF8FD",
        "hero_photo": "photo-1481627834876-b7833e8f5570",
        "about_photo": "photo-1523050854058-8df90110c9f1",
        "tagline": "Kennis die deuren opent",
        "sub": "Persoonlijke begeleiding en professioneel onderwijs dat u verder brengt. Leren op uw eigen tempo en niveau.",
        "services": [
            ("Bijles & Begeleiding", "Individuele ondersteuning afgestemd op uw leerstijl en doelen."),
            ("Groepscursussen", "Kleinschalige cursussen in een inspirerende leeromgeving."),
            ("Online Lessen", "Flexibel en effectief leren via videobellen, overal ter wereld."),
        ],
        "usps": [
            ("🎓", "Gekwalificeerd", "Ervaren, gecertificeerde docenten met passie voor hun vak."),
            ("👤", "Persoonlijk", "Elk leertraject is maatwerk, afgestemd op u."),
            ("📈", "Resultaatgericht", "Bewezen methodes die aantoonbaar werken."),
            ("📅", "Flexibel", "Lessen op tijden die voor u uitkomen."),
        ],
    },

    # ── ACCOMMODATION ───────────────────────────────────────────────────────
    "accommodation": {
        "match": lambda c: c in {
            "Bed & breakfast","Vacation Rental","Apartment","House",
            "Lodging","Cottage","Apartment complex","Hotel",
        },
        "font_url": "https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;1,300;1,400&family=Inter:wght@300;400;500&display=swap",
        "font_head": "'Cormorant Garamond', serif",
        "font_body": "'Inter', sans-serif",
        "c1": "#2C1F14",
        "c2": "#4A3428",
        "c3": "#C4804A",
        "c4": "#E4A878",
        "c5": "#F7F0E8",
        "c6": "#FDFAF5",
        "hero_photo": "photo-1566073771259-6a8506099945",
        "about_photo": "photo-1615460549969-36fa19521a4f",
        "tagline": "Thuis voelen, waar dan ook",
        "sub": "Een warme, stijlvolle verblijfplaats in het hart van Amsterdam. Comfort, rust en een persoonlijk welkom.",
        "services": [
            ("Verblijf", "Comfortabele, smaakvolle kamers en appartementen in Amsterdam."),
            ("Ontbijt & Welkom", "Verse producten en een hartelijk ontvangst om uw verblijf te beginnen."),
            ("Tips & Beleving", "Onze lokale aanbevelingen helpen u het beste van Amsterdam te ontdekken."),
        ],
        "usps": [
            ("🏠", "Huiselijk", "Geen anoniem hotel — wij bieden een warm, persoonlijk ontvangst."),
            ("📍", "Centrale Ligging", "Op loopafstand van de mooiste plekken van Amsterdam."),
            ("✨", "Schoon & Stijlvol", "Zorgvuldig onderhouden ruimtes met oog voor detail."),
            ("❤️", "Persoonlijk", "Wij helpen u een onvergetelijk verblijf te beleven."),
        ],
    },

    # ── CLEANING / MAINTENANCE ──────────────────────────────────────────────
    "cleaning": {
        "match": lambda c: c in {
            "House cleaning service","Window cleaning service","Cleaning service",
            "Mobile phone repair shop","Motorcycle repair shop",
        },
        "font_url": "https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap",
        "font_head": "'Plus Jakarta Sans', sans-serif",
        "font_body": "'Plus Jakarta Sans', sans-serif",
        "c1": "#0C2340",
        "c2": "#1A3A5C",
        "c3": "#00A8CC",
        "c4": "#4DC8E8",
        "c5": "#EAF6FA",
        "c6": "#F5FCFF",
        "hero_photo": "photo-1581578731548-c64695cc6952",
        "about_photo": "photo-1584820927498-cfe5211fd8bf",
        "tagline": "Fris, schoon en zorgeloos",
        "sub": "Professionele schoonmaak- en onderhoudsdiensten in Amsterdam. Wij zorgen dat uw ruimte altijd schittert.",
        "services": [
            ("Regulier Onderhoud", "Periodieke schoonmaak van uw woning of kantoor op een vaste afspraak."),
            ("Eenmalige Schoonmaak", "Grondige reiniging van uw ruimte — voor een verhuis, event of inhuizing."),
            ("Specialistisch Werk", "Ruiten lappen, tapijtreinigen en andere specialistische taken vakkundig uitgevoerd."),
        ],
        "usps": [
            ("✅", "Grondig", "Wij reinigen tot in de kleinste hoekjes."),
            ("🌿", "Eco-vriendelijk", "Milieuvriendelijke schoonmaakmiddelen die veilig zijn voor mens en dier."),
            ("🔑", "Discreet", "Vertrouwelijk en betrouwbaar — ook als u er niet bij bent."),
            ("📅", "Flexibel", "Op uw tijden, uw tempo, uw wensen."),
        ],
    },

    # ── INTERIOR DESIGN ─────────────────────────────────────────────────────
    "interior": {
        "match": lambda c: c in {
            "Interior Decorator","Interior plant service",
        },
        "font_url": "https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,500;1,300;1,400&family=Inter:wght@300;400;500&display=swap",
        "font_head": "'Cormorant Garamond', serif",
        "font_body": "'Inter', sans-serif",
        "c1": "#1C1916",
        "c2": "#332E28",
        "c3": "#9E8A7A",
        "c4": "#C4AE9E",
        "c5": "#F5F0EB",
        "c6": "#FDFAF7",
        "hero_photo": "photo-1586023492125-27b2c045efd7",
        "about_photo": "photo-1555041469-a586c61ea9bc",
        "tagline": "Ruimtes die u raken",
        "sub": "Interieuradvies en -ontwerp dat uw leefomgeving transformeert. Stijl, functie en sfeer in perfecte harmonie.",
        "services": [
            ("Interieuradvies", "Een professioneel adviesgesprek over kleur, stijl, meubilair en sfeer."),
            ("Totaalontwerp", "Van plattegrond tot afwerking — wij ontwerpen uw ideale interieur."),
            ("Inkoop & Styling", "Wij selecteren en regelen meubels, accessoires en kunst voor u."),
        ],
        "usps": [
            ("✨", "Eigen Stijl", "Uw persoonlijkheid staat centraal in elk ontwerp."),
            ("🏠", "Praktisch & Mooi", "Wij combineren esthetiek met functionaliteit."),
            ("🌿", "Duurzaam", "Oog voor duurzame en tijdloze keuzes."),
            ("📐", "Tot in Detail", "Perfectie in elk detail, groot en klein."),
        ],
    },

    # ── EVENTS / VENUE ──────────────────────────────────────────────────────
    "events": {
        "match": lambda c: c in {
            "Event venue","Festival","Function room facility",
            "Community center","Cultural center","Exhibit",
        },
        "font_url": "https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:wght@300;400;500&display=swap",
        "font_head": "'DM Serif Display', serif",
        "font_body": "'DM Sans', sans-serif",
        "c1": "#160D28",
        "c2": "#2A1A4A",
        "c3": "#9B60C8",
        "c4": "#C498E0",
        "c5": "#F3EEF9",
        "c6": "#FAF7FD",
        "hero_photo": "photo-1527529482837-4698179dc6ce",
        "about_photo": "photo-1561489413-985b06da5bee",
        "tagline": "Evenementen die bijblijven",
        "sub": "Een unieke locatie en professionele organisatie voor evenementen die indruk maken en mensen samenbrengen.",
        "services": [
            ("Zaalverhuur", "Sfeervolle zalen voor elk type bijeenkomst, van klein tot groot."),
            ("Eventorganisatie", "Complete ontzorging van uw bedrijfsevent, feest of bijeenkomst."),
            ("Catering & Service", "Culinaire verzorging en gastheerschap op het hoogste niveau."),
        ],
        "usps": [
            ("🏛️", "Unieke Locatie", "Een bijzondere ruimte die uw event onderscheidt."),
            ("🎯", "Ontzorging", "Wij regelen alles tot in de puntjes."),
            ("👥", "Flexibel", "Geschikt voor 10 tot 500 gasten."),
            ("⭐", "Ervaring", "Honderden succesvolle evenementen op onze naam."),
        ],
    },

    # ── NATURE / PARK ───────────────────────────────────────────────────────
    "nature": {
        "match": lambda c: c in {
            "Park","Area","Nature preserve","Lake","Botanical garden",
            "Hiking area","Garden","Community garden","Swimming lake",
            "Dog park","Playground","Canal","Tourist attraction",
        },
        "font_url": "https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;1,400&family=DM+Sans:wght@300;400;500&display=swap",
        "font_head": "'Playfair Display', serif",
        "font_body": "'DM Sans', sans-serif",
        "c1": "#142014",
        "c2": "#203320",
        "c3": "#4A8C4A",
        "c4": "#7ABF7A",
        "c5": "#EAF3EA",
        "c6": "#F4FBF4",
        "hero_photo": "photo-1500964757637-c85e8a162429",
        "about_photo": "photo-1441974231531-c6227db76b6e",
        "tagline": "Natuur midden in de stad",
        "sub": "Een groene oase in Amsterdam waar mensen tot rust komen, spelen en de natuur beleven.",
        "services": [
            ("Recreatie", "Ruimte voor sport, spel, picknick en ontspanning in het groen."),
            ("Evenementen", "De perfecte buitenlocatie voor festivals, markten en bijeenkomsten."),
            ("Natuur & Educatie", "Ontdek de flora en fauna in een unieke stedelijke omgeving."),
        ],
        "usps": [
            ("🌳", "Groen Paradijs", "Een uniek stukje natuur binnen de stadsgrenzen."),
            ("🐦", "Biodiversiteit", "Rijk ecosysteem met bijzondere plant- en diersoorten."),
            ("♿", "Toegankelijk", "Toegankelijk voor iedereen, het hele jaar door."),
            ("🆓", "Vrij Toegankelijk", "Altijd open en gratis te bezoeken."),
        ],
    },

    # ── DEFAULT ─────────────────────────────────────────────────────────────
    "default": {
        "match": lambda c: True,  # catch-all
        "font_url": "https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&family=Playfair+Display:ital,wght@0,400;1,400&display=swap",
        "font_head": "'Playfair Display', serif",
        "font_body": "'Inter', sans-serif",
        "c1": "#1A2340",
        "c2": "#2C3A5C",
        "c3": "#4A6FA5",
        "c4": "#7A9EC8",
        "c5": "#EEF2F8",
        "c6": "#F8FAFB",
        "hero_photo": "photo-1497366216548-37526070297c",
        "about_photo": "photo-1497366754035-f200968a6e72",
        "tagline": "Professioneel en betrouwbaar",
        "sub": "Vakkundig, persoonlijk en altijd op tijd. Wij staan voor kwaliteit en service in Amsterdam.",
        "services": [
            ("Onze Diensten", "Professionele dienstverlening afgestemd op uw specifieke wensen en behoeften."),
            ("Advies op Maat", "Eerlijk en deskundig advies voor de beste oplossing in uw situatie."),
            ("Nazorg & Support", "Wij staan ook na afronding van het werk voor u klaar."),
        ],
        "usps": [
            ("✅", "Betrouwbaar", "Wij doen wat we beloven, altijd."),
            ("⭐", "Kwaliteit", "Vakmanschap en zorgvuldigheid in elk project."),
            ("💬", "Persoonlijk", "Direct contact, geen call centers of tussenpersonen."),
            ("📍", "Amsterdam", "Lokaal geworteld met kennis van de stad."),
        ],
    },
}

PROFILE_ORDER = [
    "trades","painter","photographer","garden","yoga","logistics",
    "bicycle","video","art","education","accommodation","cleaning",
    "interior","events","nature","default",
]

def get_profile(category):
    for key in PROFILE_ORDER:
        if PROFILES[key]["match"](category or ""):
            return PROFILES[key]
    return PROFILES["default"]

# ── HTML TEMPLATE ────────────────────────────────────────────────────────────
def make_html(name, street, city, phone, category, profile):
    p = profile
    c1,c2,c3,c4,c5,c6 = p["c1"],p["c2"],p["c3"],p["c4"],p["c5"],p["c6"]
    fh = p["font_head"]
    fb = p["font_body"]
    hero = f"https://images.unsplash.com/photo-{p['hero_photo']}?w=1800&q=80" if p['hero_photo'] else ""
    about_img = f"https://images.unsplash.com/photo-{p['about_photo']}?w=800&q=80" if p['about_photo'] else ""

    # services
    s1n,s1d = p["services"][0]
    s2n,s2d = p["services"][1]
    s3n,s3d = p["services"][2]

    # usps
    u1i,u1t,u1d = p["usps"][0]
    u2i,u2t,u2d = p["usps"][1]
    u3i,u3t,u3d = p["usps"][2]
    u4i,u4t,u4d = p["usps"][3]

    phone_display = phone if phone else "Bel voor info"
    phone_href   = f"tel:{re.sub(r'[^+0-9]','',phone)}" if phone else "#"
    address_display = f"{street}<br>{city}" if street else city or "Amsterdam"
    cat_display = category or "Amsterdam"

    return f"""<!DOCTYPE html>
<html lang="nl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{esc(name)} | {esc(cat_display)} Amsterdam</title>
<meta name="description" content="{esc(name)} — {esc(p['tagline'])}. Gevestigd in Amsterdam.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="{p['font_url']}" rel="stylesheet">
<style>
*,*::before,*::after{{box-sizing:border-box;margin:0;padding:0}}
:root{{
  --c1:{c1};--c2:{c2};--c3:{c3};--c4:{c4};--c5:{c5};--c6:{c6};
  --fh:{fh};--fb:{fb};
}}
html{{scroll-behavior:smooth}}
body{{font-family:var(--fb);background:var(--c6);color:var(--c1);overflow-x:hidden}}

/* NAV */
nav{{position:fixed;top:0;left:0;right:0;z-index:100;padding:0 6%;height:72px;display:flex;align-items:center;justify-content:space-between;transition:background .4s,box-shadow .4s}}
nav.s{{background:rgba(253,252,250,.96);backdrop-filter:blur(12px);box-shadow:0 1px 0 rgba(0,0,0,.07)}}
.nl{{font-family:var(--fh);font-size:1.2rem;font-weight:400;color:rgba(255,255,255,.95);text-decoration:none;transition:color .4s;letter-spacing:.02em}}
nav.s .nl{{color:var(--c1)}}
.nlinks{{display:flex;gap:2.4rem;list-style:none}}
.nlinks a{{font-size:.75rem;font-weight:500;letter-spacing:.14em;text-transform:uppercase;text-decoration:none;color:rgba(255,255,255,.75);transition:color .3s}}
nav.s .nlinks a{{color:var(--c2)}}
.nlinks a:hover,.nlinks a:hover{{color:var(--c3)}}
.ncta{{background:var(--c3)!important;color:var(--c1)!important;padding:.5rem 1.4rem!important;border-radius:100px!important;font-weight:600!important}}
.ncta:hover{{background:var(--c4)!important}}
.hbg{{display:none;flex-direction:column;gap:5px;cursor:pointer}}
.hbg span{{display:block;width:24px;height:1.5px;background:white;transition:background .4s}}
nav.s .hbg span{{background:var(--c1)}}

/* HERO */
#hero{{height:100vh;min-height:600px;position:relative;display:flex;align-items:center;justify-content:center;text-align:center;overflow:hidden}}
.hbg-img{{position:absolute;inset:0;background:linear-gradient(160deg,rgba(0,0,0,.65) 0%,rgba(0,0,0,.35) 60%),url('{hero}') center/cover no-repeat}}
.hbg-img::after{{content:'';position:absolute;bottom:0;left:0;right:0;height:28%;background:linear-gradient(to bottom,transparent,var(--c6))}}
.hc{{position:relative;z-index:1;max-width:740px;padding:0 1.5rem}}
.hpill{{display:inline-block;background:rgba(255,255,255,.12);border:1px solid rgba(255,255,255,.22);color:rgba(255,255,255,.8);font-size:.66rem;font-weight:500;letter-spacing:.22em;text-transform:uppercase;padding:.38rem 1.2rem;border-radius:100px;margin-bottom:1.6rem;backdrop-filter:blur(4px)}}
.htitle{{font-family:var(--fh);font-size:clamp(2.8rem,7vw,5.2rem);font-weight:400;color:white;line-height:1.08;margin-bottom:1.4rem;letter-spacing:-.01em}}
.hsub{{font-size:.97rem;font-weight:300;color:rgba(255,255,255,.72);line-height:1.8;max-width:500px;margin:0 auto 2.6rem}}
.hbtns{{display:flex;gap:1rem;justify-content:center;flex-wrap:wrap}}
.btn-p{{font-size:.76rem;font-weight:500;letter-spacing:.12em;text-transform:uppercase;text-decoration:none;background:var(--c3);color:white;padding:.88rem 2.2rem;border-radius:100px;transition:background .3s,transform .2s}}
.btn-p:hover{{background:var(--c4);transform:translateY(-2px)}}
.btn-g{{font-size:.76rem;font-weight:400;letter-spacing:.12em;text-transform:uppercase;text-decoration:none;border:1px solid rgba(255,255,255,.45);color:rgba(255,255,255,.9);padding:.88rem 2.2rem;border-radius:100px;transition:background .3s,border-color .3s}}
.btn-g:hover{{background:rgba(255,255,255,.1);border-color:white}}
.sl{{position:absolute;bottom:2.5rem;left:50%;transform:translateX(-50%);z-index:1;display:flex;flex-direction:column;align-items:center;gap:.6rem;color:rgba(255,255,255,.4);font-size:.6rem;letter-spacing:.2em;text-transform:uppercase}}
.sl::after{{content:'';width:1px;height:44px;background:linear-gradient(to bottom,rgba(255,255,255,.45),transparent);animation:drop 2s ease-in-out infinite}}
@keyframes drop{{0%,100%{{opacity:0;transform:scaleY(0);transform-origin:top}}50%{{opacity:1;transform:scaleY(1);transform-origin:top}}}}

/* SECTIONS */
section{{padding:6rem 6%}}
.lbl{{font-size:.66rem;font-weight:500;letter-spacing:.24em;text-transform:uppercase;color:var(--c3);margin-bottom:.9rem}}
.h2{{font-family:var(--fh);font-size:clamp(2rem,4vw,3rem);font-weight:400;line-height:1.18;color:var(--c1)}}
.h2 em{{font-style:italic;color:var(--c3)}}

/* ABOUT */
#about{{background:var(--c6)}}
.about-in{{max-width:1200px;margin:0 auto;display:grid;grid-template-columns:1fr 1fr;gap:5rem;align-items:center}}
.aimg-wrap{{position:relative}}
.aimg{{width:100%;aspect-ratio:4/5;object-fit:cover;border-radius:6px;display:block}}
.aimg-accent{{position:absolute;bottom:-1.2rem;right:-1.2rem;width:55%;aspect-ratio:1;background:var(--c3);border-radius:6px;z-index:-1;opacity:.25}}
.atext p{{font-size:.95rem;font-weight:300;line-height:1.9;color:var(--c2);margin-top:1.4rem}}
.adiv{{width:40px;height:2px;background:var(--c3);margin:1.8rem 0}}
.atag{{font-family:var(--fh);font-size:1.7rem;font-weight:400;font-style:italic;color:var(--c1);margin-top:1.4rem}}
.atag small{{display:block;font-family:var(--fb);font-size:.68rem;font-style:normal;font-weight:500;letter-spacing:.12em;text-transform:uppercase;color:var(--c3);margin-top:.2rem}}

/* SERVICES */
#services{{background:var(--c5)}}
.srv-in{{max-width:1200px;margin:0 auto}}
.srv-head{{margin-bottom:3.5rem}}
.srv-grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:1.5rem}}
.srv-card{{background:var(--c6);border-radius:6px;padding:2.4rem 2rem;border:1px solid rgba(0,0,0,.05);position:relative;overflow:hidden;transition:transform .3s,box-shadow .3s}}
.srv-card::after{{content:'';position:absolute;bottom:0;left:0;width:100%;height:3px;background:var(--c3);transform:scaleX(0);transform-origin:left;transition:transform .4s ease}}
.srv-card:hover{{transform:translateY(-4px);box-shadow:0 16px 48px rgba(0,0,0,.08)}}
.srv-card:hover::after{{transform:scaleX(1)}}
.srv-num{{position:absolute;top:1.5rem;right:1.5rem;font-family:var(--fh);font-size:4.5rem;font-weight:400;color:rgba(0,0,0,.04);line-height:1;user-select:none}}
.srv-name{{font-family:var(--fh);font-size:1.3rem;font-weight:400;color:var(--c1);margin-bottom:.6rem}}
.srv-desc{{font-size:.85rem;font-weight:300;line-height:1.78;color:var(--c2)}}

/* USP */
#usp{{background:var(--c1)}}
.usp-in{{max-width:1200px;margin:0 auto}}
.usp-in .lbl{{color:rgba(255,255,255,.5)}}
.usp-in .h2{{color:white}}
.usp-in .h2 em{{color:var(--c4)}}
.usp-grid{{display:grid;grid-template-columns:repeat(4,1fr);gap:1.5rem;margin-top:3rem}}
.usp-card{{background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.07);border-radius:6px;padding:1.8rem 1.5rem;transition:background .3s}}
.usp-card:hover{{background:rgba(255,255,255,.08)}}
.usp-icon{{font-size:1.8rem;margin-bottom:.8rem}}
.usp-title{{font-family:var(--fh);font-size:1.1rem;font-weight:400;color:white;margin-bottom:.35rem}}
.usp-desc{{font-size:.82rem;font-weight:300;line-height:1.7;color:rgba(255,255,255,.5)}}

/* CONTACT */
#contact{{background:var(--c6)}}
.con-in{{max-width:1200px;margin:0 auto;display:grid;grid-template-columns:1fr 1.1fr;gap:5rem;align-items:start}}
.con-left p{{font-size:.93rem;font-weight:300;line-height:1.85;color:var(--c2);margin:1.4rem 0 2.4rem}}
.cdet{{display:flex;flex-direction:column;gap:1.2rem}}
.citem{{display:flex;gap:.9rem;align-items:center}}
.cicon{{width:40px;height:40px;background:var(--c3);border-radius:50%;display:flex;align-items:center;justify-content:center;flex-shrink:0;color:white;font-size:.9rem}}
.ctext strong{{display:block;font-size:.66rem;font-weight:600;letter-spacing:.12em;text-transform:uppercase;color:var(--c1);margin-bottom:.15rem}}
.ctext a,.ctext span{{font-size:.9rem;font-weight:300;color:var(--c2);text-decoration:none}}
.ctext a:hover{{color:var(--c3)}}
.cform{{background:white;border-radius:10px;padding:2.6rem;box-shadow:0 12px 48px rgba(0,0,0,.07)}}
.cform h3{{font-family:var(--fh);font-size:1.6rem;font-weight:400;font-style:italic;color:var(--c1);margin-bottom:.25rem}}
.cform > p{{font-size:.8rem;color:var(--c3);margin-bottom:1.8rem}}
.frow{{display:grid;grid-template-columns:1fr 1fr;gap:.9rem}}
.fg{{margin-bottom:.9rem}}
.fg label{{display:block;font-size:.66rem;font-weight:600;letter-spacing:.12em;text-transform:uppercase;color:var(--c2);margin-bottom:.4rem}}
.fg input,.fg select,.fg textarea{{width:100%;background:var(--c5);border:1px solid rgba(0,0,0,.08);border-radius:6px;padding:.72rem .9rem;font-family:var(--fb);font-size:.88rem;font-weight:300;color:var(--c1);outline:none;transition:border-color .3s;appearance:none}}
.fg input:focus,.fg select:focus,.fg textarea:focus{{border-color:var(--c3);background:white}}
.fg textarea{{resize:vertical;min-height:100px}}
.fsub{{width:100%;background:var(--c1);color:white;border:none;padding:.9rem;font-family:var(--fb);font-size:.76rem;font-weight:600;letter-spacing:.14em;text-transform:uppercase;cursor:pointer;border-radius:100px;margin-top:.4rem;transition:background .3s}}
.fsub:hover{{background:var(--c3)}}
.fsuccess{{display:none;text-align:center;padding:2.5rem 1rem}}
.fsuccess .si{{width:48px;height:48px;background:var(--c5);border-radius:50%;display:flex;align-items:center;justify-content:center;margin:0 auto 1rem;font-size:1.4rem}}
.fsuccess h4{{font-family:var(--fh);font-size:1.4rem;font-weight:400;font-style:italic;color:var(--c1);margin-bottom:.4rem}}
.fsuccess p{{font-size:.85rem;color:var(--c2);font-weight:300}}

/* FOOTER */
footer{{background:var(--c1);padding:3rem 6%}}
.ft{{display:flex;justify-content:space-between;flex-wrap:wrap;gap:2rem;padding-bottom:2rem;border-bottom:1px solid rgba(255,255,255,.07);margin-bottom:1.8rem}}
.flogo{{font-family:var(--fh);font-size:1.3rem;font-weight:400;color:var(--c4);margin-bottom:.6rem}}
.fbt p,.fbt a{{font-size:.75rem;color:rgba(255,255,255,.35);text-decoration:none}}
.fbt a:hover{{color:var(--c4)}}
.flinks h5{{font-size:.62rem;font-weight:600;letter-spacing:.18em;text-transform:uppercase;color:rgba(255,255,255,.45);margin-bottom:1rem}}
.flinks ul{{list-style:none;display:flex;flex-direction:column;gap:.6rem}}
.flinks a{{font-size:.82rem;font-weight:300;color:rgba(255,255,255,.35);text-decoration:none;transition:color .3s}}
.flinks a:hover{{color:var(--c4)}}
.fb{{display:flex;justify-content:space-between;flex-wrap:wrap;gap:.4rem}}
.fb p{{font-size:.72rem;color:rgba(255,255,255,.2)}}

/* REVEAL */
.rv{{opacity:0;transform:translateY(20px);transition:opacity .65s ease,transform .65s ease}}
.rv.vis{{opacity:1;transform:none}}
.d1{{transition-delay:.1s}}.d2{{transition-delay:.2s}}.d3{{transition-delay:.3s}}.d4{{transition-delay:.4s}}

/* MOBILE */
@media(max-width:900px){{
  section{{padding:4.5rem 5%}}
  .about-in,.con-in{{grid-template-columns:1fr;gap:3rem}}
  .srv-grid{{grid-template-columns:1fr}}
  .usp-grid{{grid-template-columns:1fr 1fr}}
  .nlinks{{display:none}}
  .hbg{{display:flex}}
  .frow{{grid-template-columns:1fr}}
  .ft{{flex-direction:column}}
  .cform{{padding:1.8rem}}
}}
@media(max-width:540px){{
  .usp-grid{{grid-template-columns:1fr}}
}}

/* MOBILE NAV */
.mnav{{display:none;position:fixed;inset:0;background:var(--c1);z-index:200;flex-direction:column;align-items:center;justify-content:center;gap:1.8rem}}
.mnav.open{{display:flex}}
.mnav a{{font-family:var(--fh);font-size:2rem;font-weight:400;font-style:italic;color:rgba(255,255,255,.85);text-decoration:none;transition:color .3s}}
.mnav a:hover{{color:var(--c4)}}
.mclose{{position:absolute;top:1.5rem;right:5%;background:none;border:none;color:rgba(255,255,255,.5);font-size:2rem;cursor:pointer;line-height:1}}
</style>
</head>
<body>

<div class="mnav" id="mn">
  <button class="mclose" onclick="document.getElementById('mn').classList.remove('open')">&times;</button>
  <a href="#about" onclick="document.getElementById('mn').classList.remove('open')">Over Ons</a>
  <a href="#services" onclick="document.getElementById('mn').classList.remove('open')">Diensten</a>
  <a href="#contact" onclick="document.getElementById('mn').classList.remove('open')">Contact</a>
</div>

<nav id="nb">
  <a href="#" class="nl">{esc(name)}</a>
  <ul class="nlinks">
    <li><a href="#about">Over Ons</a></li>
    <li><a href="#services">Diensten</a></li>
    <li><a href="#usp">Waarom Wij</a></li>
    <li><a href="#contact" class="ncta">Contact</a></li>
  </ul>
  <div class="hbg" onclick="document.getElementById('mn').classList.add('open')">
    <span></span><span></span><span></span>
  </div>
</nav>

<section id="hero">
  <div class="hbg-img"></div>
  <div class="hc">
    <div class="hpill">{esc(cat_display)} · Amsterdam</div>
    <h1 class="htitle">{esc(name)}</h1>
    <p class="hsub">{esc(p['tagline'])}. {esc(p['sub'])}</p>
    <div class="hbtns">
      <a href="#contact" class="btn-p">Neem Contact Op</a>
      <a href="#services" class="btn-g">Onze Diensten</a>
    </div>
  </div>
  <div class="sl">Ontdek</div>
</section>

<section id="about">
  <div class="about-in">
    <div class="aimg-wrap rv">
      <img src="{about_img}" alt="{esc(name)}" class="aimg">
      <div class="aimg-accent"></div>
    </div>
    <div class="atext">
      <div class="lbl rv">Over Ons</div>
      <h2 class="h2 rv d1">{esc(name)}<br><em>in Amsterdam</em></h2>
      <div class="adiv rv d2"></div>
      <p class="rv d2">Welkom bij {esc(name)}. Wij zijn een professionele {esc(cat_display).lower()} gevestigd in Amsterdam, gespecialiseerd in het leveren van hoogwaardige diensten met aandacht voor kwaliteit en klanttevredenheid.</p>
      <p class="rv d3">Met jarenlange ervaring in ons vakgebied staan wij voor vakmanschap, betrouwbaarheid en een persoonlijke aanpak. Wij behandelen elk project met de zorg en aandacht die het verdient — groot of klein.</p>
      <div class="atag rv d4">
        {esc(name)}
        <small>{esc(cat_display)} · Amsterdam</small>
      </div>
    </div>
  </div>
</section>

<section id="services">
  <div class="srv-in">
    <div class="srv-head">
      <div class="lbl rv">Wat Wij Doen</div>
      <h2 class="h2 rv d1">Onze <em>Diensten</em></h2>
    </div>
    <div class="srv-grid">
      <div class="srv-card rv">
        <span class="srv-num">01</span>
        <h3 class="srv-name">{esc(s1n)}</h3>
        <p class="srv-desc">{esc(s1d)}</p>
      </div>
      <div class="srv-card rv d1">
        <span class="srv-num">02</span>
        <h3 class="srv-name">{esc(s2n)}</h3>
        <p class="srv-desc">{esc(s2d)}</p>
      </div>
      <div class="srv-card rv d2">
        <span class="srv-num">03</span>
        <h3 class="srv-name">{esc(s3n)}</h3>
        <p class="srv-desc">{esc(s3d)}</p>
      </div>
    </div>
  </div>
</section>

<section id="usp">
  <div class="usp-in">
    <div class="lbl rv">Waarom Kiezen Voor Ons</div>
    <h2 class="h2 rv d1">Kwaliteit die je<br><em>kunt vertrouwen</em></h2>
    <div class="usp-grid">
      <div class="usp-card rv d1">
        <div class="usp-icon">{u1i}</div>
        <div class="usp-title">{esc(u1t)}</div>
        <div class="usp-desc">{esc(u1d)}</div>
      </div>
      <div class="usp-card rv d2">
        <div class="usp-icon">{u2i}</div>
        <div class="usp-title">{esc(u2t)}</div>
        <div class="usp-desc">{esc(u2d)}</div>
      </div>
      <div class="usp-card rv d3">
        <div class="usp-icon">{u3i}</div>
        <div class="usp-title">{esc(u3t)}</div>
        <div class="usp-desc">{esc(u3d)}</div>
      </div>
      <div class="usp-card rv d4">
        <div class="usp-icon">{u4i}</div>
        <div class="usp-title">{esc(u4t)}</div>
        <div class="usp-desc">{esc(u4d)}</div>
      </div>
    </div>
  </div>
</section>

<section id="contact">
  <div class="con-in">
    <div class="con-left">
      <div class="lbl rv">Contact</div>
      <h2 class="h2 rv d1">Laten we<br><em>kennismaken</em></h2>
      <p class="rv d2">Heeft u een vraag of wilt u een vrijblijvende offerte? Neem gerust contact op — wij reageren binnen 24 uur.</p>
      <div class="cdet">
        <div class="citem rv d2">
          <div class="cicon">📞</div>
          <div class="ctext">
            <strong>Telefoon</strong>
            <a href="{phone_href}">{esc(phone_display)}</a>
          </div>
        </div>
        <div class="citem rv d3">
          <div class="cicon">📍</div>
          <div class="ctext">
            <strong>Adres</strong>
            <span>{address_display}</span>
          </div>
        </div>
        <div class="citem rv d4">
          <div class="cicon">🕐</div>
          <div class="ctext">
            <strong>Bereikbaar</strong>
            <span>Ma – Vr: 08:00 – 18:00</span>
          </div>
        </div>
      </div>
    </div>
    <div class="cform rv d1">
      <h3>Stuur een bericht</h3>
      <p>Wij nemen zo snel mogelijk contact met u op.</p>
      <form onsubmit="this.style.display='none';document.getElementById('fs').style.display='block';return false">
        <div class="frow">
          <div class="fg"><label>Voornaam</label><input type="text" placeholder="Jan" required></div>
          <div class="fg"><label>Achternaam</label><input type="text" placeholder="De Vries" required></div>
        </div>
        <div class="frow">
          <div class="fg"><label>Telefoon</label><input type="tel" placeholder="+31 6 ..."></div>
          <div class="fg"><label>E-mail</label><input type="email" placeholder="u@voorbeeld.nl" required></div>
        </div>
        <div class="fg"><label>Bericht</label><textarea placeholder="Hoe kunnen wij u helpen?"></textarea></div>
        <button type="submit" class="fsub">Verstuur Bericht</button>
      </form>
      <div class="fsuccess" id="fs">
        <div class="si">✓</div>
        <h4>Bedankt voor uw bericht!</h4>
        <p>Wij nemen binnen 24 uur contact met u op.</p>
      </div>
    </div>
  </div>
</section>

<footer>
  <div class="ft">
    <div class="fbt">
      <div class="flogo">{esc(name)}</div>
      <p>{esc(cat_display)} · Amsterdam</p>
      <p style="margin-top:.4rem"><a href="{phone_href}">{esc(phone_display)}</a></p>
    </div>
    <div class="flinks">
      <h5>Navigatie</h5>
      <ul>
        <li><a href="#about">Over Ons</a></li>
        <li><a href="#services">Diensten</a></li>
        <li><a href="#usp">Waarom Wij</a></li>
        <li><a href="#contact">Contact</a></li>
      </ul>
    </div>
    <div class="flinks">
      <h5>Contact</h5>
      <ul>
        <li><a href="{phone_href}">{esc(phone_display)}</a></li>
        <li><a href="#contact">Stuur een bericht</a></li>
      </ul>
    </div>
  </div>
  <div class="fb">
    <p>© 2024 {esc(name)}. Alle rechten voorbehouden.</p>
    <p>{esc(cat_display)} · Amsterdam</p>
  </div>
</footer>

<script>
const nb=document.getElementById('nb');
window.addEventListener('scroll',()=>nb.classList.toggle('s',scrollY>60));
const rvs=document.querySelectorAll('.rv');
const obs=new IntersectionObserver(es=>{{es.forEach(e=>{{if(e.isIntersecting){{e.target.classList.add('vis');obs.unobserve(e.target)}}}});}},{{{{"threshold":0.1}}}});
rvs.forEach(e=>obs.observe(e));
</script>
</body>
</html>"""

# ── GENERATE ALL ────────────────────────────────────────────────────────────
seen_slugs = {}
generated = 0
skipped   = 0

for row in companies:
    name     = str(row[0]).strip()
    street   = str(row[3]).strip() if row[3] else ""
    city     = str(row[4]).strip() if row[4] else "Amsterdam"
    phone    = str(row[8]).strip() if row[8] else ""
    category = str(row[9]).strip() if row[9] else ""

    if not name or name == "Z":
        skipped += 1
        continue

    profile = get_profile(category)
    s = slug(name)

    # deduplicate slugs
    if s in seen_slugs:
        seen_slugs[s] += 1
        s = f"{s}-{seen_slugs[s]}"
    else:
        seen_slugs[s] = 1

    html_content = make_html(name, street, city, phone, category, profile)
    path = os.path.join(OUT, f"{s}.html")
    with open(path, "w", encoding="utf-8") as f:
        f.write(html_content)
    generated += 1

print(f"Generated: {generated} | Skipped: {skipped}")
