import streamlit as st
import ollama
import requests
import json
from datetime import datetime
from src.chat_utils import (
    extract_prediction_request, 
    make_prediction_request, 
    format_prediction_response,
    create_system_prompt
)

# Initialize Ollama client
try:
    ollama_client = ollama.Client(host='http://localhost:11434')
except:
    ollama_client = None

# API configuration
API_BASE_URL = "http://localhost:8000"

st.title("Ryan Kupiec - Personal Projects & Resume")

# Create tabs
tab1, tab2, tab3, tab4 = st.tabs(["📄 Resume", "🚀 Projects", "🤖 AI Fantasy Assistant", "📧 Contact"])

with tab1:
    st.header("Resume")
    
    st.markdown("""
    **Chicago, IL 60638**  
    [ryankupiec21@gmail.com](mailto:ryankupiec21@gmail.com)  
    773-456-7843

    ---

    **Career Objective**  
    Proven Data Scientist looking for a role as a Machine Learning Engineer. Striving to leverage my extensive knowledge of statistics and computer science to make a difference in an organization.

    ---

    **Professional Experience**
    - **Data Operations Developer, Morning Consult** (July 2021 - Present)
        - Support code base for 10+ internal R packages to optimize data pipeline and ensure accurate, speedy survey results
        - Developed a Shiny App for Client Services to automate data delivery
        - Reviewed code for optimization and seamless integration
        - Authored automated quality checks to expedite and ensure reliable data generation
        - Collaborated on continuous improvement in tooling and data operations
    - **Teaching Assistant, University of Illinois Urbana-Champaign** (June 2024 - August 2024)
        - Led office hours and discussions on data visualization
        - Supported coding projects and graded assignments for 90 students
        - Provided detailed feedback to ensure comprehension and improvement

    ---

    **Education**
    - **Master of Computer Science - Data Science** (May 2025)  
      University of Illinois Urbana-Champaign
    - **Bachelor of Arts in Data Analytics, cum laude** (May 2021)  
      DePauw University

    ---

    **Technical Skills**
    - R (Expert), Package Development (Expert), Shiny (Expert), Python (Moderate), SQL (Moderate), AWS (Beginner), Docker (Moderate), Kubernetes (Beginner), Argo Workflows (Moderate)
    """)

with tab2:
    st.header("Projects")
    
    # Create columns for better project layout
    col1, col2 = st.columns(2)
    
    projects = [
        {
            "title": "MLB Offensive Output Research Paper",
            "description": "Published MLB research paper with a model to explain as much as 70% of the variation in a player's offensive output using advanced Statcast metrics.",
            "technologies": ["R", "Statcast", "Statistical Modeling"],
            "link": ""
        },
        {
            "title": "Movie Suggestion Application",
            "description": "Movie suggestion application that can use user selected ratings to select movie suggestions.",
            "technologies": ["Python", "Machine Learning", "Recommendation Systems"],
            "link": ""
        },
        {
            "title": "Shiny App for Data Delivery",
            "description": "Developed a Shiny App for Client Services to automate data delivery, reducing manual intervention.",
            "technologies": ["R", "Shiny", "Automation"],
            "link": ""
        },
        {
            "title": "Fantasy Football Points Predictor",
            "description": "Machine learning model that predicts fantasy football points using NFL player data and advanced statistical features.",
            "technologies": ["Python", "FastAPI", "Machine Learning", "NFL Data"],
            "link": ""
        },
    ]
    
    # Display projects in columns
    for i, project in enumerate(projects):
        if i % 2 == 0:
            with col1:
                st.markdown(f"### {project['title']}")
                st.write(project['description'])
                st.write("**Technologies:** " + ", ".join(project["technologies"]))
                if project["link"]:
                    st.markdown(f"[Project Link]({project['link']})")
                st.markdown("---")
        else:
            with col2:
                st.markdown(f"### {project['title']}")
                st.write(project['description'])
                st.write("**Technologies:** " + ", ".join(project["technologies"]))
                if project["link"]:
                    st.markdown(f"[Project Link]({project['link']})")
                st.markdown("---")

with tab3:
    st.header("🤖 AI Fantasy Football Assistant")
    
    # Check if Ollama is available
    if ollama_client is None:
        st.error("⚠️ Ollama is not running. Please start Ollama to use the AI assistant.")
        st.info("To start Ollama, run: `ollama serve` in your terminal")
    else:
        st.success("✅ Ollama is connected and ready!")
    
    # Check if the prediction API is available
    try:
        response = requests.get(f"{API_BASE_URL}/docs", timeout=5)
        api_available = True
    except:
        api_available = False
    
    if not api_available:
        st.error("⚠️ Fantasy Points Prediction API is not running. Please start the API server.")
        st.info("To start the API, run: `uvicorn src.server:app --reload` in your terminal")
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask me about fantasy football predictions..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Display assistant response
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            
            try:
                if ollama_client and api_available:
                    # Check if this is a prediction request
                    prediction_params = extract_prediction_request(prompt)
                    
                    if prediction_params:
                        # Make the API call
                        prediction_result = make_prediction_request(
                            API_BASE_URL,
                            prediction_params["player_id"],
                            prediction_params["season"],
                            prediction_params["week"]
                        )
                        
                        # Format the response
                        api_response = format_prediction_response(prediction_result)
                        
                        # Get AI explanation
                        ai_prompt = f"""A user asked: "{prompt}"

I made an API call and got this result:
{api_response}

Please provide a helpful, conversational response that:
1. Acknowledges their request
2. Explains the prediction result in simple terms
3. Provides context about what the prediction means
4. Offers additional insights or tips

Keep it friendly and informative!"""
                        
                        ai_response = ollama_client.chat(
                            model='llama3.2:3b',
                            messages=[
                                {"role": "system", "content": create_system_prompt()},
                                {"role": "user", "content": ai_prompt}
                            ]
                        )
                        
                        assistant_response = ai_response['message']['content']
                        
                    else:
                        # General conversation - use Ollama with system prompt
                        ai_response = ollama_client.chat(
                            model='llama3.2:3b',
                            messages=[
                                {"role": "system", "content": create_system_prompt()},
                                {"role": "user", "content": prompt}
                            ]
                        )
                        
                        assistant_response = ai_response['message']['content']
                        
                        # Add helpful tip for prediction requests
                        if any(keyword in prompt.lower() for keyword in ['predict', 'points', 'fantasy', 'player']):
                            assistant_response += "\n\n💡 **Tip:** I can make actual predictions! Try asking something like 'Predict fantasy points for player 12345 in season 2024 week 1'"
                    
                else:
                    assistant_response = "I'm sorry, but I'm currently unable to access the prediction API or Ollama. Please make sure both services are running."
                
            except Exception as e:
                assistant_response = f"I encountered an error: {str(e)}"
            
            message_placeholder.markdown(assistant_response)
        
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": assistant_response})
    
    # Sidebar with API testing and help
    with st.sidebar:
        st.header("🔧 Tools & Help")
        
        if api_available:
            st.success("API Status: ✅ Running")
            
            # Quick prediction test
            st.subheader("Test Prediction")
            test_player_id = st.number_input("Player ID", value=12345, step=1)
            test_season = st.number_input("Season", value=2024, step=1)
            test_week = st.number_input("Week", value=1, min_value=1, max_value=18, step=1)
            
            if st.button("Test Prediction"):
                try:
                    response = requests.post(
                        f"{API_BASE_URL}/predict",
                        json={
                            "player_id": test_player_id,
                            "season": test_season,
                            "week": test_week
                        }
                    )
                    
                    if response.status_code == 200:
                        result = response.json()
                        st.success(f"✅ Prediction: {result['expected_points']:.2f} points")
                    else:
                        st.error(f"❌ Error: {response.status_code} - {response.text}")
                        
                except Exception as e:
                    st.error(f"❌ API Error: {str(e)}")
        else:
            st.error("API Status: ❌ Not Running")
        
        # Help section
        with st.expander("💡 How to use the AI Assistant"):
            st.markdown("""
            **Example requests:**
            - "Predict fantasy points for player 12345 in season 2024 week 1"
            - "What are the expected points for player 67890, 2024 season, week 5?"
            - "Can you predict fantasy points for player 11111 in 2024 week 10?"
            
            **General questions:**
            - "What factors affect fantasy football performance?"
            - "How do I interpret fantasy point predictions?"
            - "What's the difference between PPR and standard scoring?"
            """)
        
        # Clear chat button
        if st.button("Clear Chat"):
            st.session_state.messages = []
            st.rerun()

with tab4:
    st.header("Contact")
    
    st.markdown("""
    ### Get in Touch
    
    **Email:** [ryankupiec21@gmail.com](mailto:ryankupiec21@gmail.com)  
    **Phone:** 773-456-7843  
    **Location:** Chicago, IL 60638
    
    ---
    
    ### Connect with Me
    
    - **LinkedIn:** [Add your LinkedIn profile]
    - **GitHub:** [Add your GitHub profile]
    - **Portfolio:** [Add your portfolio website]
    
    ---
    
    ### Let's Work Together
    
    I'm always interested in new opportunities and collaborations. Feel free to reach out!
    """)
    
    # Optional: Add a contact form
    with st.expander("Send me a message"):
        contact_name = st.text_input("Your Name")
        contact_email = st.text_input("Your Email")
        contact_message = st.text_area("Message")
        
        if st.button("Send Message"):
            if contact_name and contact_email and contact_message:
                st.success("Thank you for your message! I'll get back to you soon.")
            else:
                st.error("Please fill in all fields.") 