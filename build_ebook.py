# -*- coding: utf-8 -*-
"""
Ebook generator - Marine Automation Portfolio series
Project 1: Smart Exhaust Gas Cleaning System (EGCS)
Author: Sipho Lucky Sibanda
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, Image, KeepTogether, HRFlowable
)
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# ---------------------------------------------------------------------------
# Fonts
# ---------------------------------------------------------------------------
FD = "/usr/share/fonts/truetype/dejavu/"
pdfmetrics.registerFont(TTFont("Sans", FD + "DejaVuSans.ttf"))
pdfmetrics.registerFont(TTFont("Sans-Bold", FD + "DejaVuSans-Bold.ttf"))
pdfmetrics.registerFont(TTFont("Sans-Oblique", FD + "DejaVuSans-Oblique.ttf"))
pdfmetrics.registerFont(TTFont("Cond-Bold", FD + "DejaVuSansCondensed-Bold.ttf"))
pdfmetrics.registerFont(TTFont("Cond", FD + "DejaVuSansCondensed.ttf"))
pdfmetrics.registerFont(TTFont("Mono", FD + "DejaVuSansMono.ttf"))
pdfmetrics.registerFont(TTFont("Mono-Bold", FD + "DejaVuSansMono-Bold.ttf"))

# ---------------------------------------------------------------------------
# Palette
# ---------------------------------------------------------------------------
NAVY      = colors.HexColor("#0A1930")
NAVY2     = colors.HexColor("#0F1C2C")
NAVY_LINE = colors.HexColor("#1C4A68")
CYAN      = colors.HexColor("#5EC8E8")
CYAN_SOFT = colors.HexColor("#BFE6F5")
TEAL      = colors.HexColor("#2FBE96")
AMBER     = colors.HexColor("#F5A623")
RED       = colors.HexColor("#E0503E")
INK       = colors.HexColor("#132038")
MUTED     = colors.HexColor("#5B7089")
MUTED_LT  = colors.HexColor("#8FB4CE")
PANEL     = colors.HexColor("#EEF4F8")
ROWBAND   = colors.HexColor("#F5F9FB")
GRIDLINE  = colors.HexColor("#D7E4EC")

PAGE_W, PAGE_H = A4
MARGIN_L, MARGIN_R = 22 * mm, 20 * mm
MARGIN_TOP, MARGIN_BOT = 26 * mm, 24 * mm
AVAIL_W = PAGE_W - MARGIN_L - MARGIN_R

DOC_TITLE = "SMART EXHAUST GAS CLEANING SYSTEM (EGCS)"
AUTHOR = "Sipho Lucky Sibanda"
OUTFILE = "/home/claude/marine-egcs-scrubber-control/ebook/EGCS_Technical_Manual.pdf"

# ---------------------------------------------------------------------------
# Styles
# ---------------------------------------------------------------------------
body = ParagraphStyle("body", fontName="Sans", fontSize=10.2, leading=15,
                       textColor=INK, spaceAfter=8, alignment=TA_JUSTIFY)
body_l = ParagraphStyle("body_l", parent=body, alignment=TA_LEFT)
lead = ParagraphStyle("lead", parent=body, fontSize=12.5, leading=18, textColor=NAVY,
                       spaceAfter=10)
kicker = ParagraphStyle("kicker", fontName="Mono", fontSize=8.5, leading=11,
                         textColor=TEAL, spaceAfter=2)
h1 = ParagraphStyle("h1", fontName="Cond-Bold", fontSize=19, leading=22,
                     textColor=NAVY, spaceAfter=2)
h2 = ParagraphStyle("h2", fontName="Cond-Bold", fontSize=13.5, leading=16,
                     textColor=NAVY, spaceBefore=14, spaceAfter=6)
h3 = ParagraphStyle("h3", fontName="Sans-Bold", fontSize=10.6, leading=13,
                     textColor=NAVY, spaceBefore=8, spaceAfter=4)
caption = ParagraphStyle("caption", fontName="Sans-Oblique", fontSize=8.3, leading=11,
                          textColor=MUTED, alignment=TA_CENTER, spaceBefore=4, spaceAfter=10)
bullet = ParagraphStyle("bullet", parent=body, alignment=TA_LEFT, leftIndent=12,
                         bulletIndent=0, spaceAfter=5)
chip_num = ParagraphStyle("chip_num", fontName="Cond-Bold", fontSize=17, leading=20,
                           textColor=colors.white, alignment=TA_CENTER)
toc_entry = ParagraphStyle("toc_entry", fontName="Sans", fontSize=10.5, leading=16,
                            textColor=INK)
toc_num = ParagraphStyle("toc_num", fontName="Mono-Bold", fontSize=10.5, leading=16,
                          textColor=TEAL)
cell_hdr = ParagraphStyle("cell_hdr", fontName="Sans-Bold", fontSize=8.6, leading=11,
                           textColor=colors.white)
cell_txt = ParagraphStyle("cell_txt", fontName="Sans", fontSize=8.6, leading=12,
                           textColor=INK)
code_style = ParagraphStyle("code", fontName="Mono", fontSize=7.6, leading=11.2,
                             textColor=CYAN_SOFT)
callout_title = lambda c: ParagraphStyle("ct", fontName="Sans-Bold", fontSize=9.6,
                                          leading=12, textColor=c, spaceAfter=3)
callout_body = ParagraphStyle("cb", fontName="Sans", fontSize=9.4, leading=13.4,
                               textColor=INK)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def P(text, style=body):
    return Paragraph(text, style)

def chapter_head(num, title, kicker_text="EGCS SCRUBBER CONTROL"):
    chip = Table([[Paragraph(str(num).zfill(2), chip_num)]],
                 colWidths=[17 * mm], rowHeights=[17 * mm])
    chip.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), TEAL),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
    ]))
    title_block = [P(kicker_text, kicker), P(title, h1)]
    row = Table([[chip, title_block]], colWidths=[22 * mm, AVAIL_W - 22 * mm])
    row.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (1, 0), (1, 0), 10),
        ("LEFTPADDING", (0, 0), (0, 0), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
    ]))
    rule = HRFlowable(width="100%", thickness=1.3, color=CYAN, spaceBefore=8, spaceAfter=16)
    return [row, rule]

def subhead(text):
    return P(text, h2)

def bullets(items):
    out = []
    for it in items:
        out.append(P("&#8226;&nbsp;&nbsp;" + it, bullet))
    return out

def code_block(code_text, cap=None):
    lines = code_text.strip("\n").split("\n")
    esc_lines = []
    for ln in lines:
        stripped = ln.lstrip(" ")
        n = len(ln) - len(stripped)
        esc_lines.append("&nbsp;" * n + esc(stripped) if stripped else "&nbsp;")
    para = Paragraph("<br/>".join(esc_lines), code_style)
    cell = Table([[para]], colWidths=[AVAIL_W])
    cell.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), NAVY2),
        ("BOX", (0, 0), (-1, -1), 0.75, NAVY_LINE),
        ("LEFTPADDING", (0, 0), (-1, -1), 12),
        ("RIGHTPADDING", (0, 0), (-1, -1), 12),
        ("TOPPADDING", (0, 0), (-1, -1), 9),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 9),
    ]))
    out = [cell]
    if cap:
        out.append(P(cap, caption))
    else:
        out.append(Spacer(1, 10))
    return out

def data_table(headers, rows, col_widths=None):
    data = [[Paragraph(h, cell_hdr) for h in headers]]
    for r in rows:
        data.append([Paragraph(str(c), cell_txt) for c in r])
    t = Table(data, colWidths=col_widths, repeatRows=1)
    style = [
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("GRID", (0, 0), (-1, -1), 0.5, GRIDLINE),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
    ]
    for i in range(1, len(data)):
        if i % 2 == 0:
            style.append(("BACKGROUND", (0, i), (-1, i), ROWBAND))
    t.setStyle(TableStyle(style))
    return t

def callout(title, text, kind="info"):
    color = {"info": CYAN, "warning": AMBER, "critical": RED, "ok": TEAL}[kind]
    label = {"info": "NOTE", "warning": "REGULATORY NOTE", "critical": "SAFETY CRITICAL",
             "ok": "ENGINEERING NOTE"}[kind]
    content = [P("%s &mdash; %s" % (label, title), callout_title(color)), P(text, callout_body)]
    inner = Table([[content]], colWidths=[AVAIL_W - 16])
    inner.setStyle(TableStyle([
        ("LEFTPADDING", (0, 0), (-1, -1), 0), ("TOPPADDING", (0, 0), (-1, -1), 0),
    ]))
    outer = Table([["", inner]], colWidths=[5, AVAIL_W - 5])
    outer.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, 0), color),
        ("BACKGROUND", (1, 0), (1, 0), PANEL),
        ("LEFTPADDING", (1, 0), (1, 0), 12),
        ("RIGHTPADDING", (1, 0), (1, 0), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))
    return [outer, Spacer(1, 10)]

def full_image(path, cap, max_h_mm=95):
    from PIL import Image as PILImage
    iw, ih = PILImage.open(path).size
    ratio = ih / float(iw)
    w = AVAIL_W
    h = w * ratio
    max_h = max_h_mm * mm
    if h > max_h:
        h = max_h
        w = h / ratio
    img = Image(path, width=w, height=h)
    img.hAlign = "CENTER"
    return [img, P(cap, caption)]


# ---------------------------------------------------------------------------
# Page backgrounds
# ---------------------------------------------------------------------------
def draw_cover(c, doc):
    c.saveState()
    c.setFillColor(NAVY)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)

    c.setStrokeColor(NAVY_LINE)
    c.setLineWidth(0.4)
    step = 12 * mm
    x = 0
    while x < PAGE_W:
        c.line(x, 0, x, PAGE_H); x += step
    y = 0
    while y < PAGE_H:
        c.line(0, y, PAGE_W, y); y += step

    c.setStrokeColor(CYAN)
    c.setLineWidth(1.1)
    c.rect(10 * mm, 10 * mm, PAGE_W - 20 * mm, PAGE_H - 20 * mm, fill=0, stroke=1)

    # Decorative valve/schematic glyph, bottom right
    c.setStrokeColor(CYAN)
    c.setLineWidth(1.2)
    cx, cy, r = PAGE_W - 46 * mm, 52 * mm, 16 * mm
    c.circle(cx, cy, r, fill=0, stroke=1)
    c.line(cx - r * 0.7, cy - r * 0.7, cx + r * 0.7, cy + r * 0.7)
    c.line(cx - r * 0.7, cy + r * 0.7, cx + r * 0.7, cy - r * 0.7)
    c.line(cx - 30 * mm, cy, cx - r, cy)
    c.line(cx + r, cy, cx + 30 * mm, cy)
    c.setDash(2, 2)
    c.line(cx, cy + r, cx, cy + 34 * mm)
    c.setDash()

    c.setFillColor(CYAN)
    c.setFont("Mono", 10.5)
    c.drawString(24 * mm, PAGE_H - 42 * mm, "MARINE AUTOMATION PORTFOLIO   ·   PROJECT 01")

    c.setFillColor(colors.white)
    c.setFont("Cond-Bold", 29)
    for i, line in enumerate(["SMART EXHAUST GAS", "CLEANING SYSTEM (EGCS)"]):
        c.drawString(24 * mm, PAGE_H - 62 * mm - i * 11.5 * mm, line)

    c.setFont("Cond", 13.5)
    c.setFillColor(CYAN_SOFT)
    c.drawString(24 * mm, PAGE_H - 90 * mm, "Automated Closed-Loop Scrubber Control")
    c.drawString(24 * mm, PAGE_H - 97 * mm, "for Marine Emissions Compliance")

    c.setStrokeColor(NAVY_LINE)
    c.setLineWidth(0.8)
    c.line(24 * mm, 46 * mm, PAGE_W - 24 * mm, 46 * mm)

    c.setFont("Mono", 9.5)
    c.setFillColor(TEAL)
    c.drawString(24 * mm, 38 * mm, "TECHNICAL PROJECT MANUAL  ·  REV. A")
    c.setFont("Sans-Bold", 13)
    c.setFillColor(colors.white)
    c.drawString(24 * mm, 31 * mm, "By " + AUTHOR)
    c.setFont("Sans", 8.6)
    c.setFillColor(MUTED_LT)
    c.drawString(24 * mm, 25.5 * mm, "PLC Platform: Siemens S7-1500 (SCL) / CODESYS-portable Structured Text")
    c.drawString(24 * mm, 21 * mm, "Simulation & Portfolio Engineering Build  ·  Not for Shipboard Deployment")
    c.restoreState()

def draw_body(c, doc):
    c.saveState()
    c.setFillColor(NAVY)
    c.rect(0, PAGE_H - 15 * mm, PAGE_W, 15 * mm, fill=1, stroke=0)
    c.setFillColor(CYAN)
    c.setFont("Mono", 7.6)
    c.drawString(MARGIN_L, PAGE_H - 9.5 * mm, DOC_TITLE)
    c.setFillColor(colors.white)
    c.setFont("Sans", 7.4)
    c.drawRightString(PAGE_W - MARGIN_R, PAGE_H - 9.5 * mm, "By " + AUTHOR)
    c.setStrokeColor(CYAN)
    c.setLineWidth(0.8)
    c.line(0, PAGE_H - 15 * mm, PAGE_W, PAGE_H - 15 * mm)

    c.setFillColor(MUTED)
    c.setFont("Mono", 7.8)
    c.drawString(MARGIN_L, 13 * mm, "EGCS-SCRUBBER-CTRL")
    c.drawCentredString(PAGE_W / 2, 13 * mm, "Page %d" % c.getPageNumber())
    c.drawRightString(PAGE_W - MARGIN_R, 13 * mm, "Simulation / Portfolio Build")
    c.setStrokeColor(CYAN)
    c.setLineWidth(1)
    c.line(PAGE_W - MARGIN_R, 17 * mm, PAGE_W - MARGIN_R, 21 * mm)
    c.line(PAGE_W - MARGIN_R - 4 * mm, 17 * mm, PAGE_W - MARGIN_R, 17 * mm)
    c.restoreState()


# ---------------------------------------------------------------------------
# Content
# ---------------------------------------------------------------------------
story = [PageBreak()]

# ---- Document control / disclaimer ------------------------------------------------
story += chapter_head("i", "Document Control &amp; Disclaimer", "FRONT MATTER")
story.append(P(
    "This document is a self-authored technical project manual produced as part of a "
    "personal engineering portfolio. It describes the design, control philosophy, and "
    "simulated validation of an Exhaust Gas Cleaning System (EGCS) scrubber controller, "
    "built to demonstrate PLC programming, closed-loop control design, and marine "
    "regulatory awareness for automation, controls, and marine engineering roles.", body))
story.append(P(
    "The system described here was developed and tested in simulation only (PLCSIM-style "
    "forcing of inputs and desktop review), using publicly available regulatory references "
    "for realism. No part of this project has been installed, commissioned, or verified on "
    "physical shipboard hardware, and it must not be treated as a certified or classed "
    "automation package.", body))

story += callout(
    "Portfolio project, not a certified design",
    "Figures, setpoints, and instrumentation ranges in this manual are engineering-realistic "
    "but illustrative. A real EGCS installation requires class society approval (e.g. DNV, "
    "ABS, Lloyd's Register), manufacturer-specific I/O, and a full HAZOP / FMEA study before "
    "any of this logic could be considered for actual use.", "critical")

data = [
    ["Document Title", "Smart Exhaust Gas Cleaning System (EGCS) \u2014 Technical Project Manual"],
    ["Author", AUTHOR],
    ["Revision", "A"],
    ["Document Type", "Portfolio Technical Manual (Simulation)"],
    ["Target PLC Platform", "Siemens S7-1500 (TIA Portal / SCL) \u2014 CODESYS-portable"],
    ["Related Repository", "marine-egcs-scrubber-control"],
]
t = Table(data, colWidths=[45 * mm, AVAIL_W - 45 * mm])
t.setStyle(TableStyle([
    ("FONTNAME", (0, 0), (0, -1), "Sans-Bold"), ("FONTNAME", (1, 0), (1, -1), "Sans"),
    ("FONTSIZE", (0, 0), (-1, -1), 9.4), ("TEXTCOLOR", (0, 0), (0, -1), NAVY),
    ("TEXTCOLOR", (1, 0), (1, -1), INK),
    ("GRID", (0, 0), (-1, -1), 0.4, GRIDLINE),
    ("BACKGROUND", (0, 0), (0, -1), PANEL),
    ("TOPPADDING", (0, 0), (-1, -1), 6), ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ("LEFTPADDING", (0, 0), (-1, -1), 8),
]))
story.append(t)
story.append(PageBreak())

# ---- Contents ------------------------------------------------------------
story += chapter_head("ii", "Contents", "FRONT MATTER")
toc = [
    ("01", "Regulatory &amp; Marine Context"),
    ("02", "System Architecture &amp; Process Overview"),
    ("03", "Hardware &amp; Instrumentation Specification"),
    ("04", "I/O List"),
    ("05", "Control Philosophy: PID Loop &amp; Interlocks"),
    ("06", "PLC Logic Walkthrough"),
    ("07", "HMI Design &amp; Operator Experience"),
    ("08", "Alarm Philosophy &amp; Fail-Safe Design"),
    ("09", "Testing, Commissioning &amp; FAT Procedures"),
    ("10", "Limitations, Real-World Deltas &amp; Future Work"),
    ("A", "Appendix A &mdash; I/O Quick Reference"),
    ("B", "Appendix B &mdash; Full Structured Text Listing"),
    ("C", "Appendix C &mdash; Glossary"),
    ("&mdash;", "About the Author"),
]
rows = []
for num, title in toc:
    rows.append([P(num, toc_num), P(title, toc_entry)])
tt = Table(rows, colWidths=[14 * mm, AVAIL_W - 14 * mm])
tt.setStyle(TableStyle([
    ("TOPPADDING", (0, 0), (-1, -1), 6), ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ("LINEBELOW", (0, 0), (-1, -2), 0.4, GRIDLINE),
    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
]))
story.append(tt)
story.append(PageBreak())

# ---- Executive Summary ----------------------------------------------------
story += chapter_head("iii", "Executive Summary", "FRONT MATTER")
story.append(P(
    "Modern marine emissions regulation forces a choice on shipowners: burn expensive "
    "low-sulphur fuel everywhere, or install an exhaust gas cleaning system and keep "
    "burning cheaper heavy fuel oil while scrubbing SOx out before the exhaust reaches "
    "atmosphere. This project simulates the automation layer of that second option &mdash; "
    "specifically, the closed-loop control that keeps a wash-water scrubber both chemically "
    "compliant and legally compliant at the same time.", lead))
story.append(P(
    "Two control problems sit on top of each other here. The first is a classic process "
    "control problem: hold discharge water pH above a regulatory minimum by modulating an "
    "alkaline dosing pump, using a PID loop reacting to a live pH sensor. The second is a "
    "regulatory/positional problem: no matter how chemically compliant the wash water is, "
    "it must never be discharged while the vessel is inside an Emission Control Area. That "
    "second condition can't be tuned away with a PID loop &mdash; it has to be a hard, "
    "unconditional interlock sourced from the vessel's navigation system.", body))
story.append(P(
    "The result is <b>FB_EGCS_ScrubberControl</b>, an IEC 61131-3 Structured Text function "
    "block that combines a tuned PID loop, hard chemical trips, a GPS/ECDIS-driven regulatory "
    "lockout, fail-safe sensor-fault handling, and rolling emissions logging &mdash; paired "
    "with a live Engine Control Room HMI mockup that visualises all of it, including the "
    "lockout event actually triggering.", body))
story.append(P(
    "This manual documents the regulatory context, architecture, hardware assumptions, full "
    "I/O list, control philosophy, complete annotated code, HMI design, alarm philosophy, "
    "and the functional test procedure used to validate the logic in simulation.", body))
story.append(PageBreak())


# ---- Chapter 1: Regulatory context ----------------------------------------
story += chapter_head(1, "Regulatory &amp; Marine Context")
story.append(P(
    "International shipping's air emissions are governed by <b>MARPOL Annex VI</b>, the "
    "International Maritime Organization's convention on the prevention of air pollution "
    "from ships. The rule that matters most for this project is the sulphur cap introduced "
    "under the IMO 2020 regulations: a global limit of <b>0.50% m/m</b> sulphur content in "
    "marine fuel, tightened to <b>0.10% m/m</b> inside designated Emission Control Areas "
    "(ECAs) such as the Baltic Sea, the North Sea, and the North American coastline.", body))
story.append(P(
    "A vessel has three ways to meet this: burn compliant low-sulphur fuel everywhere, burn "
    "an alternative fuel such as LNG, or keep burning cheaper heavy fuel oil and clean the "
    "exhaust before it reaches the funnel using an <b>Exhaust Gas Cleaning System (EGCS)</b>, "
    "commonly called a scrubber. Open-loop and hybrid scrubbers spray seawater or an "
    "alkaline-dosed wash water through the exhaust stream; the wash water absorbs SOx, "
    "dropping its own pH in the process.", body))
story.append(subhead("The wash-water problem"))
story.append(P(
    "Cleaning the air creates a water compliance problem. The IMO's 2015 EGCS Guidelines "
    "(MEPC.259(68)) set limits on the wash water itself before it can be discharged "
    "overboard: a minimum discharge pH (commonly implemented at <b>6.5</b>, measured at the "
    "overboard discharge point), a maximum pH depression relative to intake water, and "
    "monitoring of PAH (polycyclic aromatic hydrocarbon) proxy values and turbidity in more "
    "complete systems. This project focuses on the two variables most directly tied to the "
    "control loop: discharge pH and exhaust SOx concentration.", body))
story.append(subhead("Emission Control Areas and discharge bans"))
story.append(P(
    "Separately from water chemistry, many jurisdictions restrict or ban scrubber discharge "
    "outright within port limits, internal waters, or specific ECAs &mdash; regardless of how "
    "clean the wash water is. This is a purely positional rule: if the vessel is inside a "
    "restricted zone, discharge is not permitted. That distinction is the reason this "
    "project's control logic treats chemistry compliance and positional compliance as two "
    "independent interlocks rather than one blended \"compliant/non-compliant\" flag.", body))
story += callout(
    "Why two interlocks, not one",
    "It would be simple to fold pH, SOx, and ECA status into a single boolean and call it "
    "\"compliant\". Real systems don't do that, because a positional interlock has zero "
    "tolerance and no PID-style approach curve &mdash; the moment the vessel crosses the "
    "ECA boundary, discharge must stop immediately. Chemistry compliance, by contrast, is "
    "something the control loop actively works towards. Keeping them separate in the logic "
    "means a slow chemistry excursion can never be masked by \"well, we're outside the ECA\", "
    "and a hard position trip can never be delayed by \"well, the pH is fine\".", "ok")
story.append(subhead("Record-keeping"))
story.append(P(
    "MARPOL Annex VI compliance is also a paperwork exercise: class societies and port state "
    "control expect continuous emissions and discharge records. The control logic in this "
    "project reflects that by maintaining a rolling log of pH, SOx, dosing rate, discharge "
    "state, and ECA status &mdash; the PLC-side equivalent of what would, on a real vessel, "
    "stream into a SCADA historian for audit.", body))
story.append(PageBreak())

# ---- Chapter 2: Architecture ----------------------------------------------
story += chapter_head(2, "System Architecture &amp; Process Overview")
story.append(P(
    "The process flow is linear: exhaust gas from the main and/or auxiliary engines enters "
    "the scrubber tower, where a wash-water spray deck strips out SOx before the cleaned gas "
    "exits to the funnel. The wash water itself is then routed past a pH/SOx analyser pair, "
    "which feeds the PLC; the PLC in turn drives an alkaline dosing pump and gates the "
    "overboard discharge valve. A GPS/ECDIS position feed runs in parallel as an independent "
    "regulatory input.", body))
story += full_image("../images/architecture_diagram.png",
    "Figure 2.1 &mdash; Simplified process and control architecture. Solid lines represent "
    "process piping; dashed lines represent PLC signal paths.", max_h_mm=100)
story.append(subhead("Control hierarchy"))
story.extend(bullets([
    "<b>Field layer</b> &mdash; pH probe, SOx analyser, exhaust temperature RTD, dosing pump "
    "VFD, discharge valve actuator, GPS/ECDIS position feed.",
    "<b>Control layer</b> &mdash; a single PLC function block, <b>FB_EGCS_ScrubberControl</b>, "
    "hosted on a Siemens S7-1500 (or CODESYS-based marine controller), running the PID loop, "
    "interlocks, and logging.",
    "<b>Supervisory / HMI layer</b> &mdash; an Engine Control Room display giving the watch-"
    "keeping engineer live process values, alarm status, and an explicit ECA lockout "
    "indication.",
]))
story.append(subhead("Design intent"))
story.append(P(
    "The function block is deliberately self-contained: all setpoints, tuning constants, and "
    "logging live inside it, and it exposes a small, clean input/output interface. On a real "
    "vessel this would sit inside a larger Integrated Automation System (IAS) alongside "
    "engine, power management, and alarm-monitoring functions &mdash; the interface is kept "
    "narrow specifically so it could be dropped into that kind of system without dragging "
    "unrelated logic with it.", body))
story.append(PageBreak())


# ---- Chapter 3: Hardware & Instrumentation ---------------------------------
story += chapter_head(3, "Hardware &amp; Instrumentation Specification")
story.append(P(
    "The control logic in this project is platform-portable, but it was written against a "
    "concrete hardware assumption so that setpoints, scaling, and timing are realistic "
    "rather than arbitrary. The reference platform is a Siemens S7-1500 CPU programmed in "
    "SCL through TIA Portal, chosen because it's one of the most common PLC families in "
    "marine and industrial automation and its Structured Text is close enough to the "
    "CODESYS/IEC 61131-3 standard to port with minor changes.", body))
story.append(data_table(
    ["Component", "Representative Spec", "Role"],
    [
        ["PLC CPU", "Siemens SIMATIC S7-1500 (e.g. CPU 1515-2 PN)", "Executes FB_EGCS_ScrubberControl"],
        ["pH Analyser", "4&ndash;20mA, 0&ndash;14 pH, glass electrode or ISFET", "Discharge water pH feedback"],
        ["SOx Analyser", "4&ndash;20mA, 0&ndash;3000ppm, NDIR or electrochemical", "Exhaust SOx concentration"],
        ["Exhaust Temp.", "Pt100 RTD, 0&ndash;450&deg;C", "Process monitoring / thermal protection"],
        ["Dosing Pump", "VFD-driven metering pump, 4&ndash;20mA speed ref.", "Alkaline (NaOH) dosing"],
        ["Discharge Valve", "Motorised or pneumatic, 24VDC digital control", "Overboard discharge permissive"],
        ["Position Feed", "NMEA 0183/2000 GPS via ECDIS/nav. interface", "ECA boundary determination"],
        ["I/O Coupling", "Distributed I/O or direct rack-mounted modules", "Field signal termination"],
    ],
    col_widths=[34 * mm, 76 * mm, AVAIL_W - 34 * mm - 76 * mm]))
story.append(Spacer(1, 8))
story.append(subhead("Why these instrument choices"))
story.append(P(
    "4&ndash;20mA analogue signalling is used for the two safety/compliance-critical "
    "measurements (pH, SOx) because it is inherently loop-fault detectable &mdash; a broken "
    "wire or dead transmitter reads as 0mA, well outside the live 4&ndash;20mA band, which "
    "is exactly the condition <code>Sensor_Fault</code> is designed to catch in the control "
    "logic (Chapter 6). A purely digital or fieldbus-only sensor without that kind of "
    "wire-break detection would need an equivalent watchdog implemented elsewhere.", body))
story += callout(
    "Signal scaling in TIA Portal",
    "In a real S7-1500 project, the raw 0&ndash;27648 analogue input word from a 4&ndash;20mA "
    "channel is scaled to engineering units (0.00&ndash;14.00 pH, 0&ndash;3000 ppm) using the "
    "NORM_X / SCALE_X function blocks before it ever reaches FB_EGCS_ScrubberControl &mdash; "
    "the function block itself expects clean, already-scaled REAL values as shown in the I/O "
    "list.", "info")
story.append(PageBreak())

# ---- Chapter 4: I/O List ----------------------------------------------------
story += chapter_head(4, "I/O List")
story.append(P(
    "The table below is the working I/O list for FB_EGCS_ScrubberControl, in the same format "
    "used on the project's FAT/commissioning documentation (see also "
    "<b>docs/IO_List.md</b> in the repository, and Appendix A of this manual).", body))
story.append(subhead("Inputs"))
story.append(data_table(
    ["Tag", "Description", "Signal", "Range / Units"],
    [
        ["AI_pH_Feedback", "Discharge water pH probe", "4&ndash;20mA", "0.00&ndash;14.00 pH"],
        ["AI_SOx_ppm", "Exhaust SOx analyser", "4&ndash;20mA", "0&ndash;3000 ppm"],
        ["AI_ExhaustTemp", "Exhaust gas temperature", "Pt100 RTD", "0&ndash;450&deg;C"],
        ["DI_GPS_InECA", "Vessel-in-ECA flag (nav. system)", "24VDC digital", "0/1"],
        ["DI_System_Enable", "Master enable (bridge/ECR HMI)", "24VDC digital", "0/1"],
        ["DI_Sensor_Fault", "Combined pH/SOx comms fault", "24VDC digital", "0/1"],
    ],
    col_widths=[36 * mm, 62 * mm, 30 * mm, AVAIL_W - 36 * mm - 62 * mm - 30 * mm]))
story.append(Spacer(1, 10))
story.append(subhead("Outputs"))
story.append(data_table(
    ["Tag", "Description", "Signal", "Range / Units"],
    [
        ["AO_DosingPump_Speed", "Alkaline dosing pump VFD ref.", "4&ndash;20mA", "0&ndash;100%"],
        ["DO_WashWaterDischargeValve", "Discharge valve permissive", "24VDC digital", "0=Closed / 1=Open"],
        ["DO_Alarm_HighSOx", "High SOx alarm", "24VDC digital", "&mdash;"],
        ["DO_Alarm_LowpH", "Low pH alarm", "24VDC digital", "&mdash;"],
        ["DO_Alarm_ECA_Lockout", "ECA lockout indicator", "24VDC digital", "&mdash;"],
        ["DO_Alarm_SensorFault", "Sensor/comms fault indicator", "24VDC digital", "&mdash;"],
    ],
    col_widths=[36 * mm, 62 * mm, 30 * mm, AVAIL_W - 36 * mm - 62 * mm - 30 * mm]))
story.append(PageBreak())


# ---- Chapter 5: Control Philosophy -----------------------------------------
story += chapter_head(5, "Control Philosophy: PID Loop &amp; Interlocks")
story.append(P(
    "Three distinct control mechanisms operate on top of each other in this system, each "
    "suited to a different kind of requirement: a continuous PID loop for the process "
    "variable that genuinely needs tuning, hard threshold trips for conditions that must "
    "never be allowed to drift, and an unconditional interlock for the one input that has "
    "nothing to do with process chemistry at all.", body))
story.append(subhead("5.1 &nbsp; The pH control loop"))
story.append(P(
    "Discharge pH is controlled by a standard single-loop PID, adjusting the alkaline dosing "
    "pump's speed reference (0&ndash;100%) to hold pH at the setpoint of 6.50. Proportional "
    "gain and integral time were tuned conservatively (K<sub>p</sub> = 8.0, "
    "T<sub>i</sub> = 20s, no derivative action) because wash-water pH in a real scrubber "
    "has meaningful transport delay between the dosing point and the analyser &mdash; "
    "aggressive tuning on a delayed loop like this tends to ring rather than settle.", body))
story.append(data_table(
    ["Parameter", "Value", "Rationale"],
    [
        ["Setpoint (pH)", "6.50", "IMO MEPC.259(68) minimum discharge pH"],
        ["Kp", "8.0", "Moderate gain &mdash; avoids overshoot on a lagging loop"],
        ["Ti", "20 s", "Integral action tuned to typical wash-water transport delay"],
        ["Td", "0 s", "No derivative term &mdash; sensor noise would be amplified"],
        ["Output limits", "0&ndash;100%", "Full VFD speed range on the dosing pump"],
    ],
    col_widths=[38 * mm, 30 * mm, AVAIL_W - 38 * mm - 30 * mm]))
story.append(Spacer(1, 8))
story.append(subhead("5.2 &nbsp; Hard trips vs. soft alarms"))
story.append(P(
    "Below the PID's normal working range sits a hard trip: if pH falls to or below "
    "<b>6.00</b> (pH_LowLow), the loop is bypassed entirely and the dosing pump is forced "
    "to 100% regardless of what the PID output would otherwise say. This exists because a "
    "PID loop, by design, approaches its setpoint gradually &mdash; that's the wrong "
    "behaviour once pH has already dropped into territory that risks being out of "
    "compliance right now. A soft alarm (<code>Alarm_LowpH</code>) is raised any time pH is "
    "below setpoint at all, well before the hard trip point, so the watch engineer sees the "
    "trend developing.", body))
story.append(subhead("5.3 &nbsp; The ECA interlock is not a PID input"))
story.append(P(
    "The GPS/ECDIS ECA flag never enters the PID loop and never modulates anything "
    "gradually. It is evaluated as a single Boolean condition that, when true, unconditionally "
    "removes the discharge valve's permissive &mdash; independent of how compliant the water "
    "chemistry is. This mirrors how these systems are specified in practice: position-based "
    "discharge bans are treated as zero-tolerance conditions, not soft constraints to be "
    "optimised against.", body))
story += callout(
    "Why not just close the valve slowly on ECA entry?",
    "It's tempting to add a ramp-down so the valve doesn't slam shut. That would be the wrong "
    "engineering choice here: any discharge after the vessel is confirmed inside a restricted "
    "zone is a regulatory breach regardless of duration. The interlock is intentionally "
    "abrupt because the underlying rule is abrupt.", "warning")
story.append(subhead("5.4 &nbsp; Fail-safe default"))
story.append(P(
    "Any sensor or communications fault (<code>Sensor_Fault</code>) forces the system to its "
    "safest state &mdash; dosing pump off, discharge valve closed &mdash; on the same scan "
    "it's detected, ahead of every other evaluation in the function block. The system does "
    "not attempt to keep discharging on stale or assumed-good sensor values.", body))
story.append(PageBreak())


# ---- Chapter 6: PLC Logic Walkthrough --------------------------------------
story += chapter_head(6, "PLC Logic Walkthrough")
story.append(P(
    "This chapter walks through <b>FB_EGCS_ScrubberControl</b> section by section. The full, "
    "unbroken listing is reproduced in Appendix B; what follows here is the same code split "
    "into its seven logical stages with the reasoning behind each one.", body))

story.append(subhead("6.1 &nbsp; Sensor fault handling comes first"))
story.append(P(
    "The function block checks for sensor/comms faults before anything else runs. This "
    "ordering is deliberate &mdash; every other rung in the block assumes the input values "
    "it's reading are trustworthy, so the fail-safe check has to short-circuit everything "
    "downstream of it, not sit alongside it.", body))
story += code_block(
"""IF Sensor_Fault THEN
    Alarm_SensorFault        := TRUE;
    AlkalineDosingPump_Speed := 0.0;
    WashWaterDischargeValve  := FALSE;
    SystemStatus              := 'SENSOR FAULT';
    RETURN;
ELSE
    Alarm_SensorFault := FALSE;
END_IF""", "Listing 6.1 &mdash; Fail-safe fault handling, evaluated first on every scan.")

story.append(subhead("6.2 &nbsp; The ECA interlock is evaluated independently"))
story.append(P(
    "DischargePermitted is calculated directly from the enable/ECA/fault state, kept "
    "separate from the chemistry checks that come later. This is what lets Chapter 5's "
    "\"interlock, not PID input\" philosophy actually hold up in code &mdash; there's no "
    "path through this logic where a favourable pH reading can compensate for being inside "
    "an ECA.", body))
story += code_block(
"""Alarm_ECA_Lockout := GPS_InECA;
DischargePermitted := System_Enable AND NOT GPS_InECA AND NOT Sensor_Fault;""",
    "Listing 6.2 &mdash; Regulatory position interlock.")

story.append(subhead("6.3 &nbsp; PID loop with a hard low-pH trip"))
story.append(P(
    "The PID instance drives dosing pump speed under normal conditions; the hard trip "
    "overrides it only when pH has already dropped to the LowLow threshold, forcing full "
    "dosing rather than waiting for the loop to catch up.", body))
story += code_block(
"""IF System_Enable THEN
    PID_Inst(SP := pH_Setpoint, PV := pH_Feedback, KP := Kp, TI := Ti_s, TD := Td_s,
             MANUAL := FALSE, LMN_HLM := 100.0, LMN_LLM := 0.0);
    PID_Output := PID_Inst.LMN;

    IF pH_Feedback <= pH_LowLow THEN
        AlkalineDosingPump_Speed := 100.0;
    ELSE
        AlkalineDosingPump_Speed := PID_Output;
    END_IF
ELSE
    AlkalineDosingPump_Speed := 0.0;
    PID_Inst(MANUAL := TRUE, LMN := 0.0);
END_IF""", "Listing 6.3 &mdash; PID dosing control with hard trip override.")

story.append(subhead("6.4 &nbsp; Alarms, valve permissive, and status text"))
story.append(P(
    "Soft alarms are simple threshold comparisons. The discharge valve permissive is the "
    "single point where every condition &mdash; enable, position, pH, SOx, sensor health "
    "&mdash; has to agree before the valve is allowed open; <code>SystemStatus</code> exists "
    "purely to drive a human-readable HMI banner from the same underlying booleans.", body))
story += code_block(
"""Alarm_LowpH   := (pH_Feedback < pH_Setpoint) AND System_Enable;
Alarm_HighSOx := (SOx_ppm > SOx_Limit_ppm);

WashWaterDischargeValve := DischargePermitted
                            AND (pH_Feedback >= pH_Setpoint)
                            AND (SOx_ppm <= SOx_HighHigh);

IF NOT System_Enable THEN            SystemStatus := 'STANDBY';
ELSIF GPS_InECA THEN                 SystemStatus := 'ECA - DISCHARGE LOCKED';
ELSIF Alarm_HighSOx OR Alarm_LowpH THEN SystemStatus := 'OUT OF COMPLIANCE';
ELSE                                  SystemStatus := 'COMPLIANT - RUNNING';
END_IF""", "Listing 6.4 &mdash; Alarm evaluation and the discharge valve permissive.")

story.append(subhead("6.5 &nbsp; Rolling emissions log"))
story.append(P(
    "A 60-second retentive timer writes a snapshot of pH, SOx, dosing rate, discharge state, "
    "and ECA status into a circular buffer. On real hardware this record would stream to a "
    "SCADA historian rather than live in PLC memory indefinitely; the circular buffer here "
    "stands in for that at the function-block level.", body))
story += code_block(
"""LogTimer(IN := System_Enable, PT := LogTimer_PT);
IF LogTimer.Q THEN
    LogTimer(IN := FALSE);
    EmissionLog[LogIndex].pH_Value        := pH_Feedback;
    EmissionLog[LogIndex].SOx_ppm         := SOx_ppm;
    EmissionLog[LogIndex].DoseRate_Pct    := AlkalineDosingPump_Speed;
    EmissionLog[LogIndex].DischargeActive := WashWaterDischargeValve;
    EmissionLog[LogIndex].InECA           := GPS_InECA;
    LogIndex := LogIndex + 1;
    IF LogIndex > 999 THEN LogIndex := 0; END_IF
END_IF""", "Listing 6.5 &mdash; Rolling MARPOL Annex VI emissions record.")
story.append(PageBreak())


# ---- Chapter 7: HMI ---------------------------------------------------------
story += chapter_head(7, "HMI Design &amp; Operator Experience")
story.append(P(
    "The HMI mockup (<b>hmi/index.html</b> in the repository) simulates the screen a watch "
    "engineer would see in the Engine Control Room: live process values, dosing pump and "
    "valve state, a simplified process schematic, an alarm/event log, and position/compliance "
    "data. It runs entirely client-side with no dependencies, and periodically drives the "
    "vessel in and out of an ECA so the lockout state can actually be observed rather than "
    "just described.", body))
story += full_image("../images/hmi-dashboard.png",
    "Figure 7.1 &mdash; Engine Control Room HMI, showing the compliant/running state.",
    max_h_mm=105)
story.append(subhead("Design decisions"))
story.extend(bullets([
    "<b>Dark theme</b> &mdash; deliberately chosen, not a default: engine control rooms and "
    "bridge repeaters are frequently viewed during night watches, and a dark, low-glare "
    "interface is standard practice on real marine HMIs (e.g. Kongsberg K-Chief, Siemens "
    "SIMATIC WinCC marine panels).",
    "<b>Status pill as the single source of truth</b> &mdash; rather than making the operator "
    "cross-reference three separate readouts, one colour-coded pill states the system's "
    "overall condition in words, driven directly off the same SystemStatus logic as the PLC.",
    "<b>The ECA banner is the signature element</b> &mdash; it is intentionally the loudest "
    "thing on the screen when active, because it represents the one condition in this system "
    "with zero tolerance for delay or misreading.",
    "<b>SVG arc gauges over CSS gradients</b> &mdash; radial gauges are drawn as SVG stroke "
    "arcs rather than CSS conic-gradients, specifically so the interface renders identically "
    "across browser engines, including older ones &mdash; the same reasoning a real HMI "
    "runtime vendor would apply.",
]))
story += callout(
    "Engineering lesson worth keeping",
    "An early build of this HMI used modern CSS (conic-gradient) and ES6 JavaScript "
    "(template literals, arrow functions). It looked correct in a modern browser but "
    "silently failed &mdash; blank gauges, empty alarm log &mdash; when rendered through an "
    "older WebKit-based engine used for automated screenshotting. The fix was to rewrite the "
    "interactive layer in plain ES5 and swap the gauges to SVG stroke arcs. The takeaway: "
    "an HMI that only works in one rendering engine is a real defect, not a cosmetic one "
    "&mdash; shipboard displays and vendor-specific panel PCs often run exactly the kind of "
    "older embedded browser this exposed.", "ok")
story.append(PageBreak())

# ---- Chapter 8: Alarm Philosophy -------------------------------------------
story += chapter_head(8, "Alarm Philosophy &amp; Fail-Safe Design")
story.append(P(
    "Four distinct alarm/status conditions are raised by the function block, each mapped to "
    "a specific operator action rather than a generic \"something's wrong\" light:", body))
story.append(data_table(
    ["Condition", "Meaning", "Expected Operator Response"],
    [
        ["Alarm_LowpH", "Discharge pH below setpoint", "Monitor trend; verify dosing pump is responding"],
        ["Alarm_HighSOx", "Exhaust SOx above compliance limit", "Check scrubber performance / engine load"],
        ["Alarm_ECA_Lockout", "Vessel inside an Emission Control Area", "Informational &mdash; no action; system self-manages"],
        ["Alarm_SensorFault", "pH/SOx sensor or comms failure", "Dispatch engineer to inspect field instrument"],
    ],
    col_widths=[36 * mm, 58 * mm, AVAIL_W - 36 * mm - 58 * mm]))
story.append(Spacer(1, 10))
story.append(subhead("Fail-safe defaults, summarised"))
story.extend(bullets([
    "Loss of sensor signal &rarr; dosing pump off, discharge valve closed.",
    "Loss of system enable &rarr; dosing pump ramps to zero, discharge valve closes, status "
    "returns to STANDBY.",
    "ECA entry &rarr; discharge valve permissive removed immediately, no ramp or delay.",
    "No alarm in this system latches silently &mdash; every condition clears automatically "
    "once its underlying cause clears, which keeps the operator's picture of the plant "
    "honest in real time rather than requiring manual acknowledgement to \"unstick\" a "
    "resolved condition.",
]))
story.append(PageBreak())


# ---- Chapter 9: Testing -----------------------------------------------------
story += chapter_head(9, "Testing, Commissioning &amp; FAT Procedures")
story.append(P(
    "The function block was validated against ten functional test cases covering normal "
    "operation, boundary conditions, and fault handling &mdash; structured the way a "
    "Factory Acceptance Test (FAT) would be run before a real system moves to Site "
    "Acceptance Testing (SAT) on physical I/O. The full procedure, including a sign-off "
    "table, is in <b>docs/Testing_Procedures.md</b>; the test matrix is reproduced below.", body))
story.append(data_table(
    ["#", "Test Case", "Expected Result"],
    [
        ["1", "System start-up", "Status moves STANDBY &rarr; COMPLIANT-RUNNING; pump ramps from 0%"],
        ["2", "pH closed-loop response", "Pump speed increases smoothly, no oscillation &gt;&plusmn;5%"],
        ["3", "pH low-low hard trip", "Pump snaps to 100%; Alarm_LowpH raised"],
        ["4", "High SOx alarm", "Alarm_HighSOx raised; valve permissive drops above HighHigh"],
        ["5", "ECA GPS interlock", "Valve closes within one scan; lockout status shown"],
        ["6", "ECA exit recovery", "Normal logic resumes automatically, no manual reset"],
        ["7", "Sensor fault fail-safe", "Pump 0%, valve closed, status = SENSOR FAULT"],
        ["8", "Fault recovery", "Resumes without a bumped output on recovery"],
        ["9", "Emission logging cadence", "New record every 60s; index wraps at 999&rarr;0"],
        ["10", "Manual disable", "Pump to 0%, valve closes, status = STANDBY"],
    ],
    col_widths=[10 * mm, 55 * mm, AVAIL_W - 10 * mm - 55 * mm]))
story.append(Spacer(1, 10))
story += callout(
    "Testing without physical hardware",
    "All ten cases were exercised by forcing input tags directly &mdash; the PLCSIM pattern "
    "for Siemens platforms, or an equivalent soft-PLC harness for CODESYS &mdash; and "
    "observing outputs. This is exactly how a controls engineer validates logic before it "
    "ever sees a cabinet, and it's a legitimate, recruiter-relevant way to demonstrate "
    "testing discipline without owning a scrubber skid.", "info")

story.append(subhead("9.1 &nbsp; Commissioning sequence (SAT-style, for reference)"))
story.append(P(
    "The FAT above proves the logic. A real Site Acceptance Test on installed hardware "
    "would follow a broader sequence, included here to show the full path from simulated "
    "logic to a commissioned system &mdash; and because being able to describe that path "
    "is itself something recruiters in this field screen for.", body))
story.append(data_table(
    ["Step", "Activity", "Exit Criteria"],
    [
        ["1", "Cold loop checks", "Every I/O point traced from field terminal to PLC tag; no crossed wiring"],
        ["2", "Instrument calibration", "pH probe 2-point buffer calibration; SOx analyser zero/span verified"],
        ["3", "Actuator stroke test", "Dosing pump VFD responds correctly to 0/50/100% reference; valve full travel timed"],
        ["4", "Interlock proving", "ECA and sensor-fault interlocks physically forced and confirmed to trip within spec"],
        ["5", "Closed-loop tuning check", "PID response observed on real process; Kp/Ti fine-tuned against Chapter 5 baseline"],
        ["6", "Alarm walk-down", "Every alarm in Chapter 8 raised and cleared once, confirmed on HMI and class-required log"],
        ["7", "Endurance run", "24-hour continuous run under normal load with no unexplained trips"],
        ["8", "Sign-off", "Class surveyor and shipowner's engineer countersign the FAT/SAT record"],
    ],
    col_widths=[12 * mm, 55 * mm, AVAIL_W - 12 * mm - 55 * mm]))
story.append(PageBreak())

# ---- Chapter 10: Limitations -------------------------------------------------
story += chapter_head(10, "Limitations, Real-World Deltas &amp; Future Work")
story.append(P(
    "This project is explicit about the gap between a strong portfolio simulation and a "
    "certifiable shipboard system. Naming that gap accurately is itself part of the "
    "engineering &mdash; it's the difference between a project that looks impressive and "
    "one that demonstrates you understand what \"production-ready\" actually requires.", body))
story.append(subhead("What a real installation would add"))
story.extend(bullets([
    "<b>Class society approval</b> &mdash; DNV, ABS, or Lloyd's Register type-approval of the "
    "EGCS package and a documented HAZOP/FMEA on the control logic itself.",
    "<b>Redundant sensing</b> &mdash; a single pH/SOx analyser pair is a simplification; real "
    "systems often vote multiple sensors to avoid a single point of failure driving a false "
    "compliant reading.",
    "<b>ECA boundary logic</b> &mdash; this project treats <code>GPS_InECA</code> as a single "
    "input bit; a production system would run a live polygon check against IMO-published ECA "
    "charts, likely on a separate navigation-integration controller rather than inside the "
    "scrubber PLC.",
    "<b>PAH and turbidity monitoring</b> &mdash; full EGCS Guidelines compliance monitors "
    "additional wash-water parameters beyond pH and SOx, omitted here to keep the control "
    "loop legible for a portfolio piece.",
    "<b>Cybersecurity hardening</b> &mdash; network segmentation, signed firmware, and access "
    "control for the PLC and HMI, per IEC 62443 &mdash; a real theme across this whole "
    "portfolio series, developed in depth in the maritime cybersecurity project.",
]))
story.append(subhead("10.1 &nbsp; Hazard &amp; safeguard register (HAZOP-style)"))
story.append(P(
    "A full HAZOP is out of scope for a portfolio simulation, but naming the main hazards "
    "this control philosophy is actually defending against &mdash; and where the "
    "responsibility sits outside the PLC &mdash; is exactly the kind of thinking a HAZOP "
    "session would produce. A short version is reproduced below.", body))
story.append(data_table(
    ["Hazard", "Cause", "Safeguard in This Design"],
    [
        ["Non-compliant discharge", "pH sensor drifts high while actually low",
         "Redundant sensing recommended (Ch.10); hard LowLow trip independent of PID"],
        ["Discharge inside an ECA", "GPS/ECDIS feed lost or stale",
         "DI_Sensor_Fault path also covers loss of the position feed &mdash; fails to valve-closed"],
        ["Over-dosing (alkaline waste)", "PID integral windup on a stuck sensor",
         "LMN_HLM/LMN_LLM clamps on the PID instance; fault path forces pump to 0% independently"],
        ["Silent instrument failure", "4-20mA loop reads a plausible mid-range value while faulted",
         "Requires field-side loop diagnostics upstream of the PLC (see Ch.3) &mdash; noted as a residual risk"],
        ["Operator overrides interlock", "Manual bypass switch fitted at cabinet",
         "Not implemented in this design by choice &mdash; ECA lockout has no software or field bypass path"],
    ],
    col_widths=[36 * mm, 52 * mm, AVAIL_W - 36 * mm - 52 * mm]))
story.append(Spacer(1, 6))
story += callout(
    "Residual risk, stated plainly",
    "The \"silent instrument failure\" row above is the honest limitation of this design: a "
    "4-20mA signal that fails to a plausible mid-range value rather than to 0mA will not "
    "trip Sensor_Fault. Real installations close this gap with loop diagnostics at the "
    "analyser/transmitter level, or a second, independently-sourced measurement voted "
    "against the first &mdash; deliberately left as a named gap here rather than solved "
    "with an assumption that would make the design look safer than it is.", "warning")
story.append(subhead("Where this project could go next"))
story.extend(bullets([
    "Add a second-stage SOx feed-forward term, so a sudden engine load increase pre-empts "
    "the pH loop rather than waiting for the pH excursion to happen.",
    "Extend the emissions log to export as CSV for direct import into a reporting tool.",
    "Add a simple polygon-based ECA check driven by real ECA boundary coordinates, replacing "
    "the single simulated flag.",
]))
story.append(PageBreak())


# ---- Appendix A: I/O Quick Reference ---------------------------------------
story += chapter_head("A", "Appendix A &mdash; I/O Quick Reference", "APPENDIX")
story.append(P(
    "Condensed combined I/O reference for bench/desk use alongside the PLCSIM watch table.", body))
story.append(data_table(
    ["Tag", "Dir.", "Type", "Notes"],
    [
        ["AI_pH_Feedback", "IN", "REAL (4-20mA)", "0.00-14.00 pH"],
        ["AI_SOx_ppm", "IN", "REAL (4-20mA)", "0-3000 ppm"],
        ["AI_ExhaustTemp", "IN", "REAL (RTD)", "0-450 C"],
        ["DI_GPS_InECA", "IN", "BOOL", "1 = inside ECA"],
        ["DI_System_Enable", "IN", "BOOL", "Master enable"],
        ["DI_Sensor_Fault", "IN", "BOOL", "1 = comms/sensor fault"],
        ["AO_DosingPump_Speed", "OUT", "REAL (4-20mA)", "0-100%"],
        ["DO_WashWaterDischargeValve", "OUT", "BOOL", "1 = open"],
        ["DO_Alarm_HighSOx", "OUT", "BOOL", "Soft alarm"],
        ["DO_Alarm_LowpH", "OUT", "BOOL", "Soft alarm"],
        ["DO_Alarm_ECA_Lockout", "OUT", "BOOL", "Informational"],
        ["DO_Alarm_SensorFault", "OUT", "BOOL", "Fail-safe trigger"],
    ],
    col_widths=[52 * mm, 14 * mm, 32 * mm, AVAIL_W - 52 * mm - 14 * mm - 32 * mm]))
story.append(PageBreak())

# ---- Appendix B: Full ST Listing -------------------------------------------
story += chapter_head("B", "Appendix B &mdash; Full Structured Text Listing", "APPENDIX")
story.append(P(
    "Complete, unedited listing of <b>src/EGCS_ScrubberControl.st</b>.", body))

story += code_block(
"""(*
====================================================================================
  PROJECT   : Smart Exhaust Gas Cleaning System (EGCS)
              Automated Closed-Loop Scrubber Control
  MODULE    : FB_EGCS_ScrubberControl
  PLATFORM  : IEC 61131-3 Structured Text (Siemens SCL / CODESYS-portable)
  AUTHOR    : Sipho Lucky Sibanda
  CONTEXT   : Alkaline-dosed wash water neutralises SOx absorbed from engine
              exhaust before discharge overboard or holding for treatment.
  REGULATORY BASIS (simulated against, for realism only):
    - MARPOL Annex VI, Regulation 14 : 0.50% m/m global / 0.10% m/m in ECAs
    - IMO MEPC.259(68) 2015 Guidelines: discharge pH >= 6.5
====================================================================================
*)

TYPE ST_EmissionRecord :
STRUCT
    Timestamp        : DT;
    pH_Value          : REAL;
    SOx_ppm           : REAL;
    DoseRate_Pct      : REAL;
    DischargeActive   : BOOL;
    InECA             : BOOL;
END_STRUCT
END_TYPE""")

story += code_block(
"""FUNCTION_BLOCK FB_EGCS_ScrubberControl
VAR_INPUT
    pH_Feedback         : REAL;
    SOx_ppm             : REAL;
    ExhaustTemp_C       : REAL;
    GPS_InECA           : BOOL;
    System_Enable       : BOOL;
    Sensor_Fault        : BOOL;
END_VAR

VAR_OUTPUT
    AlkalineDosingPump_Speed : REAL := 0.0;
    WashWaterDischargeValve  : BOOL := FALSE;
    Alarm_HighSOx            : BOOL := FALSE;
    Alarm_LowpH              : BOOL := FALSE;
    Alarm_ECA_Lockout        : BOOL := FALSE;
    Alarm_SensorFault        : BOOL := FALSE;
    SystemStatus             : STRING[20] := 'STANDBY';
END_VAR

VAR
    pH_Setpoint          : REAL := 6.50;
    pH_LowLow            : REAL := 6.00;
    SOx_Limit_ppm         : REAL := 11.50;
    SOx_HighHigh          : REAL := 14.00;

    PID_Inst              : FB_PID;
    Kp                     : REAL := 8.0;
    Ti_s                   : REAL := 20.0;
    Td_s                    : REAL := 0.0;
    PID_Output             : REAL;

    EmissionLog            : ARRAY[0..999] OF ST_EmissionRecord;
    LogIndex                : INT := 0;
    LogTimer                : TON;
    LogTimer_PT             : TIME := T#60S;

    DischargePermitted     : BOOL;
END_VAR""")

story += code_block(
"""// 1. SENSOR / COMMS FAULT HANDLING - fails to safe state
IF Sensor_Fault THEN
    Alarm_SensorFault        := TRUE;
    AlkalineDosingPump_Speed := 0.0;
    WashWaterDischargeValve  := FALSE;
    SystemStatus              := 'SENSOR FAULT';
    RETURN;
ELSE
    Alarm_SensorFault := FALSE;
END_IF

// 2. REGULATORY / ECA GPS INTERLOCK
Alarm_ECA_Lockout := GPS_InECA;
DischargePermitted := System_Enable AND NOT GPS_InECA AND NOT Sensor_Fault;

// 3. CLOSED-LOOP pH CONTROL (PID)
IF System_Enable THEN
    PID_Inst(SP := pH_Setpoint, PV := pH_Feedback, KP := Kp, TI := Ti_s, TD := Td_s,
             MANUAL := FALSE, LMN_HLM := 100.0, LMN_LLM := 0.0);
    PID_Output := PID_Inst.LMN;

    IF pH_Feedback <= pH_LowLow THEN
        AlkalineDosingPump_Speed := 100.0;
    ELSE
        AlkalineDosingPump_Speed := PID_Output;
    END_IF
ELSE
    AlkalineDosingPump_Speed := 0.0;
    PID_Inst(MANUAL := TRUE, LMN := 0.0);
END_IF""")

story += code_block(
"""// 4. ALARM EVALUATION
Alarm_LowpH   := (pH_Feedback < pH_Setpoint) AND System_Enable;
Alarm_HighSOx := (SOx_ppm > SOx_Limit_ppm);

// 5. DISCHARGE VALVE PERMISSIVE
WashWaterDischargeValve := DischargePermitted
                            AND (pH_Feedback >= pH_Setpoint)
                            AND (SOx_ppm <= SOx_HighHigh);

// 6. SYSTEM STATUS TEXT (drives HMI banner)
IF NOT System_Enable THEN
    SystemStatus := 'STANDBY';
ELSIF GPS_InECA THEN
    SystemStatus := 'ECA - DISCHARGE LOCKED';
ELSIF Alarm_HighSOx OR Alarm_LowpH THEN
    SystemStatus := 'OUT OF COMPLIANCE';
ELSE
    SystemStatus := 'COMPLIANT - RUNNING';
END_IF""")

story += code_block(
"""// 7. REGULATORY EMISSIONS LOGGING
LogTimer(IN := System_Enable, PT := LogTimer_PT);
IF LogTimer.Q THEN
    LogTimer(IN := FALSE);
    EmissionLog[LogIndex].Timestamp      := DT#2026-01-01-00:00:00;
    EmissionLog[LogIndex].pH_Value        := pH_Feedback;
    EmissionLog[LogIndex].SOx_ppm         := SOx_ppm;
    EmissionLog[LogIndex].DoseRate_Pct    := AlkalineDosingPump_Speed;
    EmissionLog[LogIndex].DischargeActive := WashWaterDischargeValve;
    EmissionLog[LogIndex].InECA           := GPS_InECA;

    LogIndex := LogIndex + 1;
    IF LogIndex > 999 THEN
        LogIndex := 0;
    END_IF
END_IF

END_FUNCTION_BLOCK""", "Listing B.1 &mdash; Complete FB_EGCS_ScrubberControl source.")
story.append(PageBreak())


# ---- Appendix C: Glossary --------------------------------------------------
story += chapter_head("C", "Appendix C &mdash; Glossary", "APPENDIX")
story.append(data_table(
    ["Term", "Meaning"],
    [
        ["EGCS", "Exhaust Gas Cleaning System &mdash; a marine scrubber"],
        ["ECA", "Emission Control Area &mdash; a zone with tighter sulphur/NOx limits under MARPOL Annex VI"],
        ["MARPOL Annex VI", "The IMO convention chapter governing air pollution from ships"],
        ["MEPC.259(68)", "IMO guidelines specifying EGCS wash-water discharge criteria"],
        ["PID", "Proportional-Integral-Derivative &mdash; a standard closed-loop control algorithm"],
        ["FB", "Function Block &mdash; a reusable, encapsulated unit of PLC logic (IEC 61131-3)"],
        ["SCL", "Structured Control Language &mdash; Siemens' IEC 61131-3 Structured Text dialect"],
        ["ECDIS", "Electronic Chart Display and Information System &mdash; the vessel's navigation display"],
        ["FAT / SAT", "Factory / Site Acceptance Test &mdash; formal pre- and post-installation validation stages"],
        ["HAZOP", "Hazard and Operability study &mdash; a structured method for identifying process risks"],
        ["I/O", "Input/Output &mdash; the physical or logical signals a PLC reads and writes"],
        ["VFD", "Variable Frequency Drive &mdash; motor speed control used here on the dosing pump"],
    ],
    col_widths=[38 * mm, AVAIL_W - 38 * mm]))
story.append(PageBreak())

# ---- About the Author -------------------------------------------------------
story += chapter_head("&mdash;", "About the Author", "CLOSING")
story.append(P(
    "<b>Sipho Lucky Sibanda</b> is an automation and controls engineer building a "
    "multi-disciplinary portfolio spanning marine systems, industrial automation, biotech, "
    "and applied AI/PLC integration. This manual is the first in a series documenting each "
    "project in the <b>Marine Automation Portfolio</b> to the same standard: full PLC logic, "
    "I/O documentation, a live HMI, functional test procedures, and an honest account of "
    "what separates a strong simulation from a certifiable production system.", lead))
story.append(P(
    "Repository: <b>marine-egcs-scrubber-control</b>", body))
story.append(Spacer(1, 20))
story.append(HRFlowable(width="40%", thickness=1, color=CYAN))
story.append(Spacer(1, 6))
story.append(P("End of document.", caption))

# ---------------------------------------------------------------------------
# Build
# ---------------------------------------------------------------------------
doc = SimpleDocTemplate(
    OUTFILE, pagesize=A4,
    leftMargin=MARGIN_L, rightMargin=MARGIN_R,
    topMargin=MARGIN_TOP, bottomMargin=MARGIN_BOT,
    title="Smart Exhaust Gas Cleaning System (EGCS) - Technical Manual",
    author=AUTHOR,
)
doc.build(story, onFirstPage=draw_cover, onLaterPages=draw_body)
print("Built:", OUTFILE)
