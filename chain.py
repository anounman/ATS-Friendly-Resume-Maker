import json
import os

import streamlit as st
from dotenv import load_dotenv
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq
from PyPDF2 import PdfReader

load_dotenv()


class Chain:
    def __init__(self):
        apikey = os.getenv("lama_api") or st.secrets.get("LAMA_API")
        self.llm = ChatGroq(
        temperature=0,
        timeout=None,
        groq_api_key=os.getenv("lama_api"),
        model_name="llama-3.1-70b-versatile"
        )
    def extract_text_from_pdf(self , pdf_file):
        reader = PdfReader(pdf_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text

    def process_cv_text_with_llm(self , text , st):
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
            response = self.llm.invoke(prompt_content)
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


    def generate_cv_with_llm(self , transformed_data , job_description , st):
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

            % Page layout
            \\geometry{{left=1in, right=1in, top=0.5in, bottom=0.5in}}
            \\pagestyle{{empty}}
            \\setlength{{\\parindent}}{{0pt}}
            \\setlength{{\\columnsep}}{{1cm}}

            % Hyperlink formatting
            \\hypersetup{{
                colorlinks=true,
                urlcolor=black,
                pdftitle={{Professional Resume}},
                pdfauthor={{[NAME]}}
            }}

            % Custom section formatting
            \\titleformat{{\\section}}{{\\large\\bfseries}}{{}}{{0pt}}{{\\uppercase}}
            \\titlespacing*{{\\section}}{{0pt}}{{12pt}}{{6pt}}

            \\begin{{document}}
            % Header
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
            % Left Column
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

            % Right Column
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
        
        ### **Instructions:**
            1. Start by aligning the CV data with the job description.  
            - For **missing attributes**, infer and add relevant information accoring to the job description.  
            - For **irrelevant attributes**, remove or de-emphasize those sections.  
            2. Structure the CV according to the provided LaTeX template, ensuring it is visually appealing and compliant with professional standards and it should strictly follow the given latex templete.  
            3. Return only the updated LaTeX code with changes incorporated based on the job description.  
            4. Do not include markdown formatting or additional explanations in the output.  
        """
        
        try:
            response = self.llm.invoke(prompt)
            return response.content.removeprefix("```latex").removesuffix("```")
        except Exception as e:
            st.error(f"Error generating LaTeX CV: {e}")
            return None


    def ats_checker(self, job_description, cv_code, st):
        prompt_extract = PromptTemplate.from_template(
            """
            Analyze the CV and job description to determine ATS compatibility.
            Return ONLY a numeric score between 0-100 without any additional text or explanation.
            
            Job Description:
            ---
            {job_description}
            ---
        
            CV:
            ---
            {cv_code}
            ---
            """
        )
        try:
            chain_extract = prompt_extract | self.llm
            response = chain_extract.invoke(input={
                "job_description": job_description,
                "cv_code": cv_code
            })
            
           
    
            return response.content
            
        except Exception as e:
            st.error(f"Error calculating ATS score: {e}")
            return 0.0
       