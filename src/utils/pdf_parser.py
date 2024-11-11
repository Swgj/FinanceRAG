from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed
import os
import pymupdf4llm
import pathlib
import shutil

def parse_pdfs_md(pdf_dir, output_dirs, max_workers=4):
    if not os.path.exists(output_dirs):
        os.makedirs(output_dirs)
    
    pdf_files = [pdf for pdf in os.listdir(pdf_dir) if (pdf.lower()).endswith(".pdf")]

    # exclude files that have already been processed
    existing_dirs = os.listdir(output_dirs)
    md_files = [md+'.PDF' for md in existing_dirs]
    pdf_files = [pdf for pdf in pdf_files if pdf not in md_files]
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = []
        for pdf in pdf_files:
            pdf_path = os.path.join(pdf_dir, pdf)
            output_dir = os.path.join(output_dirs, pdf.split('.')[0])
            futures.append(executor.submit(pdf2md, pdf_path, output_dir))
        
        for future in tqdm(as_completed(futures), total=len(futures), desc="Preprocessing PDFs"):
            try:
                future.result()
            except Exception as e:
                print(f"Error processing PDF: {str(e)}")


def pdf2md(pdf_path, output_dir):
    try:
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
        
        print(f"Processed {pdf_path}")
    except Exception as e:
        print(f"Error processing {pdf_path}: {str(e)}")

