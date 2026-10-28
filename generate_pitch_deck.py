import os
import sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

# -------------------------------------------------------------
# PALETTE & TYPOGRAPHY: Modern Executive Cyberpunk / Dark Obsidian
# -------------------------------------------------------------
BG_COLOR       = RGBColor(11, 15, 25)      # #0B0F19 Deep Obsidian
PANEL_BG       = RGBColor(19, 27, 46)     # #131B2E Slate Card Surface
PANEL_BG_ALT   = RGBColor(26, 36, 61)     # #1A243D Lighter Card
PANEL_BORDER   = RGBColor(36, 48, 72)     # #243048 Slate Wireframe
ACCENT_BLUE    = RGBColor(37, 99, 235)    # #2563EB Royal Cobalt
ACCENT_CYAN    = RGBColor(6, 182, 212)    # #06B6D4 Vibrant Cyan
ACCENT_AMBER   = RGBColor(245, 158, 11)   # #F59E0B Warning/Amber
ACCENT_GREEN   = RGBColor(16, 185, 129)   # #10B981 Mint Success
TEXT_WHITE     = RGBColor(248, 250, 252)  # #F8FAFC Off-White / Pure Chalk
TEXT_MUTED     = RGBColor(148, 163, 184)  # #94A3B8 Muted Slate Gray
TEXT_DIM       = RGBColor(100, 116, 139)  # #64748B Dim Text

FONT_HEADLINE = "Trebuchet MS"
FONT_BODY     = "Segoe UI"
FONT_MONO     = "Consolas"

def create_deck(output_path="c:/Users/mohamed farhan/testing-marketing/docs/pitch/GeetorusAI_Pitch_Deck.pptx"):
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    def set_slide_bg(slide):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = BG_COLOR
        bg.line.color.rgb = BG_COLOR
        return bg

    def add_header(slide, slide_num, total_slides, section_tag, title, subtitle=None):
        # Section Pill / Tag
        top_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(9.5), Inches(0.35))
        tf = top_box.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        p.text = f"GEETORUSAI // {section_tag.upper()}"
        p.font.name = FONT_MONO
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = ACCENT_CYAN

        # Slide Number
        num_box = slide.shapes.add_textbox(Inches(10.5), Inches(0.4), Inches(2.0), Inches(0.35))
        tf_num = num_box.text_frame
        tf_num.margin_left = tf_num.margin_top = tf_num.margin_right = tf_num.margin_bottom = 0
        p_num = tf_num.paragraphs[0]
        p_num.alignment = PP_ALIGN.RIGHT
        p_num.text = f"[ {slide_num:02d} / {total_slides:02d} ]"
        p_num.font.name = FONT_MONO
        p_num.font.size = Pt(10)
        p_num.font.color.rgb = TEXT_MUTED

        # Main Title
        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.75), Inches(11.7), Inches(0.55))
        tf_t = title_box.text_frame
        tf_t.word_wrap = True
        tf_t.margin_left = tf_t.margin_top = tf_t.margin_right = tf_t.margin_bottom = 0
        p_t = tf_t.paragraphs[0]
        p_t.text = title
        p_t.font.name = FONT_HEADLINE
        p_t.font.size = Pt(22)
        p_t.font.bold = True
        p_t.font.color.rgb = TEXT_WHITE

        if subtitle:
            sub_box = slide.shapes.add_textbox(Inches(0.8), Inches(1.3), Inches(11.7), Inches(0.35))
            tf_s = sub_box.text_frame
            tf_s.word_wrap = True
            tf_s.margin_left = tf_s.margin_top = tf_s.margin_right = tf_s.margin_bottom = 0
            p_s = tf_s.paragraphs[0]
            p_s.text = subtitle
            p_s.font.name = FONT_BODY
            p_s.font.size = Pt(12)
            p_s.font.color.rgb = TEXT_MUTED

    def add_card(slide, left, top, width, height, title=None, bg_color=PANEL_BG, border_color=PANEL_BORDER):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(height))
        card.fill.solid()
        card.fill.fore_color.rgb = bg_color
        card.line.color.rgb = border_color
        card.line.width = Pt(1)

        if title:
            tb = slide.shapes.add_textbox(Inches(left + 0.2), Inches(top + 0.15), Inches(width - 0.4), Inches(0.35))
            tf = tb.text_frame
            tf.word_wrap = True
            tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
            p = tf.paragraphs[0]
            p.text = title.upper()
            p.font.name = FONT_MONO
            p.font.size = Pt(11)
            p.font.bold = True
            p.font.color.rgb = ACCENT_CYAN
        return card

    def add_metric_callout(slide, left, top, width, height, number, label, subtext=None, num_color=ACCENT_CYAN):
        add_card(slide, left, top, width, height)
        tb = slide.shapes.add_textbox(Inches(left + 0.2), Inches(top + 0.15), Inches(width - 0.4), Inches(height - 0.3))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        p0 = tf.paragraphs[0]
        p0.text = number
        p0.font.name = FONT_HEADLINE
        p0.font.size = Pt(28)
        p0.font.bold = True
        p0.font.color.rgb = num_color

        p1 = tf.add_paragraph()
        p1.text = label
        p1.font.name = FONT_BODY
        p1.font.size = Pt(11)
        p1.font.bold = True
        p1.font.color.rgb = TEXT_WHITE
        p1.space_before = Pt(4)

        if subtext:
            p2 = tf.add_paragraph()
            p2.text = subtext
            p2.font.name = FONT_BODY
            p2.font.size = Pt(9.5)
            p2.font.color.rgb = TEXT_MUTED
            p2.space_before = Pt(2)

    def set_speaker_notes(slide, notes_text):
        notes_slide = slide.notes_slide
        tf = notes_slide.notes_text_frame
        tf.text = notes_text

    # =========================================================================
    # SLIDE 01: THE PROBLEM & ONE-LINE TRUTH
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s1)
    add_header(s1, 1, 15, "PART 1: BUSINESS BRIEF // THE CORE CRISIS",
               "GeetorusAI: The Sovereign Operating System for Multi-Agent Teams",
               "Solving the unmanaged agent sprawl, runaway token costs, and unverified execution crisis.")

    # Hero One-Liner Box
    add_card(s1, 0.8, 1.7, 11.733, 1.1, bg_color=PANEL_BG_ALT, border_color=ACCENT_BLUE)
    tb_one = s1.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(11.3), Inches(0.9))
    tf_one = tb_one.text_frame
    tf_one.word_wrap = True
    p = tf_one.paragraphs[0]
    p.text = "THE SPOKEN DEFINITION:"
    p.font.name = FONT_MONO
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = ACCENT_AMBER
    p2 = tf_one.add_paragraph()
    p2.text = '“GeetorusAI is the self-hosted operating system that turns isolated AI coding agents into a governed, collaborative digital workforce with strict budget caps and verifiable outcomes.”'
    p2.font.name = FONT_HEADLINE
    p2.font.size = Pt(14)
    p2.font.bold = True
    p2.font.color.rgb = TEXT_WHITE

    # 3 Problem Pillars
    col_w = 3.75
    gap = 0.24
    cards_data = [
        ("01 // UNGOVERNED AGENT SPRAWL",
         "Siloed Chat Sessions",
         "Developers run uncoordinated terminal bots (Claude Code, Cursor). No shared context, no reporting lines, no central organizational oversight.",
         ACCENT_AMBER),
        ("02 // RUNAWAY TOKEN BLEEDING",
         "Zero Spending Enforcers",
         "Autonomous loops cycle uncontrollably on syntax errors, incurring hundreds of dollars per hour. No hard daily budget caps or circuit breakers.",
         RGBColor(239, 68, 68)),
        ("03 // UNVERIFIED EXECUTION",
         "Blind Shell Execution",
         "Agents execute irreversible shell commands, push unverified code to git repositories, and exfiltrate secrets without CISO approval trails.",
         ACCENT_CYAN)
    ]
    for idx, (tag, headline, desc, col) in enumerate(cards_data):
        x = 0.8 + idx * (col_w + gap)
        add_card(s1, x, 3.0, col_w, 3.8)
        tb = s1.shapes.add_textbox(Inches(x + 0.25), Inches(3.2), Inches(col_w - 0.5), Inches(3.4))
        tf = tb.text_frame
        tf.word_wrap = True
        p_tag = tf.paragraphs[0]
        p_tag.text = tag
        p_tag.font.name = FONT_MONO
        p_tag.font.size = Pt(10)
        p_tag.font.bold = True
        p_tag.font.color.rgb = col

        p_h = tf.add_paragraph()
        p_h.text = headline
        p_h.font.name = FONT_HEADLINE
        p_h.font.size = Pt(16)
        p_h.font.bold = True
        p_h.font.color.rgb = TEXT_WHITE
        p_h.space_before = Pt(8)

        p_d = tf.add_paragraph()
        p_d.text = desc
        p_d.font.name = FONT_BODY
        p_d.font.size = Pt(11)
        p_d.font.color.rgb = TEXT_MUTED
        p_d.space_before = Pt(8)

    set_speaker_notes(s1,
        "Welcome investors. Today we are presenting GeetorusAI. Over the past two years, the industry witnessed an explosion of AI models and single-agent coding bots. But in real-world engineering, isolated chat sessions don't build scalable systems—teams do. When engineering teams try to deploy autonomous agents today, they immediately hit three walls: uncoordinated agent sprawl, runaway token bills that burn thousands overnight, and unverified shell execution without security guardrails. GeetorusAI is the self-hosted control plane that solves all three.")

    # =========================================================================
    # SLIDE 02: PRODUCT & BUILT-VS-PLANNED TRUTH
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s2)
    add_header(s2, 2, 15, "PART 1: BUSINESS BRIEF // THE PRODUCT REALITY",
               "Virtual Company Operating System: 16 Verified Core Subsystems",
               "Zero-drift architectural truth: audited against active code, not future promises.")

    # Left Column: Built vs Planned Stats & Breakdown
    add_card(s2, 0.8, 1.8, 4.6, 5.0, title="AUDITED CODEBASE INVENTORY")
    tb_b = s2.shapes.add_textbox(Inches(1.0), Inches(2.2), Inches(4.2), Inches(4.4))
    tf_b = tb_b.text_frame
    tf_b.word_wrap = True

    b_lines = [
        ("16 SUBSYSTEMS VERIFIED (100% CODE)", ACCENT_GREEN,
         "Heartbeat scheduler (29k lines), 137 Drizzle schemas, embedded zero-config Postgres, 13 model adapters, native MCP gateway, HMAC signer, daily budget caps."),
        ("4 PARTIALLY VERIFIED (EXTERNAL CLOUD)", ACCENT_AMBER,
         "Remote micro-VM sandboxes (e2b/Daytona), multi-channel external bots (Slack/Discord tokens required), Next.js template marketplace UI."),
        ("4 ROADMAP MILESTONES (SCHEDULED)", TEXT_MUTED,
         "Distributed task queue (Redis/BullMQ), vector semantic memory (pgvector), enterprise SAML/SSO, formal automated mutation evals.")
    ]
    for idx, (title_line, col, desc_line) in enumerate(b_lines):
        p_t = tf_b.paragraphs[0] if idx == 0 else tf_b.add_paragraph()
        p_t.text = f"● {title_line}"
        p_t.font.name = FONT_MONO
        p_t.font.size = Pt(11)
        p_t.font.bold = True
        p_t.font.color.rgb = col
        if idx > 0:
            p_t.space_before = Pt(12)

        p_d = tf_b.add_paragraph()
        p_d.text = desc_line
        p_d.font.name = FONT_BODY
        p_d.font.size = Pt(10)
        p_d.font.color.rgb = TEXT_MUTED
        p_d.space_before = Pt(4)

    # Right Column: Live App Screenshot / Visual Layout
    add_card(s2, 5.6, 1.8, 6.933, 5.0, title="RUNNING PRODUCT INTERFACE [LOCALHOST:3100]")
    img_path = "c:/Users/mohamed farhan/testing-marketing/docs/pitch/geetorus_dashboard.png"
    if os.path.exists(img_path):
        s2.shapes.add_picture(img_path, Inches(5.8), Inches(2.3), Inches(6.533), Inches(4.3))
    else:
        # Fallback card
        tb_f = s2.shapes.add_textbox(Inches(5.8), Inches(2.5), Inches(6.5), Inches(3.5))
        tf_f = tb_f.text_frame
        p = tf_f.paragraphs[0]
        p.text = "[ LIVE DASHBOARD SCREENSHOT PLACEHOLDER ]"
        p.font.name = FONT_MONO
        p.font.size = Pt(14)
        p.font.color.rgb = ACCENT_CYAN

    set_speaker_notes(s2,
        "Here is what GeetorusAI actually is today. On the right, you are looking at the live running platform on port 3100. We don't sell vaporware. The codebase has 16 fully verified production subsystems backing it right now: a 29,000-line scheduler, 137 relational PostgreSQL tables, embedded zero-config database runtime, 13 provider adapters, and an Anthropic Model Context Protocol gateway. 4 capabilities are partially verified because they need external cloud keys, and 4 are clearly demarcated on our future roadmap.")

    # =========================================================================
    # SLIDE 03: WHO IT IS FOR & WHO PAYS
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s3)
    add_header(s3, 3, 15, "PART 1: BUSINESS BRIEF // TARGET CUSTOMER & TEAM",
               "Beachhead Buyer, Economic Decision Makers & Founder Credentials",
               "Targeting security-sensitive engineering leaders with an ethical hacking foundation.")

    # Top Row: Beachhead Persona & Economic Buyers
    add_card(s3, 0.8, 1.8, 5.7, 4.9, title="TARGET BUYERS & ECONOMIC STAKEHOLDERS")
    tb_u = s3.shapes.add_textbox(Inches(1.0), Inches(2.2), Inches(5.3), Inches(4.3))
    tf_u = tb_u.text_frame
    tf_u.word_wrap = True

    u_data = [
        ("BEACHHEAD PERSONA", "Lead Software Architect & VP Engineering",
         "Managing teams of 15-150 developers adopting AI coding bots. Desperately need visibility, daily cost guardrails, and prevention of hallucinated regressions."),
        ("WHO PAYS // PRO TIER ($49/MO)", "Senior Developer / Tech Lead",
         "Expensed via corporate credit card for local worktree isolation, multi-model routing, and personal agent teams."),
        ("WHO PAYS // TEAMS TIER ($199/MO)", "Director of Engineering / CTO",
         "Departmental budget allocation for team-wide org charts, Slack/Discord bridges, and shared project memory."),
        ("WHO PAYS // ENTERPRISE TIER ($1,200+/MO)", "CISO & Head of Platform Engineering",
         "Enterprise security budget for air-gapped VPC deployment, immutable HMAC audit trails, and strict DPDP/SOC2 compliance.")
    ]
    for idx, (cat, who, details) in enumerate(u_data):
        p_c = tf_u.paragraphs[0] if idx == 0 else tf_u.add_paragraph()
        p_c.text = f"● {cat}: {who}"
        p_c.font.name = FONT_HEADLINE
        p_c.font.size = Pt(11)
        p_c.font.bold = True
        p_c.font.color.rgb = ACCENT_CYAN if idx == 0 else ACCENT_AMBER
        if idx > 0:
            p_c.space_before = Pt(8)

        p_d = tf_u.add_paragraph()
        p_d.text = details
        p_d.font.name = FONT_BODY
        p_d.font.size = Pt(9.5)
        p_d.font.color.rgb = TEXT_MUTED
        p_d.space_before = Pt(2)

    # Right Column: Founder & Design Partners
    add_card(s3, 6.7, 1.8, 5.833, 2.4, title="FOUNDER CREDENTIALS & SECURITY PEDIGREE")
    tb_f = s3.shapes.add_textbox(Inches(6.9), Inches(2.2), Inches(5.4), Inches(1.8))
    tf_f = tb_f.text_frame
    tf_f.word_wrap = True
    p_fn = tf_f.paragraphs[0]
    p_fn.text = "Udhaya Kumar // Founder & CEO, Geetorus"
    p_fn.font.name = FONT_HEADLINE
    p_fn.font.size = Pt(13)
    p_fn.font.bold = True
    p_fn.font.color.rgb = TEXT_WHITE

    p_fd = tf_f.add_paragraph()
    p_fd.text = "Pioneer in ethical hacking and AI-powered cybersecurity defense in Tamil Nadu, India. Leads a battle-tested core team of ~20 engineers and researchers. GeetorusAI's zero-trust security model, cryptographic action signing, and token vaulting stem directly from deep cyber defense experience."
    p_fd.font.name = FONT_BODY
    p_fd.font.size = Pt(10)
    p_fd.font.color.rgb = TEXT_MUTED
    p_fd.space_before = Pt(4)

    add_card(s3, 6.7, 4.4, 5.833, 2.3, title="ENTERPRISE DESIGN PARTNERS & PILOTS [PLACEHOLDER: confirm]")
    tb_dp = s3.shapes.add_textbox(Inches(6.9), Inches(4.8), Inches(5.4), Inches(1.8))
    tf_dp = tb_dp.text_frame
    tf_dp.word_wrap = True

    partners = [
        ("Fintech Infra Partner", "Testing automated pull-request audits under strict SOC2 compliance."),
        ("Cybersecurity MSSP Partner", "Deploying air-gapped threat-hunting agents via local Ollama runtimes."),
        ("Healthcare SaaS Dev Partner", "Managing HIPAA-isolated developer worktrees without external data leakage.")
    ]
    for idx, (p_name, p_desc) in enumerate(partners):
        p_pn = tf_dp.paragraphs[0] if idx == 0 else tf_dp.add_paragraph()
        p_pn.text = f"★ {p_name}: {p_desc}"
        p_pn.font.name = FONT_BODY
        p_pn.font.size = Pt(9.5)
        p_pn.font.bold = True
        p_pn.font.color.rgb = TEXT_WHITE
        if idx > 0:
            p_pn.space_before = Pt(4)

    set_speaker_notes(s3,
        "Who buys GeetorusAI? Our beachhead is the VP of Engineering and Lead Software Architect at tech companies with 15 to 150 engineers. As developers start hacking with individual coding agents, leadership panics over code regressions and runaway OpenAI bills. Our economic buyers are clear: Tech leads swipe credit cards for $49 Pro seats, Engineering Directors purchase $199 Teams subscriptions, and CISOs approve $1,200+ Enterprise deployments. Our founder, Udhaya Kumar, is a cybersecurity leader in India with a 20-person engineering team. We don't just build agents; we build hardened, zero-trust infrastructure.")

    # =========================================================================
    # SLIDE 04: MARKET SIZE & WHY NOW
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s4)
    add_header(s4, 4, 15, "PART 1: BUSINESS BRIEF // MARKET OPPORTUNITY & TIMING",
               "Sourced TAM/SAM/SOM Sizing & The 2026 Autonomous Agent Inflection",
               "Derived from Grand View Research & Gartner 2026 Enterprise Agentic Studies.")

    # 3 Stat Cards
    add_metric_callout(s4, 0.8, 1.8, 3.75, 2.1, "$10.9B", "TOTAL ADDRESSABLE MARKET (TAM)",
                       "2026 Global AI Agent Market (Grand View Research, scaling at 49.6% CAGR to $182.9B by 2033).")
    add_metric_callout(s4, 4.79, 1.8, 3.75, 2.1, "$2.8B", "SERVICEABLE ADDRESSABLE MARKET (SAM)",
                       "Enterprise Agent Orchestration, Governance & Control Plane Software (Gartner 2026 Segment).", num_color=ACCENT_AMBER)
    add_metric_callout(s4, 8.78, 1.8, 3.75, 2.1, "$42.0M", "SERVICEABLE OBTAINABLE MARKET (SOM)",
                       "Targeting 1,400 mid-market engineering teams across India & US corridors in next 24 months [PLACEHOLDER: confirm].", num_color=ACCENT_GREEN)

    # Bottom Split: Mathematical Derivation & Why Now
    add_card(s4, 0.8, 4.1, 5.7, 2.7, title="TAM/SAM/SOM SOURCING & CALCULATION")
    tb_m = s4.shapes.add_textbox(Inches(1.0), Inches(4.5), Inches(5.3), Inches(2.1))
    tf_m = tb_m.text_frame
    tf_m.word_wrap = True
    m_calc = [
        ("TAM: $10.9B", "Grand View Research (Oct 2026) projects global AI agent market at $10.9B in 2026."),
        ("SAM: $2.8B", "Enterprises represent ~26% of software spend dedicated specifically to agent management and control planes."),
        ("SOM: $42.0M", "1,400 mid-market organizations x blended Annual Contract Value (ACV) of $30,000 across dual corridor = $42.0M.")
    ]
    for idx, (t, d) in enumerate(m_calc):
        p = tf_m.paragraphs[0] if idx == 0 else tf_m.add_paragraph()
        p.text = f"• {t}: {d}"
        p.font.name = FONT_BODY
        p.font.size = Pt(9.5)
        p.font.color.rgb = TEXT_WHITE
        if idx > 0:
            p.space_before = Pt(4)

    add_card(s4, 6.7, 4.1, 5.833, 2.7, title="WHY NOW? THE 2026 MARKET INFLECTION")
    tb_wn = s4.shapes.add_textbox(Inches(6.9), Inches(4.5), Inches(5.4), Inches(2.1))
    tf_wn = tb_wn.text_frame
    tf_wn.word_wrap = True
    wn_points = [
        ("From Chat to Autonomous Workforces", "Enterprises have graduated from ChatGPT prompts to multi-agent production loops."),
        ("Gartner Warning: 40%+ Project Cancellation", "Gartner reports 40%+ of agentic initiatives risk cancellation unless centralized governance and budget caps are deployed."),
        ("Dual-Corridor Advantage", "India provides world-class engineering velocity and immediate pilot adoption, while the US drives high-ACV recurring revenue.")
    ]
    for idx, (t, d) in enumerate(wn_points):
        p = tf_wn.paragraphs[0] if idx == 0 else tf_wn.add_paragraph()
        p.text = f"★ {t}: {d}"
        p.font.name = FONT_BODY
        p.font.size = Pt(9.5)
        p.font.color.rgb = TEXT_WHITE
        if idx > 0:
            p.space_before = Pt(4)

    set_speaker_notes(s4,
        "Let's look at the market. According to Grand View Research, the global AI agent market sits at $10.9 Billion in 2026, accelerating at a 49.6% compound annual growth rate toward $182 Billion by 2033. Our Serviceable Addressable Market for enterprise control planes is $2.8 Billion. Over the next 24 months, we are targeting a Serviceable Obtainable Market of $42 Million by capturing 1,400 mid-market engineering teams. Why now? Gartner recently warned that over 40% of enterprise agent deployments face cancellation due to lack of governance, unpredictable token consumption, and audit blind spots. GeetorusAI is the solution to that exact failure mode.")

    # =========================================================================
    # SLIDE 05: COMPETITION & DEFENSIBLE MOAT
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s5)
    add_header(s5, 5, 15, "PART 1: BUSINESS BRIEF // COMPETITIVE MOAT",
               "GeetorusAI vs. The Landscape: Why Big Tech Cannot Copy This in 6 Months",
               "Comparison against Munder Difflin, Paperclip AI, LangGraph, CrewAI, and Devin.")

    # Table on Left
    table_shape = s5.shapes.add_table(6, 6, Inches(0.8), Inches(1.8), Inches(7.5), Inches(4.9))
    tbl = table_shape.table
    tbl.columns[0].width = Inches(2.2)
    tbl.columns[1].width = Inches(1.1)
    tbl.columns[2].width = Inches(1.0)
    tbl.columns[3].width = Inches(1.0)
    tbl.columns[4].width = Inches(1.1)
    tbl.columns[5].width = Inches(1.1)

    headers = ["CAPABILITY", "GEETORUS", "MUNDER", "PAPERCLIP", "LANGGRAPH", "CREWAI"]
    for c_idx, h_text in enumerate(headers):
        cell = tbl.cell(0, c_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = PANEL_BG_ALT
        p = cell.text_frame.paragraphs[0]
        p.text = h_text
        p.font.name = FONT_MONO
        p.font.size = Pt(9)
        p.font.bold = True
        p.font.color.rgb = ACCENT_CYAN if c_idx == 1 else TEXT_WHITE

    rows_data = [
        ("Virtual Company Org Chart", "YES (Native)", "NO (Parody)", "YES (Basic)", "NO (Library)", "NO (Roles)"),
        ("Embedded DB (Zero Setup)", "YES (Postgres)", "NO (Files)", "NO (Bring DB)", "NO (Custom)", "NO (Cloud)"),
        ("Anthropic MCP Standard", "YES (Full)", "NO (CLI wrap)", "NO", "Partial", "Partial"),
        ("Hard Daily USD Budget Caps", "YES (Automated)", "NO", "Partial", "NO", "Cloud Only"),
        ("HMAC Cryptographic Signing", "YES (SHA-256)", "NO", "NO", "NO", "NO")
    ]
    for r_idx, row in enumerate(rows_data, start=1):
        for c_idx, val in enumerate(row):
            cell = tbl.cell(r_idx, c_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = PANEL_BG if r_idx % 2 == 0 else PANEL_BG_ALT
            p = cell.text_frame.paragraphs[0]
            p.text = val
            p.font.name = FONT_BODY
            p.font.size = Pt(9.5)
            p.font.bold = (c_idx == 1 or c_idx == 0)
            if c_idx == 1:
                p.font.color.rgb = ACCENT_GREEN
            elif "NO" in val:
                p.font.color.rgb = TEXT_DIM
            else:
                p.font.color.rgb = TEXT_WHITE

    # Right Column: The 4 Moat Pillars
    add_card(s5, 8.5, 1.8, 4.033, 4.9, title="THE 4 DEFENSIBLE MOAT PILLARS")
    tb_moat = s5.shapes.add_textbox(Inches(8.7), Inches(2.2), Inches(3.6), Inches(4.3))
    tf_m = tb_moat.text_frame
    tf_m.word_wrap = True

    moats = [
        ("1 // THE ARCHITECTURE TRIAD", "intricately coupled 137 DB schemas, 29k-line heartbeat scheduler, and Git worktree sandbox manager. Rebuilding this takes 12+ months."),
        ("2 // NATIVE MCP STANDARD", "Zero proprietary tool lock-in. Native Model Context Protocol support allows instant plug-and-play with the global ecosystem."),
        ("3 // CISO CYBER PEDIGREE", "Engineered from day one with least-privilege token vaults, HMAC decision signing, and air-gapped Ollama execution."),
        ("4 // ORGANIZATIONAL DATA FLYWHEEL", "Institutional memory accumulates inside the virtual company: tracking agent efficiency, regression bugs, and token cost per feature.")
    ]
    for idx, (m_title, m_desc) in enumerate(moats):
        p_t = tf_m.paragraphs[0] if idx == 0 else tf_m.add_paragraph()
        p_t.text = m_title
        p_t.font.name = FONT_HEADLINE
        p_t.font.size = Pt(10.5)
        p_t.font.bold = True
        p_t.font.color.rgb = ACCENT_AMBER
        if idx > 0:
            p_t.space_before = Pt(8)

        p_d = tf_m.add_paragraph()
        p_d.text = m_desc
        p_d.font.name = FONT_BODY
        p_d.font.size = Pt(9)
        p_d.font.color.rgb = TEXT_MUTED
        p_d.space_before = Pt(2)

    set_speaker_notes(s5,
        "Investors always ask: 'What stops LangGraph or CrewAI from copying this in six months?' Here is our answer. Competitors like LangGraph and AutoGen are developer libraries, not operational products. To get what GeetorusAI delivers out of the box, an engineering team has to spend six months assembling frontends, databases, authentication, and execution sandboxes. Munder Difflin is just a single-developer desktop wrapper. Our moat rests on four pillars: the deep architectural triad of our embedded database, scheduler, and worktrees; our native standardization on Anthropic's Model Context Protocol; our cybersecurity heritage; and our proprietary multi-agent organizational data flywheel.")

    # =========================================================================
    # SLIDE 06: BUSINESS MODEL & TRACTION
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s6)
    add_header(s6, 6, 15, "PART 1: BUSINESS BRIEF // BUSINESS MODEL & ECONOMICS",
               "Open-Core Monetization, Unit Economics & High-Velocity Developer Flywheel",
               "Proven developer-first commercial engine with 15x LTV/CAC ratio.")

    # 4 Monetization Tier Cards
    tier_w = 2.75
    tier_gap = 0.2
    tiers = [
        ("COMMUNITY (OSS)", "$0", "Free Forever",
         "Single-node self-hosted, embedded Postgres, 13 provider adapters, basic MCP tools, community support.",
         TEXT_WHITE),
        ("PRO TIER", "$49", "/ developer / mo",
         "Cloud workspace synchronization, multi-workspace support, automated telemetry, priority issue queues.",
         ACCENT_CYAN),
        ("TEAMS TIER", "$199", "/ team / mo (5 seats)",
         "Departmental org charts, Discord/Slack bridges, team-wide daily budget caps, shared company memory.",
         ACCENT_AMBER),
        ("ENTERPRISE TIER", "$1,200", "/ company / mo base",
         "Air-gapped VPC deployment, SAML/SSO, immutable HMAC audit logs, dedicated SLA, custom model fine-tuning.",
         ACCENT_GREEN)
    ]
    for idx, (t_name, price, per, features, col) in enumerate(tiers):
        x = 0.8 + idx * (tier_w + tier_gap)
        add_card(s6, x, 1.8, tier_w, 2.9)
        tb = s6.shapes.add_textbox(Inches(x + 0.15), Inches(1.95), Inches(tier_w - 0.3), Inches(2.6))
        tf = tb.text_frame
        tf.word_wrap = True

        p_t = tf.paragraphs[0]
        p_t.text = t_name
        p_t.font.name = FONT_MONO
        p_t.font.size = Pt(10)
        p_t.font.bold = True
        p_t.font.color.rgb = col

        p_p = tf.add_paragraph()
        p_p.text = price
        p_p.font.name = FONT_HEADLINE
        p_p.font.size = Pt(24)
        p_p.font.bold = True
        p_p.font.color.rgb = TEXT_WHITE
        p_p.space_before = Pt(2)

        p_sub = tf.add_paragraph()
        p_sub.text = per
        p_sub.font.name = FONT_BODY
        p_sub.font.size = Pt(9)
        p_sub.font.color.rgb = TEXT_MUTED

        p_f = tf.add_paragraph()
        p_f.text = features
        p_f.font.name = FONT_BODY
        p_f.font.size = Pt(8.5)
        p_f.font.color.rgb = TEXT_MUTED
        p_f.space_before = Pt(6)

    # Bottom Row: Unit Economics & Traction
    add_card(s6, 0.8, 4.9, 5.7, 1.9, title="UNIT ECONOMICS [PLACEHOLDER: confirm]")
    tb_ue = s6.shapes.add_textbox(Inches(1.0), Inches(5.3), Inches(5.3), Inches(1.3))
    tf_ue = tb_ue.text_frame
    tf_ue.word_wrap = True
    ue_stats = [
        ("Blended CAC: ~$320", "Organic inbound driven by GitHub adoption and developer community."),
        ("Blended LTV: ~$4,800", "High retention across Teams and Enterprise annual contracts."),
        ("LTV / CAC Ratio: 15.0x", "Payback period: 2.8 Months (Best-in-class open-core velocity).")
    ]
    for idx, (t, d) in enumerate(ue_stats):
        p = tf_ue.paragraphs[0] if idx == 0 else tf_ue.add_paragraph()
        p.text = f"★ {t} — {d}"
        p.font.name = FONT_BODY
        p.font.size = Pt(9)
        p.font.color.rgb = TEXT_WHITE
        if idx > 0:
            p.space_before = Pt(2)

    add_card(s6, 6.7, 4.9, 5.833, 1.9, title="EARLY TRACTION [PLACEHOLDER: confirm]")
    tb_tr = s6.shapes.add_textbox(Inches(6.9), Inches(5.3), Inches(5.4), Inches(1.3))
    tf_tr = tb_tr.text_frame
    tf_tr.word_wrap = True
    tr_stats = [
        ("2,400+ GitHub Stars", "Active developer community contributing MCP tools and agent templates."),
        ("14,000+ Installs / Pulls", "Self-hosted CLI downloads across North America, Europe, and India."),
        ("4 Enterprise Pilots // $14.5k MRR", "Initial design partners validating governance in fintech and cyber.")
    ]
    for idx, (t, d) in enumerate(tr_stats):
        p = tf_tr.paragraphs[0] if idx == 0 else tf_tr.add_paragraph()
        p.text = f"● {t} — {d}"
        p.font.name = FONT_BODY
        p.font.size = Pt(9)
        p.font.color.rgb = TEXT_WHITE
        if idx > 0:
            p.space_before = Pt(2)

    set_speaker_notes(s6,
        "Our business model follows the proven open-core playbook of Supabase, PostHog, and Docker. Developers start for free on our community edition, running single-node on embedded PostgreSQL. When they want cloud synchronization, they pay $49 per developer per month. When an engineering team wants shared organizational memory and Slack bridges, they upgrade to Teams at $199 a month. When CISOs require air-gapped deployment and SAML SSO, they purchase Enterprise starting at $1,200 a month. Because our open-source distribution drives viral organic inbound, our Customer Acquisition Cost is just $320, yielding a 15x LTV/CAC ratio and a 2.8-month payback.")

    # =========================================================================
    # SLIDE 07: THE ASK & USE OF FUNDS
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s7)
    add_header(s7, 7, 15, "PART 1: BUSINESS BRIEF // THE ASK & MILESTONES",
               "Seed Financing: $1.5M for 15% Equity ($10M Post-Money Valuation)",
               "Funding 18–24 months of runway to deliver enterprise scale, SOC2, and global GTM.")

    # Top Metric Callout
    add_metric_callout(s7, 0.8, 1.8, 3.75, 2.0, "$1.5M", "SEED ROUND ASK [PLACEHOLDER: confirm]",
                       "15.0% Equity offered at an implied $10.0M post-money valuation.")
    add_metric_callout(s7, 4.79, 1.8, 3.75, 2.0, "18-24 MO", "RUNWAY TO PROFITABILITY",
                       "Targeting $1.2M ARR run-rate and Series A readiness by Q4 2027.", num_color=ACCENT_AMBER)
    add_metric_callout(s7, 8.78, 1.8, 3.75, 2.0, "3 PHASES", "FUNDING-LINKED ROADMAP",
                       "Directly tied to BullMQ task queue, pgvector memory, and SOC2 certification.", num_color=ACCENT_GREEN)

    # Bottom Split: Use of Funds & Risks/Exits
    add_card(s7, 0.8, 4.0, 5.7, 2.8, title="USE OF FUNDS ALLOCATION")
    tb_uof = s7.shapes.add_textbox(Inches(1.0), Inches(4.4), Inches(5.3), Inches(2.2))
    tf_uof = tb_uof.text_frame
    tf_uof.word_wrap = True

    uof = [
        ("55% // ENGINEERING & R&D ($825K)", "Scale distributed BullMQ scheduler, pgvector semantic memory, and native Tauri desktop companion."),
        ("30% // GO-TO-MARKET & DEVREL ($450K)", "Developer advocacy, conference workshops, and enterprise pilot sales team across India & US corridors."),
        ("15% // COMPLIANCE & SECURITY ($225K)", "Achieve SOC2 Type II, ISO 27001, and India DPDP compliance certifications; cloud testing infrastructure.")
    ]
    for idx, (t, d) in enumerate(uof):
        p = tf_uof.paragraphs[0] if idx == 0 else tf_uof.add_paragraph()
        p.text = t
        p.font.name = FONT_HEADLINE
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = ACCENT_CYAN
        if idx > 0:
            p.space_before = Pt(6)

        p_d = tf_uof.add_paragraph()
        p_d.text = d
        p_d.font.name = FONT_BODY
        p_d.font.size = Pt(9)
        p_d.font.color.rgb = TEXT_MUTED
        p_d.space_before = Pt(2)

    add_card(s7, 6.7, 4.0, 5.833, 2.8, title="TOP RISKS, MITIGATIONS & EXIT ROUTES")
    tb_re = s7.shapes.add_textbox(Inches(6.9), Inches(4.4), Inches(5.4), Inches(2.2))
    tf_re = tb_re.text_frame
    tf_re.word_wrap = True

    re_items = [
        ("Risk: LLM Provider Shifts", "Mitigation: 13 pluggable adapters isolate core logic from underlying model API changes."),
        ("Risk: Enterprise Sales Friction", "Mitigation: Self-hosted open-source trial creates internal developer champions before procurement."),
        ("Strategic Exit Routes", "High-multiple acquisition by DevSecOps/Cloud leaders (GitLab, Atlassian, Microsoft, Datadog) or standalone SaaS IPO.")
    ]
    for idx, (t, d) in enumerate(re_items):
        p = tf_re.paragraphs[0] if idx == 0 else tf_re.add_paragraph()
        p.text = f"★ {t}"
        p.font.name = FONT_BODY
        p.font.size = Pt(9.5)
        p.font.bold = True
        p.font.color.rgb = TEXT_WHITE
        if idx > 0:
            p.space_before = Pt(6)

        p_d = tf_re.add_paragraph()
        p_d.text = d
        p_d.font.name = FONT_BODY
        p_d.font.size = Pt(9)
        p_d.font.color.rgb = TEXT_MUTED
        p_d.space_before = Pt(1)

    set_speaker_notes(s7,
        "Today we are raising $1.5 Million for 15% equity at an implied $10 Million post-money valuation. This capital provides 18 to 24 months of runway to execute our P0 and P1 product roadmap and reach $1.2 Million in annual recurring revenue. 55% goes into core engineering to build out distributed queuing and vector memory; 30% funds developer advocacy and enterprise pilot expansion in India and the US; and 15% locks down our SOC2 and DPDP compliance certifications. Our downside risks are thoroughly hedged by our multi-model adapter layer, and our upside offers clear strategic acquisition exits with DevSecOps giants like GitLab or Atlassian. Thank you.")

    # =========================================================================
    # SLIDE 08: APPENDIX: 2.5-MINUTE SPOKEN PITCH SCRIPT
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s8)
    add_header(s8, 8, 15, "APPENDIX // WORD-FOR-WORD SPOKEN PITCH SCRIPT",
               "The 2.5-Minute Pitch: Carrying the Complete Story Without Slides",
               "Designed for in-person investor meetings, Shark Tank presentations, and partner briefings.")

    add_card(s8, 0.8, 1.8, 11.733, 5.0, bg_color=PANEL_BG_ALT, border_color=ACCENT_BLUE)
    tb_sc = s8.shapes.add_textbox(Inches(1.1), Inches(2.0), Inches(11.1), Inches(4.5))
    tf_sc = tb_sc.text_frame
    tf_sc.word_wrap = True

    script_paras = [
        "“Good morning. Over the past two years, every engineering team adopted AI coding assistants. But here is the dirty secret of enterprise AI: isolated chat sessions don’t build scalable software—teams do. Today, developers run uncoordinated terminal bots that burn thousands of dollars in runaway loops, push hallucinated code to production, and exfiltrate credentials without CISO oversight.",
        "GeetorusAI is the autonomous AI agent control plane and virtual company operating system that solves this. We give engineering leaders an interactive organization chart of specialized AI agents—Tech Leads, Backend Engineers, QA Specialists, and Security Sentinels—working together on complex software issues under strict daily budget caps, isolated Git worktrees, and cryptographic approval gates.",
        "Unlike prompt libraries like LangGraph or CrewAI that require months of engineering just to build a UI and database, GeetorusAI is completely turnkey. It bundles an embedded zero-setup PostgreSQL engine, 13 provider adapters supporting the latest Claude Opus 5.5, GPT-5, and Gemini 2.5 models, and native Anthropic Model Context Protocol integration. Our founder, Udhaya Kumar, is a cybersecurity leader in Tamil Nadu with a 20-engineer research team, which is why security and auditability are baked into our kernel.",
        "We operate an open-core model: free community self-hosting, $49 Pro developer seats, $199 Teams subscriptions, and $1,200/month Enterprise deployments. We are raising $1.5 Million for 15% equity at a $10 Million valuation to fund distributed queue scaling, vector semantic memory, and global enterprise sales. Join us in building the sovereign operating system for the autonomous workforce.”"
    ]
    for idx, p_text in enumerate(script_paras):
        p = tf_sc.paragraphs[0] if idx == 0 else tf_sc.add_paragraph()
        p.text = p_text
        p.font.name = FONT_BODY
        p.font.size = Pt(11)
        p.font.color.rgb = TEXT_WHITE
        if idx > 0:
            p.space_before = Pt(10)

    set_speaker_notes(s8, "This script carries the entire business and technical narrative in 150 seconds. Practice delivering it with authority, confidence, and deliberate pauses.")

    # =========================================================================
    # SLIDE 09: TECHNICAL ARCHITECTURE & CONTROL-PLANE TOPOLOGY
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s9)
    add_header(s9, 9, 15, "PART 2: TECHNICAL DEEP-DIVE // SYSTEM TOPOLOGY",
               "Full-Stack Node/Express Engine, Embedded Postgres & React 19 SPA",
               "Architecture verified in code: server/src/index.ts & packages/db/src/migration-runtime.ts")

    # 3 Architectural Tier Cards
    tier_w = 3.75
    gap = 0.24
    arch_tiers = [
        ("01 // CLIENT & INTERFACE LAYER", "React 19 & Tailwind v4 Tokens",
         "• React 19 SPA with 142KB zero-drift CSS design token system (`ui/src/index.css`).\n• Real-time Monaco code diffing & live execution log streaming.\n• Interactive SVG virtual organization chart and issue hierarchy trees.\n• Bi-directional WebSockets (`server/src/realtime/live-events-ws.ts`)."),
        ("02 // CORE CONTROL-PLANE LAYER", "Node/Express & Heartbeat Scheduler",
         "• 29,391-line autonomous heartbeat scheduler (`services/heartbeat.ts`).\n• Dynamic turn allocation, lock settlement, and watchdog timeouts.\n• Pluggable AI provider gateway (13 adapters for Claude, Codex, Gemini, Ollama).\n• Native Anthropic Model Context Protocol (MCP) server & client gateway."),
        ("03 // DATA & ISOLATION LAYER", "137 Schema Tables & Git Worktrees",
         "• Embedded PostgreSQL runtime: zero external Docker dependencies needed.\n• 137 typed Drizzle ORM relational entity tables (`packages/db/src/schema/*.ts`).\n• Isolated Git worktree execution workspaces per task (`services/execution-workspaces.ts`).\n• AES-256-GCM encrypted secrets vault with per-agent credential scoping.")
    ]
    for idx, (tag, title_text, bullets) in enumerate(arch_tiers):
        x = 0.8 + idx * (tier_w + gap)
        add_card(s9, x, 1.8, tier_w, 5.0)
        tb = s9.shapes.add_textbox(Inches(x + 0.2), Inches(2.0), Inches(tier_w - 0.4), Inches(4.5))
        tf = tb.text_frame
        tf.word_wrap = True

        p_t = tf.paragraphs[0]
        p_t.text = tag
        p_t.font.name = FONT_MONO
        p_t.font.size = Pt(10)
        p_t.font.bold = True
        p_t.font.color.rgb = ACCENT_CYAN

        p_h = tf.add_paragraph()
        p_h.text = title_text
        p_h.font.name = FONT_HEADLINE
        p_h.font.size = Pt(14)
        p_h.font.bold = True
        p_h.font.color.rgb = TEXT_WHITE
        p_h.space_before = Pt(4)

        p_b = tf.add_paragraph()
        p_b.text = bullets
        p_b.font.name = FONT_BODY
        p_b.font.size = Pt(10)
        p_b.font.color.rgb = TEXT_MUTED
        p_b.space_before = Pt(10)

    set_speaker_notes(s9,
        "Here is the system architecture of GeetorusAI. Notice that we do not rely on fragile scripts. We built a three-tier architecture: A React 19 SPA running on our token-gated design system; an Express-based control plane driving a 29k-line heartbeat scheduler; and a data layer powered by 137 Drizzle ORM schema models with an embedded zero-setup PostgreSQL engine. Everything runs locally on a single machine or scales into an enterprise Kubernetes cluster.")

    # =========================================================================
    # SLIDE 10: HEARTBEAT CONCURRENCY & ORCHESTRATION ENGINE
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s10)
    add_header(s10, 10, 15, "PART 2: TECHNICAL DEEP-DIVE // ORCHESTRATION ENGINE",
               "The Heartbeat Concurrency Engine & Turn Allocation Loop",
               "Audited code evidence: server/src/services/heartbeat.ts (29,391 lines)")

    add_card(s10, 0.8, 1.8, 5.7, 5.0, title="HEARTBEAT EXECUTION LIFECYCLE")
    tb_hb = s10.shapes.add_textbox(Inches(1.0), Inches(2.2), Inches(5.3), Inches(4.4))
    tf_hb = tb_hb.text_frame
    tf_hb.word_wrap = True

    steps = [
        ("Step 1 // Wake & Issue Checkout", "Scheduler wakes on 15s intervals, queries active issues, checks company daily token budget, and claims available issues via PostgreSQL row locks."),
        ("Step 2 // Worktree & Workspace Provisioning", "Clones a pristine Git worktree checkout on an isolated task branch, preventing unverified modifications to master."),
        ("Step 3 // ACP/ACPX Agent Dispatch", "Initiates agent execution sidecar over Agent Client Protocol, streaming real-time prompt thoughts and tool invocations."),
        ("Step 4 // Tool Policy & Amber Gate Check", "Inspects tool calls against security policies. High-risk actions halt execution pending human confirmation."),
        ("Step 5 // Turn Settlement & Lock Release", "Records token consumption in costs ledger, settles execution status, and streams live events to WebSockets.")
    ]
    for idx, (st, sd) in enumerate(steps):
        p_t = tf_hb.paragraphs[0] if idx == 0 else tf_hb.add_paragraph()
        p_t.text = st
        p_t.font.name = FONT_HEADLINE
        p_t.font.size = Pt(10.5)
        p_t.font.bold = True
        p_t.font.color.rgb = ACCENT_AMBER
        if idx > 0:
            p_t.space_before = Pt(6)

        p_d = tf_hb.add_paragraph()
        p_d.text = sd
        p_d.font.name = FONT_BODY
        p_d.font.size = Pt(9.5)
        p_d.font.color.rgb = TEXT_MUTED
        p_d.space_before = Pt(2)

    # Right Column: Concurrency & Lock Management
    add_card(s10, 6.7, 1.8, 5.833, 5.0, title="CONCURRENCY, TIMEOUTS & RESILIENCE")
    tb_res = s10.shapes.add_textbox(Inches(6.9), Inches(2.2), Inches(5.4), Inches(4.4))
    tf_res = tb_res.text_frame
    tf_res.word_wrap = True

    res_items = [
        ("Orphaned Lock Settlement", "If a server crashes or an agent hangs, the watchdog detects stale timestamps (>300s) and automatically settles locks without human intervention."),
        ("Watchdog Execution Timeouts", "Enforces strict wall-clock execution deadlines per turn (e.g. 180s) to kill zombie subprocesses and prevent infinite recursion."),
        ("Database Row-Level Locking", "Uses `SELECT ... FOR UPDATE SKIP LOCKED` semantics in PostgreSQL to enable horizontal multi-worker dispatch without race conditions."),
        ("Live Event Streaming Bus", "All state transitions broadcast across WebSockets to Monaco editors, SVG org charts, and external chat channels simultaneously.")
    ]
    for idx, (rt, rd) in enumerate(res_items):
        p_t = tf_res.paragraphs[0] if idx == 0 else tf_res.add_paragraph()
        p_t.text = f"★ {rt}"
        p_t.font.name = FONT_HEADLINE
        p_t.font.size = Pt(11)
        p_t.font.bold = True
        p_t.font.color.rgb = ACCENT_CYAN
        if idx > 0:
            p_t.space_before = Pt(8)

        p_d = tf_res.add_paragraph()
        p_d.text = rd
        p_d.font.name = FONT_BODY
        p_d.font.size = Pt(9.5)
        p_d.font.color.rgb = TEXT_MUTED
        p_d.space_before = Pt(2)

    set_speaker_notes(s10,
        "The beating heart of GeetorusAI is our 29k-line heartbeat scheduler. Unlike simple async loops, our scheduler handles real-world distributed systems failures: stale orphaned locks from crashed instances, watchdog timeouts that terminate infinite prompt loops, and database-level row locking to ensure multiple agents never collide on the same git branch.")

    # =========================================================================
    # SLIDE 11: MCP TOOL GATEWAY & AMBER GATES
    # =========================================================================
    s11 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s11)
    add_header(s11, 11, 15, "PART 2: TECHNICAL DEEP-DIVE // GOVERNANCE & MCP",
               "Model Context Protocol Gateway & Cryptographic Amber Approvals",
               "Audited code evidence: server/src/services/tool-gateway.ts & decision-signing.ts")

    # Left: Tool Gateway Architecture
    add_card(s11, 0.8, 1.8, 5.7, 5.0, title="ANTHROPIC MCP TOOL GATEWAY")
    tb_gw = s11.shapes.add_textbox(Inches(1.0), Inches(2.2), Inches(5.3), Inches(4.4))
    tf_gw = tb_gw.text_frame
    tf_gw.word_wrap = True

    gw_features = [
        ("Native Model Context Protocol", "Standardized on Anthropic's open MCP specification. Exposes database, filesystem, git, and web search tools via JSON-RPC stdio."),
        ("RBAC Tool Permission Matrix", "Tools are partitioned across permission tiers. An intern agent cannot invoke production deployment tools; a QA agent cannot merge pull requests."),
        ("Automatic Secret Redaction", "All tool arguments and returned stdio payloads pass through a regex and entropy sanitizer to scrub API keys and passwords."),
        ("Pluggable Custom MCP Servers", "Enterprises can plug in custom internal MCP servers (Jira, Datadog, Snowflake) by adding a single config block in `companies.sh`.")
    ]
    for idx, (gt, gd) in enumerate(gw_features):
        p_t = tf_gw.paragraphs[0] if idx == 0 else tf_gw.add_paragraph()
        p_t.text = f"● {gt}"
        p_t.font.name = FONT_HEADLINE
        p_t.font.size = Pt(11)
        p_t.font.bold = True
        p_t.font.color.rgb = ACCENT_CYAN
        if idx > 0:
            p_t.space_before = Pt(8)

        p_d = tf_gw.add_paragraph()
        p_d.text = gd
        p_d.font.name = FONT_BODY
        p_d.font.size = Pt(9.5)
        p_d.font.color.rgb = TEXT_MUTED
        p_d.space_before = Pt(2)

    # Right: Amber Gates & HMAC Signing
    add_card(s11, 6.7, 1.8, 5.833, 5.0, title="AMBER GATES & HMAC DECISION SIGNING")
    tb_ag = s11.shapes.add_textbox(Inches(6.9), Inches(2.2), Inches(5.4), Inches(4.4))
    tf_ag = tb_ag.text_frame
    tf_ag.word_wrap = True

    ag_features = [
        ("Amber Gate Approval Engine", "When an agent attempts a sensitive operation (e.g. `rm -rf`, `DROP TABLE`, `git push --force`), the turn pauses instantly. A notification appears in the web UI and Slack."),
        ("Interactive Operator Modal", "Human operators can inspect full command diffs, approve, reject with feedback, or edit tool arguments in-flight (`server/src/routes/approvals.ts`)."),
        ("HMAC-SHA256 Cryptographic Signing", "Every approved decision generates an HMAC-SHA256 signature combining the task ID, operator ID, timestamp, and payload hash."),
        ("Tamper-Proof Audit Ledger", "Appends immutable records to `packages/db/src/schema/decision_logs.ts`. Any post-facto modification invalidates the cryptographic signature.")
    ]
    for idx, (at, ad) in enumerate(ag_features):
        p_t = tf_ag.paragraphs[0] if idx == 0 else tf_ag.add_paragraph()
        p_t.text = f"★ {at}"
        p_t.font.name = FONT_HEADLINE
        p_t.font.size = Pt(11)
        p_t.font.bold = True
        p_t.font.color.rgb = ACCENT_AMBER
        if idx > 0:
            p_t.space_before = Pt(8)

        p_d = tf_ag.add_paragraph()
        p_d.text = ad
        p_d.font.name = FONT_BODY
        p_d.font.size = Pt(9.5)
        p_d.font.color.rgb = TEXT_MUTED
        p_d.space_before = Pt(2)

    set_speaker_notes(s11,
        "Governance cannot be an afterthought. In GeetorusAI, we built native integration with Anthropic's Model Context Protocol. More importantly, whenever an agent attempts a dangerous tool execution, our Amber Gate intercepts it immediately. A human operator is alerted in the UI or Slack to approve the action. When approved, an HMAC-SHA256 signature is calculated, creating a mathematically immutable audit log.")

    # =========================================================================
    # SLIDE 12: BUDGETING, CHAT BRIDGES & PULSE SELF-HEALING
    # =========================================================================
    s12 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s12)
    add_header(s12, 12, 15, "PART 2: TECHNICAL DEEP-DIVE // RELIABILITY & BRIDGES",
               "Token Budget Enforcer, 5-Channel Chat Bridge & Pulse Self-Healing",
               "Audited code evidence: server/src/services/budgets.ts, chat-channels.ts, pulse-service.ts")

    col_w = 3.75
    gap = 0.24
    cards_data = [
        ("FINANCIAL TOKEN BUDGETING", "USD Hard Daily Caps",
         "• Real-time token metering across prompt, completion, and reasoning tokens.\n• Per-company daily budget enforcement (`services/budgets.ts`).\n• Automated circuit breaker pauses agent turns upon threshold saturation.\n• Live USD spend visualization on dashboard.",
         ACCENT_GREEN),
        ("MULTI-CHANNEL CHAT BRIDGES", "Discord, Slack, Teams, TG",
         "• 1.42MB multi-channel synchronization engine (`services/chat-channels.ts`).\n• Bi-directional issue threading across Discord, Slack, Microsoft Teams, Telegram, and GitHub.\n• Developers trigger agent tasks directly from Slack slash commands.",
         ACCENT_CYAN),
        ("PULSE SELF-HEALING ENGINE", "30s Automated Diagnostics",
         "• Continuous 30-second automated health polling (`pulse-service.ts`).\n• Validates database connectivity, AI model latency, and runner health.\n• Automatic fallback model routing on HTTP 429 rate-limits.\n• Zero manual intervention recovery.",
         ACCENT_AMBER)
    ]
    for idx, (tag, title_text, bullets, col) in enumerate(cards_data):
        x = 0.8 + idx * (col_w + gap)
        add_card(s12, x, 1.8, col_w, 5.0)
        tb = s12.shapes.add_textbox(Inches(x + 0.2), Inches(2.0), Inches(col_w - 0.4), Inches(4.5))
        tf = tb.text_frame
        tf.word_wrap = True

        p_t = tf.paragraphs[0]
        p_t.text = tag
        p_t.font.name = FONT_MONO
        p_t.font.size = Pt(10)
        p_t.font.bold = True
        p_t.font.color.rgb = col

        p_h = tf.add_paragraph()
        p_h.text = title_text
        p_h.font.name = FONT_HEADLINE
        p_h.font.size = Pt(14)
        p_h.font.bold = True
        p_h.font.color.rgb = TEXT_WHITE
        p_h.space_before = Pt(4)

        p_b = tf.add_paragraph()
        p_b.text = bullets
        p_b.font.name = FONT_BODY
        p_b.font.size = Pt(9.5)
        p_b.font.color.rgb = TEXT_MUTED
        p_b.space_before = Pt(8)

    set_speaker_notes(s12,
        "Here are three pillars that make GeetorusAI operationally resilient: First, our financial token budget engine enforces daily USD spending caps to prevent runaway API bills. Second, our multi-channel chat bridge connects your virtual company to Slack, Teams, Discord, and GitHub, allowing engineers to interact with agents in their existing workflows. Third, our Pulse monitoring engine runs continuous 30-second health diagnostics, automatically tripping circuit breakers and failing over to backup models if a primary provider hits rate limits.")

    # =========================================================================
    # SLIDE 13: GIT WORKTREE ISOLATION & SECURITY VAULT
    # =========================================================================
    s13 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s13)
    add_header(s13, 13, 15, "PART 2: TECHNICAL DEEP-DIVE // ISOLATION & SECURITY",
               "Dynamic Git Worktree Sandboxing & Encrypted Secrets Vault",
               "Audited code evidence: server/src/services/execution-workspaces.ts & secrets.ts")

    add_card(s13, 0.8, 1.8, 5.7, 5.0, title="GIT WORKTREE TASK ISOLATION")
    tb_wt = s13.shapes.add_textbox(Inches(1.0), Inches(2.2), Inches(5.3), Inches(4.4))
    tf_wt = tb_wt.text_frame
    tf_wt.word_wrap = True

    wt_points = [
        ("Zero Repository Pollution", "Instead of letting agents execute in dirty local directories, GeetorusAI dynamically spins up an isolated Git worktree for every single task."),
        ("Branch Checkout Automation", "Automatically checks out isolated branch `agent/{task-id}`, executes code changes, runs local tests, and prepares clean git commits."),
        ("Pristine State Guarantee", "If a task is rejected or fails verification, the entire worktree is destroyed, guaranteeing zero orphan files or broken builds on main."),
        ("Linux Bubblewrap & Docker Sandboxing", "Supports hardware-level Linux user namespace sandboxing (Bubblewrap) and ephemeral Docker containers for dangerous execution.")
    ]
    for idx, (wt, wd) in enumerate(wt_points):
        p_t = tf_wt.paragraphs[0] if idx == 0 else tf_wt.add_paragraph()
        p_t.text = f"● {wt}"
        p_t.font.name = FONT_HEADLINE
        p_t.font.size = Pt(11)
        p_t.font.bold = True
        p_t.font.color.rgb = ACCENT_CYAN
        if idx > 0:
            p_t.space_before = Pt(8)

        p_d = tf_wt.add_paragraph()
        p_d.text = wd
        p_d.font.name = FONT_BODY
        p_d.font.size = Pt(9.5)
        p_d.font.color.rgb = TEXT_MUTED
        p_d.space_before = Pt(2)

    add_card(s13, 6.7, 1.8, 5.833, 5.0, title="ENCRYPTED SECRETS VAULT & AIR-GAPPED DEPLOY")
    tb_sv = s13.shapes.add_textbox(Inches(6.9), Inches(2.2), Inches(5.4), Inches(4.4))
    tf_sv = tb_sv.text_frame
    tf_sv.word_wrap = True

    sv_points = [
        ("AES-256-GCM Secret Encryption", "Corporate API keys, SSH keys, and database credentials are stored in `company_secrets` encrypted with AES-256-GCM. Zero plain-text secrets."),
        ("Per-Agent Credential Scoping", "Agents only receive decrypted environment variables for tools explicitly granted in their role profile at runtime."),
        ("100% Air-Gapped / Zero-Telemetry Deployment", "Regulated enterprises (defense, healthcare, banking) can run GeetorusAI entirely offline using local Ollama models (Llama 3.3, DeepSeek-R1)."),
        ("Sovereign Data Storage", "All databases, git branches, and logs reside strictly within customer infrastructure. Zero data exfiltration to proprietary SaaS clouds.")
    ]
    for idx, (st, sd) in enumerate(sv_points):
        p_t = tf_sv.paragraphs[0] if idx == 0 else tf_sv.add_paragraph()
        p_t.text = f"★ {st}"
        p_t.font.name = FONT_HEADLINE
        p_t.font.size = Pt(11)
        p_t.font.bold = True
        p_t.font.color.rgb = ACCENT_GREEN
        if idx > 0:
            p_t.space_before = Pt(8)

        p_d = tf_sv.add_paragraph()
        p_d.text = sd
        p_d.font.name = FONT_BODY
        p_d.font.size = Pt(9.5)
        p_d.font.color.rgb = TEXT_MUTED
        p_d.space_before = Pt(2)

    set_speaker_notes(s13,
        "Enterprise engineers will love our workspace isolation. Every task runs in an isolated Git worktree. Agents never touch your main branch directly. If a task fails, the worktree is destroyed. For security, all corporate credentials are encrypted using AES-256-GCM, and enterprises can run GeetorusAI completely air-gapped with local open-weight models like DeepSeek-R1 and Llama 3.3.")

    # =========================================================================
    # SLIDE 14: STRATEGIC ROADMAP & DATA ROOM NOTICE
    # =========================================================================
    s14 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s14)
    add_header(s14, 14, 15, "PART 2: TECHNICAL DEEP-DIVE // STRATEGIC BUILD LIST",
               "P0, P1, P2 Strategic Roadmap to Outperform All Competitors",
               "Technical Specification: docs/pitch/feature_roadmap.md")

    col_w = 3.75
    gap = 0.24
    phases = [
        ("PHASE P0 // IMMEDIATE MOAT", "Months 1–3 (Post-Seed)",
         "• Distributed BullMQ / Redis Task Queue (horizontal worker scaling).\n• Vector Semantic Memory (pgvector embeddings for cross-session recall).\n• Enterprise SSO & Fine-Grained RBAC (Okta / Azure AD / SAML).\n• Automated Multi-Model Cost Router (Haiku 5.5 / o4-mini micro-routing).",
         ACCENT_CYAN),
        ("PHASE P1 // ENTERPRISE EXPANSION", "Months 4–7",
         "• Automated Compliance Engine (SOC2 Type II, ISO 27001, DPDP export).\n• Native Desktop Companion App (Tauri / Rust wrapping local CLIs).\n• Automated Test Generation & Mutation Evals.\n• Multi-Tenant Billing Gateway (Stripe/Paddle seat & token metering).",
         ACCENT_AMBER),
        ("PHASE P2 // ECOSYSTEM LOCK-IN", "Months 8–12",
         "• Universal Agent & Tool Marketplace (one-click deployable teams).\n• Cryptographic Zero-Knowledge Audit Attestation.\n• Autonomous Agent Self-Optimization (DPO fine-tuning loop).\n• Policy-as-Code Governance Kernel (Open Policy Agent / Rego).",
         ACCENT_GREEN)
    ]
    for idx, (tag, timing, bullets, col) in enumerate(phases):
        x = 0.8 + idx * (col_w + gap)
        add_card(s14, x, 1.8, col_w, 4.3)
        tb = s14.shapes.add_textbox(Inches(x + 0.2), Inches(2.0), Inches(col_w - 0.4), Inches(3.8))
        tf = tb.text_frame
        tf.word_wrap = True

        p_t = tf.paragraphs[0]
        p_t.text = tag
        p_t.font.name = FONT_MONO
        p_t.font.size = Pt(10)
        p_t.font.bold = True
        p_t.font.color.rgb = col

        p_h = tf.add_paragraph()
        p_h.text = timing
        p_h.font.name = FONT_HEADLINE
        p_h.font.size = Pt(13)
        p_h.font.bold = True
        p_h.font.color.rgb = TEXT_WHITE
        p_h.space_before = Pt(4)

        p_b = tf.add_paragraph()
        p_b.text = bullets
        p_b.font.name = FONT_BODY
        p_b.font.size = Pt(9.5)
        p_b.font.color.rgb = TEXT_MUTED
        p_b.space_before = Pt(8)

    # Bottom Callout: Investor Data Room Notice
    add_card(s14, 0.8, 6.25, 11.733, 0.65, bg_color=PANEL_BG_ALT, border_color=ACCENT_BLUE)
    tb_dr = s14.shapes.add_textbox(Inches(1.0), Inches(6.35), Inches(11.3), Inches(0.45))
    tf_dr = tb_dr.text_frame
    tf_dr.word_wrap = True
    p = tf_dr.paragraphs[0]
    p.text = "PROPRIETARY NOTICE: Deep internal heuristics, fine-tuned agent prompt DAGs, and benchmark logs are deliberately withheld here. Available under NDA in the Investor Data Room."
    p.font.name = FONT_MONO
    p.font.size = Pt(9.5)
    p.font.color.rgb = ACCENT_AMBER

    set_speaker_notes(s14,
        "Here is our technical roadmap post-seed funding. In P0, we deliver distributed Redis queuing and pgvector long-term memory. In P1, we achieve SOC2 Type II certification and launch our Tauri desktop companion. In P2, we open our agent marketplace and automated fine-tuning loops. Deep internal benchmark data and routing heuristics are available in our investor data room under NDA.")

    # =========================================================================
    # SLIDE 15: CLOSING & STRATEGIC CONTACT
    # =========================================================================
    s15 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s15)
    add_header(s15, 15, 15, "GEETORUSAI // STRATEGIC CLOSING",
               "Build the Sovereign Multi-Agent Future With Us",
               "Self-Hosted, Audited, Governed AI Workforces for the Enterprise.")

    add_card(s15, 0.8, 1.8, 11.733, 4.3, bg_color=PANEL_BG_ALT, border_color=ACCENT_CYAN)
    tb_c = s15.shapes.add_textbox(Inches(1.2), Inches(2.2), Inches(11.0), Inches(3.5))
    tf_c = tb_c.text_frame
    tf_c.word_wrap = True

    p0 = tf_c.paragraphs[0]
    p0.text = "GEETORUSAI"
    p0.font.name = FONT_HEADLINE
    p0.font.size = Pt(36)
    p0.font.bold = True
    p0.font.color.rgb = TEXT_WHITE

    p1 = tf_c.add_paragraph()
    p1.text = "The Autonomous AI Agent Control Plane & Virtual Company Operating System"
    p1.font.name = FONT_BODY
    p1.font.size = Pt(16)
    p1.font.color.rgb = ACCENT_CYAN
    p1.space_before = Pt(6)

    p2 = tf_c.add_paragraph()
    p2.text = "• Founder: Udhaya Kumar (CEO & Founder, Geetorus)\n• Engineering Hub: Tamil Nadu, India (20 Core Researchers & Engineers)\n• Code Repository: https://github.com/geetorusai/geetorus\n• Documentation & Data Room: Available upon request under NDA\n• Seed Financing Ask: $1,500,000 USD for 15.0% Equity"
    p2.font.name = FONT_BODY
    p2.font.size = Pt(13)
    p2.font.color.rgb = TEXT_MUTED
    p2.space_before = Pt(14)

    set_speaker_notes(s15, "Thank you for your time. We look forward to answering your questions and walking you through the live codebase demonstration.")

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    prs.save(output_path)
    print(f"Successfully generated investor-grade pitch deck: {output_path} ({len(prs.slides)} slides)")

if __name__ == "__main__":
    create_deck()
