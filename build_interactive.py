import os
import json
import re

explanations = {
    # ====== ROOT DIAGRAM ======
    'block_pv': {'title': 'Solar Power Model (PV Physics)', 'text': 'النموذج الفيزيائي للوح الشمسي. يستقبل الإشعاع والحرارة ويحسب الطاقة الكهربائية P_pv.'},
    'block_fopid': {'title': 'Fractional Order PID', 'text': 'المتحكم التناسبي التكاملي التفاضلي الكسري. يعطي استجابة تحكم مرنة جداً للتيار والطاقة.'},
    'block_vfd': {'title': 'Variable Frequency Drive', 'text': 'العاكس الذي يمد المضخة بالجهد والتردد المناسبين لتعمل بالكفاءة المطلوبة.'},
    'block_pump': {'title': 'Motor & Pump Drive', 'text': 'المحرك الذي يولد طاقة حركية لضخ المياه بناءً على طاقة العاكس.'},
    'block_tank': {'title': 'Water Tank', 'text': 'الخزان. يعتمد على موازنة الكتلة لحساب مستوى المياه.'},
    'block_demand': {'title': 'Water Demand Profile', 'text': 'حجم المياه المستهلكة المتغير زمنياً.'},
    'block_ai': {'title': 'AI Neural Predictor', 'text': 'الشبكة العصبية للتنبؤ بالإشعاع المستقبلي.'},
    'block_mpc_mgr': {'title': 'MPC Manager', 'text': 'المدير المرجعي. يحسب المسار المثالي للتحكم.'},
    'block_mpc_ctrl': {'title': 'MPC Controller', 'text': 'متحكم الطبقة السفلية. يولد أوامر التحكم بدقة رياضية عالية.'},
    
    # Root Small Blocks
    'block_gain_root': {'title': 'Flow Conversion Gain', 'text': 'يحول التدفق الخام إلى تدفق معياري داخل الخزان.'},
    'block_day_root': {'title': 'Day Selector', 'text': 'يحدد الأيام التاريخية لتسليمها للذكاء الاصطناعي.'},
    'block_time_root': {'title': 'Simulation Clock', 'text': 'مؤقت المحاكاة. يضمن التزامن الدقيق للعمليات.'},
    'block_delay_root': {'title': 'Discrete Delay (z^-1)', 'text': 'تأخير زمني يحاكي تأخر وصول قراءات الحساسات الحقيقية.'},
    'block_ghi_in': {'title': 'Solar Irradiance (GHI)', 'text': 'الإشعاع الشمسي الخام.'},
    'block_temp_in': {'title': 'Ambient Temperature', 'text': 'درجة الحرارة البيئية.'},
    'block_mux_1': {'title': 'Input Multiplexer 1', 'text': 'يجمع المدخلات قبل توجيهها للوح الشمسي.'},
    'block_mux_2': {'title': 'Input Multiplexer 2', 'text': 'يجمع المدخلات قبل توجيهها للوح الشمسي.'},
    
    # ====== AI BLOCK DIAGRAM ======
    'ai_day': {'title': 'Day Selection Input', 'text': 'إشارة اليوم المراد التنبؤ به.'},
    'ai_mux1': {'title': 'Future Data Multiplexer', 'text': 'يجمع أيام المستقبل كمتجه واحد.'},
    'ai_mux2': {'title': 'Historical Data Multiplexer', 'text': 'يجمع بيانات التاريخ والسياق الزمني.'},
    'ai_demux': {'title': '1:4 Demultiplexer', 'text': 'يفصل المتجهات للتعامل معها بشكل فردي.'},
    'ai_mux_41': {'title': '4:1 Multiplexer', 'text': 'يعيد دمج البيانات المنقاة.'},
    'ai_transpose': {'title': 'Matrix Transpose', 'text': 'تعديل شكل المصفوفة لتلائم مدخلات الشبكة العصبية.'},
    'ai_clock': {'title': 'Local Clock', 'text': 'مؤقت متزامن خاص ببلوك الذكاء الاصطناعي.'},
    'ai_nn': {'title': 'PI-HybridNet', 'text': 'دالة ماتلاب المدمج بها أوزان الشبكة العصبية لحساب التنبؤ النهائي.'},
    'ai_out_ghi': {'title': 'Predicted GHI', 'text': 'ناتج التنبؤ بالإشعاع الشمسي.'},
    'ai_out_v': {'title': 'Future Vector', 'text': 'متجه البيانات المستقبلية المعالج.'},
    
    # ====== WATER TANK DIAGRAM ======
    'wt_qin': {'title': 'Inlet Flow (Qin)', 'text': 'المياه المتدفقة من المضخة إلى الخزان.'},
    'wt_qout': {'title': 'Outlet Flow (Qout)', 'text': 'المياه المسحوبة من الخزان.'},
    'wt_sum': {'title': 'Flow Summation', 'text': 'يحسب الفرق (Delta Q) بين المياه الداخلة والخارجة.'},
    'wt_gain': {'title': 'Area Inverse (1/A)', 'text': 'يقسم تدفق المياه على مساحة الخزان لتحويله إلى ارتفاع.'},
    'wt_int': {'title': 'Integrator (1/s)', 'text': 'يجمع التغيرات في الارتفاع عبر الزمن للحصول على المستوى الكلي.'},
    'wt_sat': {'title': 'Saturation', 'text': 'يضمن عدم تجاوز المستوى لسعة الخزان أو هبوطه تحت الصفر.'},
    'wt_ht': {'title': 'Tank Level (H)', 'text': 'مستوى المياه الفعلي.'}
}

# Add dynamic inputs for root and AI
for i in range(3): explanations[f'block_ghi_{i}'] = {'title': f'GHI Day {i+1}', 'text': 'إشارة إشعاع شمسية منفصلة.'}
for i in range(3): explanations[f'block_tmp_{i}'] = {'title': f'Temp Day {i+1}', 'text': 'إشارة درجة حرارة منفصلة.'}
for i in range(3): explanations[f'ai_ghi_fut_{i}'] = {'title': f'Future GHI {i+1}', 'text': 'بيانات مستقبلية نظرية.'}
for i in range(3): explanations[f'ai_hist_{i}'] = {'title': f'Historical Data {i+1}', 'text': 'بيانات تاريخية كمرجع للشبكة.'}

# Mirror vertical blocks
vertical_explanations = {}
for k, v in explanations.items():
    if k.startswith('block_') or k.startswith('path_') or k.startswith('ai_') or k.startswith('wt_'):
        vertical_explanations['v_' + k] = v
explanations.update(vertical_explanations)

html_template = """<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <title>شرح مخططات التحكم والمحاكاة التفاعلية</title>
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
        
        .telemetry-overlay {{ position: absolute; top: 120px; left: 30px; background: rgba(15, 23, 42, 0.85); color: #F8FAFC; padding: 20px; border-radius: 12px; font-family: monospace; font-size: 16px; border: 1px solid #334155; box-shadow: 0 10px 25px rgba(0,0,0,0.2); z-index: 50; display: flex; flex-direction: column; gap: 10px; transition: 0.3s; backdrop-filter: blur(4px); }}
        .telemetry-item {{ display: flex; justify-content: space-between; gap: 20px; }}
        .telemetry-val {{ font-weight: bold; color: #10B981; }}
        
        body.cloudy-mode .flowing-path {{ stroke: #94A3B8 !important; filter: drop-shadow(0 0 4px rgba(148, 163, 184, 0.8)); }}
        body.cloudy-mode .flowing-block {{ stroke: #94A3B8 !important; filter: drop-shadow(0 0 4px rgba(148, 163, 184, 0.8)); }}
        
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
                <div class="tab active" onclick="switchTab(0)">المخطط الرئيسي (Root)</div>
                <div class="tab" onclick="switchTab(1)">الذكاء الاصطناعي (AI Block)</div>
                <div class="tab" onclick="switchTab(2)">خزان المياه (Water Tank)</div>
            </div>
            <div style="position: relative; margin-left: 15px; display: flex; align-items: center;">
                <button class="btn-ctrl" onclick="document.getElementById('ctrl-panel').classList.toggle('active')">⚙️ مركز التحكم</button>
                <div id="ctrl-panel" class="ctrl-panel">
                    <label><input type="checkbox" id="autoCam" checked> 🎥 كاميرا التتبع التلقائي</label>
                    <label><input type="checkbox" id="toggleSidebar" checked onchange="document.getElementById('sidebar').style.display = this.checked ? 'flex' : 'none'"> 🗂️ عرض شريط الشرح</label>
                    <label><input type="checkbox" id="toggleVertical" onchange="toggleVerticalLayout(this.checked)"> 📄 التخطيط العمودي (Vertical)</label>
                    <label><input type="checkbox" id="toggleTelemetry" checked onchange="document.getElementById('telemetry-box').style.display = this.checked ? 'flex' : 'none'"> 📊 لوحة القياسات الحية</label>
                    <label><input type="checkbox" id="toggleWeather" onchange="document.body.classList.toggle('cloudy-mode', this.checked)"> ☁️ محاكاة يوم غائم</label>
                    <hr style="margin: 10px 0; border: 0; border-top: 1px solid #E2E8F0; width: 100%;">
                    <div style="margin-bottom: 5px; font-weight: bold; color: #475569; font-size: 13px;">⏱️ سرعة المحاكاة</div>
                    <input type="range" id="simSpeed" min="0.5" max="2" step="0.5" value="1" style="width: 100%; direction: ltr;">
                    <hr style="margin: 10px 0; border: 0; border-top: 1px solid #E2E8F0; width: 100%;">
                    <button class="btn-export" onclick="export4KPNG()">📥 تصدير 4K PNG</button>
                    <button class="btn-export" style="margin-top: 8px; background: #475569;" onclick="exportSVG()">📥 تصدير SVG الأصلي</button>
                </div>
            </div>
            <button id="simBtn" class="btn-sim" onclick="toggleSimulation()">▶ تشغيل المحاكاة</button>
        </div>
        
        <div class="svg-container active" id="tab0"><div class="zoom-wrapper" id="zoom0">{SVG_ROOT}</div></div>
        <div class="svg-container" id="tab0_v"><div class="zoom-wrapper" id="zoom0_v">{SVG_ROOT_V}</div></div>
        <div class="svg-container" id="tab1"><div class="zoom-wrapper" id="zoom1">{SVG_AI}</div></div>
        <div class="svg-container" id="tab2"><div class="zoom-wrapper" id="zoom2">{SVG_WT}</div></div>
        
        <div id="telemetry-box" class="telemetry-overlay">
            <div style="color: #60A5FA; font-weight: bold; border-bottom: 1px solid #334155; padding-bottom: 5px; margin-bottom: 5px;">LIVE TELEMETRY</div>
            <div class="telemetry-item"><span>GHI:</span> <span id="tel-ghi" class="telemetry-val">0 W/m²</span></div>
            <div class="telemetry-item"><span>Temp:</span> <span id="tel-temp" class="telemetry-val">25 °C</span></div>
            <div class="telemetry-item"><span>Q_ref:</span> <span id="tel-qref" class="telemetry-val">0.0 L/s</span></div>
            <div class="telemetry-item"><span>H(t):</span> <span id="tel-h" class="telemetry-val">3.50 m</span></div>
        </div>
    </div>
    
    <div id="sidebar">
        <h1>التفاصيل والشرح</h1>
        <div id="info-content">
            <div class="placeholder">انقر على أي عنصر أو بلوك مهما كان صغيراً لعرض شرحه التفصيلي.<br><br>اضغط على "تشغيل المحاكاة" لتتبع مسار الإشارات والطاقة عبر الأسلاك والبلوكات.<br><br>💡 يمكنك استخدام عجلة الفأرة (Scroll) للتكبير والسحب للتحريك.</div>
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
                btn.innerHTML = '▶ تشغيل المحاكاة';
                btn.classList.remove('running');
                isSimulating = false;
            }} else {{
                switchTab(0); // Run root simulation
                startRootSimulation();
                btn.innerHTML = '■ إيقاف المحاكاة';
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
            document.getElementById('info-content').innerHTML = '<div class="placeholder">تم إيقاف المحاكاة. انقر على البلوكات للتصفح الحُر.</div>';
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
                <div id="info-title" style="color: #F59E0B;">🔄 ${{title}}</div>
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
            const isVertical = document.getElementById('toggleVertical').checked;
            switchTab(isVertical ? '0_v' : 0);
            
            const isCloudy = document.getElementById('toggleWeather').checked;
            document.getElementById('tel-ghi').innerText = '0 W/m²';
            document.getElementById('tel-temp').innerText = '25 °C';
            document.getElementById('tel-qref').innerText = '0.0 L/s';
            document.getElementById('tel-h').innerText = '3.50 m';
            
            const speed = parseFloat(document.getElementById('simSpeed').value) || 1;
            const dt = 1 / speed;
            
            // Phase 1
            simIntervals.push(setTimeout(() => {{
                if(!isVertical) flyTo(250, 50, 1.3, 0); else flyTo(0, 300, 1.2, '0_v');
                addFlow('[id^="path_in_"], [id^="path_ghi"], [id^="path_temp"], [id^="path_day_"]');
                addFlow('[id^="v_path_in_"], [id^="v_path_ghi"], [id^="v_path_temp"], [id^="v_path_day"]');
                addFlow('#block_mux_1, #block_mux_2, #block_day_root, #v_block_mux_1, #v_block_mux_2, #v_block_day_root', 'block');
                document.getElementById('tel-ghi').innerText = isCloudy ? '250 W/m²' : '850 W/m²';
                updateSimText('المرحلة 1: تجميع الإشارات', 'يتم التقاط قراءات الإشعاع الشمسي والحرارة وتمريرها عبر الـ Multiplexers نحو الطبقة الفيزيائية. كما يتم اختيار اليوم المطلوب وارساله للذكاء الاصطناعي.');
            }}, 500 * dt));

            // Phase 2
            simIntervals.push(setTimeout(() => {{
                if(!isVertical) flyTo(150, -150, 1.4, 0); else flyTo(0, 100, 1.2, '0_v');
                addFlow('#block_ai, #v_block_ai', 'block');
                addFlow('[id^="path_ai_"], [id^="v_path_ai_"]');
                updateSimText('المرحلة 2: التنبؤ (الذكاء الاصطناعي)', 'يستقبل الذكاء الاصطناعي بيانات اليوم ويبدأ بحساب الإشعاع المتوقع GHI_pred وتمريره لمدير التحكم.');
            }}, 3500 * dt));

            // Phase 3
            simIntervals.push(setTimeout(() => {{
                if(!isVertical) flyTo(-100, -150, 1.4, 0); else flyTo(0, 50, 1.2, '0_v');
                addFlow('#block_mpc_mgr, #v_block_mpc_mgr', 'block');
                addFlow('[id^="path_mgr_"], [id^="v_path_mgr"]');
                addFlow('[id^="path_clock"], #block_time_root, [id^="v_path_clock"], #v_block_time_root', 'block');
                document.getElementById('tel-qref').innerText = isCloudy ? '1.8 L/s' : '4.2 L/s';
                updateSimText('المرحلة 3: التوجيه المرجعي', 'يحسب المدير المرجعي MPC Manager التدفق المستهدف (Q_ref) ويرسله كإشارة تغذية أمامية (Feedforward) للعاكس مباشرة، وكهدف للمتحكم السفلي.');
            }}, 6500 * dt));

            // Phase 4
            simIntervals.push(setTimeout(() => {{
                if(!isVertical) flyTo(-300, -150, 1.4, 0); else flyTo(0, -50, 1.2, '0_v');
                addFlow('#block_mpc_ctrl, #v_block_mpc_ctrl', 'block');
                addFlow('[id^="path_mpc_cmd"], [id^="v_path_mpc_cmd"]');
                updateSimText('المرحلة 4: الحسابات الرياضية (التحكم)', 'يقوم متحكم MPC Controller بحل معادلات Optimization معقدة لضمان استقرار الخزان والمضخة معاً، ثم يصدر إشارة التحكم (Command) لمتحكم الفولتية.');
            }}, 9500 * dt));

            // Phase 5
            simIntervals.push(setTimeout(() => {{
                if(!isVertical) flyTo(-150, 150, 1.3, 0); else flyTo(0, -150, 1.2, '0_v');
                addFlow('#block_pv, #block_fopid, #block_vfd, #block_pump, #v_block_pv, #v_block_fopid, #v_block_vfd, #v_block_pump', 'block');
                addFlow('[id^="path_pv"], [id^="path_fopid"], [id^="path_vfd"], [id^="path_pump"], [id^="v_path_pv"], [id^="v_path_fopid"], [id^="v_path_pump"]');
                updateSimText('المرحلة 5: تشغيل المضخة وتدفق الطاقة', 'يتم استخراج الطاقة من اللوح الشمسي P_pv، ثم تتولى الـ FOPID تنقية الطاقة الذاهبة للـ VFD لتشغيل المضخة وإنتاج التدفق Q_raw.');
            }}, 12500 * dt));

            // Phase 6
            simIntervals.push(setTimeout(() => {{
                if(!isVertical) flyTo(-450, 50, 1.4, 0); else flyTo(0, -300, 1.2, '0_v');
                addFlow('#block_gain_root, #block_tank, #block_demand, #v_block_gain_root, #v_block_tank, #v_block_demand', 'block');
                addFlow('[id^="path_gain"], [id^="path_tank_out"], [id^="path_demand"], [id^="v_path_gain"], [id^="v_path_demand"]');
                addFlow('[id^="path_fb_"], [id^="v_path_fb_"]');
                addFlow('#block_delay_root, #v_block_delay_root', 'block');
                
                let hLevel = 3.50;
                let targetH = isCloudy ? 3.75 : 4.20;
                const hInterval = setInterval(() => {{
                    hLevel += 0.05;
                    document.getElementById('tel-h').innerText = hLevel.toFixed(2) + ' m';
                    if(hLevel >= targetH) clearInterval(hInterval);
                }}, 100);
                simIntervals.push(hInterval);
                
                updateSimText('المرحلة 6: موازنة الخزان والتغذية الراجعة', 'يصل التدفق للخزان، وتُحسب الزيادة في المنسوب H(t). ثم تعود الإشارة كـ Feedback في المسار السفلي الطويل وتمر عبر الـ Delay استعداداً للثانية القادمة.');
            }}, 15500 * dt));
            
            // Phase 7 Reset View
            simIntervals.push(setTimeout(() => {{
                if(!isVertical) flyTo(0, 0, 1, 0); else flyTo(0, 0, 1, '0_v');
                updateSimText('اكتملت المحاكاة', 'دورة التحكم اكتملت بنجاح. يمكنك إعادة التشغيل أو التصفح الحُر.');
                document.getElementById('simBtn').innerHTML = '▶ إعادة المحاكاة';
                document.getElementById('simBtn').classList.remove('running');
                isSimulating = false;
            }}, 21000 * dt));
        }}
        
        function toggleVerticalLayout(isVertical) {{
            if(isVertical) {{
                switchTab('0_v');
            }} else {{
                switchTab(0);
            }}
        }}
        // Pan and Zoom Logic
        let scales = {'0': 1, '1': 1, '2': 1, '0_v': 1};
        let translates = {'0': {x:0, y:0}, '1': {x:0, y:0}, '2': {x:0, y:0}, '0_v': {x:0, y:0}};
        let isPanning = false;
        let startX = 0, startY = 0;
        let currentTabIndex = 0;

        document.querySelectorAll('.svg-container').forEach((container) => {{
            const index = container.id.replace('tab', '');
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
    with open(rf'c:\Users\Mohammed26\Desktop\مخطط سيموليشن\{filename}', 'r', encoding='utf-8') as f:
        return clean_svg(f.read())

svg_root = read_svg('01_Root_Level_Final.svg')
svg_root_v = read_svg('01_Root_Level_Vertical_Final.svg')
svg_ai = read_svg('02_AI_BLOCK_Final.svg')
svg_wt = read_svg('03_Water_Tank_Final.svg')

html_content = html_template.format(
    SVG_ROOT=svg_root,
    SVG_ROOT_V=svg_root_v,
    SVG_AI=svg_ai,
    SVG_WT=svg_wt,
    EXPLANATIONS_JSON=json.dumps(explanations, ensure_ascii=False)
)

html_path = r'c:\Users\Mohammed26\Desktop\مخطط سيموليشن\04_Interactive_Explanation.html'
with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html_content)

print("Advanced Interactive HTML Generated with all missing elements.")
