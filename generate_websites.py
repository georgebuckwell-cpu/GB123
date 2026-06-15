#!/usr/bin/env python3
"""
Website generator for Amsterdam businesses.
Generates a polished, professional HTML demo site for each company.
Purpose: outreach / lead generation to sell web design services.
"""

import csv
import os
import re
import html as html_lib

OUTPUT_DIR = "websites"
CSV_PATH = "/root/.claude/uploads/b553d4c3-fa71-535d-b226-64e15b822f4e/e9e48877-dataset_amsterdam1_20260614_171131429.csv"

# Skip entries that aren't real businesses
SKIP_CATEGORIES = {
    "Park", "Garden", "Lake", "Community garden", "Area", "Hiking area",
    "House", "Vacation rental", "Shipyard",
}

# Category → (primary_color, accent_color, icon, tagline, services, hero_desc)
CATEGORY_CONFIG = {
    "Bricklayer": {
        "primary": "#1a1a2e", "accent": "#e94560",
        "icon": "🧱",
        "tagline": "Building Amsterdam's Future, One Brick at a Time",
        "hero_desc": "Expert bricklaying and restoration masonry serving Amsterdam and surroundings.",
        "services": ["Brickwork & Pointing", "Facade Restoration", "New Build Masonry", "Repointing & Repairs", "Heritage Stonework"],
    },
    "Masonry contractor": {
        "primary": "#2c3e50", "accent": "#e67e22",
        "icon": "🏗️",
        "tagline": "Precision Masonry. Lasting Results.",
        "hero_desc": "Professional masonry contracting for residential and commercial projects across Amsterdam.",
        "services": ["Brick & Block Laying", "Structural Masonry", "Renovation & Restoration", "Garden Walls & Patios", "Chimney Repairs"],
    },
    "Carpenter": {
        "primary": "#3d2b1f", "accent": "#c0832f",
        "icon": "🪵",
        "tagline": "Crafted with Precision. Built to Last.",
        "hero_desc": "Expert carpentry and joinery for homes and businesses throughout Amsterdam.",
        "services": ["Custom Furniture & Cabinetry", "Flooring Installation", "Doors & Windows", "Renovations & Fit-outs", "Stairs & Balustrades"],
    },
    "Plumber": {
        "primary": "#0f3460", "accent": "#00b4d8",
        "icon": "🔧",
        "tagline": "Fast, Reliable Plumbing — Day or Night",
        "hero_desc": "Professional plumbing installation, repair and maintenance across Amsterdam.",
        "services": ["Emergency Call-outs", "Boiler Installation & Service", "Bathroom Fitting", "Leak Detection & Repair", "Central Heating"],
    },
    "Painter": {
        "primary": "#2d2d2d", "accent": "#f7c59f",
        "icon": "🎨",
        "tagline": "Transforming Spaces with Colour & Care",
        "hero_desc": "Professional interior and exterior painting for Amsterdam homes and businesses.",
        "services": ["Interior Painting", "Exterior Painting", "Wallpapering", "Wood Staining & Varnishing", "Commercial Painting"],
    },
    "Electrician": {
        "primary": "#1b1b2f", "accent": "#ffd700",
        "icon": "⚡",
        "tagline": "Powering Amsterdam — Safely & Reliably",
        "hero_desc": "Certified electricians providing installation, maintenance and emergency services.",
        "services": ["Electrical Installations", "Fuse Board Upgrades", "Lighting Design", "Solar & EV Charging", "Safety Inspections"],
    },
    "Electrical installation service": {
        "primary": "#1b1b2f", "accent": "#ffd700",
        "icon": "⚡",
        "tagline": "Expert Electrical Solutions for Every Project",
        "hero_desc": "Reliable electrical installation services for residential and commercial clients in Amsterdam.",
        "services": ["New Installations", "Rewiring", "Smart Home Systems", "Emergency Lighting", "PAT Testing"],
    },
    "Bicycle repair shop": {
        "primary": "#1a3c34", "accent": "#52b788",
        "icon": "🚲",
        "tagline": "Get Back on the Road — Fast",
        "hero_desc": "Expert bicycle repairs, servicing and sales right here in Amsterdam.",
        "services": ["Full Bike Service", "Puncture Repairs", "Brake & Gear Tuning", "E-Bike Servicing", "Custom Builds"],
    },
    "Bicycle Shop": {
        "primary": "#1a3c34", "accent": "#52b788",
        "icon": "🚲",
        "tagline": "Amsterdam's Trusted Bike Specialists",
        "hero_desc": "Quality bikes, expert repairs and accessories for every Amsterdam cyclist.",
        "services": ["New Bike Sales", "Bike Servicing", "Accessories & Parts", "E-Bike Expertise", "Second-hand Bikes"],
    },
    "Photographer": {
        "primary": "#111111", "accent": "#e0c080",
        "icon": "📸",
        "tagline": "Moments Captured. Stories Told.",
        "hero_desc": "Professional photography for portraits, events, products and commercial projects in Amsterdam.",
        "services": ["Portrait Photography", "Event Coverage", "Commercial & Product", "Headshots", "Photo Editing"],
    },
    "Photography studio": {
        "primary": "#111111", "accent": "#e0c080",
        "icon": "📸",
        "tagline": "Creative Photography Studio in Amsterdam",
        "hero_desc": "A fully equipped studio for portraits, fashion, product and creative photography.",
        "services": ["Studio Hire", "Portrait Sessions", "Fashion & Editorial", "Product Photography", "Video Shoots"],
    },
    "Commercial photographer": {
        "primary": "#0d0d0d", "accent": "#c9a84c",
        "icon": "📷",
        "tagline": "Visual Excellence for Your Brand",
        "hero_desc": "High-impact commercial photography that makes brands stand out.",
        "services": ["Brand Photography", "Product Shoots", "Corporate Portraits", "Advertising Campaigns", "Social Media Content"],
    },
    "Photography service": {
        "primary": "#111111", "accent": "#e0c080",
        "icon": "📸",
        "tagline": "Professional Photography Services in Amsterdam",
        "hero_desc": "Capturing your most important moments with skill and artistry.",
        "services": ["Event Photography", "Portrait Sessions", "Documentary", "Editing & Retouching", "Print Services"],
    },
    "Yoga studio": {
        "primary": "#1e3a3a", "accent": "#7ec8a0",
        "icon": "🧘",
        "tagline": "Find Your Balance. Find Your Peace.",
        "hero_desc": "A welcoming yoga studio for all levels in the heart of Amsterdam.",
        "services": ["Hatha Yoga", "Vinyasa Flow", "Yin Yoga", "Kids Yoga", "Private Sessions"],
    },
    "Dog trainer": {
        "primary": "#2c2c54", "accent": "#f9a825",
        "icon": "🐕",
        "tagline": "Happier Dogs. Happier Owners.",
        "hero_desc": "Positive, reward-based dog training for puppies and adult dogs in Amsterdam.",
        "services": ["Puppy Classes", "One-to-One Training", "Obedience Training", "Behaviour Consultation", "Group Classes"],
    },
    "Pet trainer": {
        "primary": "#2c2c54", "accent": "#f9a825",
        "icon": "🐾",
        "tagline": "Expert Pet Training in Amsterdam",
        "hero_desc": "Professional animal training using proven, positive methods.",
        "services": ["Behavioural Assessments", "One-to-One Sessions", "Group Workshops", "Anxiety & Aggression", "Obedience Training"],
    },
    "Tutoring service": {
        "primary": "#003049", "accent": "#fcbf49",
        "icon": "📚",
        "tagline": "Unlock Every Student's Potential",
        "hero_desc": "Expert tutoring in Amsterdam for school, university and professional development.",
        "services": ["Maths & Science", "Languages", "Exam Preparation", "University Applications", "Online Tutoring"],
    },
    "Private tutor": {
        "primary": "#003049", "accent": "#fcbf49",
        "icon": "📖",
        "tagline": "Personalised Learning That Gets Results",
        "hero_desc": "Tailored private tutoring sessions for students of all ages and levels.",
        "services": ["1-on-1 Tuition", "Homework Support", "Exam Coaching", "Subject Specialists", "Online & In-person"],
    },
    "Education center": {
        "primary": "#003049", "accent": "#fcbf49",
        "icon": "🏫",
        "tagline": "Inspiring Minds. Building Futures.",
        "hero_desc": "A dedicated education centre helping students achieve their academic goals.",
        "services": ["Academic Programmes", "Test Preparation", "After-School Support", "Adult Learning", "Online Courses"],
    },
    "Mover": {
        "primary": "#1c2541", "accent": "#3a86ff",
        "icon": "🚚",
        "tagline": "Your Move, Made Easy",
        "hero_desc": "Professional, careful removals for homes and offices across Amsterdam and beyond.",
        "services": ["Home Removals", "Office Relocations", "Packing & Unpacking", "Storage Solutions", "International Moves"],
    },
    "Moving and storage service": {
        "primary": "#1c2541", "accent": "#3a86ff",
        "icon": "📦",
        "tagline": "Stress-Free Moving & Secure Storage",
        "hero_desc": "Full-service removals and storage solutions for Amsterdam residents and businesses.",
        "services": ["Local Moves", "Long-distance Moves", "Secure Storage", "Packing Materials", "Furniture Assembly"],
    },
    "Trucking company": {
        "primary": "#212529", "accent": "#ff6b35",
        "icon": "🚛",
        "tagline": "Reliable Transport. On Time. Every Time.",
        "hero_desc": "Professional freight and logistics services operating across the Netherlands and Europe.",
        "services": ["Freight Transport", "Same-day Delivery", "Pallet & Bulk Loads", "Temperature Controlled", "Cross-border Logistics"],
    },
    "Courier service": {
        "primary": "#1a1a2e", "accent": "#e94560",
        "icon": "📬",
        "tagline": "Fast. Secure. Delivered.",
        "hero_desc": "Same-day and next-day courier services across Amsterdam and the Netherlands.",
        "services": ["Same-day Delivery", "Next-day Courier", "Parcel Tracking", "Business Accounts", "International Shipping"],
    },
    "Shipping company": {
        "primary": "#023e8a", "accent": "#48cae4",
        "icon": "🚢",
        "tagline": "Your Cargo, Our Commitment",
        "hero_desc": "International and domestic shipping solutions you can rely on.",
        "services": ["International Freight", "Customs Clearance", "Parcel Services", "Door-to-door Delivery", "Supply Chain Management"],
    },
    "Delivery service": {
        "primary": "#1a1a2e", "accent": "#e94560",
        "icon": "🏃",
        "tagline": "Speed. Reliability. Delivered to Your Door.",
        "hero_desc": "Fast, dependable delivery services in Amsterdam.",
        "services": ["Express Delivery", "Scheduled Runs", "Last-mile Logistics", "Parcel Tracking", "Business Contracts"],
    },
    "Contractor": {
        "primary": "#2c2c2c", "accent": "#ff8c00",
        "icon": "🏗️",
        "tagline": "Quality Contracting. Guaranteed Satisfaction.",
        "hero_desc": "Full-service construction and contracting for residential and commercial clients.",
        "services": ["New Build", "Renovation", "Project Management", "Fit-out & Finishing", "Structural Work"],
    },
    "General contractor": {
        "primary": "#2c2c2c", "accent": "#ff8c00",
        "icon": "🏗️",
        "tagline": "From Foundation to Finish — We Build It All",
        "hero_desc": "Experienced general contractors delivering quality builds across Amsterdam.",
        "services": ["Project Management", "New Construction", "Renovations", "Commercial Fit-out", "Subcontractor Coordination"],
    },
    "Construction company": {
        "primary": "#1a1a2e", "accent": "#ff6b35",
        "icon": "🏛️",
        "tagline": "Built on Trust. Built to Last.",
        "hero_desc": "A leading construction company delivering quality projects across Amsterdam.",
        "services": ["Residential Construction", "Commercial Projects", "Structural Engineering", "Site Management", "Turnkey Solutions"],
    },
    "Home builder": {
        "primary": "#3d2b1f", "accent": "#c0832f",
        "icon": "🏡",
        "tagline": "Building the Home You've Always Dreamed Of",
        "hero_desc": "Custom home builders delivering quality craftsmanship across Amsterdam.",
        "services": ["Custom New Builds", "Extensions & Loft Conversions", "Full Renovations", "Kitchen & Bathroom", "Architectural Design"],
    },
    "Custom home builder": {
        "primary": "#3d2b1f", "accent": "#c0832f",
        "icon": "🏡",
        "tagline": "Your Vision. Our Craftsmanship.",
        "hero_desc": "Bespoke home building tailored exactly to your needs and style.",
        "services": ["Bespoke Design", "Custom Builds", "Extensions", "Interior Fit-out", "Project Management"],
    },
    "Landscaper": {
        "primary": "#1b4332", "accent": "#52b788",
        "icon": "🌿",
        "tagline": "Beautiful Outdoor Spaces, Expertly Created",
        "hero_desc": "Professional landscaping and garden design services across Amsterdam.",
        "services": ["Garden Design", "Planting & Turfing", "Paving & Decking", "Irrigation Systems", "Maintenance Plans"],
    },
    "House cleaning service": {
        "primary": "#e0f4ff", "accent": "#0077b6",
        "icon": "🧹",
        "tagline": "A Spotless Home, Every Time",
        "hero_desc": "Professional domestic and commercial cleaning services in Amsterdam.",
        "services": ["Regular Cleaning", "Deep Cleaning", "End-of-tenancy Cleaning", "Office Cleaning", "Window Cleaning"],
    },
    "Cleaning service": {
        "primary": "#e0f4ff", "accent": "#0077b6",
        "icon": "✨",
        "tagline": "Clean Spaces. Clear Minds.",
        "hero_desc": "Reliable cleaning services for homes and businesses across Amsterdam.",
        "services": ["Domestic Cleaning", "Commercial Cleaning", "Deep Cleans", "Graffiti Removal", "Specialist Cleaning"],
    },
    "Roofing contractor": {
        "primary": "#1c1c1c", "accent": "#c0392b",
        "icon": "🏠",
        "tagline": "Protecting Your Home from the Top Down",
        "hero_desc": "Expert roofing installation, repair and maintenance across Amsterdam.",
        "services": ["Roof Repairs", "New Roof Installation", "Flat Roofing", "Gutter Cleaning & Repair", "Roof Inspections"],
    },
    "Plasterer": {
        "primary": "#f5f0e8", "accent": "#8b6914",
        "icon": "🪣",
        "tagline": "Flawless Walls. Perfect Finishes.",
        "hero_desc": "Expert plastering and skimming services for homes and businesses in Amsterdam.",
        "services": ["Skimming & Plastering", "Render & External Finishes", "Decorative Plasterwork", "Dry Lining", "Patch & Repair"],
    },
    "Stucco contractor": {
        "primary": "#f5f0e8", "accent": "#8b6914",
        "icon": "🪣",
        "tagline": "Smooth Finishes. Exceptional Quality.",
        "hero_desc": "Professional stucco and plastering contractors serving Amsterdam.",
        "services": ["Interior Plastering", "External Render", "Ornamental Stucco", "Repair & Restoration", "Dry Lining"],
    },
    "Import export company": {
        "primary": "#023e8a", "accent": "#48cae4",
        "icon": "🌍",
        "tagline": "Global Trade. Local Expertise.",
        "hero_desc": "Connecting Amsterdam businesses to global markets through reliable import and export services.",
        "services": ["Import & Export Logistics", "Customs Clearance", "Trade Compliance", "Warehousing", "Supply Chain Consulting"],
    },
    "Video production service": {
        "primary": "#0d0d0d", "accent": "#e63946",
        "icon": "🎬",
        "tagline": "Your Story. Beautifully Told.",
        "hero_desc": "Professional video production for brands, events and content creators in Amsterdam.",
        "services": ["Brand Films", "Event Videography", "Social Media Content", "Corporate Video", "Post-production & Editing"],
    },
    "Art studio": {
        "primary": "#1a1a2e", "accent": "#ff6b9d",
        "icon": "🖌️",
        "tagline": "Where Creativity Comes to Life",
        "hero_desc": "A vibrant creative studio offering art classes, workshops and bespoke commissions.",
        "services": ["Art Classes", "Private Commissions", "Workshop Events", "Studio Hire", "Art Supplies"],
    },
    "Website designer": {
        "primary": "#0f0f23", "accent": "#6c63ff",
        "icon": "💻",
        "tagline": "Websites That Work as Hard as You Do",
        "hero_desc": "Creative web design and development for businesses that want to stand out online.",
        "services": ["Website Design", "E-commerce Development", "SEO & Performance", "Branding & Identity", "Hosting & Maintenance"],
    },
    "Handyman/Handywoman/Handyperson": {
        "primary": "#2c2c2c", "accent": "#f4a261",
        "icon": "🔨",
        "tagline": "No Job Too Small. Quality Every Time.",
        "hero_desc": "Your trusted local handyman for repairs, maintenance and small renovations in Amsterdam.",
        "services": ["General Repairs", "Flat-pack Assembly", "Tiling & Grouting", "Door & Lock Fitting", "Painting & Decorating"],
    },
    "Taxi service": {
        "primary": "#1a1a2e", "accent": "#ffd60a",
        "icon": "🚕",
        "tagline": "Your Ride, On Your Terms",
        "hero_desc": "Professional, reliable taxi and transport services across Amsterdam.",
        "services": ["Airport Transfers", "City Rides", "Business Accounts", "Event Transport", "Long-distance"],
    },
    "Mailing service": {
        "primary": "#023e8a", "accent": "#48cae4",
        "icon": "✉️",
        "tagline": "Your Mail in Safe Hands",
        "hero_desc": "Professional mailing and postal services for individuals and businesses.",
        "services": ["Parcel Handling", "PO Box Services", "Document Scanning", "Mail Forwarding", "Business Post"],
    },
    "Garden building supplier": {
        "primary": "#1b4332", "accent": "#95d5b2",
        "icon": "🌱",
        "tagline": "Everything You Need for the Perfect Garden",
        "hero_desc": "Quality garden buildings, materials and supplies for Amsterdam's outdoor spaces.",
        "services": ["Garden Sheds & Cabins", "Decking & Timber", "Fencing & Gates", "Garden Furniture", "Tools & Accessories"],
    },
}

# Fallback for unknown categories
DEFAULT_CONFIG = {
    "primary": "#1a1a2e", "accent": "#e94560",
    "icon": "⭐",
    "tagline": "Professional Services in Amsterdam",
    "hero_desc": "Trusted local professionals delivering quality services across Amsterdam.",
    "services": ["Professional Services", "Quality Guaranteed", "Local Expertise", "Competitive Rates", "Free Consultation"],
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


def stars_html(score):
    if not score:
        return ""
    try:
        s = float(score)
    except ValueError:
        return ""
    full = int(s)
    half = 1 if (s - full) >= 0.5 else 0
    empty = 5 - full - half
    return "★" * full + ("½" if half else "") + "☆" * empty


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
    city = company.get("city", "Amsterdam").strip() or "Amsterdam"
    phone = company.get("phone", "").strip()
    website = company.get("website", "").strip()
    score = company.get("totalScore", "").strip()
    reviews = company.get("reviewsCount", "").strip()
    maps_url = company.get("url", "").strip()

    primary = cfg["primary"]
    accent = cfg["accent"]
    icon = cfg["icon"]
    tagline = cfg["tagline"]
    hero_desc = cfg["hero_desc"]
    services = cfg["services"]

    # Determine text color for primary bg (dark = white, light = dark)
    # Simple heuristic: if primary starts with #f or #e or #d it's light
    primary_text = "#ffffff" if primary[1].lower() not in ('f', 'e', 'd', 'c') else "#1a1a1a"

    address_parts = [p for p in [street, city, "Netherlands"] if p]
    address = ", ".join(address_parts)

    services_html = "\n".join(
        f'<div class="service-card"><span class="check">✓</span><span>{html_lib.escape(s)}</span></div>'
        for s in services
    )

    rating_html = ""
    if score and reviews:
        rating_html = f"""
        <div class="rating-badge">
            <span class="stars">{stars_html(score)}</span>
            <span class="rating-text">{score} / 5 &nbsp;·&nbsp; {reviews} reviews</span>
        </div>"""

    cat_label = primary_cat if primary_cat else "Professional Services"

    phone_html = f'<a href="tel:{html_lib.escape(phone)}" class="cta-btn">{html_lib.escape(phone)}</a>' if phone else '<span class="cta-btn no-phone">Contact us for a quote</span>'
    maps_html = f'<a href="{html_lib.escape(maps_url)}" target="_blank" class="map-link">📍 View on Google Maps</a>' if maps_url else ""

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{html_lib.escape(name)} — {html_lib.escape(city)}</title>
<meta name="description" content="{html_lib.escape(name)} — {html_lib.escape(hero_desc)}">
<style>
  *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
  :root {{
    --primary: {primary};
    --accent: {accent};
    --primary-text: {primary_text};
  }}
  html {{ scroll-behavior: smooth; }}
  body {{ font-family: 'Segoe UI', system-ui, -apple-system, sans-serif; background: #f8f9fa; color: #1a1a1a; }}

  /* NAV */
  nav {{
    position: fixed; top: 0; left: 0; right: 0; z-index: 100;
    background: rgba(0,0,0,0.85); backdrop-filter: blur(12px);
    display: flex; align-items: center; justify-content: space-between;
    padding: 0 5%; height: 64px;
  }}
  .nav-brand {{ color: #fff; font-weight: 700; font-size: 1.1rem; letter-spacing: -0.3px; }}
  .nav-cta {{
    background: var(--accent); color: #fff; border: none; border-radius: 6px;
    padding: 8px 20px; font-size: 0.9rem; font-weight: 600; cursor: pointer;
    text-decoration: none; transition: opacity 0.2s;
  }}
  .nav-cta:hover {{ opacity: 0.85; }}

  /* HERO */
  .hero {{
    min-height: 100vh;
    background: linear-gradient(135deg, var(--primary) 0%, color-mix(in srgb, var(--primary) 70%, #000) 100%);
    display: flex; flex-direction: column; align-items: center; justify-content: center;
    text-align: center; padding: 100px 5% 80px;
    position: relative; overflow: hidden;
  }}
  .hero::before {{
    content: '';
    position: absolute; inset: 0;
    background: radial-gradient(ellipse 80% 60% at 50% 50%, color-mix(in srgb, var(--accent) 15%, transparent), transparent);
  }}
  .hero-icon {{ font-size: 4rem; margin-bottom: 16px; position: relative; }}
  .hero-badge {{
    background: color-mix(in srgb, var(--accent) 20%, transparent);
    border: 1px solid color-mix(in srgb, var(--accent) 40%, transparent);
    color: var(--accent); border-radius: 999px;
    padding: 6px 18px; font-size: 0.8rem; font-weight: 600; letter-spacing: 1px;
    text-transform: uppercase; margin-bottom: 24px; display: inline-block;
    position: relative;
  }}
  .hero h1 {{
    font-size: clamp(2.2rem, 5vw, 3.8rem); font-weight: 800; color: #fff;
    line-height: 1.1; letter-spacing: -1px; margin-bottom: 12px;
    position: relative;
  }}
  .hero-tagline {{
    font-size: clamp(1rem, 2vw, 1.35rem); color: rgba(255,255,255,0.7);
    max-width: 600px; line-height: 1.6; margin-bottom: 32px;
    position: relative;
  }}
  {rating_html and ".rating-badge { display: inline-flex; align-items: center; gap: 10px; background: rgba(255,255,255,0.1); border: 1px solid rgba(255,255,255,0.2); border-radius: 999px; padding: 8px 20px; margin-bottom: 28px; color: #fff; font-size: 0.9rem; position: relative; }" or ""}
  .stars {{ color: var(--accent); font-size: 1rem; letter-spacing: 1px; }}
  .hero-actions {{ display: flex; gap: 14px; flex-wrap: wrap; justify-content: center; position: relative; }}
  .btn-primary {{
    background: var(--accent); color: #fff; border: none; border-radius: 8px;
    padding: 14px 32px; font-size: 1rem; font-weight: 700; cursor: pointer;
    text-decoration: none; transition: transform 0.15s, box-shadow 0.15s;
    box-shadow: 0 4px 20px color-mix(in srgb, var(--accent) 40%, transparent);
  }}
  .btn-primary:hover {{ transform: translateY(-2px); box-shadow: 0 8px 28px color-mix(in srgb, var(--accent) 50%, transparent); }}
  .btn-secondary {{
    background: transparent; color: #fff; border: 2px solid rgba(255,255,255,0.4);
    border-radius: 8px; padding: 14px 32px; font-size: 1rem; font-weight: 600;
    cursor: pointer; text-decoration: none; transition: border-color 0.2s, background 0.2s;
  }}
  .btn-secondary:hover {{ border-color: #fff; background: rgba(255,255,255,0.08); }}

  /* STATS BAR */
  .stats-bar {{
    background: var(--accent); padding: 20px 5%;
    display: flex; justify-content: center; gap: 60px; flex-wrap: wrap;
  }}
  .stat {{ text-align: center; color: #fff; }}
  .stat-num {{ font-size: 1.6rem; font-weight: 800; display: block; }}
  .stat-label {{ font-size: 0.78rem; opacity: 0.85; font-weight: 500; text-transform: uppercase; letter-spacing: 0.5px; }}

  /* SECTIONS */
  section {{ padding: 80px 5%; max-width: 1200px; margin: 0 auto; }}
  .section-label {{
    color: var(--accent); font-size: 0.8rem; font-weight: 700;
    text-transform: uppercase; letter-spacing: 2px; margin-bottom: 10px;
  }}
  h2 {{ font-size: clamp(1.8rem, 3.5vw, 2.8rem); font-weight: 800; line-height: 1.15; letter-spacing: -0.5px; }}
  .section-intro {{ font-size: 1.1rem; color: #555; line-height: 1.7; margin-top: 14px; max-width: 620px; }}

  /* SERVICES */
  .services-grid {{
    display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 16px; margin-top: 40px;
  }}
  .service-card {{
    background: #fff; border-radius: 12px; padding: 20px 24px;
    display: flex; align-items: center; gap: 14px;
    box-shadow: 0 2px 12px rgba(0,0,0,0.06); border: 1px solid #f0f0f0;
    font-weight: 600; font-size: 0.95rem; transition: transform 0.15s, box-shadow 0.15s;
  }}
  .service-card:hover {{ transform: translateY(-3px); box-shadow: 0 6px 24px rgba(0,0,0,0.1); }}
  .check {{
    width: 32px; height: 32px; border-radius: 50%;
    background: color-mix(in srgb, var(--accent) 15%, transparent);
    color: var(--accent); display: flex; align-items: center; justify-content: center;
    font-weight: 800; flex-shrink: 0;
  }}

  /* WHY US */
  .why-section {{ background: var(--primary); border-radius: 24px; padding: 60px; margin: 0 5% 80px; }}
  .why-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 32px; margin-top: 36px; }}
  .why-card {{ text-align: center; color: var(--primary-text); }}
  .why-icon {{ font-size: 2.2rem; margin-bottom: 12px; }}
  .why-title {{ font-weight: 700; font-size: 1rem; margin-bottom: 6px; color: #fff; }}
  .why-desc {{ font-size: 0.875rem; opacity: 0.65; color: #fff; line-height: 1.5; }}
  .why-section h2 {{ color: #fff; }}
  .why-section .section-label {{ color: var(--accent); }}

  /* CONTACT */
  .contact-section {{
    background: #fff; border-radius: 24px; padding: 60px;
    margin: 0 5% 80px; box-shadow: 0 4px 32px rgba(0,0,0,0.07);
    display: grid; grid-template-columns: 1fr 1fr; gap: 48px; align-items: center;
  }}
  .contact-info h2 {{ margin-bottom: 20px; }}
  .contact-detail {{ display: flex; align-items: flex-start; gap: 12px; margin-bottom: 16px; font-size: 0.95rem; color: #444; }}
  .contact-icon {{ font-size: 1.2rem; flex-shrink: 0; margin-top: 2px; }}
  .cta-btn {{
    display: inline-block; background: var(--accent); color: #fff;
    padding: 14px 32px; border-radius: 8px; font-size: 1rem; font-weight: 700;
    text-decoration: none; margin-top: 8px;
    box-shadow: 0 4px 20px color-mix(in srgb, var(--accent) 40%, transparent);
    transition: transform 0.15s;
  }}
  .cta-btn:hover {{ transform: translateY(-2px); }}
  .cta-btn.no-phone {{ opacity: 0.7; cursor: default; }}
  .map-link {{ display: inline-block; margin-top: 12px; color: var(--accent); text-decoration: none; font-weight: 600; font-size: 0.9rem; }}
  .map-link:hover {{ text-decoration: underline; }}
  .contact-visual {{
    background: linear-gradient(135deg, var(--primary), color-mix(in srgb, var(--primary) 70%, #000));
    border-radius: 16px; padding: 40px; color: #fff; text-align: center;
  }}
  .contact-visual .big-icon {{ font-size: 5rem; margin-bottom: 16px; }}
  .contact-visual p {{ opacity: 0.75; font-size: 0.95rem; line-height: 1.6; }}

  /* FOOTER */
  footer {{
    background: #111; color: rgba(255,255,255,0.5);
    text-align: center; padding: 30px 5%; font-size: 0.85rem;
  }}
  footer strong {{ color: rgba(255,255,255,0.8); }}

  @media (max-width: 700px) {{
    .contact-section {{ grid-template-columns: 1fr; }}
    .why-section, .contact-section {{ padding: 36px 24px; border-radius: 16px; }}
    .stats-bar {{ gap: 28px; }}
  }}
</style>
</head>
<body>

<nav>
  <span class="nav-brand">{html_lib.escape(icon)} {html_lib.escape(name)}</span>
  <a href="#contact" class="nav-cta">Get in Touch</a>
</nav>

<section class="hero">
  <div class="hero-icon">{icon}</div>
  <div class="hero-badge">{html_lib.escape(cat_label)}</div>
  <h1>{html_lib.escape(name)}</h1>
  <p class="hero-tagline">{html_lib.escape(tagline)}</p>
  {rating_html}
  <div class="hero-actions">
    <a href="#contact" class="btn-primary">Get a Free Quote</a>
    <a href="#services" class="btn-secondary">Our Services</a>
  </div>
</section>

<div class="stats-bar">
  <div class="stat"><span class="stat-num">10+</span><span class="stat-label">Years Experience</span></div>
  <div class="stat"><span class="stat-num">500+</span><span class="stat-label">Projects Completed</span></div>
  <div class="stat"><span class="stat-num">100%</span><span class="stat-label">Satisfaction Guarantee</span></div>
  <div class="stat"><span class="stat-num">Amsterdam</span><span class="stat-label">Based & Trusted</span></div>
</div>

<section id="services">
  <p class="section-label">What We Offer</p>
  <h2>Our Services</h2>
  <p class="section-intro">{html_lib.escape(hero_desc)}</p>
  <div class="services-grid">
    {services_html}
  </div>
</section>

<div class="why-section">
  <p class="section-label">Why Choose Us</p>
  <h2>The {html_lib.escape(name.split()[0])} Difference</h2>
  <div class="why-grid">
    <div class="why-card">
      <div class="why-icon">🏆</div>
      <div class="why-title">Quality First</div>
      <div class="why-desc">We never cut corners. Every job is done to the highest standard.</div>
    </div>
    <div class="why-card">
      <div class="why-icon">⏱️</div>
      <div class="why-title">On Time, Every Time</div>
      <div class="why-desc">We respect your time and always deliver on schedule.</div>
    </div>
    <div class="why-card">
      <div class="why-icon">💬</div>
      <div class="why-title">Clear Communication</div>
      <div class="why-desc">No surprises. We keep you informed at every step.</div>
    </div>
    <div class="why-card">
      <div class="why-icon">💰</div>
      <div class="why-title">Fair Pricing</div>
      <div class="why-desc">Transparent quotes with no hidden costs. Great value guaranteed.</div>
    </div>
  </div>
</div>

<section id="contact">
  <div class="contact-section" style="max-width:100%;margin:0;padding:60px;">
    <div class="contact-info">
      <p class="section-label">Get in Touch</p>
      <h2>Let's Talk About Your Project</h2>
      <p style="color:#555;line-height:1.7;margin:14px 0 24px;">Ready to get started? Contact us today for a free, no-obligation quote. We'd love to hear from you.</p>
      {"<div class='contact-detail'><span class='contact-icon'>📞</span><div><strong>Phone</strong><br>" + html_lib.escape(phone) + "</div></div>" if phone else ""}
      {"<div class='contact-detail'><span class='contact-icon'>📍</span><div><strong>Address</strong><br>" + html_lib.escape(address) + "</div></div>" if address else ""}
      {phone_html}
      {maps_html}
    </div>
    <div class="contact-visual">
      <div class="big-icon">{icon}</div>
      <h3 style="font-size:1.4rem;margin-bottom:10px;">{html_lib.escape(name)}</h3>
      <p>{html_lib.escape(hero_desc)}</p>
    </div>
  </div>
</section>

<footer>
  <strong>{html_lib.escape(name)}</strong> &nbsp;·&nbsp; {html_lib.escape(city)}, Netherlands &nbsp;·&nbsp;
  {html_lib.escape(cat_label)} &nbsp;·&nbsp; © 2025
</footer>

</body>
</html>"""


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
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

            name = row.get("title", "").strip()
            base_slug = slugify(name)
            if not base_slug:
                skipped += 1
                continue

            # Deduplicate slugs
            count = seen_slugs.get(base_slug, 0)
            seen_slugs[base_slug] = count + 1
            slug = base_slug if count == 0 else f"{base_slug}-{count}"

            out_path = os.path.join(OUTPUT_DIR, f"{slug}.html")
            with open(out_path, "w", encoding="utf-8") as out:
                out.write(page)
            generated += 1

    print(f"Done. Generated: {generated} websites, Skipped: {skipped}")
    print(f"Output directory: {os.path.abspath(OUTPUT_DIR)}/")


if __name__ == "__main__":
    main()
