 # Research Paper Filename Proposer
These helper scripts suport you in renaming your research paper pdf collection. The provided scripts extract the beginning of a paper as raw text and then utilize ChatGPT to find the last name of the first author and the paper title. Both are then used to suggest a new filename.

 ## rename_helper.py

 This scripts combines the filename_proposer.py with a first page preview and a GUI that supports you in renaming your pdf files.
 
 ## filename_proposer.py

 This script helps you to generate proposed filenames for research papers using the scheme AUTHOR-TITLE. It utilizes the `pdfplumber` library to extract text from the first page of a PDF and the OpenAI GPT model to identify the title and the last name of the first author.

 ### Dependencies

 - pdfplumber
 - openai
 - os
 - sys
 - argparse
 - re
 - json

 ### Installation

 1. Clone this repository.
 2. Install the required libraries by running `pip install pdfplumber openai`

 ### Usage

 There are two ways to use this script: providing a single PDF file or providing a folder containing multiple PDF files. The script will then suggest a filename for each PDF file.

 #### Single PDF File

 ```bash
 python filename_proposer.py --pdf_file /path/to/pdf/file.pdf --suggest_filename
 ```

 #### Folder with PDF Files

 ```bash
 python filename_proposer.py --folder /path/to/pdf/folder/ --suggest_filename
 ```

 #### Output JSON

 If you prefer to get the output in JSON format, you can use the `--output_json` flag:

 ```bash
 python filename_proposer.py --pdf_file /path/to/pdf/file.pdf --output_json
 ```

 ### Example

 For example, if you provide the script with a PDF file containing the research paper "The Effectiveness of Deep Learning" by John Doe, the output might look like this:

 ```plaintext
 /path/to/pdf/file.pdf
 ---> Doe-The_Effectiveness_of_Deep_Learning.pdf
 ```
