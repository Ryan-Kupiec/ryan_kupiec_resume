# Fantasy Football Points Predictor with AI Chat

A machine learning system that predicts fantasy football points using NFL player data, enhanced with an interactive AI chat interface powered by Ollama.

## Features

- **ML Model**: Predicts fantasy football points using advanced statistical features
- **FastAPI Backend**: RESTful API for predictions
- **Streamlit Frontend**: Interactive web interface with resume and projects
- **AI Chat Assistant**: Ollama-powered chat that can make predictions and answer questions
- **Real-time Integration**: Chat interface directly calls the prediction API

## System Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Streamlit     │    │   FastAPI       │    │     Ollama      │
│   Frontend      │◄──►│   Prediction    │◄──►│   AI Model      │
│   (Port 8501)   │    │   API (8000)    │    │   (Port 11434)  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## Prerequisites

- Python 3.8+
- Ollama installed and running
- NFL data access (via nfl-data-py)

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd ryan_kupiec_resume
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install Ollama** (if not already installed)
   ```bash
   # macOS
   brew install ollama
   
   # Linux
   curl -fsSL https://ollama.ai/install.sh | sh
   
   # Windows
   # Download from https://ollama.ai/download
   ```

4. **Start Ollama and pull a model**
   ```bash
   ollama serve
   # In another terminal:
   ollama pull llama3.2:3b
   ```

## Quick Start

### Option 1: Use the startup script (Recommended)
```bash
python start_services.py
```

This will:
- Check if Ollama is running
- Start the FastAPI server
- Start the Streamlit app
- Provide status updates

### Option 2: Manual startup

1. **Start the API server**
   ```bash
   uvicorn src.server:app --reload --host 0.0.0.0 --port 8000
   ```

2. **Start the Streamlit app** (in another terminal)
   ```bash
   streamlit run projects_app.py --server.port 8501
   ```

3. **Ensure Ollama is running**
   ```bash
   ollama serve
   ```

## Usage

### Web Interface
1. Open your browser to `http://localhost:8501`
2. Navigate to the "🤖 AI Fantasy Assistant" tab
3. Start chatting with the AI assistant!

### API Endpoints
- **Prediction**: `POST /predict`
  ```json
  {
    "player_id": 12345,
    "season": 2024,
    "week": 1
  }
  ```
- **API Documentation**: `http://localhost:8000/docs`

### Chat Examples

**Prediction Requests:**
- "Predict fantasy points for player 12345 in season 2024 week 1"
- "What are the expected points for player 67890, 2024 season, week 5?"
- "Can you predict fantasy points for player 11111 in 2024 week 10?"

**General Questions:**
- "What factors affect fantasy football performance?"
- "How do I interpret fantasy point predictions?"
- "What's the difference between PPR and standard scoring?"

## Project Structure

```
ryan_kupiec_resume/
├── src/
│   ├── server.py          # FastAPI prediction server
│   ├── train.py           # Model training code
│   ├── model_utils.py     # Model loading utilities
│   └── chat_utils.py      # Chat integration utilities
├── models/
│   └── model_bundle.pkl   # Trained model bundle
├── projects_app.py        # Streamlit main app
├── start_services.py      # Startup script
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## Configuration

### API Configuration
- **Base URL**: `http://localhost:8000` (configurable in `projects_app.py`)
- **Port**: 8000 (FastAPI), 8501 (Streamlit)

### Ollama Configuration
- **Host**: `http://localhost:11434` (default)
- **Model**: `llama3.2:3b` (configurable in `projects_app.py`)

## Troubleshooting

### Ollama Issues
- **"Ollama is not running"**: Run `ollama serve` in a terminal
- **Model not found**: Run `ollama pull llama3.2:3b`
- **Connection refused**: Check if Ollama is running on port 11434

### API Issues
- **"API is not running"**: Start the FastAPI server with `uvicorn src.server:app --reload`
- **Model loading errors**: Ensure `models/model_bundle.pkl` exists
- **Data errors**: Check if NFL data is accessible via `nfl-data-py`

### Streamlit Issues
- **Port conflicts**: Change the port in `start_services.py` or use `--server.port`
- **Import errors**: Ensure all dependencies are installed with `pip install -r requirements.txt`

## Development

### Adding New Features
1. **New API endpoints**: Add to `src/server.py`
2. **Chat improvements**: Modify `src/chat_utils.py`
3. **UI changes**: Update `projects_app.py`

### Model Updates
1. Retrain the model using `src/train.py`
2. Update the model bundle in `models/`
3. Restart the API server

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

[Add your license information here]

## Contact

- **Email**: ryankupiec21@gmail.com
- **Phone**: 773-456-7843
- **Location**: Chicago, IL 60638