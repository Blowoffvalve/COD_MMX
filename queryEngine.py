
from llama_index.core import (
    SimpleDirectoryReader,
    VectorStoreIndex,
    StorageContext,
    load_index_from_storage,
)
from llama_index.core.tools import QueryEngineTool, ToolMetadata

from pymilvus import connections
from llama_index.vector_stores.milvus import MilvusVectorStore
from milvus import default_server

default_server.start()

news_docs = SimpleDirectoryReader(
        input_files=["./data/News.pdf"]
    ).load_data()

# build index
vector_store_news = MilvusVectorStore(dim=1536, collection_name="news", overwrite=True)
storage_context_news = StorageContext.from_defaults(vector_store=vector_store_news)
news_index = VectorStoreIndex.from_documents(news_docs, storage_context=storage_context_news)


# persist index
news_index.storage_context.persist(persist_dir="./storage/news")

news_engine = news_index.as_query_engine(similarity_top_k=3)
#news_engine = news_index.as_query_engine()

queryEngineName = "news"
queryEngineDescription =  "Provides information about Nigerian news"

query_engine_tools = [
    QueryEngineTool(
        query_engine=news_engine,
        metadata=ToolMetadata(
            name=queryEngineName,
            description=queryEngineDescription,
        ),
    )
]

from llama_index.core.agent import ReActAgent
from llama_index.llms.openai import OpenAI

llm = OpenAI(model="gpt-3.5-turbo-0613")

agent = ReActAgent.from_tools(
    query_engine_tools,
    llm=llm,
    verbose=True,
    # context=context
)

question = "What was the news?"
response = agent.chat(question)
print(str(response))