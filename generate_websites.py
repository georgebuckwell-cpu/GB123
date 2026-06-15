#!/usr/bin/env python3
"""
Website generator — v3: curated stock photos + max UI/UX polish.
Downloads one hero + 3 gallery images per category from Unsplash.
Purpose: outreach / lead generation to sell web design services.
"""

import csv, os, re, html as hl, threading, time
from urllib.request import urlopen, Request
from urllib.error import URLError

OUTPUT_DIR = "websites"
IMG_DIR    = os.path.join(OUTPUT_DIR, "img")
CSV_PATH   = "/root/.claude/uploads/b553d4c3-fa71-535d-b226-64e15b822f4e/e9e48877-dataset_amsterdam1_20260614_171131429.csv"

SKIP_CATEGORIES = {
    "Park","Garden","Lake","Community garden","Area","Hiking area",
    "House","Vacation rental","Shipyard",
}

# Unsplash source URL — downloads a real photo for each keyword set
def unsplash(query, w=1400, h=900):
    q = query.replace(" ", "+")
    return f"https://source.unsplash.com/featured/{w}x{h}/?{q}"

CATEGORY_CONFIG = {
    "Bricklayer": {
        "primary":"#0f172a","accent":"#f97316","accent2":"#fb923c",
        "icon":"🧱",
        "tagline":"Building Amsterdam's Future,\nOne Brick at a Time",
        "hero_desc":"Expert bricklaying and facade restoration. Trusted by homeowners and developers across Amsterdam for craftsmanship that stands the test of time.",
        "img_hero": unsplash("bricklaying masonry wall construction"),
        "img_gallery": [unsplash("brick wall restoration"), unsplash("construction site masonry"), unsplash("amsterdam building facade")],
        "services":[("🧱","Brickwork & Pointing","Precision brickwork for new builds and repairs."),("🏛️","Facade Restoration","Breathing new life into historic Amsterdam facades."),("🔨","New Build Masonry","Structural masonry for residential and commercial projects."),("🪨","Repointing & Repairs","Weatherproof repointing to protect your property."),("✨","Heritage Stonework","Specialist restoration of ornate and historic stonework.")],
        "testimonials":[("Jan V.","Amsterdam Noord","Excellent craftsmanship. The facade looks better than ever — really professional team."),("Maria S.","De Pijp","On time, clean, and the quality is superb. Would recommend to everyone."),("Thomas B.","Jordaan","Best decision we made for our renovation. Outstanding work from start to finish.")],
        "process":[("📞","Free Consultation","Tell us about your project and we'll assess your needs."),("📋","Detailed Quote","Transparent, itemised quote with no hidden costs."),("🏗️","Expert Delivery","Skilled team delivers on time to the highest standard.")],
        "trust":["Licensed & Insured","10+ Years Experience","Free Quotes","Amsterdam Based"],
    },
    "Masonry contractor": {
        "primary":"#1c1917","accent":"#ea580c","accent2":"#f97316",
        "icon":"🏗️",
        "tagline":"Precision Masonry.\nLasting Results.",
        "hero_desc":"Professional masonry contracting for residential and commercial projects. We bring craftsmanship, reliability and quality to every job in Amsterdam.",
        "img_hero": unsplash("masonry construction brickwork"),
        "img_gallery": [unsplash("stone wall construction"), unsplash("brick laying craftsman"), unsplash("construction renovation amsterdam")],
        "services":[("🧱","Brick & Block Laying","Expert masonry for walls, structures and facades."),("🏗️","Structural Masonry","Load-bearing work to the highest standard."),("🔄","Renovation & Restoration","Sympathetic restoration that preserves character."),("🌿","Garden Walls & Patios","Beautiful outdoor structures built to last."),("🏠","Chimney Repairs","Safe, thorough chimney repair and repointing.")],
        "testimonials":[("Peter K.","Amsterdam West","Excellent work, very clean and professional. Highly recommended."),("Anna L.","Centrum","Transformed our garden wall completely. Really happy with the result."),("Rob M.","Oost","Reliable, skilled and great value for money. Will use again.")],
        "process":[("📞","Free Consultation","We discuss your project and visit the site if needed."),("📋","Transparent Quote","A detailed, fixed-price quote with no surprises."),("✅","Quality Build","Skilled tradespeople who take pride in every job.")],
        "trust":["Fully Insured","Free Site Visits","Satisfaction Guaranteed","Local Experts"],
    },
    "Carpenter": {
        "primary":"#1c1409","accent":"#d97706","accent2":"#f59e0b",
        "icon":"🪵",
        "tagline":"Crafted with Precision.\nBuilt to Last.",
        "hero_desc":"Expert carpentry and bespoke joinery for homes and businesses throughout Amsterdam. From custom furniture to full renovations, we craft spaces you'll love.",
        "img_hero": unsplash("carpentry woodworking workshop"),
        "img_gallery": [unsplash("wood furniture craftsmanship"), unsplash("carpenter tools timber"), unsplash("bespoke kitchen cabinetry")],
        "services":[("🗄️","Custom Furniture & Cabinetry","Bespoke pieces designed and built for your space."),("🪵","Flooring Installation","Solid wood, engineered and laminate flooring fitted perfectly."),("🚪","Doors & Windows","New installations, repairs and draught-proofing."),("🏠","Renovations & Fit-outs","Complete interior transformations from start to finish."),("🪜","Stairs & Balustrades","Beautiful, safe staircases crafted to your specification.")],
        "testimonials":[("Sophie D.","Oud-West","Our new kitchen is absolutely stunning. Incredible craftsmanship."),("Erik J.","Buitenveldert","Built exactly what we envisioned — and on budget. Amazing."),("Clara M.","Rivierenbuurt","The staircase is a work of art. Couldn't be happier.")],
        "process":[("💬","Design Chat","We listen to your vision and suggest the best approach."),("📐","Precise Planning","Detailed drawings and material selection before a single cut."),("🔨","Master Craftsmanship","Hand-finished work that exceeds expectations every time.")],
        "trust":["Bespoke Craftsmanship","15+ Years Experience","Free Design Consult","5-Year Guarantee"],
    },
    "Plumber": {
        "primary":"#0c1a2e","accent":"#0ea5e9","accent2":"#38bdf8",
        "icon":"🔧",
        "tagline":"Fast, Reliable Plumbing —\nDay or Night",
        "hero_desc":"Professional plumbing for emergencies, installations and maintenance. Available 24/7 across Amsterdam — we fix it right the first time.",
        "img_hero": unsplash("plumber bathroom modern renovation"),
        "img_gallery": [unsplash("bathroom interior design"), unsplash("plumbing pipes installation"), unsplash("boiler heating system")],
        "services":[("🚨","24/7 Emergency Call-outs","Available around the clock for urgent plumbing issues."),("🔥","Boiler Installation & Service","Expert boiler fitting, servicing and repair."),("🛁","Bathroom Fitting","Full bathroom design and installation services."),("💧","Leak Detection & Repair","Fast, accurate leak finding and fixing."),("♨️","Central Heating","Installation, maintenance and power flushing.")],
        "testimonials":[("Hans B.","Amsterdam Zuid","Arrived within the hour. Fixed the leak perfectly. Lifesavers."),("Lotte V.","De Baarsjes","New bathroom is gorgeous. Clean, fast and professional."),("Dirk S.","Noord","Excellent service, fair price, and great advice. Highly recommend.")],
        "process":[("📞","Call or Book Online","Reach us any time — we respond fast, day or night."),("🔍","Diagnose & Quote","We identify the issue and give you an upfront price."),("✅","Fix & Follow Up","We fix it right and check in to make sure you're happy.")],
        "trust":["24/7 Available","Gas Safe Registered","No Call-out Fee","Fully Insured"],
    },
    "Painter": {
        "primary":"#18181b","accent":"#a855f7","accent2":"#c084fc",
        "icon":"🎨",
        "tagline":"Transforming Spaces with\nColour & Care",
        "hero_desc":"Professional interior and exterior painting and decorating for Amsterdam homes and businesses. Flawless finishes, minimal disruption, outstanding results.",
        "img_hero": unsplash("interior painting decorator room"),
        "img_gallery": [unsplash("freshly painted bright room"), unsplash("painter decorator professional"), unsplash("colourful interior design")],
        "services":[("🏠","Interior Painting","Perfect finishes for every room, every surface."),("🌦️","Exterior Painting","Durable, weather-resistant exterior decoration."),("🖼️","Wallpapering","Precision hanging of all wallpaper types."),("🪵","Wood Staining & Varnishing","Beautiful protective finishes for timber surfaces."),("🏢","Commercial Painting","Efficient, minimal-disruption commercial decorating.")],
        "testimonials":[("Noor A.","Vondelpark area","Incredible transformation. The finish is absolutely flawless."),("Bas W.","Watergraafsmeer","Professional, tidy and the results are stunning. 10/10."),("Eva K.","IJburg","Our office looks completely refreshed. Great team to work with.")],
        "process":[("🎨","Colour Consultation","We help you choose the perfect palette for your space."),("🛡️","Surface Preparation","Thorough prep work ensures a lasting, flawless finish."),("✨","Pristine Finish","We leave your space spotless and looking its absolute best.")],
        "trust":["Free Colour Advice","Premium Paints Only","Zero Mess Guarantee","Fully Insured"],
    },
    "Electrician": {
        "primary":"#0f172a","accent":"#eab308","accent2":"#fde047",
        "icon":"⚡",
        "tagline":"Powering Amsterdam —\nSafely & Reliably",
        "hero_desc":"Certified electricians delivering safe, reliable installation and maintenance services for homes and businesses across Amsterdam.",
        "img_hero": unsplash("electrician electrical installation professional"),
        "img_gallery": [unsplash("electrical panel wiring"), unsplash("smart home lighting modern"), unsplash("solar panel installation roof")],
        "services":[("💡","Electrical Installations","Full wiring for new builds and renovations."),("🔌","Fuse Board Upgrades","Modern consumer unit installation for safety and capacity."),("💡","Lighting Design","Ambient, task and feature lighting solutions."),("☀️","Solar & EV Charging","Future-ready energy solutions for your property."),("📋","Safety Inspections","Electrical Installation Condition Reports.")],
        "testimonials":[("Frank H.","Amsterdam Oost","Incredibly knowledgeable and thorough. Feel much safer now."),("Inge P.","Centrum","Installed our EV charger quickly and cleanly. Great service."),("Marc D.","Amstelveen","Transformed our lighting completely. The place looks amazing.")],
        "process":[("📞","Book a Visit","We arrange a convenient time to assess your requirements."),("📋","Safety Assessment","We evaluate your electrics and provide a full written quote."),("⚡","Expert Installation","Certified work completed safely, cleanly and on schedule.")],
        "trust":["DEKRA Certified","All Work Guaranteed","Free Safety Check","24h Emergency"],
    },
    "Electrical installation service": {
        "primary":"#0f172a","accent":"#eab308","accent2":"#fde047",
        "icon":"⚡",
        "tagline":"Expert Electrical Solutions\nfor Every Project",
        "hero_desc":"Reliable electrical installation services for residential and commercial clients. Safe, certified and always delivered on time.",
        "img_hero": unsplash("electrical installation wiring professional"),
        "img_gallery": [unsplash("fuse board consumer unit"), unsplash("LED lighting installation modern"), unsplash("smart home technology")],
        "services":[("🔌","New Installations","Complete electrical fit-outs for new builds and refurbs."),("🔄","Rewiring","Full and partial rewiring for older properties."),("🏠","Smart Home Systems","Control your home with the latest smart technology."),("🚨","Emergency Lighting","Safety-compliant emergency lighting systems."),("📋","Electrical Testing","Thorough testing and certification of all installations.")],
        "testimonials":[("Wim B.","Noord","Rewired our entire house with zero fuss. Brilliant team."),("Sandra K.","Zuid","Smart home system is incredible — these guys know their stuff."),("Paul V.","West","Professional, punctual and great value. Highly recommended.")],
        "process":[("📞","Get in Touch","Call or email to discuss your electrical needs."),("📐","Site Survey","We survey the site and provide a detailed, fixed quote."),("✅","Certified Completion","All work is tested, certified and handed over with full documentation.")],
        "trust":["NEN 1010 Compliant","All Work Certified","Clean & Tidy","Local Specialists"],
    },
    "Bicycle repair shop": {
        "primary":"#14532d","accent":"#22c55e","accent2":"#4ade80",
        "icon":"🚲",
        "tagline":"Get Back on the Road —\nFast",
        "hero_desc":"Expert bicycle repairs, servicing and upgrades in the heart of Amsterdam. We keep Amsterdam cycling — whatever the bike, whatever the problem.",
        "img_hero": unsplash("bicycle repair mechanic workshop"),
        "img_gallery": [unsplash("bike shop cycling amsterdam"), unsplash("bicycle maintenance tools"), unsplash("electric bike e-bike")],
        "services":[("🔧","Full Bike Service","Comprehensive inspection, adjustment and lubrication."),("🩹","Puncture Repairs","Fast, reliable tyre repairs while you wait."),("⚙️","Brake & Gear Tuning","Precise adjustment for smooth, safe riding."),("⚡","E-Bike Servicing","Specialist servicing for all electric bicycle brands."),("🛠️","Custom Builds","Build your perfect bike from the ground up.")],
        "testimonials":[("Femke O.","Oost","Fixed in 20 minutes and at a fair price. My go-to bike shop."),("Joost L.","Centrum","Great service on my e-bike. They really know their stuff."),("Roos V.","West","Super friendly and fast. Would never go anywhere else.")],
        "process":[("🚲","Bring Your Bike","Drop in or book an appointment — we're always welcoming."),("🔍","Free Diagnostic","We inspect your bike and tell you exactly what it needs."),("✅","Back on the Road","Most repairs done same-day. Riding again in no time.")],
        "trust":["Same-Day Repairs","All Brands Welcome","Free Diagnostics","E-Bike Specialists"],
    },
    "Bicycle Shop": {
        "primary":"#14532d","accent":"#22c55e","accent2":"#4ade80",
        "icon":"🚲",
        "tagline":"Amsterdam's Trusted\nBike Specialists",
        "hero_desc":"Quality bikes, expert repairs and everything a cyclist needs. Your local Amsterdam bike shop — passionate about cycling since day one.",
        "img_hero": unsplash("bicycle shop bikes cycling"),
        "img_gallery": [unsplash("city bike amsterdam cycling"), unsplash("road bike mountain bike"), unsplash("electric bike modern")],
        "services":[("🛒","New Bike Sales","City, road, mountain and e-bikes from top brands."),("🔧","Bike Servicing","Full service and repairs by expert mechanics."),("🎽","Accessories & Parts","Lights, locks, helmets, bags and everything in between."),("⚡","E-Bike Expertise","Test rides, sales and servicing of electric bikes."),("♻️","Second-hand Bikes","Quality pre-owned bikes at great prices.")],
        "testimonials":[("Lars P.","Jordaan","Best bike shop in Amsterdam. Knowledgeable staff and great range."),("Hanna M.","De Pijp","Found the perfect city bike here. Amazing advice and service."),("Kees R.","Noord","Bought my e-bike here — couldn't be happier with it.")],
        "process":[("💬","Expert Advice","Tell us how you ride and we'll find your perfect bike."),("🚲","Test Ride","Take your favourite bikes for a spin before you decide."),("🛒","Ride Away Happy","We set up your new bike perfectly before you leave.")],
        "trust":["Expert Staff","Test Rides Available","All Brands Stocked","Service Guarantee"],
    },
    "Photographer": {
        "primary":"#0c0a09","accent":"#d97706","accent2":"#f59e0b",
        "icon":"📸",
        "tagline":"Moments Captured.\nStories Told.",
        "hero_desc":"Professional photography for portraits, events, products and commercial projects. Every image tells a story — let us tell yours beautifully.",
        "img_hero": unsplash("photographer studio professional camera"),
        "img_gallery": [unsplash("portrait photography beautiful light"), unsplash("event photography people"), unsplash("product photography commercial")],
        "services":[("👤","Portrait Photography","Authentic, flattering portraits that capture your personality."),("🎉","Event Coverage","Full event documentation from arrival to last dance."),("📦","Commercial & Product","High-impact imagery that makes your products shine."),("💼","Corporate Headshots","Professional headshots for individuals and teams."),("🖥️","Editing & Retouching","Expert post-production to perfect every image.")],
        "testimonials":[("Olivia T.","Amsterdam","Absolutely stunning photos. Captured exactly the feel we wanted."),("Michael R.","Centrum","Our product photos look incredible. Sales have gone up noticeably."),("Emma S.","Zuid","The most natural, beautiful headshots I've ever had. Thank you!")],
        "process":[("💬","Creative Brief","We discuss your vision, style and requirements in detail."),("📸","The Shoot","A relaxed, professional session guided from start to finish."),("🖼️","Gallery Delivery","Edited, high-resolution images delivered to your private gallery.")],
        "trust":["Fast Turnaround","Full Commercial Rights","Private Online Gallery","100% Satisfaction"],
    },
    "Photography studio": {
        "primary":"#0c0a09","accent":"#d97706","accent2":"#f59e0b",
        "icon":"📸",
        "tagline":"Creative Photography\nStudio in Amsterdam",
        "hero_desc":"A fully equipped, professionally lit studio for portraits, fashion, products and creative projects. Everything you need to create stunning imagery.",
        "img_hero": unsplash("photography studio professional lighting"),
        "img_gallery": [unsplash("studio portrait photography"), unsplash("product photography white background"), unsplash("fashion photography editorial")],
        "services":[("🏢","Studio Hire","Hire our fully equipped studio by the hour or day."),("👤","Portrait Sessions","Relaxed, flattering portrait photography for everyone."),("👗","Fashion & Editorial","High-end fashion and editorial photography."),("📦","Product Photography","Clean, commercial product images for every platform."),("🎬","Video Shoots","Professional video production in our versatile studio space.")],
        "testimonials":[("Zara M.","Fashion brand","The best studio in Amsterdam. Perfect light, great team."),("Tim H.","E-commerce","Our product photos are transformed. Sales up 40% since the shoot."),("Nina P.","Model","So professional and the results are stunning every time.")],
        "process":[("📅","Book Your Session","Choose your date and session type — we'll handle the rest."),("💡","Studio Setup","We prep the lighting, backdrops and equipment for your vision."),("🖼️","Delivered & Edited","Professionally edited images delivered within 5 working days.")],
        "trust":["Professional Equipment","Flexible Hire","Fast Delivery","All Skill Levels Welcome"],
    },
    "Commercial photographer": {
        "primary":"#0c0a09","accent":"#c2410c","accent2":"#ea580c",
        "icon":"📷",
        "tagline":"Visual Excellence\nfor Your Brand",
        "hero_desc":"High-impact commercial photography that makes brands stand out. We create images that sell, inspire and connect with your audience.",
        "img_hero": unsplash("commercial brand photography professional"),
        "img_gallery": [unsplash("advertising campaign photography"), unsplash("brand identity visual"), unsplash("corporate photography office")],
        "services":[("🏢","Brand Photography","Consistent, powerful visuals that define your brand identity."),("📦","Product Shoots","Studio and lifestyle product photography that drives conversions."),("💼","Corporate Portraits","Professional portraits for executives and teams."),("📢","Advertising Campaigns","Campaign imagery for print, digital and out-of-home."),("📱","Social Media Content","Scroll-stopping imagery optimised for every platform.")],
        "testimonials":[("Brand Manager","Amsterdam","Transformed our brand visuals completely. Exceptional quality."),("Marketing Director","Retail chain","These photos have been our best performing content this year."),("CEO, Startup","Amsterdam","Professional, creative and incredibly easy to work with.")],
        "process":[("📋","Creative Brief","We develop a detailed shot list aligned with your brand goals."),("📸","Professional Shoot","Expert direction to bring out the best in every subject."),("🚀","Ready to Publish","Retouched, formatted images ready for every platform.")],
        "trust":["Commercial Licensing","Art Direction Included","48h Rush Delivery","NDA Available"],
    },
    "Photography service": {
        "primary":"#0c0a09","accent":"#d97706","accent2":"#f59e0b",
        "icon":"📸",
        "tagline":"Professional Photography\nServices in Amsterdam",
        "hero_desc":"Capturing your most important moments with skill, artistry and heart. Photography services tailored to every occasion.",
        "img_hero": unsplash("photography beautiful moment capture"),
        "img_gallery": [unsplash("wedding photography couple"), unsplash("event photography celebration"), unsplash("family portrait photography")],
        "services":[("🎉","Event Photography","Full coverage of weddings, parties and corporate events."),("👤","Portrait Sessions","Beautiful, natural portraits for all the family."),("📖","Documentary","Authentic storytelling photography for editorial and personal projects."),("🖥️","Editing & Retouching","Expert post-production for your own photos too."),("🖼️","Print Services","Museum-quality prints delivered to your door.")],
        "testimonials":[("Anna V.","Amsterdam","Our wedding photos are breathtaking. So glad we chose them."),("Peter L.","Oost","Family portraits that we'll treasure forever. Wonderful experience."),("Sara B.","Centrum","Talented, professional and so easy to work with.")],
        "process":[("💬","Initial Consultation","We discuss your needs, style preferences and expectations."),("📸","The Session","A professional shoot guided to get the best from every moment."),("🖼️","Gallery Delivery","Online gallery of edited images ready within 7 days.")],
        "trust":["All Occasions","Fast Delivery","Print Options","Fully Insured"],
    },
    "Yoga studio": {
        "primary":"#1a2e1e","accent":"#4ade80","accent2":"#86efac",
        "icon":"🧘",
        "tagline":"Find Your Balance.\nFind Your Peace.",
        "hero_desc":"A welcoming, inclusive yoga studio for all levels in Amsterdam. Whatever your experience, we have a class that will nurture your body and calm your mind.",
        "img_hero": unsplash("yoga studio serene meditation wellness"),
        "img_gallery": [unsplash("yoga class group instructor"), unsplash("meditation mindfulness calm"), unsplash("yoga pose strength flexibility")],
        "services":[("🌅","Hatha Yoga","Classic postures and breathing for strength and flexibility."),("🌊","Vinyasa Flow","Dynamic, flowing sequences that energise and challenge."),("🌙","Yin Yoga","Deep, restorative poses held for longer to release tension."),("🧒","Kids Yoga","Fun, playful yoga sessions designed for children."),("🎯","Private Sessions","One-to-one sessions tailored entirely to your needs.")],
        "testimonials":[("Miriam K.","Amsterdam","This studio changed my life. So welcoming and professional."),("David H.","Oost","Best yoga I've ever practised. The instructors are phenomenal."),("Lena S.","De Pijp","The Yin classes are incredible. I leave feeling completely renewed.")],
        "process":[("👋","Welcome Session","Your first class is on us — no experience needed."),("🎯","Find Your Class","We guide you to the perfect class for your level and goals."),("🌱","Grow Your Practice","Progress at your pace with a supportive, expert community.")],
        "trust":["All Levels Welcome","First Class Free","Certified Instructors","Small Class Sizes"],
    },
    "Dog trainer": {
        "primary":"#1c1430","accent":"#a78bfa","accent2":"#c4b5fd",
        "icon":"🐕",
        "tagline":"Happier Dogs.\nHappier Owners.",
        "hero_desc":"Positive, reward-based dog training for puppies and adult dogs in Amsterdam. We solve behaviour problems and build a bond you'll both love.",
        "img_hero": unsplash("dog training professional happy"),
        "img_gallery": [unsplash("puppy training obedience"), unsplash("dog owner bond outdoors"), unsplash("dog agility training park")],
        "services":[("🐶","Puppy Classes","Essential early training for a confident, well-mannered dog."),("🎯","One-to-One Training","Personalised sessions at home or in a chosen location."),("📚","Obedience Training","Basic to advanced commands taught with positive methods."),("🧠","Behaviour Consultation","Expert analysis and solutions for challenging behaviours."),("👥","Group Classes","Socialisation and training in a fun group environment.")],
        "testimonials":[("Joep V.","Amsterdam Noord","Our dog is transformed. Can't believe the difference. Amazing!"),("Sanne B.","West","Patient, knowledgeable and brilliant with our nervous rescue dog."),("Arjan D.","Zuid","The puppy classes were brilliant. Our puppy is an angel now.")],
        "process":[("📋","Behaviour Assessment","We assess your dog's needs, history and specific challenges."),("🎯","Tailored Programme","A training plan designed specifically for you and your dog."),("🐾","Lasting Results","Ongoing support to make sure the good behaviour sticks.")],
        "trust":["Positive Methods Only","All Breeds Welcome","Proven Results","Ongoing Support"],
    },
    "Pet trainer": {
        "primary":"#1c1430","accent":"#a78bfa","accent2":"#c4b5fd",
        "icon":"🐾",
        "tagline":"Expert Pet Training\nin Amsterdam",
        "hero_desc":"Professional animal training using proven, positive methods. Building better relationships between pets and their owners across Amsterdam.",
        "img_hero": unsplash("pet training animals professional"),
        "img_gallery": [unsplash("dog training outdoor"), unsplash("pet owner happy animal"), unsplash("animal behaviour training")],
        "services":[("📋","Behavioural Assessment","In-depth assessment to understand your pet's needs."),("🎯","One-to-One Sessions","Private training tailored to your pet and your goals."),("👥","Group Workshops","Socialisation and training in a supportive group setting."),("🧠","Anxiety & Aggression","Specialist support for complex behavioural challenges."),("📚","Obedience Training","Building reliable responses and good manners.")],
        "testimonials":[("Kim O.","Amsterdam","Incredible results with our reactive dog. Highly recommend."),("Sam L.","Oost","Expert, patient and genuinely brilliant with animals."),("Bas T.","Noord","Our anxious cat is so much calmer now. Life-changing service.")],
        "process":[("📞","Initial Chat","We discuss your pet's history and your goals in detail."),("🔍","Assessment","An in-person assessment to observe behaviour first-hand."),("🎯","Training Plan","A bespoke programme for measurable, lasting improvement.")],
        "trust":["Positive Methods Only","All Species Welcome","Certified Trainers","Free Initial Call"],
    },
    "Tutoring service": {
        "primary":"#0f2044","accent":"#3b82f6","accent2":"#60a5fa",
        "icon":"📚",
        "tagline":"Unlock Every Student's\nPotential",
        "hero_desc":"Expert tutoring in Amsterdam for school, university and professional development. We inspire confidence, build skills and deliver measurable results.",
        "img_hero": unsplash("tutoring education student learning"),
        "img_gallery": [unsplash("student studying books concentration"), unsplash("teacher mentor education"), unsplash("exam success university")],
        "services":[("🔢","Maths & Science","Clear, patient explanations from experienced specialists."),("🌍","Languages","Dutch, English, French, German and more."),("📝","Exam Preparation","Targeted revision programmes for top grades."),("🎓","University Applications","Personal statement coaching and application guidance."),("💻","Online Tutoring","Flexible, effective sessions via video call.")],
        "testimonials":[("Parent of Tom K.","Amsterdam Zuid","Tom went from a D to an A in maths. Genuinely life-changing."),("Student, 17","Amstelveen","Finally understand chemistry. My confidence is through the roof."),("Parent of Lisa V.","Centrum","Incredibly professional and the results speak for themselves.")],
        "process":[("📋","Assessment","We identify gaps, strengths and exactly what's needed to succeed."),("🎯","Personalised Plan","A tailored programme aligned with the student's goals and schedule."),("📈","Measurable Progress","Regular progress reports so you always know how it's going.")],
        "trust":["DBS Checked Tutors","Guaranteed Progress","Flexible Scheduling","All Levels"],
    },
    "Private tutor": {
        "primary":"#0f2044","accent":"#3b82f6","accent2":"#60a5fa",
        "icon":"📖",
        "tagline":"Personalised Learning\nThat Gets Results",
        "hero_desc":"Tailored private tutoring for students of all ages and levels. We build understanding, confidence and the skills to achieve real academic success.",
        "img_hero": unsplash("private tutoring one on one education"),
        "img_gallery": [unsplash("student notebook studying"), unsplash("learning classroom education"), unsplash("academic success grades")],
        "services":[("🎯","1-on-1 Tuition","Fully personalised sessions focused entirely on the student."),("📚","Homework Support","Clear, patient help with daily school work and assignments."),("📝","Exam Coaching","Proven strategies and practice papers for top exam results."),("👩‍🏫","Subject Specialists","Expert tutors for every subject and curriculum."),("💻","Online & In-person","Flexible sessions to suit every schedule and location.")],
        "testimonials":[("Parent","Amsterdam Oost","Results improved dramatically. Warm, encouraging and expert."),("Adult learner","Centrum","Finally cracked Dutch grammar! Patient and brilliant teacher."),("Student, 15","Noord","Makes everything so clear. Wish I'd found this tutor sooner.")],
        "process":[("💬","Free Intro Call","We discuss the student's needs, challenges and ambitions."),("📐","Custom Plan","A structured learning plan built around the student's schedule."),("📈","Track & Improve","Regular check-ins to adapt and accelerate progress.")],
        "trust":["Free First Session","All Subjects","Flexible Hours","DBS Checked"],
    },
    "Education center": {
        "primary":"#0f2044","accent":"#3b82f6","accent2":"#60a5fa",
        "icon":"🏫",
        "tagline":"Inspiring Minds.\nBuilding Futures.",
        "hero_desc":"A dedicated education centre helping students of all ages achieve their full academic potential with expert tuition and personalised support.",
        "img_hero": unsplash("education centre learning students"),
        "img_gallery": [unsplash("classroom teaching modern"), unsplash("student success achievement"), unsplash("online learning digital education")],
        "services":[("📚","Academic Programmes","Structured courses covering all major subjects and levels."),("📝","Test Preparation","Intensive prep programmes for any exam."),("📖","After-School Support","Daily homework help and study skills training."),("👨‍💼","Adult Learning","Upskilling and professional development courses."),("💻","Online Courses","Learn from anywhere with our online learning platform.")],
        "testimonials":[("Parent of student","Amsterdam","My daughter's grades have soared. Excellent teachers here."),("Adult student","West","Completed my language course and got the job I wanted. Thank you!"),("Parent","Zuid","Wonderful environment and incredibly supportive staff.")],
        "process":[("📋","Initial Assessment","We evaluate skills and learning goals for each student."),("🎯","Tailored Programme","A personalised study plan designed for success."),("🏆","Achieve & Progress","Ongoing support to reach targets and set new ones.")],
        "trust":["Qualified Educators","Small Class Sizes","Online & In-person","Progress Reports"],
    },
    "Mover": {
        "primary":"#0f1b35","accent":"#3b82f6","accent2":"#60a5fa",
        "icon":"🚚",
        "tagline":"Your Move,\nMade Easy",
        "hero_desc":"Professional, careful removals for homes and offices across Amsterdam and beyond. We handle everything so moving day is stress-free.",
        "img_hero": unsplash("moving house removals professional"),
        "img_gallery": [unsplash("moving boxes packing careful"), unsplash("removal van truck"), unsplash("new home moving furniture")],
        "services":[("🏠","Home Removals","Careful, efficient moves for houses and apartments."),("🏢","Office Relocations","Minimal-disruption business moves, any size."),("📦","Packing & Unpacking","Expert packing using quality materials to protect your belongings."),("🏭","Storage Solutions","Secure short and long-term storage for any situation."),("🌍","International Moves","Worldwide relocation services you can trust.")],
        "testimonials":[("Simone L.","Amsterdam","Moved our entire 3-bed flat without a single scratch. Brilliant."),("Office Manager","Centrum","Office move completed over a weekend with zero downtime. Excellent."),("Jonas R.","Noord","Careful, fast and friendly team. Moving day was actually enjoyable!")],
        "process":[("📋","Free Survey","We assess your move and provide a precise, competitive quote."),("📦","Expert Packing","Our team packs everything safely using professional materials."),("🚚","Delivered Safely","Your belongings arrive on time, intact and perfectly placed.")],
        "trust":["Fully Insured","No Hidden Charges","Weekend Availability","Fragile Item Specialists"],
    },
    "Moving and storage service": {
        "primary":"#0f1b35","accent":"#3b82f6","accent2":"#60a5fa",
        "icon":"📦",
        "tagline":"Stress-Free Moving\n& Secure Storage",
        "hero_desc":"Full-service removals and secure storage solutions for Amsterdam residents and businesses. Your belongings are always in safe hands.",
        "img_hero": unsplash("storage facility secure organized"),
        "img_gallery": [unsplash("moving van professional"), unsplash("storage boxes organized"), unsplash("house move packing")],
        "services":[("🚚","Local Moves","Fast, careful moves anywhere in Amsterdam."),("🌍","Long-distance Moves","Nationwide and international removals."),("🏭","Secure Storage","Clean, monitored storage units for any duration."),("📦","Packing Materials","Professional packing supplies available to purchase or hire."),("🔧","Furniture Assembly","Full assembly and disassembly service at both ends.")],
        "testimonials":[("Rachel G.","Amsterdam","Used their storage for 3 months. Clean, secure and affordable."),("Martin H.","West","Smoothest move I've ever had. Would absolutely use again."),("Fatima A.","Oost","Packed our whole house beautifully. Not a thing was damaged.")],
        "process":[("📋","Free Quote","Tell us about your move and we'll give you a fixed price."),("📦","We Pack & Collect","Our team arrives on time and handles everything professionally."),("✅","Delivered & Settled","We deliver, unpack and even reassemble furniture if needed.")],
        "trust":["Fully Insured","GPS-Tracked Vehicles","Flexible Storage","24h Support"],
    },
    "Trucking company": {
        "primary":"#1c1917","accent":"#f97316","accent2":"#fb923c",
        "icon":"🚛",
        "tagline":"Reliable Transport.\nOn Time. Every Time.",
        "hero_desc":"Professional freight and logistics services operating across the Netherlands and Europe. Your cargo, delivered safely and on schedule.",
        "img_hero": unsplash("truck freight logistics transport"),
        "img_gallery": [unsplash("highway trucking logistics"), unsplash("warehouse distribution centre"), unsplash("cargo freight loading")],
        "services":[("📦","Freight Transport","Full and part loads across the Netherlands and Europe."),("🏃","Same-day Delivery","Urgent collections and deliveries for time-critical freight."),("🎯","Pallet & Bulk Loads","Efficient handling of palletised and bulk cargo."),("❄️","Temperature Controlled","Refrigerated transport for sensitive goods."),("🌍","Cross-border Logistics","Customs-cleared international transport solutions.")],
        "testimonials":[("Logistics Manager","Amsterdam","Consistently on time and always professional. Our top carrier."),("Operations Director","Rotterdam","Handled our urgent cross-border delivery perfectly. Very impressed."),("Warehouse Manager","Noord","Reliable, careful and great communication throughout.")],
        "process":[("📞","Book Collection","Call or book online and we'll confirm your slot."),("📋","Collection & Manifest","We collect on time with full documentation."),("🚛","Tracked Delivery","Real-time tracking until your freight reaches its destination.")],
        "trust":["GPS Tracked","Fully Insured","EU-Wide Coverage","Same-day Available"],
    },
    "Courier service": {
        "primary":"#1c1917","accent":"#ef4444","accent2":"#f87171",
        "icon":"📬",
        "tagline":"Fast. Secure.\nDelivered.",
        "hero_desc":"Same-day and next-day courier services across Amsterdam and the Netherlands. When it absolutely must arrive on time, trust us.",
        "img_hero": unsplash("courier delivery fast professional"),
        "img_gallery": [unsplash("parcel delivery city"), unsplash("courier bicycle urban"), unsplash("package delivery door")],
        "services":[("⚡","Same-day Delivery","Urgent city deliveries within hours."),("📬","Next-day Courier","Reliable next-day nationwide delivery."),("📍","Parcel Tracking","Real-time tracking on every delivery."),("🏢","Business Accounts","Dedicated account management for regular business customers."),("🌍","International Shipping","Door-to-door international courier services.")],
        "testimonials":[("PA at law firm","Centrum","Delivered critical documents same day. Absolute lifesaver."),("E-commerce Manager","Amsterdam","Our delivery SLAs have never been better. Excellent partner."),("Retailer","West","Fast, reliable and the tracking is brilliant. Highly recommend.")],
        "process":[("📞","Book a Collection","Call, email or use our app to schedule a pickup."),("📦","We Collect & Dispatch","On-time collection and immediate dispatch to your recipient."),("✅","Confirmed Delivery","Proof of delivery notification as soon as it's signed for.")],
        "trust":["Same-day Available","Real-time Tracking","Insured Deliveries","Business Accounts"],
    },
    "Shipping company": {
        "primary":"#0c2340","accent":"#06b6d4","accent2":"#22d3ee",
        "icon":"🚢",
        "tagline":"Your Cargo,\nOur Commitment",
        "hero_desc":"International and domestic shipping solutions you can rely on. Expert logistics from Amsterdam to the world.",
        "img_hero": unsplash("shipping container port logistics"),
        "img_gallery": [unsplash("cargo ship ocean freight"), unsplash("customs clearance logistics"), unsplash("warehouse shipping distribution")],
        "services":[("🌍","International Freight","Worldwide sea, air and road freight solutions."),("📋","Customs Clearance","Smooth customs processing for all international shipments."),("📦","Parcel Services","Reliable parcel delivery domestically and internationally."),("🚪","Door-to-door Delivery","Complete collection and delivery management."),("🔗","Supply Chain Management","End-to-end logistics optimisation for your business.")],
        "testimonials":[("Import Manager","Amsterdam","Handles our international freight flawlessly every time."),("Export Director","Schiphol area","Customs is never a problem with this team. Brilliant service."),("SME Owner","Noord","Affordable, reliable and always communicate proactively.")],
        "process":[("📋","Freight Quote","Tell us your cargo details for a competitive, all-inclusive quote."),("📦","We Handle Logistics","Collection, documentation, customs and dispatch all managed."),("🌍","World Delivery","Real-time updates until your freight arrives at destination.")],
        "trust":["Worldwide Coverage","Customs Experts","Cargo Insurance","Track & Trace"],
    },
    "Delivery service": {
        "primary":"#1c1917","accent":"#ef4444","accent2":"#f87171",
        "icon":"🏃",
        "tagline":"Speed. Reliability.\nDelivered to Your Door.",
        "hero_desc":"Fast, dependable delivery services across Amsterdam. We deliver for businesses and individuals who need things to arrive on time, every time.",
        "img_hero": unsplash("delivery service fast urban city"),
        "img_gallery": [unsplash("food delivery package"), unsplash("express courier city"), unsplash("last mile delivery")],
        "services":[("⚡","Express Delivery","Urgent deliveries completed in hours."),("📅","Scheduled Runs","Regular collection routes for ongoing business needs."),("🏘️","Last-mile Logistics","Efficient final-mile delivery anywhere in Amsterdam."),("📍","Parcel Tracking","Real-time updates for every delivery."),("🤝","Business Contracts","Tailored agreements for high-volume senders.")],
        "testimonials":[("Restaurant owner","Oost","Deliveries are always on time and the food arrives perfect."),("Online retailer","Amsterdam","Reliable and our customers are always happy. Great service."),("Medical practice","Zuid","Critical supplies arrive exactly when promised. We trust them completely.")],
        "process":[("📦","Book Collection","Schedule online or by phone — quick and easy."),("🏃","Collected Fast","We arrive promptly at the agreed collection time."),("✅","Delivered & Confirmed","Proof of delivery straight to your inbox.")],
        "trust":["Same-hour Available","Live Tracking","Fully Insured","Business Contracts"],
    },
    "Contractor": {
        "primary":"#1c1917","accent":"#f97316","accent2":"#fb923c",
        "icon":"🏗️",
        "tagline":"Quality Contracting.\nGuaranteed Satisfaction.",
        "hero_desc":"Full-service construction and contracting for residential and commercial clients. We manage every detail so you can focus on what matters.",
        "img_hero": unsplash("construction contractor building site"),
        "img_gallery": [unsplash("renovation interior building"), unsplash("construction worker professional"), unsplash("completed building architecture")],
        "services":[("🏗️","New Build","Complete construction of new residential and commercial properties."),("🔄","Renovation","Full property renovations handled from design to completion."),("📋","Project Management","End-to-end management of your entire building project."),("✨","Fit-out & Finishing","High-quality interior fit-outs and finishing work."),("🏛️","Structural Work","Expert structural alterations and extensions.")],
        "testimonials":[("Property developer","Amsterdam","Completed on time and budget. Exceptional quality throughout."),("Home owner","Zuid","Our renovation is everything we dreamed of. Outstanding work."),("Business owner","Oost","Professional team, great communication, perfect result.")],
        "process":[("📐","Site Assessment","We assess your project and provide a detailed fixed-price quote."),("📋","Project Planning","Full schedule, material selection and team coordination."),("🏗️","Expert Delivery","Skilled tradespeople and a dedicated project manager throughout.")],
        "trust":["Fixed-price Contracts","Fully Licensed","Project Manager Assigned","10-Year Guarantee"],
    },
    "General contractor": {
        "primary":"#1c1917","accent":"#f97316","accent2":"#fb923c",
        "icon":"🏗️",
        "tagline":"From Foundation to Finish —\nWe Build It All",
        "hero_desc":"Experienced general contractors delivering quality builds across Amsterdam. One point of contact for your entire project.",
        "img_hero": unsplash("general contractor building construction management"),
        "img_gallery": [unsplash("construction site management"), unsplash("building renovation professional"), unsplash("construction finished result")],
        "services":[("📋","Project Management","Complete oversight of all trades and schedules."),("🏗️","New Construction","Residential and commercial builds to the highest standard."),("🔄","Renovations","Full property renovations from planning to completion."),("🏢","Commercial Fit-out","Efficient, professional commercial interior works."),("🤝","Subcontractor Coordination","We manage all trades — you have one contact.")],
        "testimonials":[("Developer","Amsterdam","Our go-to contractor. Always professional, always on time."),("Restaurant owner","Centrum","Delivered our full fit-out in record time. Brilliant team."),("Home owner","West","Managed everything seamlessly. The result is stunning.")],
        "process":[("📞","Initial Consultation","Discuss scope, timeline and budget with our project team."),("📐","Detailed Planning","Comprehensive project plan with fixed milestones and costs."),("🏗️","Managed Build","We coordinate everything — you just watch it come together.")],
        "trust":["Single Point of Contact","Fixed Milestones","Full Insurance Cover","Transparent Costs"],
    },
    "Construction company": {
        "primary":"#0f172a","accent":"#f97316","accent2":"#fb923c",
        "icon":"🏛️",
        "tagline":"Built on Trust.\nBuilt to Last.",
        "hero_desc":"A leading construction company delivering quality projects across Amsterdam. From foundations to finishing touches, we build with pride.",
        "img_hero": unsplash("construction company modern architecture"),
        "img_gallery": [unsplash("modern building architecture amsterdam"), unsplash("construction crew professional"), unsplash("completed building exterior")],
        "services":[("🏠","Residential Construction","Quality homes built to your exact specification."),("🏢","Commercial Projects","Offices, retail and commercial builds delivered on time."),("🏗️","Structural Engineering","Expert structural solutions for complex building challenges."),("📋","Site Management","Professional site management and health & safety compliance."),("🔑","Turnkey Solutions","Complete design-and-build packages for maximum convenience.")],
        "testimonials":[("Property investor","Amsterdam","Our best build to date. Quality, speed and communication all superb."),("Corporate client","Zuidoost","Office delivered 2 weeks early and under budget. Remarkable."),("Home buyer","Noord","Our new home is perfect. Every detail executed beautifully.")],
        "process":[("🎨","Design & Planning","Architectural design, permits and detailed project planning."),("🏗️","Construction Phase","Expert tradespeople managed by our experienced site team."),("🔑","Handover","Snagging complete, keys in hand and fully compliant sign-off.")],
        "trust":["ISO Certified","10-Year Structural Warranty","NVOB Member","Award-winning builds"],
    },
    "Home builder": {
        "primary":"#292524","accent":"#d97706","accent2":"#f59e0b",
        "icon":"🏡",
        "tagline":"Building the Home\nYou've Always Dreamed Of",
        "hero_desc":"Expert home builders delivering quality craftsmanship across Amsterdam. We turn your vision into a home you'll love for generations.",
        "img_hero": unsplash("dream home interior beautiful"),
        "img_gallery": [unsplash("modern kitchen interior design"), unsplash("living room beautiful home"), unsplash("house exterior architecture")],
        "services":[("🏡","Custom New Builds","Unique homes designed and built entirely around you."),("🔝","Extensions & Loft Conversions","Add space and value to your existing home."),("🔄","Full Renovations","Complete property transformations from top to bottom."),("🍳","Kitchen & Bathroom","Stunning kitchen and bathroom installations."),("📐","Architectural Design","In-house design service to visualise your dream home.")],
        "testimonials":[("New home owner","Amsterdam","Our dream home became reality. Incredible team to work with."),("Homeowner","Noord","Extension transformed our house. Brilliant quality and value."),("Renovation client","Zuid","Every detail was perfect. We couldn't be more delighted.")],
        "process":[("💭","Dream It","Share your vision and we'll show you what's possible."),("📐","Design It","Our architects produce detailed plans and 3D visualisations."),("🏡","Build It","Skilled craftspeople bring your dream home to life.")],
        "trust":["In-house Architects","Fixed Contracts","10-Year Guarantee","Award-winning Homes"],
    },
    "Custom home builder": {
        "primary":"#292524","accent":"#d97706","accent2":"#f59e0b",
        "icon":"🏡",
        "tagline":"Your Vision.\nOur Craftsmanship.",
        "hero_desc":"Bespoke home building tailored exactly to your needs, lifestyle and style. Every home we build is a one-of-a-kind masterpiece.",
        "img_hero": unsplash("bespoke custom home luxury interior"),
        "img_gallery": [unsplash("luxury interior design bespoke"), unsplash("architect blueprint planning"), unsplash("finished home beautiful exterior")],
        "services":[("✏️","Bespoke Design","Unique architectural design created around your brief."),("🏡","Custom Builds","Hand-crafted homes built to a standard you won't find elsewhere."),("🔝","Extensions","Sensitive extensions that complement your existing home perfectly."),("✨","Interior Fit-out","Bespoke interior finishes from floors to ceilings."),("📋","Project Management","Complete management from planning consent to handover.")],
        "testimonials":[("Client","Amsterdam Zuid","Truly bespoke — they built exactly what we had in mind. Perfect."),("Client","Jordaan","The craftsmanship is extraordinary. Our home is a work of art."),("Client","Noord","Seamless process from start to finish. Exceptional team.")],
        "process":[("💬","Vision Workshop","An in-depth session to understand exactly what you want."),("🎨","Design Development","Full architectural drawings and material specifications."),("🏡","Masterful Build","Expert craftspeople delivering your bespoke home on time.")],
        "trust":["100% Bespoke","3D Visualisations","Fixed-price Builds","5-Star Rated"],
    },
    "Landscaper": {
        "primary":"#052e16","accent":"#22c55e","accent2":"#4ade80",
        "icon":"🌿",
        "tagline":"Beautiful Outdoor Spaces,\nExpertly Created",
        "hero_desc":"Professional landscaping and garden design across Amsterdam. We create stunning outdoor spaces that are as functional as they are beautiful.",
        "img_hero": unsplash("garden landscaping beautiful outdoor"),
        "img_gallery": [unsplash("landscape design garden plants"), unsplash("paving decking outdoor"), unsplash("garden terrace patio")],
        "services":[("✏️","Garden Design","Creative, practical garden design for every style and budget."),("🌱","Planting & Turfing","Seasonal planting schemes and premium lawn installation."),("🪨","Paving & Decking","Natural stone, porcelain and composite decking solutions."),("💧","Irrigation Systems","Efficient watering systems to keep your garden thriving."),("✂️","Maintenance Plans","Regular garden care to keep your outdoor space looking perfect.")],
        "testimonials":[("Homeowner","Amsterdam","Our garden is completely transformed. It's like a different house."),("Restaurant owner","Oost","Our terrace is now our most popular feature. Brilliant work."),("Client","Zuid","Professional, creative and the results are just stunning.")],
        "process":[("🎨","Design Concept","We visit your space and produce a detailed design proposal."),("🌱","Installation","Expert team installs your new garden to perfection."),("✂️","Ongoing Care","Optional maintenance plans to keep it beautiful year-round.")],
        "trust":["Award-winning Designs","10-Year Plant Guarantee","Fully Insured","Free Design Visit"],
    },
    "House cleaning service": {
        "primary":"#0c1f3f","accent":"#0ea5e9","accent2":"#38bdf8",
        "icon":"🧹",
        "tagline":"A Spotless Home,\nEvery Time",
        "hero_desc":"Professional domestic and commercial cleaning services across Amsterdam. Trusted, insured cleaners who treat your home as their own.",
        "img_hero": unsplash("clean modern home bright spotless"),
        "img_gallery": [unsplash("cleaning professional house"), unsplash("spotless kitchen interior"), unsplash("organised clean living space")],
        "services":[("🧹","Regular Cleaning","Weekly, fortnightly or monthly domestic cleaning."),("✨","Deep Cleaning","Thorough top-to-bottom deep cleans for any property."),("🔑","End-of-tenancy Cleaning","Landlord-approved deep cleans to secure your deposit."),("🏢","Office Cleaning","Professional workplace cleaning that impresses clients."),("🪟","Window Cleaning","Streak-free interior and exterior window cleaning.")],
        "testimonials":[("Homeowner","Amsterdam","My house has never been this clean. Exceptional attention to detail."),("Landlord","Oost","Used them for end-of-tenancy clean. Deposit returned in full."),("Office manager","Centrum","Office looks immaculate every morning. Great team.")],
        "process":[("📅","Book Online","Choose your cleaning type, date and time — takes 2 minutes."),("🔑","We Arrive & Clean","Vetted, insured cleaners who bring all their own equipment."),("✨","Enjoy the Result","Come home to a spotless, fresh-smelling property every time.")],
        "trust":["DBS Checked","Fully Insured","Eco-friendly Products","Satisfaction Guarantee"],
    },
    "Cleaning service": {
        "primary":"#0c1f3f","accent":"#0ea5e9","accent2":"#38bdf8",
        "icon":"✨",
        "tagline":"Clean Spaces.\nClear Minds.",
        "hero_desc":"Reliable cleaning services for homes and businesses across Amsterdam. We leave every space spotless, fresh and feeling brand new.",
        "img_hero": unsplash("professional cleaning service commercial"),
        "img_gallery": [unsplash("office cleaning professional"), unsplash("deep clean bathroom"), unsplash("spotless workspace")],
        "services":[("🏠","Domestic Cleaning","Regular home cleaning tailored to your schedule."),("🏢","Commercial Cleaning","Professional cleaning for offices and commercial premises."),("💎","Deep Cleans","Intensive cleaning for properties that need a thorough refresh."),("🎨","Graffiti Removal","Fast, effective removal of graffiti from any surface."),("🔬","Specialist Cleaning","Sensitive surface, post-build and specialist cleaning.")],
        "testimonials":[("Business owner","Amsterdam","Reliable, thorough and always professional. Highly recommended."),("Homeowner","West","The deep clean was transformative. Absolutely delighted."),("Facilities manager","Centrum","Our offices are spotless every day. Excellent company.")],
        "process":[("📞","Get a Quote","Tell us what you need and we'll give you a fast, fair price."),("📅","Book a Time","We arrange a convenient time and send a confirmed team."),("✨","Spotless Results","We clean to a high professional standard, guaranteed.")],
        "trust":["Vetted Staff","Eco Products","Fully Insured","Same-day Available"],
    },
    "Roofing contractor": {
        "primary":"#1c1917","accent":"#dc2626","accent2":"#ef4444",
        "icon":"🏠",
        "tagline":"Protecting Your Home\nfrom the Top Down",
        "hero_desc":"Expert roofing installation, repair and maintenance across Amsterdam. We keep the elements out and your property safe.",
        "img_hero": unsplash("roofing contractor tiles repair"),
        "img_gallery": [unsplash("roof tiles installation"), unsplash("roofer professional work"), unsplash("gutter repair maintenance")],
        "services":[("🔨","Roof Repairs","Fast, reliable repairs to stop leaks and prevent damage."),("🏠","New Roof Installation","Full roof replacements using premium materials."),("⬛","Flat Roofing","EPDM, felt and GRP flat roof systems expertly installed."),("🌧️","Gutter Cleaning & Repair","Clearing and repairing gutters to protect your property."),("🔍","Roof Inspections","Thorough surveys with a full photographic report.")],
        "testimonials":[("Homeowner","Amsterdam","Fixed our persistent leak in a single visit. Excellent work."),("Landlord","Noord","Replaced three roofs for us. Professional, fast and great value."),("Property manager","Zuid","Reliable and responsive. Our first call for any roof issue.")],
        "process":[("🔍","Free Inspection","We inspect your roof and provide a full written assessment."),("📋","Transparent Quote","Detailed quote with no hidden costs or nasty surprises."),("🏠","Expert Repair","Skilled roofers complete the work safely and efficiently.")],
        "trust":["Free Roof Survey","10-Year Guarantee","Emergency Cover","Fully Insured"],
    },
    "Plasterer": {
        "primary":"#1c1917","accent":"#ca8a04","accent2":"#eab308",
        "icon":"🪣",
        "tagline":"Flawless Walls.\nPerfect Finishes.",
        "hero_desc":"Expert plastering and skimming for homes and businesses across Amsterdam. Smooth, perfect surfaces every time — ready to paint in days.",
        "img_hero": unsplash("plastering wall smooth finish"),
        "img_gallery": [unsplash("interior wall plaster smooth"), unsplash("plasterer craftsman work"), unsplash("room renovation walls")],
        "services":[("🪣","Skimming & Plastering","Silky-smooth skim coats on walls and ceilings."),("🏠","Render & External Finishes","Durable, attractive external render systems."),("✨","Decorative Plasterwork","Coving, cornicing and ornamental plaster features."),("🧱","Dry Lining","Efficient plasterboard installation and finishing."),("🔧","Patch & Repair","Invisible repairs to damaged plaster surfaces.")],
        "testimonials":[("Homeowner","Amsterdam","Walls are absolutely perfect. You'd never know they were damaged."),("Interior designer","De Pijp","Best plasterer I've worked with. Immaculate finish every time."),("Builder","Noord","My go-to plasterer. Fast, clean and consistently excellent.")],
        "process":[("📋","Free Assessment","We assess the work needed and provide a competitive quote."),("🛡️","Surface Prep","Thorough preparation to ensure the perfect bond and finish."),("✨","Flawless Result","Smooth, paint-ready surfaces delivered on time.")],
        "trust":["Dust-free Techniques","Premium Materials","Fast Drying","Fully Insured"],
    },
    "Stucco contractor": {
        "primary":"#1c1917","accent":"#ca8a04","accent2":"#eab308",
        "icon":"🪣",
        "tagline":"Smooth Finishes.\nExceptional Quality.",
        "hero_desc":"Professional stucco and plastering contractors serving Amsterdam. Perfect walls and ceilings, every job, every time.",
        "img_hero": unsplash("stucco plaster smooth wall renovation"),
        "img_gallery": [unsplash("smooth plaster wall interior"), unsplash("render exterior wall"), unsplash("decorative plaster coving")],
        "services":[("🏠","Interior Plastering","Premium interior plaster finishes for any room."),("🏛️","External Render","Weather-resistant external render for a beautiful facade."),("✨","Ornamental Stucco","Decorative plasterwork to add character and elegance."),("🔧","Repair & Restoration","Sympathetic repairs to historic and damaged plaster."),("🧱","Dry Lining","Fast, clean plasterboard installation and taping.")],
        "testimonials":[("Home owner","Amsterdam","Flawless stucco work — the house looks completely transformed."),("Interior architect","Centrum","Consistently the best plaster finish I've ever seen. Brilliant."),("Renovator","West","On time, on budget and absolutely immaculate workmanship.")],
        "process":[("🔍","Site Survey","We assess your walls and recommend the best finish."),("📋","Fixed Quote","A detailed quote with no unexpected extras."),("✨","Perfect Finish","Smooth, beautiful results completed to schedule.")],
        "trust":["All Finish Types","Eco-friendly Mixes","Rapid Drying","5-Year Warranty"],
    },
    "Import export company": {
        "primary":"#0c2340","accent":"#06b6d4","accent2":"#22d3ee",
        "icon":"🌍",
        "tagline":"Global Trade.\nLocal Expertise.",
        "hero_desc":"Connecting Amsterdam businesses to global markets through reliable, efficient import and export services. Your gateway to the world.",
        "img_hero": unsplash("international trade port amsterdam"),
        "img_gallery": [unsplash("container ship cargo"), unsplash("customs warehouse logistics"), unsplash("global business trade")],
        "services":[("🚢","Import & Export Logistics","End-to-end handling of international trade shipments."),("📋","Customs Clearance","Expert customs documentation and duty management."),("⚖️","Trade Compliance","Ensuring full compliance with all international regulations."),("🏭","Warehousing","Secure Amsterdam warehousing for import and export goods."),("🔗","Supply Chain Consulting","Optimising your international supply chain.")],
        "testimonials":[("Import director","Amsterdam","Handles our customs brilliantly. Zero delays, zero stress."),("Exporter","Schiphol","Opened up new markets for us. Invaluable expertise and support."),("SME owner","Noord","Made international trade accessible for our small business. Excellent.")],
        "process":[("💬","Trade Consultation","We assess your import or export requirements in detail."),("📋","Full Documentation","We prepare and manage all required trade documentation."),("🌍","Seamless Delivery","Your goods move across borders smoothly and on schedule.")],
        "trust":["EU Trade Specialists","Customs Certified","Cargo Insurance","Global Network"],
    },
    "Video production service": {
        "primary":"#0c0a09","accent":"#e11d48","accent2":"#f43f5e",
        "icon":"🎬",
        "tagline":"Your Story.\nBeautifully Told.",
        "hero_desc":"Professional video production for brands, events and content creators in Amsterdam. We create video that moves, inspires and converts.",
        "img_hero": unsplash("video production film cinema professional"),
        "img_gallery": [unsplash("video camera crew filming"), unsplash("film editing post production"), unsplash("brand video marketing")],
        "services":[("🏢","Brand Films","Cinematic brand stories that define and elevate your identity."),("🎉","Event Videography","Full event coverage from highlights to full documentation."),("📱","Social Media Content","Platform-optimised short-form video that stops the scroll."),("💼","Corporate Video","Training, recruitment and internal communication video."),("🎬","Post-production & Editing","Expert editing, colour grading, motion graphics and sound.")],
        "testimonials":[("Marketing Director","Amsterdam","Our brand film generated 500k views in the first week. Exceptional."),("Event organiser","Centrum","Beautiful coverage of our conference. Client is absolutely thrilled."),("Startup founder","Noord","Our social content has never performed better. Great team.")],
        "process":[("💡","Creative Development","Script, storyboard and shot list developed with your team."),("🎬","Professional Shoot","Cinematic production using broadcast-quality equipment."),("✨","Post-production","Edit, grade, sound and delivery across all required formats.")],
        "trust":["4K & Drone Available","Fast Turnaround","Commercial Licensing","Award-winning Team"],
    },
    "Art studio": {
        "primary":"#0f0f1a","accent":"#ec4899","accent2":"#f472b6",
        "icon":"🖌️",
        "tagline":"Where Creativity\nComes to Life",
        "hero_desc":"A vibrant, inspiring creative studio in Amsterdam offering classes, workshops and bespoke commissions for all ages and skill levels.",
        "img_hero": unsplash("art studio creative painting workshop"),
        "img_gallery": [unsplash("artist painting canvas studio"), unsplash("art class workshop group"), unsplash("creative artwork colourful")],
        "services":[("🎨","Art Classes","Weekly classes in painting, drawing, sculpture and more."),("🖼️","Private Commissions","Bespoke original artwork created to your brief."),("🎉","Workshop Events","Fun, social workshops perfect for teams and celebrations."),("🏢","Studio Hire","Hire our fully equipped studio space for your own projects."),("🛒","Art Supplies","Quality materials available to purchase in-studio.")],
        "testimonials":[("Student","Amsterdam","Best art class I've ever taken. Inspiring and so much fun."),("Corporate client","Centrum","Team workshop was brilliant — everyone loved it."),("Art collector","Zuid","My commissioned piece is absolutely stunning. A true talent.")],
        "process":[("👋","Join a Class","Browse our schedule and book a session that suits you."),("🎨","Create & Learn","Expert tuition in a relaxed, inspiring atmosphere."),("🖼️","Take Home Your Art","Leave with a finished piece and new skills to build on.")],
        "trust":["All Skill Levels","Professional Materials","Small Groups","Private Events Available"],
    },
    "Website designer": {
        "primary":"#0f0f23","accent":"#7c3aed","accent2":"#8b5cf6",
        "icon":"💻",
        "tagline":"Websites That Work\nas Hard as You Do",
        "hero_desc":"Creative web design and development for businesses that want to grow. We build websites that look incredible and convert visitors into customers.",
        "img_hero": unsplash("web design technology laptop modern"),
        "img_gallery": [unsplash("website design UI UX"), unsplash("coding development computer"), unsplash("digital agency creative")],
        "services":[("🎨","Website Design","Bespoke, responsive websites that reflect your brand perfectly."),("🛒","E-commerce Development","Powerful online stores that drive sales 24/7."),("📈","SEO & Performance","Optimised sites that rank on Google and load instantly."),("✏️","Branding & Identity","Logo, colours and brand guidelines from scratch."),("🛡️","Hosting & Maintenance","Secure, fast hosting and ongoing site management.")],
        "testimonials":[("Business owner","Amsterdam","Our new website generated 3x more leads in the first month."),("E-commerce manager","Noord","Online sales up 80% since the redesign. Incredible result."),("Startup founder","Centrum","Beautiful design, fast build, exceptional value. Highly recommend.")],
        "process":[("💬","Discovery Call","We learn about your business, goals and target audience."),("🎨","Design & Build","Stunning designs approved by you before a line of code is written."),("🚀","Launch & Grow","We launch your site and support your growth with ongoing optimisation.")],
        "trust":["Mobile-first Design","Google-ready SEO","Fast Turnaround","Unlimited Revisions"],
    },
    "Handyman/Handywoman/Handyperson": {
        "primary":"#1c1917","accent":"#f59e0b","accent2":"#fbbf24",
        "icon":"🔨",
        "tagline":"No Job Too Small.\nQuality Every Time.",
        "hero_desc":"Your trusted local handyman for repairs, maintenance and small renovations across Amsterdam. Fast, reliable and always done right.",
        "img_hero": unsplash("handyman repair tools professional"),
        "img_gallery": [unsplash("home repair maintenance"), unsplash("diy tools workshop"), unsplash("home improvement renovation")],
        "services":[("🔧","General Repairs","All household repairs handled quickly and professionally."),("📦","Flat-pack Assembly","All brands assembled correctly, first time, every time."),("🪟","Tiling & Grouting","Precise tiling for kitchens, bathrooms and more."),("🚪","Door & Lock Fitting","Doors adjusted, locks changed and handles fitted."),("🎨","Painting & Decorating","Neat, professional interior painting and decorating.")],
        "testimonials":[("Homeowner","Amsterdam","Fixed 10 jobs in one visit. Fast, friendly and great value."),("Landlord","Oost","Reliable, goes above and beyond. My first call for any job."),("Tenant","West","Sorted my flat-pack nightmare in under an hour. Brilliant.")],
        "process":[("📞","Tell Us the Job","Call or message with your list — we price it quickly."),("📅","Book a Time","Flexible appointments including evenings and weekends."),("✅","Job Done Right","Professional workmanship, clean up included, every time.")],
        "trust":["No Job Too Small","Same-week Appointments","Fully Insured","Fixed Hourly Rate"],
    },
}

DEFAULT_CONFIG = {
    "primary":"#0f172a","accent":"#6366f1","accent2":"#818cf8",
    "icon":"⭐",
    "tagline":"Professional Services\nin Amsterdam",
    "hero_desc":"Trusted local professionals delivering quality services across Amsterdam. Experienced, reliable and dedicated to your satisfaction.",
    "img_hero": unsplash("professional business service amsterdam"),
    "img_gallery": [unsplash("team professional work"), unsplash("office modern workspace"), unsplash("business success amsterdam")],
    "services":[("✅","Professional Services","Expert service delivered to the highest standard."),("🏆","Quality Guaranteed","We stand behind every job we do."),("📍","Local Expertise","Deep knowledge of Amsterdam and its unique needs."),("💰","Competitive Rates","Fair, transparent pricing with no hidden costs."),("💬","Free Consultation","Talk to us first — no obligation, no pressure.")],
    "testimonials":[("Client","Amsterdam","Excellent service from start to finish. Highly recommended."),("Customer","Noord","Professional, punctual and great value. Would use again."),("Client","Zuid","Friendly, skilled and reliable. Very happy with the result.")],
    "process":[("📞","Get in Touch","Contact us to discuss your needs — we respond fast."),("📋","Receive Your Quote","A clear, competitive quote with no hidden extras."),("✅","Job Done Right","We deliver quality work and ensure you're 100% satisfied.")],
    "trust":["Fully Insured","Free Consultation","Satisfaction Guaranteed","Amsterdam Based"],
}


# ── Image downloader ──────────────────────────────────────────────────────────

def download_image(url, dest, retries=3):
    """Download a URL (following redirects) to dest. Returns True on success."""
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120 Safari/537.36",
        "Accept": "image/webp,image/apng,image/*,*/*",
    }
    for attempt in range(retries):
        try:
            req = Request(url, headers=headers)
            with urlopen(req, timeout=20) as resp:
                data = resp.read()
            if len(data) < 1000:
                raise ValueError("Response too small")
            with open(dest, "wb") as f:
                f.write(data)
            return True
        except Exception as e:
            if attempt < retries - 1:
                time.sleep(1.5 * (attempt + 1))
    return False


def fetch_category_images(cat_slug, cfg, img_base):
    """Download hero + 3 gallery images for a category. Returns paths dict or None."""
    cat_dir = os.path.join(img_base, cat_slug)
    os.makedirs(cat_dir, exist_ok=True)

    result = {}
    hero_path = os.path.join(cat_dir, "hero.jpg")
    if not os.path.exists(hero_path):
        ok = download_image(cfg["img_hero"], hero_path)
        if not ok:
            return None
    result["hero"] = f"img/{cat_slug}/hero.jpg"

    for i, url in enumerate(cfg["img_gallery"], 1):
        gpath = os.path.join(cat_dir, f"gallery{i}.jpg")
        if not os.path.exists(gpath):
            download_image(url, gpath)
        if os.path.exists(gpath):
            result[f"gallery{i}"] = f"img/{cat_slug}/gallery{i}.jpg"

    return result


# ── HTML generator ────────────────────────────────────────────────────────────

def slugify(name):
    name = name.lower()
    name = re.sub(r'[^\w\s-]', '', name)
    name = re.sub(r'[\s_]+', '-', name)
    name = re.sub(r'-+', '-', name).strip('-')
    return name[:80]


def cat_slug(cat):
    return re.sub(r'[^a-z0-9]+', '-', cat.lower()).strip('-')


def get_config(categories):
    for cat in categories:
        if cat in CATEGORY_CONFIG:
            return cat, CATEGORY_CONFIG[cat]
    return None, DEFAULT_CONFIG


def initials(name):
    words = name.strip().split()
    if len(words) >= 2:
        return (words[0][0] + words[-1][0]).upper()
    return name[:2].upper()


def stars(score):
    try:
        s = float(score)
        return "★" * int(round(s)) + "☆" * (5 - int(round(s)))
    except Exception:
        return ""


def generate_html(company, img_paths):
    name = (company.get("title") or company.get("﻿title") or "").strip()
    if not name or name in (".", "Z", ""):
        return None

    cats = [company.get(f"categories/{i}", "").strip() for i in range(9)]
    cats = [c for c in cats if c]
    primary_cat = cats[0] if cats else ""
    if primary_cat in SKIP_CATEGORIES:
        return None

    matched_cat, cfg = get_config(cats)
    cslug = cat_slug(matched_cat or primary_cat or "general")

    street  = company.get("street", "").strip()
    city    = (company.get("city", "") or "Amsterdam").strip() or "Amsterdam"
    phone   = company.get("phone", "").strip()
    score   = company.get("totalScore", "").strip()
    reviews = company.get("reviewsCount", "").strip()
    maps_url = company.get("url", "").strip()

    P = cfg["primary"]; A = cfg["accent"]; A2 = cfg.get("accent2", A)
    icon      = cfg["icon"]
    tparts    = cfg["tagline"].split("\n")
    t1, t2    = hl.escape(tparts[0]), hl.escape(tparts[1] if len(tparts)>1 else "")
    hero_desc = cfg["hero_desc"]
    svclist   = cfg["services"]
    testis    = cfg.get("testimonials", DEFAULT_CONFIG["testimonials"])
    steps     = cfg.get("process", DEFAULT_CONFIG["process"])
    trust     = cfg.get("trust", DEFAULT_CONFIG["trust"])

    mono = initials(name)
    addr = ", ".join(p for p in [street, city, "Netherlands"] if p)
    cat_label = primary_cat or "Professional Services"

    # Image paths (relative to HTML file, which is in websites/)
    hero_img  = img_paths.get("hero", "")
    gal1 = img_paths.get("gallery1",""); gal2 = img_paths.get("gallery2",""); gal3 = img_paths.get("gallery3","")

    hero_bg = f'background-image:linear-gradient(to bottom,rgba(0,0,0,0.55) 0%,rgba(0,0,0,0.45) 60%,{P} 100%),url("{hl.escape(hero_img)}");background-size:cover;background-position:center;' if hero_img else f"background:{P};"

    # Gallery section only if we have images
    gallery_html = ""
    if gal1 or gal2 or gal3:
        imgs = [g for g in [gal1,gal2,gal3] if g]
        gcards = "".join(f'<div class="gal-card" style="background-image:url(\'{hl.escape(i)}\')"></div>' for i in imgs)
        gallery_html = f"""
<div class="gallery-section">
  <div class="gallery-inner reveal">
    <p class="section-tag">Our Work</p>
    <h2 class="section-title">Recent <span>Projects</span></h2>
    <div class="gal-grid">{gcards}</div>
  </div>
</div>"""

    # Services
    svcs = "".join(f"""<div class="svc-card"><div class="svc-icon">{si}</div><h3>{hl.escape(sn)}</h3><p>{hl.escape(sd)}</p></div>""" for si,sn,sd in svclist)

    # Process
    procs = "".join(f"""<div class="step"><div class="step-num">0{i}</div><div class="step-icon">{pi}</div><h3>{hl.escape(pt)}</h3><p>{hl.escape(pd)}</p></div>""" for i,(pi,pt,pd) in enumerate(steps,1))

    # Testimonials
    ts = "".join(f"""<div class="testi-card"><div class="testi-stars">★★★★★</div><p class="testi-text">"{hl.escape(tt)}"</p><div class="testi-author"><div class="testi-avatar">{hl.escape(initials(tn))}</div><div><strong>{hl.escape(tn)}</strong><span>{hl.escape(tl)}</span></div></div></div>""" for tn,tl,tt in testis)

    # Trust badges
    tbs = "".join(f'<div class="trust-badge"><div class="trust-dot"></div>{hl.escape(t)}</div>' for t in trust)

    # Rating
    rating_html = ""
    if score and reviews:
        rating_html = f'<div class="hero-rating"><span class="hero-stars">{stars(score)}</span><span>{score} / 5 &nbsp;·&nbsp; {reviews} Google reviews</span></div>'

    phone_btn = f'<a href="tel:{hl.escape(phone)}" class="btn-primary">📞 Call Us</a>' if phone else '<a href="#contact" class="btn-primary">Get in Touch</a>'
    maps_btn  = f'<a href="{hl.escape(maps_url)}" target="_blank" class="btn-outline">📍 View on Maps</a>' if maps_url else ""

    phone_detail = f"<div class='cdetail'><div class='cdetail-icon'>📞</div><div><div class='cdetail-label'>Phone</div><div class='cdetail-val'>{hl.escape(phone)}</div></div></div>" if phone else ""
    addr_detail  = f"<div class='cdetail'><div class='cdetail-icon'>📍</div><div><div class='cdetail-label'>Address</div><div class='cdetail-val'>{hl.escape(addr)}</div></div></div>" if addr else ""

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{hl.escape(name)} | {hl.escape(cat_label)} Amsterdam</title>
<meta name="description" content="{hl.escape(hero_desc[:155])}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
<style>
*,*::before,*::after{{box-sizing:border-box;margin:0;padding:0}}
:root{{--p:{P};--a:{A};--a2:{A2};--bg:#f5f5f3;--card:#fff;--text:#111;--sub:#6b7280;--bdr:#e5e7eb;--r:16px}}
html{{scroll-behavior:smooth}}
body{{font-family:'Inter',system-ui,sans-serif;background:var(--bg);color:var(--text);-webkit-font-smoothing:antialiased;line-height:1.6}}

/* NAV */
.nav{{position:fixed;top:0;left:0;right:0;z-index:200;height:64px;padding:0 5%;display:flex;align-items:center;justify-content:space-between;background:rgba(255,255,255,0.9);backdrop-filter:blur(20px) saturate(180%);border-bottom:1px solid rgba(0,0,0,0.07);transition:box-shadow .3s}}
.nav.scrolled{{box-shadow:0 4px 30px rgba(0,0,0,.08)}}
.nav-logo{{display:flex;align-items:center;gap:10px;text-decoration:none;min-width:0}}
.monogram{{width:36px;height:36px;border-radius:9px;background:linear-gradient(135deg,var(--a),var(--a2));color:#fff;font-weight:800;font-size:.8rem;display:flex;align-items:center;justify-content:center;flex-shrink:0}}
.nav-text{{min-width:0}}
.nav-name{{font-weight:700;font-size:.9rem;color:var(--text);white-space:nowrap;overflow:hidden;text-overflow:ellipsis;max-width:200px}}
.nav-cat{{font-size:.7rem;color:var(--sub);display:block;font-weight:500}}
.nav-cta{{background:var(--a);color:#fff;padding:9px 20px;border-radius:8px;font-size:.85rem;font-weight:700;text-decoration:none;transition:opacity .2s,transform .15s;white-space:nowrap;flex-shrink:0}}
.nav-cta:hover{{opacity:.88;transform:translateY(-1px)}}

/* HERO */
.hero{{min-height:100vh;{hero_bg}display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:100px 5% 80px;position:relative;overflow:hidden}}
.hero-noise{{position:absolute;inset:0;pointer-events:none;opacity:.03;background-image:url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='4'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E");background-size:200px}}
.hero-content{{position:relative;max-width:820px}}
.hero-pill{{display:inline-flex;align-items:center;gap:8px;background:rgba(255,255,255,.12);border:1px solid rgba(255,255,255,.25);border-radius:999px;padding:6px 18px;font-size:.75rem;font-weight:700;letter-spacing:1.2px;text-transform:uppercase;color:rgba(255,255,255,.9);margin-bottom:28px;backdrop-filter:blur(8px)}}
.pill-dot{{width:7px;height:7px;border-radius:50%;background:var(--a);animation:pulse 2s infinite}}
@keyframes pulse{{0%,100%{{opacity:1;transform:scale(1)}}50%{{opacity:.5;transform:scale(.8)}}}}
.hero h1{{font-size:clamp(2.8rem,6.5vw,4.8rem);font-weight:900;color:#fff;line-height:1.02;letter-spacing:-2px;margin-bottom:10px;text-shadow:0 2px 20px rgba(0,0,0,.3)}}
.hero h1 em{{font-style:normal;color:var(--a);}}
.hero-sub{{font-size:clamp(.95rem,2vw,1.2rem);color:rgba(255,255,255,.68);max-width:560px;margin:0 auto 32px;font-weight:400;line-height:1.75}}
.hero-rating{{display:inline-flex;align-items:center;gap:10px;background:rgba(255,255,255,.1);border:1px solid rgba(255,255,255,.18);border-radius:999px;padding:8px 20px;color:rgba(255,255,255,.85);font-size:.85rem;margin-bottom:30px;backdrop-filter:blur(8px)}}
.hero-stars{{color:var(--a);letter-spacing:2px}}
.hero-btns{{display:flex;gap:12px;flex-wrap:wrap;justify-content:center}}
.btn-primary{{background:linear-gradient(135deg,var(--a),var(--a2));color:#fff;padding:15px 36px;border-radius:10px;font-size:1rem;font-weight:700;text-decoration:none;border:none;cursor:pointer;box-shadow:0 4px 24px color-mix(in srgb,var(--a) 45%,transparent);transition:transform .15s,box-shadow .15s;display:inline-block}}
.btn-primary:hover{{transform:translateY(-2px);box-shadow:0 8px 36px color-mix(in srgb,var(--a) 55%,transparent)}}
.btn-ghost{{color:#fff;padding:15px 36px;border-radius:10px;font-size:1rem;font-weight:600;text-decoration:none;border:2px solid rgba(255,255,255,.3);transition:border-color .2s,background .2s;display:inline-block}}
.btn-ghost:hover{{border-color:rgba(255,255,255,.75);background:rgba(255,255,255,.06)}}

/* TRUST BAR */
.trust-bar{{background:var(--card);border-bottom:1px solid var(--bdr);padding:16px 5%;display:flex;align-items:center;justify-content:center;gap:28px;flex-wrap:wrap}}
.trust-badge{{display:flex;align-items:center;gap:8px;font-size:.8rem;font-weight:600;color:#374151}}
.trust-dot{{width:8px;height:8px;border-radius:50%;background:var(--a)}}

/* LAYOUT */
.wrap{{max-width:1160px;margin:0 auto;padding:0 5%}}

/* SERVICES */
.services-section{{padding:96px 0}}
.svc-grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(210px,1fr));gap:18px;margin-top:52px}}
.svc-card{{background:var(--card);border-radius:var(--r);padding:28px 22px;border:1px solid var(--bdr);transition:transform .2s,box-shadow .2s,border-color .2s}}
.svc-card:hover{{transform:translateY(-5px);box-shadow:0 16px 40px rgba(0,0,0,.09);border-color:var(--a)}}
.svc-icon{{font-size:1.6rem;width:50px;height:50px;border-radius:12px;background:color-mix(in srgb,var(--a) 12%,transparent);display:flex;align-items:center;justify-content:center;margin-bottom:16px}}
.svc-card h3{{font-size:.95rem;font-weight:700;margin-bottom:8px;line-height:1.3}}
.svc-card p{{font-size:.85rem;color:var(--sub);line-height:1.6}}

/* GALLERY */
.gallery-section{{background:var(--p);padding:96px 0}}
.gallery-inner{{max-width:1160px;margin:0 auto;padding:0 5%}}
.gallery-section .section-tag{{color:var(--a)}}
.gallery-section .section-title{{color:#fff}}
.gal-grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin-top:48px}}
.gal-card{{border-radius:var(--r);background-size:cover;background-position:center;aspect-ratio:4/3;transition:transform .25s,box-shadow .25s;overflow:hidden}}
.gal-card:hover{{transform:scale(1.02);box-shadow:0 20px 50px rgba(0,0,0,.3)}}

/* PROCESS */
.process-section{{padding:96px 0;background:var(--p)}}
.process-grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:36px;margin-top:56px}}
.step{{position:relative}}
.step-num{{font-size:2.8rem;font-weight:900;color:rgba(255,255,255,.06);line-height:1;margin-bottom:-4px}}
.step-icon{{font-size:1.5rem;width:50px;height:50px;border-radius:14px;background:color-mix(in srgb,var(--a) 20%,transparent);border:1px solid color-mix(in srgb,var(--a) 35%,transparent);display:flex;align-items:center;justify-content:center;margin-bottom:14px}}
.step h3{{font-size:1rem;font-weight:700;color:#fff;margin-bottom:8px}}
.step p{{font-size:.875rem;color:rgba(255,255,255,.5);line-height:1.65}}
.process-section .section-tag{{color:var(--a)}}
.process-section .section-title{{color:#fff}}

/* TESTIMONIALS */
.testi-section{{padding:96px 0}}
.testi-grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:20px;margin-top:52px}}
.testi-card{{background:var(--card);border-radius:var(--r);padding:30px;border:1px solid var(--bdr);transition:box-shadow .2s}}
.testi-card:hover{{box-shadow:0 10px 36px rgba(0,0,0,.08)}}
.testi-stars{{color:var(--a);letter-spacing:2px;font-size:1.1rem;margin-bottom:14px}}
.testi-text{{font-size:.95rem;line-height:1.75;color:#374151;margin-bottom:22px;font-style:italic}}
.testi-author{{display:flex;align-items:center;gap:12px}}
.testi-avatar{{width:40px;height:40px;border-radius:50%;background:linear-gradient(135deg,var(--a),var(--a2));color:#fff;font-weight:700;font-size:.85rem;display:flex;align-items:center;justify-content:center;flex-shrink:0}}
.testi-author strong{{font-size:.9rem;display:block;margin-bottom:2px}}
.testi-author span{{font-size:.78rem;color:var(--sub)}}

/* CONTACT */
.contact-section{{padding:96px 0;background:linear-gradient(135deg,var(--p),color-mix(in srgb,var(--p) 75%,#000))}}
.contact-grid{{display:grid;grid-template-columns:1fr 1fr;gap:64px;align-items:center}}
.contact-section .section-tag{{color:var(--a)}}
.contact-section .section-title{{color:#fff}}
.contact-lead{{color:rgba(255,255,255,.6);margin:16px 0 28px;font-size:1rem;line-height:1.75}}
.cdetail{{display:flex;align-items:flex-start;gap:14px;background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.1);border-radius:12px;padding:16px 20px;margin-bottom:12px;color:#fff}}
.cdetail-icon{{font-size:1.2rem;flex-shrink:0;margin-top:1px}}
.cdetail-label{{font-size:.7rem;color:rgba(255,255,255,.45);font-weight:600;text-transform:uppercase;letter-spacing:.8px;margin-bottom:3px}}
.cdetail-val{{font-size:.95rem;font-weight:600}}
.contact-btns{{display:flex;gap:12px;flex-wrap:wrap;margin-top:26px}}
.btn-outline{{color:#fff;padding:13px 28px;border-radius:10px;font-size:.9rem;font-weight:600;text-decoration:none;border:2px solid rgba(255,255,255,.3);transition:border-color .2s;display:inline-block}}
.btn-outline:hover{{border-color:rgba(255,255,255,.75)}}
.contact-card{{background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.12);border-radius:24px;padding:48px 36px;text-align:center}}
.card-mono{{width:80px;height:80px;border-radius:20px;background:linear-gradient(135deg,var(--a),var(--a2));color:#fff;font-weight:800;font-size:1.8rem;display:flex;align-items:center;justify-content:center;margin:0 auto 18px}}
.card-name{{color:#fff;font-size:1.3rem;font-weight:700;margin-bottom:6px}}
.card-cat{{color:rgba(255,255,255,.45);font-size:.85rem;margin-bottom:18px}}
.card-desc{{color:rgba(255,255,255,.6);font-size:.875rem;line-height:1.7}}

/* FOOTER */
footer{{background:#0a0a0a;padding:28px 5%;display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:14px}}
.footer-brand{{display:flex;align-items:center;gap:10px}}
.footer-mono{{width:30px;height:30px;border-radius:7px;background:linear-gradient(135deg,var(--a),var(--a2));color:#fff;font-weight:800;font-size:.7rem;display:flex;align-items:center;justify-content:center}}
.footer-name{{color:rgba(255,255,255,.65);font-size:.85rem;font-weight:600}}
.footer-meta{{color:rgba(255,255,255,.3);font-size:.78rem}}

/* TYPOGRAPHY */
.section-tag{{display:inline-block;color:var(--a);font-size:.72rem;font-weight:700;letter-spacing:2.5px;text-transform:uppercase;margin-bottom:12px}}
.section-title{{font-size:clamp(1.9rem,4vw,2.9rem);font-weight:800;letter-spacing:-.5px;line-height:1.12}}
.section-title span{{color:var(--a)}}
.section-lead{{color:var(--sub);font-size:1.05rem;line-height:1.8;margin-top:14px;max-width:560px}}

/* ANIMATIONS */
.reveal{{opacity:0;transform:translateY(30px);transition:opacity .65s ease,transform .65s ease}}
.reveal.visible{{opacity:1;transform:none}}
.reveal:nth-child(2){{transition-delay:.1s}}
.reveal:nth-child(3){{transition-delay:.2s}}

@media(max-width:768px){{
  .contact-grid{{grid-template-columns:1fr}}
  .contact-card{{display:none}}
  .gal-grid{{grid-template-columns:1fr}}
  .nav-cta{{padding:8px 14px;font-size:.8rem}}
  footer{{flex-direction:column;text-align:center}}
}}
</style>
</head>
<body>

<nav class="nav" id="nav">
  <a href="#" class="nav-logo">
    <div class="monogram">{hl.escape(mono)}</div>
    <div class="nav-text">
      <div class="nav-name">{hl.escape(name)}</div>
      <span class="nav-cat">{hl.escape(cat_label)} · Amsterdam</span>
    </div>
  </a>
  <a href="#contact" class="nav-cta">Free Quote →</a>
</nav>

<section class="hero">
  <div class="hero-noise"></div>
  <div class="hero-content">
    <div class="hero-pill"><span class="pill-dot"></span>{hl.escape(icon)} {hl.escape(cat_label)} · Amsterdam</div>
    <h1>{t1}<br><em>{t2}</em></h1>
    <p class="hero-sub">{hl.escape(hero_desc)}</p>
    {rating_html}
    <div class="hero-btns">
      {phone_btn}
      <a href="#services" class="btn-ghost">See Our Services</a>
    </div>
  </div>
</section>

<div class="trust-bar">{tbs}</div>

<div class="services-section">
  <div class="wrap reveal">
    <p class="section-tag">What We Do</p>
    <h2 class="section-title">Our <span>Services</span></h2>
    <p class="section-lead">{hl.escape(hero_desc)}</p>
    <div class="svc-grid" id="services">{svcs}</div>
  </div>
</div>

{gallery_html}

<div class="process-section">
  <div class="wrap reveal">
    <p class="section-tag">How It Works</p>
    <h2 class="section-title">Simple. <span>Straightforward.</span> Sorted.</h2>
    <div class="process-grid">{procs}</div>
  </div>
</div>

<div class="testi-section">
  <div class="wrap reveal">
    <p class="section-tag">Client Reviews</p>
    <h2 class="section-title">Trusted by <span>Amsterdam</span></h2>
    <p class="section-lead">Don't just take our word for it — here's what our customers say.</p>
    <div class="testi-grid">{ts}</div>
  </div>
</div>

<div class="contact-section" id="contact">
  <div class="wrap">
    <div class="contact-grid">
      <div class="reveal">
        <p class="section-tag">Get in Touch</p>
        <h2 class="section-title">Ready to Get<br><span>Started?</span></h2>
        <p class="contact-lead">Contact us today for a free, no-obligation quote. We typically respond within a few hours.</p>
        {phone_detail}{addr_detail}
        <div class="contact-btns">{phone_btn}{maps_btn}</div>
      </div>
      <div class="contact-card reveal">
        <div class="card-mono">{hl.escape(mono)}</div>
        <div class="card-name">{hl.escape(name)}</div>
        <div class="card-cat">{hl.escape(cat_label)} · {hl.escape(city)}</div>
        <div class="card-desc">{hl.escape(hero_desc)}</div>
      </div>
    </div>
  </div>
</div>

<footer>
  <div class="footer-brand">
    <div class="footer-mono">{hl.escape(mono)}</div>
    <span class="footer-name">{hl.escape(name)}</span>
  </div>
  <span class="footer-meta">{hl.escape(cat_label)} · {hl.escape(city)}, Netherlands · © 2025</span>
</footer>

<script>
const nav=document.getElementById('nav');
window.addEventListener('scroll',()=>nav.classList.toggle('scrolled',scrollY>20),{{passive:true}});
const io=new IntersectionObserver(es=>es.forEach(e=>{{if(e.isIntersecting){{e.target.classList.add('visible');io.unobserve(e.target)}}}}),{{threshold:.1}});
document.querySelectorAll('.reveal').forEach(el=>io.observe(el));
</script>
</body>
</html>"""


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs(IMG_DIR, exist_ok=True)

    # Pre-download images for every category
    print("Downloading category images (one set per category)...")
    img_cache = {}  # cat_slug → paths dict

    all_cats = list(CATEGORY_CONFIG.keys()) + [None]
    for cat in all_cats:
        cfg = CATEGORY_CONFIG[cat] if cat else DEFAULT_CONFIG
        cs = cat_slug(cat) if cat else "default"
        print(f"  {cs}...", end=" ", flush=True)
        paths = fetch_category_images(cs, cfg, IMG_DIR)
        img_cache[cs] = paths or {}
        print("✓" if paths else "✗ (using gradient fallback)")

    # Generate HTML
    print("\nGenerating HTML files...")
    for f in os.listdir(OUTPUT_DIR):
        if f.endswith('.html'):
            os.remove(os.path.join(OUTPUT_DIR, f))

    generated = skipped = 0
    seen_slugs = {}

    with open(CSV_PATH, newline='', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            cats = [row.get(f"categories/{i}", "").strip() for i in range(9)]
            cats = [c for c in cats if c]
            matched_cat, _ = get_config(cats)
            cs = cat_slug(matched_cat) if matched_cat else "default"
            img_paths = img_cache.get(cs, {})

            page = generate_html(row, img_paths)
            if page is None:
                skipped += 1
                continue

            name = (row.get("title") or row.get("﻿title") or "").strip()
            base = slugify(name)
            if not base:
                skipped += 1
                continue

            n = seen_slugs.get(base, 0)
            seen_slugs[base] = n + 1
            slug = base if n == 0 else f"{base}-{n}"

            with open(os.path.join(OUTPUT_DIR, f"{slug}.html"), "w", encoding="utf-8") as out:
                out.write(page)
            generated += 1

    print(f"\nDone. Generated: {generated} | Skipped: {skipped}")
    print(f"Output: {os.path.abspath(OUTPUT_DIR)}/")


if __name__ == "__main__":
    main()
