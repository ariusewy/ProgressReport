# 个人项目进度管理系统

## 📋 系统概述

这是一个分布式的个人项目进度管理系统，支持多项目、多机器的进度管理，并自动同步到GitHub Pages展示。

## 🏗️ 系统架构

```
ProgressReport/                    # 中央仓库
├── projects/                     # 所有项目进度
│   ├── project1_progress.json   # 项目1进度
│   └── project2_progress.json   # 项目2进度
├── scripts/                      # 核心脚本
│   ├── progress_manager.py      # 进度管理核心
│   └── sync_progress.py         # 同步脚本
└── pages/                        # GitHub Pages
    └── index.html               # 展示页面

your_project/                     # 本地项目目录
├── .progress_config.json        # 项目配置
└── progress_update.py           # 本地更新脚本
```

## 🚀 快速开始

### 1. 项目初始化

在项目目录下运行：
```bash
curl -s https://raw.githubusercontent.com/yourusername/ProgressReport/main/scripts/init_project.py | python3 - "项目名称" "大项目" "开发目标"
```

### 2. 添加进度

```bash
# 使用本地脚本
python3 progress_update.py "进度描述" "附注"

# 或使用别名（需要配置）
progress "完成了功能A" "性能优化待完成"
```

### 3. 查看进度

```bash
# 查看项目进度
progress --show

# 查看所有项目
progress --list
```

## 📊 进度格式

```json
{
  "project_name": "项目名称",
  "parent_project": "隶属大项目",
  "development_goal": "开发目标",
  "created_date": "2024-01-15",
  "last_updated": "2024-01-16",
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
  "central_repo_url": "https://github.com/yourusername/ProgressReport",
  "last_sync": "2024-01-16T10:30:00Z",
  "sync_mode": "realtime"
}
```

## 📈 功能特性

- ✅ 分布式项目管理
- ✅ 自动同步到GitHub
- ✅ GitHub Pages展示
- ✅ 离线支持
- ✅ 多机器同步
- ✅ 智能冲突解决

## 🛠️ 开发状态

- [x] 核心架构设计
- [ ] 进度管理脚本
- [ ] 同步机制
- [ ] GitHub Pages生成
- [ ] 自动化部署
