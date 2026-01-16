from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="pdf2md",
    version="1.0.0",
    author="Seu Nome",
    description="Conversor profissional de PDF para Markdown",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "PyMuPDF>=1.23.0",
        "pdfplumber>=0.10.0",
        "tabula-py>=2.8.0",
        "pytesseract>=0.3.10",
        "Pillow>=10.0.0",
        "click>=8.1.0",
        "rich>=13.0.0",
        "tqdm>=4.65.0",
        "python-dotenv>=1.0.0",
        "pyyaml>=6.0",
    ],
    entry_points={
        "console_scripts": [
            "pdf2md=pdf2md.__main__:main",
        ],
    },
)
