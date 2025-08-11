import gradio as gr
import LLM_functions
import question_list


# 单个题库内容展示
def show_question_lists(questions):
    content = []
    for i, qa in enumerate(questions, 1):
        # 每个题目显示为：Q1: ...\nA1: ...
        content.append(f"**Q{i}：** {qa['Q']}\n\n**A{i}：** {qa['A']}\n\n---")
    return "\n".join(content)



######################################
#
#            创建聊天界面  
#
######################################


##### 创建题库生成界面
def create_generate_interface():
    generate_interface = gr.Interface(
        fn=LLM_functions.generate_QA,
        inputs=[
            gr.Textbox(label="关键词", placeholder="请输入关键词"),
            gr.Number(label="返回结果数量", value=5, step=1),
            gr.Textbox(label="模型名称", value="qwen-turbo", placeholder="请输入模型名称"),
        ],
        outputs=gr.JSON(label="生成的Q&A列表"),
        title="Q&A生成器",
        description="根据关键词生成相关的Q&A列表",
        allow_flagging="never"
    )
    return generate_interface


##### 创建题库列表展示界面
def create_question_list_interface():
    # 加载题库
    question_lists = question_list.load_all_question_lists("./question_list/question_lists.json")
    with gr.Blocks() as question_list_interface:
        gr.Markdown("# 📚 题库列表")
        
        # 遍历所有题库，用折叠面板分组显示
        for bank_name, questions in question_lists.items():
            # 每个题库用一个折叠面板（Accordion）
            with gr.Accordion(label=bank_name, open=False):  # open=False 初始折叠
                # 用 Markdown 展示题目（支持加粗和换行）
                gr.Markdown(show_question_lists(questions))
    return question_list_interface


##### 创建主界面
def create_main_interface():
    with gr.Blocks(title="智选题库") as main_interface:
        gr.Markdown("# 📋 智选题库管理系统 ")
        
        # 创建标签导航栏
        with gr.Tabs():
            # 第一个标签：题库列表（demo1）
            with gr.Tab("题库列表"):
                create_question_list_interface()  # 嵌入demo1
            
            # 第二个标签：题库生成（demo2）
            with gr.Tab("题库生成"):
                create_generate_interface()  # 嵌入demo2
    return main_interface