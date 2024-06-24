from dotenv import load_dotenv
from llama_index.core import VectorStoreIndex
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding

from llama_parse import LlamaParse
from llama_index.core.schema import TextNode
import os, json

load_dotenv()

llm = OpenAI(model='gpt-4o')
embed_model = OpenAIEmbedding(model="text-embedding-3-large")

def parse(path):
    parser = LlamaParse(result_type='markdown', gpt4o_mode=True, gpt4o_key=os.getenv("OPENAI_API_KEY"))
    json_objs = parser.get_json_result(path)
    
    with open('output.json', 'w') as f:
        json.dump(json_objs, f)

    return json_objs

def get_text_nodes(json_list: list[dict]):
    text_nodes = []
    for idx, page in enumerate(json_list):
        text_node = TextNode(text=page["md"], metadata={"page": page["page"]})
        text_nodes.append(text_node)
    return text_nodes



# json_objs = parse('docs/3/Admissions, curriculum, and diversity of thought at the military service academies : hearing before .pdf') ## <-- PATH
json_objs = json.load(open('output.json', 'r'))

nodes = get_text_nodes(json_objs[0]["pages"])

vector_index = VectorStoreIndex(nodes, embed_model=embed_model)
# print(vector_index.__sizeof__())
query_engine = vector_index.as_query_engine(llm=llm, similarity_top_k=20)

response = query_engine.query(open('prompt.txt').read())

print(response)