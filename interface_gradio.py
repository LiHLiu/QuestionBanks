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
    with gr.Blocks() as generate_interface:
        gr.Markdown("# Q&A生成器")
        gr.Markdown("根据关键词生成相关的Q&A列表")
        
        with gr.Row():
            keyword = gr.Textbox(label="关键词", placeholder="请输入关键词")
            num_results = gr.Number(label="返回结果数量", value=5, step=1)
            model_name = gr.Textbox(label="模型名称", value="qwen-turbo", placeholder="请输入模型名称")
        
        generate_btn = gr.Button("生成Q&A", variant="primary")
        
        qa_output = gr.JSON(label="生成的Q&A列表")
        
        save_btn = gr.Button("保存到题库", variant="secondary")
        save_status = gr.Textbox(label="保存状态", interactive=False)
        
        generate_btn.click(
            fn=LLM_functions.generate_QA,
            inputs=[keyword, num_results, model_name],
            outputs=qa_output
        )
        
        def save_qa_list(qa_data, keyword_text):
            if not qa_data: 
                return "请先生成Q&A列表再保存"
            try:
                
                question_list.add_question_list(
                    existing_file_path="./question_list/question_lists.json", 
                    new_list_name=keyword_text,
                    new_qa_list=qa_data
                )
                return f"保存成功！已添加到题库:{keyword_text}"
            except Exception as e:
                return f"保存失败：{str(e)}"
        
        save_btn.click(
            fn=save_qa_list,
            inputs=[qa_output, keyword], 
            outputs=save_status
        )

    return generate_interface


##### 创建题库列表展示界面
def create_question_list_interface():
    # 定义加载题库数据的函数
    def load_question_data():
        try:
            question_lists = question_list.load_all_question_lists("./question_list/question_lists.json")
            return question_lists
        except Exception as e:
            return {"错误": [f"加载题库失败: {str(e)}"]}

    # 解析单个QA项（针对你的数据格式）
    def parse_single_qa(qa_item):
        """解析QA项，针对 Q/A 格式"""
        if isinstance(qa_item, dict):
            # 优先查找 Q/A 键
            question = (qa_item.get('Q') or 
                       qa_item.get('question') or 
                       qa_item.get('问题') or 
                       '未知问题')
            
            answer = (qa_item.get('A') or 
                     qa_item.get('answer') or 
                     qa_item.get('答案') or 
                     '未知答案')
            
            return question, answer
        else:
            return str(qa_item), '未知答案'

    # 将单个题库数据转换为HTML格式
    def format_questions_to_html(question_lists):
        if not question_lists:
            return "<div style='padding: 20px;'><p>暂无题库数据</p></div>"
        
        html_content = "<div style='padding: 20px;'>"
        
        for bank_name, questions in question_lists.items():
            # 格式化每个题库的内容
            content = ""
            if isinstance(questions, list):
                for i, qa in enumerate(questions, 1):
                    question, answer = parse_single_qa(qa)
                    content += f"<p><strong>{i}. 问题:</strong> {question}</p>"
                    content += f"<p><strong>答案:</strong> {answer}</p><br>"
            else:
                # 如果不是列表，直接显示
                content = f"<p>{str(questions)}</p>"
            
            # 使用HTML details标签实现折叠效果
            html_content += f'''
            <details style="margin-bottom: 15px; border: 1px solid #ddd; border-radius: 5px; padding: 10px;">
                <summary style="cursor: pointer; font-weight: bold; font-size: 16px;">{bank_name}</summary>
                <div style="margin-top: 10px; padding: 10px;">
                    {content}
                </div>
            </details>
            '''
        
        html_content += "</div>"
        return html_content

    with gr.Blocks() as question_list_interface:
        gr.Markdown("# 📚 题库列表")
        
        # 使用HTML组件显示题库内容（支持原生折叠效果）
        html_display = gr.HTML()
        
        # 刷新按钮
        refresh_btn = gr.Button("刷新题库列表", variant="primary")
        
        # 刷新函数
        def refresh_question_list():
            question_lists = load_question_data()
            html_content = format_questions_to_html(question_lists)
            return html_content
        
        # 绑定按钮点击事件
        refresh_btn.click(
            fn=refresh_question_list,
            inputs=[],
            outputs=[html_display]
        )
        
        # 初始化时加载数据
        question_list_interface.load(
            fn=refresh_question_list,
            inputs=[],
            outputs=[html_display]
        )
    
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