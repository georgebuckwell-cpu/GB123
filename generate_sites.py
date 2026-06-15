#!/usr/bin/env python3
import openpyxl, re, os, html as htmlmod
from collections import defaultdict

OUT = "/home/user/GB123/sites"
os.makedirs(OUT, exist_ok=True)

wb = openpyxl.load_workbook(
    "/root/.claude/uploads/29439921-ed30-5fc8-aa62-2417c0aef4fa/fe96e0b4-Amsterdam_Data_Set_1.xlsx"
)
ws = wb["Data"]
rows = list(ws.iter_rows(values_only=True))
companies = [r for r in rows[1:] if r[0] and str(r[0]).strip() not in ("", "Z")]

def slug(name):
    s = name.lower().strip()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-")[:80]

def e(v): return htmlmod.escape(str(v)) if v else ""

# ── PROFILES ─────────────────────────────────────────────────────────────────
PROFILES = {
"trades": {
    "match": lambda c: c in {"Carpenter","Bricklayer","Masonry contractor","Plumber",
        "Electrician","Electrical installation service","Roofing contractor","Plasterer",
        "Stucco contractor","General contractor","Home builder","Custom home builder",
        "Contractor","Construction company","Paving contractor","Interior construction contractor",
        "Handyman/Handywoman/Handyperson","Installation service","Appliance repair service",
        "Modular home builder","Woodworker","Foreman builders association","Cabinet maker",
        "Foundry","Boat builders","Shipyard","Tool store","Home improvement store"},
    "font_import": "https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,500;1,300;1,400&family=Inter:wght@300;400;500;600&display=swap",
    "font_h": "'Cormorant Garamond', serif",
    "font_b": "'Inter', sans-serif",
    "dark":  "#1E2019", "mid": "#2E3028", "accent": "#B8860B", "accent2": "#D4A840",
    "light": "#F5F0E8", "bg": "#FDFAF4",
    "hero_id":    "1504307651254-35680f356dfd",
    "about_id":   "1590496793929-36417d3117de",
    "about2_id":  "1581578731548-c64695cc6952",
    "srv1_id":    "1504307651254-35680f356dfd",
    "srv2_id":    "1558618666-fcd25c85cd64",
    "srv3_id":    "1486325212027-8081e485255e",
    "port_ids":   ["1590496793929-36417d3117de","1504307651254-35680f356dfd","1558618666-fcd25c85cd64","1486325212027-8081e485255e","1600585154526-990dced4db0d"],
    "why_id":     "1581578731548-c64695cc6952",
    "eyebrow":    "Vakmanschap · Amsterdam",
    "tagline":    "Kwaliteit die generaties meegaat",
    "sub":        "Betrouwbaar, vakkundig en altijd op tijd. Wij leveren bouwwerk van de hoogste kwaliteit in Amsterdam en omgeving — groot of klein.",
    "about_p1":   "Met jarenlange ervaring in ons vakgebied brengen wij vakmanschap en een oog voor detail bij elk project. Wij behandelen uw woning of pand met de zorg die het verdient.",
    "about_p2":   "Van kleine reparaties tot grootschalige renovaties — wij werken met eigen, vast personeel en leveren altijd op tijd en binnen budget. Eerlijk advies, transparante prijzen.",
    "stats": [("15+","Jaar Ervaring"),("400+","Projecten"),("100%","Tevredenheid"),("GVA","Gecertificeerd")],
    "services": [
        ("Nieuwbouw & Renovatie","Solide constructies van fundering tot dakrand, uitgevoerd met de beste materialen en jarenlange expertise.",),
        ("Reparatie & Herstel","Snelle en vakkundige reparaties voor elk probleem — wij lossen het op, professioneel en netjes.",),
        ("Advies & Inspectie","Gratis inspectie en eerlijk advies over de staat van uw pand en de beste oplossing voor uw situatie.",),
    ],
    "port_labels": [("Renovatie","Historische Gevel"),("Nieuwbouw","Aanbouw Villa"),("Herstelwerk","Kozijnen & Voegwerk"),("Restauratie","Monumentaal Pand"),("Inspectie","Dakrenovatie")],
    "testimonials": [
        ("De renovatie van onze gevel is prachtig uitgevoerd. Vakkundig, netjes en precies op tijd — wij zijn erg tevreden.","Marjolein van Berg","Amsterdam Centrum"),
        ("Al onze reparaties zijn in één keer goed gedaan. Eerlijk advies en een scherpe prijs. Absoluut een aanrader.","Peter Hoekstra","Oud-Zuid"),
        ("Professioneel, betrouwbaar en altijd bereikbaar. Het resultaat overtrof onze verwachtingen volledig.","Sofie Dekker","De Pijp"),
    ],
    "why_title": "Kwaliteit die je\nkunt vertrouwen",
    "why_items": [
        ("🛡️","Gecertificeerd & Verzekerd","Volledig gecertificeerd en uitgebreid verzekerd. U bent altijd gedekt."),
        ("👷","Vast Eigen Team","Geen wisselende onderaannemers. Altijd ons vaste, betrouwbare team."),
        ("💬","Transparante Prijzen","Duidelijke offertes zonder verrassingen achteraf."),
        ("⏱️","Strakke Planning","Wij houden ons aan de afgesproken tijdlijn, altijd."),
    ],
},
"painter": {
    "match": lambda c: c in {"Painter","Painting"},
    "font_import": "https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,500;1,300;1,400&family=Inter:wght@300;400;500;600&display=swap",
    "font_h": "'Cormorant Garamond', serif",
    "font_b": "'Inter', sans-serif",
    "dark":  "#231A0E", "mid": "#3A2C1C", "accent": "#C9823A", "accent2": "#E4A86A",
    "light": "#F7F0E6", "bg": "#FDFAF4",
    "hero_id":    "1562259949-e8e7689d7828",
    "about_id":   "1589939705384-5185137a7f0f",
    "about2_id":  "1562259949-e8e7689d7828",
    "srv1_id":    "1589939705384-5185137a7f0f",
    "srv2_id":    "1562259949-e8e7689d7828",
    "srv3_id":    "1513694153872-9a621a9f5d85",
    "port_ids":   ["1589939705384-5185137a7f0f","1562259949-e8e7689d7828","1513694153872-9a621a9f5d85","1589939705384-5185137a7f0f","1562259949-e8e7689d7828"],
    "why_id":     "1589939705384-5185137a7f0f",
    "eyebrow":    "Schildersbedrijf · Amsterdam",
    "tagline":    "Kleur die uw ruimte tot leven brengt",
    "sub":        "Professioneel schilder- en afwerkwerk voor binnen en buiten. Strakke afwerking, mooie kleuren, duurzaam resultaat.",
    "about_p1":   "Wij zijn schilders met passie voor ons vak. Elk project — van een klein kamertje tot een complete gevel — verdient onze volledige aandacht en zorg.",
    "about_p2":   "Met de juiste producten, goede voorbereiding en een scherp oog voor detail leveren wij een afwerking waar u jaren plezier van heeft.",
    "stats": [("20+","Jaar Ervaring"),("800+","Woningen"),("100%","Garantie"),("Gratis","Kleuradvies")],
    "services": [
        ("Binnenschilderwerk","Muren, plafonds, kozijnen en deuren — strakke afwerking met de beste materialen voor elk interieur."),
        ("Buitenschilderwerk","Gevels, kozijnen en houtwerk duurzaam en mooi beschermd — wij verzorgen een perfecte buitenafwerking."),
        ("Behangen & Spuitwerk","Behang, spuitwerk en speciale afwerkingen voor een uniek en sfeervol resultaat in uw ruimte."),
    ],
    "port_labels": [("Interieur","Woonkamer Renovatie"),("Exterieur","Gevelrenovatie"),("Spuitwerk","Moderne Afwerking"),("Behang","Klassiek Interieur"),("Kozijnen","Buitenafwerking")],
    "testimonials": [
        ("Ons huis is helemaal opgeknapt. De schilders werkten netjes en het resultaat is geweldig — vol complimenten van iedereen die langskomt.","Anna Vermeer","Jordaan"),
        ("De gevel ziet er als nieuw uit. Goede communicatie, eerlijke prijs en een prachtig eindresultaat. Zeker een aanrader!","Thomas de Vries","Oud-West"),
        ("Van kleuradvies tot eindresultaat: alles klopte. Professioneel team en een strakke afwerking. Zeer tevreden.","Laura Smit","Amsterdam Noord"),
    ],
    "why_title": "Schilders die je\nkunt vertrouwen",
    "why_items": [
        ("🎨","Gratis Kleuradvies","Onze specialisten helpen u de perfecte kleur te kiezen."),
        ("✨","Strakke Afwerking","Wij staan voor een perfect, strak eindresultaat."),
        ("🛡️","Garantie op Werk","Op al ons werk geven wij garantie."),
        ("🧹","Netjes & Schoon","Wij werken netjes en laten uw woning schoon achter."),
    ],
},
"photographer": {
    "match": lambda c: c in {"Photographer","Photography service","Photography studio",
        "Commercial photographer","Wedding photographer","Aerial photographer","Portrait studio","Photo shop"},
    "font_import": "https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,500;1,300;1,400&family=Inter:wght@300;400;500;600&display=swap",
    "font_h": "'Cormorant Garamond', serif",
    "font_b": "'Inter', sans-serif",
    "dark":  "#1A1A1A", "mid": "#2E2E2E", "accent": "#B8996A", "accent2": "#D4B896",
    "light": "#F5F3EF", "bg": "#FDFCF9",
    "hero_id":    "1452587925148-ce544e77e70d",
    "about_id":   "1542038374597-5e3c0ac69c7d",
    "about2_id":  "1516035069371-29a1b244cc32",
    "srv1_id":    "1452587925148-ce544e77e70d",
    "srv2_id":    "1542038374597-5e3c0ac69c7d",
    "srv3_id":    "1492619375914-88005aa9e8fb",
    "port_ids":   ["1452587925148-ce544e77e70d","1542038374597-5e3c0ac69c7d","1492619375914-88005aa9e8fb","1516035069371-29a1b244cc32","1452587925148-ce544e77e70d"],
    "why_id":     "1542038374597-5e3c0ac69c7d",
    "eyebrow":    "Fotografie · Amsterdam",
    "tagline":    "Momenten die eeuwig duren",
    "sub":        "Professionele fotografie met oog voor detail, sfeer en emotie. Elk beeld vertelt uw unieke verhaal op een authentieke manier.",
    "about_p1":   "Fotografie is meer dan een foto maken — het is een moment vastleggen dat nooit terugkomt. Met een scherp oog en passie voor ons vak zorgen wij dat elke opname telt.",
    "about_p2":   "Van portretfotografie en bedrijfsopnames tot bruiloften en evenementen. Wij werken met professionele apparatuur en jarenlange ervaring.",
    "stats": [("10+","Jaar Ervaring"),("2000+","Shoots"),("500+","Tevreden Klanten"),("Award","Winnend")],
    "services": [
        ("Portret & Lifestyle","Natuurlijke, authentieke portretten die uw karakter en persoonlijkheid uitstralen — in studio of op locatie."),
        ("Bedrijfsfotografie","Professionele beelden voor uw website, social media en marketingmateriaal die uw merk versterken."),
        ("Bruiloft & Evenement","Onvergetelijke verslaglegging van uw bijzondere dag of evenement — emotioneel, tijdloos en authentiek."),
    ],
    "port_labels": [("Portret","Lifestyle Sessie"),("Bedrijf","Corporate Shoot"),("Bruiloft","Trouwreportage"),("Product","Productfotografie"),("Evenement","Eventfotografie")],
    "testimonials": [
        ("De trouwfoto's zijn werkelijk prachtig. Elk moment is perfect vastgelegd — wij zijn zo blij met het resultaat.","Emma & Joris de Boer","Bruidspaar"),
        ("Onze bedrijfsfoto's zien er geweldig uit. Professioneel, creatief en snel geleverd. Absoluut een aanrader!","Robert Jansen","Ondernemer"),
        ("Mijn portretfoto's zijn geworden zoals ik me had voorgesteld — natuurlijk, ontspannen en prachtig bewerkt.","Fleur van Dam","Lifestyle"),
    ],
    "why_title": "Fotografie die je\nbijblijft",
    "why_items": [
        ("📸","Professioneel","High-end apparatuur en jarenlange expertise voor het beste resultaat."),
        ("🎨","Eigen Stijl","Een herkenbare, authentieke beeldtaal die bij ú past."),
        ("⚡","Snelle Levering","Bewerkte foto's binnen 7 werkdagen in uw inbox."),
        ("💬","Persoonlijk","Intensief contact en een ontspannen sfeer tijdens elke shoot."),
    ],
},
"garden": {
    "match": lambda c: c in {"Garden","Gardener","Landscaper","Landscape designer",
        "Landscape architect","Community garden","Garden center","Garden building supplier",
        "Garden furniture shop","Botanical garden","Plant nursery","Interior plant service",
        "Hydroponics equipment supplier","Christmas tree farm"},
    "font_import": "https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,300;0,400;0,500;1,300;1,400&family=DM+Sans:wght@300;400;500;600&display=swap",
    "font_h": "'Playfair Display', serif",
    "font_b": "'DM Sans', sans-serif",
    "dark":  "#1B2E1E", "mid": "#2E4A30", "accent": "#6B9E5E", "accent2": "#9DC78D",
    "light": "#EEF4EB", "bg": "#F8FBF6",
    "hero_id":    "1416879595882-3373a0480b5b",
    "about_id":   "1500530855697-b586d89ba3ee",
    "about2_id":  "1416879595882-3373a0480b5b",
    "srv1_id":    "1416879595882-3373a0480b5b",
    "srv2_id":    "1500530855697-b586d89ba3ee",
    "srv3_id":    "1416879595882-3373a0480b5b",
    "port_ids":   ["1416879595882-3373a0480b5b","1500530855697-b586d89ba3ee","1416879595882-3373a0480b5b","1500530855697-b586d89ba3ee","1416879595882-3373a0480b5b"],
    "why_id":     "1500530855697-b586d89ba3ee",
    "eyebrow":    "Tuinspecialist · Amsterdam",
    "tagline":    "Natuur die uw leven verrijkt",
    "sub":        "Tuinontwerp, aanleg en onderhoud met passie voor groen. Wij creëren buitenruimtes om van te genieten, het hele jaar door.",
    "about_p1":   "Een mooie tuin is geen toeval — het is het resultaat van kennis, smaak en vakmanschap. Wij ontwerpen en onderhouden tuinen die echt bij u passen.",
    "about_p2":   "Van kleine stadstuin tot grote landschapstuin: wij luisteren naar uw wensen en vertalen die naar een groen paradijs dat u jarenlang plezier geeft.",
    "stats": [("12+","Jaar Ervaring"),("600+","Tuinen"),("100%","Tevredenheid"),("Groen","Gecertificeerd")],
    "services": [
        ("Tuinontwerp","Van eerste schets tot beplantingsplan — wij ontwerpen een tuin die perfect bij uw huis en leefstijl past."),
        ("Aanleg & Beplanting","Professionele aanleg van borders, gazon, bestrating, waterpartijen en terras naar uw wensen."),
        ("Seizoensonderhoud","Periodiek tuinonderhoud zodat uw tuin het hele jaar door mooi, gezond en verzorgd blijft."),
    ],
    "port_labels": [("Ontwerp","Tuinontwerp op Maat"),("Aanleg","Nieuwe Tuin"),("Onderhoud","Seizoensbeheer"),("Bestrating","Terrasaanleg"),("Beplanting","Kleurrijke Borders")],
    "testimonials": [
        ("Onze tuin is compleet getransformeerd. Prachtig ontwerp, vakkundige aanleg en altijd attent op detail. Wij genieten er elke dag van.","Caroline Mulder","Amsterdam Zuid"),
        ("Het onderhoud is perfect — onze tuin ziet er altijd verzorgd uit, in alle seizoenen. Fijn om mee te werken.","Mark van den Berg","Amstelveen"),
        ("Van ontwerp tot oplevering een geweldige ervaring. Creatief, betrouwbaar en vol kennis van planten. Absolute aanrader!","Inge Bakker","Buitenveldert"),
    ],
    "why_title": "Tuinen die je\nbijblijven",
    "why_items": [
        ("🌿","Duurzaam","Inheemse planten en duurzame materialen voor een groene toekomst."),
        ("🎨","Op Maat","Elk tuinontwerp is uniek en afgestemd op uw wensen."),
        ("📅","Heel het Jaar","Onderhoudscontracten voor groen dat altijd mooi is."),
        ("🌱","Gratis Advies","Gratis adviesgesprek over de mogelijkheden in uw tuin."),
    ],
},
"yoga": {
    "match": lambda c: c in {"Yoga studio","Yoga instructor","Gym","Personal trainer",
        "Coaching center","Dog trainer","Pet trainer"},
    "font_import": "https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,300;0,400;0,500;1,300;1,400&family=DM+Sans:wght@300;400;500;600&display=swap",
    "font_h": "'Playfair Display', serif",
    "font_b": "'DM Sans', sans-serif",
    "dark":  "#1E2D2A", "mid": "#2A3D38", "accent": "#7A9E8E", "accent2": "#B8CCBF",
    "light": "#EEF4F1", "bg": "#FDFAF6",
    "hero_id":    "1545205597-3d9d02c29597",
    "about_id":   "1544367567-0f2fcb009e0b",
    "about2_id":  "1506126613408-eca07ce68773",
    "srv1_id":    "1599901860904-17e6ed7083a0",
    "srv2_id":    "1588286840104-8957b019727f",
    "srv3_id":    "1575052814086-f385e2e2ad1b",
    "port_ids":   ["1545205597-3d9d02c29597","1599901860904-17e6ed7083a0","1588286840104-8957b019727f","1575052814086-f385e2e2ad1b","1544367567-0f2fcb009e0b"],
    "why_id":     "1518611012118-696072aa579a",
    "eyebrow":    "Wellness · Amsterdam",
    "tagline":    "Vind je balans, voel je kracht",
    "sub":        "Professionele begeleiding voor een gezonder, bewuster en sterker leven — in een warme, persoonlijke omgeving midden in Amsterdam.",
    "about_p1":   "Wij geloven in de kracht van beweging, rust en bewustwording. In een sfeervolle omgeving met kleine groepen bieden wij lessen voor elk niveau.",
    "about_p2":   "Van dynamische flows tot herstellende sessies — iedereen is welkom, beginners net zo goed als gevorderden. Kom kennismaken met een gratis proefles.",
    "stats": [("8+","Jaar Studio"),("12","Lessen/Week"),("Max 10","Per Klas"),("500+","Leden")],
    "services": [
        ("Groepslessen","Dynamische en herstellende groepssessies voor alle niveaus in een warme, hechte community."),
        ("Privébegeleiding","Één-op-één sessies volledig afgestemd op jouw doelen, tempo en niveau — intensief en persoonlijk."),
        ("Workshops & Retreats","Verdiepende workshops en bijzondere evenementen voor extra inspiratie en verbinding."),
    ],
    "port_labels": [("Vinyasa","Ochtendflow"),("Yin","Herstellende Sessie"),("Hatha","Klassieke Les"),("Workshop","Verdieping"),("Meditatie","Stille Sessie")],
    "testimonials": [
        ("Dit is mijn wekelijkse retraite. Kleine groepen, warme sfeer en geweldige instructeurs — ik zou het niemand onthouden.","Anna de Boer","Lid seit 2022"),
        ("Als absolute beginner voelde ik me meteen welkom. De lessen zijn perfect voor elk niveau. Echt een aanrader!","Joris Mulder","Beginner"),
        ("De privélessen hebben mij enorm geholpen. Persoonlijke aandacht en een duidelijke progressie — heel fijn!","Fleur van Dam","Maandabonnement"),
    ],
    "why_title": "Meer dan beweging —\neen levenswijze",
    "why_items": [
        ("🌿","Kleine Groepen","Maximaal 10 personen per sessie voor echte persoonlijke aandacht."),
        ("🏅","Gecertificeerd","Al onze instructeurs zijn gecertificeerd met jarenlange ervaring."),
        ("❤️","Voor Iedereen","Van beginner tot gevorderde — iedereen is van harte welkom."),
        ("🕯️","Sfeervolle Ruimte","Een zorgvuldig ontworpen, rustgevende omgeving om tot rust te komen."),
    ],
},
"logistics": {
    "match": lambda c: c in {"Mover","Moving and storage service","Trucking company",
        "Shipping company","Courier service","Delivery service","Freight forwarding service",
        "Logistics service","Import export company","Shipping service",
        "Shipping and mailing service","Mailing service","Transportation service",
        "Taxi service","Wholesaler"},
    "font_import": "https://fonts.googleapis.com/css2?family=Barlow:wght@300;400;500;600;700&family=Barlow+Condensed:wght@500;600;700&display=swap",
    "font_h": "'Barlow Condensed', sans-serif",
    "font_b": "'Barlow', sans-serif",
    "dark":  "#0D1B2A", "mid": "#1B3A5C", "accent": "#E8A020", "accent2": "#F5C842",
    "light": "#F0F4F8", "bg": "#FAFCFF",
    "hero_id":    "1601584115197-04ecc0da31d7",
    "about_id":   "1586528116311-ad8dd3c8310d",
    "about2_id":  "1601584115197-04ecc0da31d7",
    "srv1_id":    "1601584115197-04ecc0da31d7",
    "srv2_id":    "1586528116311-ad8dd3c8310d",
    "srv3_id":    "1601584115197-04ecc0da31d7",
    "port_ids":   ["1601584115197-04ecc0da31d7","1586528116311-ad8dd3c8310d","1601584115197-04ecc0da31d7","1586528116311-ad8dd3c8310d","1601584115197-04ecc0da31d7"],
    "why_id":     "1586528116311-ad8dd3c8310d",
    "eyebrow":    "Transport & Logistiek · Amsterdam",
    "tagline":    "Uw lading, onze verantwoordelijkheid",
    "sub":        "Betrouwbaar transport en logistiek in Amsterdam en heel Nederland. Op tijd, veilig en altijd tegen een scherpe prijs.",
    "about_p1":   "Wij zorgen dat uw goederen veilig en op tijd op de juiste plek aankomen. Met een eigen vloot en ervaren chauffeurs zijn wij altijd inzetbaar.",
    "about_p2":   "Van kleine pakketten tot volledige verhuizingen en grootschalig goederentransport — wij bieden een betrouwbare, flexibele oplossing voor elk logistiek vraagstuk.",
    "stats": [("20+","Jaar Actief"),("50.000+","Transporten"),("100%","Op Tijd"),("24/7","Bereikbaar")],
    "services": [
        ("Verhuizingen","Complete verhuisservice van in- tot uitpakken — stressvrij verhuizen naar uw nieuwe plek."),
        ("Goederentransport","Snelle en veilige levering van uw goederen naar elke bestemming in Nederland en Europa."),
        ("Opslag & Warehousing","Flexibele opslagoplossingen voor uw goederen, voor korte of langere duur."),
    ],
    "port_labels": [("Verhuizing","Particuliere Verhuizing"),("Transport","Zakelijk Transport"),("Opslag","Warehousing"),("Express","Spoedlevering"),("Internationaal","EU Transport")],
    "testimonials": [
        ("Onze verhuizing verliep vlekkeloos. Het team was vriendelijk, efficiënt en alles arriveerde onbeschadigd. Top service!","Familie Bakker","Amsterdam"),
        ("Wij vertrouwen al jaren op hen voor ons zakelijke transport. Altijd op tijd, altijd betrouwbaar. Niet meer zonder!","Robert van Dijk","Ondernemer"),
        ("Snelle reactie en uitstekende service. Onze goederen werden veilig en op tijd afgeleverd — precies wat wij nodig hadden.","Miriam Laan","Importeur"),
    ],
    "why_title": "Transport dat je\nkunt vertrouwen",
    "why_items": [
        ("🚛","Eigen Vloot","Moderne voertuigen en eigen chauffeurs voor betrouwbaar transport."),
        ("📍","Realtime Tracking","Altijd inzicht in de locatie van uw zending via ons systeem."),
        ("🛡️","Volledig Verzekerd","Al uw goederen zijn verzekerd tijdens het transport."),
        ("📞","24/7 Bereikbaar","Onze dispatch is dag en nacht beschikbaar voor u."),
    ],
},
"bicycle": {
    "match": lambda c: c in {"Bicycle Shop","Bicycle repair shop","Bicycle rental service",
        "Used bicycle shop","Parking lot for bicycles"},
    "font_import": "https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&display=swap",
    "font_h": "'Space Grotesk', sans-serif",
    "font_b": "'Space Grotesk', sans-serif",
    "dark":  "#1A2E1A", "mid": "#2C4A2C", "accent": "#4CAF50", "accent2": "#81C784",
    "light": "#EDF5ED", "bg": "#F5FBF5",
    "hero_id":    "1571188654248-7a89213915f7",
    "about_id":   "1558618047-3c8c76ca4624",
    "about2_id":  "1571188654248-7a89213915f7",
    "srv1_id":    "1558618047-3c8c76ca4624",
    "srv2_id":    "1571188654248-7a89213915f7",
    "srv3_id":    "1558618047-3c8c76ca4624",
    "port_ids":   ["1558618047-3c8c76ca4624","1571188654248-7a89213915f7","1558618047-3c8c76ca4624","1571188654248-7a89213915f7","1558618047-3c8c76ca4624"],
    "why_id":     "1571188654248-7a89213915f7",
    "eyebrow":    "Fietsspecialist · Amsterdam",
    "tagline":    "Amsterdam op zijn best — op de fiets",
    "sub":        "De beste fietsen, reparaties en service voor de echte Amsterdammer. Persoonlijk advies en vakkundig werk, altijd met een glimlach.",
    "about_p1":   "Fietsen zit in ons bloed. Al jaren helpen wij Amsterdammers met de beste fiets voor hun route, lifestyle en budget.",
    "about_p2":   "Of u nu een nieuwe fiets zoekt, een lekke band heeft of uw fiets wilt laten reviseren — wij helpen u snel en vakkundig verder.",
    "stats": [("15+","Jaar Ervaring"),("5000+","Reparaties/Jaar"),("200+","Fietsen op Voorraad"),("Alle","Merken")],
    "services": [
        ("Verkoop","Breed assortiment kwaliteitsfietsen voor elke rijder — van stadsfiets tot sportief model."),
        ("Reparatie & Onderhoud","Snelle en vakkundige reparaties — van lekke band en remmen tot complete fietsrevisiebeurten."),
        ("Verhuur & Accessoires","Huur een fiets per dag of week en compleet uw rit met de juiste accessoires en helmen."),
    ],
    "port_ids":   ["1558618047-3c8c76ca4624","1571188654248-7a89213915f7","1558618047-3c8c76ca4624","1571188654248-7a89213915f7","1558618047-3c8c76ca4624"],
    "port_labels": [("Verkoop","Nieuwe Stadsfietsen"),("Reparatie","Snelle Service"),("Revisie","Complete Beurt"),("Verhuur","Dagverhuur"),("Accessoires","Fietsaccessoires")],
    "testimonials": [
        ("Mijn fiets was binnen een uur gerepareerd en rijdt als nieuw. Super vriendelijk personeel en eerlijke prijs!","Sanne de Jong","Amsterdam"),
        ("Geweldige service! Ik heb hier mijn nieuwe fiets gekocht en het advies was perfect. Heel tevreden.","Bas Kuiper","Amsterdam Oost"),
        ("Al jaren kom ik hier voor onderhoud. Altijd snel, altijd goed. De beste fietswinkel van Amsterdam!","Lotte Visser","Jordaan"),
    ],
    "why_title": "Fietsexperts die je\nkunt vertrouwen",
    "why_items": [
        ("🚲","Fietsexperts","Jarenlange ervaring met alle merken en modellen fietsen."),
        ("⚡","Snel Geholpen","Kleine reparaties vaak dezelfde dag nog klaar."),
        ("🏙️","Amsterdams","Wij kennen de stad, de fietser en de routes."),
        ("♻️","Duurzaam","Tweedehands fietsen en onderdelen voor een groenere keuze."),
    ],
},
"video": {
    "match": lambda c: c in {"Video production service","Video editing service","Video",
        "Recording studio","Media company","Advertising agency","Digital printer"},
    "font_import": "https://fonts.googleapis.com/css2?family=Syne:wght@400;500;600;700&family=Inter:wght@300;400;500&display=swap",
    "font_h": "'Syne', sans-serif",
    "font_b": "'Inter', sans-serif",
    "dark":  "#0A0A0A", "mid": "#1A1A1A", "accent": "#E63946", "accent2": "#F08080",
    "light": "#F5F5F5", "bg": "#FAFAFA",
    "hero_id":    "1516035069371-29a1b244cc32",
    "about_id":   "1492619375914-88005aa9e8fb",
    "about2_id":  "1516035069371-29a1b244cc32",
    "srv1_id":    "1516035069371-29a1b244cc32",
    "srv2_id":    "1492619375914-88005aa9e8fb",
    "srv3_id":    "1516035069371-29a1b244cc32",
    "port_ids":   ["1516035069371-29a1b244cc32","1492619375914-88005aa9e8fb","1516035069371-29a1b244cc32","1492619375914-88005aa9e8fb","1516035069371-29a1b244cc32"],
    "why_id":     "1492619375914-88005aa9e8fb",
    "eyebrow":    "Media & Creatie · Amsterdam",
    "tagline":    "Uw verhaal in beeld gebracht",
    "sub":        "Creatieve video- en mediaproductie die uw boodschap krachtig, helder en onvergetelijk overbrengt aan uw doelgroep.",
    "about_p1":   "Wij geloven dat elk verhaal de moeite waard is om te vertellen. Met een creatief team en professionele apparatuur brengen wij uw boodschap tot leven.",
    "about_p2":   "Van conceptontwikkeling tot postproductie — wij begeleiden u door het hele proces en zorgen voor een eindproduct waar u trots op kunt zijn.",
    "stats": [("10+","Jaar Ervaring"),("300+","Producties"),("50+","Vaste Klanten"),("Award","Winnend")],
    "services": [
        ("Videoproductie","Van concept tot eindproduct — wij realiseren video's die indruk maken en uw boodschap krachtig overbrengen."),
        ("Editing & Postproductie","Professionele nabewerking, kleurcorrectie, animaties en geluidsmix voor een strak eindresultaat."),
        ("Content & Strategie","Wij denken mee over de inzet van uw content op alle kanalen voor maximaal bereik en impact."),
    ],
    "port_labels": [("Productie","Bedrijfsfilm"),("Editing","Reclamespot"),("Social","Social Content"),("Event","Eventfilm"),("Interview","Documentaire")],
    "testimonials": [
        ("De bedrijfsfilm heeft onze uitstraling enorm versterkt. Creatief, professioneel en precies zoals wij het voor ogen hadden.","Mark Hendriksen","CEO"),
        ("Binnen twee weken een complete productiereeks opgeleverd — kwaliteit was uitstekend en het team een plezier om mee te werken.","Lisa de Groot","Marketing Manager"),
        ("Onze social media content is naar een ander niveau getild. Betrokken team, scherpe visie en geweldig resultaat.","Daan Vis","Ondernemer"),
    ],
    "why_title": "Creatie die je\nbijblijft",
    "why_items": [
        ("🎬","Professioneel","Cinema-grade apparatuur en een ervaren creatief team."),
        ("🎯","On Brand","Uw merkidentiteit staat centraal in elk project dat wij maken."),
        ("🚀","Snelle Doorlooptijd","Efficiënt proces van brief tot oplevering, zonder concessies aan kwaliteit."),
        ("🤝","Partnerschap","Wij zijn meer dan een leverancier — wij zijn uw creatieve partner."),
    ],
},
"education": {
    "match": lambda c: c in {"Tutoring service","Private tutor","Language school",
        "Culinary school","Education center","Educational institution",
        "University","Community center"},
    "font_import": "https://fonts.googleapis.com/css2?family=Lora:ital,wght@0,400;0,500;1,400&family=Source+Sans+3:wght@300;400;500;600&display=swap",
    "font_h": "'Lora', serif",
    "font_b": "'Source Sans 3', sans-serif",
    "dark":  "#2B1F3A", "mid": "#4A3660", "accent": "#9B72CF", "accent2": "#C4A8E8",
    "light": "#F2EDF8", "bg": "#FAF8FD",
    "hero_id":    "1481627834876-b7833e8f5570",
    "about_id":   "1523050854058-8df90110c9f1",
    "about2_id":  "1481627834876-b7833e8f5570",
    "srv1_id":    "1523050854058-8df90110c9f1",
    "srv2_id":    "1481627834876-b7833e8f5570",
    "srv3_id":    "1523050854058-8df90110c9f1",
    "port_ids":   ["1481627834876-b7833e8f5570","1523050854058-8df90110c9f1","1481627834876-b7833e8f5570","1523050854058-8df90110c9f1","1481627834876-b7833e8f5570"],
    "why_id":     "1523050854058-8df90110c9f1",
    "eyebrow":    "Onderwijs & Begeleiding · Amsterdam",
    "tagline":    "Kennis die deuren opent",
    "sub":        "Persoonlijke begeleiding en professioneel onderwijs dat u écht verder brengt. Leren op uw eigen tempo en niveau, met aandacht voor uw doelen.",
    "about_p1":   "Wij geloven dat goed onderwijs het leven verandert. Met ervaren, gecertificeerde docenten bieden wij onderwijs dat aansluit bij uw behoeften en leerstijl.",
    "about_p2":   "Of u nu bijles zoekt, een nieuwe taal wil leren of een vak wil verdiepen — wij begeleiden u stap voor stap naar uw doel met plezier en passie.",
    "stats": [("10+","Jaar Ervaring"),("1000+","Leerlingen"),("95%","Slagingspercentage"),("Alle","Niveaus")],
    "services": [
        ("Bijles & Begeleiding","Individuele ondersteuning afgestemd op uw leerstijl en doelen — voor elk niveau en vak."),
        ("Groepscursussen","Kleinschalige cursussen in een inspirerende leeromgeving met aandacht voor iedere deelnemer."),
        ("Online Lessen","Flexibel en effectief leren via videobellen — overal, op tijden die voor u uitkomen."),
    ],
    "port_labels": [("Bijles","Wiskunde & Exact"),("Taal","Taalonderwijs"),("Groep","Groepscursus"),("Online","Online Begeleiding"),("Examen","Examenvoorbereiding")],
    "testimonials": [
        ("Dankzij de bijles ben ik geslaagd voor mijn examen! Duidelijke uitleg, geduldig en altijd beschikbaar voor vragen.","Sophie van Dijk","Leerling"),
        ("De cursus was geweldig — kleine groep, goede sfeer en een ervaren docent. Ik heb enorm veel geleerd!","Ahmed El Mansouri","Cursist"),
        ("De online lessen zijn super flexibel en effectief. Ik merk echt vooruitgang en ben erg tevreden met de aanpak.","Nina Boersma","Online Student"),
    ],
    "why_title": "Onderwijs dat je\nbijblijft",
    "why_items": [
        ("🎓","Gekwalificeerd","Ervaren, gecertificeerde docenten met passie voor hun vak."),
        ("👤","Persoonlijk","Elk leertraject is maatwerk, volledig afgestemd op u."),
        ("📈","Resultaatgericht","Bewezen methodes die aantoonbaar werken en resultaat geven."),
        ("📅","Flexibel","Lessen op tijden die voor u uitkomen, ook online mogelijk."),
    ],
},
"accommodation": {
    "match": lambda c: c in {"Bed & breakfast","Vacation Rental","Apartment","House",
        "Lodging","Cottage","Apartment complex","Hotel"},
    "font_import": "https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,500;1,300;1,400&family=Inter:wght@300;400;500&display=swap",
    "font_h": "'Cormorant Garamond', serif",
    "font_b": "'Inter', sans-serif",
    "dark":  "#2C1F14", "mid": "#4A3428", "accent": "#C4804A", "accent2": "#E4A878",
    "light": "#F7F0E8", "bg": "#FDFAF5",
    "hero_id":    "1566073771259-6a8506099945",
    "about_id":   "1615460549969-36fa19521a4f",
    "about2_id":  "1566073771259-6a8506099945",
    "srv1_id":    "1615460549969-36fa19521a4f",
    "srv2_id":    "1566073771259-6a8506099945",
    "srv3_id":    "1615460549969-36fa19521a4f",
    "port_ids":   ["1566073771259-6a8506099945","1615460549969-36fa19521a4f","1566073771259-6a8506099945","1615460549969-36fa19521a4f","1566073771259-6a8506099945"],
    "why_id":     "1615460549969-36fa19521a4f",
    "eyebrow":    "Verblijf · Amsterdam",
    "tagline":    "Thuis voelen, waar dan ook",
    "sub":        "Een warme, stijlvolle verblijfplaats in het hart van Amsterdam. Comfort, rust en een persoonlijk welkom wachten op u.",
    "about_p1":   "Wij bieden meer dan een plek om te slapen — wij bieden een thuis. Zorgvuldig ingericht, warm en persoonlijk, in een van de mooiste steden ter wereld.",
    "about_p2":   "Geniet van een authentiek Amsterdams verblijf met alle comfort die u nodig heeft. Wij helpen u ook graag met tips voor de beste plekken in de stad.",
    "stats": [("500+","Tevreden Gasten/Jaar"),("5","Sterren Beoordeling"),("Centraal","Gelegen"),("Persoonlijk","Ontvangst")],
    "services": [
        ("Verblijf & Kamers","Comfortabele, smaakvolle kamers en appartementen met alle moderne faciliteiten in Amsterdam."),
        ("Ontbijt & Welkom","Verse producten en een hartelijk ontvangst om uw verblijf op de beste manier te beginnen."),
        ("Amsterdam Ontdekken","Onze lokale tips en aanbevelingen helpen u het allerbeste van Amsterdam te beleven."),
    ],
    "port_labels": [("Kamer","Superieure Kamer"),("Suite","Deluxe Suite"),("Ontbijt","Vers Ontbijt"),("Lounge","Gemeenschappelijke Ruimte"),("Stad","Amsterdam Uitzicht")],
    "testimonials": [
        ("Een fantastisch verblijf! De kamer was prachtig ingericht en het ontvangst was super warm en persoonlijk. Wij komen zeker terug.","Familie Jansen","Nederland"),
        ("Perfecte locatie en geweldige service. Het ontbijt was heerlijk en de tips voor Amsterdam waren super waardevol!","Sophie & Thomas","Duitsland"),
        ("Voel je echt thuis hier. Schoon, stijlvol en de gastvrijheid is ongeëvenaard. Hoogste aanbeveling!","Michael Brown","Engeland"),
    ],
    "why_title": "Gastvrij en\nonvergetelijk",
    "why_items": [
        ("🏠","Huiselijk","Geen anoniem hotel — een warm, persoonlijk ontvangst."),
        ("📍","Centrale Ligging","Op loopafstand van de mooiste plekken van Amsterdam."),
        ("✨","Schoon & Stijlvol","Zorgvuldig onderhouden ruimtes met oog voor elk detail."),
        ("❤️","Persoonlijk","Wij helpen u een onvergetelijk verblijf te beleven."),
    ],
},
"cleaning": {
    "match": lambda c: c in {"House cleaning service","Window cleaning service","Cleaning service",
        "Mobile phone repair shop","Motorcycle repair shop"},
    "font_import": "https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap",
    "font_h": "'Plus Jakarta Sans', sans-serif",
    "font_b": "'Plus Jakarta Sans', sans-serif",
    "dark":  "#0C2340", "mid": "#1A3A5C", "accent": "#00A8CC", "accent2": "#4DC8E8",
    "light": "#EAF6FA", "bg": "#F5FCFF",
    "hero_id":    "1581578731548-c64695cc6952",
    "about_id":   "1584820927498-cfe5211fd8bf",
    "about2_id":  "1581578731548-c64695cc6952",
    "srv1_id":    "1584820927498-cfe5211fd8bf",
    "srv2_id":    "1581578731548-c64695cc6952",
    "srv3_id":    "1584820927498-cfe5211fd8bf",
    "port_ids":   ["1581578731548-c64695cc6952","1584820927498-cfe5211fd8bf","1581578731548-c64695cc6952","1584820927498-cfe5211fd8bf","1581578731548-c64695cc6952"],
    "why_id":     "1581578731548-c64695cc6952",
    "eyebrow":    "Schoonmaak · Amsterdam",
    "tagline":    "Fris, schoon en zorgeloos",
    "sub":        "Professionele schoonmaak- en onderhoudsdiensten in Amsterdam. Wij zorgen dat uw ruimte altijd schittert — netjes, betrouwbaar en discreet.",
    "about_p1":   "Een schone omgeving is meer dan een luxe — het is een basisbehoefte. Wij leveren professionele schoonmaakdiensten die u ontzorgen en uw ruimte laten stralen.",
    "about_p2":   "Met eco-vriendelijke producten en een betrouwbaar, discreet team zorgen wij voor uw woning of kantoor — ook als u er niet bij bent.",
    "stats": [("10+","Jaar Ervaring"),("300+","Vaste Klanten"),("Eco","Vriendelijk"),("100%","Tevreden")],
    "services": [
        ("Regulier Onderhoud","Periodieke schoonmaak van uw woning of kantoor op een vaste afspraak — altijd netjes en grondig."),
        ("Eenmalige Schoonmaak","Grondige reiniging van uw ruimte voor een verhuis, inhuizing, event of gewoon een grote beurt."),
        ("Specialistisch Werk","Ruiten lappen, tapijtreinigen en andere specialistische reinigingstaken vakkundig uitgevoerd."),
    ],
    "port_labels": [("Woning","Woningschoonmaak"),("Kantoor","Kantoorschoonmaak"),("Ramen","Raamreiniging"),("Tapijt","Tapijtreinigen"),("Verhuis","Verhuisschoonmaak")],
    "testimonials": [
        ("Onze woning schittert na elke beurt. Betrouwbaar, discreet en altijd grondig. Wij zijn er heel erg blij mee!","Carla Jansen","Amsterdam"),
        ("Het kantoor ziet er altijd perfect uit. Goede communicatie, vaste prijzen en altijd op tijd. Aanrader!","Peter de Vos","Ondernemer"),
        ("Eindschoonmaak voor onze verhuur was geweldig. Alles glom en de huurder was enorm tevreden. Zeker herhalen!","Anne van Dijk","Verhuurder"),
    ],
    "why_title": "Schoonmaak die je\nkunt vertrouwen",
    "why_items": [
        ("✅","Grondig","Wij reinigen tot in de kleinste hoekjes, altijd."),
        ("🌿","Eco-vriendelijk","Milieuvriendelijke middelen, veilig voor mens en dier."),
        ("🔑","Discreet","Vertrouwelijk en betrouwbaar — ook als u er niet bij bent."),
        ("📅","Flexibel","Op uw tijden, uw tempo en uw wensen."),
    ],
},
"interior": {
    "match": lambda c: c in {"Interior Decorator","Interior plant service",
        "Art studio","Art gallery","Sculpture","Statuary"},
    "font_import": "https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,500;1,300;1,400&family=Inter:wght@300;400;500&display=swap",
    "font_h": "'Cormorant Garamond', serif",
    "font_b": "'Inter', sans-serif",
    "dark":  "#1C1916", "mid": "#332E28", "accent": "#9E8A7A", "accent2": "#C4AE9E",
    "light": "#F5F0EB", "bg": "#FDFAF7",
    "hero_id":    "1586023492125-27b2c045efd7",
    "about_id":   "1555041469-a586c61ea9bc",
    "about2_id":  "1586023492125-27b2c045efd7",
    "srv1_id":    "1555041469-a586c61ea9bc",
    "srv2_id":    "1586023492125-27b2c045efd7",
    "srv3_id":    "1555041469-a586c61ea9bc",
    "port_ids":   ["1586023492125-27b2c045efd7","1555041469-a586c61ea9bc","1586023492125-27b2c045efd7","1555041469-a586c61ea9bc","1586023492125-27b2c045efd7"],
    "why_id":     "1555041469-a586c61ea9bc",
    "eyebrow":    "Interieur & Stijl · Amsterdam",
    "tagline":    "Ruimtes die u raken",
    "sub":        "Interieuradvies en -ontwerp dat uw leefomgeving transformeert. Stijl, functie en sfeer in perfecte harmonie — afgestemd op u.",
    "about_p1":   "Een mooi interieur is geen toeval. Het is het resultaat van smaak, kennis en oog voor detail. Wij helpen u een ruimte te creëren die echt bij u past.",
    "about_p2":   "Van kleuradvies en meubilairkeuze tot een compleet interieurontwerp — wij begeleiden u door het hele proces met plezier en professionaliteit.",
    "stats": [("12+","Jaar Ervaring"),("400+","Projecten"),("100%","Op Maat"),("Eigen","Stijl")],
    "services": [
        ("Interieuradvies","Een professioneel adviesgesprek over kleur, stijl, meubilair en sfeer — praktisch en inspirerend."),
        ("Totaalontwerp","Van plattegrond tot afwerking — wij ontwerpen uw ideale interieur volledig op maat."),
        ("Inkoop & Styling","Wij selecteren en regelen meubels, accessoires en kunst voor een perfect eindresultaat."),
    ],
    "port_labels": [("Woonkamer","Modern Interieur"),("Keuken","Keukenontwerp"),("Slaapkamer","Slaapkamerdesign"),("Kantoor","Thuiskantoor"),("Compleet","Totaalrenovatie")],
    "testimonials": [
        ("Ons huis is getransformeerd! Het advies was heel persoonlijk en het resultaat is precies zoals wij het voor ogen hadden.","Rianne Smit","Amsterdam"),
        ("Van kleuren tot meubels — alles klopte. Het totaalontwerp heeft onze woning veranderd in een thuis. Fantastisch werk!","Lars & Emma Bakker","Buitenveldert"),
        ("Professioneel, creatief en altijd met oog voor ons budget. Het eindresultaat is geweldig en we zijn er super blij mee.","Nathalie de Boer","Amsterdam Zuid"),
    ],
    "why_title": "Design dat je\nbijblijft",
    "why_items": [
        ("✨","Eigen Stijl","Uw persoonlijkheid staat centraal in elk ontwerp dat wij maken."),
        ("🏠","Praktisch & Mooi","Wij combineren esthetiek en functionaliteit in elk project."),
        ("🌿","Duurzaam","Oog voor duurzame en tijdloze keuzes die jaren meegaan."),
        ("📐","Tot in Detail","Perfectie in elk detail, groot en klein — altijd."),
    ],
},
"events": {
    "match": lambda c: c in {"Event venue","Festival","Function room facility",
        "Cultural center","Exhibit","Recording studio"},
    "font_import": "https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:wght@300;400;500;600&display=swap",
    "font_h": "'DM Serif Display', serif",
    "font_b": "'DM Sans', sans-serif",
    "dark":  "#160D28", "mid": "#2A1A4A", "accent": "#9B60C8", "accent2": "#C498E0",
    "light": "#F3EEF9", "bg": "#FAF7FD",
    "hero_id":    "1527529482837-4698179dc6ce",
    "about_id":   "1561489413-985b06da5bee",
    "about2_id":  "1527529482837-4698179dc6ce",
    "srv1_id":    "1561489413-985b06da5bee",
    "srv2_id":    "1527529482837-4698179dc6ce",
    "srv3_id":    "1561489413-985b06da5bee",
    "port_ids":   ["1527529482837-4698179dc6ce","1561489413-985b06da5bee","1527529482837-4698179dc6ce","1561489413-985b06da5bee","1527529482837-4698179dc6ce"],
    "why_id":     "1561489413-985b06da5bee",
    "eyebrow":    "Events & Locaties · Amsterdam",
    "tagline":    "Evenementen die bijblijven",
    "sub":        "Een unieke locatie en professionele organisatie voor evenementen die indruk maken, mensen samenbrengen en herinneringen creëren.",
    "about_p1":   "Wij geloven dat elk evenement bijzonder moet zijn. Met een unieke locatie, professionele organisatie en oog voor detail maken wij van elk event een succes.",
    "about_p2":   "Van kleine bijeenkomsten tot grote feesten en festivals — wij ontzorgen u volledig en zorgen dat uw gasten een onvergetelijke avond beleven.",
    "stats": [("500+","Evenementen"),("15+","Jaar Ervaring"),("10-500","Gasten"),("5","Sterren")],
    "services": [
        ("Locatieverhuur","Sfeervolle zalen en unieke ruimtes voor elk type bijeenkomst, klein of groot."),
        ("Eventorganisatie","Complete ontzorging van uw bedrijfsevent, feest of bijeenkomst van A tot Z."),
        ("Catering & Service","Culinaire verzorging en gastheerschap op het allerhoogste niveau."),
    ],
    "port_labels": [("Bedrijfsevent","Zakelijke Bijeenkomst"),("Feest","Privéfeest"),("Festival","Outdoor Event"),("Congres","Congres & Seminarie"),("Bruiloft","Trouwlocatie")],
    "testimonials": [
        ("Ons bedrijfsevent was een groot succes! De locatie was prachtig en de organisatie was tot in de puntjes geregeld.","Sandra Hoekstra","Event Manager"),
        ("Een onvergetelijke avond. De catering was uitstekend en de sfeer was geweldig. Wij boeken zeker opnieuw!","Jan van der Meer","Organisator"),
        ("Alles verliep vlekkeloos. Professioneel team, geweldige locatie en onze gasten waren erg onder de indruk!","Marie Dubois","Bruidspaar"),
    ],
    "why_title": "Events die je\nbijblijven",
    "why_items": [
        ("🏛️","Unieke Locatie","Een bijzondere ruimte die uw event echt onderscheidt."),
        ("🎯","Volledige Ontzorging","Wij regelen alles tot in de puntjes voor u."),
        ("👥","Flexibel","Geschikt voor groepen van 10 tot 500 personen."),
        ("⭐","Ervaring","Honderden succesvolle evenementen op onze naam."),
    ],
},
"nature": {
    "match": lambda c: c in {"Park","Area","Nature preserve","Lake","Botanical garden",
        "Hiking area","Community garden","Swimming lake","Dog park","Playground",
        "Canal","Tourist attraction","Historical landmark","Cultural landmark",
        "Garden","Scenic lookout"},
    "font_import": "https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,300;0,400;1,300;1,400&family=DM+Sans:wght@300;400;500&display=swap",
    "font_h": "'Playfair Display', serif",
    "font_b": "'DM Sans', sans-serif",
    "dark":  "#142014", "mid": "#203320", "accent": "#4A8C4A", "accent2": "#7ABF7A",
    "light": "#EAF3EA", "bg": "#F4FBF4",
    "hero_id":    "1500964757637-c85e8a162429",
    "about_id":   "1441974231531-c6227db76b6e",
    "about2_id":  "1500964757637-c85e8a162429",
    "srv1_id":    "1441974231531-c6227db76b6e",
    "srv2_id":    "1500964757637-c85e8a162429",
    "srv3_id":    "1441974231531-c6227db76b6e",
    "port_ids":   ["1500964757637-c85e8a162429","1441974231531-c6227db76b6e","1500964757637-c85e8a162429","1441974231531-c6227db76b6e","1500964757637-c85e8a162429"],
    "why_id":     "1441974231531-c6227db76b6e",
    "eyebrow":    "Natuur & Recreatie · Amsterdam",
    "tagline":    "Natuur midden in de stad",
    "sub":        "Een groene oase in Amsterdam waar mensen tot rust komen, spelen, sporten en de natuur in al haar pracht beleven.",
    "about_p1":   "Temidden van de bruisende stad biedt deze bijzondere plek een verademing. Groen, rust en natuur binnen handbereik voor iedereen.",
    "about_p2":   "Kom wandelen, fietsen, picknicken of gewoon genieten van de stilte. Een unieke plek in Amsterdam die het hele jaar door mooi is.",
    "stats": [("∞","Altijd Open"),("Gratis","Toegang"),("100+","Vogelsoorten"),("Alle","Seizoenen")],
    "services": [
        ("Recreatie & Sport","Ruimte voor wandelen, fietsen, sporten, spelen en ontspanning in een groene omgeving."),
        ("Natuur & Educatie","Ontdek de unieke flora en fauna in een bijzondere stedelijke natuuromgeving."),
        ("Evenementen & Activiteiten","De perfecte buitenlocatie voor festivals, markten, picknicks en bijeenkomsten."),
    ],
    "port_labels": [("Lente","Bloesemtijd"),("Zomer","Zonnige Dagen"),("Herfst","Herfstkleuren"),("Winter","Winterlandschap"),("Natuur","Bijzondere Flora")],
    "testimonials": [
        ("Mijn favoriete plek in Amsterdam. Elke dag even langs voor een wandeling — heerlijk groen midden in de stad!","Caroline Mulder","Amsterdam"),
        ("Geweldige plek voor onze familie. De kinderen spelen buiten terwijl wij ontspannen. Absoluut een aanrader!","Familie de Wit","Amsterdam Noord"),
        ("Bijzonder mooi in alle seizoenen. Rustgevend, groen en altijd goed onderhouden. Een echte stadsoase.","Thomas Berg","Fietser"),
    ],
    "why_title": "Groen hart\nvan Amsterdam",
    "why_items": [
        ("🌳","Groene Oase","Een uniek stukje natuur binnen de Amsterdamse stadsgrenzen."),
        ("🐦","Biodiversiteit","Rijk ecosysteem met bijzondere plant- en diersoorten."),
        ("♿","Toegankelijk","Toegankelijk voor iedereen, het hele jaar door."),
        ("🆓","Vrij Toegankelijk","Altijd open en gratis te bezoeken voor iedereen."),
    ],
},
"default": {
    "match": lambda c: True,
    "font_import": "https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,500;1,300;1,400&family=Inter:wght@300;400;500;600&display=swap",
    "font_h": "'Cormorant Garamond', serif",
    "font_b": "'Inter', sans-serif",
    "dark":  "#1A2340", "mid": "#2C3A5C", "accent": "#4A6FA5", "accent2": "#7A9EC8",
    "light": "#EEF2F8", "bg": "#F8FAFB",
    "hero_id":    "1497366216548-37526070297c",
    "about_id":   "1497366754035-f200968a6e72",
    "about2_id":  "1497366216548-37526070297c",
    "srv1_id":    "1497366754035-f200968a6e72",
    "srv2_id":    "1497366216548-37526070297c",
    "srv3_id":    "1497366754035-f200968a6e72",
    "port_ids":   ["1497366216548-37526070297c","1497366754035-f200968a6e72","1497366216548-37526070297c","1497366754035-f200968a6e72","1497366216548-37526070297c"],
    "why_id":     "1497366754035-f200968a6e72",
    "eyebrow":    "Professionele Diensten · Amsterdam",
    "tagline":    "Vakmanschap en betrouwbaarheid",
    "sub":        "Professionele dienstverlening in Amsterdam met aandacht voor kwaliteit, eerlijkheid en een persoonlijke aanpak bij elk project.",
    "about_p1":   "Wij staan voor kwaliteit en betrouwbaarheid. Met jarenlange ervaring in ons vakgebied leveren wij diensten die het verschil maken voor onze klanten.",
    "about_p2":   "Persoonlijk contact, eerlijk advies en een vakkundige uitvoering — dat zijn de pijlers waarop ons bedrijf is gebouwd.",
    "stats": [("10+","Jaar Ervaring"),("500+","Projecten"),("100%","Tevredenheid"),("Amsterdam","Gevestigd")],
    "services": [
        ("Professionele Diensten","Vakkundige dienstverlening afgestemd op uw specifieke wensen en behoeften."),
        ("Advies op Maat","Eerlijk en deskundig advies voor de beste oplossing in elke situatie."),
        ("Nazorg & Support","Wij staan ook na afronding van het werk voor u klaar met ondersteuning."),
    ],
    "port_labels": [("Project","Project 1"),("Opdracht","Opdracht 2"),("Werk","Werk 3"),("Resultaat","Resultaat 4"),("Portfolio","Portfolio 5")],
    "testimonials": [
        ("Uitstekende service en vakmanschap. Wij zijn zeer tevreden met het resultaat en bevelen hen van harte aan.","Jan de Vries","Amsterdam"),
        ("Betrouwbaar, professioneel en altijd op tijd. Het werk werd precies uitgevoerd zoals afgesproken. Top!","Maria Smit","Ondernemer"),
        ("Goede communicatie en een sterk eindresultaat. Wij zijn blij dat wij voor hen hebben gekozen.","Peter Bakker","Klant"),
    ],
    "why_title": "Kwaliteit die je\nkunt vertrouwen",
    "why_items": [
        ("✅","Betrouwbaar","Wij doen wat we beloven, altijd en zonder uitzondering."),
        ("⭐","Kwaliteit","Vakmanschap en zorgvuldigheid staan centraal in elk project."),
        ("💬","Persoonlijk","Direct contact, geen call centers of tussenpersonen."),
        ("📍","Amsterdam","Lokaal geworteld met diepgaande kennis van de stad."),
    ],
},
}

PROFILE_ORDER = ["trades","painter","photographer","garden","yoga","logistics",
    "bicycle","video","education","accommodation","cleaning","interior",
    "events","nature","default"]

def get_profile(cat):
    for k in PROFILE_ORDER:
        if PROFILES[k]["match"](cat or ""):
            return PROFILES[k]
    return PROFILES["default"]

def img(photo_id, w=1800, q=80):
    return f"https://images.unsplash.com/photo-{photo_id}?w={w}&q={q}"

# ── HTML TEMPLATE ─────────────────────────────────────────────────────────────
def build_page(name, street, city, phone, category, p):
    phone_href    = f"tel:{re.sub(r'[^+0-9]','',phone)}" if phone else "#"
    phone_display = phone if phone else "Neem contact op"
    address       = f"{street}, {city}" if street else (city or "Amsterdam")
    cat_display   = category or "Amsterdam"

    s1n,s1d = p["services"][0]; s2n,s2d = p["services"][1]; s3n,s3d = p["services"][2]
    t1q,t1a,t1s = p["testimonials"][0]; t2q,t2a,t2s = p["testimonials"][1]; t3q,t3a,t3s = p["testimonials"][2]
    u1i,u1t,u1d = p["why_items"][0]; u2i,u2t,u2d = p["why_items"][1]
    u3i,u3t,u3d = p["why_items"][2]; u4i,u4t,u4d = p["why_items"][3]
    stat_items = p["stats"]
    wt_lines = p["why_title"].split("\n")
    wt_html = f'{e(wt_lines[0])}<br><em>{e(wt_lines[1])}</em>' if len(wt_lines)>1 else e(wt_lines[0])
    port = p["port_ids"]; pl = p["port_labels"]

    stats_html = "".join(f'<div class="stat rv d{i+1}"><div class="sn">{e(s[0])}</div><div class="sl2">{e(s[1])}</div></div>' for i,s in enumerate(stat_items))

    return f"""<!DOCTYPE html>
<html lang="nl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{e(name)} | {e(cat_display)} Amsterdam</title>
<meta name="description" content="{e(name)} — {e(p['tagline'])}. {e(cat_display)} in Amsterdam.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="{p['font_import']}" rel="stylesheet">
<style>
*,*::before,*::after{{box-sizing:border-box;margin:0;padding:0}}
:root{{
  --dark:{p['dark']};--mid:{p['mid']};--acc:{p['accent']};--acc2:{p['accent2']};
  --light:{p['light']};--bg:{p['bg']};
  --fh:{p['font_h']};--fb:{p['font_b']};
}}
html{{scroll-behavior:smooth}}
body{{font-family:var(--fb);background:var(--bg);color:var(--dark);overflow-x:hidden}}

/* ── NAV ── */
nav{{position:fixed;top:0;left:0;right:0;z-index:100;padding:0 5%;height:74px;display:flex;align-items:center;justify-content:space-between;transition:background .45s,box-shadow .45s}}
nav.sc{{background:rgba(253,252,250,.96);backdrop-filter:blur(14px);box-shadow:0 1px 0 rgba(0,0,0,.07)}}
.nlogo{{font-family:var(--fh);font-size:1.25rem;font-weight:400;font-style:italic;color:white;text-decoration:none;transition:color .45s;letter-spacing:.02em}}
nav.sc .nlogo{{color:var(--dark)}}
.nlinks{{display:flex;align-items:center;gap:2.5rem;list-style:none}}
.nlinks a{{font-size:.75rem;font-weight:500;letter-spacing:.14em;text-transform:uppercase;text-decoration:none;color:rgba(255,255,255,.78);transition:color .3s}}
nav.sc .nlinks a{{color:var(--mid)}}
.nlinks a:hover{{color:var(--acc2)}}
.ncta{{background:var(--acc)!important;color:white!important;padding:.52rem 1.5rem;border-radius:100px;font-weight:600!important}}
.ncta:hover{{background:var(--acc2)!important}}
.hbg{{display:none;flex-direction:column;gap:5px;cursor:pointer}}
.hbg span{{display:block;width:24px;height:1.5px;background:white;transition:background .45s}}
nav.sc .hbg span{{background:var(--dark)}}

/* ── HERO ── */
#hero{{height:100vh;min-height:640px;position:relative;display:flex;align-items:center;justify-content:center;text-align:center;overflow:hidden}}
.hbg-img{{position:absolute;inset:0;background:linear-gradient(160deg,rgba(0,0,0,.62) 0%,rgba(0,0,0,.32) 55%,rgba(0,0,0,.55) 100%),url('{img(p["hero_id"])}') center/cover no-repeat}}
.hbg-img::after{{content:'';position:absolute;bottom:0;left:0;right:0;height:30%;background:linear-gradient(to bottom,transparent,var(--bg))}}
.hc{{position:relative;z-index:1;max-width:760px;padding:0 1.5rem}}
.heyebrow{{display:inline-block;font-size:.68rem;font-weight:500;letter-spacing:.22em;text-transform:uppercase;color:rgba(255,255,255,.8);background:rgba(255,255,255,.1);border:1px solid rgba(255,255,255,.2);padding:.38rem 1.2rem;border-radius:100px;margin-bottom:1.6rem;backdrop-filter:blur(4px)}}
.htitle{{font-family:var(--fh);font-size:clamp(3rem,7.5vw,5.6rem);font-weight:400;font-style:italic;color:white;line-height:1.07;margin-bottom:1.5rem;letter-spacing:-.01em}}
.hsub{{font-size:1rem;font-weight:300;color:rgba(255,255,255,.72);line-height:1.82;max-width:520px;margin:0 auto 2.8rem}}
.hbtns{{display:flex;gap:1rem;justify-content:center;flex-wrap:wrap}}
.btn-a{{font-size:.76rem;font-weight:500;letter-spacing:.12em;text-transform:uppercase;text-decoration:none;background:var(--acc);color:white;padding:.9rem 2.3rem;border-radius:100px;transition:background .3s,transform .2s}}
.btn-a:hover{{background:var(--acc2);transform:translateY(-2px)}}
.btn-b{{font-size:.76rem;font-weight:400;letter-spacing:.12em;text-transform:uppercase;text-decoration:none;border:1px solid rgba(255,255,255,.45);color:rgba(255,255,255,.9);padding:.9rem 2.3rem;border-radius:100px;transition:background .3s,border-color .3s}}
.btn-b:hover{{background:rgba(255,255,255,.1);border-color:white}}
.scroll-hint{{position:absolute;bottom:2.5rem;left:50%;transform:translateX(-50%);z-index:1;display:flex;flex-direction:column;align-items:center;gap:.55rem;color:rgba(255,255,255,.42);font-size:.6rem;letter-spacing:.2em;text-transform:uppercase}}
.scroll-hint::after{{content:'';width:1px;height:46px;background:linear-gradient(to bottom,rgba(255,255,255,.45),transparent);animation:sdrop 2s ease-in-out infinite}}
@keyframes sdrop{{0%,100%{{opacity:0;transform:scaleY(0);transform-origin:top}}50%{{opacity:1;transform:scaleY(1);transform-origin:top}}}}

/* ── STATS ── */
.stats-bar{{background:var(--dark);padding:3.2rem 5%}}
.stats-grid{{max-width:1100px;margin:0 auto;display:grid;grid-template-columns:repeat(4,1fr);gap:2rem;text-align:center}}
.sn{{font-family:var(--fh);font-size:3rem;font-weight:400;font-style:italic;color:var(--acc2);line-height:1;margin-bottom:.3rem}}
.sl2{{font-size:.7rem;font-weight:400;letter-spacing:.14em;text-transform:uppercase;color:rgba(255,255,255,.45)}}

/* ── ABOUT ── */
#about{{background:var(--bg);padding:7rem 5%}}
.about-in{{max-width:1200px;margin:0 auto;display:grid;grid-template-columns:1fr 1fr;gap:5rem;align-items:center}}
.aimg-wrap{{position:relative}}
.aimg-main{{width:100%;aspect-ratio:4/5;object-fit:cover;border-radius:4px;display:block}}
.aimg-small{{position:absolute;bottom:-2rem;right:-2rem;width:52%;aspect-ratio:4/3;object-fit:cover;border-radius:4px;border:5px solid var(--bg);box-shadow:0 16px 48px rgba(0,0,0,.18)}}
.aimg-badge{{position:absolute;top:2rem;left:-1.5rem;background:var(--acc);color:white;padding:1.1rem 1.3rem;border-radius:4px;text-align:center}}
.aimg-badge strong{{display:block;font-family:var(--fh);font-size:2.2rem;font-weight:400;font-style:italic;line-height:1;margin-bottom:.15rem}}
.aimg-badge span{{font-size:.6rem;letter-spacing:.14em;text-transform:uppercase;color:rgba(255,255,255,.75)}}
.atext .lbl{{font-size:.67rem;font-weight:500;letter-spacing:.22em;text-transform:uppercase;color:var(--acc);margin-bottom:.9rem}}
.atext .h2{{font-family:var(--fh);font-size:clamp(2rem,4vw,3rem);font-weight:400;line-height:1.18;color:var(--dark)}}
.atext .h2 em{{font-style:italic;color:var(--acc)}}
.adiv{{width:44px;height:2px;background:var(--acc);margin:1.8rem 0}}
.atext p{{font-size:.95rem;font-weight:300;line-height:1.9;color:var(--mid);margin-bottom:1rem}}
.asig{{font-family:var(--fh);font-size:1.8rem;font-weight:400;font-style:italic;color:var(--dark);margin-top:1.6rem}}
.asig small{{display:block;font-family:var(--fb);font-size:.67rem;font-style:normal;font-weight:500;letter-spacing:.13em;text-transform:uppercase;color:var(--acc);margin-top:.22rem}}

/* ── SERVICES ── */
#services{{background:var(--light);padding:7rem 5%}}
.services-in{{max-width:1200px;margin:0 auto}}
.sec-head{{margin-bottom:3.8rem}}
.lbl{{font-size:.67rem;font-weight:500;letter-spacing:.22em;text-transform:uppercase;color:var(--acc);margin-bottom:.9rem}}
.h2{{font-family:var(--fh);font-size:clamp(2rem,4vw,3rem);font-weight:400;line-height:1.18;color:var(--dark)}}
.h2 em{{font-style:italic;color:var(--acc)}}
.srv-grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:1.5rem}}
.srv-card{{background:var(--bg);border-radius:6px;overflow:hidden;transition:transform .35s,box-shadow .35s}}
.srv-card:hover{{transform:translateY(-6px);box-shadow:0 20px 56px rgba(0,0,0,.1)}}
.srv-img{{width:100%;height:210px;object-fit:cover;display:block}}
.srv-body{{padding:1.8rem 1.6rem}}
.srv-num{{font-size:.62rem;font-weight:500;letter-spacing:.18em;text-transform:uppercase;color:var(--acc);margin-bottom:.5rem}}
.srv-name{{font-family:var(--fh);font-size:1.3rem;font-weight:400;color:var(--dark);margin-bottom:.6rem}}
.srv-desc{{font-size:.85rem;font-weight:300;line-height:1.8;color:var(--mid)}}

/* ── PORTFOLIO ── */
#portfolio{{background:var(--bg);padding:7rem 5%}}
.port-in{{max-width:1200px;margin:0 auto}}
.port-head{{text-align:center;margin-bottom:3.5rem}}
.port-grid{{display:grid;grid-template-columns:repeat(12,1fr);grid-template-rows:260px 260px;gap:12px}}
.pi{{overflow:hidden;border-radius:4px;position:relative;cursor:pointer}}
.pi:nth-child(1){{grid-column:span 7}}
.pi:nth-child(2){{grid-column:span 5}}
.pi:nth-child(3){{grid-column:span 4}}
.pi:nth-child(4){{grid-column:span 5}}
.pi:nth-child(5){{grid-column:span 3}}
.pi img{{width:100%;height:100%;object-fit:cover;display:block;transition:transform .6s ease}}
.pi:hover img{{transform:scale(1.06)}}
.pi-ov{{position:absolute;inset:0;background:linear-gradient(to top,rgba(0,0,0,.82) 0%,transparent 55%);opacity:0;transition:opacity .4s;display:flex;align-items:flex-end;padding:1.4rem}}
.pi:hover .pi-ov{{opacity:1}}
.pi-cap h4{{font-family:var(--fh);font-size:1.1rem;font-weight:400;font-style:italic;color:white;margin-bottom:.15rem}}
.pi-cap p{{font-size:.65rem;letter-spacing:.12em;text-transform:uppercase;color:var(--acc2)}}

/* ── WHY ── */
#why{{background:var(--dark);padding:7rem 5%}}
.why-in{{max-width:1200px;margin:0 auto;display:grid;grid-template-columns:1fr 1fr;gap:5rem;align-items:center}}
.why-text .lbl{{color:rgba(255,255,255,.45)}}
.why-text .h2{{color:white}}
.why-text .h2 em{{color:var(--acc2)}}
.why-list{{margin-top:2.8rem;display:flex;flex-direction:column;gap:1.6rem}}
.wi{{display:flex;gap:1.1rem;align-items:flex-start}}
.wi-icon{{flex-shrink:0;width:44px;height:44px;border:1px solid rgba(255,255,255,.12);border-radius:4px;display:flex;align-items:center;justify-content:center;font-size:1.1rem;margin-top:.1rem}}
.wi-title{{font-family:var(--fh);font-size:1.1rem;font-weight:400;color:white;margin-bottom:.28rem}}
.wi-desc{{font-size:.84rem;font-weight:300;line-height:1.72;color:rgba(255,255,255,.5)}}
.why-img-wrap{{position:relative}}
.why-img{{width:100%;aspect-ratio:3/4;object-fit:cover;border-radius:4px;display:block}}
.why-badge{{position:absolute;bottom:2rem;left:-2rem;background:var(--acc);padding:1.2rem 1.6rem;border-radius:4px}}
.why-badge p{{font-family:var(--fh);font-size:1.2rem;font-style:italic;color:white;line-height:1.35;margin-bottom:.15rem}}
.why-badge span{{font-size:.62rem;font-weight:500;letter-spacing:.13em;text-transform:uppercase;color:rgba(255,255,255,.7)}}

/* ── TESTIMONIALS ── */
#testimonials{{background:var(--light);padding:7rem 5%}}
.testi-in{{max-width:1100px;margin:0 auto}}
.testi-head{{text-align:center;margin-bottom:3.5rem}}
.testi-grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:1.5rem}}
.tcard{{background:var(--bg);border-radius:6px;padding:2rem 1.8rem;border:1px solid rgba(0,0,0,.06)}}
.tstars{{color:var(--acc);font-size:.9rem;letter-spacing:.08em;margin-bottom:1rem}}
.tquote{{font-family:var(--fh);font-size:1rem;font-weight:400;font-style:italic;line-height:1.65;color:var(--dark);margin-bottom:1.5rem}}
.tauthor strong{{display:block;font-size:.8rem;font-weight:600;color:var(--dark)}}
.tauthor span{{font-size:.72rem;color:var(--acc);letter-spacing:.06em}}

/* ── CONTACT ── */
#contact{{background:var(--bg);padding:7rem 5%}}
.con-in{{max-width:1200px;margin:0 auto;display:grid;grid-template-columns:1fr 1.1fr;gap:5rem;align-items:start}}
.con-left .h2{{margin-bottom:1.2rem}}
.con-left>p{{font-size:.93rem;font-weight:300;line-height:1.85;color:var(--mid);margin-bottom:2.4rem}}
.cdet{{display:flex;flex-direction:column;gap:1.2rem}}
.citem{{display:flex;gap:1rem;align-items:center}}
.cicon{{width:42px;height:42px;background:var(--acc);border-radius:50%;display:flex;align-items:center;justify-content:center;flex-shrink:0;font-size:1rem;color:white}}
.ctxt strong{{display:block;font-size:.66rem;font-weight:600;letter-spacing:.12em;text-transform:uppercase;color:var(--dark);margin-bottom:.15rem}}
.ctxt a,.ctxt span{{font-size:.9rem;font-weight:300;color:var(--mid);text-decoration:none}}
.ctxt a:hover{{color:var(--acc)}}
.cform{{background:white;border-radius:10px;padding:2.8rem;box-shadow:0 12px 48px rgba(0,0,0,.07)}}
.cform h3{{font-family:var(--fh);font-size:1.65rem;font-weight:400;font-style:italic;color:var(--dark);margin-bottom:.25rem}}
.cform>p{{font-size:.8rem;color:var(--acc);margin-bottom:1.8rem}}
.frow{{display:grid;grid-template-columns:1fr 1fr;gap:.9rem}}
.fg{{margin-bottom:.9rem}}
.fg label{{display:block;font-size:.65rem;font-weight:600;letter-spacing:.12em;text-transform:uppercase;color:var(--mid);margin-bottom:.4rem}}
.fg input,.fg select,.fg textarea{{width:100%;background:var(--light);border:1px solid rgba(0,0,0,.09);border-radius:6px;padding:.72rem .95rem;font-family:var(--fb);font-size:.88rem;font-weight:300;color:var(--dark);outline:none;transition:border-color .3s;appearance:none}}
.fg input:focus,.fg select:focus,.fg textarea:focus{{border-color:var(--acc);background:white}}
.fg textarea{{resize:vertical;min-height:105px}}
.fsub{{width:100%;background:var(--dark);color:white;border:none;padding:.95rem;font-family:var(--fb);font-size:.76rem;font-weight:600;letter-spacing:.14em;text-transform:uppercase;cursor:pointer;border-radius:100px;margin-top:.4rem;transition:background .3s}}
.fsub:hover{{background:var(--acc)}}
.fsuccess{{display:none;text-align:center;padding:2.5rem 1rem}}
.fsuccess .si{{width:52px;height:52px;background:var(--light);border-radius:50%;display:flex;align-items:center;justify-content:center;margin:0 auto 1rem;font-size:1.4rem}}
.fsuccess h4{{font-family:var(--fh);font-size:1.4rem;font-style:italic;color:var(--dark);margin-bottom:.4rem}}
.fsuccess p{{font-size:.85rem;font-weight:300;color:var(--mid)}}

/* ── FOOTER ── */
footer{{background:var(--dark);padding:4rem 5% 2.5rem}}
.ft{{display:flex;justify-content:space-between;flex-wrap:wrap;gap:2rem;padding-bottom:2.5rem;border-bottom:1px solid rgba(255,255,255,.07);margin-bottom:2rem}}
.flogo{{font-family:var(--fh);font-size:1.4rem;font-style:italic;color:var(--acc2);margin-bottom:.6rem}}
.fbrand p{{font-size:.8rem;font-weight:300;color:rgba(255,255,255,.35);line-height:1.7}}
.flinks h5{{font-size:.62rem;font-weight:600;letter-spacing:.18em;text-transform:uppercase;color:rgba(255,255,255,.4);margin-bottom:1rem}}
.flinks ul{{list-style:none;display:flex;flex-direction:column;gap:.65rem}}
.flinks a{{font-size:.83rem;font-weight:300;color:rgba(255,255,255,.35);text-decoration:none;transition:color .3s}}
.flinks a:hover{{color:var(--acc2)}}
.fb{{display:flex;justify-content:space-between;flex-wrap:wrap;gap:.4rem}}
.fb p{{font-size:.72rem;color:rgba(255,255,255,.2)}}

/* ── REVEAL ── */
.rv{{opacity:0;transform:translateY(22px);transition:opacity .68s ease,transform .68s ease}}
.rv.vis{{opacity:1;transform:none}}
.d1{{transition-delay:.1s}}.d2{{transition-delay:.2s}}.d3{{transition-delay:.3s}}.d4{{transition-delay:.4s}}

/* ── MOBILE ── */
@media(max-width:960px){{
  #about,#services,#portfolio,#why,#testimonials,#contact{{padding:5rem 5%}}
  .about-in,.why-in,.con-in{{grid-template-columns:1fr;gap:3rem}}
  .srv-grid,.testi-grid{{grid-template-columns:1fr 1fr}}
  .stats-grid{{grid-template-columns:repeat(2,1fr)}}
  .aimg-small{{display:none}}
  .why-img-wrap{{display:none}}
  .nlinks{{display:none}}
  .hbg{{display:flex}}
  .port-grid{{grid-template-columns:1fr 1fr;grid-template-rows:repeat(3,200px)}}
  .pi:nth-child(n){{grid-column:span 1}}
  .pi:nth-child(1){{grid-column:span 2}}
  .frow{{grid-template-columns:1fr}}
  .cform{{padding:1.8rem}}
  .ft{{flex-direction:column}}
}}
@media(max-width:560px){{
  .srv-grid,.testi-grid{{grid-template-columns:1fr}}
  .stats-grid{{grid-template-columns:1fr 1fr}}
  .port-grid{{grid-template-columns:1fr;grid-template-rows:none}}
  .pi{{height:200px}}
  .pi:nth-child(n){{grid-column:span 1}}
}}

/* MOBILE NAV */
.mnav{{display:none;position:fixed;inset:0;background:var(--dark);z-index:200;flex-direction:column;align-items:center;justify-content:center;gap:1.8rem}}
.mnav.open{{display:flex}}
.mnav a{{font-family:var(--fh);font-size:2.2rem;font-weight:400;font-style:italic;color:rgba(255,255,255,.85);text-decoration:none;transition:color .3s}}
.mnav a:hover{{color:var(--acc2)}}
.mclose{{position:absolute;top:1.5rem;right:5%;background:none;border:none;color:rgba(255,255,255,.5);font-size:2.2rem;cursor:pointer;line-height:1;font-family:var(--fb)}}
</style>
</head>
<body>

<div class="mnav" id="mn">
  <button class="mclose" onclick="document.getElementById('mn').classList.remove('open')">&times;</button>
  <a href="#about"        onclick="document.getElementById('mn').classList.remove('open')">Over Ons</a>
  <a href="#services"     onclick="document.getElementById('mn').classList.remove('open')">Diensten</a>
  <a href="#portfolio"    onclick="document.getElementById('mn').classList.remove('open')">Portfolio</a>
  <a href="#testimonials" onclick="document.getElementById('mn').classList.remove('open')">Reviews</a>
  <a href="#contact"      onclick="document.getElementById('mn').classList.remove('open')">Contact</a>
</div>

<nav id="nb">
  <a href="#" class="nlogo">{e(name)}</a>
  <ul class="nlinks">
    <li><a href="#about">Over Ons</a></li>
    <li><a href="#services">Diensten</a></li>
    <li><a href="#portfolio">Portfolio</a></li>
    <li><a href="#testimonials">Reviews</a></li>
    <li><a href="#contact" class="ncta">Contact</a></li>
  </ul>
  <div class="hbg" onclick="document.getElementById('mn').classList.add('open')">
    <span></span><span></span><span></span>
  </div>
</nav>

<!-- HERO -->
<section id="hero">
  <div class="hbg-img"></div>
  <div class="hc">
    <div class="heyebrow">{e(p['eyebrow'])}</div>
    <h1 class="htitle">{e(name)}</h1>
    <p class="hsub">{e(p['tagline'])}. {e(p['sub'])}</p>
    <div class="hbtns">
      <a href="#contact" class="btn-a">Neem Contact Op</a>
      <a href="#services" class="btn-b">Onze Diensten</a>
    </div>
  </div>
  <div class="scroll-hint">Ontdek</div>
</section>

<!-- STATS -->
<div class="stats-bar">
  <div class="stats-grid">{stats_html}</div>
</div>

<!-- ABOUT -->
<section id="about">
  <div class="about-in">
    <div class="aimg-wrap rv">
      <img src="{img(p['about_id'],800)}" alt="{e(name)}" class="aimg-main">
      <img src="{img(p['about2_id'],500)}" alt="{e(name)}" class="aimg-small">
      <div class="aimg-badge">
        <strong>✦</strong>
        <span>Amsterdam</span>
      </div>
    </div>
    <div class="atext">
      <div class="lbl rv">Over Ons</div>
      <h2 class="h2 rv d1">{e(name)}<br><em>in Amsterdam</em></h2>
      <div class="adiv rv d2"></div>
      <p class="rv d2">{e(p['about_p1'])}</p>
      <p class="rv d3">{e(p['about_p2'])}</p>
      <div class="asig rv d4">
        {e(name)}
        <small>{e(cat_display)} · Amsterdam</small>
      </div>
    </div>
  </div>
</section>

<!-- SERVICES -->
<section id="services">
  <div class="services-in">
    <div class="sec-head">
      <div class="lbl rv">Wat Wij Doen</div>
      <h2 class="h2 rv d1">Onze <em>Diensten</em></h2>
    </div>
    <div class="srv-grid">
      <div class="srv-card rv">
        <img src="{img(p['srv1_id'],600)}" alt="{e(s1n)}" class="srv-img">
        <div class="srv-body">
          <div class="srv-num">01</div>
          <h3 class="srv-name">{e(s1n)}</h3>
          <p class="srv-desc">{e(s1d)}</p>
        </div>
      </div>
      <div class="srv-card rv d1">
        <img src="{img(p['srv2_id'],600)}" alt="{e(s2n)}" class="srv-img">
        <div class="srv-body">
          <div class="srv-num">02</div>
          <h3 class="srv-name">{e(s2n)}</h3>
          <p class="srv-desc">{e(s2d)}</p>
        </div>
      </div>
      <div class="srv-card rv d2">
        <img src="{img(p['srv3_id'],600)}" alt="{e(s3n)}" class="srv-img">
        <div class="srv-body">
          <div class="srv-num">03</div>
          <h3 class="srv-name">{e(s3n)}</h3>
          <p class="srv-desc">{e(s3d)}</p>
        </div>
      </div>
    </div>
  </div>
</section>

<!-- PORTFOLIO -->
<section id="portfolio">
  <div class="port-in">
    <div class="port-head">
      <div class="lbl rv">Ons Werk</div>
      <h2 class="h2 rv d1">Recente <em>Projecten</em></h2>
    </div>
    <div class="port-grid">
      <div class="pi rv">
        <img src="{img(port[0],900)}" alt="{e(pl[0][1])}">
        <div class="pi-ov"><div class="pi-cap"><p>{e(pl[0][0])}</p><h4>{e(pl[0][1])}</h4></div></div>
      </div>
      <div class="pi rv d1">
        <img src="{img(port[1],700)}" alt="{e(pl[1][1])}">
        <div class="pi-ov"><div class="pi-cap"><p>{e(pl[1][0])}</p><h4>{e(pl[1][1])}</h4></div></div>
      </div>
      <div class="pi rv">
        <img src="{img(port[2],600)}" alt="{e(pl[2][1])}">
        <div class="pi-ov"><div class="pi-cap"><p>{e(pl[2][0])}</p><h4>{e(pl[2][1])}</h4></div></div>
      </div>
      <div class="pi rv d1">
        <img src="{img(port[3],700)}" alt="{e(pl[3][1])}">
        <div class="pi-ov"><div class="pi-cap"><p>{e(pl[3][0])}</p><h4>{e(pl[3][1])}</h4></div></div>
      </div>
      <div class="pi rv d2">
        <img src="{img(port[4],500)}" alt="{e(pl[4][1])}">
        <div class="pi-ov"><div class="pi-cap"><p>{e(pl[4][0])}</p><h4>{e(pl[4][1])}</h4></div></div>
      </div>
    </div>
  </div>
</section>

<!-- WHY US -->
<section id="why">
  <div class="why-in">
    <div class="why-text">
      <div class="lbl rv">Waarom Wij</div>
      <h2 class="h2 rv d1">{wt_html}</h2>
      <div class="why-list">
        <div class="wi rv d1"><div class="wi-icon">{u1i}</div><div><div class="wi-title">{e(u1t)}</div><div class="wi-desc">{e(u1d)}</div></div></div>
        <div class="wi rv d2"><div class="wi-icon">{u2i}</div><div><div class="wi-title">{e(u2t)}</div><div class="wi-desc">{e(u2d)}</div></div></div>
        <div class="wi rv d3"><div class="wi-icon">{u3i}</div><div><div class="wi-title">{e(u3t)}</div><div class="wi-desc">{e(u3d)}</div></div></div>
        <div class="wi rv d4"><div class="wi-icon">{u4i}</div><div><div class="wi-title">{e(u4t)}</div><div class="wi-desc">{e(u4d)}</div></div></div>
      </div>
    </div>
    <div class="why-img-wrap rv d2">
      <img src="{img(p['why_id'],700)}" alt="{e(name)}" class="why-img">
      <div class="why-badge">
        <p>{e(name)}</p>
        <span>{e(cat_display)} · Amsterdam</span>
      </div>
    </div>
  </div>
</section>

<!-- TESTIMONIALS -->
<section id="testimonials">
  <div class="testi-in">
    <div class="testi-head">
      <div class="lbl rv">Klantervaringen</div>
      <h2 class="h2 rv d1">Wat onze klanten <em>zeggen</em></h2>
    </div>
    <div class="testi-grid">
      <div class="tcard rv">
        <div class="tstars">★★★★★</div>
        <p class="tquote">"{e(t1q)}"</p>
        <div class="tauthor"><strong>{e(t1a)}</strong><span>{e(t1s)}</span></div>
      </div>
      <div class="tcard rv d1">
        <div class="tstars">★★★★★</div>
        <p class="tquote">"{e(t2q)}"</p>
        <div class="tauthor"><strong>{e(t2a)}</strong><span>{e(t2s)}</span></div>
      </div>
      <div class="tcard rv d2">
        <div class="tstars">★★★★★</div>
        <p class="tquote">"{e(t3q)}"</p>
        <div class="tauthor"><strong>{e(t3a)}</strong><span>{e(t3s)}</span></div>
      </div>
    </div>
  </div>
</section>

<!-- CONTACT -->
<section id="contact">
  <div class="con-in">
    <div class="con-left">
      <div class="lbl rv">Contact</div>
      <h2 class="h2 rv d1">Laten we <em>kennismaken</em></h2>
      <p class="rv d2">Heeft u een vraag of wilt u een vrijblijvende offerte? Neem gerust contact met ons op — wij reageren altijd binnen 24 uur.</p>
      <div class="cdet">
        <div class="citem rv d2">
          <div class="cicon">📞</div>
          <div class="ctxt"><strong>Telefoon</strong><a href="{phone_href}">{e(phone_display)}</a></div>
        </div>
        <div class="citem rv d3">
          <div class="cicon">📍</div>
          <div class="ctxt"><strong>Adres</strong><span>{e(address)}</span></div>
        </div>
        <div class="citem rv d4">
          <div class="cicon">🕐</div>
          <div class="ctxt"><strong>Bereikbaar</strong><span>Ma – Vr: 08:00 – 18:00<br>Za: 09:00 – 14:00</span></div>
        </div>
      </div>
    </div>
    <div class="cform rv d1">
      <h3>Stuur een bericht</h3>
      <p>Wij nemen zo snel mogelijk contact met u op.</p>
      <form id="cf" onsubmit="document.getElementById('cf').style.display='none';document.getElementById('fs').style.display='block';return false">
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
    <div class="fbrand">
      <div class="flogo">{e(name)}</div>
      <p>{e(cat_display)} · Amsterdam<br>{e(phone_display)}<br>{e(address)}</p>
    </div>
    <div class="flinks">
      <h5>Navigatie</h5>
      <ul>
        <li><a href="#about">Over Ons</a></li>
        <li><a href="#services">Diensten</a></li>
        <li><a href="#portfolio">Portfolio</a></li>
        <li><a href="#testimonials">Reviews</a></li>
      </ul>
    </div>
    <div class="flinks">
      <h5>Contact</h5>
      <ul>
        <li><a href="{phone_href}">{e(phone_display)}</a></li>
        <li><a href="#contact">Stuur een bericht</a></li>
        <li><a href="#contact">Vraag een offerte</a></li>
      </ul>
    </div>
  </div>
  <div class="fb">
    <p>© 2024 {e(name)}. Alle rechten voorbehouden.</p>
    <p>{e(cat_display)} · Amsterdam</p>
  </div>
</footer>

<script>
const nb = document.getElementById('nb');
window.addEventListener('scroll', () => nb.classList.toggle('sc', scrollY > 60));
const obs = new IntersectionObserver(es => {{
  es.forEach(el => {{ if (el.isIntersecting) {{ el.target.classList.add('vis'); obs.unobserve(el.target); }} }});
}}, {{ threshold: 0.1 }});
document.querySelectorAll('.rv').forEach(el => obs.observe(el));
</script>
</body>
</html>"""

# ── GENERATE ─────────────────────────────────────────────────────────────────
seen = {}
generated = 0
for row in companies:
    name     = str(row[0]).strip()
    street   = str(row[3]).strip() if row[3] else ""
    city     = str(row[4]).strip() if row[4] else "Amsterdam"
    phone    = str(row[8]).strip() if row[8] else ""
    category = str(row[9]).strip() if row[9] else ""

    profile = get_profile(category)
    s = slug(name)
    if s in seen:
        seen[s] += 1
        s = f"{s}-{seen[s]}"
    else:
        seen[s] = 1

    with open(f"{OUT}/{s}.html", "w", encoding="utf-8") as f:
        f.write(build_page(name, street, city, phone, category, profile))
    generated += 1

print(f"Generated {generated} sites")
