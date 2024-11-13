"""
As the extracted markdown is not well formatted,
we need to make sure the company name is the only head one in the markdown file.
"""

import os
import markdown
import re
from bs4 import BeautifulSoup
from tqdm import tqdm
from markdownify import markdownify as md



def preprocess_markdown(md_dir, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    bad_md = [] # store the bad markdown files
    check_md = []

    for root, _, files in os.walk(md_dir):
        files = [f for f in files if f.endswith('.md')]

        for id, file in tqdm(enumerate(files),total=len(files), desc="Preprocessing markdown files"):
            file_path = os.path.join(root, file)

            with open(file_path, 'r', encoding='utf-8') as f:
                md_content = f.read()
            
            # parse markdown
            html_content = markdown.markdown(md_content, extensions=['tables'])
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # find all headers
            headers = soup.find_all(re.compile(r'h\d'))
            # make sure the company name is the only header one
            company_name_header = None
            for header in headers:
                if header.name == 'h1':
                    if header.text.endswith('有限公司'):
                        company_name_header = header
                    else:
                        header.name = 'h2'
            
            if company_name_header is None:
                print(f"Warning: {file} does not contain the company name in h1")

                # try to find company name in other headers
                for header in headers:
                    if header.text.endswith('有限公司'):
                        company_name_header = header
                        break
                
                try:
                    # add the company name to the first line
                    company_name = company_name_header.text
                    company_name_header.extract()
                    new_header = soup.new_tag('h1')
                    new_header.string = company_name
                    soup.insert(0, new_header) 
                    check_md.append(file)
                except:
                    print(f"Error: {file} does not contain the company name in any headers")
                    bad_md.append(file)
                    continue
                
            # turn the soup back to markdown
            cleaned_md_content = md(soup.prettify())
            
            # save the cleaned markdown
            output_file_path = os.path.join(output_dir, file)
            # output_file_path = os.path.join(output_dir, file.replace('.md', '.html'))
            with open(output_file_path, 'w', encoding='utf-8') as f:
                f.write(cleaned_md_content)
                        
            # print(f"Processed and saved {output_file_path}")
    
    print(f"Found {len(bad_md)} bad markdown files")
    for bad in bad_md:
        print(bad)
    print(f"please check {len(check_md)} markdown files")
    for check in check_md:
        print(check)


