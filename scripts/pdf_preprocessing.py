import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.config import config
from src.utils.data_preprocessing import preprocess_markdown


if __name__ == '__main__':
    print('Data Preprocessing...')
    
    
    preprocess_markdown(config.get_path('dataset', 'markdown'), config.get_path('dataset', 'preprocessed_md'))
    print('Data Preprocessing Done!')