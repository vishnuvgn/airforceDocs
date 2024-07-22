from dotenv import load_dotenv
from llama_index.core import VectorStoreIndex
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding

from llama_parse import LlamaParse
from llama_index.core import SimpleDirectoryReader
# from llama_index.core.schema import TextNode
import os, json

load_dotenv()

parser = LlamaParse(result_type='markdown', gpt4o_mode=True, gpt4o_key=os.getenv("OPENAI_API_KEY"))
file_extractor = {".pdf": parser}

llm = OpenAI(model='gpt-4o')
embed_model = OpenAIEmbedding(model="text-embedding-3-large")

# def parse(path, output_path):
#     parser = LlamaParse(result_type='markdown', gpt4o_mode=True, gpt4o_key=os.getenv("OPENAI_API_KEY"))
#     json_objs = parser.get_json_result(path)
    
#     with open(output_path, 'w') as f:
#         json.dump(json_objs, f)

#     return json_objs

# def get_text_nodes(json_list: list[dict]):
#     text_nodes = []
#     for idx, page in enumerate(json_list):
#         text_node = TextNode(text=page["md"], metadata={"page": page["page"]})
#         text_nodes.append(text_node)
#     return text_nodes


def process_json(json_path):
    # Placeholder function to process JSON files
    # print(f"Processing JSON file: {json_path}")
    with open(json_path, 'r') as f:
        data = json.load(f)
    return data


for docdir in os.listdir('docs'):
    print(f'docdir: {docdir}')
    docpath = os.path.join('docs', docdir)
    pdf_file = None
    json_file = None
    for file_name in os.listdir(docpath):
        if file_name.endswith('.pdf'):
            pdf_file = os.path.join(docpath, file_name)
        elif file_name.endswith('.json'):
            json_file = os.path.join(docpath, file_name)
    
    if pdf_file and json_file:
        json_data = process_json(json_file)
        # print(json_data["year"])
        if int(json_data["year"]) >= 2010:
            print(pdf_file)
            docs = SimpleDirectoryReader(input_files=[pdf_file], file_extractor=file_extractor).load_data()
            vector_index = VectorStoreIndex.from_documents(docs, embed_model=embed_model)
            query_engine = vector_index.as_query_engine(llm=llm, similarity_top_k=20)
            response = query_engine.query(open('qnaPrompt.txt').read())

            with open(docpath + '/qnas.txt', 'w') as f:
                f.write(str(response))