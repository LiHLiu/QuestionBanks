import json

def add_question_list(existing_file_path, new_list_name, new_qa_list):
    # 1. 读取现有JSON文件
    try:
        with open(existing_file_path, "r", encoding="utf-8") as f:
            existing_data = json.load(f)
    except FileNotFoundError:
        # 若文件不存在，初始化一个空字典
        existing_data = {}
    
    # 2. 添加新的question_list（如question_list2）
    existing_data[new_list_name] = new_qa_list
    
    # 3. 保存更新后的JSON文件
    with open(existing_file_path, "w", encoding="utf-8") as f:
        json.dump(existing_data, f, ensure_ascii=False, indent=2)
    
    print(f"已成功添加{new_list_name}，与原有列表并列")
