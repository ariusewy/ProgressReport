#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
个人项目进度管理系统 - 核心管理脚本
支持分布式项目进度管理，自动同步到GitHub
"""

import os
import json
import sys
import time
import uuid
import subprocess
import requests
from datetime import datetime
from pathlib import Path
import argparse

class ProgressManager:
    def __init__(self):
        self.config_file = ".progress_config.json"
        self.central_repo_url = "https://github.com/ariusewy/ProgressReport"
        self.projects_dir = "projects"
        
    def init_project(self, project_name, parent_project, development_goal):
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
                "central_repo_url": self.central_repo_url,
                "last_sync": datetime.now().isoformat(),
                "sync_mode": "realtime"
            }
            
            # 保存配置文件
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            
            # 创建本地更新脚本
            self._create_local_script()
            
            print(f"✅ 项目 '{project_name}' 初始化成功！")
            print(f"📁 配置文件: {self.config_file}")
            print(f"🆔 项目ID: {project_id}")
            print(f"📊 隶属大项目: {parent_project}")
            print(f"🎯 开发目标: {development_goal}")
            
            return True
            
        except Exception as e:
            print(f"❌ 项目初始化失败: {e}")
            return False
    
    def add_progress(self, description, notes=""):
        """添加进度条目"""
        try:
            # 读取配置
            config = self._load_config()
            if not config:
                return False
            
            # 创建进度条目
            progress_entry = {
                "date": datetime.now().strftime("%Y-%m-%d"),
                "time": datetime.now().strftime("%H:%M"),
                "description": description,
                "notes": notes,
                "tags": []
            }
            
            # 读取或创建进度文件
            progress_file = f"{config['project_id']}_progress.json"
            progress_data = self._load_progress(progress_file)
            
            if not progress_data:
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
            self._save_progress(progress_file, progress_data)
            
            print(f"✅ 进度添加成功！")
            print(f"📅 日期: {progress_entry['date']}")
            print(f"⏰ 时间: {progress_entry['time']}")
            print(f"📝 描述: {description}")
            if notes:
                print(f"📌 附注: {notes}")
            
            # 尝试同步到中央仓库
            self._sync_to_central(progress_file, progress_data)
            
            return True
            
        except Exception as e:
            print(f"❌ 添加进度失败: {e}")
            return False
    
    def show_progress(self):
        """显示项目进度"""
        try:
            config = self._load_config()
            if not config:
                return False
            
            progress_file = f"{config['project_id']}_progress.json"
            progress_data = self._load_progress(progress_file)
            
            if not progress_data:
                print("📭 暂无进度记录")
                return True
            
            print(f"\n📊 项目进度: {progress_data['project_name']}")
            print(f"🏷️ 隶属大项目: {progress_data['parent_project']}")
            print(f"🎯 开发目标: {progress_data['development_goal']}")
            print(f"📅 创建日期: {progress_data['created_date']}")
            print(f"🔄 最后更新: {progress_data['last_updated']}")
            print(f"\n📝 进度记录 ({len(progress_data['progress_entries'])} 条):")
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
    
    def _load_config(self):
        """加载项目配置"""
        if not os.path.exists(self.config_file):
            print(f"❌ 配置文件 {self.config_file} 不存在")
            print("请先运行: python progress_manager.py init <项目名> <大项目> <开发目标>")
            return None
        
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"❌ 读取配置文件失败: {e}")
            return None
    
    def _load_progress(self, progress_file):
        """加载进度文件"""
        if os.path.exists(progress_file):
            try:
                with open(progress_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"⚠️ 读取进度文件失败: {e}")
        return None
    
    def _save_progress(self, progress_file, progress_data):
        """保存进度文件"""
        try:
            with open(progress_file, 'w', encoding='utf-8') as f:
                json.dump(progress_data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"❌ 保存进度文件失败: {e}")
            raise
    
    def _create_local_script(self):
        """创建本地更新脚本"""
        script_content = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
本地进度更新脚本
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'scripts'))
from progress_manager import ProgressManager

if __name__ == "__main__":
    manager = ProgressManager()
    if len(sys.argv) < 2:
        print("用法: python progress_update.py <进度描述> [附注]")
        sys.exit(1)
    
    description = sys.argv[1]
    notes = sys.argv[2] if len(sys.argv) > 2 else ""
    
    manager.add_progress(description, notes)
'''
        
        with open("progress_update.py", 'w', encoding='utf-8') as f:
            f.write(script_content)
        
        # 设置执行权限
        os.chmod("progress_update.py", 0o755)
    
    def _sync_to_central(self, progress_file, progress_data):
        """同步到中央仓库"""
        try:
            # 这里应该实现与GitHub的同步逻辑
            # 暂时只是打印信息
            print(f"🔄 尝试同步到中央仓库...")
            print(f"📁 进度文件: {progress_file}")
            print(f"📊 条目数量: {len(progress_data['progress_entries'])}")
            
            # TODO: 实现实际的GitHub同步
            # 1. 克隆中央仓库
            # 2. 更新进度文件
            # 3. 提交并推送
            
        except Exception as e:
            print(f"⚠️ 同步失败: {e}")

def main():
    parser = argparse.ArgumentParser(description="个人项目进度管理系统")
    subparsers = parser.add_subparsers(dest='command', help='可用命令')
    
    # 初始化项目命令
    init_parser = subparsers.add_parser('init', help='初始化项目')
    init_parser.add_argument('project_name', help='项目名称')
    init_parser.add_argument('parent_project', help='隶属大项目')
    init_parser.add_argument('development_goal', help='开发目标')
    
    # 添加进度命令
    add_parser = subparsers.add_parser('add', help='添加进度')
    add_parser.add_argument('description', help='进度描述')
    add_parser.add_argument('notes', nargs='?', default='', help='附注')
    
    # 显示进度命令
    show_parser = subparsers.add_parser('show', help='显示进度')
    
    args = parser.parse_args()
    
    manager = ProgressManager()
    
    if args.command == 'init':
        manager.init_project(args.project_name, args.parent_project, args.development_goal)
    elif args.command == 'add':
        manager.add_progress(args.description, args.notes)
    elif args.command == 'show':
        manager.show_progress()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
