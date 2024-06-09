import os, time
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.chains import ConversationalRetrievalChain
from langchain_core.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
)
from langchain.docstore.document import Document
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain.memory import ConversationBufferMemory


def load_db(input_path):
    embeddings = OpenAIEmbeddings()
    return Chroma(
        persist_directory=input_path,
        embedding_function=embeddings
    )


def get_llm_chain(input_path):
    db = load_db(input_path)
    llm = ChatOpenAI(temperature=0, model_name='gpt-3.5-turbo')
    prompt = ChatPromptTemplate.from_messages(
        [
            SystemMessagePromptTemplate.from_template(
                'Provide answers based only on the context given.{context}'
            ),
            HumanMessagePromptTemplate.from_template('{question}'),
        ]
    )
    memory = ConversationBufferMemory(
        llm=llm, memory_key='chat_history', output_key='answer', return_messages=True
    )
    chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        memory=memory,
        retriever=db.as_retriever(
            search_type='similarity',
            search_kwargs={
                'k': len(db) if len(db) < 10 else 10,
            },
        ),
        return_source_documents=True,
        chain_type='stuff',
        combine_docs_chain_kwargs={'prompt': prompt},
    )
    return chain


class Chat:
    def __init__(self, input_path):
        if 'OPENAI_API_KEY' not in os.environ:
            print('OPENAI_API_KEY env variable is not set - exiting.')
            exit(0)
        self.llm_chain = get_llm_chain(input_path)

    def ask(self, q):
        result = self.llm_chain.invoke({'question': q})
        return result['answer']
