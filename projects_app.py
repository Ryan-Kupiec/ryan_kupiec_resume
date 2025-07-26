import streamlit as st

st.title("Ryan Kupiec - Personal Projects & Resume")

# Create tabs
tab1, tab2, tab3 = st.tabs(["📄 Resume", "🚀 Projects", "📧 Contact"])

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