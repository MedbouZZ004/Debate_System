"""
Streamlit UI for WSD Debate System.

Beautiful, interactive interface for creating and analyzing debates.
"""

import streamlit as st
import asyncio
from datetime import datetime
import json
from debate_manager import DebateSession
from utils import DebateExporter, DebateConfigBuilder
from logger import DebateLogger

# Page configuration
st.set_page_config(
    page_title="WSD Debate System",
    page_icon="🎤",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    body {
        background-color: #ffffff;
        color: #000000;
    }
    
    .main {
        background-color: #ffffff;
    }
    
    .stMarkdown {
        color: #000000;
    }
    
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
    
    .position-correlation-box strong {
        color: #1f77b4;
    }
    
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
    
    .header-box h1 {
        color: white;
        margin: 0;
    }
    
    .header-box p {
        color: white;
        margin: 5px 0;
    }
    
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    
    a {
        color: #1f77b4;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'debate_state' not in st.session_state:
    st.session_state.debate_state = None
if 'session' not in st.session_state:
    st.session_state.session = DebateSession()
if 'debate_running' not in st.session_state:
    st.session_state.debate_running = False

# Header
st.markdown("""
    <div class="header-box">
        <h1>🎤 WSD Debate System</h1>
        <p>AI-Powered World Schools Debate Preparation & Analysis</p>
        <p style="font-size: 14px; opacity: 0.9;">Multi-Agent LLM Framework with LangGraph Orchestration</p>
    </div>
""", unsafe_allow_html=True)

# Main layout with tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "🚀 Create Debate",
    "📊 Results",
    "⚙️ Settings",
    "📚 Guide"
])

# ============================================================
# TAB 1: Create Debate
# ============================================================
with tab1:
    st.header("Create New Debate")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Debate Motion")
        motion = st.text_area(
            "Enter the debate motion:",
            value="This house believes artificial intelligence should be regulated by governments",
            height=80,
            help="The statement that both sides will debate"
        )
    
    with col2:
        st.subheader("Debate Configuration")
        num_arguments = st.slider(
            "Arguments per side:",
            min_value=1,
            max_value=10,
            value=3
        )
        num_rebuttals = st.slider(
            "Rebuttals per side:",
            min_value=1,
            max_value=10,
            value=3
        )
    
    st.divider()
    
    # Team input
    col_prop, col_opp = st.columns([1, 1])
    
    with col_prop:
        st.subheader("🟦 Proposition Team")
        prop_input = st.text_area(
            "Enter team members (one per line):",
            value="Alice\nBob\nCharlie",
            height=100,
            key="prop_members",
            help="Names of proposition team members"
        )
        proposition_members = [m.strip() for m in prop_input.split('\n') if m.strip()]
    
    with col_opp:
        st.subheader("🟥 Opposition Team")
        opp_input = st.text_area(
            "Enter team members (one per line):",
            value="David\nEve\nFrank",
            height=100,
            key="opp_members",
            help="Names of opposition team members"
        )
        opposition_members = [m.strip() for m in opp_input.split('\n') if m.strip()]
    
    st.divider()
    
    # Start debate button
    col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 2])
    
    with col_btn1:
        if st.button("🎤 Start Debate", use_container_width=True, type="primary"):
            if not motion.strip():
                st.error("❌ Please enter a debate motion")
            elif not proposition_members:
                st.error("❌ Please enter proposition team members")
            elif not opposition_members:
                st.error("❌ Please enter opposition team members")
            else:
                st.session_state.debate_running = True
                
                # Show progress
                with st.spinner("⏳ Starting debate... This may take 2-5 minutes"):
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    try:
                        status_text.text("🔄 Phase 1: Researching motion...")
                        progress_bar.progress(15)
                        
                        status_text.text("🔄 Phase 2: Constructing arguments...")
                        progress_bar.progress(45)
                        
                        status_text.text("🔄 Phase 3: Generating rebuttals...")
                        progress_bar.progress(75)
                        
                        status_text.text("🔄 Phase 4: Analyzing debate...")
                        progress_bar.progress(90)
                        
                        # Run async debate
                        async def run_debate():
                            session = st.session_state.session
                            state = await session.start_debate(
                                motion=motion,
                                proposition_members=proposition_members,
                                opposition_members=opposition_members,
                                num_arguments=num_arguments,
                                num_rebuttals=num_rebuttals
                            )
                            return state
                        
                        state = asyncio.run(run_debate())
                        st.session_state.debate_state = state
                        
                        progress_bar.progress(100)
                        status_text.text("✅ Debate completed successfully!")
                        
                        st.success("✅ Debate prepared! View results in the Results tab.")
                        st.session_state.debate_running = False
                        
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")
                        DebateLogger.error(f"Debate creation error: {str(e)}", exc_info=True)
                        st.session_state.debate_running = False
    
    with col_btn2:
        if st.button("📋 Use Template", use_container_width=True):
            st.info("Template loaded! Modify and click 'Start Debate'")
    
    with col_btn3:
        pass


# ============================================================
# TAB 2: Results
# ============================================================
with tab2:
    if st.session_state.debate_state is None:
        st.info("🔍 No debate results yet. Create a debate in the 'Create Debate' tab first.")
    else:
        state = st.session_state.debate_state
        
        # Summary metrics
        st.subheader("📊 Debate Summary")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "Motion",
                state.motion[:30] + "..." if len(state.motion) > 30 else state.motion,
                help=state.motion
            )
        
        with col2:
            st.metric(
                "Execution Time",
                f"{state.execution_time_seconds:.1f}s" if state.execution_time_seconds else "N/A"
            )
        
        with col3:
            st.metric(
                "Total Arguments",
                len(state.proposition.arguments) + len(state.opposition.arguments)
            )
        
        with col4:
            st.metric(
                "Winner",
                state.predicted_winner or "TBD"
            )
        
        st.divider()
        
        # Results tabs
        results_tab1, results_tab2, results_tab3, results_tab4 = st.tabs([
            "📝 Proposition Case",
            "📝 Opposition Case",
            "⚖️ Analysis",
            "💾 Export"
        ])
        
        with results_tab1:
            st.subheader(f"🟦 Proposition: {', '.join(state.proposition.team_members)}")
            
            if state.proposition.motion_analysis:
                with st.expander("📖 Motion Analysis", expanded=False):
                    st.write(state.proposition.motion_analysis)
            
            if state.proposition.key_definitions:
                with st.expander("📚 Key Definitions", expanded=False):
                    for term, definition in state.proposition.key_definitions.items():
                        st.write(f"**{term}:** {definition}")
            
            st.subheader("Main Arguments")
            for i, arg in enumerate(state.proposition.arguments, 1):
                st.markdown(f"""
                    <div class="argument-box">
                    <h4>Argument {i}: {arg.contention}</h4>
                    <p><strong>Reasoning:</strong> {arg.reasoning}</p>
                    """, unsafe_allow_html=True)
                
                if arg.evidence:
                    st.write("**Evidence:**")
                    for evidence in arg.evidence:
                        st.write(f"• {evidence}")
                
                if arg.impact:
                    st.write(f"**Impact:** {arg.impact}")
                
                # Display case studies if available
                if arg.case_studies:
                    st.write("**📚 Case Studies:**")
                    for cs in arg.case_studies:
                        st.markdown(f"""
                            <div class="case-study-box">
                            <h5>{cs.title}</h5>
                            <p><strong>Background:</strong> {cs.background}</p>
                            """, unsafe_allow_html=True)
                        
                        if cs.methodology:
                            st.write(f"**Methodology:** {cs.methodology}")
                        st.write(f"**Outcomes:** {cs.outcomes}")
                        st.write(f"**Impact on Argument:** {cs.impact}")
                        st.markdown("</div>", unsafe_allow_html=True)
                
                # Display position correlation
                if arg.position_correlation:
                    st.markdown(f"""
                        <div class="position-correlation-box">
                        <strong>🔗 Position Correlation:</strong><br>
                        {arg.position_correlation}
                        </div>
                        """, unsafe_allow_html=True)
                
                st.markdown("</div>", unsafe_allow_html=True)
            
            if state.proposition.rebuttals:
                st.subheader("Rebuttals to Opposition")
                for key, rebuttal in state.proposition.rebuttals.items():
                    if isinstance(rebuttal, dict):
                        st.markdown(f"""
                            <div class="rebuttal-box">
                            <h5>{rebuttal.get('targets_argument', 'Rebuttal')}</h5>
                            <p><strong>Main Rebuttal:</strong> {rebuttal.get('main_rebuttal', 'N/A')}</p>
                            <p><strong>Logical Flaw:</strong> {rebuttal.get('logical_flaw', 'N/A')}</p>
                            <p><strong>Impact:</strong> {rebuttal.get('impact', 'N/A')}</p>
                            </div>
                            """, unsafe_allow_html=True)
        
        with results_tab2:
            st.subheader(f"🟥 Opposition: {', '.join(state.opposition.team_members)}")
            
            if state.opposition.motion_analysis:
                with st.expander("📖 Motion Analysis", expanded=False):
                    st.write(state.opposition.motion_analysis)
            
            if state.opposition.key_definitions:
                with st.expander("📚 Key Definitions", expanded=False):
                    for term, definition in state.opposition.key_definitions.items():
                        st.write(f"**{term}:** {definition}")
            
            st.subheader("Main Arguments")
            for i, arg in enumerate(state.opposition.arguments, 1):
                st.markdown(f"""
                    <div class="argument-box">
                    <h4>Argument {i}: {arg.contention}</h4>
                    <p><strong>Reasoning:</strong> {arg.reasoning}</p>
                    """, unsafe_allow_html=True)
                
                if arg.evidence:
                    st.write("**Evidence:**")
                    for evidence in arg.evidence:
                        st.write(f"• {evidence}")
                
                if arg.impact:
                    st.write(f"**Impact:** {arg.impact}")
                
                # Display case studies if available
                if arg.case_studies:
                    st.write("**📚 Case Studies:**")
                    for cs in arg.case_studies:
                        st.markdown(f"""
                            <div class="case-study-box">
                            <h5>{cs.title}</h5>
                            <p><strong>Background:</strong> {cs.background}</p>
                            """, unsafe_allow_html=True)
                        
                        if cs.methodology:
                            st.write(f"**Methodology:** {cs.methodology}")
                        st.write(f"**Outcomes:** {cs.outcomes}")
                        st.write(f"**Impact on Argument:** {cs.impact}")
                        st.markdown("</div>", unsafe_allow_html=True)
                
                # Display position correlation
                if arg.position_correlation:
                    st.markdown(f"""
                        <div class="position-correlation-box">
                        <strong>🔗 Position Correlation:</strong><br>
                        {arg.position_correlation}
                        </div>
                        """, unsafe_allow_html=True)
                
                st.markdown("</div>", unsafe_allow_html=True)
            
            if state.opposition.rebuttals:
                st.subheader("Rebuttals to Proposition")
                for key, rebuttal in state.opposition.rebuttals.items():
                    if isinstance(rebuttal, dict):
                        st.markdown(f"""
                            <div class="rebuttal-box">
                            <h5>{rebuttal.get('targets_argument', 'Rebuttal')}</h5>
                            <p><strong>Main Rebuttal:</strong> {rebuttal.get('main_rebuttal', 'N/A')}</p>
                            <p><strong>Logical Flaw:</strong> {rebuttal.get('logical_flaw', 'N/A')}</p>
                            <p><strong>Impact:</strong> {rebuttal.get('impact', 'N/A')}</p>
                            </div>
                            """, unsafe_allow_html=True)
        
        with results_tab3:
            st.subheader("⚖️ Debate Analysis")
            
            # Predicted winner
            if state.predicted_winner:
                winner_col = st.columns(1)[0]
                with winner_col:
                    col1, col2 = st.columns([1, 3])
                    with col1:
                        st.markdown(f"### 🏆 Winner")
                    with col2:
                        st.markdown(f"### {state.predicted_winner}")
            
            if state.strategic_analysis:
                with st.expander("📊 Strategic Analysis", expanded=True):
                    st.write(state.strategic_analysis)
            
            if state.critical_clashes:
                st.subheader("Critical Clash Points")
                for i, clash in enumerate(state.critical_clashes, 1):
                    st.markdown(f"""
                        <div class="analysis-box">
                        <strong>Clash {i}:</strong> {clash}
                        </div>
                        """, unsafe_allow_html=True)
        
        with results_tab4:
            st.subheader("💾 Export Results")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                # Export JSON
                json_data = DebateExporter.to_json(state)
                st.download_button(
                    label="📥 Download JSON",
                    data=json_data,
                    file_name=f"debate_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json",
                    use_container_width=True
                )
            
            with col2:
                # Export Markdown
                md_data = DebateExporter.to_markdown(state)
                st.download_button(
                    label="📥 Download Markdown",
                    data=md_data,
                    file_name=f"debate_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                    mime="text/markdown",
                    use_container_width=True
                )
            
            with col3:
                if st.button("🔄 Create New Debate", use_container_width=True):
                    st.session_state.debate_state = None
                    st.rerun()


# ============================================================
# TAB 3: Settings
# ============================================================
with tab3:
    st.subheader("⚙️ System Settings")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("API Configuration")
        from config import config
        
        api_key_masked = "●" * 8 + config.groq_api_key[-4:] if config.groq_api_key else "Not set"
        st.write(f"**API Key:** {api_key_masked}")
        st.write(f"**Model:** {config.groq_model}")
        st.write(f"**Temperature:** {config.groq_temperature}")
        st.write(f"**Max Tokens:** {config.groq_max_tokens}")
    
    with col2:
        st.subheader("System Configuration")
        st.write(f"**Log Level:** {config.log_level}")
        st.write(f"**Debug Mode:** {config.debug_mode}")
        st.write(f"**Parallel Execution:** {config.parallel_execution}")
        st.write(f"**Timeout:** {config.timeout_seconds}s")
    
    st.divider()
    
    st.subheader("About")
    st.info("""
    **WSD Debate System v1.0.0**
    
    A production-grade, multi-agent AI debate system built with:
    - LangChain & LangGraph for orchestration
    - Groq API (Mixtral 8x7B) for fast inference
    - Pydantic for data validation
    - Streamlit for this beautiful UI
    
    **Features:**
    - Multi-agent framework with 4 specialized agents
    - Automatic debate preparation workflow
    - Parallel execution for speed
    - Export to JSON and Markdown
    - Comprehensive logging
    
    **Technology Stack:**
    - Python 3.8+
    - LangChain 0.1.14
    - LangGraph 0.0.37
    - Pydantic 2.5.3
    - Streamlit 1.0+
    """)


# ============================================================
# TAB 4: Guide
# ============================================================
with tab4:
    st.subheader("📚 User Guide")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Getting Started")
        st.markdown("""
        1. **Enter Motion** - Type the debate motion
        2. **Add Teams** - Enter team member names
        3. **Configure** - Set number of arguments/rebuttals
        4. **Start** - Click "Start Debate" button
        5. **Review** - Check results in Results tab
        6. **Export** - Download JSON or Markdown
        """)
    
    with col2:
        st.subheader("What Happens")
        st.markdown("""
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
        """)
    
    st.divider()
    
    st.subheader("Tips & Tricks")
    with st.expander("💡 How to write effective motions"):
        st.markdown("""
        - Be clear and specific
        - Use "This house believes..." format
        - Make it debatable (not obviously true/false)
        - Keep it concise
        """)
    
    with st.expander("👥 Team member tips"):
        st.markdown("""
        - Use realistic speaker names
        - Include first and last names for clarity
        - Typically 3-5 members per side
        - Can include titles (e.g., "Alice PM" for Prime Minister)
        """)
    
    with st.expander("⏱️ Performance tips"):
        st.markdown("""
        - First debate takes 2-5 minutes
        - Ensure internet connection is stable
        - Reduce token limit for faster results
        - Use simpler motions for quicker analysis
        """)

# Footer
st.divider()
st.markdown("""
    <div style="text-align: center; color: #888; padding: 20px;">
    <p>🎤 WSD Debate System v1.0.0 | Built with LangChain, LangGraph & Streamlit</p>
    <p>For documentation, visit the included README.md and ARCHITECTURE.md files</p>
    </div>
""", unsafe_allow_html=True)
