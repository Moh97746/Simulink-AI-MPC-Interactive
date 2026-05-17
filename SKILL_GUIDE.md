# Simulink-to-Interactive-Web: Complete Agent Skill Guide

## Overview
This skill converts any MATLAB Simulink `.slx` model into a professional, interactive web-based diagram with animated simulation, bilingual support (AR/EN), dark mode, and 8K export — all in a single static HTML file deployable on GitHub Pages.

**Repository:** https://github.com/Marco9249/Simulink-AI-MPC-Interactive

## Architecture (3 Core Files + 1 Tool)

```
draw_light.py        → Core drawing library (matplotlib → SVG)
build_interactive.py → HTML assembler (SVGs + JS interactivity + i18n)
slx_parser.py        → Auto-extractor for .slx files → generates layout code
gen_*.py             → Model-specific layout scripts (one per diagram)
```

### Pipeline Flow
```
.slx file → slx_parser.py → gen_model.py → [run] → SVG files → build_interactive.py → single HTML file → GitHub Pages
```

## CRITICAL RULE #1: Python `.format()` vs JavaScript `{}`

The HTML template in `build_interactive.py` uses Python's `.format()` method. This means:

- **ALL JavaScript curly braces `{}` MUST be doubled: `{{}}`**
- `{SVG_ROOT}`, `{SVG_AI}`, `{SVG_WT}`, `{EXPLANATIONS_JSON}` stay single-braced (they are the format placeholders)
- Template literals: `` `${var}` `` → `` `${{var}}` ``
- JS objects: `{x:0}` → `{{x:0}}`
- If/else blocks: `if(x) { ... }` → `if(x) {{ ... }}`

**Alternative:** If using `.replace()` instead of `.format()`, JS braces can stay single. But NEVER mix both approaches.

## CRITICAL RULE #2: Never Use Regex Refactoring Scripts

Do NOT create regex-based scripts (like `run_refactor.py`) to modify `build_interactive.py`. The mixed Python template syntax (`{{}}`) and JavaScript code makes regex replacements catastrophically error-prone. Always use targeted, line-specific edits.

## CRITICAL RULE #3: SVG Cleaning

Matplotlib SVGs include `width` and `height` attributes that prevent responsive scaling. Always strip them:
```python
def clean_svg(svg_str):
    if svg_str.startswith('<?xml'):
        svg_str = svg_str.split('?>', 1)[1]
    svg_str = re.sub(r'width="[^"]+"', '', svg_str, count=1)
    svg_str = re.sub(r'height="[^"]+"', '', svg_str, count=1)
    return svg_str
```

## CRITICAL RULE #4: Block IDs Are Mandatory

Every block and path MUST have a unique `gid` parameter matching a key in the `explanations` dictionary:
```python
draw_block(ax, x, y, w, h, 'My Block', COLORS['ai'], COLORS['ai_bg'], gid='block_myblock')
```

## Step-by-Step: Converting a New Simulink Model

### Step 1: Extract blocks from .slx
```bash
python slx_parser.py new_model.slx
```
The `.slx` file is actually a ZIP containing XML. The parser reads `simulink/systems/system_root.xml`, extracts all `<Block>` elements (SID, BlockType, Name) and `<Line>` elements (Src, Dst connections), then generates a Python layout file.

### Step 2: Refine the generated layout
Open `gen_new_model.py` and:
- Adjust `(x, y)` coordinates for each `draw_block()` call for professional positioning
- Replace placeholder wire comments with actual `draw_ortho_arrow()` calls using waypoints
- Set appropriate colors from the `COLORS` dict based on block function
- Ensure every element has a unique `gid='...'`

### Step 3: Generate SVGs
```bash
python gen_new_model.py
```
This produces `new_model_Final.svg` and `new_model_Final.png`.

### Step 4: Add explanations to build_interactive.py
Add entries to the `explanations` dict with:
```python
'block_name': {
    'title': 'English Title',
    'text': 'Arabic description...',
    'text_en': 'English description...'
}
```

### Step 5: Wire up the HTML template
In `build_interactive.py`:
1. Add a new tab in the header: `<div class="tab" onclick="switchTab(N)">Tab Name</div>`
2. Add a new svg-container: `<div class="svg-container" id="tabN"><div class="zoom-wrapper" id="zoomN">{SVG_NEW}</div></div>`
3. Read the SVG in the Python section: `svg_new = read_svg('new_model_Final.svg')`
4. Add to format: `.format(SVG_ROOT=svg_root, ..., SVG_NEW=svg_new, ...)`

### Step 6: Update the i18n dictionary
Inside the `toggleLanguage()` function, add translations for all new tabs, labels, and simulation phases.

### Step 7: Build and test
```bash
python build_interactive.py
# Open 04_Interactive_Explanation.html in browser
```

### Step 8: Deploy
```bash
copy 04_Interactive_Explanation.html index.html
git add . && git commit -m "feat: Add new model" && git push
```

## draw_light.py API Reference

| Function | Signature | Purpose |
|---|---|---|
| `setup_fig` | `(w=24, h=14)` | Create matplotlib figure |
| `draw_block` | `(ax, x, y, w, h, label, color, bg_color, icon, fontsize, rx, border_w, sublabel, gid)` | Labeled rectangle with shadow |
| `draw_small_block` | `(ax, x, y, w, h, label, color, bg_color, fontsize, gid)` | Compact block without shadow |
| `draw_circle` | `(ax, cx, cy, r, label, color, bg_color, fontsize, gid)` | Circle element (summation, etc.) |
| `draw_triangle` | `(ax, x, y, w, h, label, color, fontsize, gid)` | Triangle element (gain blocks) |
| `draw_ortho_arrow` | `(ax, pts, color, lw, label, label_pos, style, zorder, gid)` | Orthogonal routed wire with arrowhead |
| `draw_section` | `(ax, x, y, w, h, label, color)` | Dashed region boundary |
| `save_fig` | `(fig, path, dpi=300)` | Export to PNG/SVG/PDF |
| `GridBuilder` | `(start_x, start_y, spacing_x, spacing_y)` | Auto-positioning helper |

### Color Palette (COLORS dict)
```
ai/ai_bg, pv/pv_bg, fopid/fopid_bg, vfd/vfd_bg, pump/pump_bg,
mpc_mgr/mpc_mgr_bg, mpc/mpc_bg, tank/tank_bg, demand/demand_bg,
fw/fw_bg, gain/gain_bg, const/const_bg, clock/clock_bg,
mux/mux_bg, sum, int/int_bg, sat/sat_bg, delay/delay_bg
```

## Interactive Features (build_interactive.py)

### Control Center Options
| Feature | Implementation | Toggle |
|---|---|---|
| Auto-tracking camera | `flyTo()` during simulation | Checkbox `#autoCam` |
| Sidebar show/hide | CSS display toggle | Checkbox `#toggleSidebar` |
| Dark mode | `body.dark` CSS class | Checkbox `#toggleDark` |
| Simulation speed | Slider 0.5x-2x, affects `dt` | Range `#simSpeed` |
| 8K PNG export | Canvas 4x viewBox | Button |
| SVG export | XMLSerializer | Button |
| Language toggle | `toggleLanguage()` | Button `#langToggle` |

### Simulation Animation System
Phases are timed with `setTimeout()`, speed-adjusted by `dt = 1/speed`:
1. Each phase calls `flyTo()` to animate camera
2. `addFlow()` adds CSS classes for wire/block animation
3. `updateSimText()` updates sidebar with phase description
4. Phase 7 resets view and marks simulation complete

### Language System
- `window._L` stores current language dictionary
- `toggleLanguage()` updates ALL visible text elements
- Block explanations use `data.text_en` when `lang === 'en'`
- Simulation phases read from `window._L.p1t`, `window._L.p1`, etc.
- Direction stays RTL always (no LTR flip)

## Common Errors & Solutions

| Error | Cause | Solution |
|---|---|---|
| `KeyError` in Python | JS `{}` not doubled | Double ALL JS braces: `{{}}` |
| `ValueError: Single '}'` | Unmatched brace | Find and double all `}` in JS |
| SVG not responsive | `width`/`height` attrs | Run through `clean_svg()` |
| Blocks not clickable | Missing `gid` | Add `gid='...'` to `draw_block()` |
| Arabic text garbled | Wrong encoding | Use `encoding='utf-8'` everywhere |
| Export blurry | Canvas too small | Multiply viewBox by 4 for 8K |
| UI partially translated | Missing i18n entries | Update `toggleLanguage()` L dict |
| Orphan `}` breaks CSS | Regex script corruption | Never use regex refactoring |
| Duplicate functions | Bad merge/edit | Always check for conflicts before editing |

## File Size Expectations
- `draw_light.py`: ~7KB (stable, rarely changes)
- `build_interactive.py`: ~35-42KB (grows with explanations & i18n)
- `slx_parser.py`: ~4KB (stable tool)
- Generated HTML: ~300-400KB (mostly SVG data)
- SVG files: ~60-155KB each
