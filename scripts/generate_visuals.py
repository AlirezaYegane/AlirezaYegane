#!/usr/bin/env python3
"""Generate original, deterministic SVG assets for the GitHub profile.

The visual system is deliberately local-first: the README remains coherent even if
external widgets are unavailable. profile.json is the single source of truth.
"""
from __future__ import annotations

import html
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "profile.json"
ASSETS = ROOT / "assets"
PROJECT_DIR = ASSETS / "project-covers"
ROUTE_DIR = ASSETS / "routes"
CONTRIB_DIR = ROOT / "profile-3d-contrib"


def esc(value: object) -> str:
    return html.escape(str(value), quote=True)


def palette(dark: bool) -> dict[str, str]:
    return {
        "bg": "#07111F" if dark else "#F4F7FC",
        "panel": "#0D1B2A" if dark else "#FFFFFF",
        "panel2": "#102438" if dark else "#EAF0F8",
        "line": "#28445E" if dark else "#C7D4E3",
        "text": "#F5F7FA" if dark else "#132238",
        "muted": "#9EB2C7" if dark else "#52677E",
        "purple": "#A78BFA" if dark else "#6D28D9",
        "cyan": "#35D7FF" if dark else "#007FA3",
        "green": "#43D9AD" if dark else "#087F5B",
        "amber": "#F6C85F" if dark else "#A15C00",
        "pink": "#FB7185" if dark else "#C02654",
    }


def theme_style() -> str:
    return """<style>
    .orbit { transform-origin: 910px 250px; animation: orbit 24s linear infinite; }
    .orbit-reverse { transform-origin: 910px 250px; animation: orbit-reverse 34s linear infinite; }
    .pulse { animation: pulse 2.8s ease-in-out infinite; }
    .dash { animation: dash 10s linear infinite; }
    .cursor { animation: blink 1.1s steps(2,end) infinite; }
    .scan { animation: scan 6s ease-in-out infinite; }
    @keyframes orbit { to { transform: rotate(360deg); } }
    @keyframes orbit-reverse { to { transform: rotate(-360deg); } }
    @keyframes pulse { 0%,100% { opacity:.35; transform:scale(.96) } 50% { opacity:1; transform:scale(1.05) } }
    @keyframes dash { to { stroke-dashoffset:-180; } }
    @keyframes blink { 0%,49% { opacity:1 } 50%,100% { opacity:0 } }
    @keyframes scan { 0%,100% { transform:translateY(-24px); opacity:0 } 20%,80% { opacity:.35 } 50% { transform:translateY(365px); opacity:.18 } }
    @media (prefers-reduced-motion: reduce) {
      .orbit,.orbit-reverse,.pulse,.dash,.cursor,.scan { animation:none !important; }
    }
  </style>"""


def hero_svg(data: dict, dark: bool) -> str:
    p = palette(dark)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="500" viewBox="0 0 1200 500" role="img" aria-labelledby="title desc">
  <title id="title">Alireza Yegane research mission control</title>
  <desc id="desc">Animated research mission-control panel introducing Alireza Yegane, his role in AI and machine learning, Sydney location, and a visual orbit connecting research, engineering, and delivery.</desc>
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop stop-color="{p['bg']}"/><stop offset="1" stop-color="{p['panel2']}"/></linearGradient>
    <radialGradient id="glow"><stop stop-color="{p['cyan']}" stop-opacity=".35"/><stop offset="1" stop-color="{p['cyan']}" stop-opacity="0"/></radialGradient>
    <filter id="soft"><feGaussianBlur stdDeviation="12"/></filter>
    <pattern id="grid" width="32" height="32" patternUnits="userSpaceOnUse"><path d="M32 0H0V32" fill="none" stroke="{p['line']}" stroke-width="1" opacity=".2"/></pattern>
  </defs>
  {theme_style()}
  <rect width="1200" height="500" rx="30" fill="url(#bg)"/>
  <rect x="18" y="18" width="1164" height="464" rx="22" fill="url(#grid)" stroke="{p['line']}" stroke-width="2"/>
  <rect class="scan" x="30" y="42" width="1140" height="3" fill="{p['cyan']}" opacity=".15"/>
  <g font-family="ui-monospace,SFMono-Regular,Consolas,Liberation Mono,monospace">
    <circle cx="52" cy="50" r="6" fill="#FF5F57"/><circle cx="74" cy="50" r="6" fill="#FEBC2E"/><circle cx="96" cy="50" r="6" fill="#28C840"/>
    <text x="125" y="57" font-size="15" fill="{p['muted']}">ALIREZA / RESEARCH-MISSION-CONTROL</text>
    <rect x="1000" y="37" width="145" height="28" rx="14" fill="{p['green']}" opacity=".13" stroke="{p['green']}"/>
    <circle class="pulse" cx="1019" cy="51" r="5" fill="{p['green']}"/>
    <text x="1032" y="56" font-size="12" font-weight="700" fill="{p['green']}">SYSTEM ONLINE</text>

    <text x="58" y="122" font-size="16" fill="{p['green']}">$ whoami</text>
    <text x="58" y="177" font-family="system-ui,-apple-system,Segoe UI,sans-serif" font-size="48" font-weight="800" fill="{p['text']}">{esc(data['name'])}</text>
    <text x="58" y="218" font-family="system-ui,-apple-system,Segoe UI,sans-serif" font-size="22" font-weight="600" fill="{p['purple']}">{esc(data['headline'])}</text>
    <text x="58" y="265" font-size="16" fill="{p['green']}">$ objective</text>
    <text x="58" y="299" font-size="19" fill="{p['text']}">build reliable AI &amp; data systems</text>
    <text x="58" y="329" font-size="19" fill="{p['text']}">from evidence -&gt; experiment -&gt; usable software</text>
    <text x="58" y="381" font-size="16" fill="{p['green']}">$ coordinates</text>
    <text x="58" y="414" font-size="18" fill="{p['text']}">{esc(data['location'])} · {esc(data['role'])}</text>
    <text x="58" y="455" font-size="14" fill="{p['muted']}">assert evidence &gt; hype</text><rect class="cursor" x="257" y="440" width="11" height="20" fill="{p['cyan']}"/>
  </g>

  <circle cx="910" cy="250" r="190" fill="url(#glow)" filter="url(#soft)"/>
  <g fill="none" stroke="{p['line']}" stroke-width="2">
    <circle cx="910" cy="250" r="164"/><circle cx="910" cy="250" r="118" stroke-dasharray="7 9"/><circle cx="910" cy="250" r="72"/>
  </g>
  <g class="orbit" fill="none" stroke="{p['cyan']}" stroke-width="3" stroke-dasharray="12 12"><circle cx="910" cy="250" r="164"/></g>
  <g class="orbit-reverse" fill="none" stroke="{p['purple']}" stroke-width="2" stroke-dasharray="5 16"><circle cx="910" cy="250" r="118"/></g>
  <path class="dash" d="M746 250 C790 150 860 120 910 178 C960 236 1020 130 1074 250 C1024 350 956 378 910 322 C864 266 798 370 746 250Z" fill="none" stroke="{p['green']}" stroke-width="2" stroke-dasharray="10 10"/>
  <circle cx="910" cy="250" r="48" fill="{p['panel']}" stroke="{p['cyan']}" stroke-width="3"/>
  <text x="910" y="243" text-anchor="middle" font-family="ui-monospace,SFMono-Regular,Consolas,monospace" font-size="15" font-weight="700" fill="{p['text']}">RELIABLE</text>
  <text x="910" y="265" text-anchor="middle" font-family="ui-monospace,SFMono-Regular,Consolas,monospace" font-size="15" font-weight="700" fill="{p['text']}">SYSTEMS</text>
  <g font-family="ui-monospace,SFMono-Regular,Consolas,monospace" font-size="13" font-weight="700">
    <g><circle class="pulse" cx="910" cy="86" r="11" fill="{p['purple']}"/><text x="910" y="67" text-anchor="middle" fill="{p['purple']}">RESEARCH</text></g>
    <g><circle class="pulse" cx="1074" cy="250" r="11" fill="{p['cyan']}"/><text x="1080" y="225" text-anchor="middle" fill="{p['cyan']}">BUILD</text></g>
    <g><circle class="pulse" cx="910" cy="414" r="11" fill="{p['green']}"/><text x="910" y="448" text-anchor="middle" fill="{p['green']}">DELIVER</text></g>
    <g><circle class="pulse" cx="746" cy="250" r="11" fill="{p['amber']}"/><text x="724" y="225" text-anchor="middle" fill="{p['amber']}">EVALUATE</text></g>
  </g>
</svg>'''


def focus_svg(data: dict, dark: bool) -> str:
    p = palette(dark)
    rows = []
    y = 83
    accents = [p['purple'], p['cyan'], p['green'], p['amber']]
    for idx, item in enumerate(data['current_focus']):
        rows.append(f'''<rect x="46" y="{y-28}" width="1108" height="54" rx="12" fill="{p['panel2']}" stroke="{p['line']}"/>
  <rect x="46" y="{y-28}" width="8" height="54" rx="4" fill="{accents[idx]}"/>
  <text x="78" y="{y+5}" font-family="ui-monospace,SFMono-Regular,Consolas,monospace" font-size="14" font-weight="700" fill="{accents[idx]}">{esc(item['label'])}</text>
  <text x="260" y="{y+5}" font-family="system-ui,-apple-system,Segoe UI,sans-serif" font-size="18" font-weight="600" fill="{p['text']}">{esc(item['value'])}</text>''')
        y += 66
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="370" viewBox="0 0 1200 370" role="img" aria-labelledby="title desc">
  <title id="title">Current research and engineering signals</title>
  <desc id="desc">A mission-status panel listing current research, software building, evaluation, and teaching activities.</desc>
  <defs><linearGradient id="focusbg" x1="0" y1="0" x2="1" y2="1"><stop stop-color="{p['panel']}"/><stop offset="1" stop-color="{p['bg']}"/></linearGradient></defs>
  <rect width="1200" height="370" rx="24" fill="url(#focusbg)" stroke="{p['line']}" stroke-width="2"/>
  <text x="46" y="35" font-family="ui-monospace,SFMono-Regular,Consolas,monospace" font-size="15" fill="{p['muted']}">/now · signal buffer · manually verified {esc(data['last_manual_review'])}</text>
  {''.join(rows)}
  <text x="46" y="347" font-family="ui-monospace,SFMono-Regular,Consolas,monospace" font-size="13" fill="{p['muted']}">status: active work, not a production-readiness claim</text>
</svg>'''


def route_svg(title: str, code: str, line1: str, line2: str, accent: str) -> str:
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1120" height="138" viewBox="0 0 1120 138" role="img" aria-labelledby="title desc">
  <title id="title">{esc(title)} route</title><desc id="desc">A navigation card for the {esc(title.lower())} view of Alireza's profile.</desc>
  <defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#0B1423"/><stop offset="1" stop-color="#142A41"/></linearGradient></defs>
  <rect x="3" y="3" width="1114" height="132" rx="22" fill="url(#g)" stroke="{accent}" stroke-width="2"/>
  <rect x="24" y="26" width="94" height="28" rx="14" fill="{accent}" opacity=".14" stroke="{accent}"/>
  <text x="71" y="45" text-anchor="middle" font-family="ui-monospace,SFMono-Regular,Consolas,monospace" font-size="12" font-weight="700" fill="{accent}">{esc(code)}</text>
  <text x="145" y="55" font-family="system-ui,-apple-system,Segoe UI,sans-serif" font-size="27" font-weight="800" fill="#F7FAFC">{esc(title)}</text>
  <text x="145" y="91" font-family="system-ui,-apple-system,Segoe UI,sans-serif" font-size="15" fill="#AEC2D5">{esc(line1)} · {esc(line2)}</text>
  <text x="866" y="79" font-family="ui-monospace,SFMono-Regular,Consolas,monospace" font-size="13" font-weight="700" fill="{accent}">OPEN ROUTE</text>
  <circle cx="1054" cy="69" r="34" fill="{accent}" opacity=".14"/>
  <path d="M1035 69h38M1060 55l14 14-14 14" fill="none" stroke="{accent}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>
</svg>'''


def project_icon(slug: str, accent: str) -> str:
    if slug == "ehr":
        return f'''<g transform="translate(426 30)" stroke="{accent}" fill="none" stroke-width="3"><circle cx="52" cy="52" r="42" opacity=".35"/><path d="M52 27v50M27 52h50"/><circle cx="19" cy="19" r="6" fill="{accent}"/><circle cx="87" cy="19" r="6" fill="{accent}"/><circle cx="87" cy="87" r="6" fill="{accent}"/><path d="M24 24l22 22M82 24L60 46M82 82L60 60" opacity=".7"/></g>'''
    if slug == "pilot":
        return f'''<g transform="translate(425 28)" fill="none" stroke="{accent}" stroke-width="3"><circle cx="54" cy="54" r="44" opacity=".3"/><circle cx="54" cy="54" r="30" opacity=".45"/><circle cx="54" cy="54" r="16"/><path d="M54 54L84 32"/><circle cx="54" cy="54" r="5" fill="{accent}"/><path d="M54 6v10M102 54H92M54 102V92M6 54h10"/></g>'''
    if slug == "dax":
        return f'''<g transform="translate(424 31)" stroke="{accent}" stroke-width="3" fill="none"><path d="M8 94V14M8 94h102" opacity=".45"/><rect x="23" y="62" width="15" height="32" rx="3" fill="{accent}" opacity=".35"/><rect x="51" y="42" width="15" height="52" rx="3" fill="{accent}" opacity=".55"/><rect x="79" y="20" width="15" height="74" rx="3" fill="{accent}" opacity=".8"/><path d="M20 48l30-20 24 8 31-24" stroke-linecap="round" stroke-linejoin="round"/></g>'''
    if slug == "gnn":
        return f'''<g transform="translate(423 26)" stroke="{accent}" stroke-width="3"><path d="M20 72L52 23l45 18 8 53-54 12zM20 72l77-31M52 23l-1 83M97 41L51 106" fill="none" opacity=".65"/><g fill="{accent}"><circle cx="20" cy="72" r="7"/><circle cx="52" cy="23" r="7"/><circle cx="97" cy="41" r="7"/><circle cx="105" cy="94" r="7"/><circle cx="51" cy="106" r="7"/></g></g>'''
    if slug == "constructflow":
        return f'''<g transform="translate(417 31)" fill="none" stroke="{accent}" stroke-width="3"><rect x="5" y="14" width="38" height="28" rx="6"/><rect x="72" y="14" width="38" height="28" rx="6"/><rect x="39" y="74" width="38" height="28" rx="6"/><path d="M43 28h29M91 42v20L77 76M24 42v20l15 14"/><circle cx="58" cy="57" r="7" fill="{accent}"/></g>'''
    return f'''<g transform="translate(420 26)" fill="none" stroke="{accent}" stroke-width="3"><circle cx="55" cy="55" r="47" opacity=".22"/><circle cx="55" cy="55" r="33" opacity=".38"/><circle cx="55" cy="55" r="18" opacity=".7"/><path d="M14 37c20-24 60-30 86 0M10 73c30 21 65 20 93-2"/><circle cx="55" cy="55" r="5" fill="{accent}"/></g>'''


def wrap_words(text: str, max_chars: int, max_lines: int = 2) -> list[str]:
    words = text.split()
    lines: list[str] = []
    current = ""
    for word in words:
        candidate = f"{current} {word}".strip()
        if current and len(candidate) > max_chars:
            lines.append(current)
            current = word
            if len(lines) == max_lines - 1:
                break
        else:
            current = candidate
    remaining_start = sum(len(line.split()) for line in lines)
    remaining_words = words[remaining_start:]
    if len(lines) < max_lines and remaining_words:
        final = " ".join(remaining_words)
        if len(final) > max_chars + 8:
            final = final[: max_chars + 5].rstrip() + "…"
        lines.append(final)
    return lines[:max_lines]


def project_svg(project: dict) -> str:
    accent = project['accent']
    title_lines = wrap_words(project['name'], 31, 2)
    question_lines = wrap_words(project['question'], 58, 2)
    title_svg = "".join(
        f'<text x="24" y="{82 + i * 29}" font-family="system-ui,-apple-system,Segoe UI,sans-serif" font-size="23" font-weight="800" fill="#F7FAFC">{esc(line)}</text>'
        for i, line in enumerate(title_lines)
    )
    question_y = 145 if len(title_lines) == 2 else 128
    question_svg = "".join(
        f'<text x="24" y="{question_y + i * 22}" font-family="system-ui,-apple-system,Segoe UI,sans-serif" font-size="14" fill="#B7C9D9">{esc(line)}</text>'
        for i, line in enumerate(question_lines)
    )
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="560" height="270" viewBox="0 0 560 270" role="img" aria-labelledby="title desc">
  <title id="title">{esc(project['name'])}</title><desc id="desc">Project card: {esc(project['question'])}. {esc(project['metric'])}. Status: {esc(project['status'])}.</desc>
  <defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#08111F"/><stop offset="1" stop-color="#142A41"/></linearGradient><radialGradient id="a"><stop stop-color="{accent}" stop-opacity=".25"/><stop offset="1" stop-color="{accent}" stop-opacity="0"/></radialGradient></defs>
  <rect x="3" y="3" width="554" height="264" rx="22" fill="url(#g)" stroke="#2D455C" stroke-width="2"/>
  <circle cx="492" cy="66" r="92" fill="url(#a)"/>
  <rect x="24" y="22" width="8" height="31" rx="4" fill="{accent}"/>
  <text x="46" y="43" font-family="ui-monospace,SFMono-Regular,Consolas,monospace" font-size="12" font-weight="700" fill="{accent}">{esc(project['eyebrow'])}</text>
  {title_svg}
  {question_svg}
  <rect x="24" y="183" width="350" height="38" rx="12" fill="{accent}" opacity=".12" stroke="{accent}" stroke-opacity=".55"/>
  <text x="42" y="207" font-family="ui-monospace,SFMono-Regular,Consolas,monospace" font-size="14" font-weight="700" fill="{accent}">{esc(project['metric'])}</text>
  <text x="24" y="246" font-family="ui-monospace,SFMono-Regular,Consolas,monospace" font-size="12" fill="#7F95AA">STATUS / {esc(project['status'].upper())}</text>
  {project_icon(project['slug'], accent)}
</svg>'''


def proof_svg(data: dict, dark: bool) -> str:
    p = palette(dark)
    metrics = data['verified_metrics']
    width = 210
    gap = 18
    x0 = 38
    cards = []
    colors = [p['purple'], p['cyan'], p['green'], p['amber'], p['pink']]
    for i, metric in enumerate(metrics):
        x = x0 + i * (width + gap)
        cards.append(f'''<rect x="{x}" y="65" width="{width}" height="155" rx="18" fill="{p['panel2']}" stroke="{p['line']}"/>
  <text x="{x+18}" y="116" font-family="system-ui,-apple-system,Segoe UI,sans-serif" font-size="31" font-weight="850" fill="{colors[i]}">{esc(metric['value'])}</text>
  <text x="{x+18}" y="153" font-family="system-ui,-apple-system,Segoe UI,sans-serif" font-size="15" font-weight="700" fill="{p['text']}">{esc(metric['label'])}</text>
  <text x="{x+18}" y="183" font-family="system-ui,-apple-system,Segoe UI,sans-serif" font-size="13" fill="{p['muted']}">{esc(metric['sub'])}</text>
  <path d="M{x+18} 201H{x+width-18}" stroke="{colors[i]}" stroke-width="3" stroke-linecap="round" opacity=".65"/>''')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="260" viewBox="0 0 1200 260" role="img" aria-labelledby="title desc">
  <title id="title">Proof, not promises</title><desc id="desc">Five verified research and engineering metrics with their context.</desc>
  <rect width="1200" height="260" rx="24" fill="{p['bg']}" stroke="{p['line']}" stroke-width="2"/>
  <text x="38" y="39" font-family="ui-monospace,SFMono-Regular,Consolas,monospace" font-size="15" font-weight="700" fill="{p['green']}">PROOF / NOT PROMISES</text>
  {''.join(cards)}
</svg>'''


def constellation_svg(dark: bool) -> str:
    p = palette(dark)
    nodes = [
        (170, 120, "RNA", "foundation models", p['purple']),
        (560, 78, "Clinical", "ontologies", p['green']),
        (990, 150, "Graph ML", "temporal shift", p['cyan']),
        (1015, 440, "AI tooling", "reliability", p['amber']),
        (560, 520, "Analytics", "Power BI · DAX", p['pink']),
        (170, 430, "Evaluation", "tests · ablations", p['cyan']),
    ]
    lines = []
    circles = []
    for i, (x, y, title, sub, color) in enumerate(nodes):
        lines.append(f'<path d="M600 300 Q{(600+x)//2} {(300+y)//2 - 35} {x} {y}" fill="none" stroke="{color}" stroke-width="2" stroke-dasharray="8 10" opacity=".65"/>')
        circles.append(f'''<circle cx="{x}" cy="{y}" r="72" fill="{p['panel']}" stroke="{color}" stroke-width="3"/>
  <circle class="pulse" cx="{x}" cy="{y}" r="83" fill="none" stroke="{color}" stroke-width="1" opacity=".25"/>
  <text x="{x}" y="{y-4}" text-anchor="middle" font-family="system-ui,-apple-system,Segoe UI,sans-serif" font-size="19" font-weight="800" fill="{p['text']}">{esc(title)}</text>
  <text x="{x}" y="{y+23}" text-anchor="middle" font-family="ui-monospace,SFMono-Regular,Consolas,monospace" font-size="12" fill="{p['muted']}">{esc(sub)}</text>''')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="610" viewBox="0 0 1200 610" role="img" aria-labelledby="title desc">
  <title id="title">Research and engineering constellation</title><desc id="desc">A constellation linking RNA foundation models, clinical ontologies, graph machine learning, AI tooling, analytics, and evaluation to reliable AI and data systems.</desc>
  {theme_style()}
  <defs><radialGradient id="center"><stop stop-color="{p['purple']}" stop-opacity=".3"/><stop offset="1" stop-color="{p['purple']}" stop-opacity="0"/></radialGradient></defs>
  <rect width="1200" height="610" rx="24" fill="{p['bg']}" stroke="{p['line']}" stroke-width="2"/>
  <g class="dash">{''.join(lines)}</g>
  {''.join(circles)}
  <circle cx="600" cy="300" r="132" fill="url(#center)"/>
  <circle cx="600" cy="300" r="102" fill="{p['panel']}" stroke="{p['purple']}" stroke-width="4"/>
  <text x="600" y="277" text-anchor="middle" font-family="system-ui,-apple-system,Segoe UI,sans-serif" font-size="23" font-weight="850" fill="{p['text']}">RELIABLE AI</text>
  <text x="600" y="309" text-anchor="middle" font-family="system-ui,-apple-system,Segoe UI,sans-serif" font-size="23" font-weight="850" fill="{p['text']}">&amp; DATA SYSTEMS</text>
  <text x="600" y="345" text-anchor="middle" font-family="ui-monospace,SFMono-Regular,Consolas,monospace" font-size="13" fill="{p['green']}">measure · reproduce · test · deliver</text>
</svg>'''


def pipeline_svg(dark: bool) -> str:
    p = palette(dark)
    stages = [
        (60, "QUESTION", "define the claim"),
        (275, "EVIDENCE", "data + assumptions"),
        (490, "EXPERIMENT", "reproducible run"),
        (705, "FAILURE", "analyse what broke"),
        (920, "OUTPUT", "tested + usable"),
    ]
    cards = []
    for i, (x, title, sub) in enumerate(stages):
        color = [p['purple'], p['cyan'], p['green'], p['amber'], p['pink']][i]
        cards.append(f'''<rect x="{x}" y="75" width="178" height="120" rx="18" fill="{p['panel']}" stroke="{color}" stroke-width="2"/>
  <text x="{x+89}" y="123" text-anchor="middle" font-family="ui-monospace,SFMono-Regular,Consolas,monospace" font-size="14" font-weight="800" fill="{color}">{title}</text>
  <text x="{x+89}" y="157" text-anchor="middle" font-family="system-ui,-apple-system,Segoe UI,sans-serif" font-size="14" fill="{p['muted']}">{sub}</text>''')
    arrows = []
    for x in [238, 453, 668, 883]:
        arrows.append(f'<path d="M{x} 135h29" stroke="{p["line"]}" stroke-width="3"/><path d="M{x+22} 128l8 7-8 7" fill="none" stroke="{p["line"]}" stroke-width="3"/>')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="270" viewBox="0 0 1200 270" role="img" aria-labelledby="title desc">
  <title id="title">Evidence-to-output signal path</title><desc id="desc">A five-stage workflow moving from research question to evidence, reproducible experiment, failure analysis, and tested usable output.</desc>
  <rect width="1200" height="270" rx="24" fill="{p['bg']}" stroke="{p['line']}" stroke-width="2"/>
  <text x="60" y="40" font-family="ui-monospace,SFMono-Regular,Consolas,monospace" font-size="15" fill="{p['muted']}">SIGNAL PATH / HOW THE WORK MOVES</text>
  {''.join(cards)}{''.join(arrows)}
  <text x="600" y="235" text-anchor="middle" font-family="ui-monospace,SFMono-Regular,Consolas,monospace" font-size="13" fill="{p['muted']}">negative results are routed back into the next experiment</text>
</svg>'''


def timeline_svg(data: dict, dark: bool) -> str:
    p = palette(dark)
    experiences = data['experience']
    ys = [82, 162, 242, 322]
    items = []
    colors = [p['purple'], p['cyan'], p['green'], p['amber']]
    for i, item in enumerate(experiences):
        y = ys[i]
        items.append(f'''<circle cx="112" cy="{y}" r="10" fill="{colors[i]}"/><circle cx="112" cy="{y}" r="19" fill="none" stroke="{colors[i]}" opacity=".28"/>
  <text x="152" y="{y-14}" font-family="ui-monospace,SFMono-Regular,Consolas,monospace" font-size="13" font-weight="700" fill="{colors[i]}">{esc(item['dates'])}</text>
  <text x="152" y="{y+12}" font-family="system-ui,-apple-system,Segoe UI,sans-serif" font-size="20" font-weight="800" fill="{p['text']}">{esc(item['role'])}</text>
  <text x="540" y="{y+12}" font-family="system-ui,-apple-system,Segoe UI,sans-serif" font-size="17" font-weight="650" fill="{p['text']}">{esc(item['org'])}</text>
  <text x="820" y="{y+12}" font-family="ui-monospace,SFMono-Regular,Consolas,monospace" font-size="13" fill="{p['muted']}">{esc(item['signal'])}</text>''')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="390" viewBox="0 0 1200 390" role="img" aria-labelledby="title desc">
  <title id="title">Career signal timeline</title><desc id="desc">Timeline of research assistant, technical contractor, data scientist, and backend developer experience.</desc>
  <rect width="1200" height="390" rx="24" fill="{p['bg']}" stroke="{p['line']}" stroke-width="2"/>
  <text x="48" y="39" font-family="ui-monospace,SFMono-Regular,Consolas,monospace" font-size="15" fill="{p['muted']}">git log --career --signal-only</text>
  <path d="M112 64V342" stroke="{p['line']}" stroke-width="4" stroke-linecap="round"/>
  {''.join(items)}
</svg>'''



def typing_fallback_svg(dark: bool) -> str:
    p = palette(dark)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="900" height="42" viewBox="0 0 900 42" role="img" aria-labelledby="title desc">
  <title id="title">Research workflow statement</title><desc id="desc">Research question to reproducible experiment to tested system.</desc>
  <text x="450" y="28" text-anchor="middle" font-family="ui-monospace,SFMono-Regular,Consolas,monospace" font-size="18" font-weight="600" fill="{p['purple']}">research_question -&gt; reproducible_experiment -&gt; tested_system</text>
</svg>'''

def contribution_placeholder() -> str:
    blocks = []
    colors = ["#183A37", "#24594F", "#2F7A68", "#43D9AD"]
    for row in range(7):
        for col in range(46):
            if (row * 7 + col * 3) % 11 in {0, 2, 5, 7}:
                level = (row + col * 2) % 4
                x = 175 + col * 18
                y = 78 + row * 18
                blocks.append(f'<rect x="{x}" y="{y}" width="12" height="12" rx="2" fill="{colors[level]}" opacity="{0.28 + level*0.18:.2f}"/>')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="290" viewBox="0 0 1200 290" role="img" aria-labelledby="title desc">
  <title id="title">GitHub contribution telemetry bootstrap</title><desc id="desc">A labelled placeholder that will be replaced by the GitHub Profile 3D Contribution workflow using public contribution data.</desc>
  <defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#07111F"/><stop offset="1" stop-color="#12283E"/></linearGradient></defs>
  <rect width="1200" height="290" rx="24" fill="url(#g)" stroke="#28445E" stroke-width="2"/>
  <text x="44" y="42" font-family="ui-monospace,SFMono-Regular,Consolas,monospace" font-size="15" font-weight="700" fill="#43D9AD">GITHUB TELEMETRY / BOOTSTRAP</text>
  <text x="44" y="70" font-family="system-ui,-apple-system,Segoe UI,sans-serif" font-size="14" fill="#9EB2C7">Run the included profile-3d workflow once to replace this scaffold with live public contribution data.</text>
  {''.join(blocks)}
  <path d="M163 220H1034" stroke="#43D9AD" stroke-width="2" opacity=".5"/><path d="M1034 220l-10-7v14z" fill="#43D9AD"/>
  <text x="175" y="250" font-family="ui-monospace,SFMono-Regular,Consolas,monospace" font-size="12" fill="#7F95AA">workflow_dispatch → generate SVG → commit only when changed</text>
</svg>'''


def main() -> None:
    data = json.loads(DATA.read_text(encoding="utf-8"))
    ASSETS.mkdir(exist_ok=True)
    PROJECT_DIR.mkdir(exist_ok=True)
    ROUTE_DIR.mkdir(exist_ok=True)
    CONTRIB_DIR.mkdir(exist_ok=True)

    for dark, suffix in [(False, "light"), (True, "dark")]:
        (ASSETS / f"hero-{suffix}.svg").write_text(hero_svg(data, dark) + "\n", encoding="utf-8")
        (ASSETS / f"focus-{suffix}.svg").write_text(focus_svg(data, dark) + "\n", encoding="utf-8")
        (ASSETS / f"proof-{suffix}.svg").write_text(proof_svg(data, dark) + "\n", encoding="utf-8")
        (ASSETS / f"research-constellation-{suffix}.svg").write_text(constellation_svg(dark) + "\n", encoding="utf-8")
        (ASSETS / f"signal-path-{suffix}.svg").write_text(pipeline_svg(dark) + "\n", encoding="utf-8")
        (ASSETS / f"career-timeline-{suffix}.svg").write_text(timeline_svg(data, dark) + "\n", encoding="utf-8")
        (ASSETS / f"typing-fallback-{suffix}.svg").write_text(typing_fallback_svg(dark) + "\n", encoding="utf-8")

    routes = [
        ("Research route", "ROUTE 01", "Biomedical AI · RNA models", "evaluation · reproducibility", "#A78BFA", "research"),
        ("Engineering route", "ROUTE 02", "Python tools · APIs · testing", "local-first · delivery", "#35D7FF", "engineering"),
        ("Career route", "ROUTE 03", "Research · data · software", "teaching · collaboration", "#43D9AD", "career"),
    ]
    for title, code, line1, line2, accent, slug in routes:
        (ROUTE_DIR / f"{slug}.svg").write_text(route_svg(title, code, line1, line2, accent) + "\n", encoding="utf-8")

    for project in data['projects']:
        (PROJECT_DIR / f"{project['slug']}.svg").write_text(project_svg(project) + "\n", encoding="utf-8")

    contrib = CONTRIB_DIR / "profile-night-rainbow.svg"
    if not contrib.exists() or "GITHUB TELEMETRY / BOOTSTRAP" in contrib.read_text(encoding="utf-8", errors="ignore"):
        contrib.write_text(contribution_placeholder() + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
