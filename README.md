# ATS-Friendly CV Generator

An AI-powered tool that analyzes your existing CV and job descriptions to generate LaTeX code for ATS-optimized resumes. The generated LaTeX code can be compiled into a PDF using Overleaf.

🔗 [Live Demo](https://ats-friendly-resume-maker.streamlit.app/)

## Features

- **CV Analysis**: Extracts information from existing PDF resumes
- **Job Matching**: Optimizes content based on job requirements
- **ATS Score**: Shows compatibility with job description
- **LaTeX Generation**: Creates professional, ATS-friendly CV code
- **Real-time Processing**: Instant analysis and generation
- **Customizable Output**: Edit generated LaTeX code as needed

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/yourusername/cv-generator.git
    cd cv-generator
    ```

2. Create virtual environment:

    ```bash
    python -m venv venv
    venv\Scripts\activate
    ```

3. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. Start the application:

    ```bash
    streamlit run main.py
    ```

2. Upload your existing CV (PDF format)
3. Paste the job description
4. Click "Generate Custom CV"
5. View your ATS score and LaTeX code

### Converting to PDF using Overleaf

1. Copy the generated LaTeX code
2. Go to [Overleaf](https://www.overleaf.com)
3. Create a new project
4. Paste the LaTeX code
5. Click "Compile" to generate PDF

## Contributing

1. Fork the repository
2. Create your feature branch:

    ```bash
    git checkout -b feature-name
    ```

3. Commit your changes:

    ```bash
    git commit -m "Add feature"
    ```

4. Push to the branch:

    ```bash
    git push origin feature-name
    ```

5. Open a pull request

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) file for details.

## Contact

- Email: <ankush@grevelops.co>
- Live Demo: <https://ats-friendly-resume-maker.streamlit.app/>
