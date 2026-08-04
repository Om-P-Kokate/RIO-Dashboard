"""Data extracted verbatim from CUB-Meta Alignment_Interactive Companion.html.

Every array below is a 1:1 transcription of the constants in that file's <script>
block. HTML entities (&amp;) are decoded to plain text. No values are rounded,
estimated, or added.
"""

# --- R: the 8 strategic routes -------------------------------------------------
# s = [Importance, Investment, Momentum, Clarity, Alumni, Risk]  (each 1-5)
# w = weighted priority score, st = status, d = alignment note, u = near-term use
R = {
    "ai": {
        "n": "Meta AI / agents",
        "f": "Meta AI / MSL / FAIR / Llama / agentic AI",
        "s": [5, 5, 5, 4, 5, 4], "w": 4.6, "st": "Lead",
        "d": "Strong capability; direct relationship history is thinner but strategically central.",
        "u": "Ask university lead which AI route is active: evaluation, agents, open models, AI safety, multimodal systems, or product AI.",
    },
    "infra": {
        "n": "AI infrastructure",
        "f": "AI infrastructure / data centres / energy / water / cooling",
        "s": [5, 5, 5, 2, 5, 3], "w": 4.4, "st": "Strategic route to qualify",
        "d": "Broadest CU capability pool; company need is clear, route unclear.",
        "u": "Ask whether university partnerships can reach data-center/energy/infrastructure owners or whether this is vendor/procurement-only.",
    },
    "rl": {
        "n": "Reality Labs / XR",
        "f": "Reality Labs / AI glasses / wearables / XR",
        "s": [5, 4, 4, 5, 4, 3], "w": 4.3, "st": "Lead",
        "d": "Strongest documented CU–Meta relationship history and strong technical capability.",
        "u": "Use as the most distinctive CU-Meta handshake lane if Meta confirms route owner: smart glasses, EMG, HCI, optics/RF, spatial audio, wearables, accessibility.",
    },
    "perc": {
        "n": "Multimodal perception",
        "f": "Multimodal perception / computer vision / 3D / embodied AI",
        "s": [4, 4, 4, 3, 4, 3], "w": 3.8, "st": "Cross-cutting technical lane",
        "d": "Strong cross-cutting bridge between Meta AI and Reality Labs.",
        "u": "Treat as bridge between AI and Reality Labs: perception, localization, 3D scene understanding, spatial audio, camera systems.",
    },
    "os": {
        "n": "Open-source AI",
        "f": "Open-source AI / developer ecosystem / evaluation tools",
        "s": [4, 4, 4, 4, 3, 3], "w": 3.8, "st": "Good mechanism lane",
        "d": "Open-weight model strategy and academic tooling ecosystem.",
        "u": "Potentially lower-friction because it can use open-science, benchmarks, tools, evaluation libraries, and developer communities.",
    },
    "trust": {
        "n": "Trust / privacy",
        "f": "Trust / privacy / security / integrity / youth",
        "s": [5, 4, 4, 3, 3, 5], "w": 3.7, "st": "Sensitive high-need lane",
        "d": "Strong CU capability and prior Meta/Facebook signals; high sensitivity.",
        "u": "Frame technically: evaluation, measurement, privacy-preserving systems, security, youth wellbeing, and safety-by-design; avoid adversarial framing.",
    },
    "ux": {
        "n": "UX / accessibility",
        "f": "Design / UX / accessibility / inclusive interaction",
        "s": [4, 3, 4, 4, 3, 2], "w": 3.7, "st": "Safe distinctive bridge lane",
        "d": "Strong cross-cutting CU strength.",
        "u": "Use as a low-reputational-risk bridge: accessibility, assistive tech, inclusive design, sensory/cognitive interaction, human factors.",
    },
    "apps": {
        "n": "Family of Apps",
        "f": "Family of Apps / ads / discovery / creator economy",
        "s": [5, 4, 4, 2, 3, 5], "w": 3.5, "st": "Business-core but data-sensitive",
        "d": "Business-critical but proprietary-data-sensitive.",
        "u": "Hold as a second-order lane unless Meta raises ads/discovery/product; likely requires proprietary data and careful privacy framing.",
    },
}

DIMS = ["Importance", "Investment", "Momentum", "Clarity", "Alumni", "Risk"]
O = ["ai", "infra", "rl", "perc", "os", "trust", "ux", "apps"]

# --- Evidence-stream counts ----------------------------------------------------
JOBS = {"ai": 24, "rl": 46, "perc": 11, "trust": 22, "infra": 118, "apps": 25, "ux": 7, "biz": 20, "unc": 20}
PAT = {"ai": 14, "rl": 178, "perc": 43, "trust": 8, "infra": 64, "apps": 4, "ux": 11, "unc": 128}

# [awarded, proposed] grant records
ERA = {"rl": [9, 14], "trust": [5, 7], "ai": [0, 1], "apps": [1, 2], "infra": [0, 0], "perc": [0, 0], "ux": [1, 0], "os": [0, 0]}
# [total signals, distinct activities]
FRP = {"rl": [29, 22], "ai": [11, 10], "infra": [8, 8], "trust": [8, 6], "apps": [0, 0], "perc": [0, 0], "ux": [0, 0], "os": [0, 0]}
# [total scholarly signals, confirmed]
SCH = {"rl": [11, 11], "apps": [51, 5], "ai": [38, 5], "trust": [23, 5], "infra": [3, 2], "perc": [0, 0], "ux": [0, 0], "os": [0, 0]}
# [awarded $, proposed $]
FUND = {"rl": [4269469, 4386473], "trust": [171443, 245729], "ai": [0, 199590], "apps": [0, 0], "infra": [0, 0], "perc": [0, 0], "ux": [0, 0], "os": [0, 0]}
ALUMR = {"ai": 39, "infra": 30, "apps": 16, "rl": 13, "ux": 4, "trust": 1, "perc": 0, "os": 0}

ALUM = [
    ["Meta AI / AI-ML / data science", 39],
    ["Software engineering", 34],
    ["AI infra / data centres / networking", 30],
    ["Family of Apps / ads", 16],
    ["Reality Labs / XR", 13],
    ["Engineering (general)", 8],
    ["Other / unclear", 7],
    ["UX / design / content", 4],
    ["Privacy / security / integrity", 1],
]

YRS = [[2019, 46], [2020, 235], [2021, 255], [2022, 297], [2023, 261], [2024, 395], [2025, 286]]

# [source, scanned, signals, rate %]
SIG = [
    ["Publications", 36048, 117, 0.32],
    ["Datasets", 28191, 6, 0.02],
    ["Grants", 2216, 5, 0.23],
    ["Patents", 484, 0, 0.00],
    ["Clinical trials", 157, 1, 0.64],
]

TERMS = [
    ["Displays", 141], ["Optics / waveguides", 74], ["Wearable / head-mounted", 51],
    ["Audio / speech", 42], ["AR / VR", 30], ["Eye-tracking / gaze", 25],
    ["Machine learning", 19], ["Avatars", 12], ["Micro-LED", 8], ["Haptics", 6],
]

# --- P: researchers ------------------------------------------------------------
# [name, unit, focus, relevance to Meta, [routes], relationship_flag(1/0)]
P = [
    ["Robert McLeod", "Chemical & Biological Engineering", "Holographic photopolymers, optical and display materials", "A documented Meta/Reality Labs anchor for displays, optics and holography.", ["rl"], 1],
    ["Steven George", "Chemistry", "Atomic layer processing, micro-LED materials, semiconductor surfaces", "Direct Meta relationship around AlInGaP micro-LED manufacturing; highest infrastructure-alignment score.", ["rl", "infra"], 1],
    ["Christopher Bowman", "Chemical & Biological Engineering", "Photopolymer chemistry, holographic systems", "Closely tied to the McLeod display-materials route.", ["rl"], 1],
    ["Noel Clark", "Physics", "Ferroelectric nematic liquid crystals", "Reality Labs evidence around fast-display materials.", ["rl"], 1],
    ["Joseph Maclennan", "Physics", "Fluid ferroelectrics, fast photonics", "Direct fast-display and agreement-related activity.", ["rl"], 1],
    ["Juliet Gopinath", "Electrical, Computer & Energy Engineering", "Photonics, imaging, integrated optical devices", "Very strong capability fit for glasses optics and waveguides.", ["rl"], 0],
    ["Jianliang Xiao", "Mechanical Engineering", "Flexible, self-healing wearables; energy harvesting", "Direct Meta evidence around wearable energy harvesting.", ["rl"], 1],
    ["Leanne Hirshfield", "Institute of Cognitive Science", "Neurophysiological HCI, gaze and brain signals, XR", "Prior Meta/Reality Labs eye-brain-interface collaboration signal.", ["rl", "ux"], 1],
    ["Danielle Szafir", "Information Science", "Immersive analytics, trust in smart devices", "Proposed Meta/Facebook work on trust and immersive interfaces.", ["rl"], 1],
    ["Ashutosh Trivedi", "Computer Science", "Reinforcement learning, decision processes, formal reasoning", "Highest-scoring Meta AI alignment fit; agent evaluation and reliable decision systems.", ["ai"], 0],
    ["Alvaro Velasquez", "Computer Science", "Robust AI, adversarial hardening, LLM planning", "Direct fit for Meta’s AI safety, evaluation and model-reliability needs.", ["ai"], 0],
    ["Sidney D’Mello", "Institute of Cognitive Science", "Human-centered AI, multimodal interaction", "Bridges Meta AI and human-centered deployment and feedback.", ["ai"], 0],
    ["Morteza Lahijanian", "Aerospace Engineering Sciences", "Safe reinforcement learning, verification, autonomous systems", "Safe agent behaviour and evaluation of autonomous and agentic systems.", ["ai"], 0],
    ["Bradley Hayes", "Computer Science", "Human-robot interaction, agent communication", "Prior Meta relationship signal; embodied agents and human-AI interaction.", ["ai", "perc"], 1],
    ["Alessandro Roncone", "Computer Science", "Embodied AI, interactive autonomy, assistive robotics", "Prior Meta talent and relationship signal; social agents and human-AI teaming.", ["ai", "perc"], 1],
    ["Nisar Ahmed", "Aerospace Engineering Sciences", "Competency self-assessment, uncertainty modelling, autonomous mapping", "AI agents that communicate their own limits and competency to people.", ["ai", "perc"], 0],
    ["Danna Gurari", "Computer Science", "Visual question answering, visual privacy, accessibility-centered vision", "Direct Meta AI and multimodal vision signals; accessibility and visual AI.", ["ai", "perc", "trust", "ux"], 1],
    ["Christoffer Heckman", "Mechanical Engineering", "Robust perception, navigation, multi-agent autonomy", "Spatial AI and device or robot perception under imperfect sensing.", ["perc"], 0],
    ["Eric Frew", "Aerospace Engineering Sciences", "Autonomous systems, multi-agent robot teams", "Spatial AI, autonomous mapping and multi-agent coordination.", ["perc"], 0],
    ["Kaushik Jayaram", "Mechanical Engineering", "Bioinspired robotics, deployable mechanisms", "Lightweight embodied systems; prior Meta/Facebook gift signal.", ["perc"], 1],
    ["Bri-Mathias Hodge", "Civil, Environmental & Architectural Engineering", "Grid integration, energy storage for AI data centres", "Surfaced work on energy storage for AI data centres specifically.", ["infra"], 0],
    ["Kyri Baker", "Civil, Environmental & Architectural Engineering", "Grid-interactive systems, optimisation, storage", "Data-centre and grid integration, demand flexibility.", ["infra"], 0],
    ["Dejan Filipovic", "Electrical, Computer & Energy Engineering", "Antennas, RF systems, wideband communications", "Connectivity and network-adjacent communications; Reality Labs signal.", ["infra"], 1],
    ["Michael Toney", "Chemical & Biological Engineering", "Semiconductor, battery and energy materials", "Materials, energy storage and hardware reliability.", ["infra"], 0],
    ["Moncef Krarti", "Civil, Environmental & Architectural Engineering", "Building energy efficiency, renewable integration", "Data-centre energy efficiency and building-energy systems.", ["infra"], 0],
    ["Gregor Henze", "Civil, Environmental & Architectural Engineering", "Building-to-grid systems, energy control", "Operational energy optimisation for grid-interactive facilities.", ["infra"], 0],
    ["Michael McGehee", "Chemical & Biological Engineering", "Photovoltaics, tandem solar, energy materials", "Renewable procurement, power systems, energy-materials strategy.", ["infra"], 0],
    ["Ben Livneh", "CIRES", "Hydrology, climate-water systems", "Data-centre water stewardship, siting and climate-water risk.", ["infra"], 0],
    ["Casey Fiesler", "Information Science", "Tech ethics, online communities, responsible AI", "Strong trust and social-systems candidate; prior Facebook Research-funded work.", ["trust", "apps"], 1],
    ["Jed Brubaker", "Information Science", "Digital identity, memorialisation, content moderation", "Strongest formal Family-of-Apps and social-systems relationship node.", ["trust", "apps"], 1],
    ["Robin Burke", "Information Science", "Recommender fairness, user control, transparency", "Prior Meta consulting on recommendation and user-control features.", ["trust", "apps"], 1],
    ["Morgan Scheuerman", "Information Science", "Harmful content, severity frameworks, moderation", "Prior Facebook Research-funded harmful-content cluster.", ["trust"], 1],
    ["Stephen Voida", "Information Science", "Privacy, social computing, crisis informatics", "Prior Meta/Facebook proposal and faculty-reported relationship signals.", ["trust"], 1],
    ["Nathan Schneider", "Media Studies", "Platform and cooperative governance, platform economy", "Community support, online governance, non-adversarial design.", ["trust", "apps"], 0],
    ["Aaron Clauset", "BioFrontiers", "Information flow, networks, fairness", "Network dynamics, content exposure and social-platform measurement.", ["trust"], 0],
    ["Qin Lv", "Computer Science", "Social-media sensing, civic data systems", "Social-data infrastructure and privacy-aware platform analytics.", ["apps"], 0],
    ["Brian Keegan", "Information Science", "Platform migration, online-community behaviour", "Platform ecosystem dynamics and user migration.", ["apps"], 0],
    ["Erin Willis", "Advertising, PR & Media Design", "Influencer advertising, social marketing", "Creator economy, influencer marketing and monetisation ethics.", ["apps"], 0],
    ["Shaun Kane", "Computer Science", "Accessibility, assistive technology, AR coaching", "Very strong fit for accessible AR, smart glasses and inclusive XR.", ["ux"], 0],
    ["Laura Devendorf", "ATLAS Institute", "Smart textiles, interactive materials, co-design", "Wearables, soft interfaces and inclusive device design.", ["ux"], 0],
    ["Mirela Alistar", "ATLAS Institute", "HCI, embodied interaction, design research", "Exploratory interaction design and human-centered evaluation.", ["ux"], 0],
    ["Anu Sharma", "Speech, Language & Hearing Sciences", "Hearing, auditory processing, assistive audio", "Audio interfaces, hearing accessibility and captions for glasses.", ["ux"], 0],
    ["Kathryn Arehart", "Speech, Language & Hearing Sciences", "Speech intelligibility and quality metrics", "Smart-glasses audio, captions and speech-quality evaluation.", ["ux"], 0],
    ["Emily Moore", "Physics", "Accessible simulations, inclusive STEM learning", "Accessible learning, inclusive XR content and educational uses.", ["ux"], 0],
]

# --- SC: foresight scenarios ---------------------------------------------------
SC = [
    {"k": "A", "t": "AI glasses take off",
     "d": "AI infrastructure scales sufficiently, and consumer trust and adoption of smart glasses improves.",
     "l": "Lead with Reality Labs and wearables, displays, optics, HCI, accessibility, multimodal AI and human-centered evaluation.",
     "c": "Privacy, recording, youth, accessibility and social acceptability become core design issues.",
     "r": ["rl", "perc", "ux"]},
    {"k": "B", "t": "Infrastructure bottleneck",
     "d": "AI demand grows faster than power, cooling, water, grid and supply chains can support.",
     "l": "Lead with AI infrastructure, energy systems, water, cooling, grid integration, digital twins, photonics and efficient AI systems.",
     "c": "The university route may sit outside Meta’s academic partnerships function.",
     "r": ["infra", "perc"]},
    {"k": "C", "t": "Trust and regulation shock",
     "d": "Public, regulatory, youth, privacy or AI-safety events constrain product deployment.",
     "l": "Lead with trustworthy AI, recommender accountability, content provenance, privacy-preserving systems and youth wellbeing measurement.",
     "c": "This route is sensitive; poor framing could appear adversarial or reputationally risky.",
     "r": ["trust", "ai", "ux"]},
    {"k": "D", "t": "XR slow burn, AI acceleration",
     "d": "VR and MR headset demand remains uneven, but AI, software, open models and multimodal agents accelerate.",
     "l": "Lead with multimodal AI, agent evaluation, human-centered AI, open-model evaluation, visual AI and selected display capabilities.",
     "c": "Do not overinvest the pitch in metaverse or headset-centric framing.",
     "r": ["ai", "os", "perc"]},
]

# --- FM: foresight validation matrix -------------------------------------------
# [thrust zone, durability, evidence, CU alignment, route clarity, interpretation]
FM = [
    ["Reality Labs / AI glasses / wearables / displays", "High", "Strong", "High", "Medium-high", "Best first differentiated route. Frame as AI-native interaction, not metaverse."],
    ["Meta AI / agents / evaluation / open-weight models", "High", "Strong", "High", "Medium", "Strong route, but too broad unless narrowed to evaluation, agents, safety, multimodal AI and human-centered deployment."],
    ["AI infrastructure / data centres / energy / water / cooling", "Very high", "Very strong", "High", "Low-medium", "Strategically important but route-uncertain. Ask Meta whether there is a university-facing infrastructure route."],
    ["Trust / privacy / safety / youth / platform integrity", "High", "Strong", "High", "Low-medium", "Important but sensitive. Frame as technical evaluation, safety-by-design, privacy-preserving systems and wellbeing measurement."],
    ["Family of Apps / ads / recommendations / discovery", "Medium-high", "Strong", "Medium-high", "Low", "Business-critical but proprietary-data-sensitive. Use only if Meta raises product, ads, discovery or recommender control."],
    ["Open-source AI ecosystem / developer tools", "Medium-high", "Moderate", "Medium", "Medium", "Useful secondary route around Llama/PyTorch use, reproducibility, open evaluation, domain-specific models and talent."],
    ["Sustainability / circularity / responsible supply chain", "Medium", "Moderate", "Medium-high", "Low-medium", "Valuable if tied to data centres, wearables, electronics, materials or water. Too broad if framed as sustainability generally."],
]

# --- W: early-warning indicators -----------------------------------------------
# [indicator, why it matters, route affected]
W = [
    ["New Meta or Reality Labs university RFPs, invite-only calls, workshops, or sponsored research mechanisms", "Confirms whether alignment can become engagement", "All routes"],
    ["Meta AI / MSL / FAIR hiring in evaluation, post-training, safety, multimodal AI, agents and Llama", "Shows current team demand and vocabulary", "Meta AI"],
    ["Reality Labs hiring and patents in smart glasses, EMG, haptics, optics, displays, sensors, accessibility", "Shows whether Reality Labs remains university-routeable", "Wearables / XR"],
    ["Meta capex revisions, data-centre commitments, grid interconnection issues, energy procurement, cooling announcements", "Indicates whether infrastructure is becoming a stronger route", "AI infrastructure"],
    ["Water-restoration, water-use, digital-twin and data-centre cooling disclosures", "Indicates whether water and cooling are moving into technical partnership space", "Water / cooling"],
    ["EU and US youth, privacy, AI and content-provenance regulation", "Could accelerate need for independent measurement and safety-by-design", "Trust / safety"],
    ["Llama release cadence, safety disclosures, third-party evaluations, licensing changes", "Indicates open-model strategy and academic collaboration potential", "Meta AI / open source"],
    ["XR and smart-glasses shipment and adoption data", "Validates or weakens the AI-glasses route", "Reality Labs / wearables"],
    ["Alumni movements and CU student/postdoc placements into Meta route teams", "Indicates warm-path and talent-pipeline value", "Routing"],
]

# --- Company-signal figures (from the HTML's company() function) ---------------
SEGMENT_SHARE = [["Family of Apps", 198.759, "98.9%"], ["Reality Labs", 2.207, "1.1%"]]
XR_SHARE = [["Meta", 72.2, "72.2%"], ["Rest of market", 27.8, ""]]
SEGMENT_ECONOMICS = [
    ["Family of Apps", "$198.8B", "+$102.5B"],
    ["Reality Labs", "$2.2B", "−$19.2B"],
    ["2026 capex guidance", "$125B – $145B", None],
]
FIN_YEARS = ["FY2023", "FY2024", "FY2025"]
FIN_REVENUE = [134.9, 164.5, 201.0]
FIN_NET_INCOME = [39.1, 62.4, 75.7]

# Route label order used by the jobs-vs-patents chart in section 3
JP_LABELS = [
    ["infra", "AI infrastructure"], ["rl", "Reality Labs / XR"], ["apps", "Family of Apps"],
    ["ai", "Meta AI / agents"], ["trust", "Trust / privacy"], ["perc", "Multimodal perception"],
    ["ux", "UX / accessibility"], ["biz", "Business / corporate"], ["unc", "Uncoded"],
]

# Unclassified funding row in section 4
FUND_UNCLASSIFIED = [357316, 391066]
# "No strategic-route equivalent" row in the route-strength matrix
RMX_NO_EQUIV = {"grants": 9, "faculty": 4, "scholarly": None, "alumni": 49}

# Section-2 stream denominators, from the HTML's routeDetail() function
STREAM_TOTALS = {
    "Meta job postings": 293, "Meta patents": 450, "Awarded grant records": 14,
    "Proposed grant records": 14, "Faculty-reported activities": 22,
    "Confirmed scholarly signals": 11, "Alumni by job function": 39,
}
