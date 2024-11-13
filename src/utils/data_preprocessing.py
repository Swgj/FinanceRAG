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
    # 使用正则表达式将公司名称提取出来，并添加到第一行 作为h1
    # 并将其他的h1改为h2
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    file_paths = []
    for root, _, files_all in os.walk(md_dir):
        files =[f for f in files_all if f.endswith('.md')]
        for single_file in files:
            file_paths.append(os.path.join(root, single_file))

    com_name_pa = re.compile(r'#\s+.*有限公司')
    header_pa = re.compile(r'^(#+)\s+(.*)',re.MULTILINE)
    bad_md = []
    for file_path in tqdm(file_paths, desc="Preprocessing markdown files"):
        with open(file_path, 'r', encoding='utf-8') as f:
            md_content = f.read()
        
        # 进行匹配
        conpany_name_match = com_name_pa.search(md_content)
        if conpany_name_match:
            company_name = conpany_name_match.group(0)
            # 提取纯公司名称文本（去除 '# '）
            company_name_text = company_name.lstrip('#').strip()
            # 将公司名称添加到第一行
            md_content = f"# {company_name_text}" + '\n' + md_content
        else:
            print(f"Error: {file_path} does not contain the company name")
            bad_md.append(file_path)
            continue

        # 将其他的h1改为h2
        def replace_header(match):
            hashes, title = match.groups()
            if hashes == '#' and title.strip() != company_name_text:
                return f"## {title}"
            return match.group(0)
        
        cleaned_md_content = header_pa.sub(replace_header, md_content)


        # save the cleaned markdown
        output_file_path = os.path.join(output_dir, file_path.split('/')[-1])
        with open(output_file_path, 'w', encoding='utf-8') as f:
            f.write(cleaned_md_content)
            # f.write(modified_content)
        print(f"Processed and saved {output_file_path}")

    

def bad_preprocess_markdown(md_dir, output_dir):
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

