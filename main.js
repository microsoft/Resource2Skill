// Resource2Skill — project page gallery renderer.

const motionPreference = typeof window.matchMedia === "function"
  ? window.matchMedia("(prefers-reduced-motion: reduce)")
  : null;

const motionState = (() => {
  let enabled = !motionPreference?.matches;
  let userOverride = false;
  const listeners = new Set();

  const reflect = () => {
    if (document.documentElement) {
      document.documentElement.dataset.motion = enabled ? "enabled" : "paused";
    }
  };

  const api = {
    isEnabled: () => enabled,
    setEnabled(next, options = {}) {
      const value = Boolean(next);
      if (options.userInitiated) userOverride = true;
      if (value === enabled) return;
      enabled = value;
      reflect();
      if (!enabled) pauseAutoplayMedia();
      listeners.forEach(listener => listener(enabled));
    },
    subscribe(listener) {
      listeners.add(listener);
      return () => listeners.delete(listener);
    }
  };

  reflect();
  const handlePreferenceChange = event => {
    if (!userOverride) api.setEnabled(!event.matches);
  };
  if (motionPreference) {
    if (typeof motionPreference.addEventListener === "function") {
      motionPreference.addEventListener("change", handlePreferenceChange);
    } else if (typeof motionPreference.addListener === "function") {
      motionPreference.addListener(handlePreferenceChange);
    }
  }
  window.Resource2SkillMotion = api;
  return api;
})();

const assetBase = "assets/videos/";
const audioBase = "assets/audio/";
// Bump when clip *content* changes under an unchanged filename (e.g. the PPT
// recipe re-render) so browsers/CDN don't serve a stale cached copy.
const assetVer = "?v=20260625-ppt-recipe-33";
const psychedelicRockAudio = "psychedelic-rock-with-skills.mp3";
const blackArtistChipmunkSoulAudio = "black-artist-chipmunk-soul.mp3";
const trapMoonlitAudio = "trap-moonlit.mp3";
const synthwaveNeonChaseAudio = "synthwave-neon-chase.mp3";
const jazzPianoAfterhoursAudio = "jazz-piano-afterhours.mp3";
const dnbCityRunnerAudio = "dnb-city-runner.mp3";
const psychedelicRockAudioWithout = "psychedelic-rock-without-skills.mp3";

const heroReelClips = [
  { src: "ppt_esports_series_a_with.mp4", label: "PowerPoint — esports Series A deck" },
  { src: "web_sequoia-bed-command-center_with.mp4", label: "Web — command-center UI" },
  { src: "audio_synthwave_retro_with.mp4", label: "Reaper — synthwave arrangement" },
  { src: "excel_crypto_trading_pnl_with.mp4", label: "Excel — crypto trading P&L" },
  { src: "blender_supercar_with.mp4", label: "Blender — electric supercar render" }
];

const taxonomySections = [
  {
    domain: "web",
    title: "Web Pages",
    chip: "HTML / CSS / JS",
    output: "Live HTML pages",
    description: "Agent browses the web-domain skill wiki, composes layout primitives, and emits a static site with real CSS animations.",
    items: [
      { src: "web_yarrow-culture-190.mp4",  caption: "Boutique cultural-archive landing — skill-driven editorial layout" },
      { src: "web_silt-portfolio-184.mp4",  caption: "Designer portfolio assembled from layout-primitive skills" },
      { src: "web_obsidian-fintech-94.mp4", caption: "Fintech product page with skill-composed hero + data sections" },
      { src: "web_plinth-travel-161.mp4",   caption: "Travel platform landing — skill-composed gallery + CTA" },
      { src: "web_notch-portfolio-295.mp4", caption: "Designer portfolio with skill-composed scroll narrative" },
      { src: "web_harbor-beverage-72.mp4",  caption: "Beverage brand site with skill-driven scrolling story" }
    ]
  },
  {
    domain: "powerpoint",
    title: "PowerPoint Decks",
    chip: "PPTMaster SVG",
    output: "Editable .pptx files",
    description: "Real GPT-5.5 agents use PPTMaster's SVG-first backend; R2S references add visual mechanisms without fixing the deck template.",
    items: [
      {
        src: "pptmaster_r2s_real_agent_compare.mp4",
        caption: "PPTMaster SVG backend: real agent w/o vs w R2S on restaurant, kids science, and financial deck prompts"
      }
    ]
  },
  {
    domain: "blender",
    title: "Blender Scenes",
    chip: "bpy",
    output: ".blend + rendered images",
    description: "Agent assembles Blender scenes by browsing skills for materials, lighting, camera moves, and modifiers — then renders.",
    items: [
      { src: "blender_ramen_bowl_closeup.mp4",         caption: "Photoreal ramen-bowl close-up assembled from skill recipes" },
      { src: "blender_lightning-high-contrast-162.mp4",caption: "High-contrast lightning scene composed via skill lookups" },
      { src: "blender_helmet-vehicle-9.mp4",           caption: "Mech helmet/vehicle composition with skill-driven materials" },
      { src: "blender_neon-isometric-76.mp4",          caption: "Neon isometric scene assembled from skill snippets" },
      { src: "blender_samurai-hand-painted-141.mp4",   caption: "Hand-painted samurai character with skill-driven shading" }
    ]
  },
  {
    domain: "excel",
    title: "Excel Workbooks",
    chip: "openpyxl",
    output: ".xlsx workbooks",
    description: "Agent emits multi-sheet workbooks: formulas, pivots, formatting, charts — driven by Excel-domain skill recipes.",
    items: [
      { src: "excel_food-delivery-orders-v139.mp4", caption: "Food-delivery orders workbook with multi-tab analytics" },
      { src: "excel_university-grades-v41.mp4",     caption: "University grades & analytics workbook" },
      { src: "excel_data-pipeline-runs-v106.mp4",   caption: "Data-pipeline run-history workbook with cross-sheet refs" }
    ]
  },
  {
    domain: "audio",
    title: "REAPER-style Audio",
    chip: "MIDI + WAV",
    output: ".mid / .wav projects",
    description: "Agent browses music-production skills (chord progressions, rhythm, mixing recipes), emits MIDI, and renders to WAV.",
    items: [
      { src: "audio_psychedelic_rock_case.mp4", audio: psychedelicRockAudio, caption: "Psychedelic rock (G minor, 150 BPM) — rendered MIDI/WAV arrangement" },
      { src: "audio_black_artist_chipmunk_soul_case.mp4", audio: blackArtistChipmunkSoulAudio, caption: "Black-artist-inspired chipmunk-soul throwback - chopped groove render" },
      { src: "audio_trap_moonlit_case.mp4", audio: trapMoonlitAudio, caption: "Moonlit trap sketch — 808-driven beat with sparse melodic layers" },
      { src: "audio_synthwave_neon_chase_case.mp4", audio: synthwaveNeonChaseAudio, caption: "Synthwave neon chase — retro arps, bass pulse, and drum-machine structure" },
      { src: "audio_jazz_piano_afterhours_case.mp4", audio: jazzPianoAfterhoursAudio, caption: "Jazz piano afterhours — late-night comping and harmonic color" },
      { src: "audio_dnb_city_runner_case.mp4", audio: dnbCityRunnerAudio, caption: "DnB city runner — fast breakbeat energy with bass motion" }
    ]
  }
];

const featuredDemos = [
  {
    domain: "Web",
    title: "Interactive marketing page",
    src: "web_obsidian-fintech-94.mp4",
    note: "A static HTML/CSS/JS product page composed from layout, hero, metric-card, and CTA skills."
  },
  {
    domain: "PowerPoint",
    title: "PPTMaster SVG backend",
    src: "pptmaster_r2s_real_agent_compare.mp4",
    note: "Real GPT-5.5 agent runs with strict layout validation: open PPTMaster baseline vs prompt-specific R2S-enhanced editable .pptx decks."
  },
  {
    domain: "Excel",
    title: "Analytics workbook",
    src: "excel_food-delivery-orders-v139.mp4",
    note: "A multi-sheet workbook with formulas, tables, formatting, and rendered chart outputs."
  },
  {
    domain: "Blender",
    title: "3D scene construction",
    src: "blender_ramen_bowl_closeup.mp4",
    note: "A Blender scene assembled from lighting, material, camera, and composition recipes."
  },
  {
    domain: "Audio",
    title: "Rendered music project",
    src: "audio_psychedelic_rock_case.mp4",
    audio: psychedelicRockAudio,
    note: "A MIDI/WAV arrangement rendered and visualized from generated audio artifacts."
  }
];

const comparisonCases = [
  { domain: "PowerPoint", title: "AI Safety Research Keynote", stem: "ppt_ai_safety_keynote", note: "With R2S a GPT-5.4 designer rebuilds the four content slides from distilled wiki skills (Modular Technical Architecture Layout + Progressive Reveal Flowchart), laying out this deck's own content in each skill's style; without R2S the same brief stays a plain PPT Master template.", sources: [{"vid": "yhvQ5csqD2s", "title": "Architecture Diagram PowerPoint Presentation", "channel": "SlideEgg"}, {"vid": "aNEFnrkAsuo", "title": "學術簡報案例：複雜流程圖該如何設計｜10 分鐘學簡報 #084 #學術簡報 #流程圖", "channel": "簡報藝術烘焙坊 SlideArt"}, {"vid": "h51DktZw-WQ", "title": "How To Create Architecture Design Presentation on Microsoft Powerpoint", "channel": "How To Media"}, {"vid": "fijZPi26lKs", "title": "Architecture Presentation Tips | 4 FUNDAMENTAL Principles", "channel": "DamiLee"}] },
  { domain: "PowerPoint", title: "Northstar Coffee Rebrand Pitch", stem: "ppt_creative_agency_rebrand", note: "With R2S a GPT-5.4 designer rebuilds the four content slides from distilled wiki skills (Curated Identity Moodboard Grid + Editorial Magazine Split-Grid & Color Block), laying out this deck's own content in each skill's style; without R2S the same brief stays a plain PPT Master template.", sources: [{"vid": "xAEZlJe3MrU", "title": "我用 Lovart 做設計，結果比專業設計師還好！一隻影片教你如何用 Lovart做設計", "channel": "李厂长来了"}, {"vid": "D8Me_lvbtrU", "title": "HOERA Magazine - Powerpoint Template", "channel": "Norma Daenna"}, {"vid": "qwOqPo8liqM", "title": "How To Mask Text in PowerPoint (FAST & EASY) | 100% WORKS | NO Yapping", "channel": "Guide Hub (2026 WORKING GUIDES)"}, {"vid": "fSGO_DmdjjI", "title": "How to create a custom color palette in PowerPoint", "channel": "PoweredTemplate.com"}] },
  { domain: "PowerPoint", title: "Vector Arena Series A", stem: "ppt_esports_series_a", note: "With R2S a GPT-5.4 designer rebuilds the four content slides from distilled wiki skills (Neon Circular Hub Team Roster + Neon Glow Data Dashboard), laying out this deck's own content in each skill's style; without R2S the same brief stays a plain PPT Master template.", sources: [{"vid": "o0JOAUFbIdo", "title": "🔥Best Team Introduction PowerPoint🔥| 🔥Team Introduction Presentation🔥", "channel": "Clean Powerpoint Studio"}, {"vid": "xxs3rKIa5kE", "title": "无论是作为学习素材还是直接套用，这个仪表板你值得拥有~", "channel": "布衣公子PPT"}, {"vid": "uxhCnoU5MAk", "title": "How to make animation round diagonal corner in PowerPoint", "channel": "F J"}, {"vid": "upHH5jslZLE", "title": "Section Breaker PowerPoint Templates", "channel": "Warna Slides - Multi-Purpose PowerPoint Template"}] },
  { domain: "PowerPoint", title: "PulsePatch 510(k) Readiness Review", stem: "ppt_healthtech_device_approval", note: "With R2S a GPT-5.4 designer rebuilds the four content slides from distilled wiki skills (Minimalist \"High Data-Ink\" Dashboard Panel + Tiered Feature Comparison Grid), laying out this deck's own content in each skill's style; without R2S the same brief stays a plain PPT Master template.", sources: [{"vid": "5pCdw-PV0Js", "title": "🚨 YOU'RE VISUALIZING YOUR DATA WRONG. And Here's Why...", "channel": "Adam Finer - Learn BI"}, {"vid": "Ne0y_NINzk0", "title": "Product Capability Comparison Powerpoint Ppt Template Bundles", "channel": "SlideTeam"}, {"vid": "G3l47G9Z6mw", "title": "How to Create Gantt Charts in PowerPoint", "channel": "SlideBazaar - PowerPoint Tutorials"}, {"vid": "cfccmFfD1Xg", "title": "How to Create This AWESOME Comparison Slide in PowerPoint #powerpointa", "channel": "SlideUpLift"}] },
  { domain: "PowerPoint", title: "How Satellites Help Earth", stem: "ppt_kids_space_science_lesson", note: "With R2S a GPT-5.4 designer rebuilds the four content slides from distilled wiki skills (Animated Process Trajectory + Semantic Logic Flowchart), laying out this deck's own content in each skill's style; without R2S the same brief stays a plain PPT Master template.", sources: [{"vid": "X8xl_oR7B1M", "title": "What Is a Motion Path in PowerPoint?", "channel": "Envato Tuts+"}, {"vid": "UlAHtHlMCos", "title": "How to Create Flowchart in Microsoft Word", "channel": "Office Master Tutorials"}, {"vid": "d25sLKnjau8", "title": "Intro TCP/IP 3: How to determine the number of networks in a network d", "channel": "Cisco Mmu"}, {"vid": "h4qJjW7lIsk", "title": "How to make your employees feel important | Employee Spotlight Tips", "channel": "Vantage Circle"}] },
  { domain: "PowerPoint", title: "Literacy Forward Annual Impact", stem: "ppt_nonprofit_annual_impact", note: "With R2S a GPT-5.4 designer rebuilds the four content slides from distilled wiki skills (Minimalist Rule of Thirds Data Storytelling Layout + High-Impact Geometric Quote Reveal), laying out this deck's own content in each skill's style; without R2S the same brief stays a plain PPT Master template.", sources: [{"vid": "TQiln3CjtvM", "title": "5 QUICK Ways to Improve Your PowerPoint Design", "channel": "Leila Gharani"}, {"vid": "tHFC0q6AmFM", "title": "Make AWESOME Quotes in PowerPoint 🔥 Easy Tutorial", "channel": "Slides by Sander"}, {"vid": "gKIZ09Kdk8Q", "title": "How to Drastically Improve Your KPI Presentations (in PowerPoint or Ke", "channel": "Aaron Lympany Design"}, {"vid": "2eLm7AiWQzA", "title": "Animated PowerPoint Timeline Slide Design Tutorial", "channel": "POWERPOINT UNIVERSITY"}] },
  { domain: "PowerPoint", title: "Hillside Modern Listing", stem: "ppt_real_estate_hillside_listing", note: "With R2S a GPT-5.4 designer rebuilds the four content slides from distilled wiki skills (Explanatory Storytelling Dashboard + 4-Column Image Gallery), laying out this deck's own content in each skill's style; without R2S the same brief stays a plain PPT Master template.", sources: [{"vid": "OYbPOhK0wPo", "title": "Telling a Story with Data | Dashboard Build Demo", "channel": "Maven Analytics"}, {"vid": "wIR7foez8lk", "title": "Monthly Business Review | PowerPoint Presentation Template", "channel": "Creative Presentation Ideas by infoDiagram"}] },
  { domain: "PowerPoint", title: "Juniper Lunch Counter Launch", stem: "ppt_restaurant_lunch_counter", note: "With R2S a GPT-5.4 designer rebuilds the four content slides from distilled wiki skills (Editorial Blueprint Grid + Whimsical Illustrated Map Infographic), laying out this deck's own content in each skill's style; without R2S the same brief stays a plain PPT Master template.", sources: [{"vid": "D-q5SKSNIR8", "title": "12 编辑设计（排版）（排版需要注意的文字和图片问题）", "channel": "Aworkzon"}, {"vid": "2003uzZaonQ", "title": "AI22 | [Explosive] Gemini 3 & NotebookLM directly generate high-qualit", "channel": "Meiko微課頻道"}, {"vid": "aCwrkeWsLHQ", "title": "5个易学技巧，教你做出有设计感的PPT！【经本正一】", "channel": "经本正一"}, {"vid": "uVTGvhw4I30", "title": "How to Make Business Review in PowerPoint", "channel": "Creative Presentation Ideas by infoDiagram"}] },
  { domain: "Blender", title: "Sci-Fi Docking Bay", stem: "blender_space_bay", note: "With skills adds layered hard-surface panels and guide lighting; without skills stays closer to a simple glowing box bay.", sources: [{"vid": "KTWo-iEvEB8", "title": "Boolean Modifier 2.8x | Hard-surface Modeling Update", "channel": "Gleb Alexandrov"}, {"vid": "2SiCtnXVVFw", "title": "The Best Volumetric Fog Shader (Blender Tutorial)", "channel": "Lane Wallace"}, {"vid": "OHA5rcw2qnI", "title": "How to make Glow Effect with Blender Glow Material", "channel": "blenderian"}, {"vid": "VxDEtL0WyOQ", "title": "How to Light an Interior Scene at Night in Blender (Easy Tutorial) in ", "channel": "Kailash Tutorials "}] },
  { domain: "Blender", title: "Isometric Garden", stem: "blender_iso_garden", note: "With skills produces a colorful composed diorama with pond, bridge, and soft lighting; without skills reads as a rough monochrome clay blockout.", sources: [{"vid": "mvE_TykzJQU", "title": "Essential Tips for Low Poly Scenes - Blender Tutorial", "channel": "Grant Abbitt (Gabbitt)"}, {"vid": "K8LVFNVLlYc", "title": "How to make next-level procedural materials in Blender", "channel": "Robin Squares"}, {"vid": "5yIURiec0K8", "title": "Easy Realistic Architecture And Environments In Blender - Beginner tut", "channel": "AlternaVision Studio"}, {"vid": "BWmwmF0QOzA", "title": "How to Add Volumetric Lighting in Blender (God Rays) (Fog)", "channel": "Bak3 Designs"}] },
  { domain: "Blender", title: "Electric Supercar", stem: "blender_supercar", note: "With skills forms a recognizable low wedge car with reflective paint and LED accents; without skills remains a looser studio blockout.", sources: [{"vid": "b_4FoNTHf5g", "title": "Mark Sharp vs. Crease vs. Seam vs. Bevel Weight vs.Weighted Normals - ", "channel": "Ryuu - Blender Bros"}, {"vid": "RAY88EMOC6Y", "title": "How To Make Realistic Car Paint | Blender Tutorial", "channel": "Enhanced Sight"}, {"vid": "4Uy2SzB-Kuk", "title": "Three Point Lighting Tutorial | Blender Product Rendering Series", "channel": "blenderisms"}] },
  { domain: "Blender", title: "Neon Open Sign", stem: "blender_neon_open", note: "With skills creates a clean tube sign with magenta/cyan wall lighting; without skills becomes a rough illuminated sign blockout.", sources: [{"vid": "6wuOsRkYhYU", "title": "how to make a neon text in blender in 1 minute", "channel": "blender basics"}, {"vid": "m55WW6lyScM", "title": "Glowing Edge Shader in Blender (Easy Node Setup!) | Blender Tutorial", "channel": "Blender Express"}, {"vid": "2SiCtnXVVFw", "title": "The Best Volumetric Fog Shader (Blender Tutorial)", "channel": "Lane Wallace"}, {"vid": "g3J89WPubPs", "title": "Interior Lights in Blender", "channel": "coral lab"}] },
  { domain: "Blender", title: "Observatory God Rays", stem: "blender_observatory_godrays", note: "With skills, the observatory gains book-lined architectural detail and atmosphere; without skills, it stays sparse and generic.", sources: [{"vid": "kxKUnQLn8cQ", "title": "How to Create Photorealistic Interior Lighting in Blender", "channel": "coral lab"}, {"vid": "wrzSrjAY69c", "title": "How to Make Interiors in Blender (Tutorial)", "channel": "Blender Guru"}, {"vid": "nQaUsgf9ZUg", "title": "Beginners Guide To Texturing In Blender | How To Procedural Texture AN", "channel": "NoPoly"}] },
  { domain: "Blender", title: "Drone Hangar", stem: "blender_drone_hangar", note: "With skills, the drone has worn metal, steam, and hangar mood; without skills, it remains a clean primitive blockout.", sources: [{"vid": "KTWo-iEvEB8", "title": "Boolean Modifier 2.8x | Hard-surface Modeling Update", "channel": "Gleb Alexandrov"}, {"vid": "hAWLqRpzK6I", "title": "3 Easy steps to make Realistic Materials", "channel": "Jamie Dunbar"}, {"vid": "pcBji0dSc8o", "title": "Take Your Blender Camera Animation to the Next Level", "channel": "Florin Flammer"}] },
  { domain: "Excel", title: "HR People Ops", stem: "excel_hr_people_ops", note: "With skills uses a compact blue people-ops KPI dashboard; without skills renders a heavier table-first dashboard with less consistent layout.", sources: [{"vid": "hxaflJodZsA", "title": "", "channel": "Office Tech Skill"}] },
  { domain: "Excel", title: "Battery Lab Characterization", stem: "excel_battery_lab_characterization", note: "With skills produces a technical KPI/degradation dashboard; without skills exposes broken formula cells in a flatter lab summary.", sources: [{"vid": "hxaflJodZsA", "title": "", "channel": "Office Tech Skill"}] },
  { domain: "Excel", title: "Sales Pipeline Tracker", stem: "excel_sales_pipeline_tracker", note: "With skills gives a polished CRM dashboard with KPI cards and funnel visuals; without skills is a simpler summary table and chart layout.", sources: [{"vid": "1ic8E58Bo2M", "title": "", "channel": "MyOnlineTrainingHub"}] },
  { domain: "Excel", title: "Agency Creative Briefs", stem: "excel_agency_creative_briefs", note: "With skills adds a dark KPI strip and AR/project mix panels; without skills stays closer to small summary tables.", sources: [{"vid": "MTlQvyNQ3PM", "title": "📊 How to Build Excel Interactive Dashboards", "channel": "Kevin Stratvert"}] },
  { domain: "Excel", title: "Retail Inventory Movement", stem: "excel_retail_inventory_movement", note: "With skills turns inventory movement into a dense KPI/category/stockout dashboard; without skills is a plainer turnover table summary." },
  { domain: "Excel", title: "Crypto Trading P&L", stem: "excel_crypto_trading_pnl", note: "With skills uses a dark trading-board style with conditional P&L coloring; without skills reads more like a ledger summary.", sources: [{"vid": "Iiq4Sem9GPM", "title": "", "channel": "Kenji Explains"}] },
  { domain: "Excel", title: "Data Pipeline Incident Kanban", stem: "excel_data_pipeline_incident_kanban", note: "With skills uses a true Kanban-derived incident board and KPI dashboard; without skills is a much thinner, more mechanical board/dashboard build.", sources: [{"vid": "SMFmzstfJ4k", "title": "Excel教學 | Excel制作的敏捷看板，可视化管理工作任务", "channel": "千万别学Excel"}, {"vid": "hxaflJodZsA", "title": "", "channel": "Office Tech Skill"}] },
  { domain: "Excel", title: "Construction Site Progress", stem: "excel_construction_site_progress", note: "With skills produces a cleaner KPI-led progress dashboard with structured phase and crew analysis; without skills is more table-heavy and less visually organized." },
  { domain: "Web", title: "Ferry Advocacy Homepage", stem: "web_tideway-ferry", note: "With skills produces a coherent civic campaign landing page; without skills collapses into a garbled, overflowing constructivist layout.", sources: [{"vid": "oqPbciDKi44", "title": "Build a Complete Responsive Personal Portfolio Website using HTML CSS ", "channel": "Amna Code"}, {"vid": "WhBp2MplJQA", "title": "How To Make A Responsive Pricing Table Desig Using HTML And CSS | Attr", "channel": "Study Web Today"}, {"vid": "cJ10BYWNPns", "title": "7 CRUCIAL Things Every SaaS Landing Page Should Have (with examples)", "channel": "Rob Walling"}, {"vid": "At4B7A4GOPg", "title": "Responsive Navbar Tutorial", "channel": "Web Dev Simplified"}] },
  { domain: "Web", title: "Risk Monitoring Dashboard", stem: "web_lumen-risk-dashboard", note: "With skills renders a fixed-sidebar fintech risk console; without skills breaks into overlapping narrow dashboard columns.", sources: [{"vid": "xR23ktLwvrg", "title": "CSS Grid - Create a FULL-HEIGHT RESPONSIVE Layout in Minutes", "channel": "Optimistic Web"}, {"vid": "PXiMfLiqcpg", "title": "Responsive Project Dashboard // Speedrun // HTML & CSS Tutorial", "channel": "crayon code"}, {"vid": "B7k5rOgmOGY", "title": "EVERYTHING you need to know to build a Dashboard UI in 8 minutes (begi", "channel": "Kole Jain"}, {"vid": "At4B7A4GOPg", "title": "Responsive Navbar Tutorial", "channel": "Web Dev Simplified"}] },
  { domain: "Web", title: "Moderation Queue", stem: "web_meridian-content-moderation", note: "With skills creates a compact trust-and-safety command dashboard; without skills becomes a sparse, horizontally broken moderation page.", sources: [{"vid": "lCYY2t6BRSI", "title": "React CSS Grid Responsive Dashboard Tutorial | Build Adaptive Layouts ", "channel": "GoPlusPlus"}, {"vid": "B7k5rOgmOGY", "title": "EVERYTHING you need to know to build a Dashboard UI in 8 minutes (begi", "channel": "Kole Jain"}, {"vid": "At4B7A4GOPg", "title": "Responsive Navbar Tutorial", "channel": "Web Dev Simplified"}, {"vid": "FaMW-CtExrs", "title": "Responsive Number Counting Animation | HTML, CSS & Javascript", "channel": "Coding Artist"}] },
  { domain: "Web", title: "Incident Room", stem: "web_cinder-incident-room", note: "With skills gives a usable SOC incident command room; without skills falls back to a thin, generic incident page with poor layout density.", sources: [{"vid": "xR23ktLwvrg", "title": "CSS Grid - Create a FULL-HEIGHT RESPONSIVE Layout in Minutes", "channel": "Optimistic Web"}, {"vid": "NnniXasJIpY", "title": "Responsive Dashboard Layouts with CSS Grid", "channel": "ByteGrad"}, {"vid": "FaMW-CtExrs", "title": "Responsive Number Counting Animation | HTML, CSS & Javascript", "channel": "Coding Artist"}] },
  { domain: "Web", title: "Ravel Customs Clearance", stem: "web_ravel-customs-clearance-board", note: "With skills builds a dense customs-ops board with risk heatmaps and queues; without skills is much sparser and loses the command-center feel.", sources: [{"vid": "xR23ktLwvrg", "title": "CSS Grid - Create a FULL-HEIGHT RESPONSIVE Layout in Minutes", "channel": "Optimistic Web"}, {"vid": "oqPbciDKi44", "title": "Build a Complete Responsive Personal Portfolio Website using HTML CSS ", "channel": "Amna Code"}, {"vid": "NY9ojDOjOcw", "title": "", "channel": "Echoes of Ping"}, {"vid": "lCYY2t6BRSI", "title": "React CSS Grid Responsive Dashboard Tutorial | Build Adaptive Layouts ", "channel": "GoPlusPlus"}] },
  { domain: "Web", title: "Sequoia Bed Command", stem: "web_sequoia-bed-command-center", note: "With skills reads as a compact clinical bed-management console; without skills falls back toward a simpler generic hospital dashboard.", sources: [{"vid": "NnniXasJIpY", "title": "Responsive Dashboard Layouts with CSS Grid", "channel": "ByteGrad"}, {"vid": "B7k5rOgmOGY", "title": "EVERYTHING you need to know to build a Dashboard UI in 8 minutes (begi", "channel": "Kole Jain"}, {"vid": "xR23ktLwvrg", "title": "CSS Grid - Create a FULL-HEIGHT RESPONSIVE Layout in Minutes", "channel": "Optimistic Web"}, {"vid": "At4B7A4GOPg", "title": "Responsive Navbar Tutorial", "channel": "Web Dev Simplified"}] },
  { domain: "Web", title: "Forge GMP Batch Release", stem: "web_forge-gmp-batch-release", note: "With skills includes regulated manufacturing panels and audit/checklist structure; without skills is thinner and less domain-specific.", sources: [{"vid": "xR23ktLwvrg", "title": "CSS Grid - Create a FULL-HEIGHT RESPONSIVE Layout in Minutes", "channel": "Optimistic Web"}, {"vid": "B7k5rOgmOGY", "title": "EVERYTHING you need to know to build a Dashboard UI in 8 minutes (begi", "channel": "Kole Jain"}, {"vid": "PXiMfLiqcpg", "title": "Responsive Project Dashboard // Speedrun // HTML & CSS Tutorial", "channel": "crayon code"}, {"vid": "At4B7A4GOPg", "title": "Responsive Navbar Tutorial", "channel": "Web Dev Simplified"}] },
  { domain: "Web", title: "Patina Studies Numismatics", stem: "web_patina-studies-rare-coin-h8", note: "With skills delivers a bolder manga-noir coin valuation page; without skills is competent but less visually distinctive.", sources: [{"vid": "cJ10BYWNPns", "title": "7 CRUCIAL Things Every SaaS Landing Page Should Have (with examples)", "channel": "Rob Walling"}, {"vid": "WhBp2MplJQA", "title": "How To Make A Responsive Pricing Table Desig Using HTML And CSS | Attr", "channel": "Study Web Today"}, {"vid": "At4B7A4GOPg", "title": "Responsive Navbar Tutorial", "channel": "Web Dev Simplified"}, {"vid": "aLZCG8XMM_s", "title": "Best Hero Layout Inspiration of 2026", "channel": "Codex Community"}] },
  { domain: "Audio", title: "J Dilla Boom-Bap", note: "With skills layers lo-fi coordinator, boom-bap drums, neo-soul Rhodes, and additive arrangement; without skills is a simpler hand-built MPC groove.", kind: "audio", visualWith: "audio_jdilla_boom_bap_with.mp4", visualWithout: "audio_jdilla_boom_bap_without.mp4", audioAfter: "audio_jdilla_boom_bap_with.mp3", audioBefore: "audio_jdilla_boom_bap_without.mp3", sources: [{"vid": "hEKdtLwQtBY", "title": "How to write a Lofi drum pattern in Reaper", "channel": "nanee "}, {"vid": "nEQhlIxKNFQ", "title": "The 3 Vital Steps To Make Neo Soul Beats in 2024!", "channel": "Hix"}, {"vid": "4CGBBV_5srQ", "title": "Beat Arrangement Tips - Turn Your Loop Into a Full Beat!", "channel": "K. Hart"}] },
  { domain: "Audio", title: "French House", note: "With skills uses French-touch groove, sidechain, and vocoder references; without skills is a cleaner manual disco-stab arrangement.", kind: "audio", visualWith: "audio_french_house_with.mp4", visualWithout: "audio_french_house_without.mp4", audioAfter: "audio_french_house_with.mp3", audioBefore: "audio_french_house_without.mp3", sources: [{"vid": "TleGFlZioew", "title": "How To Daft Punk (Random Access Memories)", "channel": "Talha Vocoding"}, {"vid": "Lhfmcw9nQHg", "title": "", "channel": "The Ultimate Mixdown"}] },
  { domain: "Audio", title: "Synthwave Retrowave", note: "With skills adds synthwave ensemble, lush pad, glide lead, and transition references; without skills relies on direct primitive sequencing.", kind: "audio", visualWith: "audio_synthwave_retro_with.mp4", visualWithout: "audio_synthwave_retro_without.mp4", audioAfter: "audio_synthwave_retro_with.mp3", audioBefore: "audio_synthwave_retro_without.mp3", sources: [{"vid": "bc58K9a_kW4", "title": "", "channel": "Reapertips | Alejandro"}, {"vid": "gK_jgUtBOos", "title": "Synthwave Song Structure And The 8 Bar Rule (Keep People Listening)", "channel": "Orpheus Audio Academy"}, {"vid": "7qQX6YGBQEA", "title": "Free Vital Synth - Full Tutorial", "channel": "In The Mix"}, {"vid": "GlCJ1UYjuDo", "title": "Creating a Synth Preset (ReaSynth) in REAPER", "channel": "REAPER Mania"}] },
  { domain: "Audio", title: "Bossa Nova", note: "With skills adapts bossa rhythm, comping, bass, and melody references; without skills uses a straightforward hand-authored bossa groove.", kind: "audio", visualWith: "audio_bossa_nova_with.mp4", visualWithout: "audio_bossa_nova_without.mp4", audioAfter: "audio_bossa_nova_with.mp3", audioBefore: "audio_bossa_nova_without.mp3", sources: [{"vid": "5k4eNvOT6x0", "title": "How to play Bossa Nova in a minute", "channel": "Hello Foe!"}, {"vid": "VfOvhlUn0Jw", "title": "How to Play Bossa Nova (Comping Patterns, Chords, Songs)", "channel": "Learn Jazz Standards"}, {"vid": "IF5jy4qLX_I", "title": "Basic Bossa Nova Rhythm Arrangement Tutorial", "channel": "Reuben Chng"}, {"vid": "32_YePbe-BE", "title": "How To Make Better Melodies", "channel": "Emil Ludvigsen"}] },
  { domain: "Audio", title: "Future Bass Drop", note: "With skills adds a sidechained supersaw drop, risers, and low-end structure; without skills is flatter and less layered.", kind: "audio", visualWith: "audio_future_bass_drop_with.mp4", visualWithout: "audio_future_bass_drop_without.mp4", audioAfter: "audio_future_bass_drop_with.mp3", audioBefore: "audio_future_bass_drop_without.mp3", sources: [{"vid": "czX9daJUKy0", "title": "How to make a SICK Sample Beat (Reaper Beat Tutorial)", "channel": "Joshua Mallard"}, {"vid": "7qQX6YGBQEA", "title": "Free Vital Synth - Full Tutorial", "channel": "In The Mix"}, {"vid": "Lhfmcw9nQHg", "title": "", "channel": "The Ultimate Mixdown"}] },
  { domain: "Audio", title: "Riddim Wobble Drop", note: "With skills builds wobble call-and-response and pre-drop tension; without skills is closer to a basic half-time groove.", kind: "audio", visualWith: "audio_riddim_wobble_drop_with.mp4", visualWithout: "audio_riddim_wobble_drop_without.mp4", audioAfter: "audio_riddim_wobble_drop_with.mp3", audioBefore: "audio_riddim_wobble_drop_without.mp3", sources: [{"vid": "CtZFdhDPBIg", "title": "Making a Dubstep Drop from Scratch (Reaper, Serum, Defacer)", "channel": "Gabe Miller Music"}, {"vid": "KownwZSW018", "title": "How to make a trap beat in Reaper like in FL Studio (step by step tuto", "channel": "Dominik „Wodzu” Bodzek"}, {"vid": "lJAmSS-ndoU", "title": "", "channel": "Dominik „Wodzu” Bodzek"}, {"vid": "FCY2mF6sxNk", "title": "How To Make Perfect WUB Bass (Sound Design)", "channel": "Official AHEE"}] },
  { domain: "Audio", title: "Electro-Funk Boogie", note: "With skills layers slap bass, boogie drums, stabs, and mix polish; without skills is simpler and less syncopated.", kind: "audio", visualWith: "audio_electro_funk_boogie_with.mp4", visualWithout: "audio_electro_funk_boogie_without.mp4", audioAfter: "audio_electro_funk_boogie_with.mp3", audioBefore: "audio_electro_funk_boogie_without.mp3", sources: [{"vid": "J4Q-au_aRkg", "title": "How to write 80's Funk & Boogie music.", "channel": "Eliana D'Angelo Music"}, {"vid": "FVoDtyZzO8s", "title": "", "channel": "Synthet"}, {"vid": "1hUJqcfcKIs", "title": "", "channel": "8-Bit Drummer"}, {"vid": "GlCJ1UYjuDo", "title": "Creating a Synth Preset (ReaSynth) in REAPER", "channel": "REAPER Mania"}] },
  { domain: "Audio", title: "Metal Djent Riff", note: "With skills emphasizes kick-locked guitar/bass chugs and double-tracked weight; without skills has a plainer rock loop.", kind: "audio", visualWith: "audio_metal_djent_riff_with.mp4", visualWithout: "audio_metal_djent_riff_without.mp4", audioAfter: "audio_metal_djent_riff_with.mp3", audioBefore: "audio_metal_djent_riff_without.mp3", sources: [{"vid": "s2MgjCbheoY", "title": "", "channel": "Andrew Bassett"}, {"vid": "nAHJ-VJgDn0", "title": "How I write music in REAPER", "channel": "Reapertips | Alejandro"}, {"vid": "s2MgjCbheoY", "title": "", "channel": "Andrew Bassett"}, {"vid": "yuMdR7OGMmc", "title": "Beginner Reaper Tutorial | How To Record Electric Guitar", "channel": "Issac Hernandez "}] },
  { domain: "CAD", title: "Mechanical Drafting Plate", stem: "cad_demo_plate", note: "With R2S the agent applies CAD drafting, layer, and dimensioning skills to produce a titled, fully-dimensioned mechanical plate drawing; without skills it leaves a near-empty CAD canvas." },
  { domain: "UE5", title: "UE5 Desert Scene", stem: "ue5_demo_terrain", note: "With R2S the agent composes terrain sculpting, atmosphere, and a placed character into a real Unreal Engine 5 scene; without skills it stays an empty, foggy default level." },
];

// ============ rendering helpers ============

function el(tag, attrs = {}, ...children) {
  const e = document.createElement(tag);
  for (const [k, v] of Object.entries(attrs)) {
    if (k === "class") e.className = v;
    else if (k === "html") e.innerHTML = v;
    else if (k.startsWith("on") && typeof v === "function") e.addEventListener(k.slice(2), v);
    else if (v !== null && v !== undefined && v !== false) e.setAttribute(k, v === true ? "" : v);
  }
  for (const c of children) {
    if (c == null) continue;
    e.appendChild(typeof c === "string" ? document.createTextNode(c) : c);
  }
  return e;
}

function isAudioItem(item) {
  return Boolean(item.audio || item.audioBefore || item.audioAfter);
}

function isManualVideo(video) {
  return video.dataset.manualPlay === "true" || video.controls;
}

function pauseAutoplayMedia() {
  document.querySelectorAll("video").forEach(video => {
    if (!isManualVideo(video)) video.pause();
  });
}

function viewportIntersectionRatio(element) {
  const rect = element.getBoundingClientRect();
  if (rect.width <= 0 || rect.height <= 0) return 0;
  const width = Math.max(0, Math.min(rect.right, window.innerWidth) - Math.max(rect.left, 0));
  const height = Math.max(0, Math.min(rect.bottom, window.innerHeight) - Math.max(rect.top, 0));
  return (width * height) / (rect.width * rect.height);
}

function makeVideoEl(item, className = "") {
  const audioLike = isAudioItem(item);
  const playableVideo = audioLike && item.videoHasAudio;
  const video = el("video", {
    class: className,
    muted: !playableVideo,
    loop: true,
    playsinline: true,
    controls: playableVideo,
    preload: "metadata",
    "data-lazy": "true",
    "data-manual-play": playableVideo ? "true" : null,
    "data-src": assetBase + item.src
  });
  video.muted = !playableVideo;
  video.defaultMuted = !playableVideo;
  video.autoplay = false;
  video.controls = playableVideo;
  return video;
}

function makeAudioPlayer(src, label) {
  const buttonIcon = el("span", {
    class: "audio-action-icon",
    "aria-hidden": "true",
    style: "display:inline-flex;align-items:center;justify-content:center;width:14px;height:14px;flex:0 0 14px;font-size:12px;font-weight:700;line-height:1"
  }, "\u25b6");
  const buttonText = el("span", { class: "audio-toggle-text" }, "Play");
  const button = el("button", {
    class: "audio-toggle",
    type: "button",
    "aria-label": `Play ${label}`
  },
    buttonIcon,
    buttonText
  );
  const audio = el("audio", {
    class: "audio-engine",
    preload: "none",
    "data-src": audioBase + src,
    "aria-hidden": "true",
    tabindex: "-1"
  });
  let sourceAttached = false;
  let playPending = false;

  const attachSource = () => {
    if (sourceAttached) return;
    sourceAttached = true;
    audio.src = audio.dataset.src;
    audio.load();
  };

  const updateButton = isPlaying => {
    const action = isPlaying ? "Pause" : "Play";
    buttonIcon.textContent = isPlaying ? "\u2016" : "\u25b6";
    buttonText.textContent = action;
    button.setAttribute("aria-label", `${action} ${label}`);
    button.style.borderColor = isPlaying ? "var(--accent)" : "";
    button.style.background = isPlaying ? "var(--accent)" : "";
    button.style.color = isPlaying ? "#ffffff" : "";
    button.style.boxShadow = isPlaying ? "0 6px 16px rgba(36, 87, 230, 0.2)" : "";
  };

  button.addEventListener("click", async () => {
    if (!audio.paused && !audio.ended) {
      audio.pause();
      return;
    }
    if (playPending) return;

    attachSource();
    playPending = true;
    try {
      await audio.play();
    } catch (error) {
      updateButton(false);
    } finally {
      playPending = false;
    }
  });

  audio.addEventListener("play", () => updateButton(true));
  audio.addEventListener("pause", () => updateButton(false));
  audio.addEventListener("ended", () => updateButton(false));

  return el("div", { class: "audio-player" },
    el("span", { class: "audio-label" }, label),
    button,
    audio
  );
}

function makeVideoCard(item) {
  const audioLike = isAudioItem(item);
  const media = item.visual
    ? el("div", { class: "vc-media vc-media-static" },
        el("img", {
          class: "vc-visual",
          src: item.visual,
          alt: item.visualAlt || item.caption,
          loading: "lazy"
        }))
    : el("div", { class: "vc-media" }, makeVideoEl(item));
  const caption = el("div", { class: "vc-caption" },
    el("span", { class: "vc-prompt" }, audioLike ? "Playable audio render" : "Generated artifact"),
    document.createTextNode(item.caption)
  );
  const children = [media, caption];
  if (item.audio) children.push(makeAudioPlayer(item.audio, "Rendered audio"));
  return el("article", { class: audioLike ? "video-card audio-card" : "video-card" }, ...children);
}

function makeFeaturedCard(item) {
  const audioLike = isAudioItem(item);
  const media = item.visual
    ? el("img", {
        class: "featured-visual",
        src: item.visual,
        alt: item.title,
        loading: "lazy"
      })
    : makeVideoEl(item);
  const copyChildren = [
    el("span", { class: "featured-domain" }, item.domain),
    el("h3", {}, item.title),
    el("p", {}, item.note)
  ];
  if (item.audio) copyChildren.push(makeAudioPlayer(item.audio, "Rendered audio"));
  return el("article", { class: "featured-card" },
    el("div", { class: item.visual ? "featured-media featured-media-static" : "featured-media" }, media),
    el("div", { class: audioLike ? "featured-copy audio-copy" : "featured-copy" }, ...copyChildren)
  );
}

function renderFeaturedDemos() {
  const grid = document.getElementById("featured-grid");
  if (!grid) return;
  featuredDemos.forEach(item => grid.appendChild(makeFeaturedCard(item)));
}

function renderTaxonomySections() {
  const container = document.getElementById("taxonomy-sections");
  if (!container) return;
  taxonomySections.forEach(sec => {
    const head = el("div", { class: "taxonomy-section-head" },
      el("div", {},
        el("h3", {}, sec.title),
        el("div", { class: "domain-meta" },
          el("span", { class: "domain-chip" }, sec.chip),
          el("span", { class: "domain-output" }, sec.output)
        )
      ),
      el("p", { class: "domain-desc" }, sec.description)
    );
    const grid = el("div", { class: "video-grid" });
    sec.items.forEach(item => grid.appendChild(makeVideoCard(item)));
    container.appendChild(el("section", { class: "taxonomy-section-block", "data-domain": sec.domain }, head, grid));
  });
}

function makeCompareVideo(file) {
  const v = el("video", {
    class: "cmp-video",
    muted: true,
    loop: true,
    playsinline: true,
    preload: "none",
    "data-lazy": "true",
    "data-sync-row": "true",
    "data-src": assetBase + file + assetVer
  });
  v.muted = true;
  v.defaultMuted = true;
  return v;
}

function makeHeroReelVideo(clip, index) {
  const video = el("video", {
    class: index === 0 ? "hero-reel-video active" : "hero-reel-video",
    muted: true,
    loop: true,
    playsinline: true,
    preload: index === 0 ? "auto" : "metadata",
    src: assetBase + clip.src,
    "aria-label": clip.label
  });
  video.muted = true;
  video.defaultMuted = true;
  video.autoplay = false;
  return video;
}

function initHeroReel() {
  const mount = document.getElementById("hero-reel");
  if (!mount || heroReelClips.length === 0) return;
  const sources = heroReelClips.map(clip => assetBase + clip.src);
  // Two stacked <video>s; cross-fade by swapping the source on the hidden one
  // (cheaper than autoplaying all clips at once, matches the LSM hero reel).
  const vids = [0, 1].map(i => {
    const v = el("video", {
      class: i === 0 ? "hero-reel-video active" : "hero-reel-video",
      muted: true, loop: true, playsinline: true,
      preload: "metadata", "aria-hidden": "true"
    });
    v.muted = true; v.defaultMuted = true;
    mount.appendChild(v);
    return v;
  });
  const load = (v, src) => { v.src = src; v.load(); safePlay(v); };
  let active = 0;
  let idx = Math.min(1, sources.length - 1);
  let visible = viewportIntersectionRatio(mount) > 0;
  let intervalId = null;
  load(vids[0], sources[0]);
  load(vids[1], sources[idx]);
  const stopInterval = () => {
    if (intervalId === null) return;
    window.clearInterval(intervalId);
    intervalId = null;
  };
  const startInterval = () => {
    if (intervalId !== null || sources.length <= 1 || !motionState.isEnabled() || !visible) return;
    intervalId = window.setInterval(() => {
      const next = active === 0 ? 1 : 0;
      idx = (idx + 1) % sources.length;
      load(vids[next], sources[idx]);
      vids[next].classList.add("active");
      vids[active].classList.remove("active");
      active = next;
    }, 6500);
  };
  const updatePlayback = () => {
    if (!motionState.isEnabled() || !visible) {
      stopInterval();
      vids.forEach(video => video.pause());
      return;
    }
    vids.forEach(video => safePlay(video));
    startInterval();
  };

  motionState.subscribe(updatePlayback);
  if ("IntersectionObserver" in window) {
    const observer = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        visible = entry.isIntersecting && entry.intersectionRatio > 0.01;
        updatePlayback();
      });
    }, { threshold: [0, 0.01, 0.25] });
    observer.observe(mount);
  }
  updatePlayback();
}

function makeCompareAudioCell(item, variant) {
  const withSkills = variant === "with";
  const visualFile = withSkills
    ? (item.visualWith || item.visual || "compare_audio_psychedelic_rock.mp4")
    : (item.visualWithout || item.visual || "compare_audio_psychedelic_rock.mp4");
  const audioFile = withSkills ? item.audioAfter : item.audioBefore;
  const label = withSkills ? "With skills" : "Without skills";
  const visual = makeCompareVideo(visualFile);
  const player = audioFile
    ? makeAudioPlayer(audioFile, `${item.title}, ${withSkills ? "with skills" : "without skills"}`)
    : null;
  return {
    video: visual,
    cell: el("figure", { class: withSkills ? "cmp-cell cmp-audio-cell is-with" : "cmp-cell cmp-audio-cell" },
      el("div", { class: "cmp-audio-visual" }, visual),
      el("figcaption", {}, label),
      player
    )
  };
}

// Load a row's clips, then start them together so the two conditions stay in sync.
function syncPlayRow(videos, shouldPlay = () => true) {
  if (!motionState.isEnabled()) {
    videos.forEach(video => video.pause());
    return;
  }
  videos.forEach(v => {
    loadVideoSource(v, { preload: "metadata" });
  });
  const ready = videos.map(v => v.readyState >= 2
    ? Promise.resolve()
    : new Promise(res => v.addEventListener("loadeddata", res, { once: true })));
  Promise.all(ready).then(() => {
    if (!motionState.isEnabled() || !shouldPlay()) return;
    videos.forEach(v => {
      try { v.currentTime = 0; } catch (e) { /* seek may be unsupported */ }
      safePlay(v);
    });
  });
}

function makeSourceCell(sources) {
  const n = Math.min(sources.length, 4);
  const grid = el("div", { class: "cmp-source-grid n" + n });
  sources.slice(0, 4).forEach(s => {
    const tip = (s.channel ? s.channel + " — " : "") + (s.title || "YouTube source");
    const a = el("a", {
      class: "cmp-source-thumb",
      href: "https://www.youtube.com/watch?v=" + s.vid,
      target: "_blank", rel: "noopener", title: tip, "aria-label": tip
    },
      el("img", { loading: "lazy", decoding: "async", alt: "", src: "assets/yt/" + s.vid + ".jpg" }),
      el("span", { class: "cmp-source-play" }, "▶")
    );
    grid.appendChild(a);
  });
  return el("figure", { class: "cmp-cell cmp-source" }, grid, el("figcaption", {}, "Skill source · YouTube"));
}

function renderComparisons() {
  const mount = document.getElementById("comparison-grid");
  if (!mount) return;
  mount.textContent = "";
  mount.classList.add("cmp-list");

  mount.appendChild(el("div", { class: "cmp-colhead" },
    el("span", { class: "cmp-spacer", "aria-hidden": "true" }, ""),
    el("span", {}, "Without skills"),
    el("span", { class: "is-with" }, "With skills")
  ));

  const rows = [];
  comparisonCases.forEach(c => {
    const audioCase = c.kind === "audio" || c.audioBefore || c.audioAfter;
    const withoutCell = audioCase ? makeCompareAudioCell(c, "without") : null;
    const withCell = audioCase ? makeCompareAudioCell(c, "with") : null;
    const without = audioCase ? withoutCell.video : makeCompareVideo(c.stem + "_without.mp4");
    const withSkills = audioCase ? withCell.video : makeCompareVideo(c.stem + "_with.mp4");
    // Web/Excel clips are fast screen recordings — play them at half speed.
    if (c.domain === "Web" || c.domain === "Excel") {
      [without, withSkills].forEach(v => {
        const slow = () => { try { v.playbackRate = 0.5; } catch (e) {} };
        slow();
        v.addEventListener("loadeddata", slow);
        v.addEventListener("play", slow);
      });
    }
    const cells = [
      audioCase ? withoutCell.cell : el("figure", { class: "cmp-cell" }, without, el("figcaption", {}, "Without skills")),
      audioCase ? withCell.cell : el("figure", { class: "cmp-cell is-with" }, withSkills, el("figcaption", {}, "With skills"))
    ];
    const hasSource = Array.isArray(c.sources) && c.sources.length > 0;
    if (hasSource) cells.push(makeSourceCell(c.sources));
    const row = el("article", { class: audioCase ? "cmp-row cmp-row-audio reveal" : "cmp-row reveal" },
      el("div", { class: "cmp-rowhead" },
        el("span", { class: "compare-domain" }, c.domain),
        el("h4", {}, c.title),
        el("p", {}, c.note)
      ),
      el("div", { class: hasSource ? "cmp-cells has-source" : "cmp-cells" }, ...cells)
    );
    mount.appendChild(row);
    rows.push({ row, videos: [without, withSkills], visible: false });
  });

  const updateRowsForMotion = enabled => {
    rows.forEach(rec => {
      rec.visible = viewportIntersectionRatio(rec.row) > 0.3;
      if (enabled && rec.visible) syncPlayRow(rec.videos, () => rec.visible);
      else rec.videos.forEach(video => video.pause());
    });
  };
  motionState.subscribe(updateRowsForMotion);

  document.addEventListener("visibilitychange", () => {
    if (document.hidden || !motionState.isEnabled()) {
      rows.forEach(rec => rec.videos.forEach(video => video.pause()));
      return;
    }
    updateRowsForMotion(true);
  });

  if (!("IntersectionObserver" in window)) {
    rows.forEach(r => {
      r.visible = true;
      syncPlayRow(r.videos, () => r.visible);
    });
    return;
  }
  const ob = new IntersectionObserver(entries => {
    entries.forEach(en => {
      const rec = rows.find(r => r.row === en.target);
      if (!rec) return;
      rec.visible = en.isIntersecting && en.intersectionRatio > 0.3;
      if (rec.visible) syncPlayRow(rec.videos, () => rec.visible);
      else rec.videos.forEach(v => v.pause());
    });
  }, { threshold: [0, 0.3, 0.6] });
  rows.forEach(r => ob.observe(r.row));
}

// Fade + lift elements marked `.reveal` in as they scroll into view.
function initReveal() {
  const els = [...document.querySelectorAll(".reveal")];
  if (!("IntersectionObserver" in window)) {
    els.forEach(e => e.classList.add("is-visible"));
    return;
  }
  const ob = new IntersectionObserver((entries) => {
    entries.forEach(en => {
      if (en.isIntersecting) { en.target.classList.add("is-visible"); ob.unobserve(en.target); }
    });
  }, { threshold: 0.12, rootMargin: "0px 0px -8% 0px" });
  els.forEach(e => ob.observe(e));
}

// ============ video lazy-loading & lifecycle ============

function loadVideoSource(video, opts = {}) {
  if (video.dataset.loaded === "true") return;
  const src = video.dataset.src;
  if (!src) return;
  const s = document.createElement("source");
  s.src = src;
  s.type = "video/mp4";
  video.appendChild(s);
  if (opts.preload) video.preload = opts.preload;
  video.dataset.loaded = "true";
  video.load();
}

function unloadVideoSource(video) {
  if (video.dataset.lazy !== "true" || isManualVideo(video)) return false;
  video.pause();
  video.removeAttribute("src");
  video.querySelectorAll("source").forEach(source => source.remove());
  video.load();
  video.dataset.loaded = "false";
  return true;
}

function safePlay(video, opts = {}) {
  if (!opts.force && !motionState.isEnabled()) {
    video.pause();
    return null;
  }
  const p = video.play();
  if (p && typeof p.catch === "function") {
    p.catch(() => { /* autoplay can be blocked; that's fine */ });
  }
}

// ============ scroll → sticky-nav state ============

function initNavScrollState() {
  const nav = document.querySelector(".home-page .hero-nav");
  const hero = document.querySelector(".home-page .hero");
  if (!nav || !hero) return;
  const links = Array.from(nav.querySelectorAll(".hero-nav-links a[href^='#']"));
  const targets = links
    .map(link => ({ link, target: document.querySelector(link.getAttribute("href")) }))
    .filter(item => item.target);
  const update = () => {
    const trigger = hero.offsetHeight - 110;
    if (window.scrollY > trigger) nav.classList.add("scrolled");
    else nav.classList.remove("scrolled");

    let active = targets[0];
    const line = window.scrollY + 130;
    targets.forEach(item => {
      if (item.target.offsetTop <= line) active = item;
    });
    links.forEach(link => link.classList.toggle("active", active?.link === link));
  };
  update();
  window.addEventListener("scroll", update, { passive: true });
}

// ============ visibility-driven autoplay ============

function initVideoLifecycle() {
  const all = Array.from(document.querySelectorAll("video[data-lazy='true']"));
  if (!("IntersectionObserver" in window)) {
    all.forEach(v => {
      loadVideoSource(v, { preload: "metadata" });
      if (!isManualVideo(v) && v.dataset.syncRow !== "true") safePlay(v);
    });
    return;
  }

  const loadOb = new IntersectionObserver(entries => {
    entries.forEach(en => {
      if (!en.isIntersecting) return;
      const video = en.target;
      if (video.dataset.syncRow === "true") return;
      loadVideoSource(video, { preload: "metadata" });
    });
  }, { rootMargin: "600px 0px", threshold: 0.01 });

  const unloadOb = new IntersectionObserver(entries => {
    entries.forEach(en => {
      if (!en.isIntersecting) unloadVideoSource(en.target);
    });
  }, { rootMargin: "1100px 0px", threshold: 0.01 });

  const playOb = new IntersectionObserver(entries => {
    entries.forEach(en => {
      const v = en.target;
      if (v.dataset.syncRow === "true") return;
      if (v.dataset.manualPlay === "true") {
        if (en.isIntersecting) loadVideoSource(v, { preload: "metadata" });
        else v.pause();
        return;
      }
      if (en.isIntersecting && en.intersectionRatio > 0.25) {
        loadVideoSource(v, { preload: "metadata" });
        safePlay(v);
      } else {
        v.pause();
      }
    });
  }, { threshold: [0, 0.25, 0.6] });

  all.forEach(v => {
    loadOb.observe(v);
    playOb.observe(v);
    if (!isManualVideo(v)) unloadOb.observe(v);
  });

  motionState.subscribe(enabled => {
    all.forEach(v => {
      if (isManualVideo(v) || v.dataset.syncRow === "true") return;
      if (!enabled) {
        v.pause();
        return;
      }
      const visible = viewportIntersectionRatio(v) > 0.25;
      if (visible) {
        loadVideoSource(v, { preload: "metadata" });
        safePlay(v);
      }
    });
  });

  document.addEventListener("visibilitychange", () => {
    if (document.hidden) {
      all.forEach(v => v.pause());
    } else {
      all.forEach(v => {
        if (isManualVideo(v) || v.dataset.syncRow === "true") return;
        const visible = viewportIntersectionRatio(v) > 0;
        if (visible && motionState.isEnabled()) safePlay(v);
        else v.pause();
      });
    }
  });
}

function initHeroGrid() {
  const grid = document.getElementById("hero-grid");
  if (!grid) return;
  // each domain = 4 tiny background cases shown in a 2x2; cycle domains every 3s
  const DOMAINS = [
    ["ppt_1", "ppt_2", "ppt_3", "ppt_4"],
    ["web_1", "web_2", "web_3", "web_4"],
    ["reaper_1", "reaper_2", "reaper_3", "reaper_4"],
    ["excel_1", "excel_2", "excel_3", "excel_4"],
    ["blender_1", "blender_2", "blender_3", "blender_4"]
  ].map(g => g.map(n => assetBase + "hero/" + n + ".mp4" + assetVer));
  const tiles = [...grid.querySelectorAll("video")];
  if (tiles.length < 4) return;
  let visible = viewportIntersectionRatio(grid) > 0;
  let intervalId = null;
  const show = (di) => {
    DOMAINS[di].forEach((src, i) => {
      const v = tiles[i];
      if (!v) return;
      v.src = src; v.muted = true; v.defaultMuted = true; v.loop = true;
      v.preload = "metadata";
      v.load();
      safePlay(v);
    });
  };
  let d = 0;
  show(0);
  const stopInterval = () => {
    if (intervalId === null) return;
    window.clearInterval(intervalId);
    intervalId = null;
  };
  const startInterval = () => {
    if (intervalId !== null || DOMAINS.length <= 1 || !motionState.isEnabled() || !visible) return;
    intervalId = window.setInterval(() => {
      d = (d + 1) % DOMAINS.length;
      show(d);
    }, 3000);
  };
  const updatePlayback = () => {
    if (!motionState.isEnabled() || !visible) {
      stopInterval();
      tiles.forEach(video => video.pause());
      return;
    }
    tiles.forEach(video => safePlay(video));
    startInterval();
  };

  motionState.subscribe(updatePlayback);
  if ("IntersectionObserver" in window) {
    const observer = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        visible = entry.isIntersecting && entry.intersectionRatio > 0.01;
        updatePlayback();
      });
    }, { threshold: [0, 0.01, 0.25] });
    observer.observe(grid);
  }
  updatePlayback();
}

// ============ project video: fully-local preview + on-click full ============
// The YouTube iframe was the page's only continuous cross-origin stream and
// stalled on slow/CN networks, so the project video is now fully local: a tiny
// 15s muted preview loop plays in-view, and clicking "Watch full video"
// swaps in the local 2:39 cut with sound. A small corner link still points to
// YouTube for the canonical upload. Nothing here touches Google until clicked.
function initVideoEmbed() {
  const box = document.getElementById("video-embed");
  if (!box) return;
  const preview = box.querySelector(".video-preview");
  const facade = box.querySelector(".video-facade");
  const fullSrc = box.dataset.full;
  let full = null;
  let onScreen = viewportIntersectionRatio(box) > 0.25;
  const playFull = () => {
    if (full) { safePlay(full, { force: true }); return; }
    if (preview) preview.pause();
    full = el("video", {
      class: "video-full",
      controls: true,
      playsinline: true,
      src: fullSrc,
      "data-manual-play": "true"
    });
    full.playsInline = true;
    box.appendChild(full);
    box.classList.add("is-playing");
    safePlay(full, { force: true });
  };
  if (facade) facade.addEventListener("click", playFull);
  // Local clips only: play the preview while the section is on screen, and pause
  // everything when it scrolls away (also stops the full video's audio).
  if ("IntersectionObserver" in window) {
    const ob = new IntersectionObserver(entries => {
      entries.forEach(en => {
        onScreen = en.isIntersecting && en.intersectionRatio > 0.25;
        if (full) { if (!onScreen) full.pause(); }
        else if (preview) { if (onScreen) safePlay(preview); else preview.pause(); }
      });
    }, { threshold: [0, 0.25, 0.6] });
    ob.observe(box);
  } else if (preview) {
    safePlay(preview);
  }

  motionState.subscribe(enabled => {
    if (!preview || full) return;
    if (enabled && onScreen) safePlay(preview);
    else preview.pause();
  });
}

// ============ boot ============

function initMotionToggle() {
  const button = document.getElementById("motion-toggle");
  if (!button) return;
  const render = enabled => {
    const action = enabled ? "Pause motion" : "Play motion";
    button.setAttribute("aria-label", action);
    button.title = action;
    button.dataset.motionAction = enabled ? "pause" : "play";
  };
  render(motionState.isEnabled());
  motionState.subscribe(render);
  button.addEventListener("click", () => {
    motionState.setEnabled(!motionState.isEnabled(), { userInitiated: true });
  });
}

initMotionToggle();
initHeroGrid();
renderFeaturedDemos();
renderTaxonomySections();
renderComparisons();
initNavScrollState();
initVideoEmbed();
initVideoLifecycle();
initReveal();
