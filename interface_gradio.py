import gradio as gr
import LLM_functions
import question_list
import RAG_vector_store
import os

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

# 创建文件导入界面
# def create_input_file_interface():
#     with gr.Blocks() as input_file_interface:
#         gr.Markdown("## 📁 向量数据库文档导入工具")
#         gr.Markdown("上传 `.pdf`, `.txt`, `.md`, `.docx` 文件，将其添加到 FAISS 向量数据库中。")

#         # 明确指定所有参数
#         file_input = gr.File(
#             label="选择文件",
#             file_types=[".pdf", ".txt", ".md", ".docx"],
#             type="filepath",
#             value=None  # 明确设置初始值
#         )
#         upload_button = gr.Button("📥 导入到数据库")
#         output = gr.Textbox(
#             label="状态信息", 
#             interactive=False, 
#             value="",  # 明确设置初始值
#             lines=3    # 可选：设置显示行数
#         )

#         def safe_upload_file(file_obj):
#             if file_obj is None:
#                 return "⚠️ 请先上传一个文件。"
#             try:
#                 result = RAG_vector_store.add_new_documents_to_vector_store(file_obj.name)
#                 return str(result) if result else "✅ 文件导入完成！"
#             except Exception as e:
#                 return f"❌ 导入失败：{str(e)}"

#         upload_button.click(
#             fn=safe_upload_file, 
#             inputs=file_input, 
#             outputs=output
#         )

#     return input_file_interface

# 创建文件导入界面
def create_input_file_interface():
    with gr.Blocks(title="通过路径导入RAG数据库") as interface:
        gr.Markdown("## 📂 向量数据库文档导入工具（路径版）")
        gr.Markdown("输入本地文件路径（支持 `.pdf`, `.txt`, `.md`, `.docx`），将文件添加到FAISS向量数据库")
        
        # 文件路径输入框
        file_path_input = gr.Textbox(
            label="文件路径",
            placeholder="例如：C:/documents/report.pdf 或 /home/user/data.txt",
            lines=1
        )
        
        # 格式提示
        gr.Markdown("""
        > 支持格式：.pdf, .txt, .md, .docx  
        > 提示：路径需包含完整文件名和扩展名  
        > Windows示例：D:/资料/技术文档.docx  
        > Linux/Mac示例：/user/docs/notes.md
        """)
        
        # 操作按钮和结果展示
        with gr.Row():
            import_btn = gr.Button("📥 导入到数据库", variant="primary")
            clear_btn = gr.Button("🧹 清空输入", variant="secondary")
        
        result_output = gr.Textbox(
            label="操作结果",
            interactive=False,
            lines=3,
            placeholder="操作结果将显示在这里..."
        )
        
        # 验证路径并导入
        def import_by_path(file_path):
            if not file_path:
                return "⚠️ 请输入文件路径"
            
            # 基础路径验证
            if not os.path.exists(file_path):
                return f"❌ 路径不存在：{file_path}"
            
            if not os.path.isfile(file_path):
                return f"❌ 不是有效文件：{file_path}"
            
            # 验证文件格式
            valid_extensions = ('.pdf', '.txt', '.md', '.docx')
            if not file_path.lower().endswith(valid_extensions):
                return f"❌ 不支持的文件格式，仅支持：{valid_extensions}"
            
            # 调用导入函数
            try:
                result = RAG_vector_store.add_new_documents_to_vector_store(file_path)
                return str(result) if result else f"✅ 成功导入文件：{os.path.basename(file_path)}"
            except Exception as e:
                return f"❌ 导入失败：{str(e)}"
        
        # 清空输入
        def clear_input():
            return "", ""
        
        # 绑定事件
        import_btn.click(
            fn=import_by_path,
            inputs=[file_path_input],
            outputs=[result_output]
        )
        
        clear_btn.click(
            fn=clear_input,
            inputs=[],
            outputs=[file_path_input, result_output]
        )
    
    return interface
    
##### 创建题库生成界面
# def create_generate_interface():
#     with gr.Blocks() as generate_interface:
#         gr.Markdown("# Q&A生成器")
#         gr.Markdown("根据关键词生成相关的Q&A列表")
        
#         with gr.Row():
#             keyword = gr.Textbox(label="关键词", placeholder="请输入关键词")
#             num_results = gr.Number(label="返回结果数量", value=5, step=1)
#             model_name = gr.Textbox(label="模型名称", value="qwen-turbo", placeholder="请输入模型名称")
        
#         generate_btn = gr.Button("生成Q&A", variant="primary")
        
#         qa_output = gr.JSON(label="生成的Q&A列表")
        
#         save_btn = gr.Button("保存到题库", variant="secondary")
#         save_status = gr.Textbox(label="保存状态", interactive=False)
        
#         generate_btn.click(
#             fn=LLM_functions.generate_QA,
#             inputs=[keyword, num_results, model_name],
#             outputs=qa_output
#         )
        
#         def save_qa_list(qa_data, keyword_text):
#             if not qa_data: 
#                 return "请先生成Q&A列表再保存"
#             try:
                
#                 question_list.add_question_list(
#                     existing_file_path="./question_list/question_lists.json", 
#                     new_list_name=keyword_text,
#                     new_qa_list=qa_data
#                 )
#                 return f"保存成功！已添加到题库:{keyword_text}"
#             except Exception as e:
#                 return f"保存失败：{str(e)}"
        
#         save_btn.click(
#             fn=save_qa_list,
#             inputs=[qa_output, keyword], 
#             outputs=save_status
#         )

#     return generate_interface


def create_generate_interface():
    with gr.Blocks() as generate_interface:
        gr.Markdown("# Q&A生成器")
        gr.Markdown("分两步：1. 搜索关键词相关语段 2. 基于搜索结果生成Q&A")
        
        # 存储搜索结果的隐藏状态（仅用于保存实际搜索数据）
        search_results = gr.State(None)
        
        # 第一步：关键词搜索相关语段
        gr.Markdown("## 1. 搜索关键词相关语段")
        with gr.Row():
            search_keyword = gr.Textbox(label="搜索关键词", placeholder="请输入需要搜索的关键词/句子，例如：阿里云计算")
            search_top_k = gr.Number(label="搜索结果数量（k）", value=4, step=1, minimum=1)
            search_btn = gr.Button("🔍 执行搜索", variant="primary")
        
        # 显示搜索到的语段
        search_result_display = gr.HTML(
            label="搜索到的相关语段", 
            value="<div style='padding:10px; color:#666;'>请点击上方搜索按钮获取相关语段</div>"
        )
        
        # 第二步：基于搜索结果生成Q&A（生成按钮设置为始终可点击）
        gr.Markdown("## 2. 基于搜索结果生成Q&A")
        with gr.Row():
            qa_per_doc = gr.Number(label="每个语段生成QA数量", value=1, step=1, minimum=1)
            model_name = gr.Textbox(label="模型名称", value="qwen-turbo", placeholder="请输入通义千问模型名称，如qwen-turbo")
            generate_btn = gr.Button("📝 生成Q&A", variant="primary", interactive=True)  # 始终启用
        
        # Q&A输出和保存区域
        qa_output = gr.JSON(label="生成的Q&A列表")
        save_btn = gr.Button("💾 保存到题库", variant="secondary", interactive=False)
        save_status = gr.Textbox(label="保存状态", interactive=False)
        
        # ---------------------- 1. 搜索按钮逻辑 ----------------------
        def handle_search(query, k):
            similar_docs = RAG_vector_store.search_similar_documents(query=query, k=int(k))
            if not similar_docs or not query.strip():
                return (
                    "<div style='padding:10px; color:#ff4444;'>未找到相关语段，请检查关键词或增加搜索数量重试</div>",
                    None
                )
            
            html_content = "<div style='padding:10px;'>"
            for i, doc in enumerate(similar_docs, 1):
                content_preview = doc.page_content[:300] + "..." if len(doc.page_content) > 300 else doc.page_content
                source = doc.metadata.get("source", "Unknown")
                page = doc.metadata.get("page", "N/A")
                html_content += f"""
                <div style='margin-bottom:15px; padding:10px; border:1px solid #eee; border-radius:5px;'>
                    <h4 style='margin:0; color:#2196F3;'>语段 {i}</h4>
                    <p style='margin:5px 0;'><strong>来源文件：</strong>{source}</p>
                    <p style='margin:5px 0;'><strong>页码：</strong>{page}</p>
                    <p style='margin:5px 0;'><strong>内容预览：</strong>{content_preview}</p>
                </div>
                """
            html_content += "</div>"
            return html_content, similar_docs
        
        search_btn.click(
            fn=handle_search,
            inputs=[search_keyword, search_top_k],
            outputs=[search_result_display, search_results]
        )
        
        # ---------------------- 2. 生成Q&A按钮逻辑（始终可点击） ----------------------
        generate_btn.click(
            fn=LLM_functions.generate_QA,
            inputs=[
                search_keyword,
                search_top_k,
                qa_per_doc,
                model_name
            ],
            outputs=qa_output
        ).then(
            fn=lambda qa_data: gr.Button.update(interactive=bool(qa_data)),
            inputs=qa_output,
            outputs=save_btn
        )
        
        # ---------------------- 3. 保存按钮逻辑 ----------------------
        def save_qa_list(qa_data, keyword_text):
            if not qa_data:
                return "请先生成Q&A列表再保存"
            try:
                question_list.add_question_list(
                    existing_file_path="./question_list/question_lists.json",
                    new_list_name=keyword_text,
                    new_qa_list=qa_data
                )
                return f"保存成功！已添加到题库：{keyword_text}"
            except Exception as e:
                return f"保存失败：{str(e)}"
        
        save_btn.click(
            fn=save_qa_list,
            inputs=[qa_output, search_keyword],
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
            with gr.Tab("文件导入"):
                create_input_file_interface()

            with gr.Tab("题库生成"):
                create_generate_interface() 

            with gr.Tab("题库列表"):
                create_question_list_interface()  
            
    return main_interface

    # with gr.Blocks(title="智选题库") as main_interface:
    #     gr.Markdown("# 📋 智选题库管理系统 ")
        
    #     # 创建标签导航栏
    #     with gr.Tabs():
    #         with gr.Tab("文件导入"):
    #             # 直接创建组件而不是嵌套Blocks
    #             gr.Markdown("## 📁 向量数据库文档导入工具")
    #             gr.Markdown("上传 `.pdf`, `.txt`, `.md`, `.docx` 文件，将其添加到 FAISS 向量数据库中。")

    #             file_input = gr.File(
    #                 label="选择文件",
    #                 file_types=[".pdf", ".txt", ".md", ".docx"],
    #                 type="filepath"
    #             )
    #             upload_button = gr.Button("📥 导入到数据库")
    #             output = gr.Textbox(label="状态信息", interactive=False, value="")

    #             upload_button.click(fn=upload_file, inputs=file_input, outputs=output)

    #         with gr.Tab("题库生成"):
    #             create_generate_interface()()

    #         with gr.Tab("题库列表"):
    #             create_question_list_interface()()
            
    # return main_interface