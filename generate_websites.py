#!/usr/bin/env python3
"""
Website generator for Amsterdam businesses — v2 (polished).
Generates a premium, professional HTML demo site for each company.
Purpose: outreach / lead generation to sell web design services.
"""

import csv
import os
import re
import html as html_lib
import random

OUTPUT_DIR = "websites"
CSV_PATH = "/root/.claude/uploads/b553d4c3-fa71-535d-b226-64e15b822f4e/e9e48877-dataset_amsterdam1_20260614_171131429.csv"

SKIP_CATEGORIES = {
    "Park", "Garden", "Lake", "Community garden", "Area", "Hiking area",
    "House", "Vacation rental", "Shipyard",
}

CATEGORY_CONFIG = {
    "Bricklayer": {
        "primary": "#0f172a", "accent": "#f97316", "accent2": "#fb923c",
        "icon": "🧱", "emoji_bg": "🧱",
        "tagline": "Building Amsterdam's Future,\nOne Brick at a Time",
        "hero_desc": "Expert bricklaying and restoration masonry. Trusted by homeowners and developers across Amsterdam for quality work that stands the test of time.",
        "services": [
            ("🧱", "Brickwork & Pointing", "Precision brickwork for new builds and repairs."),
            ("🏛️", "Facade Restoration", "Breathing new life into historic Amsterdam facades."),
            ("🔨", "New Build Masonry", "Structural masonry for residential and commercial projects."),
            ("🪨", "Repointing & Repairs", "Weatherproof repointing to protect your property."),
            ("✨", "Heritage Stonework", "Specialist restoration of ornate and historic stonework."),
        ],
        "testimonials": [
            ("Jan V.", "Amsterdam Noord", "Excellent craftsmanship. The facade looks better than ever — really professional team."),
            ("Maria S.", "De Pijp", "On time, clean, and the quality is superb. Would recommend to everyone."),
            ("Thomas B.", "Jordaan", "Best decision we made for our renovation. Outstanding work from start to finish."),
        ],
        "process": [("📞", "Free Consultation", "Tell us about your project and we'll assess your needs."), ("📋", "Detailed Quote", "We provide a transparent, itemised quote with no hidden costs."), ("🏗️", "Expert Delivery", "Our skilled team delivers on time and to the highest standard.")],
        "trust": ["Licensed & Insured", "10+ Years Experience", "Free Quotes", "Amsterdam Based"],
    },
    "Masonry contractor": {
        "primary": "#1c1917", "accent": "#ea580c", "accent2": "#f97316",
        "icon": "🏗️", "emoji_bg": "🏗️",
        "tagline": "Precision Masonry.\nLasting Results.",
        "hero_desc": "Professional masonry contracting for residential and commercial projects. We bring craftsmanship, reliability and quality to every job in Amsterdam.",
        "services": [
            ("🧱", "Brick & Block Laying", "Expert masonry for walls, structures and facades."),
            ("🏗️", "Structural Masonry", "Load-bearing and structural work to the highest standard."),
            ("🔄", "Renovation & Restoration", "Sympathetic restoration that preserves character."),
            ("🌿", "Garden Walls & Patios", "Beautiful outdoor structures built to last."),
            ("🏠", "Chimney Repairs", "Safe, thorough chimney repair and repointing."),
        ],
        "testimonials": [
            ("Peter K.", "Amsterdam West", "Excellent work, very clean and professional. Highly recommended."),
            ("Anna L.", "Centrum", "Transformed our garden wall completely. Really happy with the result."),
            ("Rob M.", "Oost", "Reliable, skilled and great value for money. Will use again."),
        ],
        "process": [("📞", "Free Consultation", "We discuss your project and visit the site if needed."), ("📋", "Transparent Quote", "A detailed, fixed-price quote with no surprises."), ("✅", "Quality Build", "Skilled tradespeople who take pride in every job.")],
        "trust": ["Fully Insured", "Free Site Visits", "Satisfaction Guaranteed", "Local Experts"],
    },
    "Carpenter": {
        "primary": "#292524", "accent": "#d97706", "accent2": "#f59e0b",
        "icon": "🪵", "emoji_bg": "🪵",
        "tagline": "Crafted with Precision.\nBuilt to Last.",
        "hero_desc": "Expert carpentry and bespoke joinery for homes and businesses throughout Amsterdam. From custom furniture to full renovations, we craft spaces you'll love.",
        "services": [
            ("🗄️", "Custom Furniture & Cabinetry", "Bespoke pieces designed and built for your space."),
            ("🪵", "Flooring Installation", "Solid wood, engineered and laminate flooring fitted perfectly."),
            ("🚪", "Doors & Windows", "New installations, repairs and draught-proofing."),
            ("🏠", "Renovations & Fit-outs", "Complete interior transformations from start to finish."),
            ("🪜", "Stairs & Balustrades", "Beautiful, safe staircases crafted to your specification."),
        ],
        "testimonials": [
            ("Sophie D.", "Oud-West", "Our new kitchen is absolutely stunning. Incredible craftsmanship."),
            ("Erik J.", "Buitenveldert", "Built exactly what we envisioned — and on budget. Amazing."),
            ("Clara M.", "Rivierenbuurt", "The staircase is a work of art. Couldn't be happier."),
        ],
        "process": [("💬", "Design Chat", "We listen to your vision and suggest the best approach."), ("📐", "Precise Planning", "Detailed drawings and material selection before a single cut."), ("🔨", "Master Craftsmanship", "Hand-finished work that exceeds expectations every time.")],
        "trust": ["Bespoke Craftsmanship", "15+ Years Experience", "Free Design Consult", "5-Year Guarantee"],
    },
    "Plumber": {
        "primary": "#0c1a2e", "accent": "#0ea5e9", "accent2": "#38bdf8",
        "icon": "🔧", "emoji_bg": "🔧",
        "tagline": "Fast, Reliable Plumbing —\nDay or Night",
        "hero_desc": "Professional plumbing for emergencies, installations and maintenance. Available 24/7 across Amsterdam — we fix it right the first time.",
        "services": [
            ("🚨", "24/7 Emergency Call-outs", "We're available around the clock for urgent plumbing issues."),
            ("🔥", "Boiler Installation & Service", "Expert boiler fitting, servicing and repair."),
            ("🛁", "Bathroom Fitting", "Full bathroom design and installation services."),
            ("💧", "Leak Detection & Repair", "Fast, accurate leak finding and fixing."),
            ("♨️", "Central Heating", "Installation, maintenance and power flushing."),
        ],
        "testimonials": [
            ("Hans B.", "Amsterdam Zuid", "Arrived within the hour. Fixed the leak perfectly. Lifesavers."),
            ("Lotte V.", "De Baarsjes", "New bathroom is gorgeous. Clean, fast and professional."),
            ("Dirk S.", "Noord", "Excellent service, fair price, and great advice. Highly recommend."),
        ],
        "process": [("📞", "Call or Book Online", "Reach us any time — we respond fast, day or night."), ("🔍", "Diagnose & Quote", "We identify the issue and give you an upfront price."), ("✅", "Fix & Follow Up", "We fix it right and check in to make sure you're happy.")],
        "trust": ["24/7 Available", "Gas Safe Registered", "No Call-out Fee", "Fully Insured"],
    },
    "Painter": {
        "primary": "#18181b", "accent": "#a855f7", "accent2": "#c084fc",
        "icon": "🎨", "emoji_bg": "🎨",
        "tagline": "Transforming Spaces with\nColour & Care",
        "hero_desc": "Professional interior and exterior painting and decorating for Amsterdam homes and businesses. Flawless finishes, minimal disruption, outstanding results.",
        "services": [
            ("🏠", "Interior Painting", "Perfect finishes for every room, every surface."),
            ("🌦️", "Exterior Painting", "Durable, weather-resistant exterior decoration."),
            ("🖼️", "Wallpapering", "Precision hanging of all wallpaper types."),
            ("🪵", "Wood Staining & Varnishing", "Beautiful protective finishes for timber surfaces."),
            ("🏢", "Commercial Painting", "Efficient, minimal-disruption commercial decorating."),
        ],
        "testimonials": [
            ("Noor A.", "Vondelpark area", "Incredible transformation. The finish is absolutely flawless."),
            ("Bas W.", "Watergraafsmeer", "Professional, tidy and the results are stunning. 10/10."),
            ("Eva K.", "IJburg", "Our office looks completely refreshed. Great team to work with."),
        ],
        "process": [("🎨", "Colour Consultation", "We help you choose the perfect palette for your space."), ("🛡️", "Surface Preparation", "Thorough prep work ensures a lasting, flawless finish."), ("✨", "Pristine Finish", "We leave your space spotless and looking its absolute best.")],
        "trust": ["Free Colour Advice", "Premium Paints Only", "Zero Mess Guarantee", "Fully Insured"],
    },
    "Electrician": {
        "primary": "#0f172a", "accent": "#eab308", "accent2": "#fde047",
        "icon": "⚡", "emoji_bg": "⚡",
        "tagline": "Powering Amsterdam —\nSafely & Reliably",
        "hero_desc": "Certified electricians delivering safe, reliable installation and maintenance services for homes and businesses across Amsterdam.",
        "services": [
            ("💡", "Electrical Installations", "Full wiring for new builds and renovations."),
            ("🔌", "Fuse Board Upgrades", "Modern consumer unit installation for safety and capacity."),
            ("💡", "Lighting Design", "Ambient, task and feature lighting solutions."),
            ("☀️", "Solar & EV Charging", "Future-ready energy solutions for your property."),
            ("📋", "Safety Inspections", "Electrical Installation Condition Reports (EICR)."),
        ],
        "testimonials": [
            ("Frank H.", "Amsterdam Oost", "Incredibly knowledgeable and thorough. Feel much safer now."),
            ("Inge P.", "Centrum", "Installed our EV charger quickly and cleanly. Great service."),
            ("Marc D.", "Amstelveen", "Transformed our lighting completely. The place looks amazing."),
        ],
        "process": [("📞", "Book a Visit", "We arrange a convenient time to assess your requirements."), ("📋", "Safety Assessment", "We evaluate your electrics and provide a full written quote."), ("⚡", "Expert Installation", "Certified work completed safely, cleanly and on schedule.")],
        "trust": ["DEKRA Certified", "All Work Guaranteed", "Free Safety Check", "24h Emergency"],
    },
    "Electrical installation service": {
        "primary": "#0f172a", "accent": "#eab308", "accent2": "#fde047",
        "icon": "⚡", "emoji_bg": "⚡",
        "tagline": "Expert Electrical Solutions\nfor Every Project",
        "hero_desc": "Reliable electrical installation services for residential and commercial clients. Safe, certified and always delivered on time.",
        "services": [
            ("🔌", "New Installations", "Complete electrical fit-outs for new builds and refurbs."),
            ("🔄", "Rewiring", "Full and partial rewiring for older properties."),
            ("🏠", "Smart Home Systems", "Control your home with the latest smart technology."),
            ("🚨", "Emergency Lighting", "Safety-compliant emergency lighting systems."),
            ("📋", "Electrical Testing", "Thorough testing and certification of all installations."),
        ],
        "testimonials": [
            ("Wim B.", "Noord", "Rewired our entire house with zero fuss. Brilliant team."),
            ("Sandra K.", "Zuid", "Smart home system is incredible — these guys know their stuff."),
            ("Paul V.", "West", "Professional, punctual and great value. Highly recommended."),
        ],
        "process": [("📞", "Get in Touch", "Call or email to discuss your electrical needs."), ("📐", "Site Survey", "We survey the site and provide a detailed, fixed quote."), ("✅", "Certified Completion", "All work is tested, certified and handed over with full documentation.")],
        "trust": ["NEN 1010 Compliant", "All Work Certified", "Clean & Tidy", "Local Specialists"],
    },
    "Bicycle repair shop": {
        "primary": "#14532d", "accent": "#22c55e", "accent2": "#4ade80",
        "icon": "🚲", "emoji_bg": "🚲",
        "tagline": "Get Back on the Road —\nFast",
        "hero_desc": "Expert bicycle repairs, servicing and upgrades in the heart of Amsterdam. We keep Amsterdam cycling — whatever the bike, whatever the problem.",
        "services": [
            ("🔧", "Full Bike Service", "Comprehensive inspection, adjustment and lubrication."),
            ("🩹", "Puncture Repairs", "Fast, reliable tyre repairs while you wait."),
            ("⚙️", "Brake & Gear Tuning", "Precise adjustment for smooth, safe riding."),
            ("⚡", "E-Bike Servicing", "Specialist servicing for all electric bicycle brands."),
            ("🛠️", "Custom Builds", "Build your perfect bike from the ground up."),
        ],
        "testimonials": [
            ("Femke O.", "Oost", "Fixed in 20 minutes and at a fair price. My go-to bike shop."),
            ("Joost L.", "Centrum", "Great service on my e-bike. They really know their stuff."),
            ("Roos V.", "West", "Super friendly and fast. Would never go anywhere else."),
        ],
        "process": [("🚲", "Bring Your Bike", "Drop in or book an appointment — we're always welcoming."), ("🔍", "Free Diagnostic", "We inspect your bike and tell you exactly what it needs."), ("✅", "Back on the Road", "Most repairs done same-day. Riding again in no time.")],
        "trust": ["Same-Day Repairs", "All Brands Welcome", "Free Diagnostics", "E-Bike Specialists"],
    },
    "Bicycle Shop": {
        "primary": "#14532d", "accent": "#22c55e", "accent2": "#4ade80",
        "icon": "🚲", "emoji_bg": "🚲",
        "tagline": "Amsterdam's Trusted\nBike Specialists",
        "hero_desc": "Quality bikes, expert repairs and everything a cyclist needs. Your local Amsterdam bike shop — passionate about cycling since day one.",
        "services": [
            ("🛒", "New Bike Sales", "City, road, mountain and e-bikes from top brands."),
            ("🔧", "Bike Servicing", "Full service and repairs by expert mechanics."),
            ("🎽", "Accessories & Parts", "Lights, locks, helmets, bags and everything in between."),
            ("⚡", "E-Bike Expertise", "Test rides, sales and servicing of electric bikes."),
            ("♻️", "Second-hand Bikes", "Quality pre-owned bikes at great prices."),
        ],
        "testimonials": [
            ("Lars P.", "Jordaan", "Best bike shop in Amsterdam. Knowledgeable staff and great range."),
            ("Hanna M.", "De Pijp", "Found the perfect city bike here. Amazing advice and service."),
            ("Kees R.", "Noord", "Bought my e-bike here — couldn't be happier with it."),
        ],
        "process": [("💬", "Expert Advice", "Tell us how you ride and we'll find your perfect bike."), ("🚲", "Test Ride", "Take your favourite bikes for a spin before you decide."), ("🛒", "Ride Away Happy", "We set up your new bike perfectly before you leave.")],
        "trust": ["Expert Staff", "Test Rides Available", "All Brands Stocked", "Service Guarantee"],
    },
    "Photographer": {
        "primary": "#0c0a09", "accent": "#d97706", "accent2": "#f59e0b",
        "icon": "📸", "emoji_bg": "📸",
        "tagline": "Moments Captured.\nStories Told.",
        "hero_desc": "Professional photography for portraits, events, products and commercial projects. Every image tells a story — let us tell yours beautifully.",
        "services": [
            ("👤", "Portrait Photography", "Authentic, flattering portraits that capture your personality."),
            ("🎉", "Event Coverage", "Full event documentation from arrival to last dance."),
            ("📦", "Commercial & Product", "High-impact imagery that makes your products shine."),
            ("💼", "Corporate Headshots", "Professional headshots for individuals and teams."),
            ("🖥️", "Editing & Retouching", "Expert post-production to perfect every image."),
        ],
        "testimonials": [
            ("Olivia T.", "Amsterdam", "Absolutely stunning photos. Captured exactly the feel we wanted."),
            ("Michael R.", "Centrum", "Our product photos look incredible. Sales have gone up noticeably."),
            ("Emma S.", "Zuid", "The most natural, beautiful headshots I've ever had. Thank you!"),
        ],
        "process": [("💬", "Creative Brief", "We discuss your vision, style and requirements in detail."), ("📸", "The Shoot", "A relaxed, professional session guided from start to finish."), ("🖼️", "Gallery Delivery", "Edited, high-resolution images delivered to your private gallery.")],
        "trust": ["Fast Turnaround", "Full Commercial Rights", "Private Online Gallery", "100% Satisfaction"],
    },
    "Photography studio": {
        "primary": "#0c0a09", "accent": "#d97706", "accent2": "#f59e0b",
        "icon": "📸", "emoji_bg": "📸",
        "tagline": "Creative Photography\nStudio in Amsterdam",
        "hero_desc": "A fully equipped, professionally lit studio for portraits, fashion, products and creative projects. Everything you need to create stunning imagery.",
        "services": [
            ("🏢", "Studio Hire", "Hire our fully equipped studio by the hour or day."),
            ("👤", "Portrait Sessions", "Relaxed, flattering portrait photography for everyone."),
            ("👗", "Fashion & Editorial", "High-end fashion and editorial photography."),
            ("📦", "Product Photography", "Clean, commercial product images for every platform."),
            ("🎬", "Video Shoots", "Professional video production in our versatile studio space."),
        ],
        "testimonials": [
            ("Zara M.", "Fashion brand", "The best studio in Amsterdam. Perfect light, great team."),
            ("Tim H.", "E-commerce", "Our product photos are transformed. Sales up 40% since the shoot."),
            ("Nina P.", "Model", "So professional and the results are stunning every time."),
        ],
        "process": [("📅", "Book Your Session", "Choose your date and session type — we'll handle the rest."), ("💡", "Studio Setup", "We prep the lighting, backdrops and equipment for your vision."), ("🖼️", "Delivered & Edited", "Professionally edited images delivered within 5 working days.")],
        "trust": ["Professional Equipment", "Flexible Hire", "Fast Delivery", "All Skill Levels Welcome"],
    },
    "Commercial photographer": {
        "primary": "#0c0a09", "accent": "#c2410c", "accent2": "#ea580c",
        "icon": "📷", "emoji_bg": "📷",
        "tagline": "Visual Excellence\nfor Your Brand",
        "hero_desc": "High-impact commercial photography that makes brands stand out. We create images that sell, inspire and connect with your audience.",
        "services": [
            ("🏢", "Brand Photography", "Consistent, powerful visuals that define your brand identity."),
            ("📦", "Product Shoots", "Studio and lifestyle product photography that drives conversions."),
            ("💼", "Corporate Portraits", "Professional portraits for executives and teams."),
            ("📢", "Advertising Campaigns", "Campaign imagery for print, digital and out-of-home."),
            ("📱", "Social Media Content", "Scroll-stopping imagery optimised for every platform."),
        ],
        "testimonials": [
            ("Brand Manager, TechCo", "Amsterdam", "Transformed our brand visuals completely. Exceptional quality."),
            ("Marketing Director", "Retail chain", "These photos have been our best performing content this year."),
            ("CEO, Startup", "Amsterdam", "Professional, creative and incredibly easy to work with."),
        ],
        "process": [("📋", "Creative Brief", "We develop a detailed shot list aligned with your brand goals."), ("📸", "Professional Shoot", "Expert direction to bring out the best in every subject."), ("🚀", "Ready to Publish", "Retouched, formatted images ready for every platform.")],
        "trust": ["Commercial Licensing", "Art Direction Included", "48h Rush Delivery", "NDA Available"],
    },
    "Photography service": {
        "primary": "#0c0a09", "accent": "#d97706", "accent2": "#f59e0b",
        "icon": "📸", "emoji_bg": "📸",
        "tagline": "Professional Photography\nServices in Amsterdam",
        "hero_desc": "Capturing your most important moments with skill, artistry and heart. Photography services tailored to every occasion.",
        "services": [
            ("🎉", "Event Photography", "Full coverage of weddings, parties and corporate events."),
            ("👤", "Portrait Sessions", "Beautiful, natural portraits for all the family."),
            ("📖", "Documentary", "Authentic storytelling photography for editorial and personal projects."),
            ("🖥️", "Editing & Retouching", "Expert post-production for your own photos too."),
            ("🖼️", "Print Services", "Museum-quality prints delivered to your door."),
        ],
        "testimonials": [
            ("Anna V.", "Amsterdam", "Our wedding photos are breathtaking. So glad we chose them."),
            ("Peter L.", "Oost", "Family portraits that we'll treasure forever. Wonderful experience."),
            ("Sara B.", "Centrum", "Talented, professional and so easy to work with."),
        ],
        "process": [("💬", "Initial Consultation", "We discuss your needs, style preferences and expectations."), ("📸", "The Session", "A professional shoot guided to get the best from every moment."), ("🖼️", "Gallery Delivery", "Online gallery of edited images ready within 7 days.")],
        "trust": ["All Occasions", "Fast Delivery", "Print Options", "Fully Insured"],
    },
    "Yoga studio": {
        "primary": "#1a2e1e", "accent": "#4ade80", "accent2": "#86efac",
        "icon": "🧘", "emoji_bg": "🧘",
        "tagline": "Find Your Balance.\nFind Your Peace.",
        "hero_desc": "A welcoming, inclusive yoga studio for all levels in Amsterdam. Whatever your experience, we have a class that will nurture your body and calm your mind.",
        "services": [
            ("🌅", "Hatha Yoga", "Classic postures and breathing for strength and flexibility."),
            ("🌊", "Vinyasa Flow", "Dynamic, flowing sequences that energise and challenge."),
            ("🌙", "Yin Yoga", "Deep, restorative poses held for longer to release tension."),
            ("🧒", "Kids Yoga", "Fun, playful yoga sessions designed for children."),
            ("🎯", "Private Sessions", "One-to-one sessions tailored entirely to your needs."),
        ],
        "testimonials": [
            ("Miriam K.", "Amsterdam", "This studio changed my life. So welcoming and professional."),
            ("David H.", "Oost", "Best yoga I've ever practised. The instructors are phenomenal."),
            ("Lena S.", "De Pijp", "The Yin classes are incredible. I leave feeling completely renewed."),
        ],
        "process": [("👋", "Welcome Session", "Your first class is on us — no experience needed."), ("🎯", "Find Your Class", "We guide you to the perfect class for your level and goals."), ("🌱", "Grow Your Practice", "Progress at your pace with a supportive, expert community.")],
        "trust": ["All Levels Welcome", "First Class Free", "Certified Instructors", "Small Class Sizes"],
    },
    "Dog trainer": {
        "primary": "#1c1430", "accent": "#a78bfa", "accent2": "#c4b5fd",
        "icon": "🐕", "emoji_bg": "🐕",
        "tagline": "Happier Dogs.\nHappier Owners.",
        "hero_desc": "Positive, reward-based dog training for puppies and adult dogs in Amsterdam. We solve behaviour problems and build a bond you'll both love.",
        "services": [
            ("🐶", "Puppy Classes", "Essential early training for a confident, well-mannered dog."),
            ("🎯", "One-to-One Training", "Personalised sessions at home or in a chosen location."),
            ("📚", "Obedience Training", "Basic to advanced commands taught with positive methods."),
            ("🧠", "Behaviour Consultation", "Expert analysis and solutions for challenging behaviours."),
            ("👥", "Group Classes", "Socialisation and training in a fun group environment."),
        ],
        "testimonials": [
            ("Joep V.", "Amsterdam Noord", "Our dog is transformed. Can't believe the difference. Amazing!"),
            ("Sanne B.", "West", "Patient, knowledgeable and brilliant with our nervous rescue dog."),
            ("Arjan D.", "Zuid", "The puppy classes were brilliant. Our puppy is an angel now."),
        ],
        "process": [("📋", "Behaviour Assessment", "We assess your dog's needs, history and specific challenges."), ("🎯", "Tailored Programme", "A training plan designed specifically for you and your dog."), ("🐾", "Lasting Results", "Ongoing support to make sure the good behaviour sticks.")],
        "trust": ["PETA-Aligned Methods", "All Breeds Welcome", "Proven Results", "Ongoing Support"],
    },
    "Pet trainer": {
        "primary": "#1c1430", "accent": "#a78bfa", "accent2": "#c4b5fd",
        "icon": "🐾", "emoji_bg": "🐾",
        "tagline": "Expert Pet Training\nin Amsterdam",
        "hero_desc": "Professional animal training using proven, positive methods. Building better relationships between pets and their owners across Amsterdam.",
        "services": [
            ("📋", "Behavioural Assessment", "In-depth assessment to understand your pet's needs."),
            ("🎯", "One-to-One Sessions", "Private training tailored to your pet and your goals."),
            ("👥", "Group Workshops", "Socialisation and training in a supportive group setting."),
            ("🧠", "Anxiety & Aggression", "Specialist support for complex behavioural challenges."),
            ("📚", "Obedience Training", "Building reliable responses and good manners."),
        ],
        "testimonials": [
            ("Kim O.", "Amsterdam", "Incredible results with our reactive dog. Highly recommend."),
            ("Sam L.", "Oost", "Expert, patient and genuinely brilliant with animals."),
            ("Bas T.", "Noord", "Our anxious cat is so much calmer now. Life-changing service."),
        ],
        "process": [("📞", "Initial Chat", "We discuss your pet's history and your goals in detail."), ("🔍", "Assessment", "An in-person assessment to observe behaviour first-hand."), ("🎯", "Training Plan", "A bespoke programme for measurable, lasting improvement.")],
        "trust": ["Positive Methods Only", "All Species Welcome", "Certified Trainers", "Free Initial Call"],
    },
    "Tutoring service": {
        "primary": "#0f2044", "accent": "#3b82f6", "accent2": "#60a5fa",
        "icon": "📚", "emoji_bg": "📚",
        "tagline": "Unlock Every Student's\nPotential",
        "hero_desc": "Expert tutoring in Amsterdam for school, university and professional development. We inspire confidence, build skills and deliver measurable results.",
        "services": [
            ("🔢", "Maths & Science", "Clear, patient explanations from experienced specialists."),
            ("🌍", "Languages", "Dutch, English, French, German and more."),
            ("📝", "Exam Preparation", "Targeted revision programmes for top grades."),
            ("🎓", "University Applications", "Personal statement coaching and application guidance."),
            ("💻", "Online Tutoring", "Flexible, effective sessions via video call."),
        ],
        "testimonials": [
            ("Parent of Tom K.", "Amsterdam Zuid", "Tom went from a D to an A in maths. Genuinely life-changing."),
            ("Student, 17", "Amstelveen", "Finally understand chemistry. My confidence is through the roof."),
            ("Parent of Lisa V.", "Centrum", "Incredibly professional and the results speak for themselves."),
        ],
        "process": [("📋", "Assessment", "We identify gaps, strengths and exactly what's needed to succeed."), ("🎯", "Personalised Plan", "A tailored programme aligned with the student's goals and schedule."), ("📈", "Measurable Progress", "Regular progress reports so you always know how it's going.")],
        "trust": ["DBS Checked Tutors", "Guaranteed Progress", "Flexible Scheduling", "All Levels"],
    },
    "Private tutor": {
        "primary": "#0f2044", "accent": "#3b82f6", "accent2": "#60a5fa",
        "icon": "📖", "emoji_bg": "📖",
        "tagline": "Personalised Learning\nThat Gets Results",
        "hero_desc": "Tailored private tutoring for students of all ages and levels. We build understanding, confidence and the skills to achieve real academic success.",
        "services": [
            ("🎯", "1-on-1 Tuition", "Fully personalised sessions focused entirely on the student."),
            ("📚", "Homework Support", "Clear, patient help with daily school work and assignments."),
            ("📝", "Exam Coaching", "Proven strategies and practice papers for top exam results."),
            ("👩‍🏫", "Subject Specialists", "Expert tutors for every subject and curriculum."),
            ("💻", "Online & In-person", "Flexible sessions to suit every schedule and location."),
        ],
        "testimonials": [
            ("Parent, Amsterdam", "Oost", "Results improved dramatically. Warm, encouraging and expert."),
            ("Adult learner", "Centrum", "Finally cracked Dutch grammar! Patient and brilliant teacher."),
            ("Student, 15", "Noord", "Makes everything so clear. Wish I'd found this tutor sooner."),
        ],
        "process": [("💬", "Free Intro Call", "We discuss the student's needs, challenges and ambitions."), ("📐", "Custom Plan", "A structured learning plan built around the student's schedule."), ("📈", "Track & Improve", "Regular check-ins to adapt and accelerate progress.")],
        "trust": ["Free First Session", "All Subjects", "Flexible Hours", "DBS Checked"],
    },
    "Education center": {
        "primary": "#0f2044", "accent": "#3b82f6", "accent2": "#60a5fa",
        "icon": "🏫", "emoji_bg": "🏫",
        "tagline": "Inspiring Minds.\nBuilding Futures.",
        "hero_desc": "A dedicated education centre helping students of all ages achieve their full academic potential with expert tuition and personalised support.",
        "services": [
            ("📚", "Academic Programmes", "Structured courses covering all major subjects and levels."),
            ("📝", "Test Preparation", "Intensive prep programmes for any exam."),
            ("📖", "After-School Support", "Daily homework help and study skills training."),
            ("👨‍💼", "Adult Learning", "Upskilling and professional development courses."),
            ("💻", "Online Courses", "Learn from anywhere with our online learning platform."),
        ],
        "testimonials": [
            ("Parent of student", "Amsterdam", "My daughter's grades have soared. Excellent teachers here."),
            ("Adult student", "West", "Completed my language course and got the job I wanted. Thank you!"),
            ("Parent", "Zuid", "Wonderful environment and incredibly supportive staff."),
        ],
        "process": [("📋", "Initial Assessment", "We evaluate skills and learning goals for each student."), ("🎯", "Tailored Programme", "A personalised study plan designed for success."), ("🏆", "Achieve & Progress", "Ongoing support to reach targets and set new ones.")],
        "trust": ["Qualified Educators", "Small Class Sizes", "Online & In-person", "Progress Reports"],
    },
    "Mover": {
        "primary": "#0f1b35", "accent": "#3b82f6", "accent2": "#60a5fa",
        "icon": "🚚", "emoji_bg": "🚚",
        "tagline": "Your Move,\nMade Easy",
        "hero_desc": "Professional, careful removals for homes and offices across Amsterdam and beyond. We handle everything so moving day is stress-free.",
        "services": [
            ("🏠", "Home Removals", "Careful, efficient moves for houses and apartments."),
            ("🏢", "Office Relocations", "Minimal-disruption business moves, any size."),
            ("📦", "Packing & Unpacking", "Expert packing using quality materials to protect your belongings."),
            ("🏭", "Storage Solutions", "Secure short and long-term storage for any situation."),
            ("🌍", "International Moves", "Worldwide relocation services you can trust."),
        ],
        "testimonials": [
            ("Simone L.", "Amsterdam", "Moved our entire 3-bed flat without a single scratch. Brilliant."),
            ("Office Manager", "Centrum", "Office move completed over a weekend with zero downtime. Excellent."),
            ("Jonas R.", "Noord", "Careful, fast and friendly team. Moving day was actually enjoyable!"),
        ],
        "process": [("📋", "Free Survey", "We assess your move and provide a precise, competitive quote."), ("📦", "Expert Packing", "Our team packs everything safely using professional materials."), ("🚚", "Delivered Safely", "Your belongings arrive on time, intact and perfectly placed.")],
        "trust": ["Fully Insured", "No Hidden Charges", "Weekend Availability", "Fragile Item Specialists"],
    },
    "Moving and storage service": {
        "primary": "#0f1b35", "accent": "#3b82f6", "accent2": "#60a5fa",
        "icon": "📦", "emoji_bg": "📦",
        "tagline": "Stress-Free Moving\n& Secure Storage",
        "hero_desc": "Full-service removals and secure storage solutions for Amsterdam residents and businesses. Your belongings are always in safe hands.",
        "services": [
            ("🚚", "Local Moves", "Fast, careful moves anywhere in Amsterdam."),
            ("🌍", "Long-distance Moves", "Nationwide and international removals."),
            ("🏭", "Secure Storage", "Clean, monitored storage units for any duration."),
            ("📦", "Packing Materials", "Professional packing supplies available to purchase or hire."),
            ("🔧", "Furniture Assembly", "Full assembly and disassembly service at both ends."),
        ],
        "testimonials": [
            ("Rachel G.", "Amsterdam", "Used their storage for 3 months. Clean, secure and affordable."),
            ("Martin H.", "West", "Smoothest move I've ever had. Would absolutely use again."),
            ("Fatima A.", "Oost", "Packed our whole house beautifully. Not a thing was damaged."),
        ],
        "process": [("📋", "Free Quote", "Tell us about your move and we'll give you a fixed price."), ("📦", "We Pack & Collect", "Our team arrives on time and handles everything professionally."), ("✅", "Delivered & Settled", "We deliver, unpack and even reassemble furniture if needed.")],
        "trust": ["Fully Insured", "GPS-Tracked Vehicles", "Flexible Storage", "24h Support"],
    },
    "Trucking company": {
        "primary": "#1c1917", "accent": "#f97316", "accent2": "#fb923c",
        "icon": "🚛", "emoji_bg": "🚛",
        "tagline": "Reliable Transport.\nOn Time. Every Time.",
        "hero_desc": "Professional freight and logistics services operating across the Netherlands and Europe. Your cargo, delivered safely and on schedule.",
        "services": [
            ("📦", "Freight Transport", "Full and part loads across the Netherlands and Europe."),
            ("🏃", "Same-day Delivery", "Urgent collections and deliveries for time-critical freight."),
            ("🎯", "Pallet & Bulk Loads", "Efficient handling of palletised and bulk cargo."),
            ("❄️", "Temperature Controlled", "Refrigerated transport for sensitive goods."),
            ("🌍", "Cross-border Logistics", "Customs-cleared international transport solutions."),
        ],
        "testimonials": [
            ("Logistics Manager", "Amsterdam", "Consistently on time and always professional. Our top carrier."),
            ("Operations Director", "Rotterdam", "Handled our urgent cross-border delivery perfectly. Very impressed."),
            ("Warehouse Manager", "Noord", "Reliable, careful and great communication throughout."),
        ],
        "process": [("📞", "Book Collection", "Call or book online and we'll confirm your slot."), ("📋", "Collection & Manifest", "We collect on time with full documentation."), ("🚛", "Tracked Delivery", "Real-time tracking until your freight reaches its destination.")],
        "trust": ["GPS Tracked", "Fully Insured", "EU-Wide Coverage", "Same-day Available"],
    },
    "Courier service": {
        "primary": "#1c1917", "accent": "#ef4444", "accent2": "#f87171",
        "icon": "📬", "emoji_bg": "📬",
        "tagline": "Fast. Secure.\nDelivered.",
        "hero_desc": "Same-day and next-day courier services across Amsterdam and the Netherlands. When it absolutely must arrive on time, trust us.",
        "services": [
            ("⚡", "Same-day Delivery", "Urgent city deliveries within hours."),
            ("📬", "Next-day Courier", "Reliable next-day nationwide delivery."),
            ("📍", "Parcel Tracking", "Real-time tracking on every delivery."),
            ("🏢", "Business Accounts", "Dedicated account management for regular business customers."),
            ("🌍", "International Shipping", "Door-to-door international courier services."),
        ],
        "testimonials": [
            ("PA at law firm", "Centrum", "Delivered critical documents same day. Absolute lifesaver."),
            ("E-commerce Manager", "Amsterdam", "Our delivery SLAs have never been better. Excellent partner."),
            ("Retailer", "West", "Fast, reliable and the tracking is brilliant. Highly recommend."),
        ],
        "process": [("📞", "Book a Collection", "Call, email or use our app to schedule a pickup."), ("📦", "We Collect & Dispatch", "On-time collection and immediate dispatch to your recipient."), ("✅", "Confirmed Delivery", "Proof of delivery notification as soon as it's signed for.")],
        "trust": ["Same-day Available", "Real-time Tracking", "Insured Deliveries", "Business Accounts"],
    },
    "Shipping company": {
        "primary": "#0c2340", "accent": "#06b6d4", "accent2": "#22d3ee",
        "icon": "🚢", "emoji_bg": "🚢",
        "tagline": "Your Cargo,\nOur Commitment",
        "hero_desc": "International and domestic shipping solutions you can rely on. Expert logistics from Amsterdam to the world.",
        "services": [
            ("🌍", "International Freight", "Worldwide sea, air and road freight solutions."),
            ("📋", "Customs Clearance", "Smooth customs processing for all international shipments."),
            ("📦", "Parcel Services", "Reliable parcel delivery domestically and internationally."),
            ("🚪", "Door-to-door Delivery", "Complete collection and delivery management."),
            ("🔗", "Supply Chain Management", "End-to-end logistics optimisation for your business."),
        ],
        "testimonials": [
            ("Import Manager", "Amsterdam", "Handles our international freight flawlessly every time."),
            ("Export Director", "Schiphol area", "Customs is never a problem with this team. Brilliant service."),
            ("SME Owner", "Noord", "Affordable, reliable and always communicate proactively."),
        ],
        "process": [("📋", "Freight Quote", "Tell us your cargo details for a competitive, all-inclusive quote."), ("📦", "We Handle Logistics", "Collection, documentation, customs and dispatch all managed."), ("🌍", "World Delivery", "Real-time updates until your freight arrives at destination.")],
        "trust": ["Worldwide Coverage", "Customs Experts", "Cargo Insurance", "Track & Trace"],
    },
    "Delivery service": {
        "primary": "#1c1917", "accent": "#ef4444", "accent2": "#f87171",
        "icon": "🏃", "emoji_bg": "🏃",
        "tagline": "Speed. Reliability.\nDelivered to Your Door.",
        "hero_desc": "Fast, dependable delivery services across Amsterdam. We deliver for businesses and individuals who need things to arrive on time, every time.",
        "services": [
            ("⚡", "Express Delivery", "Urgent deliveries completed in hours."),
            ("📅", "Scheduled Runs", "Regular collection routes for ongoing business needs."),
            ("🏘️", "Last-mile Logistics", "Efficient final-mile delivery anywhere in Amsterdam."),
            ("📍", "Parcel Tracking", "Real-time updates for every delivery."),
            ("🤝", "Business Contracts", "Tailored agreements for high-volume senders."),
        ],
        "testimonials": [
            ("Restaurant owner", "Oost", "Deliveries are always on time and the food arrives perfect."),
            ("Online retailer", "Amsterdam", "Reliable and our customers are always happy. Great service."),
            ("Medical practice", "Zuid", "Critical supplies arrive exactly when promised. We trust them completely."),
        ],
        "process": [("📦", "Book Collection", "Schedule online or by phone — quick and easy."), ("🏃", "Collected Fast", "We arrive promptly at the agreed collection time."), ("✅", "Delivered & Confirmed", "Proof of delivery straight to your inbox.")],
        "trust": ["Same-hour Available", "Live Tracking", "Fully Insured", "Business Contracts"],
    },
    "Contractor": {
        "primary": "#1c1917", "accent": "#f97316", "accent2": "#fb923c",
        "icon": "🏗️", "emoji_bg": "🏗️",
        "tagline": "Quality Contracting.\nGuaranteed Satisfaction.",
        "hero_desc": "Full-service construction and contracting for residential and commercial clients. We manage every detail so you can focus on what matters.",
        "services": [
            ("🏗️", "New Build", "Complete construction of new residential and commercial properties."),
            ("🔄", "Renovation", "Full property renovations handled from design to completion."),
            ("📋", "Project Management", "End-to-end management of your entire building project."),
            ("✨", "Fit-out & Finishing", "High-quality interior fit-outs and finishing work."),
            ("🏛️", "Structural Work", "Expert structural alterations and extensions."),
        ],
        "testimonials": [
            ("Property developer", "Amsterdam", "Completed on time and budget. Exceptional quality throughout."),
            ("Home owner", "Zuid", "Our renovation is everything we dreamed of. Outstanding work."),
            ("Business owner", "Oost", "Professional team, great communication, perfect result."),
        ],
        "process": [("📐", "Site Assessment", "We assess your project and provide a detailed fixed-price quote."), ("📋", "Project Planning", "Full schedule, material selection and team coordination."), ("🏗️", "Expert Delivery", "Skilled tradespeople and a dedicated project manager throughout.")],
        "trust": ["Fixed-price Contracts", "Fully Licensed", "Project Manager Assigned", "10-Year Guarantee"],
    },
    "General contractor": {
        "primary": "#1c1917", "accent": "#f97316", "accent2": "#fb923c",
        "icon": "🏗️", "emoji_bg": "🏗️",
        "tagline": "From Foundation to Finish —\nWe Build It All",
        "hero_desc": "Experienced general contractors delivering quality builds across Amsterdam. One point of contact for your entire project.",
        "services": [
            ("📋", "Project Management", "Complete oversight of all trades and schedules."),
            ("🏗️", "New Construction", "Residential and commercial builds to the highest standard."),
            ("🔄", "Renovations", "Full property renovations from planning to completion."),
            ("🏢", "Commercial Fit-out", "Efficient, professional commercial interior works."),
            ("🤝", "Subcontractor Coordination", "We manage all trades — you have one contact."),
        ],
        "testimonials": [
            ("Developer", "Amsterdam", "Our go-to contractor. Always professional, always on time."),
            ("Restaurant owner", "Centrum", "Delivered our full fit-out in record time. Brilliant team."),
            ("Home owner", "West", "Managed everything seamlessly. The result is stunning."),
        ],
        "process": [("📞", "Initial Consultation", "Discuss scope, timeline and budget with our project team."), ("📐", "Detailed Planning", "Comprehensive project plan with fixed milestones and costs."), ("🏗️", "Managed Build", "We coordinate everything — you just watch it come together.")],
        "trust": ["Single Point of Contact", "Fixed Milestones", "Full Insurance Cover", "Transparent Costs"],
    },
    "Construction company": {
        "primary": "#0f172a", "accent": "#f97316", "accent2": "#fb923c",
        "icon": "🏛️", "emoji_bg": "🏛️",
        "tagline": "Built on Trust.\nBuilt to Last.",
        "hero_desc": "A leading construction company delivering quality projects across Amsterdam. From foundations to finishing touches, we build with pride.",
        "services": [
            ("🏠", "Residential Construction", "Quality homes built to your exact specification."),
            ("🏢", "Commercial Projects", "Offices, retail and commercial builds delivered on time."),
            ("🏗️", "Structural Engineering", "Expert structural solutions for complex building challenges."),
            ("📋", "Site Management", "Professional site management and health & safety compliance."),
            ("🔑", "Turnkey Solutions", "Complete design-and-build packages for maximum convenience."),
        ],
        "testimonials": [
            ("Property investor", "Amsterdam", "Our best build to date. Quality, speed and communication all superb."),
            ("Corporate client", "Zuidoost", "Office delivered 2 weeks early and under budget. Remarkable."),
            ("Home buyer", "Noord", "Our new home is perfect. Every detail executed beautifully."),
        ],
        "process": [("🎨", "Design & Planning", "Architectural design, permits and detailed project planning."), ("🏗️", "Construction Phase", "Expert tradespeople managed by our experienced site team."), ("🔑", "Handover", "Snagging complete, keys in hand and fully compliant sign-off.")],
        "trust": ["ISO Certified", "10-Year Structural Warranty", "NVOB Member", "Award-winning builds"],
    },
    "Home builder": {
        "primary": "#292524", "accent": "#d97706", "accent2": "#f59e0b",
        "icon": "🏡", "emoji_bg": "🏡",
        "tagline": "Building the Home\nYou've Always Dreamed Of",
        "hero_desc": "Expert home builders delivering quality craftsmanship across Amsterdam. We turn your vision into a home you'll love for generations.",
        "services": [
            ("🏡", "Custom New Builds", "Unique homes designed and built entirely around you."),
            ("🔝", "Extensions & Loft Conversions", "Add space and value to your existing home."),
            ("🔄", "Full Renovations", "Complete property transformations from top to bottom."),
            ("🍳", "Kitchen & Bathroom", "Stunning kitchen and bathroom installations."),
            ("📐", "Architectural Design", "In-house design service to visualise your dream home."),
        ],
        "testimonials": [
            ("New home owner", "Amsterdam", "Our dream home became reality. Incredible team to work with."),
            ("Homeowner", "Noord", "Extension transformed our house. Brilliant quality and value."),
            ("Renovation client", "Zuid", "Every detail was perfect. We couldn't be more delighted."),
        ],
        "process": [("💭", "Dream It", "Share your vision and we'll show you what's possible."), ("📐", "Design It", "Our architects produce detailed plans and 3D visualisations."), ("🏡", "Build It", "Skilled craftspeople bring your dream home to life.")],
        "trust": ["In-house Architects", "Fixed Contracts", "10-Year Guarantee", "Award-winning Homes"],
    },
    "Custom home builder": {
        "primary": "#292524", "accent": "#d97706", "accent2": "#f59e0b",
        "icon": "🏡", "emoji_bg": "🏡",
        "tagline": "Your Vision.\nOur Craftsmanship.",
        "hero_desc": "Bespoke home building tailored exactly to your needs, lifestyle and style. Every home we build is a one-of-a-kind masterpiece.",
        "services": [
            ("✏️", "Bespoke Design", "Unique architectural design created around your brief."),
            ("🏡", "Custom Builds", "Hand-crafted homes built to a standard you won't find elsewhere."),
            ("🔝", "Extensions", "Sensitive extensions that complement your existing home perfectly."),
            ("✨", "Interior Fit-out", "Bespoke interior finishes from floors to ceilings."),
            ("📋", "Project Management", "Complete management from planning consent to handover."),
        ],
        "testimonials": [
            ("Client", "Amsterdam Zuid", "Truly bespoke — they built exactly what we had in mind. Perfect."),
            ("Client", "Jordaan", "The craftsmanship is extraordinary. Our home is a work of art."),
            ("Client", "Noord", "Seamless process from start to finish. Exceptional team."),
        ],
        "process": [("💬", "Vision Workshop", "An in-depth session to understand exactly what you want."), ("🎨", "Design Development", "Full architectural drawings and material specifications."), ("🏡", "Masterful Build", "Expert craftspeople delivering your bespoke home on time.")],
        "trust": ["100% Bespoke", "3D Visualisations", "Fixed-price Builds", "5-Star Rated"],
    },
    "Landscaper": {
        "primary": "#052e16", "accent": "#22c55e", "accent2": "#4ade80",
        "icon": "🌿", "emoji_bg": "🌿",
        "tagline": "Beautiful Outdoor Spaces,\nExpertly Created",
        "hero_desc": "Professional landscaping and garden design across Amsterdam. We create stunning outdoor spaces that are as functional as they are beautiful.",
        "services": [
            ("✏️", "Garden Design", "Creative, practical garden design for every style and budget."),
            ("🌱", "Planting & Turfing", "Seasonal planting schemes and premium lawn installation."),
            ("🪨", "Paving & Decking", "Natural stone, porcelain and composite decking solutions."),
            ("💧", "Irrigation Systems", "Efficient watering systems to keep your garden thriving."),
            ("✂️", "Maintenance Plans", "Regular garden care to keep your outdoor space looking perfect."),
        ],
        "testimonials": [
            ("Homeowner", "Amsterdam", "Our garden is completely transformed. It's like a different house."),
            ("Restaurant owner", "Oost", "Our terrace is now our most popular feature. Brilliant work."),
            ("Client", "Zuid", "Professional, creative and the results are just stunning."),
        ],
        "process": [("🎨", "Design Concept", "We visit your space and produce a detailed design proposal."), ("🌱", "Installation", "Expert team installs your new garden to perfection."), ("✂️", "Ongoing Care", "Optional maintenance plans to keep it looking beautiful year-round.")],
        "trust": ["Award-winning Designs", "10-Year Plant Guarantee", "Fully Insured", "Free Design Visit"],
    },
    "House cleaning service": {
        "primary": "#0c1f3f", "accent": "#0ea5e9", "accent2": "#38bdf8",
        "icon": "🧹", "emoji_bg": "🧹",
        "tagline": "A Spotless Home,\nEvery Time",
        "hero_desc": "Professional domestic and commercial cleaning services across Amsterdam. Trusted, insured cleaners who treat your home as their own.",
        "services": [
            ("🧹", "Regular Cleaning", "Weekly, fortnightly or monthly domestic cleaning."),
            ("✨", "Deep Cleaning", "Thorough top-to-bottom deep cleans for any property."),
            ("🔑", "End-of-tenancy Cleaning", "Landlord-approved deep cleans to secure your deposit."),
            ("🏢", "Office Cleaning", "Professional workplace cleaning that impresses clients."),
            ("🪟", "Window Cleaning", "Streak-free interior and exterior window cleaning."),
        ],
        "testimonials": [
            ("Homeowner", "Amsterdam", "My house has never been this clean. Exceptional attention to detail."),
            ("Landlord", "Oost", "Used them for end-of-tenancy clean. Deposit returned in full."),
            ("Office manager", "Centrum", "Office looks immaculate every morning. Great team."),
        ],
        "process": [("📅", "Book Online", "Choose your cleaning type, date and time — takes 2 minutes."), ("🔑", "We Arrive & Clean", "Vetted, insured cleaners who bring all their own equipment."), ("✨", "Enjoy the Result", "Come home to a spotless, fresh-smelling property every time.")],
        "trust": ["DBS Checked", "Fully Insured", "Eco-friendly Products", "Satisfaction Guarantee"],
    },
    "Cleaning service": {
        "primary": "#0c1f3f", "accent": "#0ea5e9", "accent2": "#38bdf8",
        "icon": "✨", "emoji_bg": "✨",
        "tagline": "Clean Spaces.\nClear Minds.",
        "hero_desc": "Reliable cleaning services for homes and businesses across Amsterdam. We leave every space spotless, fresh and feeling brand new.",
        "services": [
            ("🏠", "Domestic Cleaning", "Regular home cleaning tailored to your schedule."),
            ("🏢", "Commercial Cleaning", "Professional cleaning for offices and commercial premises."),
            ("💎", "Deep Cleans", "Intensive cleaning for properties that need a thorough refresh."),
            ("🎨", "Graffiti Removal", "Fast, effective removal of graffiti from any surface."),
            ("🔬", "Specialist Cleaning", "Sensitive surface, post-build and biohazard cleaning."),
        ],
        "testimonials": [
            ("Business owner", "Amsterdam", "Reliable, thorough and always professional. Highly recommended."),
            ("Homeowner", "West", "The deep clean was transformative. Absolutely delighted."),
            ("Facilities manager", "Centrum", "Our offices are spotless every day. Excellent company."),
        ],
        "process": [("📞", "Get a Quote", "Tell us what you need and we'll give you a fast, fair price."), ("📅", "Book a Time", "We arrange a convenient time and send a confirmed team."), ("✨", "Spotless Results", "We clean to a high professional standard, guaranteed.")],
        "trust": ["Vetted Staff", "Eco Products", "Fully Insured", "Same-day Available"],
    },
    "Roofing contractor": {
        "primary": "#1c1917", "accent": "#dc2626", "accent2": "#ef4444",
        "icon": "🏠", "emoji_bg": "🏠",
        "tagline": "Protecting Your Home\nfrom the Top Down",
        "hero_desc": "Expert roofing installation, repair and maintenance across Amsterdam. We keep the elements out and your property safe.",
        "services": [
            ("🔨", "Roof Repairs", "Fast, reliable repairs to stop leaks and prevent damage."),
            ("🏠", "New Roof Installation", "Full roof replacements using premium materials."),
            ("⬛", "Flat Roofing", "EPDM, felt and GRP flat roof systems expertly installed."),
            ("🌧️", "Gutter Cleaning & Repair", "Clearing and repairing gutters to protect your property."),
            ("🔍", "Roof Inspections", "Thorough surveys with a full photographic report."),
        ],
        "testimonials": [
            ("Homeowner", "Amsterdam", "Fixed our persistent leak in a single visit. Excellent work."),
            ("Landlord", "Noord", "Replaced three roofs for us. Professional, fast and great value."),
            ("Property manager", "Zuid", "Reliable and responsive. Our first call for any roof issue."),
        ],
        "process": [("🔍", "Free Inspection", "We inspect your roof and provide a full written assessment."), ("📋", "Transparent Quote", "Detailed quote with no hidden costs or nasty surprises."), ("🏠", "Expert Repair", "Skilled roofers complete the work safely and efficiently.")],
        "trust": ["Free Roof Survey", "10-Year Guarantee", "Emergency Cover", "Fully Insured"],
    },
    "Plasterer": {
        "primary": "#1c1917", "accent": "#ca8a04", "accent2": "#eab308",
        "icon": "🪣", "emoji_bg": "🪣",
        "tagline": "Flawless Walls.\nPerfect Finishes.",
        "hero_desc": "Expert plastering and skimming for homes and businesses across Amsterdam. Smooth, perfect surfaces every time — ready to paint in days.",
        "services": [
            ("🪣", "Skimming & Plastering", "Silky-smooth skim coats on walls and ceilings."),
            ("🏠", "Render & External Finishes", "Durable, attractive external render systems."),
            ("✨", "Decorative Plasterwork", "Coving, cornicing and ornamental plaster features."),
            ("🧱", "Dry Lining", "Efficient plasterboard installation and finishing."),
            ("🔧", "Patch & Repair", "Invisible repairs to damaged plaster surfaces."),
        ],
        "testimonials": [
            ("Homeowner", "Amsterdam", "Walls are absolutely perfect. You'd never know they were damaged."),
            ("Interior designer", "De Pijp", "Best plasterer I've worked with. Immaculate finish every time."),
            ("Builder", "Noord", "My go-to plasterer. Fast, clean and consistently excellent."),
        ],
        "process": [("📋", "Free Assessment", "We assess the work needed and provide a competitive quote."), ("🛡️", "Surface Prep", "Thorough preparation to ensure the perfect bond and finish."), ("✨", "Flawless Result", "Smooth, paint-ready surfaces delivered on time.")],
        "trust": ["Dust-free Techniques", "Premium Materials", "Same-day Drying Possible", "Fully Insured"],
    },
    "Stucco contractor": {
        "primary": "#1c1917", "accent": "#ca8a04", "accent2": "#eab308",
        "icon": "🪣", "emoji_bg": "🪣",
        "tagline": "Smooth Finishes.\nExceptional Quality.",
        "hero_desc": "Professional stucco and plastering contractors serving Amsterdam. Perfect walls and ceilings, every job, every time.",
        "services": [
            ("🏠", "Interior Plastering", "Premium interior plaster finishes for any room."),
            ("🏛️", "External Render", "Weather-resistant external render for a beautiful facade."),
            ("✨", "Ornamental Stucco", "Decorative plasterwork to add character and elegance."),
            ("🔧", "Repair & Restoration", "Sympathetic repairs to historic and damaged plaster."),
            ("🧱", "Dry Lining", "Fast, clean plasterboard installation and taping."),
        ],
        "testimonials": [
            ("Home owner", "Amsterdam", "Flawless stucco work — the house looks completely transformed."),
            ("Interior architect", "Centrum", "Consistently the best plaster finish I've ever seen. Brilliant."),
            ("Renovator", "West", "On time, on budget and absolutely immaculate workmanship."),
        ],
        "process": [("🔍", "Site Survey", "We assess your walls and recommend the best finish."), ("📋", "Fixed Quote", "A detailed quote with no unexpected extras."), ("✨", "Perfect Finish", "Smooth, beautiful results completed to schedule.")],
        "trust": ["All Finish Types", "Eco-friendly Mixes", "Rapid Drying", "5-Year Warranty"],
    },
    "Import export company": {
        "primary": "#0c2340", "accent": "#06b6d4", "accent2": "#22d3ee",
        "icon": "🌍", "emoji_bg": "🌍",
        "tagline": "Global Trade.\nLocal Expertise.",
        "hero_desc": "Connecting Amsterdam businesses to global markets through reliable, efficient import and export services. Your gateway to the world.",
        "services": [
            ("🚢", "Import & Export Logistics", "End-to-end handling of international trade shipments."),
            ("📋", "Customs Clearance", "Expert customs documentation and duty management."),
            ("⚖️", "Trade Compliance", "Ensuring full compliance with all international regulations."),
            ("🏭", "Warehousing", "Secure Amsterdam warehousing for import and export goods."),
            ("🔗", "Supply Chain Consulting", "Optimising your international supply chain for cost and speed."),
        ],
        "testimonials": [
            ("Import director", "Amsterdam", "Handles our customs brilliantly. Zero delays, zero stress."),
            ("Exporter", "Schiphol", "Opened up new markets for us. Invaluable expertise and support."),
            ("SME owner", "Noord", "Made international trade accessible for our small business. Excellent."),
        ],
        "process": [("💬", "Trade Consultation", "We assess your import or export requirements in detail."), ("📋", "Full Documentation", "We prepare and manage all required trade documentation."), ("🌍", "Seamless Delivery", "Your goods move across borders smoothly and on schedule.")],
        "trust": ["EU Trade Specialists", "Customs Certified", "Cargo Insurance", "Global Network"],
    },
    "Video production service": {
        "primary": "#0c0a09", "accent": "#e11d48", "accent2": "#f43f5e",
        "icon": "🎬", "emoji_bg": "🎬",
        "tagline": "Your Story.\nBeautifully Told.",
        "hero_desc": "Professional video production for brands, events and content creators in Amsterdam. We create video that moves, inspires and converts.",
        "services": [
            ("🏢", "Brand Films", "Cinematic brand stories that define and elevate your identity."),
            ("🎉", "Event Videography", "Full event coverage from highlights to full documentation."),
            ("📱", "Social Media Content", "Platform-optimised short-form video that stops the scroll."),
            ("💼", "Corporate Video", "Training, recruitment and internal communication video."),
            ("🎬", "Post-production & Editing", "Expert editing, colour grading, motion graphics and sound."),
        ],
        "testimonials": [
            ("Marketing Director", "Amsterdam", "Our brand film generated 500k views in the first week. Exceptional."),
            ("Event organiser", "Centrum", "Beautiful coverage of our conference. Client is absolutely thrilled."),
            ("Startup founder", "Noord", "Our social content has never performed better. Great team."),
        ],
        "process": [("💡", "Creative Development", "Script, storyboard and shot list developed with your team."), ("🎬", "Professional Shoot", "Cinematic production using broadcast-quality equipment."), ("✨", "Post-production", "Edit, grade, sound and delivery across all required formats.")],
        "trust": ["4K & Drone Available", "Fast Turnaround", "Commercial Licensing", "Award-winning Team"],
    },
    "Art studio": {
        "primary": "#0f0f1a", "accent": "#ec4899", "accent2": "#f472b6",
        "icon": "🖌️", "emoji_bg": "🖌️",
        "tagline": "Where Creativity\nComes to Life",
        "hero_desc": "A vibrant, inspiring creative studio in Amsterdam offering classes, workshops and bespoke commissions for all ages and skill levels.",
        "services": [
            ("🎨", "Art Classes", "Weekly classes in painting, drawing, sculpture and more."),
            ("🖼️", "Private Commissions", "Bespoke original artwork created to your brief."),
            ("🎉", "Workshop Events", "Fun, social workshops perfect for teams and celebrations."),
            ("🏢", "Studio Hire", "Hire our fully equipped studio space for your own projects."),
            ("🛒", "Art Supplies", "Quality materials available to purchase in-studio."),
        ],
        "testimonials": [
            ("Student", "Amsterdam", "Best art class I've ever taken. Inspiring and so much fun."),
            ("Corporate client", "Centrum", "Team workshop was brilliant — everyone loved it."),
            ("Art collector", "Zuid", "My commissioned piece is absolutely stunning. A true talent."),
        ],
        "process": [("👋", "Join a Class", "Browse our schedule and book a session that suits you."), ("🎨", "Create & Learn", "Expert tuition in a relaxed, inspiring atmosphere."), ("🖼️", "Take Home Your Art", "Leave with a finished piece and new skills to build on.")],
        "trust": ["All Skill Levels", "Professional Materials", "Small Groups", "Private Events Available"],
    },
    "Website designer": {
        "primary": "#0f0f23", "accent": "#7c3aed", "accent2": "#8b5cf6",
        "icon": "💻", "emoji_bg": "💻",
        "tagline": "Websites That Work\nas Hard as You Do",
        "hero_desc": "Creative web design and development for businesses that want to grow. We build websites that look incredible and convert visitors into customers.",
        "services": [
            ("🎨", "Website Design", "Bespoke, responsive websites that reflect your brand perfectly."),
            ("🛒", "E-commerce Development", "Powerful online stores that drive sales 24/7."),
            ("📈", "SEO & Performance", "Optimised sites that rank on Google and load instantly."),
            ("✏️", "Branding & Identity", "Logo, colours and brand guidelines from scratch."),
            ("🛡️", "Hosting & Maintenance", "Secure, fast hosting and ongoing site management."),
        ],
        "testimonials": [
            ("Business owner", "Amsterdam", "Our new website generated 3x more leads in the first month."),
            ("E-commerce manager", "Noord", "Online sales up 80% since the redesign. Incredible result."),
            ("Startup founder", "Centrum", "Beautiful design, fast build, exceptional value. Highly recommend."),
        ],
        "process": [("💬", "Discovery Call", "We learn about your business, goals and target audience."), ("🎨", "Design & Build", "Stunning designs approved by you before a line of code is written."), ("🚀", "Launch & Grow", "We launch your site and support your growth with ongoing optimisation.")],
        "trust": ["Mobile-first Design", "Google-ready SEO", "Fast 48h Turnaround", "Unlimited Revisions"],
    },
    "Handyman/Handywoman/Handyperson": {
        "primary": "#1c1917", "accent": "#f59e0b", "accent2": "#fbbf24",
        "icon": "🔨", "emoji_bg": "🔨",
        "tagline": "No Job Too Small.\nQuality Every Time.",
        "hero_desc": "Your trusted local handyman for repairs, maintenance and small renovations across Amsterdam. Fast, reliable and always done right.",
        "services": [
            ("🔧", "General Repairs", "All household repairs handled quickly and professionally."),
            ("📦", "Flat-pack Assembly", "All brands assembled correctly, first time, every time."),
            ("🪟", "Tiling & Grouting", "Precise tiling for kitchens, bathrooms and more."),
            ("🚪", "Door & Lock Fitting", "Doors adjusted, locks changed and handles fitted."),
            ("🎨", "Painting & Decorating", "Neat, professional interior painting and decorating."),
        ],
        "testimonials": [
            ("Homeowner", "Amsterdam", "Fixed 10 jobs in one visit. Fast, friendly and great value."),
            ("Landlord", "Oost", "Reliable, goes above and beyond. My first call for any job."),
            ("Tenant", "West", "Sorted my flat-pack nightmare in under an hour. Brilliant."),
        ],
        "process": [("📞", "Tell Us the Job", "Call or message with your list — we price it quickly."), ("📅", "Book a Time", "Flexible appointments including evenings and weekends."), ("✅", "Job Done Right", "Professional workmanship, clean up included, every time.")],
        "trust": ["No Job Too Small", "Same-week Appointments", "Fully Insured", "Fixed Hourly Rate"],
    },
    "Taxi service": {
        "primary": "#0f172a", "accent": "#fbbf24", "accent2": "#fde047",
        "icon": "🚕", "emoji_bg": "🚕",
        "tagline": "Your Ride,\nOn Your Terms",
        "hero_desc": "Professional, comfortable taxi and transport services across Amsterdam. Punctual, clean and competitively priced — book in seconds.",
        "services": [
            ("✈️", "Airport Transfers", "Stress-free transfers to Schiphol and beyond."),
            ("🏙️", "City Rides", "Fast, safe rides anywhere in Amsterdam."),
            ("💼", "Business Accounts", "Priority service and monthly invoicing for corporate clients."),
            ("🎉", "Event Transport", "Dedicated vehicles for events, parties and group travel."),
            ("🛣️", "Long-distance", "Comfortable intercity and cross-border journeys."),
        ],
        "testimonials": [
            ("Regular client", "Amsterdam", "Always on time, always spotlessly clean. My trusted driver."),
            ("Business traveller", "Centrum", "Reliable and professional — makes every trip effortless."),
            ("Event organiser", "Noord", "Coordinated 20 guests perfectly. Seamless service throughout."),
        ],
        "process": [("📱", "Book in Seconds", "Call, WhatsApp or use our app to book instantly."), ("🚕", "Driver Dispatched", "We confirm your driver and send an ETA immediately."), ("✅", "Arrive in Comfort", "Sit back, relax and arrive on time, every time.")],
        "trust": ["Licensed & Insured", "Fixed Fares", "24/7 Available", "English Spoken"],
    },
    "Mailing service": {
        "primary": "#0c2340", "accent": "#3b82f6", "accent2": "#60a5fa",
        "icon": "✉️", "emoji_bg": "✉️",
        "tagline": "Your Mail\nin Safe Hands",
        "hero_desc": "Professional mailing and postal services for businesses and individuals across Amsterdam. Reliable, discreet and always delivered.",
        "services": [
            ("📦", "Parcel Handling", "Safe receipt, storage and forwarding of parcels."),
            ("📬", "PO Box Services", "Professional business address with secure mail handling."),
            ("📄", "Document Scanning", "Digital archiving of all incoming correspondence."),
            ("🌍", "Mail Forwarding", "Domestic and international mail forwarding services."),
            ("🏢", "Business Post", "Franking, bulk mailing and business postal solutions."),
        ],
        "testimonials": [
            ("Business owner", "Amsterdam", "Professional registered address and seamless mail handling."),
            ("Expat", "Centrum", "Perfect solution for managing my post while abroad. Brilliant service."),
            ("SME owner", "Noord", "Reliable, discreet and great value for our business address needs."),
        ],
        "process": [("📋", "Set Up Your Account", "Quick registration with same-day activation."), ("📬", "Receive Your Mail", "We receive, sort and notify you of all incoming items."), ("✅", "Access Anywhere", "Collect in person, get it scanned or have it forwarded worldwide.")],
        "trust": ["Registered Address Service", "Secure Handling", "Same-day Notification", "GDPR Compliant"],
    },
    "Garden building supplier": {
        "primary": "#052e16", "accent": "#22c55e", "accent2": "#4ade80",
        "icon": "🌱", "emoji_bg": "🌱",
        "tagline": "Everything You Need\nfor the Perfect Garden",
        "hero_desc": "Quality garden buildings, timber, tools and supplies for Amsterdam's outdoor spaces. Transform your garden with our expert products and advice.",
        "services": [
            ("🏠", "Garden Sheds & Cabins", "Quality wooden and metal garden buildings for every need."),
            ("🪵", "Decking & Timber", "Premium decking timber, posts and accessories."),
            ("🚧", "Fencing & Gates", "Durable fencing panels, posts and garden gates."),
            ("🪑", "Garden Furniture", "Stylish, weather-resistant outdoor furniture."),
            ("🔧", "Tools & Accessories", "Professional-grade tools and gardening accessories."),
        ],
        "testimonials": [
            ("Garden enthusiast", "Amsterdam", "Best range and great prices. My go-to for all garden projects."),
            ("Landscaper", "Noord", "Reliable supplier with quality timber and fast delivery."),
            ("Homeowner", "Zuid", "Our new garden cabin is perfect. Great advice from the team."),
        ],
        "process": [("💬", "Expert Advice", "Tell us your project and we'll recommend the right products."), ("🛒", "Browse & Order", "Order in-store or online with fast Amsterdam delivery."), ("🏡", "Build & Enjoy", "Quality products delivered to your door, ready to install.")],
        "trust": ["Quality Guaranteed", "Fast Local Delivery", "Expert Advice", "Sustainable Materials"],
    },
}

DEFAULT_CONFIG = {
    "primary": "#0f172a", "accent": "#6366f1", "accent2": "#818cf8",
    "icon": "⭐", "emoji_bg": "⭐",
    "tagline": "Professional Services\nin Amsterdam",
    "hero_desc": "Trusted local professionals delivering quality services across Amsterdam. Experienced, reliable and dedicated to your satisfaction.",
    "services": [
        ("✅", "Professional Services", "Expert service delivered to the highest standard."),
        ("🏆", "Quality Guaranteed", "We stand behind every job we do."),
        ("📍", "Local Expertise", "Deep knowledge of Amsterdam and its unique needs."),
        ("💰", "Competitive Rates", "Fair, transparent pricing with no hidden costs."),
        ("💬", "Free Consultation", "Talk to us first — no obligation, no pressure."),
    ],
    "testimonials": [
        ("Client", "Amsterdam", "Excellent service from start to finish. Highly recommended."),
        ("Customer", "Noord", "Professional, punctual and great value. Would use again."),
        ("Client", "Zuid", "Friendly, skilled and reliable. Very happy with the result."),
    ],
    "process": [("📞", "Get in Touch", "Contact us to discuss your needs — we respond fast."), ("📋", "Receive Your Quote", "A clear, competitive quote with no hidden extras."), ("✅", "Job Done Right", "We deliver quality work and ensure you're 100% satisfied.")],
    "trust": ["Fully Insured", "Free Consultation", "Satisfaction Guaranteed", "Amsterdam Based"],
}


def slugify(name):
    name = name.lower()
    name = re.sub(r'[^\w\s-]', '', name)
    name = re.sub(r'[\s_]+', '-', name)
    name = re.sub(r'-+', '-', name).strip('-')
    return name[:80]


def get_config(categories):
    for cat in categories:
        if cat in CATEGORY_CONFIG:
            return CATEGORY_CONFIG[cat]
    return DEFAULT_CONFIG


def initials(name):
    words = name.strip().split()
    if len(words) >= 2:
        return (words[0][0] + words[1][0]).upper()
    return name[:2].upper()


def stars_html(score):
    if not score:
        return ""
    try:
        s = float(score)
    except ValueError:
        return ""
    filled = int(round(s))
    empty = 5 - filled
    return "★" * filled + "☆" * empty


def generate_html(company):
    name = (company.get("title") or company.get("﻿title") or "").strip()
    if not name or name in (".", "Z", ""):
        return None

    cats = [company.get(f"categories/{i}", "").strip() for i in range(9)]
    cats = [c for c in cats if c]
    primary_cat = cats[0] if cats else ""

    if primary_cat in SKIP_CATEGORIES:
        return None

    cfg = get_config(cats)
    street = company.get("street", "").strip()
    city = (company.get("city", "") or "Amsterdam").strip() or "Amsterdam"
    phone = company.get("phone", "").strip()
    score = company.get("totalScore", "").strip()
    reviews = company.get("reviewsCount", "").strip()
    maps_url = company.get("url", "").strip()

    primary = cfg["primary"]
    accent = cfg["accent"]
    accent2 = cfg.get("accent2", accent)
    icon = cfg["icon"]
    tagline_raw = cfg["tagline"]
    tagline_parts = tagline_raw.split("\n")
    tagline_line1 = html_lib.escape(tagline_parts[0])
    tagline_line2 = html_lib.escape(tagline_parts[1]) if len(tagline_parts) > 1 else ""
    hero_desc = cfg["hero_desc"]
    services = cfg["services"]
    testimonials = cfg.get("testimonials", DEFAULT_CONFIG["testimonials"])
    process = cfg.get("process", DEFAULT_CONFIG["process"])
    trust = cfg.get("trust", DEFAULT_CONFIG["trust"])

    monogram = initials(name)
    address_parts = [p for p in [street, city, "Netherlands"] if p]
    address = ", ".join(address_parts)
    cat_label = primary_cat if primary_cat else "Professional Services"

    # Services HTML
    services_html = ""
    for svc_icon, svc_name, svc_desc in services:
        services_html += f"""
        <div class="svc-card">
          <div class="svc-icon">{svc_icon}</div>
          <h3>{html_lib.escape(svc_name)}</h3>
          <p>{html_lib.escape(svc_desc)}</p>
        </div>"""

    # Testimonials HTML
    testi_html = ""
    for tname, tloc, ttext in testimonials:
        tini = initials(tname)
        testi_html += f"""
        <div class="testi-card">
          <div class="testi-stars">★★★★★</div>
          <p class="testi-text">"{html_lib.escape(ttext)}"</p>
          <div class="testi-author">
            <div class="testi-avatar">{html_lib.escape(tini)}</div>
            <div><strong>{html_lib.escape(tname)}</strong><br><span>{html_lib.escape(tloc)}</span></div>
          </div>
        </div>"""

    # Process HTML
    process_html = ""
    for i, (step_icon, step_title, step_desc) in enumerate(process, 1):
        process_html += f"""
        <div class="step">
          <div class="step-num">{i:02d}</div>
          <div class="step-icon">{step_icon}</div>
          <h3>{html_lib.escape(step_title)}</h3>
          <p>{html_lib.escape(step_desc)}</p>
        </div>"""

    # Trust badges
    trust_html = "".join(f'<div class="trust-badge"><span class="trust-check">✓</span>{html_lib.escape(t)}</div>' for t in trust)

    # Rating
    rating_html = ""
    if score and reviews:
        rating_html = f"""<div class="hero-rating">
          <span class="hero-stars">{stars_html(score)}</span>
          <span>{score} out of 5 &nbsp;·&nbsp; {reviews} reviews on Google</span>
        </div>"""

    phone_display = phone if phone else ""
    maps_btn = f'<a href="{html_lib.escape(maps_url)}" target="_blank" class="btn-outline">📍 View on Google Maps</a>' if maps_url else ""
    phone_btn = f'<a href="tel:{html_lib.escape(phone)}" class="btn-primary">📞 {html_lib.escape(phone)}</a>' if phone else '<span class="btn-primary">Get in Touch</span>'

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{html_lib.escape(name)} | {html_lib.escape(cat_label)} Amsterdam</title>
<meta name="description" content="{html_lib.escape(name)} — {html_lib.escape(hero_desc[:150])}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
<style>
*,*::before,*::after{{box-sizing:border-box;margin:0;padding:0}}
:root{{
  --primary:{primary};
  --accent:{accent};
  --accent2:{accent2};
  --bg:#f8f8f6;
  --card:#ffffff;
  --text:#111111;
  --muted:#6b7280;
  --border:#e5e7eb;
  --radius:16px;
}}
html{{scroll-behavior:smooth}}
body{{font-family:'Inter',system-ui,sans-serif;background:var(--bg);color:var(--text);line-height:1.6;-webkit-font-smoothing:antialiased}}

/* ── NAV ── */
.nav{{
  position:fixed;top:0;left:0;right:0;z-index:200;
  display:flex;align-items:center;justify-content:space-between;
  padding:0 6%;height:68px;
  background:rgba(255,255,255,0.92);backdrop-filter:blur(16px);
  border-bottom:1px solid rgba(0,0,0,0.06);
  transition:box-shadow 0.3s;
}}
.nav.scrolled{{box-shadow:0 4px 24px rgba(0,0,0,0.08)}}
.nav-logo{{display:flex;align-items:center;gap:12px;text-decoration:none}}
.nav-monogram{{
  width:38px;height:38px;border-radius:10px;
  background:linear-gradient(135deg,var(--accent),var(--accent2));
  color:#fff;font-weight:800;font-size:0.85rem;
  display:flex;align-items:center;justify-content:center;letter-spacing:0.5px;
  flex-shrink:0;
}}
.nav-name{{font-weight:700;font-size:0.95rem;color:var(--text);line-height:1.2;max-width:220px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}}
.nav-cat{{font-size:0.72rem;color:var(--muted);font-weight:500;display:block}}
.nav-cta{{
  background:var(--accent);color:#fff;
  padding:10px 22px;border-radius:8px;font-size:0.875rem;font-weight:700;
  text-decoration:none;transition:opacity 0.2s,transform 0.15s;white-space:nowrap;
}}
.nav-cta:hover{{opacity:0.9;transform:translateY(-1px)}}

/* ── HERO ── */
.hero{{
  min-height:100vh;
  background:var(--primary);
  position:relative;overflow:hidden;
  display:flex;flex-direction:column;align-items:center;justify-content:center;
  text-align:center;padding:100px 6% 80px;
}}
.hero-glow{{
  position:absolute;inset:0;pointer-events:none;
  background:
    radial-gradient(ellipse 70% 55% at 20% 20%,color-mix(in srgb,var(--accent) 18%,transparent),transparent),
    radial-gradient(ellipse 60% 50% at 80% 80%,color-mix(in srgb,var(--accent2) 12%,transparent),transparent);
}}
.hero-grid{{
  position:absolute;inset:0;opacity:0.04;pointer-events:none;
  background-image:linear-gradient(rgba(255,255,255,0.8) 1px,transparent 1px),
                   linear-gradient(90deg,rgba(255,255,255,0.8) 1px,transparent 1px);
  background-size:40px 40px;
}}
.hero-content{{position:relative;max-width:780px;}}
.hero-pill{{
  display:inline-flex;align-items:center;gap:8px;
  background:color-mix(in srgb,var(--accent) 18%,transparent);
  border:1px solid color-mix(in srgb,var(--accent) 35%,transparent);
  color:color-mix(in srgb,var(--accent) 90%,#fff);
  border-radius:999px;padding:6px 18px;
  font-size:0.78rem;font-weight:700;letter-spacing:1.2px;text-transform:uppercase;
  margin-bottom:28px;
}}
.hero-pill-dot{{width:7px;height:7px;border-radius:50%;background:var(--accent);animation:pulse 2s infinite}}
@keyframes pulse{{0%,100%{{opacity:1}}50%{{opacity:0.4}}}}
.hero h1{{
  font-size:clamp(2.6rem,6vw,4.2rem);font-weight:900;
  color:#fff;line-height:1.05;letter-spacing:-1.5px;
  margin-bottom:8px;
}}
.hero h1 em{{font-style:normal;color:var(--accent)}}
.hero-sub{{
  font-size:clamp(1rem,2.2vw,1.25rem);color:rgba(255,255,255,0.65);
  max-width:580px;margin:0 auto 36px;line-height:1.7;font-weight:400;
}}
.hero-rating{{
  display:inline-flex;align-items:center;gap:10px;
  background:rgba(255,255,255,0.08);border:1px solid rgba(255,255,255,0.15);
  border-radius:999px;padding:8px 20px;
  color:rgba(255,255,255,0.8);font-size:0.875rem;margin-bottom:32px;
}}
.hero-stars{{color:var(--accent);letter-spacing:2px;font-size:1rem}}
.hero-actions{{display:flex;gap:14px;flex-wrap:wrap;justify-content:center}}
.btn-primary{{
  background:linear-gradient(135deg,var(--accent),var(--accent2));
  color:#fff;padding:15px 36px;border-radius:10px;font-size:1rem;font-weight:700;
  text-decoration:none;border:none;cursor:pointer;
  box-shadow:0 4px 24px color-mix(in srgb,var(--accent) 45%,transparent);
  transition:transform 0.15s,box-shadow 0.15s;display:inline-block;
}}
.btn-primary:hover{{transform:translateY(-2px);box-shadow:0 8px 32px color-mix(in srgb,var(--accent) 55%,transparent)}}
.btn-ghost{{
  color:#fff;padding:15px 36px;border-radius:10px;font-size:1rem;font-weight:600;
  text-decoration:none;border:2px solid rgba(255,255,255,0.3);
  transition:border-color 0.2s,background 0.2s;display:inline-block;
}}
.btn-ghost:hover{{border-color:rgba(255,255,255,0.7);background:rgba(255,255,255,0.06)}}

/* ── TRUST BAR ── */
.trust-bar{{
  background:#fff;border-bottom:1px solid var(--border);
  padding:18px 6%;display:flex;align-items:center;justify-content:center;
  gap:32px;flex-wrap:wrap;
}}
.trust-badge{{
  display:flex;align-items:center;gap:8px;
  font-size:0.82rem;font-weight:600;color:#374151;
}}
.trust-check{{
  width:22px;height:22px;border-radius:50%;
  background:color-mix(in srgb,var(--accent) 15%,transparent);
  color:var(--accent);font-size:0.7rem;font-weight:800;
  display:flex;align-items:center;justify-content:center;flex-shrink:0;
}}

/* ── SECTIONS ── */
.section{{padding:96px 6%;max-width:1200px;margin:0 auto}}
.section-tag{{
  display:inline-block;
  color:var(--accent);font-size:0.75rem;font-weight:700;
  letter-spacing:2px;text-transform:uppercase;margin-bottom:14px;
}}
.section-title{{font-size:clamp(1.9rem,4vw,2.8rem);font-weight:800;letter-spacing:-0.5px;line-height:1.15;}}
.section-title span{{color:var(--accent)}}
.section-lead{{color:var(--muted);font-size:1.05rem;line-height:1.75;margin-top:16px;max-width:580px;}}

/* ── SERVICES ── */
.svc-grid{{
  display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));
  gap:20px;margin-top:48px;
}}
.svc-card{{
  background:var(--card);border-radius:var(--radius);padding:28px 24px;
  border:1px solid var(--border);
  transition:transform 0.2s,box-shadow 0.2s,border-color 0.2s;
}}
.svc-card:hover{{transform:translateY(-4px);box-shadow:0 12px 40px rgba(0,0,0,0.09);border-color:var(--accent)}}
.svc-icon{{
  font-size:1.8rem;margin-bottom:14px;
  display:inline-flex;align-items:center;justify-content:center;
  width:52px;height:52px;border-radius:12px;
  background:color-mix(in srgb,var(--accent) 12%,transparent);
}}
.svc-card h3{{font-size:1rem;font-weight:700;margin-bottom:8px;}}
.svc-card p{{font-size:0.875rem;color:var(--muted);line-height:1.6;}}

/* ── PROCESS ── */
.process-section{{background:var(--primary);padding:96px 6%;}}
.process-inner{{max-width:1200px;margin:0 auto;}}
.process-grid{{
  display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));
  gap:32px;margin-top:56px;
}}
.step{{position:relative;}}
.step-num{{
  font-size:3rem;font-weight:900;
  color:rgba(255,255,255,0.06);
  line-height:1;margin-bottom:-8px;
  font-variant-numeric:tabular-nums;
}}
.step-icon{{
  font-size:1.6rem;margin-bottom:14px;
  width:52px;height:52px;border-radius:14px;
  background:color-mix(in srgb,var(--accent) 20%,transparent);
  border:1px solid color-mix(in srgb,var(--accent) 35%,transparent);
  display:flex;align-items:center;justify-content:center;
}}
.step h3{{font-size:1.05rem;font-weight:700;color:#fff;margin-bottom:10px;}}
.step p{{font-size:0.875rem;color:rgba(255,255,255,0.55);line-height:1.65;}}
.process-section .section-tag{{color:var(--accent);}}
.process-section .section-title{{color:#fff;}}

/* ── TESTIMONIALS ── */
.testi-grid{{
  display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));
  gap:20px;margin-top:48px;
}}
.testi-card{{
  background:var(--card);border-radius:var(--radius);padding:28px;
  border:1px solid var(--border);
}}
.testi-stars{{color:var(--accent);letter-spacing:2px;font-size:1.1rem;margin-bottom:14px;}}
.testi-text{{font-size:0.95rem;line-height:1.75;color:#374151;margin-bottom:20px;font-style:italic;}}
.testi-author{{display:flex;align-items:center;gap:12px;}}
.testi-avatar{{
  width:40px;height:40px;border-radius:50%;
  background:linear-gradient(135deg,var(--accent),var(--accent2));
  color:#fff;font-weight:700;font-size:0.85rem;
  display:flex;align-items:center;justify-content:center;flex-shrink:0;
}}
.testi-author strong{{font-size:0.9rem;display:block;}}
.testi-author span{{font-size:0.78rem;color:var(--muted);}}

/* ── CONTACT ── */
.contact-section{{
  background:linear-gradient(135deg,var(--primary),color-mix(in srgb,var(--primary) 80%,#000));
  padding:96px 6%;
}}
.contact-inner{{
  max-width:1100px;margin:0 auto;
  display:grid;grid-template-columns:1fr 1fr;gap:64px;align-items:center;
}}
.contact-info .section-title{{color:#fff}}
.contact-info .section-tag{{color:var(--accent)}}
.contact-lead{{color:rgba(255,255,255,0.65);margin:16px 0 32px;font-size:1.05rem;line-height:1.75;}}
.contact-detail{{
  display:flex;align-items:flex-start;gap:14px;
  background:rgba(255,255,255,0.06);border:1px solid rgba(255,255,255,0.1);
  border-radius:12px;padding:16px 20px;margin-bottom:14px;color:#fff;
}}
.contact-detail-icon{{font-size:1.3rem;flex-shrink:0;margin-top:1px;}}
.contact-detail-label{{font-size:0.72rem;color:rgba(255,255,255,0.5);font-weight:600;text-transform:uppercase;letter-spacing:0.8px;}}
.contact-detail-value{{font-size:0.95rem;font-weight:600;margin-top:2px;}}
.contact-btns{{display:flex;gap:12px;flex-wrap:wrap;margin-top:28px;}}
.btn-outline{{
  color:#fff;padding:13px 28px;border-radius:10px;font-size:0.9rem;font-weight:600;
  text-decoration:none;border:2px solid rgba(255,255,255,0.3);
  transition:border-color 0.2s;display:inline-block;
}}
.btn-outline:hover{{border-color:rgba(255,255,255,0.7)}}
.contact-card{{
  background:rgba(255,255,255,0.06);
  border:1px solid rgba(255,255,255,0.12);
  border-radius:24px;padding:48px 36px;text-align:center;
}}
.contact-monogram{{
  width:80px;height:80px;border-radius:20px;
  background:linear-gradient(135deg,var(--accent),var(--accent2));
  color:#fff;font-weight:800;font-size:1.8rem;
  display:flex;align-items:center;justify-content:center;
  margin:0 auto 20px;letter-spacing:1px;
}}
.contact-card-name{{color:#fff;font-size:1.3rem;font-weight:700;margin-bottom:6px;}}
.contact-card-cat{{color:rgba(255,255,255,0.5);font-size:0.85rem;margin-bottom:20px;}}
.contact-card-desc{{color:rgba(255,255,255,0.6);font-size:0.875rem;line-height:1.7;}}

/* ── FOOTER ── */
footer{{
  background:#0a0a0a;padding:32px 6%;
  display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:16px;
}}
.footer-brand{{display:flex;align-items:center;gap:10px;}}
.footer-monogram{{
  width:32px;height:32px;border-radius:8px;
  background:linear-gradient(135deg,var(--accent),var(--accent2));
  color:#fff;font-weight:800;font-size:0.75rem;
  display:flex;align-items:center;justify-content:center;
}}
.footer-name{{color:rgba(255,255,255,0.7);font-size:0.875rem;font-weight:600;}}
.footer-meta{{color:rgba(255,255,255,0.35);font-size:0.8rem;}}

/* ── ANIMATIONS ── */
.reveal{{opacity:0;transform:translateY(28px);transition:opacity 0.6s ease,transform 0.6s ease;}}
.reveal.visible{{opacity:1;transform:none;}}

@media(max-width:768px){{
  .contact-inner{{grid-template-columns:1fr;gap:40px;}}
  .contact-card{{display:none;}}
  .nav-cta{{display:none;}}
  .trust-bar{{gap:16px;}}
  footer{{flex-direction:column;text-align:center;}}
}}
</style>
</head>
<body>

<!-- NAV -->
<nav class="nav" id="nav">
  <a href="#" class="nav-logo">
    <div class="nav-monogram">{html_lib.escape(monogram)}</div>
    <div>
      <div class="nav-name">{html_lib.escape(name)}</div>
      <span class="nav-cat">{html_lib.escape(cat_label)} · Amsterdam</span>
    </div>
  </a>
  <a href="#contact" class="nav-cta">Get a Free Quote</a>
</nav>

<!-- HERO -->
<section class="hero">
  <div class="hero-glow"></div>
  <div class="hero-grid"></div>
  <div class="hero-content">
    <div class="hero-pill">
      <span class="hero-pill-dot"></span>
      {html_lib.escape(icon)} {html_lib.escape(cat_label)} · Amsterdam
    </div>
    <h1>{tagline_line1}<br><em>{tagline_line2}</em></h1>
    <p class="hero-sub">{html_lib.escape(hero_desc)}</p>
    {rating_html}
    <div class="hero-actions">
      <a href="#contact" class="btn-primary">Get a Free Quote</a>
      <a href="#services" class="btn-ghost">See Our Services</a>
    </div>
  </div>
</section>

<!-- TRUST BAR -->
<div class="trust-bar">
  {trust_html}
</div>

<!-- SERVICES -->
<div class="section reveal" id="services">
  <p class="section-tag">What We Do</p>
  <h2 class="section-title">Our <span>Services</span></h2>
  <p class="section-lead">{html_lib.escape(hero_desc)}</p>
  <div class="svc-grid">
    {services_html}
  </div>
</div>

<!-- PROCESS -->
<div class="process-section">
  <div class="process-inner reveal">
    <p class="section-tag">How It Works</p>
    <h2 class="section-title" style="color:#fff;">Simple. <span>Straightforward.</span> Sorted.</h2>
    <div class="process-grid">
      {process_html}
    </div>
  </div>
</div>

<!-- TESTIMONIALS -->
<div class="section reveal">
  <p class="section-tag">What Clients Say</p>
  <h2 class="section-title">Trusted by <span>Amsterdam</span></h2>
  <p class="section-lead">Don't just take our word for it — here's what our customers say about working with us.</p>
  <div class="testi-grid">
    {testi_html}
  </div>
</div>

<!-- CONTACT -->
<div class="contact-section" id="contact">
  <div class="contact-inner">
    <div class="contact-info reveal">
      <p class="section-tag">Get in Touch</p>
      <h2 class="section-title">Ready to Get<br><span>Started?</span></h2>
      <p class="contact-lead">Contact us today for a free, no-obligation quote. We typically respond within a few hours.</p>
      {"<div class='contact-detail'><div class='contact-detail-icon'>📞</div><div><div class='contact-detail-label'>Phone</div><div class='contact-detail-value'>" + html_lib.escape(phone) + "</div></div></div>" if phone else ""}
      {"<div class='contact-detail'><div class='contact-detail-icon'>📍</div><div><div class='contact-detail-label'>Address</div><div class='contact-detail-value'>" + html_lib.escape(address) + "</div></div></div>" if address else ""}
      <div class="contact-btns">
        {phone_btn}
        {maps_btn}
      </div>
    </div>
    <div class="contact-card reveal">
      <div class="contact-monogram">{html_lib.escape(monogram)}</div>
      <div class="contact-card-name">{html_lib.escape(name)}</div>
      <div class="contact-card-cat">{html_lib.escape(cat_label)} · {html_lib.escape(city)}</div>
      <div class="contact-card-desc">{html_lib.escape(hero_desc)}</div>
    </div>
  </div>
</div>

<!-- FOOTER -->
<footer>
  <div class="footer-brand">
    <div class="footer-monogram">{html_lib.escape(monogram)}</div>
    <span class="footer-name">{html_lib.escape(name)}</span>
  </div>
  <span class="footer-meta">{html_lib.escape(cat_label)} · {html_lib.escape(city)}, Netherlands · © 2025</span>
</footer>

<script>
// Nav scroll shadow
const nav = document.getElementById('nav');
window.addEventListener('scroll', () => nav.classList.toggle('scrolled', window.scrollY > 20), {{passive:true}});

// Scroll reveal
const observer = new IntersectionObserver(entries => {{
  entries.forEach(e => {{ if(e.isIntersecting) {{ e.target.classList.add('visible'); observer.unobserve(e.target); }} }});
}}, {{threshold:0.12}});
document.querySelectorAll('.reveal').forEach(el => observer.observe(el));
</script>

</body>
</html>"""


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    # Clear old files
    for f in os.listdir(OUTPUT_DIR):
        if f.endswith('.html'):
            os.remove(os.path.join(OUTPUT_DIR, f))

    generated = 0
    skipped = 0
    seen_slugs = {}

    with open(CSV_PATH, newline='', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            page = generate_html(row)
            if page is None:
                skipped += 1
                continue

            name = (row.get("title") or row.get("﻿title") or "").strip()
            base_slug = slugify(name)
            if not base_slug:
                skipped += 1
                continue

            count = seen_slugs.get(base_slug, 0)
            seen_slugs[base_slug] = count + 1
            slug = base_slug if count == 0 else f"{base_slug}-{count}"

            out_path = os.path.join(OUTPUT_DIR, f"{slug}.html")
            with open(out_path, "w", encoding="utf-8") as out:
                out.write(page)
            generated += 1

    print(f"Done. Generated: {generated} | Skipped: {skipped}")
    print(f"Output: {os.path.abspath(OUTPUT_DIR)}/")


if __name__ == "__main__":
    main()
