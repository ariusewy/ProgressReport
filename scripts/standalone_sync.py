#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
独立同步脚本 - 可以从任何目录运行，无需本地ProgressReport仓库
"""

import os
import json
import subprocess
import requests
import tempfile
import shutil
from datetime import datetime
from pathlib import Path
import argparse

class StandaloneProgressSync:
    def __init__(self):
        self.config_file = ".progress_config.json"
        self.central_repo_url = "https://github.com/ariusewy/ProgressReport"
        self.temp_dir = None
        
    def sync_to_central(self):
        """同步到中央仓库"""
        try:
            # 读取配置
            config = self._load_config()
            if not config:
                return False
            
            # 检查网络连接
            if not self._check_network():
                print("⚠️ 网络连接不可用")
                return False
            
            # 创建临时目录
            self.temp_dir = tempfile.mkdtemp()
            
            try:
                # 克隆中央仓库到临时目录
                if not self._clone_central_repo():
                    return False
                
                # 复制进度文件
                progress_file = f"{config['project_id']}_progress.json"
                if os.path.exists(progress_file):
                    self._copy_progress_file(progress_file)
                
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
                    
            finally:
                # 清理临时目录
                if self.temp_dir and os.path.exists(self.temp_dir):
                    shutil.rmtree(self.temp_dir)
                    
        except Exception as e:
            print(f"❌ 同步失败: {e}")
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
            print(f"⚠️ 保存配置文件失败: {e}")
    
    def _check_network(self):
        """检查网络连接"""
        try:
            response = requests.get("https://github.com", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def _clone_central_repo(self):
        """克隆中央仓库到临时目录"""
        try:
            print("📥 克隆中央仓库...")
            repo_dir = os.path.join(self.temp_dir, "ProgressReport")
            
            # 检查是否已经存在
            if os.path.exists(repo_dir):
                # 更新现有仓库
                subprocess.run(["git", "pull"], cwd=repo_dir, check=True, capture_output=True)
            else:
                # 克隆新仓库
                subprocess.run(["git", "clone", self.central_repo_url, repo_dir], check=True, capture_output=True)
            
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ 克隆仓库失败: {e}")
            return False
    
    def _copy_progress_file(self, progress_file):
        """复制进度文件到中央仓库"""
        try:
            source_file = progress_file
            target_dir = os.path.join(self.temp_dir, "ProgressReport", "projects")
            target_file = os.path.join(target_dir, progress_file)
            
            # 确保目标目录存在
            os.makedirs(target_dir, exist_ok=True)
            
            # 复制文件
            shutil.copy2(source_file, target_file)
            print(f"📁 复制进度文件: {progress_file}")
            return True
        except Exception as e:
            print(f"❌ 复制文件失败: {e}")
            return False
    
    def _commit_and_push(self, config):
        """提交并推送更改"""
        try:
            repo_dir = os.path.join(self.temp_dir, "ProgressReport")
            
            # 添加文件
            subprocess.run(["git", "add", "."], cwd=repo_dir, check=True, capture_output=True)
            
            # 检查是否有更改
            result = subprocess.run(["git", "status", "--porcelain"], cwd=repo_dir, capture_output=True, text=True)
            if not result.stdout.strip():
                print("📭 没有更改需要提交")
                return True
            
            # 提交更改
            commit_message = f"Update progress for {config['project_name']} ({config['project_id']})"
            subprocess.run(["git", "commit", "-m", commit_message], cwd=repo_dir, check=True, capture_output=True)
            
            # 推送到远程仓库
            subprocess.run(["git", "push"], cwd=repo_dir, check=True, capture_output=True)
            
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ 提交推送失败: {e}")
            return False

def main():
    parser = argparse.ArgumentParser(description='独立进度同步脚本')
    parser.add_argument('action', choices=['sync'], help='同步操作')
    
    args = parser.parse_args()
    
    if args.action == 'sync':
        syncer = StandaloneProgressSync()
        syncer.sync_to_central()
    else:
        print("用法: python3 standalone_sync.py sync")

if __name__ == "__main__":
    main()
