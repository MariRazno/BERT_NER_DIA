import os
from setuptools import setup, find_packages

def get_requirements():
    # Install package dependencies
    os.system("pip3 install -r requirements.txt")
    # Download the spaCy model
    os.system("python3 -m spacy download de_core_news_sm")


with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name='bert-ner-dia',
    description='A python script for fine-tuned BERT model usage',
    long_description=long_description,
    version='0.1',
    packages=find_packages(),
    long_description_content_type="text/markdown",
    url='https://github.com/MariRazno/BERT_NER_DIA',
    author='MariiaRazno',
    author_email='mari.razno@gmail.com',
    install_requires=get_requirements(),
    zip_safe=True,
    classifiers=[
        'Topic :: Text Processing :: NER',
        'Programming Language :: Python :: 3.11',
    ],
    keywords='NER BERT ICD-10'
)