#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
项目初始化脚本 - 在项目目录下快速初始化进度管理
"""

import os
import sys
import json
import uuid
from datetime import datetime
from pathlib import Path

def init_project(project_name, parent_project, development_goal):
    """初始化项目进度管理"""
    try:
        # 生成项目ID
        project_id = str(uuid.uuid4())[:8]
        
        # 创建配置文件
        config = {
            "project_id": project_id,
            "project_name": project_name,
            "parent_project": parent_project,
            "development_goal": development_goal,
            "project_path": str(Path.cwd()),
            "central_repo_url": "https://github.com/ariusewy/ProgressReport",
            "last_sync": datetime.now().isoformat(),
            "sync_mode": "realtime"
        }
        
        # 保存配置文件
        config_file = ".progress_config.json"
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        
        # 创建进度文件
        progress_file = f"{project_id}_progress.json"
        progress_data = {
            "project_name": project_name,
            "parent_project": parent_project,
            "development_goal": development_goal,
            "created_date": datetime.now().strftime("%Y-%m-%d"),
            "last_updated": datetime.now().isoformat(),
            "progress_entries": []
        }
        
        with open(progress_file, 'w', encoding='utf-8') as f:
            json.dump(progress_data, f, indent=2, ensure_ascii=False)
        
        # 创建本地更新脚本
        create_local_script()
        
        print(f"✅ 项目 '{project_name}' 初始化成功！")
        print(f"📁 配置文件: {config_file}")
        print(f"📊 进度文件: {progress_file}")
        print(f"🆔 项目ID: {project_id}")
        print(f"📊 隶属大项目: {parent_project}")
        print(f"🎯 开发目标: {development_goal}")
        print(f"\n🚀 使用方法:")
        print(f"   python progress_update.py \"进度描述\" \"附注\"")
        print(f"   python progress_update.py --show")
        
        return True
        
    except Exception as e:
        print(f"❌ 项目初始化失败: {e}")
        return False

def create_local_script():
    """创建本地更新脚本"""
    script_content = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
本地进度更新脚本
"""

import sys
import os
import json
from datetime import datetime

def add_progress(description, notes=""):
    """添加进度条目"""
    try:
        # 读取配置
        config_file = ".progress_config.json"
        if not os.path.exists(config_file):
            print("❌ 配置文件不存在，请先运行初始化")
            return False
        
        with open(config_file, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        # 创建进度条目
        progress_entry = {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "time": datetime.now().strftime("%H:%M"),
            "description": description,
            "notes": notes,
            "tags": []
        }
        
        # 读取进度文件
        progress_file = f"{config['project_id']}_progress.json"
        if os.path.exists(progress_file):
            with open(progress_file, 'r', encoding='utf-8') as f:
                progress_data = json.load(f)
        else:
            progress_data = {
                "project_name": config["project_name"],
                "parent_project": config["parent_project"],
                "development_goal": config["development_goal"],
                "created_date": datetime.now().strftime("%Y-%m-%d"),
                "last_updated": datetime.now().isoformat(),
                "progress_entries": []
            }
        
        # 添加新条目
        progress_data["progress_entries"].append(progress_entry)
        progress_data["last_updated"] = datetime.now().isoformat()
        
        # 保存进度文件
        with open(progress_file, 'w', encoding='utf-8') as f:
            json.dump(progress_data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ 进度添加成功！")
        print(f"📅 日期: {progress_entry['date']}")
        print(f"⏰ 时间: {progress_entry['time']}")
        print(f"📝 描述: {description}")
        if notes:
            print(f"📌 附注: {notes}")
        
        return True
        
    except Exception as e:
        print(f"❌ 添加进度失败: {e}")
        return False

def show_progress():
    """显示项目进度"""
    try:
        # 读取配置
        config_file = ".progress_config.json"
        if not os.path.exists(config_file):
            print("❌ 配置文件不存在")
            return False
        
        with open(config_file, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        # 读取进度文件
        progress_file = f"{config['project_id']}_progress.json"
        if not os.path.exists(progress_file):
            print("📭 暂无进度记录")
            return True
        
        with open(progress_file, 'r', encoding='utf-8') as f:
            progress_data = json.load(f)
        
        print(f"\\n📊 项目进度: {progress_data['project_name']}")
        print(f"🏷️ 隶属大项目: {progress_data['parent_project']}")
        print(f"🎯 开发目标: {progress_data['development_goal']}")
        print(f"📅 创建日期: {progress_data['created_date']}")
        print(f"🔄 最后更新: {progress_data['last_updated']}")
        print(f"\\n📝 进度记录 ({len(progress_data['progress_entries'])} 条):")
        print("-" * 80)
        
        for entry in reversed(progress_data['progress_entries']):
            print(f"📅 {entry['date']} {entry['time']}")
            print(f"   📝 {entry['description']}")
            if entry['notes']:
                print(f"   📌 {entry['notes']}")
            print()
        
        return True
        
    except Exception as e:
        print(f"❌ 显示进度失败: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python progress_update.py <进度描述> [附注]")
        print("      python progress_update.py --show")
        sys.exit(1)
    
    if sys.argv[1] == "--show":
        show_progress()
    else:
        description = sys.argv[1]
        notes = sys.argv[2] if len(sys.argv) > 2 else ""
        add_progress(description, notes)
'''
    
    with open("progress_update.py", 'w', encoding='utf-8') as f:
        f.write(script_content)
    
    # 设置执行权限
    os.chmod("progress_update.py", 0o755)

def main():
    if len(sys.argv) != 4:
        print("用法: python init_project.py <项目名称> <隶属大项目> <开发目标>")
        print("示例: python init_project.py \"机器学习项目\" \"AI研究\" \"实现图像分类算法\"")
        sys.exit(1)
    
    project_name = sys.argv[1]
    parent_project = sys.argv[2]
    development_goal = sys.argv[3]
    
    init_project(project_name, parent_project, development_goal)

if __name__ == "__main__":
    main()
