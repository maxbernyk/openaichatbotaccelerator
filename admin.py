import os
from langchain.docstore.document import Document
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.vectorstores import Chroma

class Vectorstore:
    def __init__(self, path, collection_name='main'):
        self.path = path
        self.embeddings = OpenAIEmbeddings()
        self.text_splitter = CharacterTextSplitter(chunk_size=4000, chunk_overlap=0)
        self.vectordb = Chroma(
            persist_directory=path,
            embedding_function=self.embeddings
        )

    def add(self, doc_path):
        filename = os.path.basename(doc_path)
        with open(doc_path, 'rt') as f:
            doc = Document(page_content=f.read(), metadata={'filename': filename})
        texts = self.text_splitter.split_documents([doc])
        id = self.vectordb.add_documents(documents=texts)
        return 'ok'

    def delete(self, doc_id):
        self.vectordb.delete(ids=[doc_id])
        return 'ok'

    def list(self):
        docs = []
        data = self.vectordb.get()
        for id, meta, doc in zip(data['ids'], data['metadatas'], data['documents']):
            docs.append({'id': id, 'filename': meta['filename'], 'content': doc})
        return docs