#!/usr/bin/env python3
"""
Website generator — v4: embedded SVG illustrations, no external images.
Purpose: outreach / lead generation to sell web design services.
"""

import csv, os, re, html as hl

OUTPUT_DIR = "websites"
CSV_PATH   = "/root/.claude/uploads/b553d4c3-fa71-535d-b226-64e15b822f4e/e9e48877-dataset_amsterdam1_20260614_171131429.csv"

SKIP_CATEGORIES = {
    "Park","Garden","Lake","Community garden","Area","Hiking area",
    "House","Vacation rental","Shipyard",
}

CATEGORY_CONFIG = {
    "Bricklayer": {
        "primary":"#0f172a","accent":"#f97316","accent2":"#fb923c",
        "icon":"🧱",
        "tagline":"Building Amsterdam's Future,\nOne Brick at a Time",
        "hero_desc":"Expert bricklaying and facade restoration. Trusted by homeowners and developers across Amsterdam for craftsmanship that stands the test of time.",
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
        "services":[("🔌","New Installations","Complete electrical fit-outs for new builds and refurbs."),("🔄","Rewiring","Full and partial rewiring for older properties."),("🏠","Smart Home Systems","Control your home with the latest smart technology."),("🚨","Emergency Lighting","Safety-compliant emergency lighting systems."),("📋","Electrical Testing","Thorough testing and certification of all installations.")],
        "testimonials":[("Wim B.","Noord","Rewired our entire house with zero fuss. Brilliant team."),("Sandra K.","Zuid","Smart home system is incredible — these guys know their stuff."),("Paul V.","West","Professional, punctual and great value. Highly recommended.")],
        "process":[("📞","Neem Contact Op","Call or email to discuss your electrical needs."),("📐","Site Survey","We survey the site and provide a detailed, fixed quote."),("✅","Certified Completion","All work is tested, certified and handed over with full documentation.")],
        "trust":["NEN 1010 Compliant","All Work Certified","Clean & Tidy","Local Specialists"],
    },
    "Bicycle repair shop": {
        "primary":"#14532d","accent":"#22c55e","accent2":"#4ade80",
        "icon":"🚲",
        "tagline":"Get Back on the Road —\nFast",
        "hero_desc":"Expert bicycle repairs, servicing and upgrades in the heart of Amsterdam. We keep Amsterdam cycling — whatever the bike, whatever the problem.",
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
    "services":[("✅","Professional Services","Expert service delivered to the highest standard."),("🏆","Quality Guaranteed","We stand behind every job we do."),("📍","Local Expertise","Deep knowledge of Amsterdam and its unique needs."),("💰","Competitive Rates","Fair, transparent pricing with no hidden costs."),("💬","Free Consultation","Talk to us first — no obligation, no pressure.")],
    "testimonials":[("Client","Amsterdam","Excellent service from start to finish. Highly recommended."),("Customer","Noord","Professional, punctual and great value. Would use again."),("Client","Zuid","Friendly, skilled and reliable. Very happy with the result.")],
    "process":[("📞","Neem Contact Op","Contact us to discuss your needs — we respond fast."),("📋","Receive Your Quote","A clear, competitive quote with no hidden extras."),("✅","Job Done Right","We deliver quality work and ensure you're 100% satisfied.")],
    "trust":["Fully Insured","Free Consultation","Satisfaction Guaranteed","Amsterdam Based"],
}


# ── SVG Illustrations ─────────────────────────────────────────────────────────

CATEGORY_SVG_GROUP = {
    "Bricklayer":"construction","Masonry contractor":"construction","Contractor":"construction",
    "General contractor":"construction","Construction company":"construction",
    "Home builder":"construction","Custom home builder":"construction",
    "Carpenter":"carpentry","Plumber":"plumbing","Painter":"painting",
    "Electrician":"electrical","Electrical installation service":"electrical",
    "Bicycle repair shop":"bicycle","Bicycle Shop":"bicycle",
    "Photographer":"photography","Photography studio":"photography",
    "Commercial photographer":"photography","Photography service":"photography",
    "Yoga studio":"yoga","Dog trainer":"pets","Pet trainer":"pets",
    "Tutoring service":"education","Private tutor":"education","Education center":"education",
    "Mover":"transport","Moving and storage service":"transport",
    "Trucking company":"transport","Courier service":"transport","Delivery service":"transport",
    "Shipping company":"global","Import export company":"global",
    "House cleaning service":"cleaning","Cleaning service":"cleaning",
    "Roofing contractor":"roofing","Plasterer":"plastering","Stucco contractor":"plastering",
    "Video production service":"video","Art studio":"art","Website designer":"web",
    "Landscaper":"landscaping","Garden building supplier":"landscaping",
    "Handyman/Handywoman/Handyperson":"tools",
}

SVG_ILLUSTRATIONS = {
"construction": '''<svg viewBox="0 0 400 300" xmlns="http://www.w3.org/2000/svg" width="100%" height="100%">
  <rect x="40" y="140" width="80" height="100" fill="rgba(255,255,255,0.12)" rx="4"/>
  <rect x="55" y="155" width="20" height="25" fill="ACCENT" rx="2" opacity="0.8"/>
  <rect x="85" y="155" width="20" height="25" fill="ACCENT" rx="2" opacity="0.6"/>
  <rect x="55" y="195" width="20" height="25" fill="ACCENT" rx="2" opacity="0.5"/>
  <rect x="85" y="195" width="20" height="25" fill="ACCENT" rx="2" opacity="0.7"/>
  <rect x="150" y="80" width="120" height="160" fill="rgba(255,255,255,0.15)" rx="6"/>
  <rect x="165" y="100" width="25" height="30" fill="ACCENT" rx="3" opacity="0.9"/>
  <rect x="200" y="100" width="25" height="30" fill="ACCENT" rx="3" opacity="0.7"/>
  <rect x="235" y="100" width="20" height="30" fill="ACCENT" rx="3" opacity="0.8"/>
  <rect x="165" y="145" width="25" height="30" fill="ACCENT" rx="3" opacity="0.6"/>
  <rect x="200" y="145" width="25" height="30" fill="ACCENT" rx="3" opacity="0.9"/>
  <rect x="185" y="195" width="50" height="45" fill="rgba(255,255,255,0.2)" rx="3"/>
  <polygon points="150,80 210,30 270,80" fill="ACCENT" opacity="0.7"/>
  <rect x="290" y="160" width="70" height="80" fill="rgba(255,255,255,0.1)" rx="4"/>
  <rect x="302" y="175" width="18" height="20" fill="ACCENT" rx="2" opacity="0.7"/>
  <rect x="327" y="175" width="18" height="20" fill="ACCENT" rx="2" opacity="0.5"/>
  <line x1="330" y1="240" x2="330" y2="60" stroke="rgba(255,255,255,0.3)" stroke-width="4"/>
  <line x1="330" y1="60" x2="380" y2="60" stroke="rgba(255,255,255,0.3)" stroke-width="4"/>
  <line x1="370" y1="60" x2="370" y2="100" stroke="rgba(255,255,255,0.2)" stroke-width="2"/>
  <rect x="360" y="100" width="20" height="15" fill="ACCENT" rx="2" opacity="0.6"/>
</svg>''',
"carpentry": '''<svg viewBox="0 0 400 300" xmlns="http://www.w3.org/2000/svg" width="100%" height="100%">
  <rect x="30" y="60" width="220" height="35" fill="rgba(255,255,255,0.12)" rx="4"/>
  <rect x="30" y="105" width="220" height="35" fill="rgba(255,255,255,0.09)" rx="4"/>
  <rect x="30" y="150" width="220" height="35" fill="rgba(255,255,255,0.12)" rx="4"/>
  <rect x="30" y="195" width="220" height="35" fill="rgba(255,255,255,0.09)" rx="4"/>
  <line x1="60" y1="60" x2="60" y2="95" stroke="rgba(255,255,255,0.06)" stroke-width="1.5"/>
  <line x1="100" y1="60" x2="100" y2="95" stroke="rgba(255,255,255,0.06)" stroke-width="1.5"/>
  <line x1="150" y1="105" x2="150" y2="140" stroke="rgba(255,255,255,0.06)" stroke-width="1.5"/>
  <rect x="290" y="80" width="80" height="28" fill="ACCENT" rx="6" opacity="0.85"/>
  <rect x="340" y="55" width="18" height="80" fill="rgba(255,255,255,0.2)" rx="4"/>
  <rect x="280" y="170" width="100" height="22" fill="rgba(255,255,255,0.15)" rx="3"/>
  <line x1="295" y1="170" x2="295" y2="185" stroke="ACCENT" stroke-width="2" opacity="0.8"/>
  <line x1="325" y1="170" x2="325" y2="185" stroke="ACCENT" stroke-width="2" opacity="0.8"/>
  <line x1="355" y1="170" x2="355" y2="185" stroke="ACCENT" stroke-width="2" opacity="0.8"/>
  <circle cx="55" cy="77" r="4" fill="ACCENT" opacity="0.6"/>
  <circle cx="55" cy="122" r="4" fill="ACCENT" opacity="0.4"/>
</svg>''',
"plumbing": '''<svg viewBox="0 0 400 300" xmlns="http://www.w3.org/2000/svg" width="100%" height="100%">
  <rect x="80" y="40" width="28" height="220" fill="rgba(255,255,255,0.12)" rx="6"/>
  <rect x="200" y="80" width="28" height="180" fill="rgba(255,255,255,0.1)" rx="6"/>
  <rect x="300" y="40" width="28" height="120" fill="rgba(255,255,255,0.12)" rx="6"/>
  <rect x="80" y="100" width="150" height="28" fill="rgba(255,255,255,0.15)" rx="6"/>
  <rect x="200" y="180" width="130" height="28" fill="rgba(255,255,255,0.12)" rx="6"/>
  <circle cx="94" cy="114" r="18" fill="ACCENT" opacity="0.8"/>
  <circle cx="214" cy="114" r="18" fill="ACCENT" opacity="0.6"/>
  <circle cx="214" cy="194" r="18" fill="ACCENT" opacity="0.7"/>
  <circle cx="314" cy="194" r="16" fill="ACCENT" opacity="0.5"/>
  <circle cx="300" cy="80" r="22" fill="none" stroke="ACCENT" stroke-width="4" opacity="0.7"/>
  <line x1="278" y1="80" x2="322" y2="80" stroke="ACCENT" stroke-width="4" opacity="0.7"/>
  <line x1="300" y1="58" x2="300" y2="102" stroke="ACCENT" stroke-width="4" opacity="0.7"/>
  <ellipse cx="150" cy="260" rx="8" ry="12" fill="ACCENT" opacity="0.6"/>
  <ellipse cx="220" cy="270" rx="6" ry="9" fill="ACCENT" opacity="0.4"/>
  <ellipse cx="340" cy="255" rx="7" ry="10" fill="ACCENT" opacity="0.5"/>
</svg>''',
"painting": '''<svg viewBox="0 0 400 300" xmlns="http://www.w3.org/2000/svg" width="100%" height="100%">
  <rect x="60" y="80" width="140" height="45" fill="ACCENT" rx="8" opacity="0.3"/>
  <rect x="60" y="80" width="140" height="45" fill="rgba(255,255,255,0.1)" rx="8"/>
  <rect x="175" y="60" width="12" height="85" fill="rgba(255,255,255,0.2)" rx="4"/>
  <rect x="175" y="55" width="60" height="12" fill="rgba(255,255,255,0.2)" rx="4"/>
  <rect x="40" y="165" width="50" height="60" fill="ACCENT" rx="6" opacity="0.9"/>
  <rect x="100" y="165" width="50" height="60" fill="rgba(255,255,255,0.3)" rx="6"/>
  <rect x="160" y="165" width="50" height="60" fill="ACCENT" rx="6" opacity="0.5"/>
  <rect x="220" y="165" width="50" height="60" fill="rgba(255,255,255,0.15)" rx="6"/>
  <circle cx="290" cy="80" r="18" fill="ACCENT" opacity="0.7"/>
  <circle cx="320" cy="100" r="10" fill="ACCENT" opacity="0.5"/>
  <circle cx="270" cy="110" r="7" fill="ACCENT" opacity="0.4"/>
  <circle cx="340" cy="65" r="5" fill="ACCENT" opacity="0.6"/>
  <circle cx="305" cy="130" r="12" fill="ACCENT" opacity="0.3"/>
  <rect x="290" y="180" width="70" height="70" fill="rgba(255,255,255,0.1)" rx="4"/>
  <rect x="290" y="180" width="70" height="20" fill="ACCENT" rx="4" opacity="0.5"/>
</svg>''',
"electrical": '''<svg viewBox="0 0 400 300" xmlns="http://www.w3.org/2000/svg" width="100%" height="100%">
  <polygon points="220,30 170,155 205,155 175,270 280,120 238,120 280,30" fill="ACCENT" opacity="0.85"/>
  <polygon points="220,30 170,155 205,155 175,270 280,120 238,120 280,30" fill="none" stroke="ACCENT" stroke-width="2" opacity="0.25"/>
  <rect x="30" y="160" width="130" height="110" fill="rgba(255,255,255,0.06)" rx="8"/>
  <line x1="50" y1="185" x2="130" y2="185" stroke="ACCENT" stroke-width="2" opacity="0.4"/>
  <line x1="50" y1="210" x2="90" y2="210" stroke="ACCENT" stroke-width="2" opacity="0.4"/>
  <line x1="90" y1="210" x2="90" y2="235" stroke="ACCENT" stroke-width="2" opacity="0.4"/>
  <line x1="90" y1="235" x2="140" y2="235" stroke="ACCENT" stroke-width="2" opacity="0.4"/>
  <line x1="130" y1="185" x2="130" y2="210" stroke="ACCENT" stroke-width="2" opacity="0.4"/>
  <circle cx="90" cy="185" r="5" fill="ACCENT" opacity="0.7"/>
  <circle cx="130" cy="185" r="5" fill="ACCENT" opacity="0.7"/>
  <circle cx="90" cy="235" r="5" fill="ACCENT" opacity="0.7"/>
</svg>''',
"bicycle": '''<svg viewBox="0 0 400 300" xmlns="http://www.w3.org/2000/svg" width="100%" height="100%">
  <circle cx="120" cy="190" r="80" fill="none" stroke="rgba(255,255,255,0.15)" stroke-width="14"/>
  <circle cx="120" cy="190" r="80" fill="none" stroke="ACCENT" stroke-width="3" opacity="0.6"/>
  <line x1="120" y1="110" x2="120" y2="270" stroke="rgba(255,255,255,0.2)" stroke-width="2"/>
  <line x1="40" y1="190" x2="200" y2="190" stroke="rgba(255,255,255,0.2)" stroke-width="2"/>
  <line x1="63" y1="133" x2="177" y2="247" stroke="rgba(255,255,255,0.15)" stroke-width="2"/>
  <line x1="63" y1="247" x2="177" y2="133" stroke="rgba(255,255,255,0.15)" stroke-width="2"/>
  <circle cx="120" cy="190" r="12" fill="ACCENT" opacity="0.8"/>
  <circle cx="300" cy="190" r="80" fill="none" stroke="rgba(255,255,255,0.15)" stroke-width="14"/>
  <circle cx="300" cy="190" r="80" fill="none" stroke="ACCENT" stroke-width="3" opacity="0.6"/>
  <line x1="300" y1="110" x2="300" y2="270" stroke="rgba(255,255,255,0.2)" stroke-width="2"/>
  <line x1="220" y1="190" x2="380" y2="190" stroke="rgba(255,255,255,0.2)" stroke-width="2"/>
  <circle cx="300" cy="190" r="12" fill="ACCENT" opacity="0.8"/>
  <line x1="120" y1="190" x2="200" y2="120" stroke="rgba(255,255,255,0.3)" stroke-width="6"/>
  <line x1="200" y1="120" x2="300" y2="190" stroke="rgba(255,255,255,0.3)" stroke-width="6"/>
  <line x1="200" y1="120" x2="220" y2="190" stroke="rgba(255,255,255,0.25)" stroke-width="5"/>
  <line x1="120" y1="190" x2="220" y2="190" stroke="rgba(255,255,255,0.2)" stroke-width="5"/>
  <line x1="200" y1="120" x2="190" y2="85" stroke="rgba(255,255,255,0.25)" stroke-width="5"/>
  <rect x="170" y="75" width="40" height="12" fill="rgba(255,255,255,0.3)" rx="6"/>
  <line x1="280" y1="120" x2="290" y2="85" stroke="rgba(255,255,255,0.25)" stroke-width="5"/>
  <line x1="270" y1="78" x2="310" y2="72" stroke="ACCENT" stroke-width="6" opacity="0.7" stroke-linecap="round"/>
</svg>''',
"photography": '''<svg viewBox="0 0 400 300" xmlns="http://www.w3.org/2000/svg" width="100%" height="100%">
  <rect x="60" y="100" width="280" height="170" fill="rgba(255,255,255,0.12)" rx="16"/>
  <rect x="130" y="70" width="100" height="40" fill="rgba(255,255,255,0.12)" rx="10"/>
  <circle cx="145" cy="70" r="14" fill="ACCENT" opacity="0.8"/>
  <circle cx="200" cy="188" r="72" fill="rgba(0,0,0,0.25)"/>
  <circle cx="200" cy="188" r="72" fill="none" stroke="rgba(255,255,255,0.15)" stroke-width="10"/>
  <circle cx="200" cy="188" r="52" fill="rgba(0,0,0,0.3)"/>
  <circle cx="200" cy="188" r="52" fill="none" stroke="ACCENT" stroke-width="3" opacity="0.6"/>
  <circle cx="200" cy="188" r="32" fill="rgba(0,0,0,0.4)"/>
  <circle cx="185" cy="174" r="10" fill="rgba(255,255,255,0.12)"/>
  <rect x="310" y="110" width="24" height="16" fill="ACCENT" rx="4" opacity="0.7"/>
  <circle cx="100" cy="118" r="16" fill="rgba(255,255,255,0.1)" stroke="rgba(255,255,255,0.2)" stroke-width="2"/>
</svg>''',
"yoga": '''<svg viewBox="0 0 400 300" xmlns="http://www.w3.org/2000/svg" width="100%" height="100%">
  <ellipse cx="200" cy="200" rx="80" ry="40" fill="ACCENT" opacity="0.15" transform="rotate(-45 200 200)"/>
  <ellipse cx="200" cy="200" rx="80" ry="40" fill="ACCENT" opacity="0.15" transform="rotate(45 200 200)"/>
  <ellipse cx="200" cy="200" rx="80" ry="40" fill="ACCENT" opacity="0.15"/>
  <ellipse cx="200" cy="200" rx="80" ry="40" fill="ACCENT" opacity="0.15" transform="rotate(90 200 200)"/>
  <ellipse cx="200" cy="200" rx="55" ry="28" fill="ACCENT" opacity="0.25" transform="rotate(-45 200 200)"/>
  <ellipse cx="200" cy="200" rx="55" ry="28" fill="ACCENT" opacity="0.25" transform="rotate(45 200 200)"/>
  <ellipse cx="200" cy="200" rx="55" ry="28" fill="ACCENT" opacity="0.25"/>
  <ellipse cx="200" cy="200" rx="55" ry="28" fill="ACCENT" opacity="0.25" transform="rotate(90 200 200)"/>
  <circle cx="200" cy="200" r="30" fill="ACCENT" opacity="0.5"/>
  <circle cx="200" cy="200" r="18" fill="ACCENT" opacity="0.8"/>
  <circle cx="200" cy="200" r="100" fill="none" stroke="ACCENT" stroke-width="1" opacity="0.15"/>
  <circle cx="200" cy="90" r="22" fill="rgba(255,255,255,0.2)"/>
  <path d="M160 160 Q200 130 240 160 Q220 200 200 210 Q180 200 160 160Z" fill="rgba(255,255,255,0.15)"/>
  <line x1="200" y1="112" x2="200" y2="155" stroke="rgba(255,255,255,0.2)" stroke-width="6"/>
</svg>''',
"pets": '''<svg viewBox="0 0 400 300" xmlns="http://www.w3.org/2000/svg" width="100%" height="100%">
  <circle cx="200" cy="150" r="85" fill="rgba(255,255,255,0.12)"/>
  <ellipse cx="140" cy="90" rx="35" ry="55" fill="rgba(255,255,255,0.15)" transform="rotate(-15 140 90)"/>
  <ellipse cx="260" cy="90" rx="35" ry="55" fill="rgba(255,255,255,0.15)" transform="rotate(15 260 90)"/>
  <ellipse cx="140" cy="92" rx="22" ry="40" fill="ACCENT" opacity="0.3" transform="rotate(-15 140 92)"/>
  <ellipse cx="260" cy="92" rx="22" ry="40" fill="ACCENT" opacity="0.3" transform="rotate(15 260 92)"/>
  <circle cx="170" cy="135" r="18" fill="rgba(255,255,255,0.3)"/>
  <circle cx="230" cy="135" r="18" fill="rgba(255,255,255,0.3)"/>
  <circle cx="172" cy="137" r="11" fill="rgba(0,0,0,0.5)"/>
  <circle cx="232" cy="137" r="11" fill="rgba(0,0,0,0.5)"/>
  <circle cx="168" cy="132" r="4" fill="rgba(255,255,255,0.6)"/>
  <circle cx="228" cy="132" r="4" fill="rgba(255,255,255,0.6)"/>
  <ellipse cx="200" cy="170" rx="35" ry="25" fill="rgba(255,255,255,0.18)"/>
  <ellipse cx="200" cy="162" rx="18" ry="12" fill="ACCENT" opacity="0.6"/>
  <path d="M185 175 Q200 188 215 175" fill="none" stroke="rgba(255,255,255,0.3)" stroke-width="3"/>
  <circle cx="60" cy="250" r="12" fill="ACCENT" opacity="0.4"/>
  <circle cx="48" cy="234" r="7" fill="ACCENT" opacity="0.3"/>
  <circle cx="62" cy="230" r="7" fill="ACCENT" opacity="0.3"/>
  <circle cx="76" cy="234" r="7" fill="ACCENT" opacity="0.3"/>
  <circle cx="320" cy="255" r="12" fill="ACCENT" opacity="0.4"/>
  <circle cx="308" cy="239" r="7" fill="ACCENT" opacity="0.3"/>
  <circle cx="336" cy="239" r="7" fill="ACCENT" opacity="0.3"/>
</svg>''',
"education": '''<svg viewBox="0 0 400 300" xmlns="http://www.w3.org/2000/svg" width="100%" height="100%">
  <rect x="50" y="200" width="180" height="30" fill="ACCENT" rx="4" opacity="0.8"/>
  <rect x="50" y="164" width="180" height="30" fill="rgba(255,255,255,0.2)" rx="4"/>
  <rect x="50" y="128" width="180" height="30" fill="ACCENT" rx="4" opacity="0.5"/>
  <rect x="50" y="92" width="180" height="30" fill="rgba(255,255,255,0.15)" rx="4"/>
  <rect x="50" y="200" width="12" height="30" fill="rgba(0,0,0,0.2)" rx="2"/>
  <rect x="50" y="164" width="12" height="30" fill="rgba(0,0,0,0.15)" rx="2"/>
  <rect x="50" y="128" width="12" height="30" fill="rgba(0,0,0,0.2)" rx="2"/>
  <rect x="50" y="92" width="12" height="30" fill="rgba(0,0,0,0.15)" rx="2"/>
  <rect x="235" y="155" width="110" height="18" fill="rgba(255,255,255,0.2)" rx="3"/>
  <polygon points="290,100 235,155 345,155" fill="ACCENT" opacity="0.7"/>
  <line x1="345" y1="155" x2="345" y2="195" stroke="rgba(255,255,255,0.3)" stroke-width="3"/>
  <circle cx="345" cy="200" r="8" fill="ACCENT" opacity="0.7"/>
  <rect x="55" y="50" width="12" height="60" fill="rgba(255,255,255,0.2)" rx="4"/>
  <polygon points="55,110 67,110 61,128" fill="ACCENT" opacity="0.7"/>
</svg>''',
"transport": '''<svg viewBox="0 0 400 300" xmlns="http://www.w3.org/2000/svg" width="100%" height="100%">
  <rect x="30" y="140" width="280" height="110" fill="rgba(255,255,255,0.15)" rx="10"/>
  <rect x="250" y="110" width="120" height="140" fill="rgba(255,255,255,0.12)" rx="10"/>
  <rect x="260" y="120" width="100" height="55" fill="ACCENT" rx="6" opacity="0.25"/>
  <line x1="250" y1="140" x2="250" y2="250" stroke="rgba(255,255,255,0.15)" stroke-width="2"/>
  <rect x="60" y="160" width="160" height="60" fill="rgba(255,255,255,0.08)" rx="6"/>
  <rect x="60" y="160" width="6" height="60" fill="ACCENT" rx="3" opacity="0.7"/>
  <circle cx="100" cy="255" r="35" fill="rgba(0,0,0,0.4)"/>
  <circle cx="100" cy="255" r="35" fill="none" stroke="rgba(255,255,255,0.2)" stroke-width="6"/>
  <circle cx="100" cy="255" r="15" fill="ACCENT" opacity="0.5"/>
  <circle cx="310" cy="255" r="35" fill="rgba(0,0,0,0.4)"/>
  <circle cx="310" cy="255" r="35" fill="none" stroke="rgba(255,255,255,0.2)" stroke-width="6"/>
  <circle cx="310" cy="255" r="15" fill="ACCENT" opacity="0.5"/>
  <line x1="0" y1="180" x2="30" y2="180" stroke="ACCENT" stroke-width="3" opacity="0.5"/>
  <line x1="0" y1="200" x2="30" y2="200" stroke="ACCENT" stroke-width="2" opacity="0.3"/>
  <line x1="0" y1="215" x2="25" y2="215" stroke="ACCENT" stroke-width="2" opacity="0.25"/>
</svg>''',
"global": '''<svg viewBox="0 0 400 300" xmlns="http://www.w3.org/2000/svg" width="100%" height="100%">
  <circle cx="200" cy="150" r="120" fill="rgba(255,255,255,0.06)" stroke="rgba(255,255,255,0.2)" stroke-width="3"/>
  <ellipse cx="200" cy="150" rx="120" ry="30" fill="none" stroke="rgba(255,255,255,0.1)" stroke-width="1.5"/>
  <ellipse cx="200" cy="150" rx="120" ry="65" fill="none" stroke="rgba(255,255,255,0.1)" stroke-width="1.5"/>
  <ellipse cx="200" cy="150" rx="40" ry="120" fill="none" stroke="rgba(255,255,255,0.1)" stroke-width="1.5"/>
  <ellipse cx="200" cy="150" rx="80" ry="120" fill="none" stroke="rgba(255,255,255,0.1)" stroke-width="1.5"/>
  <line x1="80" y1="150" x2="320" y2="150" stroke="ACCENT" stroke-width="2" opacity="0.5"/>
  <ellipse cx="170" cy="120" rx="35" ry="25" fill="ACCENT" opacity="0.25"/>
  <ellipse cx="240" cy="140" rx="28" ry="20" fill="ACCENT" opacity="0.2"/>
  <circle cx="140" cy="105" r="6" fill="ACCENT" opacity="0.8"/>
  <circle cx="265" cy="130" r="6" fill="ACCENT" opacity="0.8"/>
  <circle cx="200" cy="185" r="6" fill="ACCENT" opacity="0.8"/>
  <line x1="140" y1="105" x2="265" y2="130" stroke="ACCENT" stroke-width="1.5" stroke-dasharray="4,3" opacity="0.5"/>
  <line x1="265" y1="130" x2="200" y2="185" stroke="ACCENT" stroke-width="1.5" stroke-dasharray="4,3" opacity="0.5"/>
</svg>''',
"cleaning": '''<svg viewBox="0 0 400 300" xmlns="http://www.w3.org/2000/svg" width="100%" height="100%">
  <circle cx="80" cy="200" r="50" fill="none" stroke="rgba(255,255,255,0.15)" stroke-width="3"/>
  <circle cx="280" cy="200" r="55" fill="none" stroke="rgba(255,255,255,0.15)" stroke-width="3"/>
  <circle cx="280" cy="200" r="35" fill="rgba(255,255,255,0.06)"/>
  <circle cx="150" cy="150" r="25" fill="none" stroke="rgba(255,255,255,0.1)" stroke-width="2"/>
  <circle cx="340" cy="140" r="30" fill="none" stroke="rgba(255,255,255,0.1)" stroke-width="2"/>
  <polygon points="200,50 205,65 220,65 208,73 213,88 200,80 187,88 192,73 180,65 195,65" fill="ACCENT" opacity="0.8"/>
  <polyline points="50,80 65,95 90,65" fill="none" stroke="ACCENT" stroke-width="5" stroke-linecap="round" stroke-linejoin="round" opacity="0.7"/>
  <polyline points="300,80 315,95 340,65" fill="none" stroke="ACCENT" stroke-width="5" stroke-linecap="round" stroke-linejoin="round" opacity="0.6"/>
  <polyline points="170,120 185,135 210,105" fill="none" stroke="ACCENT" stroke-width="4" stroke-linecap="round" stroke-linejoin="round" opacity="0.5"/>
</svg>''',
"roofing": '''<svg viewBox="0 0 400 300" xmlns="http://www.w3.org/2000/svg" width="100%" height="100%">
  <rect x="80" y="170" width="240" height="110" fill="rgba(255,255,255,0.12)" rx="4"/>
  <rect x="178" y="220" width="45" height="60" fill="rgba(255,255,255,0.15)" rx="4"/>
  <circle cx="217" cy="252" r="4" fill="ACCENT" opacity="0.7"/>
  <rect x="100" y="195" width="45" height="38" fill="ACCENT" rx="3" opacity="0.3"/>
  <line x1="122" y1="195" x2="122" y2="233" stroke="rgba(255,255,255,0.2)" stroke-width="1.5"/>
  <line x1="100" y1="214" x2="145" y2="214" stroke="rgba(255,255,255,0.2)" stroke-width="1.5"/>
  <rect x="255" y="195" width="45" height="38" fill="ACCENT" rx="3" opacity="0.3"/>
  <line x1="277" y1="195" x2="277" y2="233" stroke="rgba(255,255,255,0.2)" stroke-width="1.5"/>
  <line x1="255" y1="214" x2="300" y2="214" stroke="rgba(255,255,255,0.2)" stroke-width="1.5"/>
  <polygon points="60,170 200,50 340,170" fill="ACCENT" opacity="0.6"/>
  <path d="M90 165 Q105 155 120 165" fill="none" stroke="rgba(255,255,255,0.2)" stroke-width="2"/>
  <path d="M120 165 Q135 155 150 165" fill="none" stroke="rgba(255,255,255,0.2)" stroke-width="2"/>
  <path d="M150 165 Q165 155 180 165" fill="none" stroke="rgba(255,255,255,0.2)" stroke-width="2"/>
  <path d="M180 165 Q195 155 210 165" fill="none" stroke="rgba(255,255,255,0.2)" stroke-width="2"/>
  <path d="M210 165 Q225 155 240 165" fill="none" stroke="rgba(255,255,255,0.2)" stroke-width="2"/>
  <path d="M270 165 Q285 155 300 165" fill="none" stroke="rgba(255,255,255,0.2)" stroke-width="2"/>
  <rect x="265" y="85" width="30" height="70" fill="rgba(255,255,255,0.2)" rx="2"/>
  <rect x="260" y="80" width="40" height="12" fill="rgba(255,255,255,0.25)" rx="3"/>
</svg>''',
"plastering": '''<svg viewBox="0 0 400 300" xmlns="http://www.w3.org/2000/svg" width="100%" height="100%">
  <rect x="30" y="40" width="160" height="240" fill="rgba(255,255,255,0.08)" rx="4"/>
  <rect x="205" y="40" width="80" height="115" fill="rgba(255,255,255,0.05)" rx="4"/>
  <rect x="205" y="165" width="80" height="115" fill="rgba(255,255,255,0.08)" rx="4"/>
  <rect x="297" y="40" width="73" height="240" fill="ACCENT" rx="4" opacity="0.15"/>
  <rect x="30" y="40" width="160" height="240" fill="none" stroke="rgba(255,255,255,0.15)" stroke-width="2" rx="4"/>
  <rect x="297" y="40" width="73" height="240" fill="none" stroke="ACCENT" stroke-width="2" rx="4" opacity="0.4"/>
  <rect x="110" y="90" width="120" height="40" fill="rgba(255,255,255,0.2)" rx="8" transform="rotate(-35 170 110)"/>
  <rect x="200" y="50" width="10" height="70" fill="rgba(255,255,255,0.15)" rx="3" transform="rotate(-35 205 85)"/>
  <polyline points="35,270 100,270 100,60 165,60" fill="none" stroke="ACCENT" stroke-width="3" opacity="0.5" stroke-linecap="round" stroke-linejoin="round"/>
</svg>''',
"video": '''<svg viewBox="0 0 400 300" xmlns="http://www.w3.org/2000/svg" width="100%" height="100%">
  <rect x="40" y="100" width="220" height="140" fill="rgba(255,255,255,0.12)" rx="14"/>
  <circle cx="150" cy="170" r="52" fill="rgba(0,0,0,0.3)" stroke="rgba(255,255,255,0.2)" stroke-width="8"/>
  <circle cx="150" cy="170" r="34" fill="rgba(0,0,0,0.35)" stroke="ACCENT" stroke-width="3" opacity="0.6"/>
  <circle cx="150" cy="170" r="18" fill="rgba(0,0,0,0.4)"/>
  <circle cx="140" cy="160" r="7" fill="rgba(255,255,255,0.15)"/>
  <rect x="200" y="110" width="50" height="35" fill="rgba(255,255,255,0.08)" rx="4"/>
  <circle cx="240" cy="108" r="14" fill="rgba(255,255,255,0.08)" stroke="rgba(255,255,255,0.15)" stroke-width="2"/>
  <circle cx="240" cy="108" r="9" fill="#ef4444" opacity="0.85"/>
  <line x1="150" y1="240" x2="100" y2="295" stroke="rgba(255,255,255,0.2)" stroke-width="5" stroke-linecap="round"/>
  <line x1="150" y1="240" x2="150" y2="295" stroke="rgba(255,255,255,0.2)" stroke-width="5" stroke-linecap="round"/>
  <line x1="150" y1="240" x2="200" y2="295" stroke="rgba(255,255,255,0.2)" stroke-width="5" stroke-linecap="round"/>
  <polygon points="260,130 330,95 330,175 260,150" fill="ACCENT" opacity="0.5"/>
  <circle cx="62" cy="108" r="8" fill="ACCENT" opacity="0.8"/>
</svg>''',
"art": '''<svg viewBox="0 0 400 300" xmlns="http://www.w3.org/2000/svg" width="100%" height="100%">
  <ellipse cx="185" cy="170" rx="120" ry="95" fill="rgba(255,255,255,0.1)"/>
  <circle cx="145" cy="185" r="22" fill="rgba(0,0,0,0.2)"/>
  <circle cx="240" cy="115" r="18" fill="ACCENT" opacity="0.85"/>
  <circle cx="280" cy="145" r="15" fill="rgba(255,255,255,0.3)"/>
  <circle cx="260" cy="185" r="18" fill="ACCENT" opacity="0.5"/>
  <circle cx="225" cy="215" r="15" fill="rgba(255,255,255,0.2)"/>
  <circle cx="180" cy="225" r="16" fill="ACCENT" opacity="0.35"/>
  <circle cx="115" cy="220" r="14" fill="rgba(255,255,255,0.25)"/>
  <rect x="290" y="50" width="12" height="130" fill="rgba(255,255,255,0.2)" rx="4" transform="rotate(30 296 115)"/>
  <ellipse cx="314" cy="62" rx="8" ry="20" fill="ACCENT" opacity="0.7" transform="rotate(30 314 70)"/>
  <path d="M30 60 Q80 40 120 70 Q160 100 140 130" fill="none" stroke="ACCENT" stroke-width="8" stroke-linecap="round" opacity="0.4"/>
  <path d="M30 100 Q70 80 100 105" fill="none" stroke="rgba(255,255,255,0.2)" stroke-width="5" stroke-linecap="round"/>
</svg>''',
"web": '''<svg viewBox="0 0 400 300" xmlns="http://www.w3.org/2000/svg" width="100%" height="100%">
  <rect x="30" y="40" width="340" height="240" fill="rgba(255,255,255,0.08)" rx="12"/>
  <rect x="30" y="40" width="340" height="42" fill="rgba(255,255,255,0.12)" rx="12"/>
  <rect x="30" y="70" width="340" height="12" fill="rgba(255,255,255,0.06)"/>
  <circle cx="58" cy="61" r="7" fill="#ef4444" opacity="0.7"/>
  <circle cx="78" cy="61" r="7" fill="#f59e0b" opacity="0.7"/>
  <circle cx="98" cy="61" r="7" fill="#22c55e" opacity="0.7"/>
  <rect x="118" y="51" width="220" height="20" fill="rgba(255,255,255,0.08)" rx="10"/>
  <circle cx="132" cy="61" r="5" fill="ACCENT" opacity="0.6"/>
  <rect x="48" y="100" width="304" height="80" fill="ACCENT" rx="6" opacity="0.2"/>
  <rect x="48" y="100" width="304" height="80" fill="none" stroke="ACCENT" stroke-width="1.5" rx="6" opacity="0.3"/>
  <rect x="65" y="118" width="180" height="12" fill="rgba(255,255,255,0.25)" rx="3"/>
  <rect x="65" y="138" width="120" height="8" fill="rgba(255,255,255,0.15)" rx="3"/>
  <rect x="65" y="154" width="90" height="8" fill="rgba(255,255,255,0.1)" rx="3"/>
  <rect x="230" y="140" width="100" height="28" fill="ACCENT" rx="6" opacity="0.6"/>
  <rect x="48" y="198" width="90" height="65" fill="rgba(255,255,255,0.08)" rx="6"/>
  <rect x="155" y="198" width="90" height="65" fill="rgba(255,255,255,0.08)" rx="6"/>
  <rect x="262" y="198" width="90" height="65" fill="rgba(255,255,255,0.08)" rx="6"/>
  <rect x="48" y="198" width="90" height="20" fill="ACCENT" rx="6" opacity="0.2"/>
  <rect x="155" y="198" width="90" height="20" fill="ACCENT" rx="6" opacity="0.2"/>
  <rect x="262" y="198" width="90" height="20" fill="ACCENT" rx="6" opacity="0.2"/>
</svg>''',
"landscaping": '''<svg viewBox="0 0 400 300" xmlns="http://www.w3.org/2000/svg" width="100%" height="100%">
  <ellipse cx="200" cy="265" rx="180" ry="20" fill="ACCENT" opacity="0.2"/>
  <rect x="88" y="185" width="14" height="80" fill="rgba(255,255,255,0.15)" rx="4"/>
  <circle cx="95" cy="145" r="50" fill="ACCENT" opacity="0.3"/>
  <circle cx="75" cy="165" r="35" fill="ACCENT" opacity="0.35"/>
  <circle cx="115" cy="162" r="38" fill="ACCENT" opacity="0.25"/>
  <rect x="288" y="200" width="10" height="65" fill="rgba(255,255,255,0.15)" rx="3"/>
  <circle cx="293" cy="168" r="38" fill="ACCENT" opacity="0.3"/>
  <circle cx="275" cy="182" r="28" fill="ACCENT" opacity="0.25"/>
  <circle cx="170" cy="250" r="10" fill="ACCENT" opacity="0.7"/>
  <circle cx="160" cy="245" r="7" fill="rgba(255,255,255,0.3)"/>
  <circle cx="180" cy="245" r="7" fill="rgba(255,255,255,0.3)"/>
  <circle cx="240" cy="255" r="8" fill="ACCENT" opacity="0.6"/>
  <circle cx="320" cy="70" r="35" fill="ACCENT" opacity="0.4"/>
  <circle cx="320" cy="70" r="22" fill="ACCENT" opacity="0.5"/>
  <line x1="320" y1="22" x2="320" y2="35" stroke="ACCENT" stroke-width="3" opacity="0.4"/>
  <line x1="320" y1="105" x2="320" y2="118" stroke="ACCENT" stroke-width="3" opacity="0.4"/>
  <line x1="272" y1="70" x2="285" y2="70" stroke="ACCENT" stroke-width="3" opacity="0.4"/>
  <line x1="355" y1="70" x2="368" y2="70" stroke="ACCENT" stroke-width="3" opacity="0.4"/>
</svg>''',
"tools": '''<svg viewBox="0 0 400 300" xmlns="http://www.w3.org/2000/svg" width="100%" height="100%">
  <rect x="60" y="140" width="160" height="30" fill="rgba(255,255,255,0.2)" rx="8" transform="rotate(-45 140 155)"/>
  <circle cx="80" cy="195" r="28" fill="rgba(255,255,255,0.1)" stroke="rgba(255,255,255,0.2)" stroke-width="4"/>
  <circle cx="80" cy="195" r="14" fill="rgba(255,255,255,0.15)"/>
  <circle cx="200" cy="75" r="22" fill="rgba(255,255,255,0.1)" stroke="rgba(255,255,255,0.2)" stroke-width="4"/>
  <circle cx="200" cy="75" r="11" fill="rgba(255,255,255,0.15)"/>
  <rect x="220" y="145" width="90" height="30" fill="ACCENT" rx="8" opacity="0.75"/>
  <rect x="260" y="95" width="18" height="90" fill="rgba(255,255,255,0.2)" rx="5"/>
  <rect x="308" y="58" width="28" height="16" fill="ACCENT" rx="3" opacity="0.5" transform="rotate(20 322 66)"/>
  <rect x="50" y="50" width="60" height="60" fill="rgba(255,255,255,0.1)" rx="12"/>
  <circle cx="80" cy="80" r="20" fill="rgba(255,255,255,0.08)" stroke="ACCENT" stroke-width="2" opacity="0.5"/>
  <rect x="110" y="78" width="80" height="10" fill="ACCENT" rx="3" opacity="0.4"/>
</svg>''',
"general": '''<svg viewBox="0 0 400 300" xmlns="http://www.w3.org/2000/svg" width="100%" height="100%">
  <path d="M200 40 C155 40 120 75 120 118 C120 165 200 250 200 250 C200 250 280 165 280 118 C280 75 245 40 200 40Z" fill="ACCENT" opacity="0.5"/>
  <path d="M200 40 C155 40 120 75 120 118 C120 165 200 250 200 250 C200 250 280 165 280 118 C280 75 245 40 200 40Z" fill="none" stroke="rgba(255,255,255,0.3)" stroke-width="3"/>
  <circle cx="200" cy="118" r="32" fill="rgba(255,255,255,0.25)"/>
  <circle cx="200" cy="118" r="18" fill="rgba(255,255,255,0.4)"/>
  <circle cx="200" cy="265" r="20" fill="ACCENT" opacity="0.15"/>
  <circle cx="200" cy="265" r="40" fill="ACCENT" opacity="0.08"/>
  <circle cx="80" cy="100" r="4" fill="rgba(255,255,255,0.2)"/>
  <circle cx="320" cy="80" r="3" fill="rgba(255,255,255,0.15)"/>
  <circle cx="340" cy="200" r="5" fill="rgba(255,255,255,0.15)"/>
  <circle cx="60" cy="180" r="4" fill="rgba(255,255,255,0.12)"/>
</svg>''',
}


def get_svg(categories, accent):
    for cat in categories:
        group = CATEGORY_SVG_GROUP.get(cat)
        if group:
            svg = SVG_ILLUSTRATIONS.get(group, SVG_ILLUSTRATIONS["general"])
            return svg.replace("ACCENT", accent)
    return SVG_ILLUSTRATIONS["general"].replace("ACCENT", accent)


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


def generate_html(company):
    name = (company.get("title") or company.get("﻿title") or "").strip()
    if not name or name in (".", "Z", ""):
        return None

    cats = [company.get(f"categories/{i}", "").strip() for i in range(9)]
    cats = [c for c in cats if c]
    primary_cat = cats[0] if cats else ""
    if primary_cat in SKIP_CATEGORIES:
        return None

    matched_cat, cfg = get_config(cats)

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

    svg_html  = get_svg(cats, A)

    # Numbers stats section (replaces gallery)
    numbers_html = f"""
<div class="numbers-section">
  <div class="wrap">
    <div class="numbers-grid">
      <div class="number-card"><div class="number-val">10+</div><div class="number-label">Jaar Ervaring</div></div>
      <div class="number-card"><div class="number-val">500+</div><div class="number-label">Projecten Voltooid</div></div>
      <div class="number-card"><div class="number-val">100%</div><div class="number-label">Klanttevredenheid</div></div>
      <div class="number-card"><div class="number-val">Amsterdam</div><div class="number-label">Gevestigd &amp; Vertrouwd</div></div>
    </div>
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

    phone_btn = f'<a href="tel:{hl.escape(phone)}" class="btn-primary">📞 Bel Ons</a>' if phone else '<a href="#contact" class="btn-primary">Neem Contact Op</a>'
    maps_btn  = f'<a href="{hl.escape(maps_url)}" target="_blank" class="btn-outline">📍 Bekijk op Maps</a>' if maps_url else ""

    phone_detail = f"<div class='cdetail'><div class='cdetail-icon'>📞</div><div><div class='cdetail-label'>Telefoon</div><div class='cdetail-val'>{hl.escape(phone)}</div></div></div>" if phone else ""
    addr_detail  = f"<div class='cdetail'><div class='cdetail-icon'>📍</div><div><div class='cdetail-label'>Adres</div><div class='cdetail-val'>{hl.escape(addr)}</div></div></div>" if addr else ""

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
.hero{{min-height:100vh;background:var(--p);display:flex;flex-direction:column;justify-content:center;padding:100px 5% 80px;position:relative;overflow:hidden}}
.hero::before{{content:\'\';position:absolute;inset:0;background:radial-gradient(ellipse 70% 70% at 75% 50%,color-mix(in srgb,var(--a) 15%,transparent),transparent 70%);pointer-events:none}}
.hero-noise{{position:absolute;inset:0;pointer-events:none;opacity:.03;background-image:url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='4'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E");background-size:200px}}
.hero-inner{{display:grid;grid-template-columns:1fr 1fr;gap:60px;align-items:center;max-width:1160px;margin:0 auto;width:100%;position:relative}}
.hero-content{{text-align:left}}
.hero-illustration{{display:flex;align-items:center;justify-content:center}}
.hero-illustration svg{{filter:drop-shadow(0 20px 60px rgba(0,0,0,0.3))}}
.hero-pill{{display:inline-flex;align-items:center;gap:8px;background:rgba(255,255,255,.12);border:1px solid rgba(255,255,255,.25);border-radius:999px;padding:6px 18px;font-size:.75rem;font-weight:700;letter-spacing:1.2px;text-transform:uppercase;color:rgba(255,255,255,.9);margin-bottom:28px;backdrop-filter:blur(8px)}}
.pill-dot{{width:7px;height:7px;border-radius:50%;background:var(--a);animation:pulse 2s infinite}}
@keyframes pulse{{0%,100%{{opacity:1;transform:scale(1)}}50%{{opacity:.5;transform:scale(.8)}}}}
.hero h1{{font-size:clamp(2.4rem,5.5vw,4.2rem);font-weight:900;color:#fff;line-height:1.02;letter-spacing:-2px;margin-bottom:10px;text-shadow:0 2px 20px rgba(0,0,0,.3)}}
.hero h1 em{{font-style:normal;color:var(--a);}}
.hero-sub{{font-size:clamp(.9rem,1.8vw,1.1rem);color:rgba(255,255,255,.68);max-width:500px;margin:0 0 32px;font-weight:400;line-height:1.75}}
.hero-rating{{display:inline-flex;align-items:center;gap:10px;background:rgba(255,255,255,.1);border:1px solid rgba(255,255,255,.18);border-radius:999px;padding:8px 20px;color:rgba(255,255,255,.85);font-size:.85rem;margin-bottom:30px;backdrop-filter:blur(8px)}}
.hero-stars{{color:var(--a);letter-spacing:2px}}
.hero-btns{{display:flex;gap:12px;flex-wrap:wrap;justify-content:flex-start}}
/* NUMBERS */
.numbers-section{{background:var(--a);padding:56px 0}}
.numbers-grid{{display:grid;grid-template-columns:repeat(4,1fr);gap:24px;text-align:center}}
.number-val{{font-size:clamp(1.8rem,4vw,2.8rem);font-weight:900;color:#fff;line-height:1}}
.number-label{{font-size:.75rem;color:rgba(255,255,255,.75);font-weight:600;margin-top:6px;text-transform:uppercase;letter-spacing:1px}}
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
  .hero-inner{{grid-template-columns:1fr}}
  .hero-illustration{{display:none}}
  .numbers-grid{{grid-template-columns:repeat(2,1fr)}}
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
  <a href="#contact" class="nav-cta">Gratis Offerte →</a>
</nav>

<section class="hero">
  <div class="hero-noise"></div>
  <div class="hero-inner">
    <div class="hero-content">
      <div class="hero-pill"><span class="pill-dot"></span>{hl.escape(icon)} {hl.escape(cat_label)} · Amsterdam</div>
      <h1>{t1}<br><em>{t2}</em></h1>
      <p class="hero-sub">{hl.escape(hero_desc)}</p>
      {rating_html}
      <div class="hero-btns">
        {phone_btn}
        <a href="#services" class="btn-ghost">Onze Diensten</a>
      </div>
    </div>
    <div class="hero-illustration">
      {svg_html}
    </div>
  </div>
</section>

<div class="trust-bar">{tbs}</div>

<div class="services-section">
  <div class="wrap reveal">
    <p class="section-tag">Wat Wij Doen</p>
    <h2 class="section-title">Onze <span>Diensten</span></h2>
    <p class="section-lead">{hl.escape(hero_desc)}</p>
    <div class="svc-grid" id="services">{svcs}</div>
  </div>
</div>

{numbers_html}

<div class="process-section">
  <div class="wrap reveal">
    <p class="section-tag">Hoe Het Werkt</p>
    <h2 class="section-title">Eenvoudig. <span>Transparant.</span> Geregeld.</h2>
    <div class="process-grid">{procs}</div>
  </div>
</div>

<div class="testi-section">
  <div class="wrap reveal">
    <p class="section-tag">Klantbeoordelingen</p>
    <h2 class="section-title">Vertrouwd door <span>Amsterdam</span></h2>
    <p class="section-lead">Niet alleen ons woord — dit zeggen onze klanten.</p>
    <div class="testi-grid">{ts}</div>
  </div>
</div>

<div class="contact-section" id="contact">
  <div class="wrap">
    <div class="contact-grid">
      <div class="reveal">
        <p class="section-tag">Neem Contact Op</p>
        <h2 class="section-title">Klaar om te<br><span>Beginnen?</span></h2>
        <p class="contact-lead">Neem vandaag contact op voor een vrijblijvende offerte. Wij reageren doorgaans binnen enkele uren.</p>
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

    print("Generating HTML files...")
    for f in os.listdir(OUTPUT_DIR):
        if f.endswith('.html'):
            os.remove(os.path.join(OUTPUT_DIR, f))

    generated = skipped = 0
    seen_slugs = {}

    with open(CSV_PATH, newline='', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            page = generate_html(row)
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
