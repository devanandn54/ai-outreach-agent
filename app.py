import streamlit as st
import tempfile, os, json
from dotenv import load_dotenv
from agent.graph import run_agent

load_dotenv()

st.set_page_config(page_title="Outreach Agent", page_icon="⚡", layout="wide")
st.title("⚡ AI Outreach Agent")
st.caption("Research any company → Get personalized emails + resume tweaks")

# --- Sidebar: Resume Upload ---
with st.sidebar:
    st.header("📄 Your Resume")
    uploaded_file = st.file_uploader(
        "Upload PDF or DOCX",
        type=["pdf", "docx"],
    )
    target_role = st.selectbox(
        "Target Role",
        ["CTO", "CEO", "VP Engineering", "Head of Product"],
    )

# --- Main: Company Input ---
company_name = st.text_input(
    "🏢 Company Name",
    placeholder="e.g. Stripe, Notion, Vercel...",
)

if st.button("🔍 Research & Generate", type="primary"):
    if not uploaded_file:
        st.error("Please upload your resume first.")
    elif not company_name:
        st.error("Please enter a company name.")
    else:
        # Save uploaded file to temp path
        suffix = "." + uploaded_file.name.split(".")[-1]
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as f:
            f.write(uploaded_file.getvalue())
            resume_path = f.name

        # Run the agent with progress
        with st.spinner("🧠 Agent is researching... (30-60 seconds)"):
            result = run_agent(company_name, resume_path, target_role)

        # --- Display Results in Tabs ---
        tab1, tab2, tab3, tab4 = st.tabs([
            "📊 Research", "📧 Emails", "✏️ Resume Tweaks", "👥 Contacts"
        ])

        with tab1:
            st.subheader(f"Research: {company_name}")
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Industry", result["company_industry"])
                st.metric("Stage", result["company_stage"])
            with col2:
                st.write("**Pain Points:**")
                for p in result["company_pain_points"]:
                    st.write(f"• {p}")
            st.write("**Your Value Props:**")
            for v in result["value_propositions"]:
                st.success(v)

        with tab2:
            st.subheader("Generated Outreach Emails")
            for email in result["generated_emails"]:
                with st.expander(
                    f"📧 {email['variant']} → {email['recipient']}"
                ):
                    st.write(f"**Subject:** {email['subject_line']}")
                    st.text_area(
                        "Email Body",
                        email["body"],
                        height=200,
                        key=f"email_{email['variant']}_{email['recipient']}",
                    )
                    st.caption(f"Strategy: {email['strategy']}")

        with tab3:
            st.subheader("✏️ Resume Tweaks for " + company_name)
            st.info(f"**Tailored Summary:** {result['tailored_summary']}")
            for tweak in result["resume_tweaks"]:
                with st.expander(f"Section: {tweak['section']}"):
                    st.write(f"**Current:** {tweak['current_text']}")
                    st.write(f"**Suggested:** {tweak['suggested_text']}")
                    st.caption(f"Reason: {tweak['reason']}")

        with tab4:
            st.subheader("👥 Leadership Contacts")
            for c in result["leadership_contacts"]:
                st.write(f"**{c['name']}** — {c['title']}")
                if c.get("linkedin_url"):
                    st.write(f"[LinkedIn]({c['linkedin_url']})")

        # Cleanup
        os.unlink(resume_path)