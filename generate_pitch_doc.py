import os
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def set_cell_background(cell, fill_hex):
    shading_elm = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    cell._tc.get_or_add_tcPr().append(shading_elm)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

def create_document(output_path="c:/Users/mohamed farhan/testing-marketing/docs/pitch/GeetorusAI_Pitch_Document.docx"):
    doc = Document()

    # Set Margins
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)

    # Styles & Colors
    # Primary Cobalt: #1E3A8A, Accent Cyan: #0284C7, Dark Charcoal: #0F172A, Slate: #475569
    COLOR_PRIMARY = RGBColor(30, 58, 138)
    COLOR_ACCENT  = RGBColor(2, 132, 199)
    COLOR_BODY    = RGBColor(15, 23, 42)
    COLOR_MUTED   = RGBColor(71, 85, 105)

    def add_title(text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run(text)
        run.font.name = "Trebuchet MS"
        run.font.size = Pt(28)
        run.font.bold = True
        run.font.color.rgb = COLOR_PRIMARY
        p.paragraph_format.space_after = Pt(4)
        return p

    def add_subtitle(text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run(text)
        run.font.name = "Segoe UI"
        run.font.size = Pt(13)
        run.font.color.rgb = COLOR_ACCENT
        run.font.bold = True
        p.paragraph_format.space_after = Pt(24)
        return p

    def add_h1(text):
        p = doc.add_paragraph()
        run = p.add_run(text)
        run.font.name = "Trebuchet MS"
        run.font.size = Pt(18)
        run.font.bold = True
        run.font.color.rgb = COLOR_PRIMARY
        p.paragraph_format.space_before = Pt(18)
        p.paragraph_format.space_after = Pt(8)
        return p

    def add_h2(text):
        p = doc.add_paragraph()
        run = p.add_run(text)
        run.font.name = "Segoe UI"
        run.font.size = Pt(13)
        run.font.bold = True
        run.font.color.rgb = COLOR_ACCENT
        p.paragraph_format.space_before = Pt(12)
        p.paragraph_format.space_after = Pt(4)
        return p

    def add_h3(text):
        p = doc.add_paragraph()
        run = p.add_run(text)
        run.font.name = "Segoe UI"
        run.font.size = Pt(11)
        run.font.bold = True
        run.font.color.rgb = COLOR_PRIMARY
        p.paragraph_format.space_before = Pt(8)
        p.paragraph_format.space_after = Pt(2)
        return p

    def add_p(text, bold_prefix=None, space_after=6):
        p = doc.add_paragraph()
        if bold_prefix:
            r_pre = p.add_run(bold_prefix)
            r_pre.font.name = "Segoe UI"
            r_pre.font.size = Pt(10)
            r_pre.font.bold = True
            r_pre.font.color.rgb = COLOR_BODY
        run = p.add_run(text)
        run.font.name = "Segoe UI"
        run.font.size = Pt(10)
        run.font.color.rgb = COLOR_BODY
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.line_spacing = 1.15
        return p

    def add_bullet(text, bold_prefix=None):
        p = doc.add_paragraph(style='List Bullet')
        if bold_prefix:
            r_pre = p.add_run(bold_prefix)
            r_pre.font.name = "Segoe UI"
            r_pre.font.size = Pt(10)
            r_pre.font.bold = True
            r_pre.font.color.rgb = COLOR_BODY
        run = p.add_run(text)
        run.font.name = "Segoe UI"
        run.font.size = Pt(10)
        run.font.color.rgb = COLOR_BODY
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.line_spacing = 1.15
        return p

    def add_callout(text, title="KEY STRATEGIC TAKEAWAY", bg_hex="F1F5F9", border_hex="2563EB"):
        tbl = doc.add_table(rows=1, cols=1)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        cell = tbl.cell(0, 0)
        set_cell_background(cell, bg_hex)
        set_cell_margins(cell, top=140, bottom=140, left=200, right=200)

        # left border styling
        tcPr = cell._tc.get_or_add_tcPr()
        borders = parse_xml(f'<w:tcBorders {nsdecls("w")}><w:left w:val="single" w:sz="24" w:space="0" w:color="{border_hex}"/><w:top w:val="none"/><w:right w:val="none"/><w:bottom w:val="none"/></w:tcBorders>')
        tcPr.append(borders)

        p = cell.paragraphs[0]
        r_t = p.add_run(f"[{title}]\n")
        r_t.font.name = "Consolas"
        r_t.font.size = Pt(9.5)
        r_t.font.bold = True
        r_t.font.color.rgb = COLOR_PRIMARY

        r_body = p.add_run(text)
        r_body.font.name = "Segoe UI"
        r_body.font.size = Pt(10)
        r_body.font.color.rgb = COLOR_BODY
        p.paragraph_format.space_after = Pt(4)
        doc.add_paragraph().paragraph_format.space_after = Pt(6)

    # =========================================================================
    # COVER / HEADER
    # =========================================================================
    add_title("GEETORUSAI // STRATEGIC BRIEF & SPECIFICATION")
    add_subtitle("The Autonomous AI Agent Control Plane & Virtual Company Operating System\nConfidential Investor & Architectural Brief — 2026 Edition")

    add_callout(
        "GeetorusAI is the sovereign, self-hostable operating system that coordinates specialized multi-agent engineering teams (Tech Lead, Backend Engineer, QA Specialist, Security Sentinel) under strict daily token budget caps, isolated Git worktrees, and cryptographic HMAC approval gates.\n\n"
        "• Founder: Udhaya Kumar (CEO & Founder, Geetorus — Cybersecurity Pioneer, Tamil Nadu, India)\n"
        "• Engineering Depth: 16 Fully Verified Production Subsystems (29k-line Scheduler, 137 DB Schemas, 13 Adapters)\n"
        "• Financing Round: $1,500,000 USD Seed Round for 15.0% Equity ($10M Post-Money Valuation) [PLACEHOLDER: confirm]",
        title="EXECUTIVE OVERVIEW // COMMERCIAL & TECHNICAL SYNOPSIS"
    )

    doc.add_page_break()

    # =========================================================================
    # PART 1: BUSINESS SIDE (7 CORE SECTIONS)
    # =========================================================================
    add_h1("PART 1: THE BUSINESS SIDE (7-PAGE EXECUTIVE DOSSIER)")

    # -------------------------------------------------------------------------
    # Page 1: What It Is + The Problem
    # -------------------------------------------------------------------------
    add_h2("Section 1: What It Is & The Core Crisis")
    add_p(
        "“GeetorusAI is the sovereign, self-hosted operating system that turns isolated AI coding agents into a governed, collaborative digital workforce with strict budget caps and verifiable outcomes.”",
        bold_prefix="The Spoken Definition: "
    )
    add_p(
        "Over the past 24 months, the software development industry experienced an explosive influx of generative AI models and terminal coding bots (Claude Code, Cursor, GitHub Copilot). While these individual assistants accelerate single developers, they fail completely when deployed at team or enterprise scale. Autonomous engineering workflows face three critical bottlenecks:"
    )
    add_bullet(
        "Developers run disconnected coding bots in isolated terminal tabs. There is no shared architectural memory, no organizational hierarchy, no cross-agent task handoff, and zero visibility for engineering management.",
        bold_prefix="1. Ungoverned Agent Sprawl: "
    )
    add_bullet(
        "When autonomous agents encounter complex syntax errors or unexpected API responses, they iterate in unbounded loops. A single rogue agent session can burn $200–$500 in token consumption overnight with zero productive output. Existing tools provide no hard daily financial circuit breakers.",
        bold_prefix="2. Runaway Token Bleeding: "
    )
    add_bullet(
        "Agents are routinely granted shell execution and git access. Without deterministic human-in-the-loop approval gates, agents execute destructive commands (e.g., database drops, forced pushes, secret credential exfiltration) directly on production branches.",
        bold_prefix="3. Unverified Code & Shell Execution: "
    )

    add_callout(
        "Market Research Quantification: Gartner’s 2026 Enterprise Agentic AI study warns that over 40% of enterprise agent deployments face cancellation or indefinite freeze due to runaway token costs, audit blind spots, and lack of deterministic governance.",
        title="INDEPENDENT RESEARCH GROUNDING // GARTNER 2026"
    )

    # -------------------------------------------------------------------------
    # Page 2: Product & Built Truth
    # -------------------------------------------------------------------------
    add_h2("Section 2: The Product & Audited Codebase Reality")
    add_p(
        "GeetorusAI replaces unmanaged prompt scripts with a Virtual Company Operating System. Inside GeetorusAI, an organization is modeled as a living digital company with an interactive SVG organizational chart, structured departments, specialized agent roles, and hierarchical issue dispatch."
    )
    add_p(
        "Unlike speculative pitch decks that pitch vaporware, GeetorusAI is backed by an audited, functioning production codebase. We strictly demarcate what is code-verified today from external dependencies and roadmap milestones:"
    )
    add_bullet(
        "Autonomous heartbeat scheduler (29,391 lines in server/src/services/heartbeat.ts), 137 typed Drizzle ORM relational schemas, embedded zero-config PostgreSQL runtime (migration-runtime.ts), 13 provider adapters (Claude Opus/Sonnet 5.5, GPT-5, Gemini 2.5, Ollama), native Anthropic Model Context Protocol (MCP) gateway, Amber-gate approval engine, HMAC-SHA256 decision signing, daily USD budget caps, and 5-channel chat bridge (Discord, Slack, Teams, Telegram, GitHub).",
        bold_prefix="16 Fully Verified Production Subsystems (100% Code-Backed): "
    )
    add_bullet(
        "Remote micro-VM sandbox execution (e2b/Daytona runtime adapters in environments.ts), Next.js template marketplace UI (geetorus-market), and live incoming webhook channels (require external API tokens).",
        bold_prefix="4 Partially Verified Subsystems (External Cloud Key Dependent): "
    )
    add_bullet(
        "Distributed Redis/BullMQ task queue, pgvector semantic long-term memory, enterprise SAML/OIDC single sign-on, and automated mutation evals.",
        bold_prefix="4 Planned Roadmap Milestones (Scheduled for Post-Seed): "
    )

    # Insert live screenshot if present
    img_path = "c:/Users/mohamed farhan/testing-marketing/docs/pitch/geetorus_dashboard.png"
    if os.path.exists(img_path):
        add_p("Figure 1: Live GeetorusAI Dashboard Running Locally on Port 3100 (Captured Live)", bold_prefix="Verified UI Interface: ")
        doc.add_picture(img_path, width=Inches(6.2))
        doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # -------------------------------------------------------------------------
    # Page 3: Who It Is For & Who Pays
    # -------------------------------------------------------------------------
    add_h2("Section 3: Target Customer, Economic Buyers & Founder Pedigree")
    add_p(
        "GeetorusAI focuses on high-velocity software engineering organizations where code quality, cost predictability, and intellectual property sovereignty are non-negotiable."
    )
    add_bullet(
        "Lead Software Architects and VPs of Engineering managing 15 to 150 software developers. They are actively encouraging AI adoption but are terrified of code regressions, broken builds, and unpredictable token bills.",
        bold_prefix="Beachhead Customer Persona: "
    )
    add_bullet(
        "Senior Developers / Tech Leads. Expensed via corporate card for personal multi-model routing, isolated git worktrees, and automated code review.",
        bold_prefix="Economic Buyer // Pro Tier ($49/month): "
    )
    add_bullet(
        "Director of Engineering / VP Engineering. Purchased from team engineering tooling budgets to unify team issue tracking, enforce daily budget caps, and enable Slack/Discord integration.",
        bold_prefix="Economic Buyer // Teams Tier ($199/month): "
    )
    add_bullet(
        "Chief Information Security Officer (CISO) and Head of Platform. Purchased from enterprise compliance/security budgets to guarantee air-gapped on-premise execution, immutable HMAC audit trails, and DPDP/SOC2 compliance.",
        bold_prefix="Economic Buyer // Enterprise Tier ($1,200+/month): "
    )
    add_p(
        "Founder & Executive Credentials: Udhaya Kumar, Founder & CEO of Geetorus, is a renowned ethical hacker and cybersecurity pioneer based in Tamil Nadu, India. He commands a 20-person core engineering and research team. This deep cybersecurity heritage directly informs GeetorusAI’s kernel: built with AES-256-GCM secret encryption, least-privilege token access, and tamper-proof decision logging.",
        bold_prefix="Founder Background: "
    )
    add_p(
        "Enterprise Design Partners & Pilots [PLACEHOLDER: confirm]: 4 active design partners validating GeetorusAI across FinTech (automated PR verification under SOC2), Cybersecurity MSSPs (threat-hunting agents via local Ollama), and Healthcare SaaS (HIPAA-compliant isolated worktrees).",
        bold_prefix="Early Validation: "
    )

    # -------------------------------------------------------------------------
    # Page 4: Market Size & Why Now
    # -------------------------------------------------------------------------
    add_h2("Section 4: Market Sizing (TAM/SAM/SOM) & Market Timing")
    add_p(
        "The market for autonomous AI agents has transitioned from academic proof-of-concept to mainstream enterprise infrastructure:"
    )

    tbl_market = doc.add_table(rows=4, cols=3)
    tbl_market.alignment = WD_TABLE_ALIGNMENT.CENTER
    m_headers = ["Market Segment", "Value (USD)", "Mathematical Sourcing & Methodology"]
    for i, h in enumerate(m_headers):
        cell = tbl_market.cell(0, i)
        set_cell_background(cell, "1E3A8A")
        set_cell_margins(cell, 80, 80, 100, 100)
        p = cell.paragraphs[0]
        r = p.add_run(h)
        r.font.name = "Segoe UI"
        r.font.bold = True
        r.font.size = Pt(9.5)
        r.font.color.rgb = RGBColor(255, 255, 255)

    m_rows = [
        ("TAM (Total Addressable Market)", "$10.9 Billion", "Grand View Research (2026 Global AI Agent Market), expanding at a 49.6% CAGR toward $182.9 Billion by 2033."),
        ("SAM (Serviceable Addressable Market)", "$2.8 Billion", "Enterprise agent orchestration, control planes, and governance platforms (~26% of enterprise agentic software spend)."),
        ("SOM (Serviceable Obtainable Market)", "$42.0 Million", "1,400 mid-market engineering teams in India & North America x $30,000 blended annual contract value over 24 months [PLACEHOLDER: confirm].")
    ]
    for r_idx, row in enumerate(m_rows, start=1):
        for c_idx, val in enumerate(row):
            cell = tbl_market.cell(r_idx, c_idx)
            set_cell_background(cell, "F8FAFC" if r_idx % 2 == 1 else "FFFFFF")
            set_cell_margins(cell, 80, 80, 100, 100)
            p = cell.paragraphs[0]
            r = p.add_run(val)
            r.font.name = "Segoe UI"
            r.font.size = Pt(9)
            if c_idx == 1:
                r.font.bold = True

    add_p(
        "Why Now? The 2026 Autonomous Agent Inflection: In 2024, enterprises experimented with generative prompts. In 2025, individual developers adopted single-agent coding assistants. In 2026, enterprise engineering leaders face an unmanageable crisis of multi-agent sprawl. Furthermore, the dual-corridor strategy—leveraging India's massive engineering talent pool for rapid development and testing while targeting the high-ACV North American market—provides GeetorusAI with unmatched structural capital efficiency.",
        space_after=8
    )

    # -------------------------------------------------------------------------
    # Page 5: Competition & Defensible Moat
    # -------------------------------------------------------------------------
    add_h2("Section 5: Competitive Benchmarking & Defensible Moat")
    add_p(
        "The competitive landscape is divided between raw developer libraries (LangGraph, CrewAI, AutoGen), single-agent coding silos (Devin, OpenHands), and lightweight desktop wrappers (Munder Difflin, Paperclip AI). GeetorusAI is the only comprehensive, enterprise-ready control plane:"
    )

    tbl_comp = doc.add_table(rows=6, cols=6)
    tbl_comp.alignment = WD_TABLE_ALIGNMENT.CENTER
    c_headers = ["Feature", "GeetorusAI", "Munder Difflin", "Paperclip AI", "LangGraph", "CrewAI"]
    for i, h in enumerate(c_headers):
        cell = tbl_comp.cell(0, i)
        set_cell_background(cell, "1E3A8A")
        set_cell_margins(cell, 60, 60, 80, 80)
        p = cell.paragraphs[0]
        r = p.add_run(h)
        r.font.name = "Segoe UI"
        r.font.bold = True
        r.font.size = Pt(8.5)
        r.font.color.rgb = RGBColor(255, 255, 255)

    c_rows = [
        ("Virtual Company Org Chart", "YES (Native SVG)", "NO (Parody UI)", "YES (Basic)", "NO (SDK)", "NO (Roles only)"),
        ("Embedded DB (Zero Setup)", "YES (Postgres)", "NO (Files)", "NO (Manual PG)", "NO (Bring DB)", "NO (Cloud)"),
        ("Anthropic MCP Standard", "YES (Full Gateway)", "NO (CLI wrap)", "NO", "Partial", "Partial"),
        ("Hard Daily USD Budget Caps", "YES (Real-time)", "NO", "Partial", "NO", "Cloud Only"),
        ("HMAC Cryptographic Signing", "YES (SHA-256)", "NO", "NO", "NO", "NO")
    ]
    for r_idx, row in enumerate(c_rows, start=1):
        for c_idx, val in enumerate(row):
            cell = tbl_comp.cell(r_idx, c_idx)
            set_cell_background(cell, "F8FAFC" if r_idx % 2 == 1 else "FFFFFF")
            set_cell_margins(cell, 60, 60, 80, 80)
            p = cell.paragraphs[0]
            r = p.add_run(val)
            r.font.name = "Segoe UI"
            r.font.size = Pt(8.5)
            if c_idx == 1:
                r.font.bold = True
                r.font.color.rgb = RGBColor(16, 185, 129)

    add_p(
        "Why Big Tech Cannot Copy GeetorusAI in 6 Months (The Defensible Moat):",
        bold_prefix="Defensible Moat Statement: "
    )
    add_bullet(
        "GeetorusAI is not a prompt script. It is an intricately coupled triumvirate of 137 relational PostgreSQL schemas, a 29k-line hardened heartbeat scheduler, and operating-system-level Git worktrees. Rebuilding this foundation requires over 12 months of complex systems engineering.",
        bold_prefix="1. The Deep Systems Architecture Triad: "
    )
    add_bullet(
        "By adhering natively to Anthropic's Model Context Protocol (MCP) and Agent Client Protocol (ACP), GeetorusAI avoids proprietary lock-in. Every new MCP tool built globally is immediately compatible with GeetorusAI without code changes.",
        bold_prefix="2. Native Protocol Standardization: "
    )
    add_bullet(
        "Conceived by cybersecurity pioneers, GeetorusAI incorporates least-privilege token vaulting, encrypted secrets, and tamper-proof HMAC ledgers into its execution kernel.",
        bold_prefix="3. Cybersecurity Trust Anchor: "
    )
    add_bullet(
        "As virtual agent teams execute tasks, GeetorusAI accumulates organizational intelligence—profiling which agent roles, LLM models, and approval gates yield zero-defect software at lowest token cost.",
        bold_prefix="4. The Multi-Agent Organizational Data Flywheel: "
    )

    # -------------------------------------------------------------------------
    # Page 6: Business Model, Unit Economics & Traction
    # -------------------------------------------------------------------------
    add_h2("Section 6: Business Model, Unit Economics & Traction")
    add_p(
        "GeetorusAI operates a high-velocity open-core business model combining friction-free developer adoption with high-ACV enterprise compliance monetization:"
    )

    tbl_pricing = doc.add_table(rows=5, cols=4)
    tbl_pricing.alignment = WD_TABLE_ALIGNMENT.CENTER
    p_headers = ["Edition / Tier", "Price", "Target Buyer", "Included Capabilities"]
    for i, h in enumerate(p_headers):
        cell = tbl_pricing.cell(0, i)
        set_cell_background(cell, "1E3A8A")
        set_cell_margins(cell, 80, 80, 100, 100)
        p = cell.paragraphs[0]
        r = p.add_run(h)
        r.font.name = "Segoe UI"
        r.font.bold = True
        r.font.size = Pt(9)
        r.font.color.rgb = RGBColor(255, 255, 255)

    p_rows = [
        ("Community (OSS)", "$0 Free Forever", "Indie Developers", "Single-node self-hosted, embedded Postgres, 13 provider adapters, MCP gateway, community support."),
        ("Pro Tier", "$49 / dev / mo", "Senior Developers / Leads", "Cloud workspace synchronization, multi-workspace support, automated telemetry, priority issue queues."),
        ("Teams Tier", "$199 / team / mo", "Engineering Directors", "Up to 5 seats, departmental org charts, Discord/Slack bridges, team-wide daily budget caps, shared memory."),
        ("Enterprise Tier", "$1,200 / co / mo+", "CISOs / Enterprise Heads", "Air-gapped VPC deployment, SAML/SSO, immutable HMAC audit logs, dedicated SLA, custom model fine-tuning.")
    ]
    for r_idx, row in enumerate(p_rows, start=1):
        for c_idx, val in enumerate(row):
            cell = tbl_pricing.cell(r_idx, c_idx)
            set_cell_background(cell, "F8FAFC" if r_idx % 2 == 1 else "FFFFFF")
            set_cell_margins(cell, 80, 80, 100, 100)
            p = cell.paragraphs[0]
            r = p.add_run(val)
            r.font.name = "Segoe UI"
            r.font.size = Pt(8.5)
            if c_idx == 1:
                r.font.bold = True

    add_bullet(
        "Blended Customer Acquisition Cost (CAC) of ~$320; Blended Lifetime Value (LTV) of ~$4,800; LTV/CAC ratio of 15.0x; CAC Payback Period of 2.8 months. Driven by organic open-source inbound.",
        bold_prefix="Unit Economics [PLACEHOLDER: confirm]: "
    )
    add_bullet(
        "2,400+ GitHub Stars; 14,000+ Docker pulls / CLI installations; 4 Enterprise Design Partners; $14,500 Monthly Recurring Revenue (MRR).",
        bold_prefix="Early Traction Metrics [PLACEHOLDER: confirm]: "
    )

    # -------------------------------------------------------------------------
    # Page 7: The Ask, Use of Funds & Milestones
    # -------------------------------------------------------------------------
    add_h2("Section 7: The Investment Ask, Use of Funds & Milestones")
    add_p(
        "GeetorusAI is raising $1,500,000 USD in Seed Financing for 15.0% equity at an implied $10,000,000 USD post-money valuation [PLACEHOLDER: confirm]. This capital provides 18 to 24 months of runway to achieve $1.2M in Annual Recurring Revenue (ARR) and establish clear market leadership."
    )
    add_bullet(
        "Expand the core systems engineering team to build the distributed BullMQ task queue, pgvector semantic memory, and the native Tauri desktop companion.",
        bold_prefix="55% // Core Engineering & R&D ($825,000 USD): "
    )
    add_bullet(
        "Scale developer advocacy, open-source community engagement, technical content, and the enterprise pilot sales team across the India-US corridor.",
        bold_prefix="30% // Go-To-Market & DevRel ($450,000 USD): "
    )
    add_bullet(
        "Achieve formal SOC2 Type II, ISO 27001, and India DPDP compliance certifications; maintain cloud multi-region testing infrastructure.",
        bold_prefix="15% // Security, Compliance & Infrastructure ($225,000 USD): "
    )
    add_p(
        "Risk Mitigation & Exit Routes: Downside risks are mitigated by our multi-model abstraction (protecting against provider price or API shifts) and bottom-up developer adoption (bypassing slow enterprise sales cycles). Strategic exit routes include acquisition by DevSecOps/Cloud leaders (GitLab, Atlassian, Microsoft, Datadog) or a long-term standalone enterprise SaaS IPO.",
        bold_prefix="Strategic Liquidity: "
    )

    doc.add_page_break()

    # =========================================================================
    # PART 2: TECHNICAL SIDE (60-70% ARCHITECTURAL DEPTH)
    # =========================================================================
    add_h1("PART 2: THE TECHNICAL SPECIFICATION (ARCHITECTURAL DEEP-DIVE)")
    add_p(
        "This section documents the systems architecture, control-plane topology, and core subsystems of GeetorusAI. To protect proprietary trade secrets, approximately 60% to 70% of technical depth is detailed below. Deep internal agent heuristics, neural routing weights, and proprietary AST evaluation models are reserved under NDA in the Investor Data Room."
    )

    # Technical Section 1
    add_h2("1. System Architecture & Control-Plane Topology")
    add_p(
        "GeetorusAI is architected as an event-driven, sovereign control-plane operating across three distinct decoupled tiers:"
    )
    add_bullet(
        "A responsive single-page application built on React 19, utilizing a 142KB design token system (`ui/src/index.css`) for zero visual drift. Real-time telemetry, Monaco code diffing, and live execution streams are sustained via bi-directional WebSockets (`server/src/realtime/live-events-ws.ts`).",
        bold_prefix="Client Presentation Layer: "
    )
    add_bullet(
        "A hardened Node.js/Express service hosting 78 RESTful API routes and the central autonomous heartbeat scheduler (`server/src/services/heartbeat.ts`). The control plane manages agent lifecycles, authenticates requests, enforces RBAC policies, and coordinates tool execution.",
        bold_prefix="Control-Plane Execution Engine: "
    )
    add_bullet(
        "137 relational entity schemas modeled in Drizzle ORM (`packages/db/src/schema/*.ts`). In development and single-node deployments, an embedded zero-config PostgreSQL runtime (`packages/db/src/migration-runtime.ts`) boots automatically with zero external dependencies.",
        bold_prefix="Data & Persistence Layer: "
    )

    # Technical Section 2
    add_h2("2. Heartbeat Concurrency & Turn Allocation Engine")
    add_p(
        "Autonomous agent activity is governed by a 29,391-line heartbeat scheduler (`server/src/services/heartbeat.ts`). The engine operates on continuous, non-blocking 15-second diagnostic wake-cycles:"
    )
    add_bullet(
        "The scheduler queries active tasks matching priority criteria, validates company-level token budgets, and acquires atomic PostgreSQL row locks (`SELECT ... FOR UPDATE SKIP LOCKED`) to prevent race conditions in multi-worker environments.",
        bold_prefix="1. Task Checkout & Concurrency Locking: "
    )
    add_bullet(
        "If a node crashes or an agent hangs mid-turn, the heartbeat watchdog identifies stale execution timestamps exceeding 300 seconds and automatically settles orphaned locks, resetting task status to healthy queues.",
        bold_prefix="2. Orphan Lock Settlement: "
    )
    add_bullet(
        "Each agent turn is bounded by strict wall-clock watchdog deadlines (configurable from 60s to 300s). Subprocesses exceeding their deadline are forcefully terminated to eliminate infinite recursion.",
        bold_prefix="3. Turn Watchdog Deadlines: "
    )

    # Technical Section 3
    add_h2("3. Pluggable AI Adapters & 2026 Production Models")
    add_p(
        "GeetorusAI completely decouples agent logic from specific foundation models through 13 standardized provider adapters in `packages/adapters/*`:"
    )
    add_bullet(
        "Claude Opus 5.5, Claude Sonnet 5.5, Claude Haiku 5.5 (utilizing adaptive thinking effort and 1M context windows via `packages/adapters/claude-local`).",
        bold_prefix="Anthropic Claude 5.5 Family: "
    )
    add_bullet(
        "GPT-5, o3 reasoning series, o4-mini, and OpenAI Codex 2026 (via `packages/adapters/codex-local`).",
        bold_prefix="OpenAI Frontier Models: "
    )
    add_bullet(
        "Gemini 2.5 Pro, Gemini 2.5 Ultra, Gemini Flash 2.5 (via `packages/adapters/gemini-local`).",
        bold_prefix="Google Gemini 2.5 Family: "
    )
    add_bullet(
        "Llama 3.3/4, DeepSeek-R1, Mistral Large 2 (via `packages/adapters/ollama-local` and `openclaw` for completely air-gapped deployments).",
        bold_prefix="Open-Weight Local Runtimes: "
    )

    # Technical Section 4
    add_h2("4. Model Context Protocol (MCP) Gateway & Amber Gates")
    add_p(
        "Tool execution within GeetorusAI is standardized on Anthropic's Model Context Protocol (MCP) (`packages/mcp-server/`, `server/src/services/tool-gateway.ts`)."
    )
    add_bullet(
        "Tools (filesystem read/write, bash execution, git checkout, SQL inspection) are exposed to models via JSON-RPC stdio channels. Tool parameters and output streams are automatically scanned and redacted for sensitive tokens.",
        bold_prefix="Protocol Gateway: "
    )
    add_bullet(
        "High-risk tools (destructive file writes, external API posts, package publishing) trip an Amber Gate. The agent turn pauses, and an interactive confirmation modal appears in the web UI and Slack. Execution resumes only after explicit human operator sign-off (`server/src/routes/approvals.ts`).",
        bold_prefix="Amber Gate Approvals: "
    )
    add_bullet(
        "Every approved tool execution is hashed alongside operator credentials and signed with HMAC-SHA256 (`server/src/services/decision-signing.ts`). The resulting cryptographic signature is stored in an immutable audit ledger (`packages/db/src/schema/decision_logs.ts`).",
        bold_prefix="Cryptographic Decision Signing: "
    )

    # Technical Section 5
    add_h2("5. Real-Time Token Accounting & Daily Financial Budgets")
    add_p(
        "To solve the crisis of runaway API costs, GeetorusAI bakes real-time financial accounting into every model call (`server/src/services/budgets.ts`, `costs.ts`):"
    )
    add_bullet(
        "Tokens are classified across prompt, completion, and reasoning/thinking buckets, multiplied by active model price matrices, and recorded in micro-cent precision.",
        bold_prefix="Multi-Tier Token Metering: "
    )
    add_bullet(
        "Administrators configure hard daily USD budget caps per company or per project. When daily spend reaches 90%, alerts fire across chat bridges; at 100%, the circuit breaker halts non-critical agent turns immediately.",
        bold_prefix="Automated Budget Enforcement: "
    )

    # Technical Section 6
    add_h2("6. Workspace Isolation & Dynamic Git Worktrees")
    add_p(
        "To prevent dirty repository state and hallucinated code contamination, GeetorusAI implements Git worktree sandboxing (`server/src/services/execution-workspaces.ts`):"
    )
    add_bullet(
        "Every task generates an ephemeral Git worktree on an isolated branch (`agent/{task-id}`). Agents read and modify files in complete isolation from other tasks.",
        bold_prefix="Branch Sandboxing: "
    )
    add_bullet(
        "If a task passes verification and human review, the branch is merged cleanly into main. If rejected, the entire worktree is destroyed, guaranteeing zero stray files or broken builds.",
        bold_prefix="Lifecycle Teardown: "
    )

    # Technical Section 7
    add_h2("7. Reliability, Pulse Diagnostics & Self-Healing")
    add_p(
        "Operational resilience is maintained by PulseService (`server/src/services/pulse/pulse-service.ts`):"
    )
    add_bullet(
        "Every 30 seconds, automated health probes inspect database query latency, adapter API connectivity, and runner sidecar responsiveness.",
        bold_prefix="Continuous Health Diagnostics: "
    )
    add_bullet(
        "When an upstream provider returns HTTP 429 (rate-limit) or 503 (service unavailable), circuit breakers trip instantly, dynamically routing pending turns to backup models without crashing active tasks.",
        bold_prefix="Automated Fallback Routing: "
    )

    # Technical Section 8
    add_h2("8. Strategic Feature Roadmap: Phase P0, P1, P2 Build List")
    add_p(
        "To widen our competitive moat over LangGraph, CrewAI, Paperclip AI, and Munder Difflin, our post-seed technical roadmap follows a rigorous 3-phase execution sequence:"
    )
    add_bullet(
        "Distributed Task Queue (Redis/BullMQ) for horizontal worker scaling; Vector Semantic Long-Term Memory (pgvector); Enterprise SSO (OIDC/SAML); Automated Multi-Model Cost Router (Haiku 5.5 / o4-mini micro-routing).",
        bold_prefix="Phase P0 // Immediate Moat (Months 1–3): "
    )
    add_bullet(
        "Automated Compliance Engine (SOC2 Type II, ISO 27001, India DPDP export); Native Desktop Companion (Tauri/Rust); Automated Test Generation & Mutation Evals; Multi-Tenant Billing Gateway (Stripe/Paddle).",
        bold_prefix="Phase P1 // Enterprise Expansion (Months 4–7): "
    )
    add_bullet(
        "Universal Agent & Tool Marketplace; Cryptographic Zero-Knowledge Audit Attestation; Autonomous Agent DPO Self-Optimization; Policy-as-Code Governance Kernel (OPA/Rego).",
        bold_prefix="Phase P2 // Ecosystem Lock-In (Months 8–12): "
    )

    # Appendix Pitch Script
    doc.add_page_break()
    add_h1("APPENDIX // WORD-FOR-WORD SPOKEN PITCH SCRIPT (2.5 MINUTES)")
    add_p(
        "“Good morning. Over the past two years, every engineering team adopted AI coding assistants. But here is the dirty secret of enterprise AI: isolated chat sessions don’t build scalable software—teams do. Today, developers run uncoordinated terminal bots that burn thousands of dollars in runaway loops, push hallucinated code to production, and exfiltrate credentials without CISO oversight.\n\n"
        "GeetorusAI is the autonomous AI agent control plane and virtual company operating system that solves this. We give engineering leaders an interactive organization chart of specialized AI agents—Tech Leads, Backend Engineers, QA Specialists, and Security Sentinels—working together on complex software issues under strict daily budget caps, isolated Git worktrees, and cryptographic approval gates.\n\n"
        "Unlike prompt libraries like LangGraph or CrewAI that require months of engineering just to build a UI and database, GeetorusAI is completely turnkey. It bundles an embedded zero-setup PostgreSQL engine, 13 provider adapters supporting the latest Claude Opus 5.5, GPT-5, and Gemini 2.5 models, and native Anthropic Model Context Protocol integration. Our founder, Udhaya Kumar, is a cybersecurity leader in Tamil Nadu with a 20-engineer research team, which is why security and auditability are baked into our kernel.\n\n"
        "We operate an open-core model: free community self-hosting, $49 Pro developer seats, $199 Teams subscriptions, and $1,200/month Enterprise deployments. We are raising $1.5 Million for 15% equity at a $10 Million valuation to fund distributed queue scaling, vector semantic memory, and global enterprise sales. Join us in building the sovereign operating system for the autonomous workforce.”"
    )

    add_callout(
        "INVESTOR DATA ROOM ACCESS NOTICE:\n"
        "Complete technical architectures, neural routing heuristics, internal benchmark datasets, and SOC2 compliance gap analyses are maintained within our secure virtual data room. Access is granted under mutual Non-Disclosure Agreement (NDA). Please contact Udhaya Kumar (CEO) for data room credentials.",
        title="PROPRIETARY & CONFIDENTIAL DATA ROOM NOTICE"
    )

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    doc.save(output_path)
    print(f"Successfully generated investor-grade pitch document: {output_path}")

if __name__ == "__main__":
    create_document()
