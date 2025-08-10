from typing import List, Dict
import json

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


def list_to_json(array):
    """
    将列表转换为JSON格式字符串
    """
    return json.dumps(array, ensure_ascii=False, indent=2) 