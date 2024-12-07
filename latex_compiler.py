import re

import streamlit as st
from fpdf import FPDF

import main


def parse_latex(latex_code):
    """
    Parses LaTeX code to extract text content and commands.

    Args:
        latex_code (str): The LaTeX code to parse.

    Returns:
        list: Parsed commands and text.
    """
    parsed_content = []
    commands = re.findall(r"\\(section|item|textbf|textit)\{(.*?)\}", latex_code)
    text_blocks = re.split(r"\\[a-z]+\{.*?\}", latex_code)

    for text in text_blocks:
        if text.strip():
            parsed_content.append(("text", text.strip()))
    for command, content in commands:
        parsed_content.append((command, content))

    return parsed_content


class CustomPDF(FPDF):
    def add_section(self, title):
        self.set_font("Arial", "B", 16)
        self.cell(0, 10, title, ln=True)
        self.ln(5)

    def add_text(self, text):
        self.set_font("Arial", size=12)
        self.multi_cell(0, 10, text)
        self.ln()

    def add_list_item(self, item):
        self.set_font("Arial", size=12)
        self.cell(10)  # Indent for list item
        self.cell(0, 10, f"• {item}", ln=True)


def compile_latex_to_pdf(latex_code):
    """
    Compiles LaTeX code into a PDF file using FPDF.

    Args:
        latex_code (str): The LaTeX code to compile.

    Returns:
        bytes: The binary content of the generated PDF file.
    """
    parsed_content = parse_latex(latex_code)
    pdf = CustomPDF()
    pdf.add_page()

    for command, content in parsed_content:
        if command == "text":
            pdf.add_text(content)
        elif command == "section":
            pdf.add_section(content)
        elif command == "item":
            pdf.add_list_item(content)
        elif command == "textbf":
            pdf.set_font("Arial", "B", 12)
            pdf.multi_cell(0, 10, content)
            pdf.set_font("Arial", size=12)
        elif command == "textit":
            pdf.set_font("Arial", "I", 12)
            pdf.multi_cell(0, 10, content)
            pdf.set_font("Arial", size=12)

    return pdf.output(dest="S").encode("latin1")


def display_pdf_on_streamlit(pdf_content):
    """
    Displays the PDF content on a Streamlit web application.

    Args:
        pdf_content (bytes): The binary content of the PDF file.
    """
    st.download_button(
        label="Download PDF",
        data=pdf_content,
        file_name="output.pdf",
        mime="application/pdf",
    )


if __name__ == "__main__":
    st.title("LaTeX to PDF Compiler")

    # Example LaTeX code
    
    latex_code = st.text_area("Enter LaTeX Code:", latex_code, height=300)

    if st.button("Compile to PDF"):
        try:
            pdf_content = compile_latex_to_pdf(latex_code)
            st.success("PDF compiled successfully!")
            display_pdf_on_streamlit(pdf_content)
        except Exception as e:
            st.error(f"Error: {e}")
