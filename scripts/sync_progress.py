#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
进度同步脚本 - 与GitHub中央仓库同步
支持实时同步和定时同步两种模式
"""

import os
import json
import subprocess
import requests
import time
from datetime import datetime
from pathlib import Path
import argparse

class ProgressSync:
    def __init__(self):
        self.config_file = ".progress_config.json"
        self.central_repo_url = "https://github.com/ariusewy/ProgressReport"
        self.local_repo_dir = ".progress_repo"
        
    def sync_to_central(self, force=False):
        """同步到中央仓库"""
        try:
            # 读取配置
            config = self._load_config()
            if not config:
                return False
            
            # 检查网络连接
            if not self._check_network():
                print("⚠️ 网络连接不可用，将使用离线模式")
                return self._queue_sync(config)
            
            # 克隆或更新中央仓库
            if not self._setup_central_repo():
                return False
            
            # 复制进度文件
            progress_file = f"{config['project_id']}_progress.json"
            if os.path.exists(progress_file):
                self._copy_progress_file(progress_file, config)
            
            # 提交并推送
            if self._commit_and_push(config):
                print("✅ 同步成功！")
                # 更新最后同步时间
                config['last_sync'] = datetime.now().isoformat()
                self._save_config(config)
                return True
            else:
                print("❌ 同步失败")
                return False
                
        except Exception as e:
            print(f"❌ 同步失败: {e}")
            return False
    
    def sync_from_central(self):
        """从中央仓库同步"""
        try:
            # 读取配置
            config = self._load_config()
            if not config:
                return False
            
            # 检查网络连接
            if not self._check_network():
                print("⚠️ 网络连接不可用")
                return False
            
            # 克隆或更新中央仓库
            if not self._setup_central_repo():
                return False
            
            # 复制进度文件到本地
            progress_file = f"{config['project_id']}_progress.json"
            central_progress_file = os.path.join(self.local_repo_dir, "projects", progress_file)
            
            if os.path.exists(central_progress_file):
                self._copy_from_central(central_progress_file, progress_file)
                print("✅ 从中央仓库同步成功！")
                return True
            else:
                print("📭 中央仓库中未找到进度文件")
                return False
                
        except Exception as e:
            print(f"❌ 从中央仓库同步失败: {e}")
            return False
    
    def _load_config(self):
        """加载项目配置"""
        if not os.path.exists(self.config_file):
            print(f"❌ 配置文件 {self.config_file} 不存在")
            return None
        
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"❌ 读取配置文件失败: {e}")
            return None
    
    def _save_config(self, config):
        """保存项目配置"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"❌ 保存配置文件失败: {e}")
    
    def _check_network(self):
        """检查网络连接"""
        try:
            response = requests.get("https://api.github.com", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def _setup_central_repo(self):
        """设置中央仓库"""
        try:
            if not os.path.exists(self.local_repo_dir):
                # 克隆仓库
                print(f"📥 克隆中央仓库...")
                result = subprocess.run([
                    "git", "clone", self.central_repo_url, self.local_repo_dir
                ], capture_output=True, text=True)
                
                if result.returncode != 0:
                    print(f"❌ 克隆仓库失败: {result.stderr}")
                    return False
            else:
                # 更新仓库
                print(f"🔄 更新中央仓库...")
                os.chdir(self.local_repo_dir)
                result = subprocess.run(["git", "pull"], capture_output=True, text=True)
                os.chdir("..")
                
                if result.returncode != 0:
                    print(f"❌ 更新仓库失败: {result.stderr}")
                    return False
            
            # 确保projects目录存在
            projects_dir = os.path.join(self.local_repo_dir, "projects")
            os.makedirs(projects_dir, exist_ok=True)
            
            return True
            
        except Exception as e:
            print(f"❌ 设置中央仓库失败: {e}")
            return False
    
    def _copy_progress_file(self, progress_file, config):
        """复制进度文件到中央仓库"""
        try:
            source_file = progress_file
            target_file = os.path.join(self.local_repo_dir, "projects", progress_file)
            
            if os.path.exists(source_file):
                # 读取源文件
                with open(source_file, 'r', encoding='utf-8') as f:
                    progress_data = json.load(f)
                
                # 写入目标文件
                with open(target_file, 'w', encoding='utf-8') as f:
                    json.dump(progress_data, f, indent=2, ensure_ascii=False)
                
                print(f"📁 复制进度文件: {progress_file}")
                return True
            else:
                print(f"⚠️ 进度文件不存在: {progress_file}")
                return False
                
        except Exception as e:
            print(f"❌ 复制进度文件失败: {e}")
            return False
    
    def _copy_from_central(self, source_file, target_file):
        """从中央仓库复制进度文件"""
        try:
            if os.path.exists(source_file):
                # 读取源文件
                with open(source_file, 'r', encoding='utf-8') as f:
                    progress_data = json.load(f)
                
                # 写入目标文件
                with open(target_file, 'w', encoding='utf-8') as f:
                    json.dump(progress_data, f, indent=2, ensure_ascii=False)
                
                print(f"📁 从中央仓库复制进度文件: {target_file}")
                return True
            else:
                print(f"⚠️ 中央仓库中进度文件不存在: {source_file}")
                return False
                
        except Exception as e:
            print(f"❌ 从中央仓库复制进度文件失败: {e}")
            return False
    
    def _commit_and_push(self, config):
        """提交并推送到中央仓库"""
        try:
            os.chdir(self.local_repo_dir)
            
            # 添加文件
            result = subprocess.run(["git", "add", "."], capture_output=True, text=True)
            if result.returncode != 0:
                print(f"❌ Git add失败: {result.stderr}")
                return False
            
            # 检查是否有变更
            result = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True)
            if not result.stdout.strip():
                print("📭 没有变更需要提交")
                return True
            
            # 提交
            commit_message = f"Update progress for {config['project_name']} - {datetime.now().strftime('%Y-%m-%d %H:%M')}"
            result = subprocess.run([
                "git", "commit", "-m", commit_message
            ], capture_output=True, text=True)
            
            if result.returncode != 0:
                print(f"❌ Git commit失败: {result.stderr}")
                return False
            
            # 推送
            result = subprocess.run(["git", "push"], capture_output=True, text=True)
            if result.returncode != 0:
                print(f"❌ Git push失败: {result.stderr}")
                return False
            
            os.chdir("..")
            return True
            
        except Exception as e:
            print(f"❌ 提交推送失败: {e}")
            os.chdir("..")
            return False
    
    def _queue_sync(self, config):
        """队列同步（离线模式）"""
        try:
            queue_file = ".sync_queue.json"
            queue_data = []
            
            if os.path.exists(queue_file):
                with open(queue_file, 'r', encoding='utf-8') as f:
                    queue_data = json.load(f)
            
            # 添加同步任务
            sync_task = {
                "project_id": config["project_id"],
                "project_name": config["project_name"],
                "timestamp": datetime.now().isoformat(),
                "progress_file": f"{config['project_id']}_progress.json"
            }
            
            queue_data.append(sync_task)
            
            # 保存队列
            with open(queue_file, 'w', encoding='utf-8') as f:
                json.dump(queue_data, f, indent=2, ensure_ascii=False)
            
            print(f"📋 同步任务已加入队列，共 {len(queue_data)} 个待同步任务")
            return True
            
        except Exception as e:
            print(f"❌ 加入同步队列失败: {e}")
            return False
    
    def process_sync_queue(self):
        """处理同步队列"""
        try:
            queue_file = ".sync_queue.json"
            if not os.path.exists(queue_file):
                print("📭 没有待处理的同步任务")
                return True
            
            with open(queue_file, 'r', encoding='utf-8') as f:
                queue_data = json.load(f)
            
            if not queue_data:
                print("📭 没有待处理的同步任务")
                return True
            
            print(f"🔄 处理 {len(queue_data)} 个同步任务...")
            
            # 检查网络连接
            if not self._check_network():
                print("⚠️ 网络连接不可用，跳过队列处理")
                return False
            
            # 设置中央仓库
            if not self._setup_central_repo():
                return False
            
            # 处理每个任务
            processed_tasks = []
            for task in queue_data:
                progress_file = task["progress_file"]
                if os.path.exists(progress_file):
                    config = self._load_config()
                    if config and config["project_id"] == task["project_id"]:
                        if self._copy_progress_file(progress_file, config):
                            processed_tasks.append(task)
                            print(f"✅ 处理同步任务: {task['project_name']}")
                        else:
                            print(f"❌ 处理同步任务失败: {task['project_name']}")
                else:
                    print(f"⚠️ 进度文件不存在: {progress_file}")
            
            # 提交并推送
            if processed_tasks and self._commit_and_push(config):
                # 移除已处理的任务
                remaining_tasks = [task for task in queue_data if task not in processed_tasks]
                with open(queue_file, 'w', encoding='utf-8') as f:
                    json.dump(remaining_tasks, f, indent=2, ensure_ascii=False)
                
                print(f"✅ 成功处理 {len(processed_tasks)} 个同步任务")
                return True
            else:
                print("❌ 处理同步队列失败")
                return False
                
        except Exception as e:
            print(f"❌ 处理同步队列失败: {e}")
            return False

def main():
    parser = argparse.ArgumentParser(description="进度同步脚本")
    subparsers = parser.add_subparsers(dest='command', help='可用命令')
    
    # 同步到中央仓库
    sync_parser = subparsers.add_parser('sync', help='同步到中央仓库')
    sync_parser.add_argument('--force', action='store_true', help='强制同步')
    
    # 从中央仓库同步
    pull_parser = subparsers.add_parser('pull', help='从中央仓库同步')
    
    # 处理同步队列
    queue_parser = subparsers.add_parser('queue', help='处理同步队列')
    
    args = parser.parse_args()
    
    sync = ProgressSync()
    
    if args.command == 'sync':
        sync.sync_to_central(force=args.force)
    elif args.command == 'pull':
        sync.sync_from_central()
    elif args.command == 'queue':
        sync.process_sync_queue()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
