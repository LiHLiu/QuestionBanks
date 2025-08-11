from dashscope import Generation
import RAG_vector_store, data
import os

# 调用通义千问模型API 
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


# 根据答案生成干扰选项
def generate_options(answer, nums=3, model="qwen-turbo", api_key=os.environ.get("DASHSCOPE_API_KEY")):
    system_prompt = f"""
    你是一个智能选项生成助手，任务是根据用户提供的问题（Q）和正确答案（A），生成多个干扰选项。要求如下：
    1. 干扰选项必须与正确答案相关，但不能完全相同。
    2. 每个干扰选项应具有一定的迷惑性，避免过于明显或容易识别。
    3. 至少生成{nums}个干扰选项，确保多样性和复杂性。
    4. 输出格式为每个选项各一行，一共生成{nums}行的结果。
    5. 不需要包含问题（Q）的内容，只需专注于生成干扰选项。
    """

    result = call_qwen(user_prompt=answer, system_prompt=system_prompt, model=model, api_key=api_key)
    return result


# 根据答案关键词挖空生成填空题
def generate_fill_in_the_blank(QA, model="qwen-turbo", api_key=os.environ.get("DASHSCOPE_API_KEY")):
    system_prompt = f"""
    你是一个智能填空题生成助手，任务是根据用户提供的问题（Q）和答案（A）自动提取关键词并挖空，生成填空题。要求如下：
    1. 根据答案提取其中的关键词挖空，并生成填空题。
    2. 填空题应清晰明了，便于理解。
    3. 输出格式为填空题的完整句子，其中关键词被挖空，以括号的形式空出来。
    4. 关键词可以不止1个，但尽量不要超过3个，具体数量根据所提取的关键词数量决定的。
    ***重要： 生成后的结果括号内部的关键词绝对不能显示，否则就是严重的答案泄漏。***
    生成示例：阿里云的AI技术部署在（）奥运场馆中，以实现即时生成的（）高保真回放。
    """
    
    result = call_qwen(user_prompt=QA, system_prompt=system_prompt, model=model, api_key=api_key)
    return result