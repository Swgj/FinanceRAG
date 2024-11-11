from sentence_transformers import SentenceTransformer
from src.config import config
from bs4 import BeautifulSoup
import os
import markdown


def generate_embeddings(texts):
    model_name = config.get_path('models','embedding_model')
    model = SentenceTransformer(model_name)
    embeddings = model.encode(texts, convert_to_tensor=True)
    return embeddings


def load_texts(md_dir):
    texts = []
    doc_ids = []
    for file_name in os.listdir(md_dir):
        if file_name.endswith('.md'):
            md_path = os.path.join(md_dir, file_name)
            with open(md_path, 'r', encoding='utf-8') as f:
                md_content = f.read()
                # Parse markdown
                html_content = markdown.markdown(md_content)
                soup = BeautifulSoup(html_content, 'html.parser')
                text = soup.get_text()
                # parse tables
                tables = soup.find_all('table')
                for table in tables:
                    for row in table.find_all('tr'):
                        cells = row.find_all(['td', 'th'])
                        row_text = ' | '.join(cell.get_text() for cell in cells)
                        text += '\n' + row_text
                
                texts.append(text)
                doc_ids.append(file_name)
    
    return texts, doc_ids