# 🎤 WSD Debate System - AI-Powered Debate Preparation & Analysis

A production-grade, multi-agent AI debate system for **World Schools Debate (WSD)** preparation, argument construction, and strategic analysis. Built with cutting-edge LLM technology and multi-agent orchestration.

## ✨ Features

### 🤖 Multi-Agent Framework
- **Research Agent**: Analyzes motions, extracts key definitions, and identifies strategic points
- **Argument Construction Agent**: Generates sophisticated arguments backed by real-world case studies
- **Rebuttal Agent**: Constructs logical rebuttals targeting opponent arguments
- **Analysis Agent**: Provides strategic insights and predicts outcomes

### 📚 Sophisticated Argument Construction
- **Case Study Integration**: Each argument backed by 2-3 real-world case studies
- **Position Correlation**: Arguments mapped to overall team strategy
- **Evidence-Based**: Comprehensive evidence integration (3-5 pieces per argument)
- **Scholarly Reasoning**: Development-grade arguments with deep logical structure

### 🎨 Beautiful UI
- **Streamlit-Powered**: Interactive, responsive web interface
- **Clean Design**: White background with blue and orange accents
- **Real-Time Results**: Live debate preparation with progress tracking
- **Export Capabilities**: Download results as JSON or Markdown

### ⚡ Performance
- **Parallel Execution**: Concurrent agent processing for speed
- **Fast Inference**: Powered by Groq API (Mixtral 8x7B)
- **Optimized Prompts**: Structured prompts for consistent, high-quality outputs
- **Comprehensive Logging**: Full execution tracing and error handling

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Groq API Key ([Get one here](https://console.groq.com))

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/wsd-debate-system.git
cd Debate_System
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment**
```bash
# Create .env file or set environment variables
export GROQ_API_KEY="your_groq_api_key_here"
export GROQ_MODEL="mixtral-8x7b-32768"
export LOG_LEVEL="INFO"
```

5. **Run the application**
```bash
streamlit run streamlit_app.py
```

The app will open at `http://localhost:8501`

## 📋 Usage

### Basic Workflow

1. **Enter Debate Motion**: Input the statement to be debated
2. **Configure Teams**: Add proposition and opposition team members
3. **Set Parameters**: Choose number of arguments and rebuttals
4. **Start Debate**: Click "Start Debate" to initiate processing
5. **Review Results**: Examine arguments, rebuttals, and analysis
6. **Export**: Download results in JSON or Markdown format

### Example Motion
```
"This house believes artificial intelligence should be regulated by governments"
```

### API Usage (Programmatic)

```python
import asyncio
from debate_manager import DebateSession

async def run_debate():
    session = DebateSession()
    
    state = await session.start_debate(
        motion="This house believes AI should be regulated",
        proposition_members=["Alice", "Bob", "Charlie"],
        opposition_members=["David", "Eve", "Frank"],
        num_arguments=3,
        num_rebuttals=3
    )
    
    return state

# Run the debate
result = asyncio.run(run_debate())
print(f"Winner: {result.predicted_winner}")
```

## 📁 Project Structure

```
Debate_System/
├── agents/                    # Multi-agent framework
│   ├── __init__.py
│   ├── base_agent.py         # Abstract base agent
│   ├── research_agent.py     # Research & analysis
│   ├── argument_agent.py     # Argument construction
│   ├── rebuttal_agent.py     # Rebuttal generation
│   └── analysis_agent.py     # Strategic analysis
├── streamlit_app.py          # Web UI (Streamlit)
├── debate_manager.py         # Debate orchestration
├── models.py                 # Pydantic data models
├── config.py                 # Configuration management
├── logger.py                 # Logging setup
├── utils.py                  # Utility functions
├── workflow.py               # LangGraph workflow
├── requirements.txt          # Dependencies
├── tests.py                  # Test suite
└── README.md                 # This file
```

## ⚙️ Configuration

Edit `config.py` to customize:

```python
# LLM Configuration
groq_api_key = "your-api-key"
groq_model = "mixtral-8x7b-32768"
groq_temperature = 0.7
groq_max_tokens = 2048

# System Configuration
log_level = "INFO"
debug_mode = False
parallel_execution = True
timeout_seconds = 300
```

## 🏗️ Architecture

### Data Models (Pydantic)
- **Argument**: Contention, reasoning, evidence, impact, case studies, position correlation
- **CaseStudy**: Title, background, methodology, outcomes, impact
- **SideCase**: Team composition, motion analysis, arguments, rebuttals
- **DebateState**: Complete debate results and analysis

### Agent Workflow

```
Motion Input
    ↓
[Research Agent] → Motion analysis, definitions, strategic points
    ↓
[Argument Agent] → Sophisticated arguments with case studies
    ↓
[Rebuttal Agent] → Logical rebuttals to opponent arguments
    ↓
[Analysis Agent] → Strategic analysis and winner prediction
    ↓
Debate Results (JSON/Markdown)
```

## 🔧 Technologies

### Core Framework
- **LangChain 0.1.14**: LLM orchestration and chains
- **LangGraph 0.0.37**: Multi-agent workflow management
- **Pydantic 2.5.3**: Data validation and serialization

### LLM & APIs
- **Groq API**: Fast inference with Mixtral 8x7B model
- **Python 3.8+**: Backend implementation

### Frontend
- **Streamlit 1.0+**: Interactive web interface
- **Custom CSS**: Enhanced styling and theming

### Utilities
- **Logging**: Comprehensive execution tracking
- **JSON/Markdown Export**: Multiple output formats
- **Async Processing**: Concurrent execution for performance

## 📊 Output Examples

### Arguments Display
Each argument includes:
- **Contention**: Main claim
- **Reasoning**: Logical justification
- **Evidence**: 3-5 supporting pieces
- **Impact**: Debate significance
- **Case Studies**: 2-3 real-world examples with outcomes
- **Position Correlation**: Connection to team strategy

### Rebuttals
- **Target**: Which opposition argument
- **Main Rebuttal**: Counter-argument
- **Logical Flaw**: Identified weakness
- **Impact**: Why this rebuttal matters

### Analysis
- **Critical Clash Points**: Key areas of disagreement
- **Strategic Analysis**: Overall debate dynamics
- **Winner Prediction**: Adjudication forecast

## 🧪 Testing

Run the test suite:
```bash
python tests.py
```

## 📝 Logging

Logs are stored in the `logs/` directory with timestamps. Check logs for:
- Agent execution times
- LLM response details
- Error tracking
- Performance metrics

## 🔐 Security & Best Practices

- ✅ API keys stored in environment variables (never in code)
- ✅ Input validation via Pydantic models
- ✅ Error handling and graceful degradation
- ✅ Comprehensive logging for debugging
- ✅ Reasonable timeout and token limits

## 🚨 Known Limitations

- LLM quality depends on model and prompt design
- Case studies are AI-generated and should be verified
- Not designed for real-time competitive debate
- Requires active Groq API subscription

## 📈 Performance Metrics

- **Average Execution Time**: 2-5 minutes per debate
- **Arguments Generated**: Customizable (1-10 per side)
- **Parallel Processing**: 4 agents running concurrently
- **Token Usage**: ~8,000-12,000 tokens per debate

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 🎯 Roadmap

- [ ] Multi-language support
- [ ] Real-time collaboration features
- [ ] Advanced judge scoring system
- [ ] Debate strategy recommendations
- [ ] Integration with debate tournament databases
- [ ] Mobile app support
- [ ] Advanced metrics and analytics dashboard

---

**Built with ❤️ for debate enthusiasts and competitive debaters worldwide.**

*Last Updated: March 15, 2026*
