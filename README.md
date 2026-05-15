# 多租户 AI 问答系统

## 项目简介
本项目为 B2B SaaS 多租户 AI 问答系统，实现企业级知识库隔离、文件解析分块、混合检索与流式问答功能。每个租户拥有独立知识库，互相完全隔离，支持租户 Token 使用配额限制。

## 核心功能
- 多租户数据隔离：支持 tenant_a、tenant_b、tenant_c 三个租户
- 文件摄取：支持 TXT、PDF、Markdown 格式上传
- 可配置分块：Chunk 大小与重叠量可配置
- 摄取状态追踪：pending / processing / done / failed
- 混合检索：向量检索 + BM25 关键词检索，RRF 结果融合
- 来源溯源：返回文件名、相关段落
- SSE 流式问答输出
- 问答指标记录：Token 用量、检索耗时、生成耗时、使用块数量
- 租户配额控制：超配额返回明确错误提示

## 运行方式
1. 安装依赖
pip install -r requirements.txt

2. 启动服务
python run.py

3. 接口文档地址
http://127.0.0.1:8000/docs