# setup.py
from setuptools import setup, find_packages

setup(
    name='pdf2md',
    version='1.0.0',
    description='Conversor profissional de PDF para Markdown',
    author='Seu Nome',
    author_email='seu.email@exemplo.com',
    url='https://github.com/seu-usuario/pdf2md',
    packages=find_packages(),
    install_requires=[
        'PyMuPDF>=1.23.0',
        'pdfplumber>=0.10.0',
        'Pillow>=10.0.0',
        'pytesseract>=0.3.10',
        'click>=8.1.0',
    ],
    entry_points={
        'console_scripts': [
            'pdf2md=pdf2md.cli.commands:cli',
        ],
    },
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
