import json

# 向现有的JSON文件中添加新的question_list
def add_question_list(existing_file_path, new_list_name, new_qa_list):
    try:
        with open(existing_file_path, "r", encoding="utf-8") as f:
            existing_data = json.load(f)
    except FileNotFoundError:
        existing_data = {}
    
    existing_data[new_list_name] = new_qa_list
    
    with open(existing_file_path, "w", encoding="utf-8") as f:
        json.dump(existing_data, f, ensure_ascii=False, indent=2)
    
    print(f"已成功添加{new_list_name}，与原有列表并列")


# 加载题库所有question_list
def load_all_question_lists(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data
