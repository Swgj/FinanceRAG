import os
import pymupdf4llm
import pathlib
import shutil

def parse_pdfs_md(pdf_dir, output_dirs):
    if not os.path.exists(output_dirs):
        os.makedirs(output_dirs)
    
    for pdf in os.listdir(pdf_dir):
        if pdf.endswith(".pdf"):
            pdf_path = os.path.join(pdf_dir, pdf)
            output_dir = os.path.join(output_dirs, pdf.split('.')[0])
            pdf2md(pdf_path, output_dir)


def pdf2md(pdf_path, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # convert pdf to markdown
    md_text = pymupdf4llm.to_markdown(pdf_path, write_images=True)

    # save markdown to file
    md_name = os.path.basename(pdf_path).split('.')[0]+'.md'
    output_path = os.path.join(output_dir, md_name)
    pathlib.Path(output_path).write_bytes(md_text.encode('utf-8'))

    # move images to the output directory
    for img in os.listdir("."):
        if img.startswith(md_name.replace(".md", "")) and img.endswith(".png"):
            shutil.move(img, os.path.join(output_dir, img))

