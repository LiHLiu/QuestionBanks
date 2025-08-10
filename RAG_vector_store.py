from getpass import getpass
from dashscope import Generation
from langchain.document_loaders import PyPDFLoader, TextLoader
from langchain.embeddings import DashScopeEmbeddings
from langchain.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os

# 创建RAG向量数据库的函数
def create_vector_store(file_path):

    if file_path.endswith('.pdf'):
        loader = PyPDFLoader(file_path)
    elif file_path.endswith('.txt'):
        loader = TextLoader(file_path, encoding='utf-8')
    else:
        raise ValueError(f"不支持的文件类型: {file_path}")

    pages = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
    )
    docs = text_splitter.split_documents(pages)

    # 创建通义千问embeddings
    embeddings = DashScopeEmbeddings(
        model="text-embedding-v1"
    )

    vector_store = FAISS.from_documents(docs, embeddings)

    vector_store.save_local("faiss_index")

    print(f"成功创建RAG向量数据库，共处理 {len(docs)} 个文档片段")



# 添加新文档到现有向量数据库的函数
def add_new_documents_to_vector_store(file_path):
    embeddings = DashScopeEmbeddings(model="text-embedding-v1")
    vector_store = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)

    if file_path.endswith('.pdf'):
        loader = PyPDFLoader(file_path)
    elif file_path.endswith('.txt'):
        loader = TextLoader(file_path, encoding='utf-8')
    else:
        raise ValueError(f"不支持的文件类型: {file_path}")
    
    documents = loader.load()
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
    )
    docs = text_splitter.split_documents(documents)

    vector_store.add_documents(docs)

    vector_store.save_local("faiss_index")

    print(f"成功添加 {len(docs)} 个新文档片段")



# 根据查询词搜索相似文档的函数
def search_similar_documents(query, k=4):
    """
    根据查询词搜索相似文档
    query: 查询关键词或句子
    k: 返回最相似的k个结果
    """
    embeddings = DashScopeEmbeddings(model="text-embedding-v1")
    vector_store = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)

    similar_docs = vector_store.similarity_search(query, k=k)
    
    print(f"查询: {query}")
    print(f"找到 {len(similar_docs)} 个相关文档:\n")
    
    for i, doc in enumerate(similar_docs):
        print(f"--- 文档 {i+1} ---")
        print(f"内容: {doc.page_content[:200]}...")
        print(f"来源: {doc.metadata.get('source', 'Unknown')}")
        print(f"页码: {doc.metadata.get('page', 'N/A')}")
        print("-" * 50)
    
    return similar_docs


if __name__ == "__main__":

    # 安全获取API Key（输入时不显示明文）
    # api_key = getpass("请输入阿里云百炼API Key: ")
    # os.environ["DASHSCOPE_API_KEY"] = api_key
    # Generation.api_key = api_key

    # 创建向量数据库
    create_vector_store("./data/sample.pdf")
    
    # 添加新文档
    add_new_documents_to_vector_store("./data/alibaba-2.txt")
    
    # 测试查询
    results = search_similar_documents("延长学制", k=5)
    results2 = search_similar_documents("阿里", k=5)