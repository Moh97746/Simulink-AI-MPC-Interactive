<div align="center">
  
# ⚙️ Simulink-to-Web Interactive Skill
### Professional Agentic Skill for Converting MATLAB Simulink Models into Interactive Web Diagrams

[![Live Demo](https://img.shields.io/badge/🚀_Live_Interactive_Demo-Click_Here-2563EB?style=for-the-badge&logo=html5)](https://Marco9249.github.io/Simulink-AI-MPC-Interactive/)

</div>

---

## 🌟 Overview

**Simulink-to-Web** is an advanced AI Agent Skill designed to automatically parse, layout, and convert any MATLAB Simulink (`.slx`) file into a highly professional, interactive, and animated HTML web page. 

This repository serves as the home for the skill's source code, alongside a **fully functional demonstration** of a complex AI-MPC Solar Water Pumping project generated entirely by this skill.

### 🎯 What This Skill Does

1. **Auto-Parsing:** Extracts blocks, subsystems, and wiring directly from `.slx` files.
2. **Vector Graphics (SVG):** Generates publication-quality, scalable vector diagrams.
3. **Interactive UI:** Wraps the diagrams in a single-file HTML interface featuring:
   - 🖱️ **Clickable Elements:** Click any block to view its technical explanation.
   - ▶️ **Animated Simulation:** Visualizes signal and power flow with camera tracking.
   - 🌐 **Bilingual Support (i18n):** Real-time toggle between English and Arabic.
   - 🌙 **Dark Mode:** Elegant dark theme for comfortable viewing.
   - 📥 **8K Export:** Ultra-high resolution PNG exports for academic papers.

---

## 🚀 Live Demonstration

The `index.html` file in this repository is the output of this skill applied to a complex **Simulink AI-MPC Solar Water Pumping System**. 

👉 **[Click Here to Experience the Live Demo](https://Marco9249.github.io/Simulink-AI-MPC-Interactive/)**

---

## 📁 Repository Structure

To keep the workspace clean and focused solely on the skill, this repository contains **only the essential toolset** and the final generated interactive demo:

```text
├── draw_light.py           # 🎨 Core vector drawing library (matplotlib → SVG)
├── slx_parser.py           # 🔍 Auto-extractor for reading Simulink .slx files
├── build_interactive.py    # 🏗️ HTML assembler (injects SVGs + JS interactivity + i18n)
├── SKILL_GUIDE.md          # 📖 Comprehensive manual and prompt-guide for AI Agents
├── index.html              # 🌐 The final interactive demo (GitHub Pages)
└── README.md               # ℹ️ This documentation
```

---

## 🛠️ How to Use (For AI Agents & Developers)

If you are an AI assistant or a developer looking to use this skill on a new `.slx` file, follow the detailed instructions in the **[SKILL_GUIDE.md](SKILL_GUIDE.md)**.

### Quick Workflow:
1. `python slx_parser.py your_model.slx` → Generates layout script.
2. Refine the generated Python layout script for perfect block positioning.
3. Run the layout script to generate `.svg` files.
4. Add your explanations and translations to `build_interactive.py`.
5. `python build_interactive.py` → Generates your final `index.html`!

---

## 📬 Contact & Author

Developed with precision for academic and professional engineering visualization.

**Email:** izzeldeenm@gmail.com  
**License:** MIT License
