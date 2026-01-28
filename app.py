import streamlit as st
from src.helper import extract_text_from_pdf, ask_groq
from src.job_api import fetch_linkedin_jobs, fetch_naukri_jobs

st.set_page_config(page_title="Job Recommender", layout="wide")
st.title("📄 AI Job Recommender")
st.markdown("Upload your resume and get job recommendations based on your skills and experience from LinkedIn and Naukri.")

uploaded_file = st.file_uploader("Upload your resume (PDF)", type=["pdf"])

if uploaded_file:
    with st.spinner("Extracting text from your resume..."):
        resume_text = extract_text_from_pdf(uploaded_file)

    with st.spinner("Summarizing your resume..."):
        summary = ask_groq(
            f"Summarize this resume highlighting the skills, education, and experience:\n\n{resume_text}",
            max_tokens=500
        )

    with st.spinner("Finding skill gaps..."):
        gaps = ask_groq(
            f"Analyze this resume and highlight missing skills, certifications, and experiences needed for better job opportunities:\n\n{resume_text}",
            max_tokens=400
        )

    with st.spinner("Creating future roadmap..."):
        roadmap = ask_groq(
            f"Based on this resume, suggest a future roadmap to improve career prospects (skills, certifications, industry exposure):\n\n{resume_text}",
            max_tokens=400
        )

    st.markdown("---")
    st.header("📑 Resume Summary")
    st.markdown(f"<div style='background-color:#000;padding:15px;border-radius:10px;color:white;'>{summary}</div>", unsafe_allow_html=True)

    st.markdown("---")
    st.header("🛠️ Skill Gaps")
    st.markdown(f"<div style='background-color:#000;padding:15px;border-radius:10px;color:white;'>{gaps}</div>", unsafe_allow_html=True)

    st.markdown("---")
    st.header("🚀 Future Roadmap")
    st.markdown(f"<div style='background-color:#000;padding:15px;border-radius:10px;color:white;'>{roadmap}</div>", unsafe_allow_html=True)

    st.success("✅ Analysis Completed Successfully!")

    if st.button("🔎 Get Job Recommendations"):
        with st.spinner("Extracting job keywords..."):
            keywords = ask_groq(
                f"Based on this resume summary, suggest best job titles and search keywords. Give comma-separated list only.\n\nSummary:\n{summary}",
                max_tokens=100
            )

        search_keywords_clean = keywords.replace("\n", "").strip()
        st.success(f"Extracted Job Keywords: {search_keywords_clean}")

        with st.spinner("Fetching jobs..."):
            linkedin_jobs = fetch_linkedin_jobs(search_keywords_clean)
            naukri_jobs = fetch_naukri_jobs(search_keywords_clean)

        st.markdown("---")
        st.header("💼 LinkedIn Jobs")

        for job in linkedin_jobs or []:
            st.markdown(f"**{job.get('title')}** at *{job.get('companyName')}*")
            st.markdown(f"- 📍 {job.get('location')}")
            st.markdown(f"- 🔗 [View Job]({job.get('link')})")
            st.markdown("---")

        st.header("💼 Naukri Jobs")

        for job in naukri_jobs or []:
            st.markdown(f"**{job.get('title')}** at *{job.get('companyName')}*")
            st.markdown(f"- 📍 {job.get('location')}")
            st.markdown(f"- 🔗 [View Job]({job.get('url')})")
            st.markdown("---")
