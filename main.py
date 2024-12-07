import json

import streamlit as st

from chain import Chain


def create_streamlit_app(chain):
    # Custom CSS
    st.markdown("""
        <style>
        .main {
            background-color: #f5f5f5;
        }
        .stButton>button {
            background-color: #4CAF50;
            color: white;
            padding: 0.5rem 1rem;
            border-radius: 5px;
            border: none;
            transition: all 0.3s ease;
        }
        .stButton>button:hover {
            background-color: #45a049;
            transform: translateY(-2px);
        }
        .title {
            text-align: center;
            color: #2E4053;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        }
        </style>
    """, unsafe_allow_html=True)

    # Title with animation
    st.markdown("<h1 class='title'>✨ Smart CV Generator ✨</h1>", unsafe_allow_html=True)
    st.markdown("---")

    # Two-column layout for input
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📝 Job Description")
        job_description = st.text_area(
            "Enter the job description below:",
            "We are looking for a software engineer with experience in Python and Django.",
            height=200
        )

    with col2:
        st.markdown("### 📄 Upload CV")
        uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
        if uploaded_file:
            st.success("File uploaded successfully! 🎉")

    # Process button with animation
    if uploaded_file and job_description:
        if st.button("🚀 Generate Custom CV"):
            # Progress bar container
            progress_bar = st.progress(0)
            
            # Step 1: Extract Data
            with st.spinner("🔍 Extracting Data from CV..."):
                cv_text = chain.extract_text_from_pdf(uploaded_file)
                response = chain.process_cv_text_with_llm(cv_text , st)
            
                progress_bar.progress(33)
            
            try:
                st.success("✅ Data extraction successful!")

                # Step 2: Generate LaTeX
                with st.spinner("🎨 Generating Custom CV..."):
                    latex_cv = chain.generate_cv_with_llm(response, job_description , st)

                    progress_bar.progress(66)
                
                if latex_cv:
                    # Create tabs for different views
                    tab1, tab2 = st.tabs(["⚙️ LaTeX Code", "📊 ATS Score"])
                    
                    
                    with tab1:
                        st.markdown("### LaTeX Source")
                        st.code(latex_cv, language='latex')
                    
                    with tab2:
                        st.markdown("### ATS Analysis")
                        with st.spinner("📊 Analyzing ATS Compatibility..."):
                            ats_score = chain.ats_checker(job_description, response , st)
                            progress_bar.progress(100)
                            
                        if ats_score:
                            score_value = float(ats_score.strip('%'))
                            st.markdown(f"### ATS Compatibility Score: {ats_score}")
                            
                            # Circular progress indicator
                            html_code = f"""
                                <div class=uge" style="
                                    width: 200px;
                                    height: 200px;
                                    border-radius: 50%;
                                    background: conic-gradient(
                                        #4CAF50 {score_value * 3.6}deg, 
                                        #f0f0f0 {score_value * 3.6}deg
                                    );
                                    margin: auto;
                                ">
                                    <div style="
                                        position: relative;
                                        top: 50%;
                                        left: 50%;
                                        transform: translate(-50%, -50%);
                                        text-align: center;
                                        font-size: 2em;
                                        color: #2E4053;
                                    ">
                                        {ats_score}
                                    </div>
                                </div>
                            """
                            st.markdown(html_code, unsafe_allow_html=True)
                        else:
                            st.error("❌ Failed to generate ATS Score")
                
                else:
                    st.error("❌ Failed to generate LaTeX")
                    
            except json.JSONDecodeError as e:
                st.error(f"❌ Failed to parse JSON response: {e}")
            except Exception as e:
                st.error(f"❌ An error occurred: {e}")
                with st.expander("Show Error Details"):
                    st.write("Response content:")
                    st.write(response)
    else:
        st.info("👆 Please upload a CV and provide a job description to proceed.")

    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: #666;'>
            Built By ❤️ Ankush
        </div>
        """, 
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    chain = Chain()
    
    create_streamlit_app(chain)