from huggingface_hub import login
from config import HUGGING_TOKEN

class HuggingFaceNotebookLogin:
    def __init__(self ):
        self.token = HUGGING_TOKEN

    def login(self):
        print("Logging in...")
        login(self.token)