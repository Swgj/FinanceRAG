import yaml
import os
import argparse

class Config:
    def __init__(self, path):
        self.path = path
        self.config = self._load_config()
    
    def _load_config(self):
        with open(self.path, 'r') as file:
            config = yaml.safe_load(file)
        return config
    
    def get(self, key):
        value = self.config.get(key)
        if value is None:
            raise KeyError(f"Key {' -> '.join(key)} not found in configuration.")
        
        return value

    def get_path(self, base, key):
        base_path = self.get(base).get('path')
        sub_path = self.get(base).get(key)

        return os.path.join(base_path, sub_path)

# 使用 argparse 解析命令行参数
parser = argparse.ArgumentParser(description='Configuration file parser')
parser.add_argument('--config', type=str, default=os.path.join(os.path.dirname(__file__), 'config.yaml'), help='Path to the configuration file')
args, unknown = parser.parse_known_args() # use the unkonwn parameter to avoid error when running in Jupyter notebook

# 创建全局配置实例
config = Config(args.config)

# 示例用法
if __name__ == "__main__":
    print(config.get_path('dataset', 'pdf'))
    print(config.get_path('lora', 'sql'))