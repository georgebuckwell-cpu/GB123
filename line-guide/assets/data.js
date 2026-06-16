/* ============================================================================
   LINE GUIDE — Shared supplier dataset
   Single source of truth for the directory (suppliers.html) and the dynamic
   profile page (supplier.html?s=slug). In production this is an API response.
   ========================================================================== */
window.LG_SUPPLIERS = [
  {
    slug: 'meridian-robotics', name: 'Meridian Robotics', monogram: 'MR',
    rating: 4.9, reviews: 47, region: 'uk', location: 'Birmingham, UK', tier: 'Ultra',
    founded: 2009, team: '120+', lead: '10–14 wks', response: '< 24h', projects: 240,
    blurb: 'High-speed robotic packing & palletising turnkey lines for tier-1 food producers.',
    about: 'Meridian Robotics designs, builds and integrates high-throughput robotic packing and end-of-line systems for the food & beverage sector. From single cells to full turnkey lines, we specialise in speed, changeover flexibility and lifetime support.',
    cases: ['packing', 'palletising', 'end-of-line'],
    capabilities: ['Delta & SCARA robotics', 'Robotic palletising', 'Case packing', 'Tray loading', 'Line integration', 'Vision-guided pick & place'],
    formats: ['Cartons', 'Trays', 'Cans'], environments: ['Ambient', 'Chilled', 'Washdown'],
    certs: ['CE', 'UL', 'ISO 9001'],
    caseStudies: [
      { title: 'Ready-meal tray loading at 240 ppm', sector: 'Chilled foods', result: '+38% line speed, 14-week install' },
      { title: 'Mixed-case palletising cell', sector: 'Beverages', result: 'ROI in 16 months, 2 operators redeployed' },
    ],
    reviewList: [
      { author: 'Operations Director', company: 'National bakery group', rating: 5, text: 'Hit the throughput spec on day one and the support has been faultless. Genuinely turnkey.' },
      { author: 'Engineering Manager', company: 'Chilled ready meals', rating: 5, text: 'Tight footprint, fast changeover, and they understood our hygiene constraints from the start.' },
    ],
    tags: ['Robotics', 'High-speed', 'Turnkey'],
  },
  {
    slug: 'axisflow-automation', name: 'AxisFlow Automation', monogram: 'AF',
    rating: 4.8, reviews: 31, region: 'uk', location: 'Leeds, UK', tier: 'Premium',
    founded: 2014, team: '45', lead: '6–10 wks', response: '< 24h', projects: 130,
    blurb: 'Flexible packing & filling cells with quick install — ideal for varied SKUs.',
    about: 'AxisFlow builds adaptable automation for growing manufacturers. Our modular cells handle pouches, bottles and cans with fast changeover, and we pride ourselves on the quickest install times in the sector.',
    cases: ['packing', 'filling', 'manual'],
    capabilities: ['Modular packing cells', 'Liquid filling', 'Cobot integration', 'Quick changeover', 'Retrofit upgrades'],
    formats: ['Pouches', 'Bottles', 'Cans'], environments: ['Ambient', 'Chilled'],
    certs: ['CE', 'ISO 9001'],
    caseStudies: [
      { title: 'Pouch filling line for sauces', sector: 'Condiments', result: 'Installed in 6 weeks, 3× output' },
    ],
    reviewList: [
      { author: 'Plant Manager', company: 'Artisan drinks brand', rating: 5, text: 'Up and running before our peak season. Flexible team, no drama.' },
    ],
    tags: ['Flexible', 'Quick install'],
  },
  {
    slug: 'nordic-lineworks', name: 'Nordic Lineworks', monogram: 'NL',
    rating: 4.7, reviews: 28, region: 'eu', location: 'Malmö, Sweden', tier: 'Ultra',
    founded: 2006, team: '90', lead: '12–18 wks', response: '< 48h', projects: 180,
    blurb: 'End-of-line & palletising specialists for cold-chain and frozen production.',
    about: 'Nordic Lineworks delivers robust end-of-line and palletising systems engineered for the most demanding cold and frozen environments across Europe.',
    cases: ['palletising', 'end-of-line', 'inspection'],
    capabilities: ['Layer palletising', 'Frozen-rated systems', 'Conveying & sortation', 'Stretch wrapping', 'Inspection integration'],
    formats: ['Cartons', 'Trays'], environments: ['Ambient', 'Frozen', 'Washdown'],
    certs: ['CE', 'ISO 9001', 'ISO 14001'],
    caseStudies: [
      { title: 'Frozen case palletising at -24°C', sector: 'Frozen foods', result: 'Zero downtime in first year' },
    ],
    reviewList: [
      { author: 'Site Engineer', company: 'Frozen produce co.', rating: 5, text: 'Built for the cold. Other vendors couldn\'t cope — Nordic just works.' },
    ],
    tags: ['End-of-line', 'Cold chain'],
  },
  {
    slug: 'crisp-systems', name: 'Crisp Systems', monogram: 'CS',
    rating: 4.6, reviews: 22, region: 'uk', location: 'Bristol, UK', tier: 'Premium',
    founded: 2016, team: '38', lead: '8–12 wks', response: '< 24h', projects: 95,
    blurb: 'Machine-vision inspection, check-weighing and quality automation.',
    about: 'Crisp Systems protects product quality and brand reputation with vision inspection, label verification and check-weighing — integrated cleanly into existing lines.',
    cases: ['inspection', 'manual', 'packing'],
    capabilities: ['Machine vision', 'Check-weighing', 'Label verification', 'Defect detection', 'Cobot handling'],
    formats: ['Trays', 'Pouches', 'Bulk'], environments: ['Ambient', 'Washdown'],
    certs: ['CE', 'ISO 9001'],
    caseStudies: [
      { title: 'Foreign-body vision system', sector: 'Snacks', result: '99.8% detection, recall risk cut' },
    ],
    reviewList: [
      { author: 'Quality Lead', company: 'Snack manufacturer', rating: 5, text: 'Caught issues we were missing. Paid for itself in avoided complaints.' },
    ],
    tags: ['Vision', 'Quality'],
  },
  {
    slug: 'pactura-engineering', name: 'Pactura Engineering', monogram: 'PA',
    rating: 4.5, reviews: 19, region: 'eu', location: 'Eindhoven, NL', tier: 'Basic',
    founded: 2012, team: '26', lead: '6–9 wks', response: '< 48h', projects: 70,
    blurb: 'Value-focused modular packing, filling and conveying systems.',
    about: 'Pactura makes automation accessible with modular, budget-conscious systems for filling, packing and conveying — without compromising reliability.',
    cases: ['packing', 'filling', 'end-of-line'],
    capabilities: ['Modular conveying', 'Volumetric filling', 'Bottle handling', 'Budget retrofits'],
    formats: ['Bottles', 'Cans', 'Bulk'], environments: ['Ambient', 'Chilled'],
    certs: ['CE'],
    caseStudies: [
      { title: 'Entry-level bottling upgrade', sector: 'Beverages', result: 'Doubled capacity under budget' },
    ],
    reviewList: [
      { author: 'Founder', company: 'Craft beverage start-up', rating: 4, text: 'Great value and honest advice on what we actually needed.' },
    ],
    tags: ['Value', 'Modular'],
  },
  {
    slug: 'vanguard-cobotics', name: 'Vanguard Cobotics', monogram: 'VC',
    rating: 4.7, reviews: 34, region: 'uk', location: 'Manchester, UK', tier: 'Premium',
    founded: 2018, team: '52', lead: '4–8 wks', response: '< 12h', projects: 110,
    blurb: 'Collaborative robots that retrofit manual stations — fast ROI.',
    about: 'Vanguard Cobotics automates repetitive manual tasks with collaborative robots that slot into existing lines safely, with rapid deployment and fast payback.',
    cases: ['manual', 'inspection', 'packing'],
    capabilities: ['Cobot deployment', 'Manual task retrofit', 'Pick & place', 'Machine tending', 'Safety integration'],
    formats: ['Pouches', 'Cartons', 'Trays'], environments: ['Ambient', 'Chilled'],
    certs: ['CE', 'UL', 'ISO 9001'],
    caseStudies: [
      { title: 'Manual case-packing retrofit', sector: 'Dairy', result: 'Payback in 11 months, easier hiring' },
    ],
    reviewList: [
      { author: 'Continuous Improvement', company: 'Dairy producer', rating: 5, text: 'Solved a chronic staffing headache. Deployed in under a month.' },
    ],
    tags: ['Cobots', 'Retrofit', 'Fast ROI'],
  },
  {
    slug: 'helix-process', name: 'Helix Process Co.', monogram: 'HX',
    rating: 4.4, reviews: 16, region: 'eu', location: 'Lyon, France', tier: 'Basic',
    founded: 2010, team: '30', lead: '8–12 wks', response: '< 48h', projects: 64,
    blurb: 'Filling, dosing and process automation for liquids and powders.',
    about: 'Helix specialises in accurate, hygienic filling and dosing for liquid, viscous and powder products, with CIP-ready design.',
    cases: ['filling', 'manual', 'inspection'],
    capabilities: ['Viscous filling', 'Powder dosing', 'CIP-ready design', 'Recipe management'],
    formats: ['Bottles', 'Bulk', 'Pouches'], environments: ['Ambient', 'Washdown'],
    certs: ['CE', 'ISO 9001'],
    caseStudies: [
      { title: 'Multi-recipe powder dosing', sector: 'Bakery ingredients', result: '±0.5% accuracy achieved' },
    ],
    reviewList: [
      { author: 'Process Engineer', company: 'Ingredient supplier', rating: 4, text: 'Accurate and hygienic. Solid filling specialists.' },
    ],
    tags: ['Filling', 'Dosing'],
  },
  {
    slug: 'orbit-handling', name: 'Orbit Handling', monogram: 'OH',
    rating: 4.6, reviews: 25, region: 'uk', location: 'Glasgow, UK', tier: 'Ultra',
    founded: 2004, team: '75', lead: '10–16 wks', response: '< 24h', projects: 160,
    blurb: 'Palletising, conveying and complete material-handling integration.',
    about: 'Orbit Handling ties the whole line together — palletising, conveying, accumulation and integration — with decades of material-handling expertise.',
    cases: ['palletising', 'packing', 'end-of-line'],
    capabilities: ['Robotic palletising', 'Conveying systems', 'Accumulation', 'AGV integration', 'Line controls'],
    formats: ['Cartons', 'Trays', 'Cans'], environments: ['Ambient', 'Chilled', 'Frozen'],
    certs: ['CE', 'UL', 'ISO 9001'],
    caseStudies: [
      { title: 'Full-line conveying & palletising', sector: 'Bakery', result: 'Single integrator, on-time go-live' },
    ],
    reviewList: [
      { author: 'Project Lead', company: 'Industrial bakery', rating: 5, text: 'One partner for the whole line made the project far simpler.' },
    ],
    tags: ['Palletising', 'Conveying'],
  },
];
