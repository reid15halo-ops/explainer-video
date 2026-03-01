#!/usr/bin/env python3
"""
FreyAI Visions — Erklärvideo Generator
Erstellt ein professionelles Slideshow-Erklärvideo mit Animationen.
"""

import os
import math
from PIL import Image, ImageDraw, ImageFont

# === CONFIG ===
W, H = 1920, 1080
FPS = 30
OUT_DIR = "/home/openclaw/workspace/projects/explainer-video"
FRAMES_DIR = os.path.join(OUT_DIR, "frames")
OUTPUT_FILE = os.path.join(OUT_DIR, "freyai-visions-erklaervideo.mp4")

# Brand Colors
BG_DARK = (26, 26, 46)        # #1a1a2e
BG_CARD = (28, 28, 33)        # #1c1c21
TEAL = (13, 148, 136)         # #0d9488
TEAL_LIGHT = (94, 236, 198)   # #5eecc6
WHITE = (228, 228, 231)       # #e4e4e7
GRAY = (161, 161, 170)        # #a1a1aa
MUTED = (113, 113, 122)       # #71717a
RED = (239, 68, 68)           # #ef4444
AMBER = (245, 158, 11)        # #f59e0b
GREEN = (34, 197, 94)         # #22c55e
INDIGO = (99, 102, 241)       # #6366f1

# Fonts
FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

os.makedirs(FRAMES_DIR, exist_ok=True)

def get_font(size, bold=False):
    return ImageFont.truetype(FONT_BOLD if bold else FONT_REG, size)

def draw_gradient_bg(draw, w, h, color_top, color_bottom):
    for y in range(h):
        r = int(color_top[0] + (color_bottom[0] - color_top[0]) * y / h)
        g = int(color_top[1] + (color_bottom[1] - color_top[1]) * y / h)
        b = int(color_top[2] + (color_bottom[2] - color_top[2]) * y / h)
        draw.line([(0, y), (w, y)], fill=(r, g, b))

def draw_rounded_rect(draw, xy, fill, radius=20, outline=None, outline_width=0):
    x0, y0, x1, y1 = xy
    draw.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=outline_width)

def draw_centered_text(draw, y, text, font, fill=WHITE, w=W):
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    draw.text(((w - tw) // 2, y), text, font=font, fill=fill)

def draw_multiline_centered(draw, y, lines, font, fill=WHITE, spacing=10):
    for line in lines:
        draw_centered_text(draw, y, line, font, fill)
        bbox = draw.textbbox((0, 0), line, font=font)
        y += (bbox[3] - bbox[1]) + spacing
    return y

def ease_in_out(t):
    """Smooth ease in-out curve."""
    return t * t * (3 - 2 * t)

def lerp(a, b, t):
    return int(a + (b - a) * t)

def lerp_color(c1, c2, t):
    return tuple(lerp(c1[i], c2[i], t) for i in range(3))

def draw_progress_bar(draw, y, progress, label=""):
    bar_w = 600
    bar_h = 12
    x = (W - bar_w) // 2
    draw.rounded_rectangle([x, y, x + bar_w, y + bar_h], radius=6, fill=(40, 40, 50))
    fill_w = int(bar_w * progress)
    if fill_w > 0:
        draw.rounded_rectangle([x, y, x + fill_w, y + bar_h], radius=6, fill=TEAL)
    if label:
        font = get_font(16)
        draw_centered_text(draw, y + bar_h + 6, label, font, MUTED)

# ============================================================
# SLIDE DEFINITIONS
# ============================================================

def make_slide_intro(frame_i, total_frames):
    """Slide 1: Logo + Titel — FreyAI Visions"""
    img = Image.new("RGB", (W, H))
    draw = ImageDraw.Draw(img)
    draw_gradient_bg(draw, W, H, (10, 10, 30), (26, 26, 46))

    t = frame_i / max(total_frames - 1, 1)

    # Animated glow circle behind logo
    glow_r = 180 + int(20 * math.sin(t * math.pi * 2))
    cx, cy = W // 2, 320
    for r in range(glow_r, 0, -2):
        alpha = max(0, min(255, int(30 * (1 - r / glow_r))))
        c = lerp_color(BG_DARK, TEAL, 0.15 * (1 - r / glow_r))
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=c)

    # Logo
    try:
        logo = Image.open("/home/openclaw/workspace/projects/instagram-campaign/assets/logo-square-freyja.png")
        logo = logo.resize((240, 240), Image.LANCZOS)
        if logo.mode == "RGBA":
            img.paste(logo, (cx - 120, cy - 120), logo)
        else:
            img.paste(logo, (cx - 120, cy - 120))
    except:
        draw.ellipse([cx - 100, cy - 100, cx + 100, cy + 100], fill=TEAL)

    # Text fade in
    alpha_t = ease_in_out(min(1, t * 2))
    title_color = lerp_color(BG_DARK, WHITE, alpha_t)
    sub_color = lerp_color(BG_DARK, TEAL_LIGHT, alpha_t)

    font_title = get_font(72, bold=True)
    font_sub = get_font(32)
    draw_centered_text(draw, 480, "FreyAI Visions", font_title, title_color)
    draw_centered_text(draw, 570, "Die All-in-One Business-App", font_sub, sub_color)
    draw_centered_text(draw, 615, "für deutsche Handwerksbetriebe", font_sub, sub_color)

    # Tagline
    if t > 0.4:
        tag_t = ease_in_out(min(1, (t - 0.4) / 0.3))
        tag_color = lerp_color(BG_DARK, GRAY, tag_t)
        font_tag = get_font(24)
        draw_centered_text(draw, 700, "Weniger Bürokram. Mehr Handwerk.", font_tag, tag_color)

    return img


def make_slide_problem(frame_i, total_frames):
    """Slide 2: Das Problem — 20+ Stunden Papierkram"""
    img = Image.new("RGB", (W, H))
    draw = ImageDraw.Draw(img)
    draw_gradient_bg(draw, W, H, (30, 10, 10), (26, 26, 46))

    t = frame_i / max(total_frames - 1, 1)

    # Header
    font_h = get_font(52, bold=True)
    font_sub = get_font(28)
    draw_centered_text(draw, 60, "Das Problem", font_h, RED)

    # Big number animation
    hours = int(20 * ease_in_out(min(1, t * 1.5)))
    font_big = get_font(160, bold=True)
    draw_centered_text(draw, 150, f"{hours}+", font_big, RED)
    font_unit = get_font(36, bold=True)
    draw_centered_text(draw, 340, "Stunden pro Monat", font_unit, AMBER)
    draw_centered_text(draw, 390, "verschwendet mit Papierkram", font_sub, GRAY)

    # Pain points - slide in from left
    pain_points = [
        ("📝", "Angebote schreiben", "Jedes Mal von vorne anfangen"),
        ("🧾", "Rechnungen erstellen", "Manuell tippen, Fehler korrigieren"),
        ("📞", "Kunden nachfassen", "Wer hat noch nicht geantwortet?"),
        ("⚠️", "Mahnungen verschicken", "Peinlich und zeitaufwändig"),
    ]

    font_item = get_font(26, bold=True)
    font_desc = get_font(20)
    start_y = 480
    for i, (icon, title, desc) in enumerate(pain_points):
        item_t = ease_in_out(max(0, min(1, (t - 0.2 - i * 0.12) / 0.2)))
        x_offset = int((1 - item_t) * -400)
        alpha = item_t

        y = start_y + i * 100
        x = 350 + x_offset

        if alpha > 0:
            item_color = lerp_color(BG_DARK, WHITE, alpha)
            desc_color = lerp_color(BG_DARK, GRAY, alpha)

            # Card background
            draw_rounded_rect(draw, [x - 20, y - 10, x + 1200, y + 70],
                            fill=lerp_color(BG_DARK, (40, 30, 30), alpha), radius=12)
            draw.text((x, y), icon, font=get_font(36), fill=item_color)
            draw.text((x + 60, y + 5), title, font=font_item, fill=item_color)
            draw.text((x + 60, y + 40), desc, font=font_desc, fill=desc_color)

    return img


def make_slide_solution(frame_i, total_frames):
    """Slide 3: Die Lösung — Automatisierter Workflow"""
    img = Image.new("RGB", (W, H))
    draw = ImageDraw.Draw(img)
    draw_gradient_bg(draw, W, H, (10, 26, 26), (26, 26, 46))

    t = frame_i / max(total_frames - 1, 1)

    font_h = get_font(52, bold=True)
    draw_centered_text(draw, 50, "Die Lösung", font_h, TEAL_LIGHT)

    font_sub = get_font(28)
    draw_centered_text(draw, 120, "Ein automatisierter Workflow — von A bis Z", font_sub, GRAY)

    # Workflow steps as connected cards
    steps = [
        ("1", "Kundenanfrage", "Kommt rein per\nE-Mail, Telefon, Web", TEAL),
        ("2", "Angebot", "KI erstellt\nautomatisch", INDIGO),
        ("3", "Auftrag", "Bestätigt →\nKanban-Board", GREEN),
        ("4", "Rechnung", "Automatisch\ngeneriert & versendet", AMBER),
    ]

    card_w = 340
    card_h = 200
    start_x = (W - (4 * card_w + 3 * 40)) // 2
    y = 240

    for i, (num, title, desc, color) in enumerate(steps):
        step_t = ease_in_out(max(0, min(1, (t - i * 0.15) / 0.25)))

        x = start_x + i * (card_w + 40)
        card_y = y + int((1 - step_t) * 80)
        alpha = step_t

        if alpha > 0:
            # Card
            card_color = lerp_color(BG_DARK, (35, 35, 45), alpha)
            border_color = lerp_color(BG_DARK, color, alpha)
            draw_rounded_rect(draw, [x, card_y, x + card_w, card_y + card_h],
                            fill=card_color, radius=16, outline=border_color, outline_width=2)

            # Number circle
            cx = x + 40
            cy_circle = card_y + 40
            num_color = lerp_color(BG_DARK, color, alpha)
            draw.ellipse([cx - 22, cy_circle - 22, cx + 22, cy_circle + 22], fill=num_color)
            num_font = get_font(24, bold=True)
            draw_centered_text(draw, cy_circle - 14, num, num_font, WHITE, w=(cx + 22) * 2 - (cx - 22))
            nbbox = draw.textbbox((0, 0), num, font=num_font)
            nw = nbbox[2] - nbbox[0]
            draw.text((cx - nw // 2, cy_circle - 14), num, font=num_font, fill=WHITE)

            # Title
            title_font = get_font(28, bold=True)
            title_color = lerp_color(BG_DARK, WHITE, alpha)
            draw.text((x + 75, card_y + 25), title, font=title_font, fill=title_color)

            # Description
            desc_font = get_font(20)
            desc_color = lerp_color(BG_DARK, GRAY, alpha)
            draw.text((x + 20, card_y + 80), desc, font=desc_font, fill=desc_color)

            # Arrow between cards
            if i < 3 and step_t > 0.8:
                arrow_x = x + card_w + 5
                arrow_y = card_y + card_h // 2
                arrow_color = lerp_color(BG_DARK, TEAL, alpha)
                draw.polygon([(arrow_x, arrow_y - 12), (arrow_x + 25, arrow_y),
                            (arrow_x, arrow_y + 12)], fill=arrow_color)

    # Bottom section: Swipe approve animation
    if t > 0.6:
        swipe_t = ease_in_out(min(1, (t - 0.6) / 0.3))
        swipe_color = lerp_color(BG_DARK, WHITE, swipe_t)

        # Phone mockup
        phone_x = W // 2 - 150
        phone_y = 520
        phone_w = 300
        phone_h = 380
        draw_rounded_rect(draw, [phone_x, phone_y, phone_x + phone_w, phone_y + phone_h],
                        fill=(30, 30, 40), radius=24, outline=MUTED, outline_width=2)

        # Screen content
        screen_x = phone_x + 15
        screen_y = phone_y + 40
        draw_rounded_rect(draw, [screen_x, screen_y, screen_x + 270, screen_y + 120],
                        fill=(35, 35, 50), radius=12)
        draw.text((screen_x + 15, screen_y + 10), "Rechnung #2024-087", font=get_font(20, bold=True), fill=swipe_color)
        draw.text((screen_x + 15, screen_y + 40), "Mueller Heizung GmbH", font=get_font(17), fill=lerp_color(BG_DARK, GRAY, swipe_t))
        draw.text((screen_x + 15, screen_y + 65), "€ 4.350,00", font=get_font(28, bold=True), fill=lerp_color(BG_DARK, GREEN, swipe_t))

        # Swipe indicator
        swipe_x_offset = int(80 * math.sin(t * math.pi * 3)) if t > 0.7 else 0
        arrow_cx = phone_x + phone_w // 2 + swipe_x_offset
        arrow_cy = phone_y + phone_h - 80

        # Swipe arrow
        arr_color = lerp_color(BG_DARK, GREEN, swipe_t)
        draw.text((arrow_cx - 40, arrow_cy), "→ Wischen", font=get_font(22, bold=True), fill=arr_color)

        # Labels
        label_font = get_font(18)
        draw.text((phone_x - 80, arrow_cy), "✕", font=get_font(32, bold=True), fill=lerp_color(BG_DARK, RED, swipe_t))
        draw.text((phone_x + phone_w + 40, arrow_cy), "✓", font=get_font(32, bold=True), fill=lerp_color(BG_DARK, GREEN, swipe_t))

        # 95/5 Label
        if t > 0.8:
            label_t = ease_in_out(min(1, (t - 0.8) / 0.15))
            draw_centered_text(draw, phone_y + phone_h + 20, "95/5-Prinzip: KI macht 95% — Du kontrollierst 5%",
                             get_font(26, bold=True), lerp_color(BG_DARK, TEAL_LIGHT, label_t))

    return img


def make_slide_features(frame_i, total_frames):
    """Slide 4: Alleinstellungsmerkmale"""
    img = Image.new("RGB", (W, H))
    draw = ImageDraw.Draw(img)
    draw_gradient_bg(draw, W, H, (15, 15, 35), (26, 26, 46))

    t = frame_i / max(total_frames - 1, 1)

    font_h = get_font(48, bold=True)
    draw_centered_text(draw, 50, "Was FreyAI Visions besonders macht", font_h, WHITE)

    features = [
        ("📴", "Offline-fähig", "Funktioniert auf der Baustelle\nauch ohne Internet", TEAL),
        ("🔒", "DSGVO-konform", "EU-Server, Verschlüsselung,\nDatenportabilität (Art. 20)", INDIGO),
        ("📊", "DATEV-Export", "Direkter Export für den\nSteuerberater — kein Abtippen", GREEN),
        ("🧾", "E-Rechnung", "XRechnung 3.0 & ZUGFeRD 2.2\nab 2025 Pflicht — wir sind bereit", AMBER),
        ("🤖", "KI-gestützt", "Gemini AI schreibt Angebote,\nerstellt Rechnungen, mahnt", TEAL_LIGHT),
        ("💰", "Keine Abo-Falle", "Faire Preise, kein Lock-In,\ndeine Daten gehören dir", GREEN),
    ]

    cols = 3
    card_w = 520
    card_h = 200
    gap_x = 40
    gap_y = 30
    start_x = (W - (cols * card_w + (cols - 1) * gap_x)) // 2
    start_y = 160

    for i, (icon, title, desc, color) in enumerate(features):
        col = i % cols
        row = i // cols

        item_t = ease_in_out(max(0, min(1, (t - i * 0.08) / 0.2)))

        x = start_x + col * (card_w + gap_x)
        y = start_y + row * (card_h + gap_y) + int((1 - item_t) * 40)

        if item_t > 0:
            card_bg = lerp_color(BG_DARK, (35, 35, 50), item_t)
            border = lerp_color(BG_DARK, color, item_t * 0.6)
            draw_rounded_rect(draw, [x, y, x + card_w, y + card_h],
                            fill=card_bg, radius=16, outline=border, outline_width=2)

            icon_color = lerp_color(BG_DARK, WHITE, item_t)
            draw.text((x + 25, y + 20), icon, font=get_font(40), fill=icon_color)

            title_color = lerp_color(BG_DARK, WHITE, item_t)
            draw.text((x + 85, y + 25), title, font=get_font(28, bold=True), fill=title_color)

            desc_color = lerp_color(BG_DARK, GRAY, item_t)
            draw.text((x + 85, y + 70), desc, font=get_font(20), fill=desc_color)

    # Bottom highlight bar
    if t > 0.7:
        bar_t = ease_in_out(min(1, (t - 0.7) / 0.2))
        bar_color = lerp_color(BG_DARK, TEAL, bar_t * 0.3)
        draw_rounded_rect(draw, [100, 870, W - 100, 940], fill=bar_color, radius=12)
        txt_color = lerp_color(BG_DARK, WHITE, bar_t)
        draw_centered_text(draw, 885, "94 Services  •  20 UI-Komponenten  •  11 Edge Functions  •  3 Sprachen",
                         get_font(24), txt_color)

    return img


def make_slide_demo(frame_i, total_frames):
    """Slide 5: Live-Demo Simulation — Dashboard"""
    img = Image.new("RGB", (W, H))
    draw = ImageDraw.Draw(img)
    draw_gradient_bg(draw, W, H, (15, 15, 25), (20, 20, 35))

    t = frame_i / max(total_frames - 1, 1)

    # Simulated app frame
    app_x, app_y = 160, 40
    app_w, app_h = W - 320, H - 80
    draw_rounded_rect(draw, [app_x, app_y, app_x + app_w, app_y + app_h],
                    fill=(22, 22, 28), radius=16, outline=(50, 50, 60), outline_width=2)

    # Top bar
    draw_rounded_rect(draw, [app_x, app_y, app_x + app_w, app_y + 50],
                    fill=(28, 28, 35), radius=16)
    draw.rectangle([app_x, app_y + 35, app_x + app_w, app_y + 50], fill=(28, 28, 35))

    # Window controls
    for i, c in enumerate([RED, AMBER, GREEN]):
        draw.ellipse([app_x + 20 + i * 25, app_y + 15, app_x + 34 + i * 25, app_y + 29], fill=c)

    draw.text((app_x + 110, app_y + 12), "FreyAI Visions — Dashboard", font=get_font(18), fill=GRAY)

    # Sidebar
    sb_w = 220
    sb_x = app_x + 1
    sb_y = app_y + 50
    draw.rectangle([sb_x, sb_y, sb_x + sb_w, app_y + app_h - 1], fill=(18, 18, 24))

    sidebar_items = [
        ("▣", "Dashboard", True),
        ("📋", "Anfragen", False),
        ("📄", "Angebote", False),
        ("📦", "Aufträge", False),
        ("🧾", "Rechnungen", False),
        ("👥", "Kunden", False),
        ("📅", "Kalender", False),
        ("📊", "Buchhaltung", False),
    ]

    for i, (icon, label, active) in enumerate(sidebar_items):
        item_y = sb_y + 20 + i * 48
        if active:
            draw_rounded_rect(draw, [sb_x + 8, item_y - 4, sb_x + sb_w - 8, item_y + 36],
                            fill=(TEAL[0], TEAL[1], TEAL[2]), radius=8)
            txt_color = WHITE
        else:
            txt_color = GRAY
        draw.text((sb_x + 20, item_y + 2), icon, font=get_font(18), fill=txt_color)
        draw.text((sb_x + 50, item_y + 4), label, font=get_font(18), fill=txt_color)

    # Main content area
    content_x = sb_x + sb_w + 20
    content_y = sb_y + 20
    content_w = app_w - sb_w - 50

    # KPI Cards
    kpis = [
        ("Aktive Aufträge", "12", "+3 diese Woche", GREEN),
        ("Offene Rechnungen", "€ 28.450", "5 Rechnungen", AMBER),
        ("Umsatz März", "€ 47.200", "+18% vs. Vormonat", TEAL),
        ("Neue Anfragen", "8", "3 unbearbeitet", INDIGO),
    ]

    kpi_w = (content_w - 30) // 4
    for i, (label, value, sub, color) in enumerate(kpis):
        kpi_t = ease_in_out(max(0, min(1, (t - i * 0.08) / 0.15)))
        kx = content_x + i * (kpi_w + 10)
        ky = content_y

        card_bg = lerp_color((22, 22, 28), (30, 30, 40), kpi_t)
        draw_rounded_rect(draw, [kx, ky, kx + kpi_w, ky + 120], fill=card_bg, radius=12,
                        outline=lerp_color((22, 22, 28), color, kpi_t * 0.4), outline_width=1)

        draw.text((kx + 15, ky + 12), label, font=get_font(15), fill=lerp_color((22, 22, 28), GRAY, kpi_t))
        draw.text((kx + 15, ky + 38), value, font=get_font(32, bold=True), fill=lerp_color((22, 22, 28), WHITE, kpi_t))
        draw.text((kx + 15, ky + 82), sub, font=get_font(14), fill=lerp_color((22, 22, 28), color, kpi_t))

    # Activity feed
    if t > 0.3:
        feed_t = ease_in_out(min(1, (t - 0.3) / 0.2))
        feed_y = content_y + 150
        draw.text((content_x, feed_y), "Letzte Aktivitäten",
                 font=get_font(22, bold=True), fill=lerp_color((22, 22, 28), WHITE, feed_t))

        activities = [
            ("09:45", "Rechnung #2024-089 bezahlt", "Mueller GmbH — € 2.150,00", GREEN),
            ("09:30", "Neues Angebot erstellt (KI)", "Badezimmer-Sanierung — € 8.400,00", INDIGO),
            ("09:15", "Auftrag in Bearbeitung", "Dacharbeiten Hauptstr. 12", AMBER),
            ("08:50", "Mahnung automatisch versendet", "Schmidt Bau — Rechnung #2024-071", RED),
            ("08:30", "Neue Anfrage eingegangen", "Fenstermontage — Weber Immobilien", TEAL),
        ]

        for i, (time, title, desc, color) in enumerate(activities):
            act_t = ease_in_out(max(0, min(1, (t - 0.35 - i * 0.06) / 0.15)))
            ay = feed_y + 40 + i * 65

            if act_t > 0:
                row_bg = lerp_color((22, 22, 28), (28, 28, 36), act_t)
                draw_rounded_rect(draw, [content_x, ay, content_x + content_w, ay + 55],
                                fill=row_bg, radius=8)

                # Color dot
                dot_color = lerp_color((22, 22, 28), color, act_t)
                draw.ellipse([content_x + 15, ay + 18, content_x + 25, ay + 28], fill=dot_color)

                time_color = lerp_color((22, 22, 28), MUTED, act_t)
                draw.text((content_x + 35, ay + 8), time, font=get_font(14), fill=time_color)
                draw.text((content_x + 100, ay + 5), title, font=get_font(17, bold=True),
                         fill=lerp_color((22, 22, 28), WHITE, act_t))
                draw.text((content_x + 100, ay + 28), desc, font=get_font(14),
                         fill=lerp_color((22, 22, 28), GRAY, act_t))

    # "KI" badge pulsing
    if t > 0.5:
        pulse = 0.7 + 0.3 * math.sin(t * math.pi * 4)
        badge_color = lerp_color(BG_DARK, TEAL, pulse)
        bx = app_x + app_w - 120
        by = app_y + app_h - 60
        draw_rounded_rect(draw, [bx, by, bx + 90, by + 35], fill=badge_color, radius=17)
        draw.text((bx + 15, by + 5), "🤖 KI aktiv", font=get_font(14, bold=True), fill=WHITE)

    return img


def make_slide_founder(frame_i, total_frames):
    """Slide 6: Entwickelt von Jonas Glawion"""
    img = Image.new("RGB", (W, H))
    draw = ImageDraw.Draw(img)
    draw_gradient_bg(draw, W, H, (15, 20, 30), (26, 26, 46))

    t = frame_i / max(total_frames - 1, 1)

    # Portrait
    try:
        portrait = Image.open("/home/openclaw/workspace/projects/freyai-website/portrait.png")
        portrait = portrait.resize((300, 300), Image.LANCZOS)
        # Circular mask
        mask = Image.new("L", (300, 300), 0)
        mask_draw = ImageDraw.Draw(mask)
        mask_draw.ellipse([0, 0, 299, 299], fill=255)

        # Position
        px = W // 2 - 150
        py = 120

        # Teal ring
        ring_r = 160
        draw.ellipse([px + 150 - ring_r, py + 150 - ring_r, px + 150 + ring_r, py + 150 + ring_r],
                    outline=TEAL, width=3)

        img.paste(portrait, (px, py), mask)
    except:
        draw.ellipse([W//2 - 100, 170, W//2 + 100, 370], fill=TEAL)

    # Text
    fade_t = ease_in_out(min(1, t * 1.5))

    font_name = get_font(44, bold=True)
    font_role = get_font(26)
    font_desc = get_font(22)

    name_color = lerp_color(BG_DARK, WHITE, fade_t)
    role_color = lerp_color(BG_DARK, TEAL_LIGHT, fade_t)
    desc_color = lerp_color(BG_DARK, GRAY, fade_t)

    draw_centered_text(draw, 460, "Jonas Glawion", font_name, name_color)
    draw_centered_text(draw, 520, "Gründer & Entwickler — FreyAI Visions", font_role, role_color)

    # Location + info
    if t > 0.3:
        info_t = ease_in_out(min(1, (t - 0.3) / 0.3))
        info_color = lerp_color(BG_DARK, GRAY, info_t)

        draw_centered_text(draw, 590, "📍 Großostheim bei Aschaffenburg", font_desc, info_color)
        draw_centered_text(draw, 625, "Speziell entwickelt für den deutschen Markt", font_desc, info_color)

    # Quote box
    if t > 0.5:
        qt = ease_in_out(min(1, (t - 0.5) / 0.3))
        qx = W // 2 - 400
        qy = 700
        quote_bg = lerp_color(BG_DARK, (30, 35, 45), qt)
        draw_rounded_rect(draw, [qx, qy, qx + 800, qy + 120], fill=quote_bg, radius=16,
                        outline=lerp_color(BG_DARK, TEAL, qt * 0.5), outline_width=2)

        # Quote mark
        draw.text((qx + 20, qy + 5), "\"", font=get_font(60, bold=True), fill=lerp_color(BG_DARK, TEAL, qt))

        quote_font = get_font(22)
        q_color = lerp_color(BG_DARK, WHITE, qt)
        draw.text((qx + 60, qy + 30), "Handwerker sollten ihr Handwerk machen können —", font=quote_font, fill=q_color)
        draw.text((qx + 60, qy + 60), "nicht stundenlang vor dem Computer sitzen.", font=quote_font, fill=q_color)

    return img


def make_slide_cta(frame_i, total_frames):
    """Slide 7: Call to Action"""
    img = Image.new("RGB", (W, H))
    draw = ImageDraw.Draw(img)
    draw_gradient_bg(draw, W, H, (10, 30, 28), (26, 26, 46))

    t = frame_i / max(total_frames - 1, 1)

    # Pulsing glow
    glow_r = 300 + int(30 * math.sin(t * math.pi * 2))
    cx, cy = W // 2, H // 2 - 50
    for r in range(glow_r, 0, -3):
        c = lerp_color(BG_DARK, TEAL, 0.08 * (1 - r / glow_r))
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=c)

    # Logo
    try:
        logo = Image.open("/home/openclaw/workspace/projects/instagram-campaign/assets/logo-square-freyja.png")
        logo = logo.resize((160, 160), Image.LANCZOS)
        if logo.mode == "RGBA":
            img.paste(logo, (cx - 80, 140), logo)
        else:
            img.paste(logo, (cx - 80, 140))
    except:
        pass

    # Main CTA text
    fade_t = ease_in_out(min(1, t * 2))

    font_big = get_font(56, bold=True)
    font_sub = get_font(30)
    font_url = get_font(42, bold=True)

    draw_centered_text(draw, 340, "Bereit für weniger Bürokram?", font_big, lerp_color(BG_DARK, WHITE, fade_t))
    draw_centered_text(draw, 420, "Kostenloses Erstgespräch — 10 Minuten die sich lohnen",
                      font_sub, lerp_color(BG_DARK, GRAY, fade_t))

    # URL button
    if t > 0.3:
        btn_t = ease_in_out(min(1, (t - 0.3) / 0.3))
        btn_w = 600
        btn_h = 80
        btn_x = (W - btn_w) // 2
        btn_y = 520

        btn_color = lerp_color(BG_DARK, TEAL, btn_t)
        draw_rounded_rect(draw, [btn_x, btn_y, btn_x + btn_w, btn_y + btn_h],
                        fill=btn_color, radius=40)
        draw_centered_text(draw, btn_y + 15, "freyaivisions.de", font_url,
                         lerp_color(BG_DARK, WHITE, btn_t))

    # Features reminder
    if t > 0.5:
        feat_t = ease_in_out(min(1, (t - 0.5) / 0.2))
        feat_color = lerp_color(BG_DARK, GRAY, feat_t)
        feat_font = get_font(20)

        features = ["✓ Offline-fähig", "✓ DSGVO-konform", "✓ DATEV-Export", "✓ Keine Abo-Falle"]
        total_w = sum(draw.textbbox((0, 0), f, font=feat_font)[2] for f in features) + 60 * (len(features) - 1)
        fx = (W - total_w) // 2
        for feat in features:
            draw.text((fx, 660), feat, font=feat_font, fill=feat_color)
            fx += draw.textbbox((0, 0), feat, font=feat_font)[2] + 60

    # Bottom
    if t > 0.7:
        bot_t = ease_in_out(min(1, (t - 0.7) / 0.2))
        bot_font = get_font(18)
        bot_color = lerp_color(BG_DARK, MUTED, bot_t)
        draw_centered_text(draw, 760, "FreyAI Visions — Weniger Bürokram. Mehr Handwerk.", bot_font, bot_color)
        draw_centered_text(draw, 790, "© 2026 Jonas Glawion, Großostheim", get_font(14), bot_color)

    return img


# ============================================================
# VIDEO ASSEMBLY
# ============================================================

def generate_all_frames():
    slides = [
        ("Intro",    make_slide_intro,    6),    # 6 seconds
        ("Problem",  make_slide_problem,  8),    # 8 seconds
        ("Lösung",   make_slide_solution, 10),   # 10 seconds
        ("Features", make_slide_features, 8),    # 8 seconds
        ("Demo",     make_slide_demo,     10),   # 10 seconds
        ("Gründer",  make_slide_founder,  7),    # 7 seconds
        ("CTA",      make_slide_cta,      7),    # 7 seconds
    ]
    # Total: 56 seconds

    frame_num = 0
    total_slides = len(slides)

    for slide_i, (name, func, duration_s) in enumerate(slides):
        slide_frames = duration_s * FPS
        print(f"  Slide {slide_i+1}/{total_slides}: {name} ({duration_s}s, {slide_frames} frames)")

        for i in range(slide_frames):
            img = func(i, slide_frames)

            # Fade in (first 0.5s)
            if i < FPS // 2:
                fade = i / (FPS // 2)
                overlay = Image.new("RGB", (W, H), BG_DARK)
                img = Image.blend(overlay, img, fade)

            # Fade out (last 0.5s)
            if i > slide_frames - FPS // 2:
                fade = (slide_frames - i) / (FPS // 2)
                overlay = Image.new("RGB", (W, H), BG_DARK)
                img = Image.blend(overlay, img, fade)

            img.save(os.path.join(FRAMES_DIR, f"frame_{frame_num:05d}.png"))
            frame_num += 1

    print(f"\n  Total: {frame_num} frames ({frame_num/FPS:.1f}s)")
    return frame_num


if __name__ == "__main__":
    print("=== FreyAI Visions Erklärvideo Generator ===\n")
    print("1. Generiere Frames...")
    total = generate_all_frames()

    print("\n2. Kompiliere Video mit ffmpeg...")
    cmd = (
        f"ffmpeg -y -framerate {FPS} -i {FRAMES_DIR}/frame_%05d.png "
        f"-c:v libx264 -preset medium -crf 23 -pix_fmt yuv420p "
        f"-movflags +faststart "
        f"{OUTPUT_FILE}"
    )
    os.system(cmd)

    size_mb = os.path.getsize(OUTPUT_FILE) / (1024 * 1024)
    print(f"\n=== Fertig! ===")
    print(f"Video: {OUTPUT_FILE}")
    print(f"Größe: {size_mb:.1f} MB")
    print(f"Dauer: {total/FPS:.0f} Sekunden")
    print(f"Auflösung: {W}x{H} @ {FPS}fps")
