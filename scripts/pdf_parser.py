import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.utils.pdf_parser import parse_pdfs_md
from src.config import config


if __name__ == "__main__":
    # Convert the PDF to markdown
    pdf_path = config.get_path('dataset', 'pdf')
    md_path = config.get_path('dataset', 'markdown')
    
    # Note
    # do not know reason why it is not working with multiple workers,
    # plz set max_workers=1
    parse_pdfs_md(pdf_path, md_path,1) 
    