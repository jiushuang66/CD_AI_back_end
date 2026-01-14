# 项目结构与文件说明

该文档说明仓库中各文件夹和主要文件的用途，作为浏览或贡献代码时的快速参考。

**根目录**
- **alembic.ini**：Alembic 的数据库迁移配置。
- **database_setup.py**：用于创建与同步数据库表和索引的脚本。（注意：此文件曾多次编辑，运行前请先检查缩进与 SQL 定义。）
- **main.py**：应用入口，创建 FastAPI 实例并挂载路由与中间件。
- **README.md**：项目说明文档，包含运行与部署的高层说明。
- **requirements.txt**：Python 依赖清单。
- **DEPENDENCIES.md**：可选依赖或环境相关说明。
- **.gitignore**：Git 忽略规则。

**app/**
- [app/__init__.py](app/__init__.py)：包标识，可能导出应用工厂。
- [app/config.py](app/config.py)：从 `.env` 加载环境变量，构建 `DATABASE_URL` 等设置。
- [app/database.py](app/database.py)：数据库连接与会话工厂，使用 `app/config.py` 中的设置。

-- **app/api/**
- [app/api/v1/__init__.py](app/api/v1/__init__.py)：API 版本包。
- [app/api/v1/routes.py](app/api/v1/routes.py)：将各版本路由注册到 FastAPI 应用。
- [app/api/v1/endpoints/health.py](app/api/v1/endpoints/health.py)：健康检查（liveness/readiness）。
- [app/api/v1/endpoints/documents.py](app/api/v1/endpoints/documents.py)：文档/文稿相关的通用接口（兼容或历史接口）。
- [app/api/v1/endpoints/papers.py](app/api/v1/endpoints/papers.py)：论文上传与版本管理接口（校验文件类型/大小，上传 OSS，并记录元数据）。
- [app/api/v1/endpoints/groups.py](app/api/v1/endpoints/groups.py)：班级/分组导入（Excel）与管理接口。
- [app/api/v1/endpoints/annotations.py](app/api/v1/endpoints/annotations.py)：注释/批注管理接口（教师/学生注释）。
- [app/api/v1/endpoints/ai_review.py](app/api/v1/endpoints/ai_review.py)：触发 AI 审核和获取 AI 报告的接口（后台任务提交到 AI 适配器）。
- [app/api/v1/endpoints/admin.py](app/api/v1/endpoints/admin.py)：管理员接口（模板管理、统计、审计日志）。

-- **app/core/**
- [app/core/dependencies.py](app/core/dependencies.py)：FastAPI 依赖注入助手（如 `get_db`, `get_current_user`）。
- [app/core/security.py](app/core/security.py)：JWT 与安全相关工具（令牌解码、HTTP Bearer 等）。

-- **app/middleware/**
- [app/middleware/logging.py](app/middleware/logging.py)：请求/响应日志中间件，接入全局日志器。

-- **app/models/**
- [app/models/document.py](app/models/document.py)：文档/论文相关的 ORM 或数据模型定义。

-- **app/schemas/**
- [app/schemas/document.py](app/schemas/document.py)：Pydantic 请求/响应模型（论文与版本）。
- [app/schemas/annotation.py](app/schemas/annotation.py)：注释相关的 Pydantic 模型。

-- **app/services/**
- [app/services/document.py](app/services/document.py)：文档相关的业务逻辑（数据库持久化等封装）。
- [app/services/oss.py](app/services/oss.py)：OSS 上传与临时 URL 生成的封装；数据库仅保存 OSS key 与元数据。
- [app/services/ai_adapter.py](app/services/ai_adapter.py)：调用外部 AI 服务的适配器（当前为 stub 实现）。

-- **app/utils/**
- [app/utils/logger.py](app/utils/logger.py)：全局日志器配置（如 Loguru 封装）。

**tools/doc_reader/**
- [tools/doc_reader/cli.py](tools/doc_reader/cli.py)：本地文档解析工具的 CLI 入口。
- [tools/doc_reader/reader.py](tools/doc_reader/reader.py)：文档解析实现，用于 CLI 或其他调用方。
- [tools/doc_reader/README.md](tools/doc_reader/README.md)：文档阅读器工具的使用说明。

**其它顶层目录**
- **logs/**：运行时日志输出目录。
- **src/**：占位或子项目源码目录（视分支可能包含前端或其它服务）。
- **src/config/** 与 **src/middleware/**：可能包含额外的配置或中间件实现。
- **tools/**：工具脚本与辅助程序（包含 `doc_reader`）。

说明与后续工作
- `database_setup.py` 文件曾多次被编辑并出现缩进错误；在执行前请先运行语法检查。
- 目前许多 API 路由为脚手架（stub），它们会校验输入并调用 OSS/AI 的 stub 服务，但尚未完成数据库持久化与权限（如“论文所有者或指导教师”）的完整实现。
- 若需要，我可以：
  - 将已搭建的接口与实际数据库操作对接。
  - 运行 `python -m py_compile database_setup.py` 并修复可能的语法问题。
  - 在 `PROJECT_STRUCTURE.md` 中加入流程图或数据流示意。
