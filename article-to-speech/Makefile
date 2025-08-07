.PHONY: setup run clean

# Default target
all: setup

# Setup: Create virtual environment and install dependencies
setup:
	@echo "🚀 Setting up Article to Speech Converter..."
	@echo "Creating virtual environment..."
	python -m venv .venv
	@echo "Activating virtual environment and installing dependencies..."
	.venv/bin/pip install -r requirements.txt
	@echo "✅ Setup complete! Run 'make run' to start the application."

# Run: Start the Streamlit application
run:
	@echo "🎤 Starting Article to Speech Converter..."
	@echo "Opening browser at http://localhost:8501"
	.venv/bin/streamlit run app.py

# Clean: Remove virtual environment
clean:
	@echo "🧹 Cleaning up..."
	rm -rf .venv
	@echo "✅ Cleanup complete!"

# Help: Show available commands
help:
	@echo "Available commands:"
	@echo "  make setup  - Create virtual environment and install dependencies"
	@echo "  make run    - Start the Streamlit application"
	@echo "  make clean  - Remove virtual environment"
	@echo "  make help   - Show this help message" 