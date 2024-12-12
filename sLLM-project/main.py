from llama_index.core.postprocessor import SentenceTransformerRerank

import time

from hugging import HuggingFaceNotebookLogin
from dataset  import DataSetter
from embedding_setter import EmbedSettings
from load_llm import LLMLoader
from prompt_template import PromptTemplates
from db import Db
from config import ENCODER_MODEL

# function calling
from llama_index.core.agent import FunctionCallingAgent
from tools import Tools
from llama_index.core.tools import QueryEngineTool

print("hugging Login Start...")
HuggingFaceNotebookLogin().login()

print("load PDF Data Start...")
documents = DataSetter().load_dataset()

promptTP = PromptTemplates()
system_prompt = promptTP.get_system_prompt()
query_wrapper_prompt = promptTP.get_query_wrapper_prompt()

print("Setting Embed Model settings...")
settting = EmbedSettings().set_and_get_liama_settings()

print("Setting LLM settings...")
settting.llm = LLMLoader(system_prompt, query_wrapper_prompt).load_llm()
settting.llm.metadata.is_function_calling_model = True

print("Setting db Index settings...")
dbIndex = Db(documents).get_index()

print("Setting SentenceTransformerRerank settings...")
rerank = SentenceTransformerRerank(model=ENCODER_MODEL, top_n=3)

print("Setting Query Engine settings...")
query_engine = dbIndex.as_query_engine(similarity_top_k=10, node_postprocessors=[rerank])

import os
from tools import Tools
from llama_index.agent.openai import OpenAIAgent
from llama_index.llms.openai import OpenAI
from llama_index.core.tools import QueryEngineTool

rag_tool = QueryEngineTool.from_defaults(query_engine=query_engine, description="Rag from granite")

tools = Tools().get_tools()
tools.append(rag_tool)

os.environ["OPENAI_API_KEY"] = "OPENAI_API_KEY"
llm = OpenAI(api_key=os.environ["OPENAI_API_KEY"], model_name="gpt-4")

agent = OpenAIAgent.from_tools(Tools().get_tools(), llm = llm, verbose=True)
