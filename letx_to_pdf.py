import subprocess

import streamlit as st

# Define LaTeX content
latex_code = r"""
\documentclass[a4paper,10pt]{article}
\usepackage[utf8]{inputenc}
\begin{document}
Hello, World! This is a test LaTeX document.
\end{document}
"""

# Write LaTeX content to a .tex file
latex_file = "output.tex"
pdf_file = "output.pdf"

with open(latex_file, "w") as file:
    file.write(latex_code)

# Compile LaTeX to PDF
try:
    subprocess.run(["pdflatex", latex_file], check=True)
    with open(pdf_file, "rb") as pdf:
        pdf_content = pdf.read()
    
    # Display PDF in Streamlit
    st.title("LaTeX PDF Viewer")
    st.download_button(label="Download PDF", data=pdf_content, file_name="output.pdf", mime="application/pdf")
    st.write("Below is the compiled LaTeX PDF:")
    st.components.v1.iframe(pdf_file, width=700, height=500)

except subprocess.CalledProcessError as e:
    st.error("Failed to compile LaTeX code. Please check the syntax.")
