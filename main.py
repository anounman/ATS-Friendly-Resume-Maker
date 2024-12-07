import json

import streamlit as st

from chain import Chain

late_code = r""" 
\documentclass[a4paper,10pt]{article}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage{geometry}
\usepackage{enumitem}
\usepackage{multicol}
\usepackage{titlesec}
\usepackage{fontawesome5}
\usepackage{hyperref}
\usepackage{ragged2e}
\usepackage{helvet}
\usepackage{lmodern}
\renewcommand{\familydefault}{\sfdefault}
\usepackage[scaled=0.92]{helvet}

% Page layout
\geometry{left=1in, right=1in, top=0.5in, bottom=0.5in}
\pagestyle{empty}
\setlength{\parindent}{0pt}
\setlength{\columnsep}{1cm}

% Hyperlink formatting
\hypersetup{
    colorlinks=true,
    urlcolor=black,
    pdftitle={Professional Resume},
    pdfauthor={Taha Murtaza Gain}
}

% Custom section formatting
\titleformat{\section}{\large\bfseries}{}{0pt}{\uppercase}
\titlespacing*{\section}{0pt}{12pt}{6pt}

\begin{document}
% Header
\begin{center}
    \textbf{\Large Taha Murtaza Gain} \\[0.2em]
    \small 
    \href{mailto:gaintaha@gmail.com}{\faEnvelope{} gaintaha@gmail.com} \quad 
    \faPhone{} +49 15753981516 \quad 
    \faMapMarker{} Saarbrucken, Germany \\[0.2em]
    \href{https://www.linkedin.com/in/taha-murtaza-gain-a6a919171/}{\faLinkedin{} https://www.linkedin.com/in/taha-murtaza-gain-a6a919171/}
\end{center}

\vspace{0.5em}

\begin{multicols}{2}
% Left Column
\section*{Professional Summary}
\justifying
Highly motivated and detail-oriented software engineer with experience in Python, Django, and Microsoft Power Platform. Proficient in developing web applications and working with various technologies. Strong understanding of software development life cycles and Agile methodologies.

\section*{Technical Skills}
\vspace{-0.3em}
\hspace{1em}\textbf{Programming Languages}
\vspace{-0.2em}
\begin{itemize}[leftmargin=1em,itemsep=0.3em,parsep=0pt,label=$\bullet$]
    \item Python
    \item JavaScript
    \item Kotlin
    \item Java
    \item PHP
\end{itemize}

\vspace{0.3em}
\textbf{Technologies}
\vspace{-0.2em}
\begin{itemize}[leftmargin=1em,itemsep=0.3em,parsep=0pt,label=$\bullet$]
    \item Django
    \item Microsoft Power Platform
    \item Microsoft Dynamics 365
    \item Android Development
    \item HTML
    \item CSS
\end{itemize}

\vspace{0.3em}
\textbf{Development Tools}
\vspace{-0.2em}
\begin{itemize}[leftmargin=1em,itemsep=0.3em,parsep=0pt,label=$\bullet$]
    \item Power Apps
    \item Power Automate
    \item Visual Studio Code
    \item Android Studio
\end{itemize}

\section*{Soft Skills}
\vspace{-0.2em}
\begin{itemize}[leftmargin=1em,itemsep=0.2em,parsep=0pt,label=$\cdot$]
    \item Teamwork
    \item Communication
    \item Problem-solving
    \item Time management
    \item Adaptability
\end{itemize}

\section*{Languages}
\vspace{-0.2em}
\begin{itemize}[leftmargin=1em,itemsep=0.2em,parsep=0pt]
    \item Urdu (mother tongue)
    \item English (C2 listening, C1 reading, C1 spoken production, C1 spoken interaction, B2 writing)
    \item German (A2 listening, A2 reading, A2 spoken production, A2 spoken interaction, A2 writing)
\end{itemize}

% Right Column
\columnbreak
\section*{Professional Experience}
\vspace{-0.5em}
\begin{itemize}[leftmargin=1em,itemsep=0.3em,parsep=0pt]
    \item Working Student, MUTARES SE \& CO. KGAA (2024-01-15 - present)
        \begin{itemize}[leftmargin=1em,itemsep=0.2em,parsep=0pt,label=$\cdot$]
            \item Discussed client requirements and designed tailored solutions
            \item Developed applications using Power Platform tools and custom JS
            \item Applied validations and automated workflows with Power Automate
            \item Tested systems and conducted final reviews with clients
            \item Worked within Agile methodology for continuous improvement
        \end{itemize}
    \item Working Student, SOFTWARE AG (2022-06-15 - 2023-12-31)
        \begin{itemize}[leftmargin=1em,itemsep=0.2em,parsep=0pt,label=$\cdot$]
            \item Developed web applications using PHP, TWIG, CSS, and JavaScript
            \item Created custom modules and themes in Drupal; utilized Views
            \item Fixed bugs and ensured website functionality
            \item Collaborated with teams to deliver web solutions
        \end{itemize}
    \item Associate Consultant, SYSTEMS LIMITED (2021-03-31 - 2022-03-03)
        \begin{itemize}[leftmargin=1em,itemsep=0.2em,parsep=0pt,label=$\cdot$]
            \item Part of the development team working on customer service module for IRENA
            \item Created a customer service portal and power virtual agent demonstration for MusicTribe
        \end{itemize}
    \item Intern, SYSTEMS LIMITED (2020-12-22 - 2021-03-30)
        \begin{itemize}[leftmargin=1em,itemsep=0.2em,parsep=0pt,label=$\cdot$]
            \item Training related to Microsoft dynamics 365 modules and Power platform
            \item Hands on experience of custom plugins, custom workflows and actions using C\#
            \item Hands on experience of customization, workflows and validations using javascript
        \end{itemize}
\end{itemize}

\section*{Notable Projects}
\vspace{-0.5em}
\begin{itemize}[leftmargin=1em,itemsep=0.3em,parsep=0pt]
    \item Route Selection to Multiple Destinations using Optimal Path Algorithm (2019-08-31 - 2020-01-14)
        \begin{itemize}[leftmargin=1em,itemsep=0.2em,parsep=0pt,label=$\cdot$]
            \item Developed a bus hailing application using android studio for optimal Path estimation as Final Year Project (FYP)
        \end{itemize}
    \item Speaker-Independent Spoken Digit Recognition (2023-03-01 - 2023-03-31)
        \begin{itemize}[leftmargin=1em,itemsep=0.2em,parsep=0pt,label=$\cdot$]
            \item Developed a Speaker-independent spoken digit recognition (SDR) system using machine learning techniques
        \end{itemize}
    \item Anti-Doping: Sample Swapping detection (2022-07-01 - 2022-07-31)
        \begin{itemize}[leftmargin=1em,itemsep=0.2em,parsep=0pt,label=$\cdot$]
            \item Developed a Sample Swapping detection system that would identify if an athlete has swapped their sample or not using Neural Network models
        \end{itemize}
\end{itemize}

\section*{Education}
\vspace{-0.5em}
\begin{itemize}[leftmargin=1em,itemsep=0.3em,parsep=0pt]
    \item Master of Science in Computer Science, Saarland University (2022-03-31 - present)
    \item Bachelor of Science in Computer Science, Bahria University (2017-02-05 - 2021-02-22)
\end{itemize}

\section*{Certificates}
\vspace{-0.5em}
\begin{itemize}[leftmargin=1em,itemsep=0.1em,parsep=0pt]
    \item PL-200 Microsoft Power Platform Functional Consultant (2021-09-26)
    \item MB-230 Microsoft Dynamics 365 Customer Service Functional Consultant (2021-08-08)
    \item MB-901 Microsoft Dynamics 365 Fundamentals (2021-04-11)
    \item PL-900 Microsoft Power Platform Fundamentals (2021-03-23)
\end{itemize}
\end{multicols}
\end{document}
"""

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
                    tab1, tab2, tab3 = st.tabs(["📑 CV Preview", "⚙️ LaTeX Code", "📊 ATS Score"])
                    
                    with tab1:
                        st.markdown("### Generated CV")
                        # Add your PDF display logic here
                    
                    with tab2:
                        st.markdown("### LaTeX Source")
                        st.code(latex_cv, language='latex')
                    
                    with tab3:
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