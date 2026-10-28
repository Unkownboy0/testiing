import os
import sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

# -------------------------------------------------------------
# CONSTANTS & PALETTE (Modern Digital Brutalism)
# -------------------------------------------------------------
BG_COLOR       = RGBColor(8, 8, 8)        # #080808 Deep Black
PANEL_BG       = RGBColor(18, 18, 18)     # #121212 Dark Neutral Panel
PANEL_BG_ALT   = RGBColor(24, 24, 24)     # #181818 Slightly Lighter Panel
ACCENT_SAND    = RGBColor(196, 167, 125)  # #C4A77D Warm Sandalwood / Sand
ACCENT_BLUE    = RGBColor(53, 107, 255)   # #356BFF Electric Blue
TEXT_WHITE     = RGBColor(244, 240, 232)  # #F4F0E8 Off-white
TEXT_MUTED     = RGBColor(160, 160, 160)  # #A0A0A0 Soft Gray
BORDER_GRAY    = RGBColor(42, 42, 42)     # #2A2A2A Technical Border
BADGE_GREEN    = RGBColor(46, 125, 50)    # Implemented / Verified
BADGE_AMBER    = RGBColor(230, 81, 0)     # Partial
BADGE_GRAY     = RGBColor(90, 90, 90)     # Planned

FONT_HEADLINE = "Trebuchet MS"
FONT_BODY     = "Segoe UI"
FONT_MONO     = "Consolas"

def create_deck(output_path="GeetorusAI_Brutalist_Presentation.pptx"):
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]  # Blank slide

    def set_slide_bg(slide):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = BG_COLOR
        bg.line.color.rgb = BG_COLOR
        return bg

    def add_header(slide, slide_num, category, title, subtitle=None):
        # Top metadata bar
        top_bar = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.733), Inches(0.4))
        tf = top_bar.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = f"GEETORUSAI // CONTROL PLANE SPEC // {category.upper()}"
        p.font.name = FONT_MONO
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = ACCENT_SAND

        # Slide indicator top-right
        num_box = slide.shapes.add_textbox(Inches(10.5), Inches(0.4), Inches(2.0), Inches(0.4))
        tf_num = num_box.text_frame
        p_num = tf_num.paragraphs[0]
        p_num.alignment = PP_ALIGN.RIGHT
        p_num.text = f"[ {slide_num:02d} / 14 ]"
        p_num.font.name = FONT_MONO
        p_num.font.size = Pt(10)
        p_num.font.bold = True
        p_num.font.color.rgb = ACCENT_BLUE

        # Main Title Box
        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.8), Inches(11.733), Inches(0.8))
        tf_t = title_box.text_frame
        tf_t.word_wrap = True
        p_t = tf_t.paragraphs[0]
        p_t.text = title.upper()
        p_t.font.name = FONT_HEADLINE
        p_t.font.size = Pt(24)
        p_t.font.bold = True
        p_t.font.color.rgb = TEXT_WHITE

        if subtitle:
            p_sub = tf_t.add_paragraph()
            p_sub.text = subtitle
            p_sub.font.name = FONT_BODY
            p_sub.font.size = Pt(12)
            p_sub.font.color.rgb = TEXT_MUTED
            p_sub.space_before = Pt(4)

        # Thin divider rule
        line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.65), Inches(11.733), Inches(0.02))
        line.fill.solid()
        line.fill.fore_color.rgb = BORDER_GRAY
        line.line.color.rgb = BORDER_GRAY

    def add_panel(slide, left, top, width, height, border_color=BORDER_GRAY, bg_color=PANEL_BG):
        panel = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, width, height)
        panel.fill.solid()
        panel.fill.fore_color.rgb = bg_color
        panel.line.color.rgb = border_color
        panel.line.width = Pt(1.2)
        return panel

    def add_badge(slide, left, top, text, bg_color, text_color=TEXT_WHITE, width=Inches(1.4), height=Inches(0.3)):
        badge = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, width, height)
        badge.fill.solid()
        badge.fill.fore_color.rgb = bg_color
        badge.line.color.rgb = bg_color
        tf = badge.text_frame
        p = tf.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        p.text = text
        p.font.name = FONT_MONO
        p.font.size = Pt(8.5)
        p.font.bold = True
        p.font.color.rgb = text_color
        return badge

    # =========================================================
    # SLIDE 01: COVER
    # =========================================================
    s1 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s1)

    # Architectural framing line
    frame = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(0.8), Inches(11.733), Inches(5.9))
    frame.fill.background()
    frame.line.color.rgb = BORDER_GRAY
    frame.line.width = Pt(1)

    # Top Tag
    tag_box = s1.shapes.add_textbox(Inches(1.2), Inches(1.1), Inches(8), Inches(0.4))
    p = tag_box.text_frame.paragraphs[0]
    p.text = "// ARCHITECTURE SPECIFICATION & STRATEGIC BRIEF // 2026 EDITION"
    p.font.name = FONT_MONO
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = ACCENT_SAND

    # Main Brand Header
    brand_box = s1.shapes.add_textbox(Inches(1.2), Inches(1.6), Inches(10), Inches(1.4))
    p = brand_box.text_frame.paragraphs[0]
    p.text = "GEETORUSAI"
    p.font.name = FONT_HEADLINE
    p.font.size = Pt(56)
    p.font.bold = True
    p.font.color.rgb = TEXT_WHITE

    p2 = brand_box.text_frame.add_paragraph()
    p2.text = "THE AUTONOMOUS AI AGENT CONTROL PLANE"
    p2.font.name = FONT_HEADLINE
    p2.font.size = Pt(20)
    p2.font.bold = True
    p2.font.color.rgb = ACCENT_BLUE
    p2.space_before = Pt(8)

    # Subtitle narrative
    sub_box = s1.shapes.add_textbox(Inches(1.2), Inches(3.3), Inches(6.5), Inches(1.6))
    tf_sub = sub_box.text_frame
    tf_sub.word_wrap = True
    p_sub = tf_sub.paragraphs[0]
    p_sub.text = "From isolated LLM chat sessions to coordinated digital teams.\nAn open-source-oriented operating system providing multi-agent orchestration, human-in-the-loop governance, strict budget gates, and verified execution pipelines."
    p_sub.font.name = FONT_BODY
    p_sub.font.size = Pt(13)
    p_sub.font.color.rgb = TEXT_MUTED

    # Metadata Panel (Right side)
    add_panel(s1, Inches(8.2), Inches(2.2), Inches(3.9), Inches(4.0), border_color=ACCENT_SAND, bg_color=PANEL_BG)
    meta_box = s1.shapes.add_textbox(Inches(8.4), Inches(2.4), Inches(3.5), Inches(3.6))
    tf_m = meta_box.text_frame
    tf_m.word_wrap = True
    
    entries = [
        ("PROJECT CODE", "GEETORUS-CORE / v0.3.1"),
        ("SYSTEM CLASS", "Autonomous Agent Control Plane"),
        ("DEPLOYMENT", "Self-Hosted / Hybrid Cloud"),
        ("ORCHESTRATION", "Multi-Agent Directed Graph"),
        ("GOVERNANCE", "Company-Scoped Token Gates & RBAC"),
        ("COMPUTATIONAL BASIS", "Local Runtimes + Hosted Providers"),
        ("DOCUMENT VERSION", "Technical Audit & Pitch Deck v1.0"),
    ]
    for idx, (k, v) in enumerate(entries):
        p_k = tf_m.paragraphs[0] if idx == 0 else tf_m.add_paragraph()
        p_k.text = f"{k}:"
        p_k.font.name = FONT_MONO
        p_k.font.size = Pt(9)
        p_k.font.bold = True
        p_k.font.color.rgb = ACCENT_SAND
        if idx > 0:
            p_k.space_before = Pt(6)
            
        p_v = tf_m.add_paragraph()
        p_v.text = v
        p_v.font.name = FONT_BODY
        p_v.font.size = Pt(10.5)
        p_v.font.color.rgb = TEXT_WHITE

    # Bottom status bar
    bot_box = s1.shapes.add_textbox(Inches(1.2), Inches(5.8), Inches(6.5), Inches(0.5))
    p_bot = bot_box.text_frame.paragraphs[0]
    p_bot.text = "[ ARCHITECTURE // SYSTEM GOVERNANCE // MULTI-AGENT EXECUTION ]"
    p_bot.font.name = FONT_MONO
    p_bot.font.size = Pt(10)
    p_bot.font.color.rgb = ACCENT_BLUE

    # =========================================================
    # SLIDE 02: THE PROBLEM (AI TOOLS ARE FRAGMENTED)
    # =========================================================
    s2 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s2)
    add_header(s2, 2, "Market Friction & Systemic Failure Modes", 
               "THE PROBLEM: AI TOOLS ARE SILOED, UNGOVERNED & FRAGMENTED", 
               "Developers and enterprises attempt multi-agent autonomy using disjointed tools, creating chaos, spiraling API bills, and unverified outputs.")

    # Left Column: The Fragmented Reality
    add_panel(s2, Inches(0.8), Inches(1.9), Inches(5.6), Inches(5.0), border_color=BORDER_GRAY)
    add_badge(s2, Inches(1.1), Inches(2.1), "STATUS QUO: FRAGMENTED SILOS", RGBColor(120, 30, 30))
    
    left_txt = s2.shapes.add_textbox(Inches(1.1), Inches(2.55), Inches(5.0), Inches(4.1))
    tf_l = left_txt.text_frame
    tf_l.word_wrap = True
    
    prob_items = [
        ("Siloed Single-Agent Interfaces", "Engineers jump between ChatGPT, Claude, and terminal agents. No unified context, no shared execution history."),
        ("Manual Hand-offs & Glue Scripts", "Output from one tool must be manually copied, audited, and pasted to the next. Human becomes the fragile API glue."),
        ("Runaway Token Consumption", "Autonomous loops lack hard financial stop-limits, leading to unexpected $500+ bills on looping syntax errors."),
        ("Zero Execution Verification", "Agents declare 'Task Completed' without running tests, security linters, or human sign-off gates."),
        ("Blind Governance & Secret Sprawl", "API keys and sensitive tokens are exposed across raw bash scripts with zero company-level access controls.")
    ]
    for i, (title, desc) in enumerate(prob_items):
        p_t = tf_l.paragraphs[0] if i == 0 else tf_l.add_paragraph()
        p_t.text = f"> {title.upper()}"
        p_t.font.name = FONT_MONO
        p_t.font.size = Pt(10)
        p_t.font.bold = True
        p_t.font.color.rgb = ACCENT_SAND
        if i > 0:
            p_t.space_before = Pt(8)
            
        p_d = tf_l.add_paragraph()
        p_d.text = desc
        p_d.font.name = FONT_BODY
        p_d.font.size = Pt(9.5)
        p_d.font.color.rgb = TEXT_MUTED

    # Right Column: The Controlled GeetorusAI Paradigm
    add_panel(s2, Inches(6.9), Inches(1.9), Inches(5.6), Inches(5.0), border_color=ACCENT_BLUE)
    add_badge(s2, Inches(7.2), Inches(2.1), "GEETORUSAI: UNIFIED CONTROL PLANE", ACCENT_BLUE)

    right_txt = s2.shapes.add_textbox(Inches(7.2), Inches(2.55), Inches(5.0), Inches(4.1))
    tf_r = right_txt.text_frame
    tf_r.word_wrap = True

    sol_items = [
        ("Unified Virtual Company Hub", "A single operating system where specialized agents (Lead, Dev, QA, Security) collaborate under strict hierarchies."),
        ("Autonomous Goal Decomposition", "Complex goals automatically break down into dependent DAG tasks, scheduled across specialized worker agents."),
        ("Hard Token & Budget Gate Enforcers", "Real-time token gating at company and agent levels kills loops before budget thresholds are breached."),
        ("Built-in QA & Verification Loops", "Code and research must pass explicit test suites and human approval checkpoints before merge."),
        ("Enterprise-Scoped Governance", "Role-based access, sandboxed runtime execution, encrypted credentials, and full audit logs.")
    ]
    for i, (title, desc) in enumerate(sol_items):
        p_t = tf_r.paragraphs[0] if i == 0 else tf_r.add_paragraph()
        p_t.text = f"> {title.upper()}"
        p_t.font.name = FONT_MONO
        p_t.font.size = Pt(10)
        p_t.font.bold = True
        p_t.font.color.rgb = ACCENT_SAND
        if i > 0:
            p_t.space_before = Pt(8)

        p_d = tf_r.add_paragraph()
        p_d.text = desc
        p_d.font.name = FONT_BODY
        p_d.font.size = Pt(9.5)
        p_d.font.color.rgb = TEXT_WHITE

    # =========================================================
    # SLIDE 03: THE SOLUTION (ONE CONTROL PLANE, MULTIPLE AGENTS)
    # =========================================================
    s3 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s3)
    add_header(s3, 3, "Core System Concept & Categorization",
               "THE SOLUTION: ONE CONTROL PLANE, MULTIPLE SPECIALIZED AGENTS",
               "Clarifying the AI hierarchy: GeetorusAI is not just another LLM wrapper or coding agent—it is the operational orchestration layer.")

    # 4 Comparative Columns: Model vs Agent vs Multi-Agent Framework vs Control Plane
    tiers = [
        ("01 / MODEL LAYER", "RAW INTELLIGENCE", 
         "Stateless next-token predictors.\nZero execution memory.\nNo environment access.",
         ["OpenAI GPT-4o / o3", "Anthropic Claude 3.7", "Ollama / DeepSeek-R1", "Local GGUF Models"],
         BORDER_GRAY),
        ("02 / AGENT LAYER", "AUTONOMOUS ACTORS", 
         "Model paired with tools, prompt loop, and filesystem access.\nPerforms single tasks.",
         ["OpenCode Local Runtime", "SWE-Bench workers", "Browser automation agents", "Research scraping bots"],
         BORDER_GRAY),
        ("03 / ORCHESTRATION", "CODE FRAMEWORKS", 
         "Python/TS libraries to write custom graph workflows.\nRequires manual dev & host.",
         ["LangGraph / LangChain", "CrewAI Python SDK", "Microsoft AutoGen", "Custom script graphs"],
         BORDER_GRAY),
        ("04 / CONTROL PLANE", "GEETORUSAI (THE OS)", 
         "Full Virtual Company OS with Web UI, DB persistence, budget gates, and human approval.",
         ["Multi-Agent Scheduling", "Role-based Assignment", "Strict Token-Gate Limits", "Audit Trail & Verification"],
         ACCENT_SAND)
    ]

    for idx, (tier_num, title, desc, examples, b_col) in enumerate(tiers):
        left_pos = Inches(0.8 + idx * 2.98)
        is_hero = (idx == 3)
        bg_col = PANEL_BG_ALT if is_hero else PANEL_BG
        add_panel(s3, left_pos, Inches(1.9), Inches(2.8), Inches(4.2), border_color=b_col, bg_color=bg_col)
        
        box = s3.shapes.add_textbox(left_pos + Inches(0.15), Inches(2.05), Inches(2.5), Inches(3.9))
        tf_b = box.text_frame
        tf_b.word_wrap = True
        
        p0 = tf_b.paragraphs[0]
        p0.text = tier_num
        p0.font.name = FONT_MONO
        p0.font.size = Pt(8.5)
        p0.font.bold = True
        p0.font.color.rgb = ACCENT_BLUE if not is_hero else ACCENT_SAND
        
        p1 = tf_b.add_paragraph()
        p1.text = title
        p1.font.name = FONT_HEADLINE
        p1.font.size = Pt(13)
        p1.font.bold = True
        p1.font.color.rgb = TEXT_WHITE
        p1.space_before = Pt(4)
        
        p2 = tf_b.add_paragraph()
        p2.text = desc
        p2.font.name = FONT_BODY
        p2.font.size = Pt(9.5)
        p2.font.color.rgb = TEXT_MUTED if not is_hero else TEXT_WHITE
        p2.space_before = Pt(8)

        p3 = tf_b.add_paragraph()
        p3.text = "EXAMPLES / TECH:" if not is_hero else "CORE CAPABILITIES:"
        p3.font.name = FONT_MONO
        p3.font.size = Pt(8.5)
        p3.font.bold = True
        p3.font.color.rgb = ACCENT_SAND if not is_hero else ACCENT_BLUE
        p3.space_before = Pt(12)

        for ex in examples:
            p_ex = tf_b.add_paragraph()
            p_ex.text = f"• {ex}"
            p_ex.font.name = FONT_BODY
            p_ex.font.size = Pt(9)
            p_ex.font.color.rgb = TEXT_MUTED if not is_hero else TEXT_WHITE

    # Bottom Callout Banner
    bot_banner = add_panel(s3, Inches(0.8), Inches(6.25), Inches(11.733), Inches(0.75), border_color=ACCENT_BLUE)
    bb_txt = s3.shapes.add_textbox(Inches(1.0), Inches(6.32), Inches(11.3), Inches(0.6))
    p_call = bb_txt.text_frame.paragraphs[0]
    p_call.text = "CORE ARCHITECTURAL THESIS: DO NOT MANAGE ISOLATED CHAT SESSIONS. COORDINATE WHOLE TEAMS AS AN OPERATING SYSTEM."
    p_call.font.name = FONT_MONO
    p_call.font.size = Pt(10.5)
    p_call.font.bold = True
    p_call.font.color.rgb = TEXT_WHITE

    # =========================================================
    # SLIDE 04: SYSTEM ARCHITECTURE: INSIDE GEETORUSAI
    # =========================================================
    s4 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s4)
    add_header(s4, 4, "Technical Deep-Dive // Full Stack Topology",
               "SYSTEM ARCHITECTURE: INSIDE THE GEETORUSAI CONTROL PLANE",
               "A 6-layer modular stack decoupling UI, application state, multi-agent orchestration, and sandboxed runtimes.")

    layers = [
        ("LAYER 1: USER INTERFACE", "React 19 + Vite 6 + Tailwind + Lucide Icons", 
         "Company Dashboard // Agent Configurator // Task Kanban & DAG Graph // Live Token & Cost Telemetry // Real-time Approval Gates", 
         "[ VERIFIED IN REPO ]", BADGE_GREEN),
        ("LAYER 2: API & APP SERVICES", "Express + TypeScript + Modular Routes", 
         "Company Scope Guards // JWT & Session Auth // Heartbeat Daemon (heartbeat.ts) // Task Lifecycle & Dependency API", 
         "[ VERIFIED IN REPO ]", BADGE_GREEN),
        ("LAYER 3: CONTROL PLANE", "Orchestration & Goal Decomposition Engine", 
         "Goal Decomposition Pipeline // Role-based Task Dispatch // Dependency Graph Resolution // Failure Recovery Policies", 
         "[ PARTIAL / ACTIVE ]", BADGE_AMBER),
        ("LAYER 4: AGENT EXECUTION", "Pluggable Agent Runtimes & Adapters", 
         "Tech Lead // Backend Specialist // QA Auditor // Security Sentinel // Research Analyst // Custom Tool Schemas", 
         "[ PARTIAL / ACTIVE ]", BADGE_AMBER),
        ("LAYER 5: MODEL & RUNTIME ADAPTERS", "Unified Local + Remote Model Routing", 
         "OpenCode Local Model Adapter // Ollama & LMStudio Integration // OpenAI & Anthropic Hosted APIs // Auto-fallback Fallback Aliases", 
         "[ VERIFIED IN REPO ]", BADGE_GREEN),
        ("LAYER 6: DATA & OBSERVABILITY", "PostgreSQL + Drizzle ORM + Migration Runtime", 
         "Embedded PG Zero-Config Runtime // Heartbeat & Audit Logs // Token Consumption Ledger // Structured Task Artifacts", 
         "[ VERIFIED IN REPO ]", BADGE_GREEN)
    ]

    for idx, (title, tech, desc, badge_txt, badge_col) in enumerate(layers):
        top_pos = Inches(1.85 + idx * 0.76)
        panel = add_panel(s4, Inches(0.8), top_pos, Inches(9.2), Inches(0.70), border_color=BORDER_GRAY)
        
        txt_box = s4.shapes.add_textbox(Inches(0.95), top_pos + Inches(0.04), Inches(8.8), Inches(0.62))
        tf = txt_box.text_frame
        tf.word_wrap = True
        
        p0 = tf.paragraphs[0]
        p0.text = f"{title}  |  {tech}"
        p0.font.name = FONT_MONO
        p0.font.size = Pt(9.5)
        p0.font.bold = True
        p0.font.color.rgb = ACCENT_SAND
        
        p1 = tf.add_paragraph()
        p1.text = desc
        p1.font.name = FONT_BODY
        p1.font.size = Pt(8.5)
        p1.font.color.rgb = TEXT_WHITE
        p1.space_before = Pt(2)
        
        add_badge(s4, Inches(8.3), top_pos + Inches(0.18), badge_txt, badge_col, width=Inches(1.5), height=Inches(0.3))

    # Cross-Cutting Right Pillar: GOVERNANCE & SECURITY
    gov_panel = add_panel(s4, Inches(10.2), Inches(1.85), Inches(2.333), Inches(5.0), border_color=ACCENT_SAND, bg_color=PANEL_BG_ALT)
    gov_box = s4.shapes.add_textbox(Inches(10.3), Inches(1.95), Inches(2.133), Inches(4.7))
    tf_g = gov_box.text_frame
    tf_g.word_wrap = True
    
    pg0 = tf_g.paragraphs[0]
    pg0.text = "CROSS-CUTTING\nGOVERNANCE"
    pg0.font.name = FONT_HEADLINE
    pg0.font.size = Pt(12)
    pg0.font.bold = True
    pg0.font.color.rgb = ACCENT_SAND

    gov_points = [
        ("Token-Gate Enforcer", "Hard company-level limits prevent infinite cost loops."),
        ("Approval Boundaries", "Destructive git/bash operations require user sign-off."),
        ("Company Isolation", "Multi-tenant tenant ID scoping across all tables."),
        ("Audit Telemetry", "Granular timestamps and step-by-step agent transcripts.")
    ]
    for k, v in gov_points:
        p_k = tf_g.add_paragraph()
        p_k.text = f"> {k}"
        p_k.font.name = FONT_MONO
        p_k.font.size = Pt(9)
        p_k.font.bold = True
        p_k.font.color.rgb = ACCENT_BLUE
        p_k.space_before = Pt(8)
        
        p_v = tf_g.add_paragraph()
        p_v.text = v
        p_v.font.name = FONT_BODY
        p_v.font.size = Pt(8)
        p_v.font.color.rgb = TEXT_MUTED

    # =========================================================
    # SLIDE 05: HOW IT WORKS (GOAL TO VERIFIED OUTPUT)
    # =========================================================
    s5 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s5)
    add_header(s5, 5, "Execution Pipeline & State Transition",
               "HOW IT WORKS: FROM USER GOAL TO VERIFIED, PRODUCTION OUTPUT",
               "Step-by-step lifecycle showing goal decomposition, agent execution, automated QA, security gate, and human sign-off.")

    steps = [
        ("01", "GOAL INGESTION", "User specifies high-level objective in UI or via CLI/API.", "USER INITIATION"),
        ("02", "DECOMPOSITION", "Tech Lead analyzes requirements and produces task DAG.", "ORCHESTRATOR"),
        ("03", "DISPATCH & ASSIGN", "Tasks assigned to specialized workers (Dev, Analyst, QA).", "SCHEDULER"),
        ("04", "EXECUTION LOOP", "Agents write code, execute tools, and build artifacts.", "SANDBOX RUNTIME"),
        ("05", "QA VERIFICATION", "Automated test suites & syntax audits run on outputs.", "VERIFICATION ENGINE"),
        ("06", "SECURITY GATE", "Code audit scans for vulnerabilities and secret exposure.", "SECURITY SENTINEL"),
        ("07", "APPROVAL GATE", "Human reviews diffs & approves deployment/merge.", "HUMAN-IN-THE-LOOP"),
        ("08", "FINAL DELIVERY", "Verified artifact deployed or pushed to remote repository.", "OUTCOME DELIVERED")
    ]

    # Two rows of 4 panels
    for i, (num, title, desc, actor) in enumerate(steps):
        row = i // 4
        col = i % 4
        left = Inches(0.8 + col * 2.98)
        top = Inches(1.9 + row * 2.45)
        
        is_approval = (num == "07")
        border = ACCENT_SAND if is_approval else BORDER_GRAY
        bg = PANEL_BG_ALT if is_approval else PANEL_BG
        
        add_panel(s5, left, top, Inches(2.8), Inches(2.2), border_color=border, bg_color=bg)
        
        tbox = s5.shapes.add_textbox(left + Inches(0.15), top + Inches(0.12), Inches(2.5), Inches(2.0))
        tf = tbox.text_frame
        tf.word_wrap = True
        
        p0 = tf.paragraphs[0]
        p0.text = f"[ STEP {num} ]"
        p0.font.name = FONT_MONO
        p0.font.size = Pt(8.5)
        p0.font.bold = True
        p0.font.color.rgb = ACCENT_BLUE if not is_approval else ACCENT_SAND
        
        p1 = tf.add_paragraph()
        p1.text = title
        p1.font.name = FONT_HEADLINE
        p1.font.size = Pt(11)
        p1.font.bold = True
        p1.font.color.rgb = TEXT_WHITE
        p1.space_before = Pt(2)
        
        p2 = tf.add_paragraph()
        p2.text = desc
        p2.font.name = FONT_BODY
        p2.font.size = Pt(8.5)
        p2.font.color.rgb = TEXT_MUTED if not is_approval else TEXT_WHITE
        p2.space_before = Pt(4)
        
        p3 = tf.add_paragraph()
        p3.text = f"ACTOR: {actor}"
        p3.font.name = FONT_MONO
        p3.font.size = Pt(7.5)
        p3.font.color.rgb = ACCENT_SAND if not is_approval else ACCENT_BLUE
        p3.space_before = Pt(6)

    # Bottom status indicator
    bot_box = s5.shapes.add_textbox(Inches(0.8), Inches(6.8), Inches(11.733), Inches(0.4))
    p_b = bot_box.text_frame.paragraphs[0]
    p_b.text = "NOTE: Unlike black-box autonomous loops, GeetorusAI halts execution at Step 07 until explicit human confirmation is received."
    p_b.font.name = FONT_MONO
    p_b.font.size = Pt(8.5)
    p_b.font.color.rgb = ACCENT_SAND

    # =========================================================
    # SLIDE 06: MULTI-AGENT COLLABORATION (VIRTUAL AI COMPANY)
    # =========================================================
    s6 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s6)
    add_header(s6, 6, "Organizational Hierarchy & Task Delegation",
               "MULTI-AGENT COLLABORATION: A VIRTUAL AI COMPANY STRUCTURE",
               "Specialized agents mirror software company roles, passing structured artifacts through dependency-managed execution lanes.")

    roles = [
        ("ORCHESTRATOR / TECH LEAD", "Decomposes user objectives into atomic tasks, monitors agent health, resolves deadlocks, and aggregates results.", "GPT-4o / Claude 3.7", ACCENT_SAND),
        ("RESEARCH ANALYST", "Investigates APIs, retrieves documentation, scrapes requirements, and prepares background synthesis.", "DeepSeek-R1 / Sonnet", BORDER_GRAY),
        ("SOFTWARE DEVELOPER", "Implements features, writes modular code, refactors components, and generates unit test harnesses.", "OpenCode / Codex / Gemma", ACCENT_BLUE),
        ("QA ENGINEER", "Executes integration tests, runs linters, catches edge cases, and returns structured regression tickets.", "Claude Haiku / GPT-4o-mini", BORDER_GRAY),
        ("SECURITY AUDITOR", "Reviews code diffs for CVEs, credential leaks, injection vectors, and permission boundaries.", "Nemotron / Llama-Guard", BORDER_GRAY),
        ("RELEASE REVIEWER", "Validates output against original user acceptance criteria before signaling for human sign-off.", "Tech Lead / Orchestrator", BORDER_GRAY)
    ]

    for idx, (title, desc, model, border) in enumerate(roles):
        row = idx // 3
        col = idx % 3
        left = Inches(0.8 + col * 4.0)
        top = Inches(1.9 + row * 2.4)
        
        add_panel(s6, left, top, Inches(3.7), Inches(2.15), border_color=border, bg_color=PANEL_BG)
        
        box = s6.shapes.add_textbox(left + Inches(0.15), top + Inches(0.12), Inches(3.4), Inches(1.9))
        tf = box.text_frame
        tf.word_wrap = True
        
        p0 = tf.paragraphs[0]
        p0.text = f"ROLE // {idx+1:02d}"
        p0.font.name = FONT_MONO
        p0.font.size = Pt(8.5)
        p0.font.bold = True
        p0.font.color.rgb = ACCENT_SAND if border == ACCENT_SAND else (ACCENT_BLUE if border == ACCENT_BLUE else TEXT_MUTED)
        
        p1 = tf.add_paragraph()
        p1.text = title
        p1.font.name = FONT_HEADLINE
        p1.font.size = Pt(11.5)
        p1.font.bold = True
        p1.font.color.rgb = TEXT_WHITE
        p1.space_before = Pt(2)
        
        p2 = tf.add_paragraph()
        p2.text = desc
        p2.font.name = FONT_BODY
        p2.font.size = Pt(9)
        p2.font.color.rgb = TEXT_MUTED
        p2.space_before = Pt(4)
        
        p3 = tf.add_paragraph()
        p3.text = f"SUGGESTED ENGINE: {model}"
        p3.font.name = FONT_MONO
        p3.font.size = Pt(8)
        p3.font.color.rgb = ACCENT_BLUE
        p3.space_before = Pt(6)

    # Bottom workflow summary
    bot_panel = add_panel(s6, Inches(0.8), Inches(6.5), Inches(11.733), Inches(0.55), border_color=BORDER_GRAY)
    b_txt = s6.shapes.add_textbox(Inches(0.95), Inches(6.55), Inches(11.4), Inches(0.45))
    p_f = b_txt.text_frame.paragraphs[0]
    p_f.text = "PARALLEL EXECUTION: Independent research & coding run concurrently. Sequential gates block QA until development merges."
    p_f.font.name = FONT_MONO
    p_f.font.size = Pt(9)
    p_f.font.bold = True
    p_f.font.color.rgb = TEXT_WHITE

    # =========================================================
    # SLIDE 07: FEATURES & CAPABILITIES (BRUTALIST GRID)
    # =========================================================
    s7 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s7)
    add_header(s7, 7, "Capability Matrix & Verification Audit",
               "FEATURES & CAPABILITIES: AUDITED STATUS MATRIX",
               "Clear demarcation between verified production capabilities in the v0.3.1 codebase, partial implementations, and roadmap goals.")

    capabilities = [
        ("01 / AGENT MANAGEMENT", [
            ("Company-Scoped Agent Catalog", "[ VERIFIED ]", BADGE_GREEN),
            ("Custom Role & Skill Bindings", "[ VERIFIED ]", BADGE_GREEN),
            ("Real-time Heartbeat & Health Check", "[ VERIFIED ]", BADGE_GREEN),
            ("Dynamic Autonomous Agent Spawning", "[ PARTIAL ]", BADGE_AMBER),
        ]),
        ("02 / WORKFLOW ORCHESTRATION", [
            ("Task DAG Creation & State Tracking", "[ VERIFIED ]", BADGE_GREEN),
            ("Step-level Dependency Management", "[ VERIFIED ]", BADGE_GREEN),
            ("Automated Task Retry & Recovery", "[ PARTIAL ]", BADGE_AMBER),
            ("Autonomous Multi-Goal Rescheduling", "[ PLANNED ]", BADGE_GRAY),
        ]),
        ("03 / MODEL CONNECTIVITY", [
            ("OpenCode Local Execution Adapter", "[ VERIFIED ]", BADGE_GREEN),
            ("Hosted LLM Support (OpenAI/Anthropic)", "[ VERIFIED ]", BADGE_GREEN),
            ("Local Runtime Aliasing & Auto-fallback", "[ VERIFIED ]", BADGE_GREEN),
            ("Dynamic Cost/Latency Model Router", "[ PLANNED ]", BADGE_GRAY),
        ]),
        ("04 / GOVERNANCE & BUDGETS", [
            ("Hard Company Token-Gate Enforcement", "[ VERIFIED ]", BADGE_GREEN),
            ("Approval Boundary Modals in UI", "[ VERIFIED ]", BADGE_GREEN),
            ("Granular Cost Ledger per Run", "[ VERIFIED ]", BADGE_GREEN),
            ("Multi-Tenant Org SSO / RBAC", "[ PLANNED ]", BADGE_GRAY),
        ]),
        ("05 / DEVELOPER EXPERIENCE", [
            ("Modern Digital Brutalist UI", "[ VERIFIED ]", BADGE_GREEN),
            ("Comprehensive CLI & Local Runner", "[ VERIFIED ]", BADGE_GREEN),
            ("Embedded Zero-Config PostgreSQL", "[ VERIFIED ]", BADGE_GREEN),
            ("Custom Plugin SDK Architecture", "[ PARTIAL ]", BADGE_AMBER),
        ]),
        ("06 / RESILIENCE & OBSERVABILITY", [
            ("End-to-End Audit & Execution Logs", "[ VERIFIED ]", BADGE_GREEN),
            ("Structured JSON Event Streams", "[ VERIFIED ]", BADGE_GREEN),
            ("Automated Rollback on Test Failure", "[ PARTIAL ]", BADGE_AMBER),
            ("Self-Healing Agent Network", "[ PLANNED ]", BADGE_GRAY),
        ]),
    ]

    for idx, (section_title, items) in enumerate(capabilities):
        row = idx // 3
        col = idx % 3
        left = Inches(0.8 + col * 4.0)
        top = Inches(1.9 + row * 2.5)
        
        add_panel(s7, left, top, Inches(3.7), Inches(2.3), border_color=BORDER_GRAY)
        
        box = s7.shapes.add_textbox(left + Inches(0.12), top + Inches(0.1), Inches(3.45), Inches(2.1))
        tf = box.text_frame
        tf.word_wrap = True
        
        p0 = tf.paragraphs[0]
        p0.text = section_title
        p0.font.name = FONT_HEADLINE
        p0.font.size = Pt(11)
        p0.font.bold = True
        p0.font.color.rgb = ACCENT_SAND
        
        for name, status, color in items:
            p_i = tf.add_paragraph()
            p_i.text = f"• {name} "
            p_i.font.name = FONT_BODY
            p_i.font.size = Pt(8.5)
            p_i.font.color.rgb = TEXT_WHITE
            p_i.space_before = Pt(3)

            # Add status text
            run = p_i.add_run()
            run.text = f"{status}"
            run.font.name = FONT_MONO
            run.font.size = Pt(7.5)
            run.font.bold = True
            run.font.color.rgb = color

    # =========================================================
    # SLIDE 08: TARGET PERSONAS (WHO IS GEETORUSAI FOR?)
    # =========================================================
    s8 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s8)
    add_header(s8, 8, "Audience Alignment & User Value Drivers",
               "TARGET PERSONAS: WHO NEEDS THE GEETORUSAI CONTROL PLANE?",
               "Addressing specific operational pain points across indie builders, high-velocity startups, software teams, and enterprises.")

    personas = [
        ("01 / INDIE DEVELOPERS & BUILDERS", 
         "PAIN: Context switching between coding, testing, docs, and deployments alone.\n"
         "WORKFLOW: Assign feature requests to Dev agent, test generation to QA agent.\n"
         "VALUE: 5x delivery velocity without hiring contractor teams."),
        ("02 / FAST-GROWING TECH STARTUPS", 
         "PAIN: High developer burn, slow sprint cycles, unmanaged AI tool sprawl.\n"
         "WORKFLOW: Standardize automated code reviews, PR audits, and API docs.\n"
         "VALUE: Enforces team-wide standards and cuts manual review time by 60%."),
        ("03 / ENTERPRISE SOFTWARE TEAMS", 
         "PAIN: Fear of unconstrained AI agents committing unvetted code into production.\n"
         "WORKFLOW: Mandatory approval boundaries and strict token budget policies.\n"
         "VALUE: Governed autonomy with full SOC2-ready auditability and rollback."),
        ("04 / AI RESEARCHERS & EXPERIMENTERS", 
         "PAIN: Difficulty bench-marking multi-agent graphs across diverse local models.\n"
         "WORKFLOW: Pluggable model adapters (Ollama, LMStudio, OpenCode, Cloud APIs).\n"
         "VALUE: Transparent runtime metrics, token traces, and zero vendor lock-in.")
    ]

    for idx, (title, content) in enumerate(personas):
        row = idx // 2
        col = idx % 2
        left = Inches(0.8 + col * 6.0)
        top = Inches(1.9 + row * 2.45)
        
        is_highlight = (idx == 0 or idx == 2)
        border = ACCENT_SAND if is_highlight else BORDER_GRAY
        
        add_panel(s8, left, top, Inches(5.6), Inches(2.25), border_color=border)
        
        box = s8.shapes.add_textbox(left + Inches(0.2), top + Inches(0.15), Inches(5.2), Inches(1.95))
        tf = box.text_frame
        tf.word_wrap = True
        
        p0 = tf.paragraphs[0]
        p0.text = title
        p0.font.name = FONT_HEADLINE
        p0.font.size = Pt(12)
        p0.font.bold = True
        p0.font.color.rgb = ACCENT_SAND if is_highlight else ACCENT_BLUE
        
        lines = content.split("\n")
        for line in lines:
            p_l = tf.add_paragraph()
            p_l.text = line
            p_l.font.name = FONT_BODY
            p_l.font.size = Pt(9.5)
            p_l.font.color.rgb = TEXT_WHITE if "VALUE:" in line else TEXT_MUTED
            p_l.space_before = Pt(4)

    # Bottom assurance banner
    banner = add_panel(s8, Inches(0.8), Inches(6.55), Inches(11.733), Inches(0.55), border_color=ACCENT_BLUE)
    bt = s8.shapes.add_textbox(Inches(1.0), Inches(6.6), Inches(11.3), Inches(0.4))
    p_bt = bt.text_frame.paragraphs[0]
    p_bt.text = "CORE PROMISE: Whether you are 1 person building a SaaS or a 50-person engineering org, GeetorusAI scales operational control."
    p_bt.font.name = FONT_MONO
    p_bt.font.size = Pt(9.5)
    p_bt.font.bold = True
    p_bt.font.color.rgb = TEXT_WHITE

    # =========================================================
    # SLIDE 09: COMPETITIVE LANDSCAPE (WHERE DO WE FIT?)
    # =========================================================
    s9 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s9)
    add_header(s9, 9, "Market Positioning & Objective Benchmark",
               "COMPETITIVE LANDSCAPE: WHERE DOES GEETORUSAI FIT?",
               "Unlike code-only agent libraries or isolated coding bots, GeetorusAI delivers a comprehensive, self-hostable Virtual Company Control Plane.")

    # Table layout
    table_shape = s9.shapes.add_table(6, 6, Inches(0.8), Inches(1.9), Inches(11.733), Inches(4.5))
    table = table_shape.table

    # Column widths
    table.columns[0].width = Inches(2.3) # Dimension
    table.columns[1].width = Inches(1.9) # GeetorusAI
    table.columns[2].width = Inches(1.9) # LangGraph
    table.columns[3].width = Inches(1.9) # CrewAI
    table.columns[4].width = Inches(1.9) # AutoGen
    table.columns[5].width = Inches(1.833) # OpenHands

    headers = ["CAPABILITY / CRITERIA", "GEETORUSAI", "LANGGRAPH", "CREWAI", "AUTOGEN", "OPENHANDS"]
    for col_idx, h_text in enumerate(headers):
        cell = table.cell(0, col_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = PANEL_BG_ALT if col_idx != 1 else ACCENT_BLUE
        p = cell.text_frame.paragraphs[0]
        p.text = h_text
        p.alignment = PP_ALIGN.CENTER
        p.font.name = FONT_MONO
        p.font.size = Pt(9)
        p.font.bold = True
        p.font.color.rgb = TEXT_WHITE

    matrix_rows = [
        ("Primary Product Class", "Control Plane / OS", "Graph Framework", "Agent Framework", "Multi-Agent SDK", "Single Coding Agent"),
        ("Out-of-Box Web UI", "Full React Dashboard", "LangGraph Studio", "CrewAI Enterprise", "AutoGen Studio", "React Web Sandbox"),
        ("Token & Budget Gates", "Hard Limits Verified", "Config Dependent", "Manual Tracking", "Manual Tracking", "Session Limits"),
        ("Approval Boundaries", "Native Modal Gates", "Human-in-loop Node", "Manual Hook", "UserProxyAgent", "Terminal Prompts"),
        ("Self-Hosted / Open DB", "PostgreSQL + Drizzle", "Cloud / Local state", "Cloud / SQLite", "Local JSON/SQLite", "Docker Container"),
    ]

    for row_idx, row_data in enumerate(matrix_rows, start=1):
        for col_idx, text in enumerate(row_data):
            cell = table.cell(row_idx, col_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = PANEL_BG if col_idx != 1 else RGBColor(16, 26, 48)
            p = cell.text_frame.paragraphs[0]
            p.text = text
            p.alignment = PP_ALIGN.CENTER if col_idx > 0 else PP_ALIGN.LEFT
            p.font.name = FONT_MONO if col_idx == 0 else FONT_BODY
            p.font.size = Pt(8.5)
            p.font.bold = (col_idx == 1)
            p.font.color.rgb = ACCENT_SAND if col_idx == 1 else (TEXT_WHITE if col_idx == 0 else TEXT_MUTED)

    # Footnote citation
    fn_box = s9.shapes.add_textbox(Inches(0.8), Inches(6.6), Inches(11.733), Inches(0.4))
    p_fn = fn_box.text_frame.paragraphs[0]
    p_fn.text = "SOURCES: Official documentation from LangChain/LangGraph, CrewAI, Microsoft AutoGen, and OpenHands (AllRightsReserved 2025/2026). Comparative matrix reflects out-of-the-box features vs. required developer scaffolding."
    p_fn.font.name = FONT_MONO
    p_fn.font.size = Pt(8)
    p_fn.font.color.rgb = TEXT_MUTED

    # =========================================================
    # SLIDE 10: DIFFERENTIATION (WHY GEETORUSAI?)
    # =========================================================
    s10 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s10)
    add_header(s10, 10, "Strategic Moat & Technical Edge",
               "DIFFERENTIATION: WHY BUILD ON GEETORUSAI?",
               "The strategic architecture that sets GeetorusAI apart from code libraries, black-box bots, and proprietary closed clouds.")

    # 3 Strategic Pillars
    pillars = [
        ("PILLAR 01: CONTROL PLANE FIRST",
         "Libraries give you code syntax; GeetorusAI gives you an operational control plane.",
         [
             "Pre-built company workspaces and permission hierarchies.",
             "Persistent task DAGs that survive server restarts.",
             "Decoupled from specific model APIs—switch from OpenAI to local Ollama in one click.",
             "True multi-agent coordination, not a single looped prompt."
         ], ACCENT_SAND),
        ("PILLAR 02: GOVERNED BY DESIGN",
         "Autonomy without governance is an enterprise non-starter.",
         [
             "Hardware-enforced token thresholds per company.",
             "Interactive approval gates for git pushes and database migrations.",
             "Full audit trails recording model tokens, execution latency, and bash traces.",
             "Air-gapped and self-hostable on internal private clouds."
         ], ACCENT_BLUE),
        ("PILLAR 03: DEVELOPER TRANSPARENCY",
         "Zero vendor lock-in with a modular, inspectable TypeScript/React architecture.",
         [
             "Clean separation: Server, UI, DB, Shared, Adapters, Plugins.",
             "Embedded zero-config PostgreSQL for immediate local hacking.",
             "Extensible adapter SDK to plug in proprietary enterprise tools.",
             "Modern brutalist design language for dense, productive workflows."
         ], BORDER_GRAY)
    ]

    for idx, (p_title, p_lead, p_bullets, border) in enumerate(pillars):
        left = Inches(0.8 + idx * 4.0)
        add_panel(s10, left, Inches(1.9), Inches(3.7), Inches(4.5), border_color=border, bg_color=PANEL_BG)
        
        box = s10.shapes.add_textbox(left + Inches(0.18), Inches(2.05), Inches(3.34), Inches(4.2))
        tf = box.text_frame
        tf.word_wrap = True
        
        p0 = tf.paragraphs[0]
        p0.text = p_title
        p0.font.name = FONT_HEADLINE
        p0.font.size = Pt(12)
        p0.font.bold = True
        p0.font.color.rgb = border if border != BORDER_GRAY else TEXT_WHITE
        
        p1 = tf.add_paragraph()
        p1.text = p_lead
        p1.font.name = FONT_BODY
        p1.font.size = Pt(9.5)
        p1.font.bold = True
        p1.font.color.rgb = TEXT_WHITE
        p1.space_before = Pt(6)

        for b in p_bullets:
            pb = tf.add_paragraph()
            pb.text = f"> {b}"
            pb.font.name = FONT_BODY
            pb.font.size = Pt(9)
            pb.font.color.rgb = TEXT_MUTED
            pb.space_before = Pt(6)

    # Bottom summary
    bot_box = s10.shapes.add_textbox(Inches(0.8), Inches(6.6), Inches(11.733), Inches(0.4))
    p_b = bot_box.text_frame.paragraphs[0]
    p_b.text = "POSITIONING STATEMENT: GeetorusAI turns autonomous AI agents into controllable, auditable, and collaborative engineering teammates."
    p_b.font.name = FONT_MONO
    p_b.font.size = Pt(9)
    p_b.font.color.rgb = ACCENT_SAND

    # =========================================================
    # SLIDE 11: BUSINESS MODEL & COMMERCIAL OPPORTUNITY
    # =========================================================
    s11 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s11)
    add_header(s11, 11, "Commercialization & Market Dynamics",
               "BUSINESS MODEL: PROPOSED MONETIZATION & MARKET EXPANSION",
               "An open-core model designed to capture developer grassroots adoption and transition into governed enterprise control planes.")

    # 3 Revenue Streams Panels
    streams = [
        ("TIER 1: OPEN-SOURCE CORE", "FREE FOREVER // APACHE 2.0 / MIT",
         "• Self-hosted single-node instance\n• Embedded PostgreSQL runtime\n• Unlimited local and hosted model connections\n• Core task DAG decomposition engine\n• Community plugins and role definitions\n\nGOAL: Drive global developer mindshare and become the default standard for autonomous agent coordination.",
         BORDER_GRAY),
        ("TIER 2: MANAGED PRO & TEAMS", "SUBSCRIPTION (SAAS / CLOUD)",
         "• Fully hosted Geetorus Cloud (no ops required)\n• Multi-user team collaboration & shared workspaces\n• Persistent distributed cloud storage\n• Centralized API key & secret vaulting\n• Advanced analytics and cost optimization alerts\n\nGOAL: Monetize high-velocity startups and growing engineering agencies.",
         ACCENT_SAND),
        ("TIER 3: ENTERPRISE CONTROL PLANE", "ANNUAL CONTRACT // AIR-GAPPED",
         "• Private VPC & air-gapped on-premises deployment\n• Enterprise SSO (SAML/Okta) & granular RBAC\n• SOC2 Type II compliance audit logging\n• Dedicated SLA and custom adapter engineering\n• Multi-region agent mesh coordination\n\nGOAL: Capture high-value enterprise AI governance budgets.",
         ACCENT_BLUE)
    ]

    for idx, (t_title, t_badge, t_content, border) in enumerate(streams):
        left = Inches(0.8 + idx * 4.0)
        add_panel(s11, left, Inches(1.9), Inches(3.7), Inches(4.5), border_color=border, bg_color=PANEL_BG)
        
        box = s11.shapes.add_textbox(left + Inches(0.18), Inches(2.05), Inches(3.34), Inches(4.2))
        tf = box.text_frame
        tf.word_wrap = True
        
        p0 = tf.paragraphs[0]
        p0.text = t_title
        p0.font.name = FONT_HEADLINE
        p0.font.size = Pt(11.5)
        p0.font.bold = True
        p0.font.color.rgb = TEXT_WHITE
        
        p1 = tf.add_paragraph()
        p1.text = t_badge
        p1.font.name = FONT_MONO
        p1.font.size = Pt(8)
        p1.font.bold = True
        p1.font.color.rgb = border if border != BORDER_GRAY else ACCENT_SAND
        p1.space_before = Pt(2)
        
        lines = t_content.split("\n")
        for line in lines:
            pl = tf.add_paragraph()
            pl.text = line
            pl.font.name = FONT_BODY
            pl.font.size = Pt(8.5)
            pl.font.color.rgb = TEXT_MUTED if not line.startswith("GOAL:") else TEXT_WHITE
            pl.space_before = Pt(3)

    # Bottom market context
    bot_box = s11.shapes.add_textbox(Inches(0.8), Inches(6.6), Inches(11.733), Inches(0.4))
    p_b = bot_box.text_frame.paragraphs[0]
    p_b.text = "MARKET CONTEXT: Enterprise AI spending is shifting from raw inference (LLMs) to orchestration, evaluation, and governance platforms."
    p_b.font.name = FONT_MONO
    p_b.font.size = Pt(8.5)
    p_b.font.color.rgb = ACCENT_SAND

    # =========================================================
    # SLIDE 12: SECURITY, RELIABILITY & RESPONSIBLE AUTONOMY
    # =========================================================
    s12 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s12)
    add_header(s12, 12, "Risk Containment & Operational Integrity",
               "SECURITY & RESPONSIBLE AUTONOMY: GOVERNING AGENT RISKS",
               "Architectural isolation boundaries, least-privilege tool execution, hard budget fences, and deterministic rollback systems.")

    # 4 Security Pillars
    sec_cards = [
        ("01 / ISOLATED EXECUTION SANDBOXES",
         "Agent code execution (bash scripts, git operations, file writes) occurs within bounded directories. Untrusted AI code is isolated from host system secrets.",
         "DEFENSE: Host containment & ephemeral execution containers.",
         ACCENT_SAND),
        ("02 / INTERACTIVE APPROVAL BOUNDARIES",
         "High-consequence actions (pushing code to production, deleting databases, altering network configs) halt automatically until verified by a human operator.",
         "DEFENSE: Zero unauthorized production deployments.",
         ACCENT_BLUE),
        ("03 / COMPANY-LEVEL TOKEN GATES",
         "Hard budget fences enforced at the SQL database layer. If an agent loops on an error, the company token gate trips and immediately terminates execution.",
         "DEFENSE: Guaranteed protection against runaway API invoices.",
         ACCENT_SAND),
        ("04 / FULL EXECUTION TRACE AUDITABILITY",
         "Every heartbeat, model prompt, tool call, stdout/stderr stream, and state mutation is logged with immutable timestamps for complete forensics.",
         "DEFENSE: Comprehensive regulatory compliance & post-mortem debuggability.",
         ACCENT_BLUE)
    ]

    for idx, (title, desc, defense, border) in enumerate(sec_cards):
        row = idx // 2
        col = idx % 2
        left = Inches(0.8 + col * 6.0)
        top = Inches(1.9 + row * 2.3)
        
        add_panel(s12, left, top, Inches(5.6), Inches(2.1), border_color=border, bg_color=PANEL_BG)
        
        box = s12.shapes.add_textbox(left + Inches(0.2), top + Inches(0.12), Inches(5.2), Inches(1.85))
        tf = box.text_frame
        tf.word_wrap = True
        
        p0 = tf.paragraphs[0]
        p0.text = title
        p0.font.name = FONT_HEADLINE
        p0.font.size = Pt(11.5)
        p0.font.bold = True
        p0.font.color.rgb = border
        
        p1 = tf.add_paragraph()
        p1.text = desc
        p1.font.name = FONT_BODY
        p1.font.size = Pt(9)
        p1.font.color.rgb = TEXT_WHITE
        p1.space_before = Pt(4)
        
        p2 = tf.add_paragraph()
        p2.text = defense
        p2.font.name = FONT_MONO
        p2.font.size = Pt(8.5)
        p2.font.bold = True
        p2.font.color.rgb = ACCENT_SAND
        p2.space_before = Pt(6)

    # Bottom callout
    b_panel = add_panel(s12, Inches(0.8), Inches(6.6), Inches(11.733), Inches(0.5), border_color=BORDER_GRAY)
    bb_txt = s12.shapes.add_textbox(Inches(0.95), Inches(6.65), Inches(11.4), Inches(0.4))
    p_cl = bb_txt.text_frame.paragraphs[0]
    p_cl.text = "PRINCIPLE: AI autonomy is only scalable when paired with rigorous, deterministic safety boundaries."
    p_cl.font.name = FONT_MONO
    p_cl.font.size = Pt(9)
    p_cl.font.bold = True
    p_cl.font.color.rgb = TEXT_WHITE

    # =========================================================
    # SLIDE 13: PRODUCT ROADMAP (NOW / NEXT / LATER)
    # =========================================================
    s13 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s13)
    add_header(s13, 13, "Strategic Evolution & Engineering Milestones",
               "PRODUCT ROADMAP: FROM AGENT CONTROL TO AUTONOMOUS ORGS",
               "A staged progression from stable single-company control plane to distributed, self-healing multi-agent meshes.")

    phases = [
        ("PHASE 1: FOUNDATION", "CURRENT: v0.3.1 (NOW)",
         [
             "[DONE] Company-scoped agent & task persistence",
             "[DONE] Embedded zero-config PostgreSQL runtime",
             "[DONE] OpenCode local model adapter & model fallback",
             "[DONE] Hard token gates & approval boundary UI",
             "[DONE] Modern brutalist engineering interface"
         ], ACCENT_SAND),
        ("PHASE 2: COLLABORATION", "NEXT: v0.4.0 (Q1-Q2)",
         [
             "[NEXT] Multi-agent dynamic DAG rescheduling",
             "[NEXT] Automated regression QA feedback loops",
             "[NEXT] Shared vector workspace memory across agents",
             "[NEXT] Native GitHub PR & CI/CD webhook triggers",
             "[NEXT] Distributed task worker queues (Redis/BullMQ)"
         ], ACCENT_BLUE),
        ("PHASE 3: GOVERNANCE & MESH", "LATER: v0.5.0+ (ROADMAP)",
         [
             "[ROADMAP] Air-gapped enterprise SSO & SAML RBAC",
             "[ROADMAP] Dynamic cross-model cost/latency optimizer",
             "[ROADMAP] Multi-tenant Kubernetes agent cluster deploy",
             "[ROADMAP] Self-healing agent consensus verification",
             "[ROADMAP] Community marketplace for custom roles & tools"
         ], BORDER_GRAY)
    ]

    for idx, (p_head, p_sub, p_items, border) in enumerate(phases):
        left = Inches(0.8 + idx * 4.0)
        add_panel(s13, left, Inches(1.9), Inches(3.7), Inches(4.5), border_color=border, bg_color=PANEL_BG)
        
        box = s13.shapes.add_textbox(left + Inches(0.18), Inches(2.05), Inches(3.34), Inches(4.2))
        tf = box.text_frame
        tf.word_wrap = True
        
        p0 = tf.paragraphs[0]
        p0.text = p_head
        p0.font.name = FONT_HEADLINE
        p0.font.size = Pt(12)
        p0.font.bold = True
        p0.font.color.rgb = TEXT_WHITE
        
        p1 = tf.add_paragraph()
        p1.text = p_sub
        p1.font.name = FONT_MONO
        p1.font.size = Pt(8.5)
        p1.font.bold = True
        p1.font.color.rgb = border if border != BORDER_GRAY else ACCENT_SAND
        p1.space_before = Pt(2)
        
        for item in p_items:
            pi = tf.add_paragraph()
            pi.text = item
            pi.font.name = FONT_BODY
            pi.font.size = Pt(8.5)
            pi.font.color.rgb = TEXT_WHITE if "[DONE]" in item else TEXT_MUTED
            pi.space_before = Pt(4)

    # Bottom footnote
    bot_box = s13.shapes.add_textbox(Inches(0.8), Inches(6.6), Inches(11.733), Inches(0.4))
    p_b = bot_box.text_frame.paragraphs[0]
    p_b.text = "MILESTONE TRACKING: All items labeled [DONE] are verified in git history; future milestones reflect proposed engineering roadmap."
    p_b.font.name = FONT_MONO
    p_b.font.size = Pt(8.5)
    p_b.font.color.rgb = TEXT_MUTED

    # =========================================================
    # SLIDE 14: CLOSING (THE COMPANY THAT RUNS ON AI TEAMS)
    # =========================================================
    s14 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s14)

    # Architectural outer frame
    frame = s14.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(0.8), Inches(11.733), Inches(5.9))
    frame.fill.background()
    frame.line.color.rgb = BORDER_GRAY
    frame.line.width = Pt(1)

    # Headline Box
    top_box = s14.shapes.add_textbox(Inches(1.2), Inches(1.1), Inches(10.5), Inches(0.4))
    p = top_box.text_frame.paragraphs[0]
    p.text = "// CONCLUSION // GEETORUSAI CONTROL PLANE"
    p.font.name = FONT_MONO
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = ACCENT_SAND

    big_box = s14.shapes.add_textbox(Inches(1.2), Inches(1.5), Inches(11.0), Inches(1.6))
    p_big = big_box.text_frame.paragraphs[0]
    p_big.text = "ONE GOAL. MULTIPLE AGENTS.\nCOORDINATED EXECUTION."
    p_big.font.name = FONT_HEADLINE
    p_big.font.size = Pt(38)
    p_big.font.bold = True
    p_big.font.color.rgb = TEXT_WHITE

    # 3 Summary Cards
    concl_cards = [
        ("VERIFIED FOUNDATION", "Production-tested v0.3.1 core with embedded DB, React UI, heartbeat runner, and model adapters ready today."),
        ("GOVERNED AUTONOMY", "Deterministic budget limits and human-in-the-loop approval gates designed for real software engineering risks."),
        ("OPEN ECOSYSTEM", "Extensible, self-hostable control plane ready to coordinate whatever frontier models or local runtimes you deploy.")
    ]

    for idx, (title, desc) in enumerate(concl_cards):
        left = Inches(1.2 + idx * 3.75)
        add_panel(s14, left, Inches(3.3), Inches(3.45), Inches(1.8), border_color=BORDER_GRAY, bg_color=PANEL_BG)
        
        cbox = s14.shapes.add_textbox(left + Inches(0.15), Inches(3.4), Inches(3.15), Inches(1.6))
        tf = cbox.text_frame
        tf.word_wrap = True
        
        p0 = tf.paragraphs[0]
        p0.text = f"[ 0{idx+1} ]  {title}"
        p0.font.name = FONT_MONO
        p0.font.size = Pt(9.5)
        p0.font.bold = True
        p0.font.color.rgb = ACCENT_SAND if idx == 0 else (ACCENT_BLUE if idx == 1 else TEXT_WHITE)
        
        p1 = tf.add_paragraph()
        p1.text = desc
        p1.font.name = FONT_BODY
        p1.font.size = Pt(9)
        p1.font.color.rgb = TEXT_MUTED
        p1.space_before = Pt(4)

    # Call to action footer
    cta_panel = add_panel(s14, Inches(1.2), Inches(5.3), Inches(10.9), Inches(1.0), border_color=ACCENT_SAND, bg_color=PANEL_BG_ALT)
    cta_box = s14.shapes.add_textbox(Inches(1.4), Inches(5.4), Inches(10.5), Inches(0.8))
    tf_cta = cta_box.text_frame
    tf_cta.word_wrap = True
    
    p_c1 = tf_cta.paragraphs[0]
    p_c1.text = "JOIN THE NEXT GENERATION OF AUTONOMOUS ENGINEERING"
    p_c1.font.name = FONT_HEADLINE
    p_c1.font.size = Pt(13)
    p_c1.font.bold = True
    p_c1.font.color.rgb = TEXT_WHITE
    
    p_c2 = tf_cta.add_paragraph()
    p_c2.text = "GitHub: https://github.com/geetorusai/geetorus  |  Repository: geetorus-core v0.3.1  |  License: Open Source"
    p_c2.font.name = FONT_MONO
    p_c2.font.size = Pt(9.5)
    p_c2.font.color.rgb = ACCENT_SAND
    p_c2.space_before = Pt(2)

    # Save presentation
    prs.save(output_path)
    print(f"SUCCESS: Generated 14-slide Brutalist Presentation at '{output_path}'")

if __name__ == "__main__":
    out = "GeetorusAI_Brutalist_Presentation.pptx"
    if len(sys.argv) > 1:
        out = sys.argv[1]
    create_deck(out)
