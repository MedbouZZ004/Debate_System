"""
Streamlit UI for WSD Debate System.

Beautiful, interactive interface for creating and analyzing debates.
Multi-language support: English, Arabic, French.
"""

import streamlit as st
import asyncio
from datetime import datetime
import json
from debate_manager import DebateSession
from utils import DebateExporter, DebateConfigBuilder
from logger import DebateLogger

# ============================================================
# PAGE CONFIGURATION
# ============================================================
st.set_page_config(
    page_title="WSD Debate System",
    page_icon="🎤",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# TRANSLATIONS
# ============================================================
TRANSLATIONS = {
    "English": {
        "dir": "ltr",
        "app_title": "🎤 WSD Debate System",
        "app_subtitle": "AI-Powered World Schools Debate Preparation & Analysis",
        "app_subtitle2": "Multi-Agent LLM Framework with LangGraph Orchestration",
        "lang_label": "🌐 Language / اللغة / Langue",
        "tab_create": "🚀 Create Debate",
        "tab_results": "📊 Results",
        "tab_settings": "⚙️ Settings",
        "tab_guide": "📚 Guide",
        # Create tab
        "motion_section": "Debate Motion",
        "motion_label": "Enter your debate motion:",
        "motion_placeholder": "e.g. This house believes artificial intelligence should be regulated by governments",
        "motion_help": "The statement that both sides will debate",
        "config_section": "Debate Configuration",
        "args_label": "Arguments per side:",
        "rebuttals_label": "Rebuttals per side:",
        "prop_team": "🟦 Proposition Team",
        "opp_team": "🟥 Opposition Team",
        "members_label": "Enter team members (one per line):",
        "prop_default": "Alice\nBob\nCharlie",
        "opp_default": "David\nEve\nFrank",
        "members_help": "Names of team members",
        "start_btn": "🎤 Start Debate",
        "template_btn": "📋 Use Template",
        "error_no_motion": "❌ Please enter a debate motion",
        "error_no_prop": "❌ Please enter proposition team members",
        "error_no_opp": "❌ Please enter opposition team members",
        "phase1": "🔄 Phase 1: Researching motion...",
        "phase2": "🔄 Phase 2: Constructing arguments...",
        "phase3": "🔄 Phase 3: Generating rebuttals...",
        "phase4": "🔄 Phase 4: Analyzing debate...",
        "spinner": "⏳ Starting debate... This may take 2-5 minutes",
        "success": "✅ Debate prepared! View results in the Results tab.",
        "complete": "✅ Debate completed successfully!",
        # Results tab
        "no_results": "🔍 No debate results yet. Create a debate in the 'Create Debate' tab first.",
        "summary": "📊 Debate Summary",
        "metric_motion": "Motion",
        "metric_time": "Execution Time",
        "metric_args": "Total Arguments",
        "metric_winner": "Winner",
        "results_prop": "📝 Proposition Case",
        "results_opp": "📝 Opposition Case",
        "results_analysis": "⚖️ Analysis",
        "results_export": "💾 Export",
        "motion_analysis_exp": "📖 Motion Analysis",
        "key_defs_exp": "📚 Key Definitions",
        "main_args": "Main Arguments",
        "argument_label": "Argument",
        "reasoning_label": "Reasoning:",
        "evidence_label": "Evidence:",
        "impact_label": "Impact:",
        "case_studies_label": "📚 Case Studies:",
        "background_label": "Background:",
        "methodology_label": "Methodology:",
        "outcomes_label": "Outcomes:",
        "impact_on_arg": "Impact on Argument:",
        "position_corr": "🔗 Position Correlation:",
        "rebuttals_prop": "Rebuttals to Opposition",
        "rebuttals_opp": "Rebuttals to Proposition",
        "rebuttal_target": "Rebuttal",
        "main_rebuttal": "Main Rebuttal:",
        "logical_flaw": "Logical Flaw:",
        "rebuttal_impact": "Impact:",
        "analysis_title": "⚖️ Debate Analysis",
        "winner_label": "🏆 Winner",
        "strategic_exp": "📊 Strategic Analysis",
        "clash_title": "Critical Clash Points",
        "clash_label": "Clash",
        "export_title": "💾 Export Results",
        "dl_json": "📥 Download JSON",
        "dl_md": "📥 Download Markdown",
        "new_debate": "🔄 Create New Debate",
        # Settings tab
        "settings_title": "⚙️ System Settings",
        "api_config": "API Configuration",
        "sys_config": "System Configuration",
        "about": "About",
        "api_key_label": "API Key:",
        "model_label": "Model:",
        "temp_label": "Temperature:",
        "tokens_label": "Max Tokens:",
        "log_label": "Log Level:",
        "debug_label": "Debug Mode:",
        "parallel_label": "Parallel Execution:",
        "timeout_label": "Timeout:",
        # Guide tab
        "guide_title": "📚 User Guide",
        "getting_started": "Getting Started",
        "what_happens": "What Happens",
        "tips": "Tips & Tricks",
        "guide_steps": """
1. **Select Language** - Choose your preferred language first
2. **Enter Motion** - Type the debate motion in full
3. **Add Teams** - Enter team member names
4. **Configure** - Set number of arguments/rebuttals
5. **Start** - Click "Start Debate" button
6. **Review** - Check results in Results tab
7. **Export** - Download JSON or Markdown
""",
        "what_happens_txt": """
**Phase 1: Research** (30-60s)
- Analyzes motion for both sides
- Identifies key definitions
- Gathers strategic points

**Phase 2: Arguments** (30-60s)
- Constructs main arguments
- Adds evidence and reasoning

**Phase 3: Rebuttals** (30-60s)
- Generates counter-arguments
- Identifies logical flaws

**Phase 4: Analysis** (30-60s)
- Evaluates both sides
- Predicts winner
""",
        "tip_motions": "💡 How to write effective motions",
        "tip_motions_txt": """
- Be clear and specific
- Use "This house believes..." format
- Make it debatable (not obviously true/false)
- Keep it concise
""",
        "tip_teams": "👥 Team member tips",
        "tip_teams_txt": """
- Use realistic speaker names
- Include first and last names for clarity
- Typically 3-5 members per side
- Can include titles (e.g., "Alice PM" for Prime Minister)
""",
        "tip_perf": "⏱️ Performance tips",
        "tip_perf_txt": """
- First debate takes 2-5 minutes
- Ensure internet connection is stable
- Reduce token limit for faster results
- Use simpler motions for quicker analysis
""",
        "footer": "🎤 WSD Debate System v1.0.0 | Built with LangChain, LangGraph & Streamlit",
        "footer2": "For documentation, visit the included README.md",
    },

    "Arabic": {
        "dir": "rtl",
        "app_title": "🎤 نظام النقاش WSD",
        "app_subtitle": "إعداد وتحليل النقاش المدعوم بالذكاء الاصطناعي",
        "app_subtitle2": "إطار متعدد الوكلاء مع تنسيق LangGraph",
        "lang_label": "🌐 Language / اللغة / Langue",
        "tab_create": "🚀 إنشاء نقاش",
        "tab_results": "📊 النتائج",
        "tab_settings": "⚙️ الإعدادات",
        "tab_guide": "📚 الدليل",
        # Create tab
        "motion_section": "موضوع النقاش",
        "motion_label": "أدخل موضوع النقاش:",
        "motion_placeholder": "مثال: يرى هذا المجلس أن الذكاء الاصطناعي يجب أن تنظمه الحكومات",
        "motion_help": "الجملة التي سيناقشها كلا الفريقين",
        "config_section": "إعداد النقاش",
        "args_label": "عدد الحجج لكل فريق:",
        "rebuttals_label": "عدد الردود لكل فريق:",
        "prop_team": "🟦 فريق المؤيدين",
        "opp_team": "🟥 فريق المعارضين",
        "members_label": "أدخل أعضاء الفريق (واحد في كل سطر):",
        "prop_default": "أحمد\nمحمد\nسارة",
        "opp_default": "علي\nفاطمة\nعمر",
        "members_help": "أسماء أعضاء الفريق",
        "start_btn": "🎤 ابدأ النقاش",
        "template_btn": "📋 استخدم نموذجاً",
        "error_no_motion": "❌ الرجاء إدخال موضوع النقاش",
        "error_no_prop": "❌ الرجاء إدخال أعضاء فريق المؤيدين",
        "error_no_opp": "❌ الرجاء إدخال أعضاء فريق المعارضين",
        "phase1": "🔄 المرحلة 1: تحليل الموضوع...",
        "phase2": "🔄 المرحلة 2: بناء الحجج...",
        "phase3": "🔄 المرحلة 3: إنشاء الردود...",
        "phase4": "🔄 المرحلة 4: التحليل الاستراتيجي...",
        "spinner": "⏳ جاري تشغيل النقاش... قد يستغرق 2-5 دقائق",
        "success": "✅ تم إعداد النقاش! راجع النتائج في تبويب النتائج.",
        "complete": "✅ اكتمل النقاش بنجاح!",
        # Results tab
        "no_results": "🔍 لا توجد نتائج بعد. أنشئ نقاشاً أولاً من تبويب 'إنشاء نقاش'.",
        "summary": "📊 ملخص النقاش",
        "metric_motion": "الموضوع",
        "metric_time": "وقت التنفيذ",
        "metric_args": "إجمالي الحجج",
        "metric_winner": "الفائز",
        "results_prop": "📝 قضية المؤيدين",
        "results_opp": "📝 قضية المعارضين",
        "results_analysis": "⚖️ التحليل",
        "results_export": "💾 تصدير",
        "motion_analysis_exp": "📖 تحليل الموضوع",
        "key_defs_exp": "📚 التعريفات الرئيسية",
        "main_args": "الحجج الرئيسية",
        "argument_label": "الحجة",
        "reasoning_label": "المنطق:",
        "evidence_label": "الأدلة:",
        "impact_label": "التأثير:",
        "case_studies_label": "📚 دراسات الحالة:",
        "background_label": "الخلفية:",
        "methodology_label": "المنهجية:",
        "outcomes_label": "النتائج:",
        "impact_on_arg": "التأثير على الحجة:",
        "position_corr": "🔗 الارتباط بالموقف:",
        "rebuttals_prop": "ردود على المعارضين",
        "rebuttals_opp": "ردود على المؤيدين",
        "rebuttal_target": "رد",
        "main_rebuttal": "الرد الرئيسي:",
        "logical_flaw": "الخلل المنطقي:",
        "rebuttal_impact": "التأثير:",
        "analysis_title": "⚖️ تحليل النقاش",
        "winner_label": "🏆 الفائز",
        "strategic_exp": "📊 التحليل الاستراتيجي",
        "clash_title": "نقاط الخلاف الرئيسية",
        "clash_label": "خلاف",
        "export_title": "💾 تصدير النتائج",
        "dl_json": "📥 تحميل JSON",
        "dl_md": "📥 تحميل Markdown",
        "new_debate": "🔄 إنشاء نقاش جديد",
        # Settings tab
        "settings_title": "⚙️ إعدادات النظام",
        "api_config": "إعداد API",
        "sys_config": "إعداد النظام",
        "about": "حول النظام",
        "api_key_label": "مفتاح API:",
        "model_label": "النموذج:",
        "temp_label": "درجة الحرارة:",
        "tokens_label": "الحد الأقصى للرموز:",
        "log_label": "مستوى السجل:",
        "debug_label": "وضع التصحيح:",
        "parallel_label": "التنفيذ المتوازي:",
        "timeout_label": "المهلة:",
        # Guide tab
        "guide_title": "📚 دليل المستخدم",
        "getting_started": "البدء",
        "what_happens": "ما الذي يحدث",
        "tips": "نصائح وحيل",
        "guide_steps": """
1. **اختر اللغة** - اختر لغتك المفضلة أولاً
2. **أدخل الموضوع** - اكتب موضوع النقاش كاملاً
3. **أضف الفرق** - أدخل أسماء أعضاء الفريق
4. **اضبط الإعدادات** - حدد عدد الحجج والردود
5. **ابدأ** - انقر على "ابدأ النقاش"
6. **راجع** - تحقق من النتائج في تبويب النتائج
7. **صدّر** - حمّل الملفات بتنسيق JSON أو Markdown
""",
        "what_happens_txt": """
**المرحلة 1: البحث** (30-60 ثانية)
- تحليل الموضوع لكلا الجانبين
- تحديد التعريفات الرئيسية
- جمع النقاط الاستراتيجية

**المرحلة 2: الحجج** (30-60 ثانية)
- بناء الحجج الرئيسية
- إضافة الأدلة والمنطق

**المرحلة 3: الردود** (30-60 ثانية)
- إنشاء حجج مضادة
- تحديد الأخطاء المنطقية

**المرحلة 4: التحليل** (30-60 ثانية)
- تقييم كلا الفريقين
- التنبؤ بالفائز
""",
        "tip_motions": "💡 كيف تكتب مواضيع فعّالة",
        "tip_motions_txt": """
- كن واضحاً ومحدداً
- استخدم صيغة "يرى هذا المجلس..."
- اجعله قابلاً للنقاش
- حافظ على الإيجاز
""",
        "tip_teams": "👥 نصائح لأعضاء الفريق",
        "tip_teams_txt": """
- استخدم أسماء حقيقية
- أضف الاسم الأول والأخير للوضوح
- عادة 3-5 أعضاء لكل فريق
""",
        "tip_perf": "⏱️ نصائح الأداء",
        "tip_perf_txt": """
- أول نقاش يستغرق 2-5 دقائق
- تأكد من استقرار اتصال الإنترنت
- استخدم مواضيع أبسط للحصول على نتائج أسرع
""",
        "footer": "🎤 نظام النقاش WSD v1.0.0 | مبني بـ LangChain وLangGraph وStreamlit",
        "footer2": "للتوثيق، راجع ملفات README.md",
    },

    "French": {
        "dir": "ltr",
        "app_title": "🎤 Système de Débat WSD",
        "app_subtitle": "Préparation et analyse de débats alimentés par l'IA",
        "app_subtitle2": "Cadre multi-agents avec orchestration LangGraph",
        "lang_label": "🌐 Language / اللغة / Langue",
        "tab_create": "🚀 Créer un débat",
        "tab_results": "📊 Résultats",
        "tab_settings": "⚙️ Paramètres",
        "tab_guide": "📚 Guide",
        # Create tab
        "motion_section": "Motion du débat",
        "motion_label": "Entrez la motion du débat :",
        "motion_placeholder": "ex. Cette assemblée croit que l'intelligence artificielle doit être réglementée par les gouvernements",
        "motion_help": "La proposition que les deux équipes vont débattre",
        "config_section": "Configuration du débat",
        "args_label": "Arguments par équipe :",
        "rebuttals_label": "Réfutations par équipe :",
        "prop_team": "🟦 Équipe Proposition",
        "opp_team": "🟥 Équipe Opposition",
        "members_label": "Entrez les membres de l'équipe (un par ligne) :",
        "prop_default": "Alice\nBob\nCharlie",
        "opp_default": "David\nÈve\nFrank",
        "members_help": "Noms des membres de l'équipe",
        "start_btn": "🎤 Démarrer le débat",
        "template_btn": "📋 Utiliser un modèle",
        "error_no_motion": "❌ Veuillez entrer une motion de débat",
        "error_no_prop": "❌ Veuillez entrer les membres de l'équipe Proposition",
        "error_no_opp": "❌ Veuillez entrer les membres de l'équipe Opposition",
        "phase1": "🔄 Phase 1 : Recherche de la motion...",
        "phase2": "🔄 Phase 2 : Construction des arguments...",
        "phase3": "🔄 Phase 3 : Génération des réfutations...",
        "phase4": "🔄 Phase 4 : Analyse du débat...",
        "spinner": "⏳ Démarrage du débat... Cela peut prendre 2 à 5 minutes",
        "success": "✅ Débat préparé ! Consultez les résultats dans l'onglet Résultats.",
        "complete": "✅ Débat terminé avec succès !",
        # Results tab
        "no_results": "🔍 Aucun résultat pour l'instant. Créez un débat dans l'onglet 'Créer un débat'.",
        "summary": "📊 Résumé du débat",
        "metric_motion": "Motion",
        "metric_time": "Temps d'exécution",
        "metric_args": "Total des arguments",
        "metric_winner": "Vainqueur",
        "results_prop": "📝 Cas Proposition",
        "results_opp": "📝 Cas Opposition",
        "results_analysis": "⚖️ Analyse",
        "results_export": "💾 Exporter",
        "motion_analysis_exp": "📖 Analyse de la motion",
        "key_defs_exp": "📚 Définitions clés",
        "main_args": "Arguments principaux",
        "argument_label": "Argument",
        "reasoning_label": "Raisonnement :",
        "evidence_label": "Preuves :",
        "impact_label": "Impact :",
        "case_studies_label": "📚 Études de cas :",
        "background_label": "Contexte :",
        "methodology_label": "Méthodologie :",
        "outcomes_label": "Résultats :",
        "impact_on_arg": "Impact sur l'argument :",
        "position_corr": "🔗 Corrélation de position :",
        "rebuttals_prop": "Réfutations à l'Opposition",
        "rebuttals_opp": "Réfutations à la Proposition",
        "rebuttal_target": "Réfutation",
        "main_rebuttal": "Réfutation principale :",
        "logical_flaw": "Défaut logique :",
        "rebuttal_impact": "Impact :",
        "analysis_title": "⚖️ Analyse du débat",
        "winner_label": "🏆 Vainqueur",
        "strategic_exp": "📊 Analyse stratégique",
        "clash_title": "Points de clash critiques",
        "clash_label": "Clash",
        "export_title": "💾 Exporter les résultats",
        "dl_json": "📥 Télécharger JSON",
        "dl_md": "📥 Télécharger Markdown",
        "new_debate": "🔄 Créer un nouveau débat",
        # Settings tab
        "settings_title": "⚙️ Paramètres du système",
        "api_config": "Configuration API",
        "sys_config": "Configuration système",
        "about": "À propos",
        "api_key_label": "Clé API :",
        "model_label": "Modèle :",
        "temp_label": "Température :",
        "tokens_label": "Tokens max :",
        "log_label": "Niveau de log :",
        "debug_label": "Mode débogage :",
        "parallel_label": "Exécution parallèle :",
        "timeout_label": "Délai d'attente :",
        # Guide tab
        "guide_title": "📚 Guide utilisateur",
        "getting_started": "Démarrage",
        "what_happens": "Ce qui se passe",
        "tips": "Astuces",
        "guide_steps": """
1. **Choisir la langue** - Sélectionnez votre langue préférée d'abord
2. **Entrer la motion** - Tapez la motion du débat en entier
3. **Ajouter les équipes** - Entrez les noms des membres
4. **Configurer** - Définissez le nombre d'arguments/réfutations
5. **Démarrer** - Cliquez sur "Démarrer le débat"
6. **Consulter** - Vérifiez les résultats dans l'onglet Résultats
7. **Exporter** - Téléchargez en JSON ou Markdown
""",
        "what_happens_txt": """
**Phase 1 : Recherche** (30-60s)
- Analyse la motion des deux côtés
- Identifie les définitions clés
- Collecte les points stratégiques

**Phase 2 : Arguments** (30-60s)
- Construit les arguments principaux
- Ajoute preuves et raisonnement

**Phase 3 : Réfutations** (30-60s)
- Génère des contre-arguments
- Identifie les failles logiques

**Phase 4 : Analyse** (30-60s)
- Évalue les deux équipes
- Prédit le vainqueur
""",
        "tip_motions": "💡 Comment rédiger des motions efficaces",
        "tip_motions_txt": """
- Soyez clair et précis
- Utilisez le format "Cette assemblée croit..."
- Rendez-la discutable
- Restez concis
""",
        "tip_teams": "👥 Conseils pour les membres d'équipe",
        "tip_teams_txt": """
- Utilisez des noms réalistes
- Incluez prénom et nom pour la clarté
- Généralement 3 à 5 membres par équipe
""",
        "tip_perf": "⏱️ Conseils de performance",
        "tip_perf_txt": """
- Le premier débat prend 2 à 5 minutes
- Assurez une connexion Internet stable
- Utilisez des motions simples pour des résultats plus rapides
""",
        "footer": "🎤 WSD Debate System v1.0.0 | Construit avec LangChain, LangGraph & Streamlit",
        "footer2": "Pour la documentation, consultez les fichiers README.md",
    },
}

# ============================================================
# CUSTOM CSS
# ============================================================
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    body { background-color: #ffffff; color: #000000; }
    .main { background-color: #ffffff; }
    .stMarkdown { color: #000000; }

    .argument-box {
        background-color: #f0f8ff;
        padding: 20px;
        border-left: 6px solid #1f77b4;
        border-radius: 8px;
        margin: 15px 0;
        color: #000000;
    }
    .argument-box h4 {
        color: #1f77b4;
        margin-top: 0;
        margin-bottom: 12px;
        font-size: 18px;
    }

    .case-study-box {
        background-color: #e8f4f8;
        padding: 15px;
        border-left: 4px solid #1f77b4;
        border-radius: 8px;
        margin: 10px 0;
        color: #000000;
        margin-left: 20px;
        border-top: 2px solid #1f77b4;
    }
    .case-study-box h5 {
        color: #1f77b4;
        margin-top: 0;
        margin-bottom: 8px;
        font-weight: bold;
    }

    .position-correlation-box {
        background-color: #f0f8ff;
        padding: 15px;
        border-left: 5px solid #1f77b4;
        border-radius: 8px;
        margin: 15px 0;
        color: #000000;
        border-top: 2px dashed #1f77b4;
    }
    .position-correlation-box strong { color: #1f77b4; }

    .rebuttal-box {
        background-color: #fff4e6;
        padding: 15px;
        border-left: 4px solid #ff7f0e;
        border-radius: 5px;
        margin: 10px 0;
        color: #000000;
    }

    .analysis-box {
        background-color: #f0f8f0;
        padding: 15px;
        border-left: 4px solid #2ca02c;
        border-radius: 5px;
        margin: 10px 0;
        color: #000000;
    }

    .header-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 30px;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    .header-box h1 { color: white; margin: 0; }
    .header-box p { color: white; margin: 5px 0; }

    .lang-selector-box {
        background: linear-gradient(135deg, #f8f9fa, #e9ecef);
        border: 2px solid #6c757d;
        border-radius: 12px;
        padding: 18px 24px;
        margin-bottom: 24px;
        display: flex;
        align-items: center;
        gap: 16px;
    }

    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }

    a { color: #1f77b4; }

    /* RTL support */
    .rtl-content {
        direction: rtl;
        text-align: right;
    }
    </style>
""", unsafe_allow_html=True)

# ============================================================
# SESSION STATE
# ============================================================
if 'debate_state' not in st.session_state:
    st.session_state.debate_state = None
if 'session' not in st.session_state:
    st.session_state.session = DebateSession()
if 'debate_running' not in st.session_state:
    st.session_state.debate_running = False
if 'language' not in st.session_state:
    st.session_state.language = "English"

# ============================================================
# LANGUAGE SELECTOR  (top of page, before everything else)
# ============================================================
st.markdown("""
    <div style="background:linear-gradient(90deg,#667eea22,#764ba222);
                border:1.5px solid #667eea55; border-radius:12px;
                padding:16px 24px; margin-bottom:18px;">
        <span style="font-size:20px; font-weight:700; color:#764ba2;">
            🌐 Select Language &nbsp;|&nbsp; اختر اللغة &nbsp;|&nbsp; Choisir la langue
        </span>
    </div>
""", unsafe_allow_html=True)

lang_col1, lang_col2, lang_col3 = st.columns(3)
with lang_col1:
    if st.button("🇬🇧  English", use_container_width=True,
                 type="primary" if st.session_state.language == "English" else "secondary"):
        st.session_state.language = "English"
        st.rerun()
with lang_col2:
    if st.button("🇸🇦  العربية", use_container_width=True,
                 type="primary" if st.session_state.language == "Arabic" else "secondary"):
        st.session_state.language = "Arabic"
        st.rerun()
with lang_col3:
    if st.button("🇫🇷  Français", use_container_width=True,
                 type="primary" if st.session_state.language == "French" else "secondary"):
        st.session_state.language = "French"
        st.rerun()

# Load translations
T = TRANSLATIONS[st.session_state.language]
lang = st.session_state.language
is_rtl = T["dir"] == "rtl"

# RTL wrapper if Arabic
rtl_open = '<div class="rtl-content">' if is_rtl else ""
rtl_close = "</div>" if is_rtl else ""

# ============================================================
# HEADER
# ============================================================
st.markdown(f"""
    {rtl_open}
    <div class="header-box">
        <h1>{T['app_title']}</h1>
        <p>{T['app_subtitle']}</p>
        <p style="font-size: 14px; opacity: 0.9;">{T['app_subtitle2']}</p>
    </div>
    {rtl_close}
""", unsafe_allow_html=True)

# ============================================================
# TABS
# ============================================================
tab1, tab2, tab3, tab4 = st.tabs([
    T["tab_create"],
    T["tab_results"],
    T["tab_settings"],
    T["tab_guide"],
])

# ============================================================
# TAB 1: Create Debate
# ============================================================
with tab1:
    if is_rtl:
        st.markdown('<div class="rtl-content">', unsafe_allow_html=True)

    st.header(T["tab_create"])

    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader(T["motion_section"])
        motion = st.text_area(
            T["motion_label"],
            value="",
            placeholder=T["motion_placeholder"],
            height=100,
            help=T["motion_help"]
        )

    with col2:
        st.subheader(T["config_section"])
        num_arguments = st.slider(
            T["args_label"],
            min_value=1,
            max_value=10,
            value=3
        )
        num_rebuttals = st.slider(
            T["rebuttals_label"],
            min_value=1,
            max_value=10,
            value=3
        )

    st.divider()

    # Team input
    col_prop, col_opp = st.columns([1, 1])

    with col_prop:
        st.subheader(T["prop_team"])
        prop_input = st.text_area(
            T["members_label"],
            value=T["prop_default"],
            height=100,
            key="prop_members",
            help=T["members_help"]
        )
        proposition_members = [m.strip() for m in prop_input.split('\n') if m.strip()]

    with col_opp:
        st.subheader(T["opp_team"])
        opp_input = st.text_area(
            T["members_label"],
            value=T["opp_default"],
            height=100,
            key="opp_members",
            help=T["members_help"]
        )
        opposition_members = [m.strip() for m in opp_input.split('\n') if m.strip()]

    st.divider()

    # Start debate button
    col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 2])

    with col_btn1:
        if st.button(T["start_btn"], use_container_width=True, type="primary"):
            if not motion.strip():
                st.error(T["error_no_motion"])
            elif not proposition_members:
                st.error(T["error_no_prop"])
            elif not opposition_members:
                st.error(T["error_no_opp"])
            else:
                st.session_state.debate_running = True

                with st.spinner(T["spinner"]):
                    progress_bar = st.progress(0)
                    status_text = st.empty()

                    try:
                        status_text.text(T["phase1"])
                        progress_bar.progress(15)

                        status_text.text(T["phase2"])
                        progress_bar.progress(45)

                        status_text.text(T["phase3"])
                        progress_bar.progress(75)

                        status_text.text(T["phase4"])
                        progress_bar.progress(90)

                        # Run async debate
                        async def run_debate():
                            session = st.session_state.session
                            state = await session.start_debate(
                                motion=motion,
                                proposition_members=proposition_members,
                                opposition_members=opposition_members,
                                num_arguments=num_arguments,
                                num_rebuttals=num_rebuttals,
                                language=lang
                            )
                            return state

                        state = asyncio.run(run_debate())
                        st.session_state.debate_state = state

                        progress_bar.progress(100)
                        status_text.text(T["complete"])

                        st.success(T["success"])
                        st.session_state.debate_running = False

                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")
                        DebateLogger.error(f"Debate creation error: {str(e)}", exc_info=True)
                        st.session_state.debate_running = False

    with col_btn2:
        if st.button(T["template_btn"], use_container_width=True):
            st.info("Template loaded! Modify and click 'Start Debate'")

    with col_btn3:
        pass

    if is_rtl:
        st.markdown('</div>', unsafe_allow_html=True)


# ============================================================
# TAB 2: Results
# ============================================================
with tab2:
    if is_rtl:
        st.markdown('<div class="rtl-content">', unsafe_allow_html=True)

    if st.session_state.debate_state is None:
        st.info(T["no_results"])
    else:
        state = st.session_state.debate_state

        # Summary metrics
        st.subheader(T["summary"])
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                T["metric_motion"],
                state.motion[:30] + "..." if len(state.motion) > 30 else state.motion,
                help=state.motion
            )
        with col2:
            st.metric(
                T["metric_time"],
                f"{state.execution_time_seconds:.1f}s" if state.execution_time_seconds else "N/A"
            )
        with col3:
            st.metric(
                T["metric_args"],
                len(state.proposition.arguments) + len(state.opposition.arguments)
            )
        with col4:
            st.metric(
                T["metric_winner"],
                state.predicted_winner or "TBD"
            )

        st.divider()

        # Results tabs
        results_tab1, results_tab2, results_tab3, results_tab4 = st.tabs([
            T["results_prop"],
            T["results_opp"],
            T["results_analysis"],
            T["results_export"],
        ])

        # ---- Helper to render a side's arguments ----
        def render_side(side_case, rebuttals_label):
            if side_case.motion_analysis:
                with st.expander(T["motion_analysis_exp"], expanded=False):
                    st.write(side_case.motion_analysis)

            if side_case.key_definitions:
                with st.expander(T["key_defs_exp"], expanded=False):
                    for term, definition in side_case.key_definitions.items():
                        st.write(f"**{term}:** {definition}")

            st.subheader(T["main_args"])
            for i, arg in enumerate(side_case.arguments, 1):
                st.markdown(f"""
                    <div class="argument-box">
                    <h4>{T['argument_label']} {i}: {arg.contention}</h4>
                    <p><strong>{T['reasoning_label']}</strong> {arg.reasoning}</p>
                    """, unsafe_allow_html=True)

                if arg.evidence:
                    st.write(f"**{T['evidence_label']}**")
                    for evidence in arg.evidence:
                        st.write(f"• {evidence}")

                if arg.impact:
                    st.write(f"**{T['impact_label']}** {arg.impact}")

                if arg.case_studies:
                    st.write(f"**{T['case_studies_label']}**")
                    for cs in arg.case_studies:
                        st.markdown(f"""
                            <div class="case-study-box">
                            <h5>{cs.title}</h5>
                            <p><strong>{T['background_label']}</strong> {cs.background}</p>
                            """, unsafe_allow_html=True)
                        if cs.methodology:
                            st.write(f"**{T['methodology_label']}** {cs.methodology}")
                        st.write(f"**{T['outcomes_label']}** {cs.outcomes}")
                        st.write(f"**{T['impact_on_arg']}** {cs.impact}")
                        st.markdown("</div>", unsafe_allow_html=True)

                if arg.position_correlation:
                    st.markdown(f"""
                        <div class="position-correlation-box">
                        <strong>{T['position_corr']}</strong><br>
                        {arg.position_correlation}
                        </div>
                        """, unsafe_allow_html=True)

                st.markdown("</div>", unsafe_allow_html=True)

            if side_case.rebuttals:
                st.subheader(rebuttals_label)
                for key, rebuttal in side_case.rebuttals.items():
                    if isinstance(rebuttal, dict):
                        st.markdown(f"""
                            <div class="rebuttal-box">
                            <h5>{rebuttal.get('targets_argument', T['rebuttal_target'])}</h5>
                            <p><strong>{T['main_rebuttal']}</strong> {rebuttal.get('main_rebuttal', 'N/A')}</p>
                            <p><strong>{T['logical_flaw']}</strong> {rebuttal.get('logical_flaw', 'N/A')}</p>
                            <p><strong>{T['rebuttal_impact']}</strong> {rebuttal.get('impact', 'N/A')}</p>
                            </div>
                            """, unsafe_allow_html=True)

        with results_tab1:
            st.subheader(f"🟦 {', '.join(state.proposition.team_members)}")
            render_side(state.proposition, T["rebuttals_prop"])

        with results_tab2:
            st.subheader(f"🟥 {', '.join(state.opposition.team_members)}")
            render_side(state.opposition, T["rebuttals_opp"])

        with results_tab3:
            st.subheader(T["analysis_title"])

            if state.predicted_winner:
                c1, c2 = st.columns([1, 3])
                with c1:
                    st.markdown(f"### {T['winner_label']}")
                with c2:
                    st.markdown(f"### {state.predicted_winner}")

            if state.strategic_analysis:
                with st.expander(T["strategic_exp"], expanded=True):
                    st.write(state.strategic_analysis)

            if state.critical_clashes:
                st.subheader(T["clash_title"])
                for i, clash in enumerate(state.critical_clashes, 1):
                    st.markdown(f"""
                        <div class="analysis-box">
                        <strong>{T['clash_label']} {i}:</strong> {clash}
                        </div>
                        """, unsafe_allow_html=True)

        with results_tab4:
            st.subheader(T["export_title"])
            col1, col2, col3 = st.columns(3)

            with col1:
                json_data = DebateExporter.to_json(state)
                st.download_button(
                    label=T["dl_json"],
                    data=json_data,
                    file_name=f"debate_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json",
                    use_container_width=True
                )
            with col2:
                md_data = DebateExporter.to_markdown(state)
                st.download_button(
                    label=T["dl_md"],
                    data=md_data,
                    file_name=f"debate_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                    mime="text/markdown",
                    use_container_width=True
                )
            with col3:
                if st.button(T["new_debate"], use_container_width=True):
                    st.session_state.debate_state = None
                    st.rerun()

    if is_rtl:
        st.markdown('</div>', unsafe_allow_html=True)


# ============================================================
# TAB 3: Settings
# ============================================================
with tab3:
    if is_rtl:
        st.markdown('<div class="rtl-content">', unsafe_allow_html=True)

    st.subheader(T["settings_title"])

    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader(T["api_config"])
        from config import config as app_config

        api_key_masked = "●" * 8 + app_config.groq_api_key[-4:] if app_config.groq_api_key else "Not set"
        st.write(f"**{T['api_key_label']}** {api_key_masked}")
        st.write(f"**{T['model_label']}** {app_config.groq_model}")
        st.write(f"**{T['temp_label']}** {app_config.groq_temperature}")
        st.write(f"**{T['tokens_label']}** {app_config.groq_max_tokens}")

    with col2:
        st.subheader(T["sys_config"])
        st.write(f"**{T['log_label']}** {app_config.log_level}")
        st.write(f"**{T['debug_label']}** {app_config.debug_mode}")
        st.write(f"**{T['parallel_label']}** {app_config.parallel_execution}")
        st.write(f"**{T['timeout_label']}** {app_config.timeout_seconds}s")

    st.divider()
    st.subheader(T["about"])
    st.info("""
    **WSD Debate System v1.0.0**

    A production-grade, multi-agent AI debate system built with:
    - LangChain & LangGraph for orchestration
    - Groq API (Mixtral 8x7B) for fast inference
    - Pydantic for data validation
    - Streamlit for this beautiful UI

    **Features:**
    - Multi-language support: English, Arabic, French
    - Multi-agent framework with 4 specialized agents
    - Automatic debate preparation workflow
    - Parallel execution for speed
    - Export to JSON and Markdown
    """)

    if is_rtl:
        st.markdown('</div>', unsafe_allow_html=True)


# ============================================================
# TAB 4: Guide
# ============================================================
with tab4:
    if is_rtl:
        st.markdown('<div class="rtl-content">', unsafe_allow_html=True)

    st.subheader(T["guide_title"])

    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader(T["getting_started"])
        st.markdown(T["guide_steps"])

    with col2:
        st.subheader(T["what_happens"])
        st.markdown(T["what_happens_txt"])

    st.divider()

    st.subheader(T["tips"])
    with st.expander(T["tip_motions"]):
        st.markdown(T["tip_motions_txt"])
    with st.expander(T["tip_teams"]):
        st.markdown(T["tip_teams_txt"])
    with st.expander(T["tip_perf"]):
        st.markdown(T["tip_perf_txt"])

    if is_rtl:
        st.markdown('</div>', unsafe_allow_html=True)


# ============================================================
# FOOTER
# ============================================================
st.divider()
st.markdown(f"""
    <div style="text-align: center; color: #888; padding: 20px;">
    <p>{T['footer']}</p>
    <p>{T['footer2']}</p>
    </div>
""", unsafe_allow_html=True)
