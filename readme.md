
# 智选题库 QuestionBanks

![Visitor Badge](https://visitor-badge.laobi.icu/badge?page_id=LiHLiu.QuestionBanks)

## 项目简介

智选题库（QuestionBanks）是一个智能题库管理与生成系统，支持多种格式的题库数据（txt、md、pdf、docx），集成 RAG 向量检索和 FAISS 索引，结合大模型自动生成问答，适用于教育、企业知识管理等场景。系统提供 Gradio 网页界面和 Jupyter Notebook 演示，便于交互和扩展。

## 主要功能

- 多格式题库文件导入（txt、md、pdf、docx）
- RAG（检索增强生成）向量数据库构建与智能问答
- FAISS 索引管理与高效检索
- 题库自动生成、管理与筛选
- 支持大模型（如通义千问）自动生成 Q&A
- Gradio 可视化界面，支持文件导入、题库生成、题库浏览
- Jupyter Notebook 交互式演示

## 目录结构

```
data.py                 # 题库数据处理与格式化
interface_gradio.py     # Gradio 网页界面（文件导入/题库生成/题库浏览）
LLM_functions.py        # 大模型问答与选项生成
Question_Banks.ipynb    # 交互式 Notebook 演示
question_list.py        # 题库列表管理与 JSON 存储
RAG_vector_store.py     # RAG 向量数据库与 FAISS 索引
requirements.txt        # 项目依赖
data/                   # 题库原始数据（txt/md/pdf/docx）
faiss_index/            # FAISS 索引文件（index.faiss/index.pkl）
question_list/          # 题库列表 JSON 文件
readme.md               # 项目说明文档
LICENSE					# 开源协议
```

## 环境依赖

- Python 3.8+
- 推荐使用虚拟环境
- 主要依赖：faiss-cpu、langchain、dashscope、gradio、pandas、numpy 等
- 详细依赖见 `requirements.txt`

## 快速开始

1. 克隆项目
	```
	git clone git@github.com:LiHLiu/QuestionBanks.git
	cd QuestionBanks
	```
2. 安装依赖
	```
	pip install -r requirements.txt
	```

3. 数据准备
	 - 准备好需要进行题库生成的原始文件，可以是 txt、md、pdf、docx 等多种类型的文件

4. 获取并设置阿里云百炼 API Key
	 - 访问 [阿里云百炼官网](https://dashscope.aliyun.com/) 注册并获取 API Key

5. 运行 Jupyter Notebook 示例
	 ```
	 jupyter notebook Question_Banks.ipynb
	 ```

## 使用说明

- 数据预处理与格式化：`data.py`
- 向量数据库与检索：`RAG_vector_store.py`
- 题库管理与存储：`question_list.py`
- 大模型问答与选项生成：`LLM_functions.py`
- Gradio 网页界面：`interface_gradio.py`
- 交互式演示：`Question_Banks.ipynb`

## 特色亮点

- 支持多格式题库文件自动导入与处理
- 集成 RAG 检索增强生成，结合大模型智能问答
- FAISS 高效向量索引，支持快速检索
- Gradio 可视化界面，操作便捷
- 题库自动生成、管理与筛选，支持 JSON 存储

## 许可证

本项目采用 MIT License 开源协议，详见 LICENSE 文件。


