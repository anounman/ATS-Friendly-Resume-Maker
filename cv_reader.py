import base64
import json
import os
import shutil
import subprocess
import tempfile

import streamlit as st
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq
from pylatex import Command, Document, Section
from PyPDF2 import PdfReader

# Initialize the LLM
llm = ChatGroq(
    temperature=0,
    timeout=None,
    groq_api_key='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',
    model_name="llama-3.1-70b-versatile"
)

def extract_text_from_pdf(pdf_file):
    reader = PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

def process_cv_text_with_llm(text):
    prompt = PromptTemplate.from_template("""
    You are an AI specialized in extracting structured data from CVs.
    Extract the key information from the following CV and present it in JSON format.
    Only output the JSON data without any additional text.

    CV Text:
    ---
    {text}
    ---
    """)
    
    try:
        prompt_content = prompt.format(text=text)
        response = llm.invoke(prompt_content)
        if not response.content: 
            return {}
        
    except Exception as e:
        st.error(f"Error: {e}")
        return {}

    try:
        json_parser = JsonOutputParser()
        extracted_data = json_parser.parse(response.content)

        return extracted_data

    except json.JSONDecodeError as e:
        st.error(f"JSON Parse Error: {e}")
        return {}


def generate_cv_with_llm(transformed_data , job_description):
    LATEX_TEMPLATE = r"""
        \\documentclass[a4paper,10pt]{{article}}
        \\usepackage[utf8]{{inputenc}}
        \\usepackage[T1]{{fontenc}}
        \\usepackage{{geometry}}
        \\usepackage{{enumitem}}
        \\usepackage{{multicol}}
        \\usepackage{{titlesec}}
        \\usepackage{{fontawesome5}}
        \\usepackage{{hyperref}}
        \\usepackage{{ragged2e}}
        \\usepackage{{helvet}}
        \\usepackage{{lmodern}}
        \\renewcommand{{\\familydefault}}{{\\sfdefault}}
        \\usepackage[scaled=0.92]{{helvet}}

        \\geometry{{left=1in, right=1in, top=0.5in, bottom=0.5in}}
        \\pagestyle{{empty}}
        \\setlength{{\\parindent}}{{0pt}}
        \\setlength{{\\columnsep}}{{1cm}}

        \\hypersetup{{
            colorlinks=true,
            urlcolor=black,
            pdftitle={{Professional Resume}},
            pdfauthor={{[NAME]}}
        }}

        \\titleformat{{\\section}}{{\\large\\bfseries}}{{}}{{0pt}}{{\\uppercase}}
        \\titlespacing*{{\\section}}{{0pt}}{{12pt}}{{6pt}}

        \\begin{{document}}
        \\begin{{center}}
            \\textbf{{\\Large [NAME]}} \\\\[0.2em]
            \\small 
            \\href{{mailto:[EMAIL]}}{{\\faEnvelope{} [EMAIL]}} \\quad 
            \\faPhone{} [PHONE] \\quad 
            \\faMapMarker{} [LOCATION] \\\\[0.2em]
            \\href{{[GITHUB_URL]}}{{\\faGithub{} [GITHUB]}} \\quad 
            \\href{{[LINKEDIN_URL]}}{{\\faLinkedin{} [LINKEDIN]}} \\quad 
            \\href{{[WEBSITE_URL]}}{{\\faGlobe{} [WEBSITE]}}
        \\end{{center}}

        \\vspace{{0.5em}}

        \\begin{{multicols}}{{2}}

        \\section*{{Professional Summary}}
        \\justifying
        [PROFESSIONAL_SUMMARY]

        \\section*{{Technical Skills}}
        \\vspace{{-0.3em}}
        \\hspace{{1em}}\\textbf{{Programming Languages}}
        \\vspace{{-0.2em}}
        \\begin{{itemize}}[leftmargin=1em,itemsep=0.3em,parsep=0pt,label=$\\bullet$]
            [PROGRAMMING_LANGUAGES]
        \\end{{itemize}}

        \\vspace{{0.3em}}
        \\textbf{{Technologies}}
        \\vspace{{-0.2em}}
        \\begin{{itemize}}[leftmargin=1em,itemsep=0.3em,parsep=0pt,label=$\\bullet$]
            [TECHNOLOGIES]
        \\end{{itemize}}

        \\vspace{{0.3em}}
        \\textbf{{Development Tools}}
        \\vspace{{-0.2em}}
        \\begin{{itemize}}[leftmargin=1em,itemsep=0.3em,parsep=0pt,label=$\\bullet$]
            [DEV_TOOLS]
        \\end{{itemize}}

        \\section*{{Soft Skills}}
        \\vspace{{-0.2em}}
        \\begin{{itemize}}[leftmargin=1em,itemsep=0.2em,parsep=0pt,label=$\\cdot$]
            [SOFT_SKILLS]
        \\end{{itemize}}

        \\section*{{Languages}}
        \\vspace{{-0.2em}}
        \\begin{{itemize}}[leftmargin=1em,itemsep=0.2em,parsep=0pt]
            [LANGUAGES]
        \\end{{itemize}}

        \\columnbreak
        \\section*{{Professional Experience}}
        \\vspace{{-0.5em}}
        [EXPERIENCE]

        \\section*{{Notable Projects}}
        \\vspace{{-0.5em}}
        [PROJECTS]

        \\section*{{Education}}
        \\vspace{{-0.5em}}
        [EDUCATION]

        \\section*{{Certificates}}
        \\vspace{{-0.5em}}
        \\begin{{itemize}}[leftmargin=1em,itemsep=0.1em,parsep=0pt]
            [CERTIFICATES]
        \\end{{itemize}}
        \\end{{multicols}}
        \\end{{document}}
        """
    prompt = f"""
    As a LaTeX expert, your task is to generate a professional CV by filling in the placeholders in the provided LaTeX template with the corresponding data from the CV data.
    Additionally, adjust the content by adding or removing information to best fit the provided job description. 
    The output should strictly follow the exact layout, design, and formatting of the template.

    ### Requirements:

    1. Template Adherence: Use the exact LaTeX template provided. Maintain all spacing, formatting, and structure, including section titles and ordering.
    2. Placeholder Replacement: Replace all placeholders (e.g., [NAME], [EMAIL]) with the appropriate data from the CV data.
    3. Job Description Alignment: Add or remove information from the CV data to highlight the most relevant skills and experiences that match the job description. If there is a skill or something that is mentioned in the job description but not in the CV data, you can add it to the CV if it's a skill then add it in the skill section other wise add it on the summary section.
    sumarry section must content all the skills and the requirments that is mention on the job description. And also add some keyword that are related to the perticular job if needed. 
    4. Data Integration: Ensure all sections are filled using the adjusted CV data. If certain data is missing or not relevant, leave the corresponding placeholder empty.
    5. LaTeX Formatting: Properly escape any LaTeX special characters in the data to prevent compilation errors.
    6. Output Format: Return only the complete LaTeX code without any additional text, explanations, or markdown formatting.

    ### Provided  CV Data:
    {json.dumps(transformed_data, indent=2)}
    
    ### Job Description:
    {job_description}
    
    ### Template:
    
    {LATEX_TEMPLATE}
      
    """
    
    try:
        response = llm.invoke(prompt)
        return response.content.removeprefix("```latex").removesuffix("```")
    except Exception as e:
        st.error(f"Error generating LaTeX CV: {e}")
        return None


def ats_checker(job_description, cv_code):
    prompt_extract = PromptTemplate.from_template(
        """
        You are an AI specialized in analyzing CVs for Applicant Tracking Systems (ATS) compatibility.
        Analyze the provided CV and job description to determine the compatibility score based on the ATS criteria.
        Return the compatibility score as a percentage.
        
        Job Description:
        {job_description}
        CV:
        {cv_code}
        ### **Instructions:**
        1. Analyze the CV and job description to identify relevant keywords and attributes.
        2. Evaluate the CV based on the ATS criteria to determine the compatibility score.
        3. Return the compatibility score as a percentage.
        4. Do not include markdown formatting or additional explanations in the output. 
        
        """
    )
    try:
            chain_extract = prompt_extract | llm
            response_extract = chain_extract.invoke(input={"job_description":job_description, "cv_code" : cv_code})
    except Exception as e:
        st.error(f"Error generating ATS Score: {e}")
        return
    

    return response_extract.content
    
    
def convert_to_pdf(latex_code):
    doc = Document()
    with doc.create(Section('Generated Content')):
        doc.append(latex_code)

    pdf_file_path = "output.pdf"
    doc.generate_pdf(pdf_file_path, clean_tex=False)

    return pdf_file_path

   
def display_pdf(pdf_data):
    base64_pdf = base64.b64encode(pdf_data).decode('utf-8')
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)

def create_download_link(file_path):
    with open(file_path, "rb") as f:
        pdf_data = f.read()
    b64 = base64.b64encode(pdf_data).decode()
    return f'<a href="data:application/pdf;base64,{b64}" download="generated.pdf">Download PDF</a>'

# Streamlit app

st.title("CV Generator Accoring to Job Description")

## Job description
st.write("Enter the job description below:")
job_description = st.text_area("Job Description", "We are looking for a software engineer with experience in Python and Django.")

st.write("Upload a PDF file to extract CV details.")

uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")


if uploaded_file and job_description and st.button("Process CV"):
    with st.spinner("Extracting Data from the CV..."):
        cv_text = extract_text_from_pdf(uploaded_file)
        response = process_cv_text_with_llm(cv_text)
    try:
            st.success("Data extraction succeed")

            # Generate LaTeX CV
            with st.spinner("Generating LaTeX CV..."):
                latex_cv = generate_cv_with_llm(response , job_description)
            
            if latex_cv:
                
                # Show LaTeX code
                st.subheader("LaTeX Code")
                st.code(latex_cv, language='latex')
                
                        
            else:
                st.error("Failed to generate LaTeX")
                
            # ATS Checker
            st.subheader("ATS Compatibility Score")
            with st.spinner("Checking ATS Compatibility..."):
                ats_score = ats_checker(job_description, response)
            if ats_score:
                st.write(f"ATS Compatibility Score: {ats_score}")
            else:
                st.error("Failed to generate ATS Score")
    except json.JSONDecodeError as e:
            st.error(f"Failed to parse JSON response: {e}")
    except Exception as e:
            st.error(f"An error occurred: {e}")
            st.write("Response content:")
            st.write(response)    

