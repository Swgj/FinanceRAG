import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.config import config
from src.utils.data_preprocessing import preprocess_markdown


if __name__ == '__main__':
    print('Data Preprocessing...')
    
    # preprocess_markdown(
    #     os.path.join(config.get_path('dataset', 'markdown'),'d1a73ca4a204ca3f98024bca8ce0652f5e1c1a94'),
    #     config.get_path('dataset', 'preprocessed_md'))
    
    preprocess_markdown(config.get_path('dataset', 'markdown'), config.get_path('dataset', 'preprocessed_md'))
    print('Data Preprocessing Done!')