from dashscope import Generation
from typing import List, Dict
import RAG_vector_store
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


# 处理生成的QA语句，实现数据格式化
def process_generated_QA(generated_QA_list):
    qa_objects: List[Dict[str, str]] = []
    
    input_data = generated_QA_list if isinstance(generated_QA_list, list) else [generated_QA_list]
    
    for item in input_data:
        if isinstance(item, str):
            content = item.strip()
            if not content:
                continue 

            content = content.replace("\n\n", "\n").replace("\n  \n", "\n")
            
            # 按行分割，过滤空行
            lines = [line.strip() for line in content.split('\n') if line.strip()]
            
            i = 0
            while i < len(lines):
                if lines[i].startswith("Q："):
                    question = lines[i][2:].strip() 
                    i += 1 
                    
                    # 检查下一行是否是A
                    if i < len(lines) and lines[i].startswith("A："):
                        answer = lines[i][2:].strip() 
                        qa_objects.append({"Q": question, "A": answer})
                        i += 1 
                    else:
                        i += 1
                else:
                    i += 1
    
    return qa_objects


# 多次循环实现QA语句生成
def generate_QA(keyword="阿里", nums=5, model="qwen-turbo", api_key=os.environ.get("DASHSCOPE_API_KEY")):

    contents_to_generate_QA = RAG_vector_store.search_similar_documents(keyword, k=nums)

    results = []

    for i, doc in enumerate(contents_to_generate_QA):
        result = generate_QA_once(doc.page_content, model=model, api_key=api_key)
        results.append(result)

    # 处理生成的QA语句
    processed_results = process_generated_QA(results)
    
    return processed_results




# if __name__ == "__main__":
#     generated_QA_list = [
#         'Q：2024年巴黎奥运会上，阿里云的AI技术部署在多少个奥运场馆中？\n\nA：14个奥运场馆中。', 
#         'Q：本地生活集团在截至2024年6月30日止季度的收入是多少？  \nA：本地生活集团收入为人民币162.29亿元（22.33亿美元）。  \n\nQ：本地生活集团收入增长的主要驱动力是什么？  \nA：收入增长主要由高德和饿了么订单增长，以及市场营销服务收入增长所带动。  \n\nQ：大文娱集团在截至2024年6月30日止季度的收入是多少？  \nA：大文娱集团的收入为人民币55.81亿元（7.68亿美元）。  \n\nQ：大文娱集团收入增长的主要原因是什么？  \nA：主要由其演出赛事线上票务平台的GMV及收入增长所带动。  \n\nQ：阿里巴巴集团在2024年7月发布了哪份报告？  \nA：发布了《2024阿里巴巴环境、社会和治理（ESG）报告》。  \n\nQ：ESG报告中提到的阿里巴巴关键战略维度包括哪些内容？  \nA：包括在碳中和承诺等关键领域上的进展和表现。  \n\nQ：截至2024年6月30日止季度，阿里巴巴集团回购股份的总金额是多少？  \nA：以58亿美元的总价回购总计6.13亿股普通股。  \n\nQ：阿里巴巴集团在该季度回购股份的方式是否包括非公开市场交易？  \nA：包括2024年5月23日可转换票据发行同时透过非公开市场交易回购的部分。  \n\nQ：截至2024年6月30日，阿里巴巴集团流通的普通股数量是多少？  \nA：流通的普通股为190.24亿股（相当于23.78亿股美国存托股）。  \n\nQ：与2024年3月31日相比，阿里巴巴集团流通普通股的净减少量是多少？  \nA：净减少了4.45亿股普通股。  \n\nQ：阿里巴巴集团的企业使命是什么？  \nA：使命是让天下没有难做的生意。  \n\nQ：阿里巴巴集团的愿景包括哪些内容？  \nA：愿景是让客户相会、工作和生活在阿里巴巴，并成为一家活102年的好公司。', 
#         'Q：88VIP会员数量在本季度的同比增长情况如何？\n\nA：88VIP会员数量持续同比双位数增长，超过4,200万。', 
#         'Q：阿里巴巴集团2024年6月份季度的收入是多少，同比增长率是多少？  \nA：收入为人民币2,432.36亿元（334.70亿美元），同比增长4%。', 
#         'Q：2024年非公认会计准则净利润是多少？  \nA：人民币406.91亿元（55.99亿美元）。  \n  \n\nQ：非公认会计准则摊薄每股美国存托股收益同比下降了多少？  \nA：同比下降了5%。  \n  \n\nQ：经营活动产生的现金流量净额同比为何下降？  \nA：未直接说明原因，但自由现金流下降主要反映了对阿里云基础设施投入增加以及计划减少直营业务等因素导致的其他营运资金变动。  \n  \n\nQ：阿里推出的“全站推广”工具具备哪些功能？  \nA：具备自动出价、优化目标人群定位和效果看板可视化功能。  \n  \n\nQ：净利润下降的主要原因是什么？  \nA：主要是由于经营利润下降以及投资减值增加所致，部分被所持有的股权投资按市值计价的变动所抵销。'
#     ]

#     # 测试并打印结果
#     result = process_generated_QA(generated_QA_list)
#     print(f"提取到的Q&A数量：{len(result['qa_array'])}")
#     for i, qa in enumerate(result['qa_array'], 1):
#         print(f"\nQ{i}：{qa['Q']}")
#         print(f"A{i}：{qa['A']}")