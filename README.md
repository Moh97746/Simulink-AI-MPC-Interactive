# 🔧 Simulink → Interactive Web Diagram Skill

> **AI Agent Skill** for converting any MATLAB Simulink `.slx` model into a professional, interactive, bilingual (AR/EN) web-based visualization — deployable as a single static HTML file.

[![Live Demo](https://img.shields.io/badge/🌐_Live_Demo-Click_Here-2563EB?style=for-the-badge)](https://Marco9249.github.io/Simulink-AI-MPC-Interactive/)

---

## 🎯 What This Skill Does

| Input | Output |
|---|---|
| Any `.slx` Simulink model file | ✅ Professional SVG block diagrams |
| | ✅ Single-file interactive HTML with animated simulation |
| | ✅ Bilingual interface (Arabic / English) |
| | ✅ 8K ultra-resolution PNG export |
| | ✅ Dark mode, zoom/pan, auto-tracking camera |
| | ✅ GitHub Pages ready deployment |

---

## 📁 Repository Structure

```
├── draw_light.py           # Core drawing library (matplotlib → SVG)
├── build_interactive.py    # HTML assembler (injects SVGs + JS interactivity)
├── slx_parser.py           # Auto-extracts blocks & wires from .slx files
├── SKILL_GUIDE.md          # Complete step-by-step guide for AI agents
├── index.html              # Live demo (GitHub Pages)
│
└── sample_output/          # Example output from a real Simulink project
    ├── PV_GHI_System_Mezoo_3.slx    # Original Simulink file
    ├── gen_light_root.py             # Hand-tuned layout for root diagram
    ├── gen_light_subs.py             # Hand-tuned layout for subsystems
    ├── gen_PV_GHI_System_Mezoo_3.py  # Auto-generated layout (by slx_parser)
    ├── 01_Root_Level_Final.svg       # Generated root diagram
    ├── 02_AI_BLOCK_Final.svg         # Generated AI subsystem diagram
    └── 03_Water_Tank_Final.svg       # Generated water tank diagram
```

---

## 🚀 Quick Start (4 Steps)

### Step 1: Parse your Simulink file
```bash
python slx_parser.py your_model.slx
```
This auto-generates `gen_your_model.py` with all blocks and wire connections.

### Step 2: Refine the layout
Open the generated file and adjust `(x, y)` coordinates for professional positioning.

### Step 3: Generate SVG diagrams
```bash
python gen_your_model.py
```

### Step 4: Build the interactive HTML
Update `build_interactive.py` with your SVG filenames and block explanations, then:
```bash
python build_interactive.py
```

Open `04_Interactive_Explanation.html` in your browser — done! 🎉

---

## ✨ Interactive Features

| Feature | Description |
|---|---|
| 🖱️ Click any block | Shows detailed technical explanation in sidebar |
| ▶️ Run Simulation | Animated signal flow with 7 phases + camera tracking |
| 🔍 Zoom & Pan | Mouse wheel zoom, drag to pan |
| 🌐 Language Toggle | Full AR ↔ EN translation (UI + explanations + simulation) |
| 🌙 Dark Mode | Professional dark theme |
| 📥 Export 8K PNG | Ultra-high resolution for academic papers |
| 📥 Export SVG | Vector format for publications |
| 🗂️ Hide Sidebar | Maximize diagram viewing area |
| ⏱️ Speed Control | 0.5x to 2x simulation speed |

---

## ⚠️ Critical Rules for AI Agents

### 1. Python `.format()` + JavaScript `{}` Escaping
The HTML template uses Python's `.format()`. **Every JS brace must be doubled:**
```python
# ❌ WRONG — will crash with KeyError
function test() { return {x: 1}; }

# ✅ CORRECT
function test() {{ return {{x: 1}}; }}
```

### 2. Never Use Regex Refactoring
Do NOT use regex scripts to modify `build_interactive.py`. The mixed Python/JS syntax makes regex replacements extremely dangerous.

### 3. SVG Must Be Cleaned
Strip `width` and `height` attributes from matplotlib SVGs for responsive display.

### 4. Block IDs Are Mandatory
Every `draw_block()` must have a `gid='block_name'` matching an entry in the `explanations` dictionary.

---

## 📖 Full Documentation

See **[SKILL_GUIDE.md](SKILL_GUIDE.md)** for the complete guide including:
- Detailed architecture explanation
- All API references for `draw_light.py`
- Error troubleshooting table
- Bilingual support patterns
- Export resolution configuration

---

## 📬 Contact

**izzeldeenm@gmail.com**

---

## 📄 License

MIT License — Free to use for academic and commercial projects.
