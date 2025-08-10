from dashscope import Generation
import RAG_vector_store, data
import os

# 调用通义千问模型API sgtql
def call_qwen(user_prompt="请介绍一下通义千问模型", system_prompt = None, model="qwen-turbo", api_key=os.environ.get("DASHSCOPE_API_KEY")):
    
    messages = []

    if system_prompt:
        messages.append({
            "role": "system", 
            "content": system_prompt
        })

    messages.append({
        "role": "user",
        "content": user_prompt
    })
    
    try:
        response = Generation.call(
            model=model,  
            messages=messages,   
            api_key=api_key  
        )

        # 解析响应（output是字典，用["text"]获取内容）
        if response.status_code == 200:
            return response.output["text"]
        else:
            return f"请求失败，状态码: {response.status_code}，原因: {response.message}"
    except Exception as e:
        return f"调用出错: {str(e)}"


# 针对单次提问产生QA语句
def generate_QA_once(content, model="qwen-turbo", api_key=os.environ.get("DASHSCOPE_API_KEY")):

    system_prompt = """
    请你担任题库生成助手，核心任务是根据用户输入的段落内容，自动生成指定数量1个的问题及对应的答案，具体要求如下：
    问题生成准则：
    需紧扣段落核心信息，涵盖段落中的关键概念、事实、逻辑关系等，避免生成与段落无关的问题。
    问题类型可多样化，包括但不限于事实询问（如 “什么是...？”“... 发生在何时？”）、细节理解（如 “... 的原因是什么？”“文中提到的... 具体指什么？”）、逻辑推理（如 “根据段落，... 会导致什么结果？”“为什么说...？”）等。
    问题表述需清晰、准确、无歧义，符合常规语言习惯，避免使用过于复杂的句式或生僻词汇。
    每个问题必须是单一短句的形式，仅包含一个独立问题，不得包含多个隐含的小问题（例如避免出现 “XX 的营收是多少，增长率为多少？” 这类包含两个问题的表述）。
    答案生成准则：
    答案必须严格依据用户提供的段落原文内容，不得添加段落外的信息或个人主观解读。
    答案需简洁明了，直接回应问题，确保与问题的对应性，避免答非所问。
    若段落中对某一内容有多种表述，优先选择最精准、最核心的表述作为答案。
    输出格式要求：
    每个问题以 “Q：” 开头，紧随问题内容，之后换行。
    每个问题对应的答案以 “A：” 开头，紧随答案内容，之后换两行。
    按上述格式依次呈现所有生成的 n 个问题及答案，确保条理清晰，便于用户查看和使用。
    请严格遵循以上要求，当用户输入段落并指定 n 的值后，为其生成符合标准的 n 个问题及答案。
    """

    result = call_qwen(user_prompt = content, system_prompt=system_prompt, model=model, api_key=api_key)
    return result


# 多次循环实现QA语句生成
def generate_QA(keyword="阿里", nums=5, model="qwen-turbo", api_key=os.environ.get("DASHSCOPE_API_KEY")):

    contents_to_generate_QA = RAG_vector_store.search_similar_documents(keyword, k=nums)

    results = []

    for i, doc in enumerate(contents_to_generate_QA):
        result = generate_QA_once(doc.page_content, model=model, api_key=api_key)
        results.append(result)

    # 处理生成的QA语句
    processed_results = data.process_generated_QA(results)
    
    return processed_results

