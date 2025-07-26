import re
import requests
import json
from typing import Optional, Dict, Any

def extract_prediction_request(user_message: str) -> Optional[Dict[str, Any]]:
    """
    Extract prediction parameters from user message.
    Returns None if no valid prediction request is found.
    """
    # Common patterns for prediction requests
    patterns = [
        r"predict.*?player\s+(?:id\s+)?(\d+).*?(?:season\s+)?(\d{4}).*?(?:week\s+)?(\d{1,2})",
        r"player\s+(?:id\s+)?(\d+).*?(?:season\s+)?(\d{4}).*?(?:week\s+)?(\d{1,2}).*?predict",
        r"fantasy\s+points.*?player\s+(?:id\s+)?(\d+).*?(?:season\s+)?(\d{4}).*?(?:week\s+)?(\d{1,2})",
        r"(\d+).*?(\d{4}).*?(\d{1,2}).*?predict",
    ]
    
    for pattern in patterns:
        match = re.search(pattern, user_message, re.IGNORECASE)
        if match:
            try:
                player_id = int(match.group(1))
                season = int(match.group(2))
                week = int(match.group(3))
                
                # Validate ranges
                if 2020 <= season <= 2030 and 1 <= week <= 18:
                    return {
                        "player_id": player_id,
                        "season": season,
                        "week": week
                    }
            except (ValueError, IndexError):
                continue
    
    return None

def make_prediction_request(api_base_url: str, player_id: int, season: int, week: int) -> Dict[str, Any]:
    """
    Make a prediction request to the API.
    """
    try:
        response = requests.post(
            f"{api_base_url}/predict",
            json={
                "player_id": player_id,
                "season": season,
                "week": week
            },
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            return {
                "success": True,
                "data": result,
                "message": f"Prediction successful! Expected fantasy points: {result['expected_points']:.2f}"
            }
        else:
            return {
                "success": False,
                "error": f"API Error {response.status_code}: {response.text}",
                "message": f"Sorry, I couldn't get a prediction. Error: {response.status_code}"
            }
            
    except requests.exceptions.RequestException as e:
        return {
            "success": False,
            "error": str(e),
            "message": "Sorry, I couldn't connect to the prediction service."
        }

def format_prediction_response(prediction_result: Dict[str, Any]) -> str:
    """
    Format the prediction result into a user-friendly message.
    """
    if prediction_result["success"]:
        data = prediction_result["data"]
        return f"""
🎯 **Fantasy Points Prediction**

**Player ID:** {data['player_id']}
**Season:** {data['season']}
**Week:** {data['week']}
**Expected Points:** **{data['expected_points']:.2f}**

This prediction is based on historical performance data and advanced statistical modeling.
        """.strip()
    else:
        return f"❌ **Error:** {prediction_result['message']}"

def create_system_prompt() -> str:
    """
    Create the system prompt for the Ollama model.
    """
    return """You are a helpful fantasy football assistant with access to a prediction API. You can help users get fantasy points predictions for NFL players.

**Your Capabilities:**
1. Answer general fantasy football questions
2. Make predictions using the API when users provide player information
3. Explain predictions and provide context

**How to Make Predictions:**
When users ask for predictions, look for:
- Player ID (number)
- Season (4-digit year like 2024)
- Week (1-18)

**Example user requests you can handle:**
- "Predict fantasy points for player 12345 in season 2024 week 1"
- "What are the expected points for player 67890, 2024 season, week 5?"
- "Can you predict fantasy points for player 11111 in 2024 week 10?"

**API Response Format:**
The API returns predictions with expected fantasy points based on historical data and statistical modeling.

**Important Notes:**
- Always be helpful and informative
- If you can't extract prediction parameters, ask the user to provide player ID, season, and week
- Explain what the predictions mean and provide context
- Be conversational and engaging

Remember: You're here to help users make informed fantasy football decisions!""" 