# 个人项目进度管理系统 - 使用说明

## 🚀 快速开始

### 1. 系统架构

```
ProgressReport/                    # 中央仓库（GitHub）
├── projects/                     # 所有项目进度
│   ├── project1_progress.json   # 项目1进度
│   └── project2_progress.json   # 项目2进度
├── scripts/                      # 核心脚本
│   ├── progress_manager.py      # 进度管理核心
│   ├── sync_progress.py         # 同步脚本
│   └── generate_pages.py        # 页面生成脚本
└── pages/                        # GitHub Pages
    └── index.html               # 展示页面

your_project/                     # 本地项目目录
├── .progress_config.json        # 项目配置
└── progress_update.py           # 本地更新脚本
```

### 2. 项目初始化

在项目目录下运行：

```bash
# 方式1：使用curl（推荐）
curl -s https://raw.githubusercontent.com/ariusewy/ProgressReport/main/scripts/init_project.py | python3 - "项目名称" "隶属大项目" "开发目标"

# 方式2：直接运行脚本
python3 scripts/init_project.py "机器学习项目" "AI研究" "实现图像分类算法"
```

**参数说明：**
- `项目名称`：当前项目的名称
- `隶属大项目`：项目所属的大项目分类
- `开发目标`：项目的开发目标描述

**示例：**
```bash
python3 scripts/init_project.py "深度学习模型" "AI研究" "实现CNN图像分类"
```

### 3. 添加进度

```bash
# 添加进度（带附注）
python3 progress_update.py "完成了数据预处理模块" "数据清洗耗时较长"

# 添加进度（无附注）
python3 progress_update.py "实现了核心算法"

# 查看项目进度
python3 progress_update.py --show
```

### 4. 同步到GitHub

```bash
# 同步到中央仓库
python3 scripts/sync_progress.py sync

# 从中央仓库同步
python3 scripts/sync_progress.py pull

# 处理同步队列（离线模式）
python3 scripts/sync_progress.py queue
```

## 📊 进度格式

### JSON结构

```json
{
  "project_name": "项目名称",
  "parent_project": "隶属大项目",
  "development_goal": "开发目标",
  "created_date": "2024-01-15",
  "last_updated": "2024-01-16T10:30:00Z",
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

### 进度条目字段

- `date`：日期（YYYY-MM-DD格式）
- `time`：时间（HH:MM格式）
- `description`：进度描述
- `notes`：附注信息
- `tags`：标签数组

## 🔄 同步机制

### 实时同步 vs 定时同步

**实时同步（默认）：**
- 每次添加进度时立即同步
- 网络依赖性强
- 数据一致性高

**定时同步：**
- 批量处理，效率高
- 支持离线操作
- 网络友好

### 离线支持

当网络不可用时，系统会：
1. 将同步任务加入队列
2. 在本地保存进度
3. 网络恢复后自动同步

## 🌐 GitHub Pages展示

### 访问地址

部署完成后，可以通过以下地址访问：
```
https://yourusername.github.io/ProgressReport/
```

### 页面功能

1. **主页**：项目概览和统计信息
2. **时间线**：按时间顺序查看所有进度
3. **项目页面**：单个项目的详细进度

## 🛠️ 高级功能

### 1. 批量操作

```bash
# 批量添加进度
for project in project1 project2 project3; do
    cd $project
    python3 progress_update.py "完成了阶段性目标" "所有模块测试通过"
done
```

### 2. 自定义配置

编辑 `.progress_config.json`：

```json
{
  "project_id": "abc12345",
  "project_name": "项目名称",
  "parent_project": "隶属大项目",
  "development_goal": "开发目标",
  "project_path": "/path/to/project",
          "central_repo_url": "https://github.com/ariusewy/ProgressReport",
  "last_sync": "2024-01-16T10:30:00Z",
  "sync_mode": "realtime"
}
```

### 3. 脚本别名

在 `.bashrc` 中添加别名：

```bash
# 添加进度别名
alias progress='python3 progress_update.py'

# 查看进度别名
alias progress-show='python3 progress_update.py --show'

# 同步别名
alias progress-sync='python3 scripts/sync_progress.py sync'
```

## 🔧 故障排除

### 常见问题

1. **配置文件不存在**
   ```bash
   # 重新初始化项目
   python3 scripts/init_project.py "项目名称" "大项目" "目标"
   ```

2. **同步失败**
   ```bash
   # 检查网络连接
   ping github.com
   
   # 手动同步
   python3 scripts/sync_progress.py sync --force
   ```

3. **权限问题**
   ```bash
   # 设置执行权限
   chmod +x progress_update.py
   chmod +x scripts/*.py
   ```

### 日志查看

```bash
# 查看同步日志
tail -f .sync_queue.json

# 查看错误信息
python3 scripts/sync_progress.py sync 2>&1 | tee sync.log
```

## 📈 最佳实践

### 1. 进度记录建议

- **描述要具体**：避免"完成了工作"这样的模糊描述
- **附注要详细**：记录遇到的问题和解决方案
- **定期更新**：建议每天或每个重要节点更新进度

### 2. 项目管理建议

- **合理分类**：按大项目分类管理
- **目标明确**：设置清晰的开发目标
- **及时同步**：定期同步到中央仓库

### 3. 团队协作

- **统一格式**：团队成员使用相同的进度格式
- **定期回顾**：定期查看项目进度和成果
- **文档维护**：及时更新项目文档

## 🆘 技术支持

如果遇到问题，请：

1. 查看本文档的故障排除部分
2. 检查GitHub Issues
3. 提交新的Issue并附上详细信息

## 📝 更新日志

### v1.0.0 (2024-01-16)
- 初始版本发布
- 支持基本的进度管理功能
- 支持GitHub Pages展示
- 支持实时和定时同步
