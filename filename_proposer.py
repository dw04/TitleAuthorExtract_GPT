
import pdfplumber
import openai
import os
import sys
import argparse
import re
import json
from find_publication_year import find_publication_year

# Set up the OpenAI API client
openai.api_key = os.getenv("OPENAI_API_KEY") or "your_api_key_here"

CHATGPT_MODEL="text-davinci-003" # works with openai.Completion

def query_chatgpt(prompt, model, max_tokens=50, temperature=0.5):
    response = openai.Completion.create(
        engine=model,
        prompt=prompt,
        max_tokens=max_tokens,
        temperature=temperature,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    return response.choices[0].text.strip()

def extract_page_text(pdf_path,page_number,character_limit=400,verbose=True):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        first_page = pdf.pages[page_number]
        text = first_page.extract_text()
        #print(text)
    if len(text) < character_limit:
        if verbose:
            print("Extracted pdf text too small!")
        return None
    else:
        return text[0:character_limit]

def is_valid_json_string(response):
    try:
        json_obj = json.loads(response)
        if isinstance(json_obj, dict) and 'title' in json_obj and 'author' in json_obj:
            return True
    except json.JSONDecodeError:
        pass
    return False

def json_response_to_filename_proposal(json_string):
    json_obj = json.loads(json_string)

    author = json_obj['author']
    title = json_obj['title']
    year = find_publication_year(title,author)
    if year is None:
        year = 0000

    # Use regex to remove all special characters except whitespaces
    clean_title = re.sub("[^a-zA-Z0-9\\s]", "", title)
    # Use regex to remove all subsequent whitespaces
    clean_title =  re.sub("\\s+", " ", clean_title)

    proposal = str(year)+'-'+author+'-'+clean_title.replace(" ","_")
    # Use regex to remove all special characters except "-" and "_"
    clean_proposal = re.sub("[^a-zA-Z0-9-_]", "", proposal)
    return clean_proposal+'.pdf'


def get_proposal(pdf_path,output_json=False,verbose=True):
    first_page_text = extract_page_text(pdf_path,0)
    if first_page_text:
        prompt = 'I want you to act as script that can only output json. I will provide the beginning of a reasearch paper as text and you will reply with a json format that contains the key "title" containing the title of the paper and the key "author" containing the last name of the first author, and nothing else. do not write explanations. My text is "'+first_page_text+'"'
        response = query_chatgpt(prompt,CHATGPT_MODEL)
        if is_valid_json_string(response):
            if output_json:
                return response
            else:
                filename_proposal = json_response_to_filename_proposal(response)
                return filename_proposal
        else:
            print("ChatGPT response not valid! Response was: \n \n",response,"\n \n")
            print("Used pdf text:\n",first_page_text)
    return None

def is_valid_filename(filename):
    # Check if filename is in the format Year-Author-Title.pdf
    pattern = r"^\d{4}-[A-Za-z]+-([A-Za-z0-9]+_)*[A-Za-z0-9]+.pdf$"
    return bool(re.match(pattern, filename))
    
def iterate_folder(pdf_folder,output_json=False):
    for pdf_file in os.listdir(pdf_folder):
        if pdf_file.lower().endswith(".pdf") and not is_valid_filename(pdf_file):
            print("Processing: ", pdf_file)
            pdf_path = os.path.join(pdf_folder, pdf_file)
            filename_proposal = get_proposal(pdf_path,output_json)
            print_proposal(pdf_path,filename_proposal)
        else:
            print("Already valid:",pdf_file)

def print_proposal(filename,proposal):
    print(filename)
    if proposal is None:
        print("FAILED")
    else:
        print("---> " + proposal)
    print("\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="A script to propose a filename for research papers with the scheme YEAR-AUTHOR-TITLE.")
    
    # Create a mutually exclusive group
    input_group = parser.add_mutually_exclusive_group(required=True)

    input_group.add_argument("--pdf_file", type=str, help="Option A: Provide a path to a pdf file.")
    input_group.add_argument("--folder", type=str, help="Option B: Provide a folder path that contains pdf files.")

    output_group = parser.add_mutually_exclusive_group(required=True) 
    output_group.add_argument("--suggest_filename",help="Suggest filename",default=True,action="store_true")
    output_group.add_argument("--output_json",help="output json string ",default=False,action="store_true")

    args = parser.parse_args()

    if args.pdf_file:      
        proposal = get_proposal(args.pdf_file,args.output_json)
        print_proposal(args.pdf_file,proposal)
    elif args.folder:
        iterate_folder(args.folder,args.output_json)
        