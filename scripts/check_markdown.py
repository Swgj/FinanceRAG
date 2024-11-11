# check whether each markdown file is well-formed
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import re
from src.config import config

def check_md_files(directory):
    # get all markdown files
    md_sub_dir = [d for d in os.listdir(directory) if os.path.isdir(os.path.join(directory, d))] # get all subdirectories
    md_files = []
    for sub_dir in md_sub_dir:
        md_files += [os.path.join(directory, sub_dir, f) for f in os.listdir(os.path.join(directory, sub_dir)) if f.endswith('.md')]
    
    print(f"Checking {len(md_files)} markdown files...")

    # check each markdown file
    bad_md = []

    for md_file in md_files:
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()
            # check whether contain '# xx有限公司'
            search = re.search(r'#\s+.*有限公司', content)
            if not search:
                print(f"{md_file} does not contain '# xx有限公司'")
                bad_md.append(md_file)
            else:
                print(f"{md_file} contains {search}")
    return bad_md


if __name__ == "__main__":
    directory = config.get_path('dataset', 'markdown')
    bad_md = check_md_files(directory)
    if bad_md:
        print(f"Found {len(bad_md)} bad markdown files")
        for bad in bad_md:
            bad = bad.split('/')[-1]
            print(bad)
    else:
        print("All markdown files are well-formed")