# Hybrid AI-MPC Simulink Reconstruction
**شجرة وهيكلية المشروع الشاملة**

تمثل هذه الوثيقة الهيكلة المعمارية الكاملة للمشروع الذي قمنا بتحليله وبنائه معاً. المشروع ينقسم إلى مسارين رئيسيين: 
1. **الجانب الأكاديمي/الفيزيائي:** محاكاة عمل محطة طاقة شمسية هجينة مع خزان مياه.
2. **الجانب البرمجي (Python/Web):** الأكواد التي قمنا بكتابتها لتحويل هذه المخططات إلى رسومات SVG تفاعلية (Interactive Web App).

---

## 1. شجرة الأكواد والملفات (Code Directory Tree)
هذه الشجرة توضح وظيفة كل ملف قمنا بكتابته في مجلد المشروع `مخطط سيموليشن`:

```mermaid
graph LR
    Root[مجلد المشروع: مخطط سيموليشن] --> A[draw_light.py]
    Root --> B[gen_light_root.py]
    Root --> C[gen_light_subs.py]
    Root --> D[build_interactive.py]
    Root --> E[المخرجات Outputs]

    A --> A1(مكتبة الرسم الأساسية Engine)
    A1 -->|دوال| A2(draw_block, draw_ortho_arrow, etc)
    A1 -->|ميزات| A3(تخصيص الألوان, GID Injection للأسهم)

    B --> B1(المخطط الرئيسي Root Level)
    B1 --> B2(Plant Tier: 물리/PV, VFD, Pump)
    B1 --> B3(Control Tier: AI, MPC, Feedback)

    C --> C1(المخططات الفرعية Subsystems)
    C1 --> C2(AI Block: Muxes, Demux, NN)
    C1 --> C3(Water Tank: Mass Balance, Integrator)

    D --> D1(نظام التفاعل Interactive Builder)
    D1 --> D2(قراءة ملفات SVG وحقنها)
    D1 --> D3(إنشاء أزرار التشغيل والأنيميشن)

    E --> E1(01_Root_Level_Final .png/.svg)
    E --> E2(02_AI_BLOCK_Final .png/.svg)
    E --> E3(03_Water_Tank_Final .png/.svg)
    E --> E4((04_Interactive_Explanation.html))
```

---

## 2. الهيكلة الهندسية للمحاكاة (System Architecture Flow)
هذا المخطط يشرح التدفق الميكانيكي والكهربائي للمحاكاة (كيف تعمل المنظومة داخلياً):

```mermaid
flowchart TD
    %% Inputs
    Env_GHI[☀️ الإشعاع الشمسي GHI] --> MUX1
    Env_Temp[🌡️ درجة الحرارة Temp] --> MUX2
    Day_Sel[📅 محدد اليوم Day Selector] --> AI_Predictor

    %% AI & Control Layer
    subgraph Control_Layer [الطبقة السفلية: التحكم المتقدم والذكاء الاصطناعي]
        AI_Predictor((🧠 الذكاء الاصطناعي\nPI-HybridNet))
        MPC_Manager[👔 المدير المرجعي\nMPC Manager]
        MPC_Ctrl[🎮 متحكم الـ\nMPC Controller]
        
        AI_Predictor -- GHI المتوقع --> MPC_Manager
        MPC_Manager -- المسار المرجعي Q_ref --> MPC_Ctrl
    end

    %% Physical Plant Layer
    subgraph Plant_Layer [الطبقة العلوية: المنظومة الفيزيائية]
        MUX1 & MUX2 --> PV[⚡ لوح الطاقة الشمسية\nPV Physics]
        PV -- طاقة خام P_pv --> FOPID[🎛️ متحكم كسري\nFOPID]
        MPC_Ctrl -- إشارة تحكم u_cmd --> FOPID
        
        FOPID -- طاقة منظمة P_ctrl --> VFD[🔄 العاكس\nVariable Frequency Drive]
        MPC_Manager -- تغذية أمامية FF --> VFD
        
        VFD -- تردد وجهد --> Pump[💧 المضخة\nMotor & Pump]
        Pump -- تدفق خام Q_raw --> Gain[رياضيات التحويل]
        Gain -- تدفق صافي Q_in --> Tank[(🛢️ خزان المياه\nMass Balance)]
    end

    %% Feedback
    Tank -- المنسوب الفعلي H --> MPC_Manager
    Gain -- تدفق مرتد --> Delay[تأخير زمني z^-1] --> MPC_Ctrl
```

---

## 3. آلية عمل الواجهة التفاعلية (Interactive Logic)
كيف تعمل صفحة الـ HTML التي تراها في المتصفح؟

1. **الترابط (Binding):** عند رسم المخطط في بايثون، نعطي كل سلك وكل بلوك اسماً برمجياً (مثلاً `gid='block_pv'` أو `gid='path_in_1'`).
2. **التحويل (Translation):** تقوم بايثون بتحويل الرسمة إلى كود رسومي SVG. الـ SVG يحتفظ بالأسماء البرمجية.
3. **الحقن (Injection):** يقوم `build_interactive.py` بأخذ الـ SVG ولصقه مباشرة داخل ملف الـ HTML.
4. **التفاعل (Interactivity):**
   - **النقر:** الجافاسكريبت تبحث عن العناصر المطابقة في القاموس، وعند النقر تستبدل النص الجانبي بالشرح الأكاديمي.
   - **الأنيميشن:** عند الضغط على زر التشغيل، يضيف الجافاسكريبت كلاس CSS اسمه `flowing-path` للأسلاك بترتيب زمني (Timeouts)، مما يجعل السلك يضيء كأنه تيار حقيقي يتدفق.

---
> [!TIP]
> **تم حل مشكلة التداخل:**
> لقد لاحظت وجود بلوكات ثابتة (GHI و Temp) موضوعة تماماً فوق MUX 1 و MUX 2 في المخطط الرئيسي (Root). تم حذف البلوكات الزائدة المتداخلة وتنظيف بداية المخطط بنجاح ليكون انسيابياً تماماً!
