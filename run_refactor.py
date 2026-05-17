import os
import re
import json

file_path = 'build_interactive.py'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update Explanations Dictionary with English
def add_en(explanations_str):
    return explanations_str.replace("'title':", "'title_ar':").replace("'text':", "'text_ar':")

new_exps = """explanations = {
    # ====== ROOT DIAGRAM ======
    'block_pv': {'title': 'Solar Power Model (PV Physics)', 'title_en': 'Solar Power Model (PV)', 'text': 'النموذج الفيزيائي للوح الشمسي. يستقبل الإشعاع والحرارة ويحسب الطاقة الكهربائية P_pv.', 'text_en': 'Physical model of the solar panel. Receives irradiance and temperature to calculate electrical power P_pv.'},
    'block_fopid': {'title': 'Fractional Order PID', 'title_en': 'Fractional Order PID', 'text': 'المتحكم التناسبي التكاملي التفاضلي الكسري. يعطي استجابة تحكم مرنة جداً للتيار والطاقة.', 'text_en': 'Fractional Order PID controller. Provides highly flexible control response for current and power.'},
    'block_vfd': {'title': 'Variable Frequency Drive', 'title_en': 'Variable Frequency Drive', 'text': 'العاكس الذي يمد المضخة بالجهد والتردد المناسبين لتعمل بالكفاءة المطلوبة.', 'text_en': 'The inverter that supplies the pump with the appropriate voltage and frequency to operate efficiently.'},
    'block_pump': {'title': 'Motor & Pump Drive', 'title_en': 'Motor & Pump Drive', 'text': 'المحرك الذي يولد طاقة حركية لضخ المياه بناءً على طاقة العاكس.', 'text_en': 'The motor that generates kinetic energy to pump water based on the inverter power.'},
    'block_tank': {'title': 'Water Tank', 'title_en': 'Water Tank', 'text': 'الخزان. يعتمد على موازنة الكتلة لحساب مستوى المياه.', 'text_en': 'The water tank. Relies on mass balance to calculate the water level.'},
    'block_demand': {'title': 'Water Demand Profile', 'title_en': 'Water Demand Profile', 'text': 'حجم المياه المستهلكة المتغير زمنياً.', 'text_en': 'Time-varying volume of consumed water.'},
    'block_ai': {'title': 'AI Neural Predictor', 'title_en': 'AI Neural Predictor', 'text': 'الشبكة العصبية للتنبؤ بالإشعاع المستقبلي.', 'text_en': 'Neural network for predicting future solar irradiance.'},
    'block_mpc_mgr': {'title': 'MPC Manager', 'title_en': 'MPC Manager', 'text': 'المدير المرجعي. يحسب المسار المثالي للتحكم.', 'text_en': 'The reference manager. Computes the optimal control trajectory.'},
    'block_mpc_ctrl': {'title': 'MPC Controller', 'title_en': 'MPC Controller', 'text': 'متحكم الطبقة السفلية. يولد أوامر التحكم بدقة رياضية عالية.', 'text_en': 'Low-level controller. Generates precise mathematical control commands.'},
    
    # Root Small Blocks
    'block_gain_root': {'title': 'Flow Conversion Gain', 'title_en': 'Flow Conversion Gain', 'text': 'يحول التدفق الخام إلى تدفق معياري داخل الخزان.', 'text_en': 'Converts raw flow into standardized flow inside the tank.'},
    'block_day_root': {'title': 'Day Selector', 'title_en': 'Day Selector', 'text': 'يحدد الأيام التاريخية لتسليمها للذكاء الاصطناعي.', 'text_en': 'Selects historical days to feed into the AI.'},
    'block_time_root': {'title': 'Simulation Clock', 'title_en': 'Simulation Clock', 'text': 'مؤقت المحاكاة. يضمن التزامن الدقيق للعمليات.', 'text_en': 'Simulation clock. Ensures precise synchronization of operations.'},
    'block_delay_root': {'title': 'Discrete Delay (z^-1)', 'title_en': 'Discrete Delay (z^-1)', 'text': 'تأخير زمني يحاكي تأخر وصول قراءات الحساسات الحقيقية.', 'text_en': 'Time delay simulating the latency of real sensor readings.'},
    'block_ghi_in': {'title': 'Solar Irradiance (GHI)', 'title_en': 'Solar Irradiance (GHI)', 'text': 'الإشعاع الشمسي الخام.', 'text_en': 'Raw solar irradiance.'},
    'block_temp_in': {'title': 'Ambient Temperature', 'title_en': 'Ambient Temperature', 'text': 'درجة الحرارة البيئية.', 'text_en': 'Ambient environmental temperature.'},
    'block_mux_1': {'title': 'Input Multiplexer 1', 'title_en': 'Input Multiplexer 1', 'text': 'يجمع المدخلات قبل توجيهها للوح الشمسي.', 'text_en': 'Combines inputs before routing them to the solar panel.'},
    'block_mux_2': {'title': 'Input Multiplexer 2', 'title_en': 'Input Multiplexer 2', 'text': 'يجمع المدخلات قبل توجيهها للوح الشمسي.', 'text_en': 'Combines inputs before routing them to the solar panel.'},
    
    # ====== AI BLOCK DIAGRAM ======
    'ai_day': {'title': 'Day Selection Input', 'title_en': 'Day Selection Input', 'text': 'إشارة اليوم المراد التنبؤ به.', 'text_en': 'The target day signal for prediction.'},
    'ai_mux1': {'title': 'Future Data Multiplexer', 'title_en': 'Future Data Multiplexer', 'text': 'يجمع أيام المستقبل كمتجه واحد.', 'text_en': 'Combines future days into a single vector.'},
    'ai_mux2': {'title': 'Historical Data Multiplexer', 'title_en': 'Historical Data Multiplexer', 'text': 'يجمع بيانات التاريخ والسياق الزمني.', 'text_en': 'Combines historical data and temporal context.'},
    'ai_demux': {'title': '1:4 Demultiplexer', 'title_en': '1:4 Demultiplexer', 'text': 'يفصل المتجهات للتعامل معها بشكل فردي.', 'text_en': 'Separates vectors for individual processing.'},
    'ai_mux_41': {'title': '4:1 Multiplexer', 'title_en': '4:1 Multiplexer', 'text': 'يعيد دمج البيانات المنقاة.', 'text_en': 'Re-merges the filtered data.'},
    'ai_transpose': {'title': 'Matrix Transpose', 'title_en': 'Matrix Transpose', 'text': 'تعديل شكل المصفوفة لتلائم مدخلات الشبكة العصبية.', 'text_en': 'Reshapes the matrix to fit neural network inputs.'},
    'ai_clock': {'title': 'Local Clock', 'title_en': 'Local Clock', 'text': 'مؤقت متزامن خاص ببلوك الذكاء الاصطناعي.', 'text_en': 'Synchronized clock specific to the AI block.'},
    'ai_nn': {'title': 'PI-HybridNet', 'title_en': 'PI-HybridNet', 'text': 'دالة ماتلاب المدمج بها أوزان الشبكة العصبية لحساب التنبؤ النهائي.', 'text_en': 'MATLAB function embedded with NN weights to compute the final prediction.'},
    'ai_out_ghi': {'title': 'Predicted GHI', 'title_en': 'Predicted GHI', 'text': 'ناتج التنبؤ بالإشعاع الشمسي.', 'text_en': 'The resulting solar irradiance prediction.'},
    'ai_out_v': {'title': 'Future Vector', 'title_en': 'Future Vector', 'text': 'متجه البيانات المستقبلية المعالج.', 'text_en': 'Processed future data vector.'},
    
    # ====== WATER TANK DIAGRAM ======
    'wt_qin': {'title': 'Inlet Flow (Qin)', 'title_en': 'Inlet Flow (Qin)', 'text': 'المياه المتدفقة من المضخة إلى الخزان.', 'text_en': 'Water flowing from the pump into the tank.'},
    'wt_qout': {'title': 'Outlet Flow (Qout)', 'title_en': 'Outlet Flow (Qout)', 'text': 'المياه المسحوبة من الخزان.', 'text_en': 'Water drawn from the tank.'},
    'wt_sum': {'title': 'Flow Summation', 'title_en': 'Flow Summation', 'text': 'يحسب الفرق (Delta Q) بين المياه الداخلة والخارجة.', 'text_en': 'Calculates the difference (Delta Q) between inlet and outlet water.'},
    'wt_gain': {'title': 'Area Inverse (1/A)', 'title_en': 'Area Inverse (1/A)', 'text': 'يقسم تدفق المياه على مساحة الخزان لتحويله إلى ارتفاع.', 'text_en': 'Divides water flow by tank area to convert it to height.'},
    'wt_int': {'title': 'Integrator (1/s)', 'title_en': 'Integrator (1/s)', 'text': 'يجمع التغيرات في الارتفاع عبر الزمن للحصول على المستوى الكلي.', 'text_en': 'Integrates height changes over time to get the total level.'},
    'wt_sat': {'title': 'Saturation', 'title_en': 'Saturation', 'text': 'يضمن عدم تجاوز المستوى لسعة الخزان أو هبوطه تحت الصفر.', 'text_en': 'Ensures the level does not exceed tank capacity or drop below zero.'},
    'wt_ht': {'title': 'Tank Level (H)', 'title_en': 'Tank Level (H)', 'text': 'مستوى المياه الفعلي.', 'text_en': 'The actual water level.'}
}

for i in range(3): explanations[f'block_ghi_{i}'] = {'title': f'GHI Day {i+1}', 'title_en': f'GHI Day {i+1}', 'text': 'إشارة إشعاع شمسية منفصلة.', 'text_en': 'Separate solar irradiance signal.'}
for i in range(3): explanations[f'block_tmp_{i}'] = {'title': f'Temp Day {i+1}', 'title_en': f'Temp Day {i+1}', 'text': 'إشارة درجة حرارة منفصلة.', 'text_en': 'Separate temperature signal.'}
for i in range(3): explanations[f'ai_ghi_fut_{i}'] = {'title': f'Future GHI {i+1}', 'title_en': f'Future GHI {i+1}', 'text': 'بيانات مستقبلية نظرية.', 'text_en': 'Theoretical future data.'}
for i in range(3): explanations[f'ai_hist_{i}'] = {'title': f'Historical Data {i+1}', 'title_en': f'Historical Data {i+1}', 'text': 'بيانات تاريخية كمرجع للشبكة.', 'text_en': 'Historical data as reference for the network.'}
"""

content = re.sub(r'explanations = \{.*?(?=html_template = )', new_exps + '\n', content, flags=re.DOTALL)

# 2. UI Modifications (Remove unwanted toggles and add Language Button)
content = re.sub(r'\.telemetry-overlay \{.*?\n.*?\.cloudy-mode \.flowing-block \{.*?\}', '', content, flags=re.DOTALL)
content = re.sub(r'<label><input type="checkbox" id="toggleVertical".*?<hr', '<hr', content, flags=re.DOTALL)
content = re.sub(r'<div class="svg-container" id="tab0_v">.*?</div>\n', '', content, flags=re.DOTALL)
content = re.sub(r'<div id="telemetry-box".*?</div>', '', content, flags=re.DOTALL)

# Add Lang toggle next to control center button
btn = r'<div style="display:flex;gap:10px;"><button class="btn-ctrl" id="langToggle" onclick="toggleLanguage()">🌐 English</button><button class="btn-ctrl" onclick="'
content = content.replace('<button class="btn-ctrl" onclick="', btn, 1)
content = content.replace('</button>\n                <div id="ctrl-panel"', '</button></div>\n                <div id="ctrl-panel"')

# 3. Revert Root Simulation
root_sim = """        function startRootSimulation() {
            stopSimulation();
            switchTab(0);
            
            const speed = parseFloat(document.getElementById('simSpeed').value) || 1;
            const dt = 1 / speed;
            
            // Phase 1
            simIntervals.push(setTimeout(() => {
                flyTo(250, 50, 1.3, 0);
                addFlow('[id^="path_in_"], [id^="path_ghi"], [id^="path_temp"], [id^="path_day_"]');
                addFlow('#block_mux_1, #block_mux_2, #block_day_root', 'block');
                updateSimText('phase1_title', 'phase1_text');
            }, 500 * dt));

            // Phase 2
            simIntervals.push(setTimeout(() => {
                flyTo(150, -150, 1.4, 0);
                addFlow('#block_ai', 'block');
                addFlow('[id^="path_ai_"]');
                updateSimText('phase2_title', 'phase2_text');
            }, 3500 * dt));

            // Phase 3
            simIntervals.push(setTimeout(() => {
                flyTo(-100, -150, 1.4, 0);
                addFlow('#block_mpc_mgr', 'block');
                addFlow('[id^="path_mgr_"]');
                addFlow('[id^="path_clock"], #block_time_root', 'block');
                updateSimText('phase3_title', 'phase3_text');
            }, 6500 * dt));

            // Phase 4
            simIntervals.push(setTimeout(() => {
                flyTo(-300, -150, 1.4, 0);
                addFlow('#block_mpc_ctrl', 'block');
                addFlow('[id^="path_mpc_cmd"]');
                updateSimText('phase4_title', 'phase4_text');
            }, 9500 * dt));

            // Phase 5
            simIntervals.push(setTimeout(() => {
                flyTo(-150, 150, 1.3, 0);
                addFlow('#block_pv, #block_fopid, #block_vfd, #block_pump', 'block');
                addFlow('[id^="path_pv"], [id^="path_fopid"], [id^="path_vfd"], [id^="path_pump"]');
                updateSimText('phase5_title', 'phase5_text');
            }, 12500 * dt));

            // Phase 6
            simIntervals.push(setTimeout(() => {
                flyTo(-450, 50, 1.4, 0);
                addFlow('#block_gain_root, #block_tank, #block_demand', 'block');
                addFlow('[id^="path_gain"], [id^="path_tank_out"], [id^="path_demand"]');
                addFlow('[id^="path_fb_"]');
                addFlow('#block_delay_root', 'block');
                updateSimText('phase6_title', 'phase6_text');
            }, 15500 * dt));
            
            // Phase 7 Reset View
            simIntervals.push(setTimeout(() => {
                flyTo(0, 0, 1, 0);
                updateSimText('phase7_title', 'phase7_text');
                const btn = document.getElementById('simBtn');
                btn.innerHTML = lang === 'ar' ? '▶ إعادة المحاكاة' : '▶ Re-run Simulation';
                btn.classList.remove('running');
                isSimulating = false;
            }, 21000 * dt));
        }"""
content = re.sub(r'function startRootSimulation\(\) \{.*?function toggleVerticalLayout\(isVertical\) \{.*?\}', root_sim, content, flags=re.DOTALL)

# Clean up SVG reading at the bottom
content = content.replace("svg_root_v = read_svg('01_Root_Level_Vertical_Final.svg')", "")
content = content.replace("SVG_ROOT_V=svg_root_v,", "")

# Replace .format with .replace in the python file writer to avoid KeyError with JS braces
fmt_change = """html_content = html_template.replace('{SVG_ROOT}', svg_root).replace('{SVG_AI}', svg_ai).replace('{SVG_WT}', svg_wt).replace('{EXPLANATIONS_JSON}', json.dumps(explanations, ensure_ascii=False))"""
content = re.sub(r'html_content = html_template\.format\(.*?ensure_ascii=False\)\n\)', fmt_change, content, flags=re.DOTALL)


# 4. Multiply PNG dimensions by 4 (8K resolution!)
content = content.replace('let width = parseFloat(viewBox[2]);\n            let height = parseFloat(viewBox[3]);', 'let width = parseFloat(viewBox[2]) * 4;\n            let height = parseFloat(viewBox[3]) * 4;')
content = content.replace('📥 تصدير 4K PNG', '📥 تصدير 8K PNG')

# 5. Inject i18n logic into JavaScript
i18n_script = """
        let lang = 'ar';
        const ui_dict = {
            'ar': {
                'tab0': 'المخطط الرئيسي (Root)', 'tab1': 'الذكاء الاصطناعي (AI Block)', 'tab2': 'خزان المياه (Water Tank)',
                'ctrl_btn': '⚙️ مركز التحكم', 'sim_btn_play': '▶ تشغيل المحاكاة', 'sim_btn_stop': '■ إيقاف المحاكاة',
                'lbl_cam': '🎥 كاميرا التتبع التلقائي', 'lbl_sidebar': '🗂️ عرض شريط الشرح', 'lbl_speed': '⏱️ سرعة المحاكاة',
                'btn_png': '📥 تصدير 8K PNG', 'btn_svg': '📥 تصدير SVG الأصلي',
                'sidebar_title': 'التفاصيل والشرح', 'sidebar_ph': 'انقر على أي عنصر أو بلوك لعرض شرحه التفصيلي.<br><br>اضغط على "تشغيل المحاكاة" لتتبع مسار الإشارات.<br><br>💡 يمكنك استخدام عجلة الفأرة (Scroll) للتكبير.',
                'stop_ph': 'تم إيقاف المحاكاة. انقر على البلوكات للتصفح الحُر.',
                'phase1_title': 'المرحلة 1: تجميع الإشارات', 'phase1_text': 'يتم التقاط قراءات الإشعاع الشمسي والحرارة وتمريرها عبر الـ Multiplexers نحو الطبقة الفيزيائية. كما يتم اختيار اليوم المطلوب وارساله للذكاء الاصطناعي.',
                'phase2_title': 'المرحلة 2: التنبؤ (الذكاء الاصطناعي)', 'phase2_text': 'يستقبل الذكاء الاصطناعي بيانات اليوم ويبدأ بحساب الإشعاع المتوقع GHI_pred وتمريره لمدير التحكم.',
                'phase3_title': 'المرحلة 3: التوجيه المرجعي', 'phase3_text': 'يحسب المدير المرجعي التدفق المستهدف (Q_ref) ويرسله كإشارة تغذية أمامية للعاكس، وكهدف للمتحكم السفلي.',
                'phase4_title': 'المرحلة 4: الحسابات الرياضية (التحكم)', 'phase4_text': 'يقوم متحكم MPC بحل معادلات Optimization معقدة لضمان استقرار الخزان والمضخة معاً، ثم يصدر إشارة التحكم لمتحكم الفولتية.',
                'phase5_title': 'المرحلة 5: تشغيل المضخة وتدفق الطاقة', 'phase5_text': 'يتم استخراج الطاقة من اللوح الشمسي P_pv، ثم تتولى الـ FOPID تنقية الطاقة الذاهبة للـ VFD لتشغيل المضخة وإنتاج التدفق Q_raw.',
                'phase6_title': 'المرحلة 6: موازنة الخزان والتغذية الراجعة', 'phase6_text': 'يصل التدفق للخزان، وتُحسب الزيادة في المنسوب H(t). ثم تعود الإشارة كـ Feedback في المسار السفلي الطويل وتمر عبر الـ Delay استعداداً للثانية القادمة.',
                'phase7_title': 'اكتملت المحاكاة', 'phase7_text': 'دورة التحكم اكتملت بنجاح. يمكنك إعادة التشغيل أو التصفح الحُر.'
            },
            'en': {
                'tab0': 'Root Diagram', 'tab1': 'AI Block Diagram', 'tab2': 'Water Tank Diagram',
                'ctrl_btn': '⚙️ Control Center', 'sim_btn_play': '▶ Run Simulation', 'sim_btn_stop': '■ Stop Simulation',
                'lbl_cam': '🎥 Auto Tracking Camera', 'lbl_sidebar': '🗂️ Show Sidebar', 'lbl_speed': '⏱️ Simulation Speed',
                'btn_png': '📥 Export 8K PNG', 'btn_svg': '📥 Export Raw SVG',
                'sidebar_title': 'Details & Explanation', 'sidebar_ph': 'Click on any element or block to view its detailed explanation.<br><br>Click "Run Simulation" to trace the signal paths.<br><br>💡 You can use the mouse wheel to zoom in/out.',
                'stop_ph': 'Simulation stopped. Click blocks to browse freely.',
                'phase1_title': 'Phase 1: Signal Gathering', 'phase1_text': 'Solar irradiance and temperature readings are captured and passed through Multiplexers to the physical layer. The target day is selected and sent to AI.',
                'phase2_title': 'Phase 2: Prediction (AI)', 'phase2_text': 'The AI receives the day data, computes the predicted irradiance (GHI_pred), and forwards it to the MPC Manager.',
                'phase3_title': 'Phase 3: Reference Guidance', 'phase3_text': 'The MPC Manager computes the target flow (Q_ref) and sends it as a feed-forward signal to the inverter, and as a reference to the controller.',
                'phase4_title': 'Phase 4: Optimization (Control)', 'phase4_text': 'The MPC Controller solves complex optimization equations to stabilize the tank and pump, then issues the command to the VFD.',
                'phase5_title': 'Phase 5: Pump & Power Flow', 'phase5_text': 'Power is extracted from the PV panel, FOPID purifies it, and VFD drives the pump to produce raw flow (Q_raw).',
                'phase6_title': 'Phase 6: Tank Balance & Feedback', 'phase6_text': 'Flow reaches the tank, changing the water level H(t). The signal returns as feedback through the delay block for the next cycle.',
                'phase7_title': 'Simulation Complete', 'phase7_text': 'Control cycle completed successfully. You can replay or explore.'
            }
        };
        
        function toggleLanguage() {
            lang = lang === 'ar' ? 'en' : 'ar';
            document.getElementById('langToggle').innerText = lang === 'ar' ? '🌐 English' : '🌐 عربي';
            document.documentElement.dir = lang === 'ar' ? 'rtl' : 'ltr';
            
            // Update UI
            document.querySelector('.tab:nth-child(1)').innerText = ui_dict[lang].tab0;
            document.querySelector('.tab:nth-child(2)').innerText = ui_dict[lang].tab1;
            document.querySelector('.tab:nth-child(3)').innerText = ui_dict[lang].tab2;
            document.querySelector('.btn-ctrl:not(#langToggle)').innerText = ui_dict[lang].ctrl_btn;
            document.getElementById('simBtn').innerText = isSimulating ? ui_dict[lang].sim_btn_stop : ui_dict[lang].sim_btn_play;
            
            document.querySelector('#ctrl-panel label:nth-child(1)').innerHTML = `<input type="checkbox" id="autoCam" ${document.getElementById('autoCam').checked ? 'checked' : ''}> ${ui_dict[lang].lbl_cam}`;
            document.querySelector('#ctrl-panel label:nth-child(2)').innerHTML = `<input type="checkbox" id="toggleSidebar" onchange="document.getElementById('sidebar').style.display = this.checked ? 'flex' : 'none'" ${document.getElementById('toggleSidebar').checked ? 'checked' : ''}> ${ui_dict[lang].lbl_sidebar}`;
            document.querySelector('#ctrl-panel div').innerText = ui_dict[lang].lbl_speed;
            document.querySelectorAll('.btn-export')[0].innerText = ui_dict[lang].btn_png;
            document.querySelectorAll('.btn-export')[1].innerText = ui_dict[lang].btn_svg;
            
            document.querySelector('#sidebar h1').innerText = ui_dict[lang].sidebar_title;
            if(!currentActive && !isSimulating) {
                document.getElementById('info-content').innerHTML = `<div class="placeholder">${ui_dict[lang].sidebar_ph}</div>`;
            } else if (currentActive) {
                // Re-trigger click to translate active block
                currentActive.parentNode.click();
            }
        }
        
        function updateSimText(titleKey, textKey) {
            document.getElementById('info-content').innerHTML = `
                <div id="info-title" style="color: #F59E0B;">🔄 ${ui_dict[lang][titleKey]}</div>
                <div id="info-text">${ui_dict[lang][textKey]}</div>
            `;
        }
"""
content = content.replace('const explanations = {EXPLANATIONS_JSON};', 'const explanations = {EXPLANATIONS_JSON};\n' + i18n_script)

# 6. Change JS Sidebar Logic to support language
js_click = """                const data = explanations[id];
                document.getElementById('info-content').innerHTML = `
                    <div id="info-title">${lang === 'ar' ? (data.title_ar || data.title) : (data.title_en || data.title)}</div>
                    <div id="info-text">${lang === 'ar' ? (data.text_ar || data.text) : (data.text_en || data.text)}</div>
                `;"""
content = re.sub(r'const data = explanations\[id\];.*?`;', js_click, content, flags=re.DOTALL)
content = content.replace("'info-content').innerHTML = '<div class=\"placeholder\">تم إيقاف المحاكاة. انقر على البلوكات للتصفح الحُر.</div>';", "'info-content').innerHTML = `<div class=\"placeholder\">${ui_dict[lang].stop_ph}</div>`;")

# Fix button labels inside toggleSimulation()
sim_toggle = """            if (isSimulating) {
                stopSimulation();
                btn.innerHTML = ui_dict[lang].sim_btn_play;
                btn.classList.remove('running');
                isSimulating = false;
            } else {
                switchTab(0); // Run root simulation
                startRootSimulation();
                btn.innerHTML = ui_dict[lang].sim_btn_stop;
                btn.classList.add('running');
                isSimulating = true;
            }"""
content = re.sub(r'if \(isSimulating\) \{.*?isSimulating = true;\n            \}', sim_toggle, content, flags=re.DOTALL)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("File updated.")
