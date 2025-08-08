# 个人项目进度管理系统

## 📋 系统概述

这是一个分布式的个人项目进度管理系统，支持多项目、多机器的进度管理，并自动同步到GitHub Pages展示。**无需在每台机器上克隆整个仓库**，只需要下载独立的同步脚本即可在任何目录下管理项目进度。

## 🏗️ 系统架构

```
ProgressReport/                    # 中央仓库（GitHub）
├── projects/                     # 所有项目进度
│   ├── project1_progress.json   # 项目1进度
│   └── project2_progress.json   # 项目2进度
├── scripts/                      # 核心脚本
│   ├── progress_manager.py      # 进度管理核心
│   ├── sync_progress.py         # 同步脚本
│   ├── standalone_sync.py       # 独立同步脚本
│   └── init_project.py          # 项目初始化脚本
└── pages/                        # GitHub Pages
    └── index.html               # 展示页面

your_project/                     # 本地项目目录（任意位置）
├── .progress_config.json        # 项目配置
├── project_id_progress.json     # 项目进度文件
├── progress_update.py           # 本地更新脚本
└── standalone_sync.py           # 独立同步脚本
```

## 🚀 快速开始

### 1. 项目初始化

在任何项目目录下运行：
```bash
curl -s https://raw.githubusercontent.com/ariusewy/ProgressReport/main/scripts/init_project.py | python3 - "项目名称" "大项目" "开发目标"
```

### 2. 添加进度

```bash
python3 progress_update.py "进度描述" "附注"
```

### 3. 查看进度

```bash
python3 progress_update.py --show
```

### 4. 同步到GitHub

```bash
python3 progress_update.py --sync
```

## 🌐 跨机器、跨目录使用

### 新机器上的新项目

1. **下载脚本**：
```bash
curl -o standalone_sync.py https://raw.githubusercontent.com/ariusewy/ProgressReport/main/scripts/standalone_sync.py
curl -o init_project.py https://raw.githubusercontent.com/ariusewy/ProgressReport/main/scripts/init_project.py
chmod +x *.py
```

2. **初始化项目**：
```bash
python3 init_project.py "新项目名称" "大项目分类" "开发目标"
```

3. **开始使用**：
```bash
python3 progress_update.py "项目启动" "开始开发"
python3 progress_update.py --sync
```

### 现有项目添加进度管理

```bash
cd /path/to/your/existing/project
curl -s https://raw.githubusercontent.com/ariusewy/ProgressReport/main/scripts/init_project.py | python3 - "现有项目" "项目分类" "项目目标"
```

### 从其他机器同步项目

```bash
curl -o standalone_sync.py https://raw.githubusercontent.com/ariusewy/ProgressReport/main/scripts/standalone_sync.py
chmod +x standalone_sync.py
python3 standalone_sync.py sync
```

## 📊 进度格式

```json
{
  "project_name": "项目名称",
  "parent_project": "隶属大项目",
  "development_goal": "开发目标",
  "created_date": "2024-01-15",
  "last_updated": "2024-01-16T10:30:00",
  "progress_entries": [
    {
      "date": "2024-01-15",
      "time": "14:30",
      "description": "完成了项目初始化",
      "notes": "遇到了一些依赖问题，已解决",
      "tags": ["初始化", "框架搭建"]
    }
  ]
}
```

## 🔧 配置说明

### 项目配置文件 (.progress_config.json)
```json
{
  "project_id": "unique_project_id",
  "project_name": "项目名称",
  "parent_project": "隶属大项目",
  "development_goal": "开发目标",
  "project_path": "/path/to/project",
  "central_repo_url": "https://github.com/ariusewy/ProgressReport",
  "last_sync": "2024-01-16T10:30:00Z",
  "sync_mode": "realtime"
}
```

## 📈 功能特性

- ✅ **分布式项目管理** - 支持多项目、多机器管理
- ✅ **独立同步脚本** - 无需本地ProgressReport仓库即可同步
- ✅ **自动同步到GitHub** - 实时同步到中央仓库
- ✅ **GitHub Pages展示** - 自动生成网页展示
- ✅ **离线支持** - 本地存储，网络恢复后同步
- ✅ **跨机器同步** - 在任何机器、任何目录下使用
- ✅ **智能冲突解决** - 自动处理并发更新
- ✅ **多种视图** - 日视图、周视图、月视图
- ✅ **时间线展示** - 可视化项目进度时间线

## 🛠️ 开发状态

- [x] 核心架构设计
- [x] 进度管理脚本
- [x] 同步机制
- [x] 独立同步脚本
- [x] GitHub Pages生成
- [x] 自动化部署
- [x] 跨机器支持
- [x] 多种视图（日/周/月）
- [x] 时间线展示

## 🔗 相关链接

- **GitHub仓库**: https://github.com/ariusewy/ProgressReport
- **GitHub Pages**: https://ariusewy.github.io/ProgressReport/
- **独立同步脚本**: https://raw.githubusercontent.com/ariusewy/ProgressReport/main/scripts/standalone_sync.py
- **初始化脚本**: https://raw.githubusercontent.com/ariusewy/ProgressReport/main/scripts/init_project.py


