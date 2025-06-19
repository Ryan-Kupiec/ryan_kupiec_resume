import streamlit as st

st.title("Ryan Kupiec - Personal Projects & Resume")

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

---
""")

st.header("Relevant Projects")

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

for project in projects:
    st.subheader(project["title"])
    st.write(project["description"])
    st.write("Technologies: " + ", ".join(project["technologies"]))
    if project["link"]:
        st.markdown(f"[Project Link]({project['link']})")
    st.markdown("---") 