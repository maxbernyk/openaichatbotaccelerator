import os
from langchain.docstore.document import Document
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.vectorstores import Chroma

class Vectorstore:
    def __init__(self, path):
        self.path = path
        self.embeddings = OpenAIEmbeddings()
        self.text_splitter = CharacterTextSplitter(chunk_size=4000, chunk_overlap=0)
        self.vectordb = Chroma(
            persist_directory=path,
            embedding_function=self.embeddings
        )

    def add(self, filename, doc_content):
        doc = Document(page_content=doc_content, metadata={'filename': filename})
        texts = self.text_splitter.split_documents([doc])
        id = self.vectordb.add_documents(documents=texts)
        return 'ok'

    def delete(self, doc_ids):
        self.vectordb.delete(ids=[doc_ids])
        return 'ok'

    def list(self, max_length=200):
        docs = []
        data = self.vectordb.get()
        for id, meta, doc in zip(data['ids'], data['metadatas'], data['documents']):
            content = (doc[:max_length] + '...') if len(doc) > max_length else doc
            docs.append({'id': id, 'filename': meta['filename'], 'content': content})
        return docs

    def getOne(self, id):
        data = self.vectordb.get(ids=[id])
        if len(data['ids']) == 0:
            return {}
        else:
            return {'id': data['ids'][0], 'filename': data['metadatas'][0]['filename'], 'content': data['documents'][0]}
