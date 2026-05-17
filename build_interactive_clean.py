import os
import json
import re

explanations = {
    # ====== ROOT DIAGRAM ======
    'block_pv': {'title': 'Solar Power Model (PV Physics)', 'text': '╪º┘ä┘å┘à┘ê╪░╪¼ ╪º┘ä┘ü┘è╪▓┘è╪º╪ª┘è ┘ä┘ä┘ê╪¡ ╪º┘ä╪┤┘à╪│┘è. ┘è╪│╪¬┘é╪¿┘ä ╪º┘ä╪Ñ╪┤╪╣╪º╪╣ ┘ê╪º┘ä╪¡╪▒╪º╪▒╪⌐ ┘ê┘è╪¡╪│╪¿ ╪º┘ä╪╖╪º┘é╪⌐ ╪º┘ä┘â┘ç╪▒╪¿╪º╪ª┘è╪⌐ P_pv.'},
    'block_fopid': {'title': 'Fractional Order PID', 'text': '╪º┘ä┘à╪¬╪¡┘â┘à ╪º┘ä╪¬┘å╪º╪│╪¿┘è ╪º┘ä╪¬┘â╪º┘à┘ä┘è ╪º┘ä╪¬┘ü╪º╪╢┘ä┘è ╪º┘ä┘â╪│╪▒┘è. ┘è╪╣╪╖┘è ╪º╪│╪¬╪¼╪º╪¿╪⌐ ╪¬╪¡┘â┘à ┘à╪▒┘å╪⌐ ╪¼╪»╪º┘ï ┘ä┘ä╪¬┘è╪º╪▒ ┘ê╪º┘ä╪╖╪º┘é╪⌐.'},
    'block_vfd': {'title': 'Variable Frequency Drive', 'text': '╪º┘ä╪╣╪º┘â╪│ ╪º┘ä╪░┘è ┘è┘à╪» ╪º┘ä┘à╪╢╪«╪⌐ ╪¿╪º┘ä╪¼┘ç╪» ┘ê╪º┘ä╪¬╪▒╪»╪» ╪º┘ä┘à┘å╪º╪│╪¿┘è┘å ┘ä╪¬╪╣┘à┘ä ╪¿╪º┘ä┘â┘ü╪º╪í╪⌐ ╪º┘ä┘à╪╖┘ä┘ê╪¿╪⌐.'},
    'block_pump': {'title': 'Motor & Pump Drive', 'text': '╪º┘ä┘à╪¡╪▒┘â ╪º┘ä╪░┘è ┘è┘ê┘ä╪» ╪╖╪º┘é╪⌐ ╪¡╪▒┘â┘è╪⌐ ┘ä╪╢╪« ╪º┘ä┘à┘è╪º┘ç ╪¿┘å╪º╪í┘ï ╪╣┘ä┘ë ╪╖╪º┘é╪⌐ ╪º┘ä╪╣╪º┘â╪│.'},
    'block_tank': {'title': 'Water Tank', 'text': '╪º┘ä╪«╪▓╪º┘å. ┘è╪╣╪¬┘à╪» ╪╣┘ä┘ë ┘à┘ê╪º╪▓┘å╪⌐ ╪º┘ä┘â╪¬┘ä╪⌐ ┘ä╪¡╪│╪º╪¿ ┘à╪│╪¬┘ê┘ë ╪º┘ä┘à┘è╪º┘ç.'},
    'block_demand': {'title': 'Water Demand Profile', 'text': '╪¡╪¼┘à ╪º┘ä┘à┘è╪º┘ç ╪º┘ä┘à╪│╪¬┘ç┘ä┘â╪⌐ ╪º┘ä┘à╪¬╪║┘è╪▒ ╪▓┘à┘å┘è╪º┘ï.'},
    'block_ai': {'title': 'AI Neural Predictor', 'text': '╪º┘ä╪┤╪¿┘â╪⌐ ╪º┘ä╪╣╪╡╪¿┘è╪⌐ ┘ä┘ä╪¬┘å╪¿╪ñ ╪¿╪º┘ä╪Ñ╪┤╪╣╪º╪╣ ╪º┘ä┘à╪│╪¬┘é╪¿┘ä┘è.'},
    'block_mpc_mgr': {'title': 'MPC Manager', 'text': '╪º┘ä┘à╪»┘è╪▒ ╪º┘ä┘à╪▒╪¼╪╣┘è. ┘è╪¡╪│╪¿ ╪º┘ä┘à╪│╪º╪▒ ╪º┘ä┘à╪½╪º┘ä┘è ┘ä┘ä╪¬╪¡┘â┘à.'},
    'block_mpc_ctrl': {'title': 'MPC Controller', 'text': '┘à╪¬╪¡┘â┘à ╪º┘ä╪╖╪¿┘é╪⌐ ╪º┘ä╪│┘ü┘ä┘è╪⌐. ┘è┘ê┘ä╪» ╪ú┘ê╪º┘à╪▒ ╪º┘ä╪¬╪¡┘â┘à ╪¿╪»┘é╪⌐ ╪▒┘è╪º╪╢┘è╪⌐ ╪╣╪º┘ä┘è╪⌐.'},
    
    # Root Small Blocks
    'block_gain_root': {'title': 'Flow Conversion Gain', 'text': '┘è╪¡┘ê┘ä ╪º┘ä╪¬╪»┘ü┘é ╪º┘ä╪«╪º┘à ╪Ñ┘ä┘ë ╪¬╪»┘ü┘é ┘à╪╣┘è╪º╪▒┘è ╪»╪º╪«┘ä ╪º┘ä╪«╪▓╪º┘å.'},
    'block_day_root': {'title': 'Day Selector', 'text': '┘è╪¡╪»╪» ╪º┘ä╪ú┘è╪º┘à ╪º┘ä╪¬╪º╪▒┘è╪«┘è╪⌐ ┘ä╪¬╪│┘ä┘è┘à┘ç╪º ┘ä┘ä╪░┘â╪º╪í ╪º┘ä╪º╪╡╪╖┘å╪º╪╣┘è.'},
    'block_time_root': {'title': 'Simulation Clock', 'text': '┘à╪ñ┘é╪¬ ╪º┘ä┘à╪¡╪º┘â╪º╪⌐. ┘è╪╢┘à┘å ╪º┘ä╪¬╪▓╪º┘à┘å ╪º┘ä╪»┘é┘è┘é ┘ä┘ä╪╣┘à┘ä┘è╪º╪¬.'},
    'block_delay_root': {'title': 'Discrete Delay (z^-1)', 'text': '╪¬╪ú╪«┘è╪▒ ╪▓┘à┘å┘è ┘è╪¡╪º┘â┘è ╪¬╪ú╪«╪▒ ┘ê╪╡┘ê┘ä ┘é╪▒╪º╪í╪º╪¬ ╪º┘ä╪¡╪│╪º╪│╪º╪¬ ╪º┘ä╪¡┘é┘è┘é┘è╪⌐.'},
    'block_ghi_in': {'title': 'Solar Irradiance (GHI)', 'text': '╪º┘ä╪Ñ╪┤╪╣╪º╪╣ ╪º┘ä╪┤┘à╪│┘è ╪º┘ä╪«╪º┘à.'},
    'block_temp_in': {'title': 'Ambient Temperature', 'text': '╪»╪▒╪¼╪⌐ ╪º┘ä╪¡╪▒╪º╪▒╪⌐ ╪º┘ä╪¿┘è╪ª┘è╪⌐.'},
    'block_mux_1': {'title': 'Input Multiplexer 1', 'text': '┘è╪¼┘à╪╣ ╪º┘ä┘à╪»╪«┘ä╪º╪¬ ┘é╪¿┘ä ╪¬┘ê╪¼┘è┘ç┘ç╪º ┘ä┘ä┘ê╪¡ ╪º┘ä╪┤┘à╪│┘è.'},
    'block_mux_2': {'title': 'Input Multiplexer 2', 'text': '┘è╪¼┘à╪╣ ╪º┘ä┘à╪»╪«┘ä╪º╪¬ ┘é╪¿┘ä ╪¬┘ê╪¼┘è┘ç┘ç╪º ┘ä┘ä┘ê╪¡ ╪º┘ä╪┤┘à╪│┘è.'},
    
    # ====== AI BLOCK DIAGRAM ======
    'ai_day': {'title': 'Day Selection Input', 'text': '╪Ñ╪┤╪º╪▒╪⌐ ╪º┘ä┘è┘ê┘à ╪º┘ä┘à╪▒╪º╪» ╪º┘ä╪¬┘å╪¿╪ñ ╪¿┘ç.'},
    'ai_mux1': {'title': 'Future Data Multiplexer', 'text': '┘è╪¼┘à╪╣ ╪ú┘è╪º┘à ╪º┘ä┘à╪│╪¬┘é╪¿┘ä ┘â┘à╪¬╪¼┘ç ┘ê╪º╪¡╪».'},
    'ai_mux2': {'title': 'Historical Data Multiplexer', 'text': '┘è╪¼┘à╪╣ ╪¿┘è╪º┘å╪º╪¬ ╪º┘ä╪¬╪º╪▒┘è╪« ┘ê╪º┘ä╪│┘è╪º┘é ╪º┘ä╪▓┘à┘å┘è.'},
    'ai_demux': {'title': '1:4 Demultiplexer', 'text': '┘è┘ü╪╡┘ä ╪º┘ä┘à╪¬╪¼┘ç╪º╪¬ ┘ä┘ä╪¬╪╣╪º┘à┘ä ┘à╪╣┘ç╪º ╪¿╪┤┘â┘ä ┘ü╪▒╪»┘è.'},
    'ai_mux_41': {'title': '4:1 Multiplexer', 'text': '┘è╪╣┘è╪» ╪»┘à╪¼ ╪º┘ä╪¿┘è╪º┘å╪º╪¬ ╪º┘ä┘à┘å┘é╪º╪⌐.'},
    'ai_transpose': {'title': 'Matrix Transpose', 'text': '╪¬╪╣╪»┘è┘ä ╪┤┘â┘ä ╪º┘ä┘à╪╡┘ü┘ê┘ü╪⌐ ┘ä╪¬┘ä╪º╪ª┘à ┘à╪»╪«┘ä╪º╪¬ ╪º┘ä╪┤╪¿┘â╪⌐ ╪º┘ä╪╣╪╡╪¿┘è╪⌐.'},
    'ai_clock': {'title': 'Local Clock', 'text': '┘à╪ñ┘é╪¬ ┘à╪¬╪▓╪º┘à┘å ╪«╪º╪╡ ╪¿╪¿┘ä┘ê┘â ╪º┘ä╪░┘â╪º╪í ╪º┘ä╪º╪╡╪╖┘å╪º╪╣┘è.'},
    'ai_nn': {'title': 'PI-HybridNet', 'text': '╪»╪º┘ä╪⌐ ┘à╪º╪¬┘ä╪º╪¿ ╪º┘ä┘à╪»┘à╪¼ ╪¿┘ç╪º ╪ú┘ê╪▓╪º┘å ╪º┘ä╪┤╪¿┘â╪⌐ ╪º┘ä╪╣╪╡╪¿┘è╪⌐ ┘ä╪¡╪│╪º╪¿ ╪º┘ä╪¬┘å╪¿╪ñ ╪º┘ä┘å┘ç╪º╪ª┘è.'},
    'ai_out_ghi': {'title': 'Predicted GHI', 'text': '┘å╪º╪¬╪¼ ╪º┘ä╪¬┘å╪¿╪ñ ╪¿╪º┘ä╪Ñ╪┤╪╣╪º╪╣ ╪º┘ä╪┤┘à╪│┘è.'},
    'ai_out_v': {'title': 'Future Vector', 'text': '┘à╪¬╪¼┘ç ╪º┘ä╪¿┘è╪º┘å╪º╪¬ ╪º┘ä┘à╪│╪¬┘é╪¿┘ä┘è╪⌐ ╪º┘ä┘à╪╣╪º┘ä╪¼.'},
    
    # ====== WATER TANK DIAGRAM ======
    'wt_qin': {'title': 'Inlet Flow (Qin)', 'text': '╪º┘ä┘à┘è╪º┘ç ╪º┘ä┘à╪¬╪»┘ü┘é╪⌐ ┘à┘å ╪º┘ä┘à╪╢╪«╪⌐ ╪Ñ┘ä┘ë ╪º┘ä╪«╪▓╪º┘å.'},
    'wt_qout': {'title': 'Outlet Flow (Qout)', 'text': '╪º┘ä┘à┘è╪º┘ç ╪º┘ä┘à╪│╪¡┘ê╪¿╪⌐ ┘à┘å ╪º┘ä╪«╪▓╪º┘å.'},
    'wt_sum': {'title': 'Flow Summation', 'text': '┘è╪¡╪│╪¿ ╪º┘ä┘ü╪▒┘é (Delta Q) ╪¿┘è┘å ╪º┘ä┘à┘è╪º┘ç ╪º┘ä╪»╪º╪«┘ä╪⌐ ┘ê╪º┘ä╪«╪º╪▒╪¼╪⌐.'},
    'wt_gain': {'title': 'Area Inverse (1/A)', 'text': '┘è┘é╪│┘à ╪¬╪»┘ü┘é ╪º┘ä┘à┘è╪º┘ç ╪╣┘ä┘ë ┘à╪│╪º╪¡╪⌐ ╪º┘ä╪«╪▓╪º┘å ┘ä╪¬╪¡┘ê┘è┘ä┘ç ╪Ñ┘ä┘ë ╪º╪▒╪¬┘ü╪º╪╣.'},
    'wt_int': {'title': 'Integrator (1/s)', 'text': '┘è╪¼┘à╪╣ ╪º┘ä╪¬╪║┘è╪▒╪º╪¬ ┘ü┘è ╪º┘ä╪º╪▒╪¬┘ü╪º╪╣ ╪╣╪¿╪▒ ╪º┘ä╪▓┘à┘å ┘ä┘ä╪¡╪╡┘ê┘ä ╪╣┘ä┘ë ╪º┘ä┘à╪│╪¬┘ê┘ë ╪º┘ä┘â┘ä┘è.'},
    'wt_sat': {'title': 'Saturation', 'text': '┘è╪╢┘à┘å ╪╣╪»┘à ╪¬╪¼╪º┘ê╪▓ ╪º┘ä┘à╪│╪¬┘ê┘ë ┘ä╪│╪╣╪⌐ ╪º┘ä╪«╪▓╪º┘å ╪ú┘ê ┘ç╪¿┘ê╪╖┘ç ╪¬╪¡╪¬ ╪º┘ä╪╡┘ü╪▒.'},
    'wt_ht': {'title': 'Tank Level (H)', 'text': '┘à╪│╪¬┘ê┘ë ╪º┘ä┘à┘è╪º┘ç ╪º┘ä┘ü╪╣┘ä┘è.'}
}

# Add dynamic inputs for root and AI
for i in range(3): explanations[f'block_ghi_{i}'] = {'title': f'GHI Day {i+1}', 'text': '╪Ñ╪┤╪º╪▒╪⌐ ╪Ñ╪┤╪╣╪º╪╣ ╪┤┘à╪│┘è╪⌐ ┘à┘å┘ü╪╡┘ä╪⌐.'}
for i in range(3): explanations[f'block_tmp_{i}'] = {'title': f'Temp Day {i+1}', 'text': '╪Ñ╪┤╪º╪▒╪⌐ ╪»╪▒╪¼╪⌐ ╪¡╪▒╪º╪▒╪⌐ ┘à┘å┘ü╪╡┘ä╪⌐.'}
for i in range(3): explanations[f'ai_ghi_fut_{i}'] = {'title': f'Future GHI {i+1}', 'text': '╪¿┘è╪º┘å╪º╪¬ ┘à╪│╪¬┘é╪¿┘ä┘è╪⌐ ┘å╪╕╪▒┘è╪⌐.'}
for i in range(3): explanations[f'ai_hist_{i}'] = {'title': f'Historical Data {i+1}', 'text': '╪¿┘è╪º┘å╪º╪¬ ╪¬╪º╪▒┘è╪«┘è╪⌐ ┘â┘à╪▒╪¼╪╣ ┘ä┘ä╪┤╪¿┘â╪⌐.'}

html_template = """<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <title>╪┤╪▒╪¡ ┘à╪«╪╖╪╖╪º╪¬ ╪º┘ä╪¬╪¡┘â┘à ┘ê╪º┘ä┘à╪¡╪º┘â╪º╪⌐ ╪º┘ä╪¬┘ü╪º╪╣┘ä┘è╪⌐</title>
    <style>
        body {{ font-family: 'Segoe UI', Tahoma, Arial, sans-serif; background: #F8FAFC; margin: 0; display: flex; height: 100vh; overflow: hidden; }}
        #sidebar {{ width: 340px; min-width: 250px; max-width: 600px; background: #FFFFFF; box-shadow: -2px 0 10px rgba(0,0,0,0.1); padding: 30px; display: flex; flex-direction: column; z-index: 10; overflow-y: auto; resize: horizontal; direction: rtl; }}
        #main-content {{ flex: 1; display: flex; flex-direction: column; background: #F1F5F9; position: relative; overflow: hidden; }}
        
        .header-bar {{ display: flex; background: #FFFFFF; border-bottom: 1px solid #E2E8F0; align-items: center; padding: 0 10px; z-index: 5; }}
        .tabs {{ display: flex; flex: 1; }}
        .tab {{ padding: 15px 25px; cursor: pointer; color: #64748B; font-weight: bold; border-bottom: 3px solid transparent; transition: 0.2s; }}
        .tab:hover {{ color: #2563EB; }}
        .tab.active {{ color: #2563EB; border-bottom: 3px solid #2563EB; }}
        
        .btn-sim {{ background: #10B981; color: white; border: none; padding: 10px 20px; border-radius: 6px; font-weight: bold; cursor: pointer; margin-left: 20px; transition: 0.2s; }}
        .btn-sim:hover {{ background: #059669; transform: scale(1.05); }}
        .btn-sim.running {{ background: #EF4444; }}
        .btn-sim.running:hover {{ background: #DC2626; }}
        
        .svg-container {{ flex: 1; padding: 0; display: none; justify-content: center; align-items: center; overflow: hidden; cursor: grab; position: relative; }}
        .svg-container:active {{ cursor: grabbing; }}
        .svg-container.active {{ display: flex; }}
        
        /* SVG wrapper for zoom/pan transform */
        .zoom-wrapper {{ transform-origin: center; transition: transform 0.1s ease-out; width: 100%; height: 100%; display: flex; justify-content: center; align-items: center; }}
        
        svg {{ max-width: 95%; max-height: 95%; box-shadow: 0 10px 25px rgba(0,0,0,0.05); border-radius: 8px; background: white; }}
        
        h1 {{ font-size: 20px; color: #0F172A; border-bottom: 2px solid #E2E8F0; padding-bottom: 15px; margin-top: 0; }}
        #info-title {{ color: #2563EB; font-size: 18px; font-weight: bold; margin-bottom: 15px; }}
        #info-text {{ color: #475569; font-size: 15px; line-height: 1.8; }}
        .placeholder {{ color: #94A3B8; text-align: center; margin-top: 50px; font-size: 15px; line-height: 1.6; }}
        
        /* Interactive SVG Classes */
        .interactive-path {{ cursor: pointer; transition: all 0.2s; }}
        .interactive-path:hover {{ stroke: #3B82F6 !important; stroke-width: 4px !important; opacity: 0.8; fill-opacity: 0.9; }}
        .active-path {{ stroke: #2563EB !important; stroke-width: 5px !important; filter: drop-shadow(0 0 5px rgba(37,99,235,0.5)); }}
        
        /* Animation Classes */
        .flowing-path {{
            stroke-dasharray: 12 12;
            animation: dash 0.6s linear infinite;
            stroke: #F59E0B !important; 
            stroke-width: 4px !important;
            filter: drop-shadow(0 0 4px rgba(245, 158, 11, 0.8));
        }}
        @keyframes dash {{
            to {{ stroke-dashoffset: -24; }}
        }}
        .flowing-block {{
            stroke: #F59E0B !important;
            stroke-width: 3.5px !important;
            filter: drop-shadow(0 0 6px rgba(245, 158, 11, 0.6));
            transition: 0.3s;
        }}
        
        /* Control Center Styles */
        .btn-ctrl {{ background: #F1F5F9; color: #475569; border: 1px solid #CBD5E1; padding: 10px 15px; border-radius: 6px; font-weight: bold; cursor: pointer; transition: 0.2s; }}
        .btn-ctrl:hover {{ background: #E2E8F0; }}
        .ctrl-panel {{ display: none; position: absolute; top: 50px; right: 0; width: 240px; background: white; border: 1px solid #E2E8F0; box-shadow: 0 10px 25px rgba(0,0,0,0.1); border-radius: 8px; padding: 15px; z-index: 100; flex-direction: column; }}
        .ctrl-panel.active {{ display: flex; }}
        .ctrl-panel label {{ cursor: pointer; margin-bottom: 10px; display: flex; align-items: center; color: #334155; font-size: 14px; }}
        .ctrl-panel input[type="checkbox"] {{ margin-left: 8px; width: 16px; height: 16px; cursor: pointer; }}
        .btn-export {{ background: #2563EB; color: white; border: none; padding: 8px; border-radius: 4px; cursor: pointer; width: 100%; font-weight: bold; transition: 0.2s; }}
        .btn-export:hover {{ opacity: 0.9; transform: scale(1.02); }}
    </style>
</head>
<body>
    <div id="main-content">
        <div class="header-bar">
            <div class="tabs">
                <div class="tab active" onclick="switchTab(0)">╪º┘ä┘à╪«╪╖╪╖ ╪º┘ä╪▒╪ª┘è╪│┘è (Root)</div>
                <div class="tab" onclick="switchTab(1)">╪º┘ä╪░┘â╪º╪í ╪º┘ä╪º╪╡╪╖┘å╪º╪╣┘è (AI Block)</div>
                <div class="tab" onclick="switchTab(2)">╪«╪▓╪º┘å ╪º┘ä┘à┘è╪º┘ç (Water Tank)</div>
            </div>
            <div style="position: relative; margin-left: 15px; display: flex; align-items: center;">
                <button class="btn-ctrl" onclick="document.getElementById('ctrl-panel').classList.toggle('active')">ΓÜÖ∩╕Å ┘à╪▒┘â╪▓ ╪º┘ä╪¬╪¡┘â┘à</button>
                <div id="ctrl-panel" class="ctrl-panel">
                    <label><input type="checkbox" id="autoCam" checked> ≡ƒÄÑ ┘â╪º┘à┘è╪▒╪º ╪º┘ä╪¬╪¬╪¿╪╣ ╪º┘ä╪¬┘ä┘é╪º╪ª┘è</label>
                    <label><input type="checkbox" id="toggleSidebar" checked onchange="document.getElementById('sidebar').style.display = this.checked ? 'flex' : 'none'"> ≡ƒùé∩╕Å ╪╣╪▒╪╢ ╪┤╪▒┘è╪╖ ╪º┘ä╪┤╪▒╪¡</label>
                    <hr style="margin: 10px 0; border: 0; border-top: 1px solid #E2E8F0; width: 100%;">
                    <div style="margin-bottom: 5px; font-weight: bold; color: #475569; font-size: 13px;">ΓÅ▒∩╕Å ╪│╪▒╪╣╪⌐ ╪º┘ä┘à╪¡╪º┘â╪º╪⌐</div>
                    <input type="range" id="simSpeed" min="0.5" max="2" step="0.5" value="1" style="width: 100%; direction: ltr;">
                    <hr style="margin: 10px 0; border: 0; border-top: 1px solid #E2E8F0; width: 100%;">
                    <button class="btn-export" onclick="export4KPNG()">≡ƒôÑ ╪¬╪╡╪»┘è╪▒ 4K PNG</button>
                    <button class="btn-export" style="margin-top: 8px; background: #475569;" onclick="exportSVG()">≡ƒôÑ ╪¬╪╡╪»┘è╪▒ SVG ╪º┘ä╪ú╪╡┘ä┘è</button>
                </div>
            </div>
            <button id="simBtn" class="btn-sim" onclick="toggleSimulation()">Γû╢ ╪¬╪┤╪║┘è┘ä ╪º┘ä┘à╪¡╪º┘â╪º╪⌐</button>
        </div>
        
        <div class="svg-container active" id="tab0"><div class="zoom-wrapper" id="zoom0">{SVG_ROOT}</div></div>
        <div class="svg-container" id="tab1"><div class="zoom-wrapper" id="zoom1">{SVG_AI}</div></div>
        <div class="svg-container" id="tab2"><div class="zoom-wrapper" id="zoom2">{SVG_WT}</div></div>
    </div>
    
    <div id="sidebar">
        <h1>╪º┘ä╪¬┘ü╪º╪╡┘è┘ä ┘ê╪º┘ä╪┤╪▒╪¡</h1>
        <div id="info-content">
            <div class="placeholder">╪º┘å┘é╪▒ ╪╣┘ä┘ë ╪ú┘è ╪╣┘å╪╡╪▒ ╪ú┘ê ╪¿┘ä┘ê┘â ┘à┘ç┘à╪º ┘â╪º┘å ╪╡╪║┘è╪▒╪º┘ï ┘ä╪╣╪▒╪╢ ╪┤╪▒╪¡┘ç ╪º┘ä╪¬┘ü╪╡┘è┘ä┘è.<br><br>╪º╪╢╪║╪╖ ╪╣┘ä┘ë "╪¬╪┤╪║┘è┘ä ╪º┘ä┘à╪¡╪º┘â╪º╪⌐" ┘ä╪¬╪¬╪¿╪╣ ┘à╪│╪º╪▒ ╪º┘ä╪Ñ╪┤╪º╪▒╪º╪¬ ┘ê╪º┘ä╪╖╪º┘é╪⌐ ╪╣╪¿╪▒ ╪º┘ä╪ú╪│┘ä╪º┘â ┘ê╪º┘ä╪¿┘ä┘ê┘â╪º╪¬.<br><br>≡ƒÆí ┘è┘à┘â┘å┘â ╪º╪│╪¬╪«╪»╪º┘à ╪╣╪¼┘ä╪⌐ ╪º┘ä┘ü╪ú╪▒╪⌐ (Scroll) ┘ä┘ä╪¬┘â╪¿┘è╪▒ ┘ê╪º┘ä╪│╪¡╪¿ ┘ä┘ä╪¬╪¡╪▒┘è┘â.</div>
        </div>
    </div>

    <script>
        const explanations = {EXPLANATIONS_JSON};
        let currentActive = null;
        let isSimulating = false;
        let simIntervals = [];

        function switchTab(index) {{
            document.querySelectorAll('.tab').forEach((t, i) => t.classList.toggle('active', i === index));
            document.querySelectorAll('.svg-container').forEach((c, i) => c.classList.toggle('active', i === index));
            // When switching tabs, we can run a micro-simulation specific to that tab if we are simulating
        }}

        // Set up interactivity for elements
        document.querySelectorAll('svg g').forEach(group => {{
            const id = group.id;
            if (explanations[id]) {{
                const paths = group.querySelectorAll('path, rect, polygon, circle');
                // The main visible shape is usually the last or second to last
                let targetPath = paths.length > 1 ? paths[paths.length-1] : paths[0];
                if(targetPath) setupInteractivePath(group, targetPath, id);
            }} else if (id && (id.startsWith('block_') || id.startsWith('ai_') || id.startsWith('wt_'))) {{
                // Try to make any known prefix clickable even if no strict explanation is defined
                if(explanations[id]) {{
                    const paths = group.querySelectorAll('path, rect');
                    if(paths.length > 0) setupInteractivePath(group, paths[paths.length-1], id);
                }}
            }}
        }});
        
        // Directly ID'd elements (like small blocks without groups)
        Object.keys(explanations).forEach(id => {{
            const el = document.getElementById(id);
            if (el && el.tagName !== 'g') {{
                 const paths = el.querySelectorAll('path, rect, polygon, circle');
                 let targetPath = paths.length > 1 ? paths[paths.length-1] : paths[0];
                 if(targetPath) setupInteractivePath(el, targetPath, id);
                 else setupInteractivePath(el, el, id); // self
            }}
        }});

        function setupInteractivePath(group, path, id) {{
            path.classList.add('interactive-path');
            group.style.cursor = 'pointer';
            group.addEventListener('click', function(e) {{
                e.stopPropagation();
                if (currentActive) currentActive.classList.remove('active-path');
                path.classList.add('active-path');
                currentActive = path;
                const data = explanations[id];
                document.getElementById('info-content').innerHTML = `
                    <div id="info-title">${{data.title}}</div>
                    <div id="info-text">${{data.text}}</div>
                `;
            }});
        }}

        function toggleSimulation() {{
            const btn = document.getElementById('simBtn');
            if (isSimulating) {{
                stopSimulation();
                btn.innerHTML = 'Γû╢ ╪¬╪┤╪║┘è┘ä ╪º┘ä┘à╪¡╪º┘â╪º╪⌐';
                btn.classList.remove('running');
                isSimulating = false;
            }} else {{
                switchTab(0); // Run root simulation
                startRootSimulation();
                btn.innerHTML = 'Γûá ╪Ñ┘è┘é╪º┘ü ╪º┘ä┘à╪¡╪º┘â╪º╪⌐';
                btn.classList.add('running');
                isSimulating = true;
            }}
        }}

        function stopSimulation() {{
            simIntervals.forEach(clearTimeout);
            simIntervals = [];
            document.querySelectorAll('.flowing-path, .flowing-block').forEach(el => {{
                el.classList.remove('flowing-path', 'flowing-block');
            }});
            document.getElementById('info-content').innerHTML = '<div class="placeholder">╪¬┘à ╪Ñ┘è┘é╪º┘ü ╪º┘ä┘à╪¡╪º┘â╪º╪⌐. ╪º┘å┘é╪▒ ╪╣┘ä┘ë ╪º┘ä╪¿┘ä┘ê┘â╪º╪¬ ┘ä┘ä╪¬╪╡┘ü╪¡ ╪º┘ä╪¡┘Å╪▒.</div>';
        }}

        function addFlow(selector, type='path') {{
            document.querySelectorAll(selector).forEach(el => {{
                if(el.tagName === 'g') {{
                    el.querySelectorAll('path, polygon, rect').forEach(p => p.classList.add(type === 'path' ? 'flowing-path' : 'flowing-block'));
                }} else {{
                    el.classList.add(type === 'path' ? 'flowing-path' : 'flowing-block');
                }}
            }});
        }}

        function updateSimText(title, text) {{
            document.getElementById('info-content').innerHTML = `
                <div id="info-title" style="color: #F59E0B;">≡ƒöä ${{title}}</div>
                <div id="info-text">${{text}}</div>
            `;
        }}

        function flyTo(x, y, scale, index) {{
            if (!document.getElementById('autoCam').checked) return;
            const wrapper = document.getElementById('zoom' + index);
            wrapper.style.transition = 'transform 1.5s ease-in-out';
            scales[index] = scale;
            translates[index].x = x;
            translates[index].y = y;
            wrapper.style.transform = `translate(${{x}}px, ${{y}}px) scale(${{scale}})`;
            
            // Remove transition after flight to allow snappy manual panning
            setTimeout(() => {{
                wrapper.style.transition = 'transform 0.1s ease-out';
            }}, 1600);
        }}

        function startRootSimulation() {{
            stopSimulation();
            switchTab(0);
            
            const speed = parseFloat(document.getElementById('simSpeed').value) || 1;
            const dt = 1 / speed;
            
            // Phase 1
            simIntervals.push(setTimeout(() => {{
                flyTo(250, 50, 1.3, 0);
                addFlow('[id^="path_in_"], [id^="path_ghi"], [id^="path_temp"], [id^="path_day_"]');
                addFlow('#block_mux_1, #block_mux_2, #block_day_root', 'block');
                updateSimText('╪º┘ä┘à╪▒╪¡┘ä╪⌐ 1: ╪¬╪¼┘à┘è╪╣ ╪º┘ä╪Ñ╪┤╪º╪▒╪º╪¬', '┘è╪¬┘à ╪º┘ä╪¬┘é╪º╪╖ ┘é╪▒╪º╪í╪º╪¬ ╪º┘ä╪Ñ╪┤╪╣╪º╪╣ ╪º┘ä╪┤┘à╪│┘è ┘ê╪º┘ä╪¡╪▒╪º╪▒╪⌐ ┘ê╪¬┘à╪▒┘è╪▒┘ç╪º ╪╣╪¿╪▒ ╪º┘ä┘Ç Multiplexers ┘å╪¡┘ê ╪º┘ä╪╖╪¿┘é╪⌐ ╪º┘ä┘ü┘è╪▓┘è╪º╪ª┘è╪⌐. ┘â┘à╪º ┘è╪¬┘à ╪º╪«╪¬┘è╪º╪▒ ╪º┘ä┘è┘ê┘à ╪º┘ä┘à╪╖┘ä┘ê╪¿ ┘ê╪º╪▒╪│╪º┘ä┘ç ┘ä┘ä╪░┘â╪º╪í ╪º┘ä╪º╪╡╪╖┘å╪º╪╣┘è.');
            }}, 500 * dt));

            // Phase 2
            simIntervals.push(setTimeout(() => {{
                flyTo(150, -150, 1.4, 0);
                addFlow('#block_ai', 'block');
                addFlow('[id^="path_ai_"]');
                updateSimText('╪º┘ä┘à╪▒╪¡┘ä╪⌐ 2: ╪º┘ä╪¬┘å╪¿╪ñ (╪º┘ä╪░┘â╪º╪í ╪º┘ä╪º╪╡╪╖┘å╪º╪╣┘è)', '┘è╪│╪¬┘é╪¿┘ä ╪º┘ä╪░┘â╪º╪í ╪º┘ä╪º╪╡╪╖┘å╪º╪╣┘è ╪¿┘è╪º┘å╪º╪¬ ╪º┘ä┘è┘ê┘à ┘ê┘è╪¿╪»╪ú ╪¿╪¡╪│╪º╪¿ ╪º┘ä╪Ñ╪┤╪╣╪º╪╣ ╪º┘ä┘à╪¬┘ê┘é╪╣ GHI_pred ┘ê╪¬┘à╪▒┘è╪▒┘ç ┘ä┘à╪»┘è╪▒ ╪º┘ä╪¬╪¡┘â┘à.');
            }}, 3500 * dt));

            // Phase 3
            simIntervals.push(setTimeout(() => {{
                flyTo(-100, -150, 1.4, 0);
                addFlow('#block_mpc_mgr', 'block');
                addFlow('[id^="path_mgr_"]');
                addFlow('[id^="path_clock"], #block_time_root', 'block');
                updateSimText('╪º┘ä┘à╪▒╪¡┘ä╪⌐ 3: ╪º┘ä╪¬┘ê╪¼┘è┘ç ╪º┘ä┘à╪▒╪¼╪╣┘è', '┘è╪¡╪│╪¿ ╪º┘ä┘à╪»┘è╪▒ ╪º┘ä┘à╪▒╪¼╪╣┘è MPC Manager ╪º┘ä╪¬╪»┘ü┘é ╪º┘ä┘à╪│╪¬┘ç╪»┘ü (Q_ref) ┘ê┘è╪▒╪│┘ä┘ç ┘â╪Ñ╪┤╪º╪▒╪⌐ ╪¬╪║╪░┘è╪⌐ ╪ú┘à╪º┘à┘è╪⌐ (Feedforward) ┘ä┘ä╪╣╪º┘â╪│ ┘à╪¿╪º╪┤╪▒╪⌐╪î ┘ê┘â┘ç╪»┘ü ┘ä┘ä┘à╪¬╪¡┘â┘à ╪º┘ä╪│┘ü┘ä┘è.');
            }}, 6500 * dt));

            // Phase 4
            simIntervals.push(setTimeout(() => {{
                flyTo(-300, -150, 1.4, 0);
                addFlow('#block_mpc_ctrl', 'block');
                addFlow('[id^="path_mpc_cmd"]');
                updateSimText('╪º┘ä┘à╪▒╪¡┘ä╪⌐ 4: ╪º┘ä╪¡╪│╪º╪¿╪º╪¬ ╪º┘ä╪▒┘è╪º╪╢┘è╪⌐ (╪º┘ä╪¬╪¡┘â┘à)', '┘è┘é┘ê┘à ┘à╪¬╪¡┘â┘à MPC Controller ╪¿╪¡┘ä ┘à╪╣╪º╪»┘ä╪º╪¬ Optimization ┘à╪╣┘é╪»╪⌐ ┘ä╪╢┘à╪º┘å ╪º╪│╪¬┘é╪▒╪º╪▒ ╪º┘ä╪«╪▓╪º┘å ┘ê╪º┘ä┘à╪╢╪«╪⌐ ┘à╪╣╪º┘ï╪î ╪½┘à ┘è╪╡╪»╪▒ ╪Ñ╪┤╪º╪▒╪⌐ ╪º┘ä╪¬╪¡┘â┘à (Command) ┘ä┘à╪¬╪¡┘â┘à ╪º┘ä┘ü┘ê┘ä╪¬┘è╪⌐.');
            }}, 9500 * dt));

            // Phase 5
            simIntervals.push(setTimeout(() => {{
                flyTo(-150, 150, 1.3, 0);
                addFlow('#block_pv, #block_fopid, #block_vfd, #block_pump', 'block');
                addFlow('[id^="path_pv"], [id^="path_fopid"], [id^="path_vfd"], [id^="path_pump"]');
                updateSimText('╪º┘ä┘à╪▒╪¡┘ä╪⌐ 5: ╪¬╪┤╪║┘è┘ä ╪º┘ä┘à╪╢╪«╪⌐ ┘ê╪¬╪»┘ü┘é ╪º┘ä╪╖╪º┘é╪⌐', '┘è╪¬┘à ╪º╪│╪¬╪«╪▒╪º╪¼ ╪º┘ä╪╖╪º┘é╪⌐ ┘à┘å ╪º┘ä┘ä┘ê╪¡ ╪º┘ä╪┤┘à╪│┘è P_pv╪î ╪½┘à ╪¬╪¬┘ê┘ä┘ë ╪º┘ä┘Ç FOPID ╪¬┘å┘é┘è╪⌐ ╪º┘ä╪╖╪º┘é╪⌐ ╪º┘ä╪░╪º┘ç╪¿╪⌐ ┘ä┘ä┘Ç VFD ┘ä╪¬╪┤╪║┘è┘ä ╪º┘ä┘à╪╢╪«╪⌐ ┘ê╪Ñ┘å╪¬╪º╪¼ ╪º┘ä╪¬╪»┘ü┘é Q_raw.');
            }}, 12500 * dt));

            // Phase 6
            simIntervals.push(setTimeout(() => {{
                flyTo(-450, 50, 1.4, 0);
                addFlow('#block_gain_root, #block_tank, #block_demand', 'block');
                addFlow('[id^="path_gain"], [id^="path_tank_out"], [id^="path_demand"]');
                addFlow('[id^="path_fb_"]');
                addFlow('#block_delay_root', 'block');
                updateSimText('╪º┘ä┘à╪▒╪¡┘ä╪⌐ 6: ┘à┘ê╪º╪▓┘å╪⌐ ╪º┘ä╪«╪▓╪º┘å ┘ê╪º┘ä╪¬╪║╪░┘è╪⌐ ╪º┘ä╪▒╪º╪¼╪╣╪⌐', '┘è╪╡┘ä ╪º┘ä╪¬╪»┘ü┘é ┘ä┘ä╪«╪▓╪º┘å╪î ┘ê╪¬┘Å╪¡╪│╪¿ ╪º┘ä╪▓┘è╪º╪»╪⌐ ┘ü┘è ╪º┘ä┘à┘å╪│┘ê╪¿ H(t). ╪½┘à ╪¬╪╣┘ê╪» ╪º┘ä╪Ñ╪┤╪º╪▒╪⌐ ┘â┘Ç Feedback ┘ü┘è ╪º┘ä┘à╪│╪º╪▒ ╪º┘ä╪│┘ü┘ä┘è ╪º┘ä╪╖┘ê┘è┘ä ┘ê╪¬┘à╪▒ ╪╣╪¿╪▒ ╪º┘ä┘Ç Delay ╪º╪│╪¬╪╣╪»╪º╪»╪º┘ï ┘ä┘ä╪½╪º┘å┘è╪⌐ ╪º┘ä┘é╪º╪»┘à╪⌐.');
            }}, 15500 * dt));
            
            // Phase 7 Reset View
            simIntervals.push(setTimeout(() => {{
                flyTo(0, 0, 1, 0);
                updateSimText('╪º┘â╪¬┘à┘ä╪¬ ╪º┘ä┘à╪¡╪º┘â╪º╪⌐', '╪»┘ê╪▒╪⌐ ╪º┘ä╪¬╪¡┘â┘à ╪º┘â╪¬┘à┘ä╪¬ ╪¿┘å╪¼╪º╪¡. ┘è┘à┘â┘å┘â ╪Ñ╪╣╪º╪»╪⌐ ╪º┘ä╪¬╪┤╪║┘è┘ä ╪ú┘ê ╪º┘ä╪¬╪╡┘ü╪¡ ╪º┘ä╪¡┘Å╪▒.');
                document.getElementById('simBtn').innerHTML = 'Γû╢ ╪Ñ╪╣╪º╪»╪⌐ ╪º┘ä┘à╪¡╪º┘â╪º╪⌐';
                document.getElementById('simBtn').classList.remove('running');
                isSimulating = false;
            }}, 21000 * dt));
        }}
        // Pan and Zoom Logic
        let scales = [1, 1, 1];
        let translates = [{{x:0, y:0}}, {{x:0, y:0}}, {{x:0, y:0}}];
        let isPanning = false;
        let startX = 0, startY = 0;
        let currentTabIndex = 0;

        document.querySelectorAll('.svg-container').forEach((container, index) => {{
            const wrapper = document.getElementById('zoom' + index);
            
            container.addEventListener('mousedown', (e) => {{
                // Only prevent panning if clicking an interactive element
                const group = e.target.closest('g');
                const isInteractiveGroup = group && explanations[group.id];
                const isInteractivePath = e.target.closest('.interactive-path') || e.target.classList.contains('interactive-path');
                
                if(isInteractiveGroup || isInteractivePath) return; 

                isPanning = true;
                currentTabIndex = index;
                startX = e.clientX - translates[index].x;
                startY = e.clientY - translates[index].y;
            }});

            container.addEventListener('mousemove', (e) => {{
                if (!isPanning || currentTabIndex !== index) return;
                translates[index].x = e.clientX - startX;
                translates[index].y = e.clientY - startY;
                wrapper.style.transform = `translate(${{translates[index].x}}px, ${{translates[index].y}}px) scale(${{scales[index]}})`;
            }});

            container.addEventListener('mouseup', () => isPanning = false);
            container.addEventListener('mouseleave', () => isPanning = false);

            container.addEventListener('wheel', (e) => {{
                e.preventDefault();
                const delta = e.deltaY > 0 ? 0.9 : 1.1;
                
                // Zoom towards mouse position
                const rect = container.getBoundingClientRect();
                const mouseX = e.clientX - rect.left;
                const mouseY = e.clientY - rect.top;
                
                const oldScale = scales[index];
                scales[index] *= delta;
                
                // Limit zoom
                scales[index] = Math.max(0.2, Math.min(scales[index], 5));
                
                // Adjust translation to zoom to pointer
                translates[index].x = mouseX - (mouseX - translates[index].x) * (scales[index] / oldScale);
                translates[index].y = mouseY - (mouseY - translates[index].y) * (scales[index] / oldScale);
                
                wrapper.style.transform = `translate(${{translates[index].x}}px, ${{translates[index].y}}px) scale(${{scales[index]}})`;
            }});
        }});
        
        // Export Functions
        function getActiveSVG() {{
            return document.querySelector('.svg-container.active svg');
        }}

        function exportSVG() {{
            const svg = getActiveSVG();
            if(!svg) return;
            const serializer = new XMLSerializer();
            let source = serializer.serializeToString(svg);
            if(!source.match(/^<svg[^>]+xmlns="http\\:\\/\\/www\\.w3\\.org\\/2000\\/svg"/)){{
                source = source.replace(/^<svg/, '<svg xmlns="http://www.w3.org/2000/svg"');
            }}
            const url = "data:image/svg+xml;charset=utf-8," + encodeURIComponent(source);
            const a = document.createElement("a");
            a.href = url;
            a.download = "simulink_diagram.svg";
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
        }}

        function export4KPNG() {{
            const svg = getActiveSVG();
            if(!svg) return;
            const serializer = new XMLSerializer();
            let source = serializer.serializeToString(svg);
            if(!source.match(/^<svg[^>]+xmlns="http\\:\\/\\/www\\.w3\\.org\\/2000\\/svg"/)){{
                source = source.replace(/^<svg/, '<svg xmlns="http://www.w3.org/2000/svg"');
            }}
            
            // Parse Matplotlib viewBox for high native resolution
            const viewBox = svg.getAttribute('viewBox').split(' ');
            let width = parseFloat(viewBox[2]);
            let height = parseFloat(viewBox[3]);
            
            if (!width) {{ width = 3840; height = 2160; }} // 4K Fallback
            
            const canvas = document.createElement('canvas');
            canvas.width = width;
            canvas.height = height;
            const ctx = canvas.getContext('2d');
            
            // Force white background
            ctx.fillStyle = '#FFFFFF';
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            
            const img = new Image();
            const url = "data:image/svg+xml;charset=utf-8," + encodeURIComponent(source);
            img.onload = function() {{
                ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
                const a = document.createElement("a");
                a.download = "simulink_diagram_highres.png";
                a.href = canvas.toDataURL("image/png");
                document.body.appendChild(a);
                a.click();
                document.body.removeChild(a);
            }};
            img.src = url;
        }}
        
        // Close Control Panel if clicked outside
        document.addEventListener('click', (e) => {{
            const panel = document.getElementById('ctrl-panel');
            const btn = document.querySelector('.btn-ctrl');
            if (panel.classList.contains('active') && !panel.contains(e.target) && e.target !== btn) {{
                panel.classList.remove('active');
            }}
        }});
    </script>
</body>
</html>
"""

def clean_svg(svg_str):
    if svg_str.startswith('<?xml'):
        svg_str = svg_str.split('?>', 1)[1]
    svg_str = re.sub(r'width="[^"]+"', '', svg_str, count=1)
    svg_str = re.sub(r'height="[^"]+"', '', svg_str, count=1)
    return svg_str

def read_svg(filename):
    with open(rf'c:\Users\Mohammed26\Desktop\┘à╪«╪╖╪╖ ╪│┘è┘à┘ê┘ä┘è╪┤┘å\{filename}', 'r', encoding='utf-8') as f:
        return clean_svg(f.read())

svg_root = read_svg('01_Root_Level_Final.svg')
svg_ai = read_svg('02_AI_BLOCK_Final.svg')
svg_wt = read_svg('03_Water_Tank_Final.svg')

html_content = html_template.format(
    SVG_ROOT=svg_root,
    SVG_AI=svg_ai,
    SVG_WT=svg_wt,
    EXPLANATIONS_JSON=json.dumps(explanations, ensure_ascii=False)
)

html_path = r'c:\Users\Mohammed26\Desktop\┘à╪«╪╖╪╖ ╪│┘è┘à┘ê┘ä┘è╪┤┘å\04_Interactive_Explanation.html'
with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html_content)

print("Advanced Interactive HTML Generated with all missing elements.")
