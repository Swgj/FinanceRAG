"""
As the extracted markdown is not well formatted,
we need to make sure the company name is the only head one in the markdown file.
"""

import os
import re
from tqdm import tqdm

def clean_markdown(file_path, output_path):
    # delete heaf and foot lines

    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    cleaned_lines = []

    for i, line in enumerate(lines):
        # remove page split line
        if re.match(r'^-+$', line.strip()):
            continue
        # remove tail, single number line before split line
        if i < len(lines) - 3 and re.match(r'^(\d+(-\d+)*|\d+( \d+)+)$', line.strip()) and re.match(r'^-+$', lines[i+3].strip()):
            continue
        # remove head, contains '公司' or '招股意向书' afrer split line
        if i > 2 and re.match(r'^-+$', lines[i-2].strip()) and re.search(r'(公司|招股意向书)', line):
            continue

        cleaned_lines.append(line)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.writelines(cleaned_lines)

def remove_catalogue(file_path, output_path):
    """
    从 Markdown 文件中删除目录内容。

    Args:
        file_path (str): 输入 Markdown 文件路径。
        output_path (str): 输出清理后的 Markdown 文件路径。
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # 正则表达式匹配目录区域
    # 目录以 `# 目 录` 开始，以下一个标题（如 `# 第一章` 或 `# 释 义`）结束
    pattern = r"(#{1,6}\s*目\s*录[\s\S]*?)(?=#{1,6}\s+\S)"
    
    # 使用正则替换删除匹配的目录区域
    cleaned_content = re.sub(pattern, "", content, flags=re.MULTILINE)

    # 将清理后的内容写入输出文件
    with open(output_path, 'w', encoding='utf-8') as output_file:
        output_file.write(cleaned_content)

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
        
        # remove head and foot lines
        clean_markdown(output_file_path, output_file_path)
        
        # remove catalogue
        remove_catalogue(output_file_path, output_file_path)

        print(f"Processed and saved {output_file_path}")




