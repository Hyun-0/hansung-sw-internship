from llama_index.core import SimpleDirectoryReader
from config import DATASET

class DataSetter:
    def __init__(self) :
        self.dataset_dir = DATASET

    def load_dataset(self) :
        print("Loading dataset ...")
        return SimpleDirectoryReader(self.dataset_dir).load_data()

 