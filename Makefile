# WSD Debate System - Makefile
# Convenient commands for development and deployment

.PHONY: help setup install run streamlit test examples clean validate logs debug

# Default target
help:
	@echo "WSD Debate System - Available Commands"
	@echo "======================================"
	@echo ""
	@echo "Setup & Installation:"
	@echo "  make setup          - Full setup (venv + install + config)"
	@echo "  make install        - Install dependencies only"
	@echo "  make config         - Create .env from template"
	@echo ""
	@echo "Running:"
	@echo "  make streamlit      - Run Streamlit UI (Recommended)"
	@echo "  make run            - Run main debate (CLI)"
	@echo "  make examples       - Run example scenarios"
	@echo ""
	@echo "Testing & Validation:"
	@echo "  make test           - Run all unit tests"
	@echo "  make validate       - Validate configuration"
	@echo ""
	@echo "Maintenance:"
	@echo "  make logs           - View latest logs"
	@echo "  make debug          - Run with debug mode"
	@echo "  make clean          - Clean up generated files"
	@echo "  make clean-venv     - Remove virtual environment"
	@echo ""

# Full setup
setup: install config
	@echo "✅ Setup complete!"
	@echo "Next steps:"
	@echo "  1. Edit .env and add your GROQ_API_KEY"
	@echo "  2. Run: make run"

# Install dependencies
install:
	@echo "📦 Installing dependencies..."
	python -m venv venv 2>/dev/null || true
	. venv/Scripts/activate 2>/dev/null || . venv/bin/activate && pip install --upgrade pip && pip install -r requirements.txt
	@echo "✅ Dependencies installed"

# Create .env from template
config:
	@if [ ! -f .env ]; then \
		cp .env.example .env; \
		echo "✅ Created .env from template"; \
		echo "⚠️  Remember to add your GROQ_API_KEY"; \
	else \
		echo "✅ .env already exists"; \
	fi

# Run Streamlit UI (Recommended)
streamlit:
	@echo "🎨 Starting Streamlit UI..."
	streamlit run streamlit_app.py

# Run main debate (CLI)
run:
	@echo "🎤 Starting debate..."
	python main.py

# Run examples
examples:
	@echo "📚 Running examples..."
	python examples.py

# Run tests
test:
	@echo "🧪 Running tests..."
	python tests.py

# Validate configuration
validate:
	@echo "✅ Validating configuration..."
	python -c "from config import config; config.validate(); print('Configuration is valid!')" || echo "❌ Configuration validation failed"
	python -c "from models import *; print('✅ All models loaded')"
	python -c "from agents import *; print('✅ All agents loaded')"

# View logs
logs:
	@if [ -f logs/wsd_debate.log ]; then \
		tail -20 logs/wsd_debate.log; \
	else \
		echo "No logs found. Run: make run"; \
	fi

# Run with debug mode
debug:
	@echo "🔍 Running in debug mode..."
	DEBUG_MODE=true python main.py

# Clean up generated files
clean:
	@echo "🗑️  Cleaning up..."
	rm -rf logs/*.log 2>/dev/null || true
	rm -rf *.json 2>/dev/null || true
	rm -rf *.md.bak 2>/dev/null || true
	find . -type d -name "__pycache__" -exec rm -r {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@echo "✅ Cleaned up"

# Remove virtual environment
clean-venv:
	@echo "🗑️  Removing virtual environment..."
	rm -rf venv
	@echo "✅ Virtual environment removed"

# Full clean
clean-all: clean clean-venv
	@echo "✅ Full cleanup complete"

# Development tasks
dev: setup validate test
	@echo "✅ Development environment ready!"

# Quick start
quick: run

# Phony targets
.PHONY: all
all: setup validate test
	@echo "✅ All tasks completed!"
