# QuestionBanks 题库系统

## 项目简介

QuestionBanks 是一个用于生成并管理和检索题库的系统，支持文本、PDF 等多种格式的题库数据，并集成了 RAG 向量检索、FAISS 索引等功能，便于智能问答和知识管理。

## 目录结构

```
data.py                # 数据处理相关代码
LLM_functions.py       # 大模型相关功能
Question_Banks.ipynb   # 交互式 Jupyter Notebook 示例
question_list.py       # 题目列表管理
RAG_vector_store.py    # RAG 向量存储与检索
readme.md              # 项目说明文档
data/                  # 题库原始数据（txt、md、pdf等）
faiss_index/           # FAISS 索引文件
question_list/         # 题目列表JSON文件

```

## 主要功能

- 支持多格式题库数据导入（txt、md、pdf）
- 题目列表管理与筛选
- RAG 向量检索与问答
- FAISS 索引构建与查询
- Jupyter Notebook 交互式演示

## 环境依赖

- Python 3.8+
- 主要依赖库：faiss、numpy、pandas、openai、langchain 等
- 推荐使用虚拟环境管理依赖

## 快速开始

1. 克隆项目到本地：
	```
	git clone <项目地址>
	cd QuestionBanks
	```

2. 安装依赖：
	```
	pip install -r requirements.txt
	```

3. 数据准备：
	- 将题库文件放入 `data/` 目录
	- 题目列表 JSON 文件放入 `question_list/` 目录

4. 构建 FAISS 索引：
	```
	python RAG_vector_store.py
	```

5. 运行 Jupyter Notebook 示例：
	```
	jupyter notebook Question_Banks.ipynb
	```

## 使用说明

- 通过 `data.py` 进行数据预处理
- 使用 `RAG_vector_store.py` 构建和查询向量索引
- 题目管理与筛选请参考 `question_list.py`
- 交互式操作可在 `Question_Banks.ipynb` 中完成

## 许可证

