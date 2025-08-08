#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GitHub Pages生成脚本 - 自动生成进度展示页面
"""

import os
import json
import glob
from datetime import datetime, timedelta
from pathlib import Path
import calendar

class PagesGenerator:
    def __init__(self):
        self.projects_dir = "projects"
        self.pages_dir = "pages"
        self.template_dir = "templates"
        
        # 语言配置
        self.languages = {
            'zh': {
                'title': '个人项目进度管理系统',
                'subtitle': '管理你的研究项目进度，追踪开发历程',
                'home': '🏠 主页',
                'timeline': '📅 时间线',
                'projects': '📁 项目列表',
                'daily_view': '📅 日视图',
                'weekly_view': '📅 周视图',
                'monthly_view': '📅 月视图',
                'active_projects': '活跃项目',
                'total_entries': '总进度条目',
                'project_categories': '大项目分类',
                'back_to_home': '← 返回主页',
                'project_list_title': '📁 项目列表',
                'project_list_subtitle': '查看所有项目的详细信息和进度',
                'timeline_title': '📅 项目进度时间线',
                'timeline_subtitle': '按时间顺序查看所有项目进度',
                'daily_view_title': '📅 日视图',
                'daily_view_subtitle': '查看指定日期的项目进度',
                'weekly_view_title': '📅 周视图',
                'weekly_view_subtitle': '查看指定周的项目进度',
                'monthly_view_title': '📅 月视图',
                'monthly_view_subtitle': '查看指定月的项目进度',
                'no_projects': '📭 暂无项目',
                'no_projects_desc': '还没有创建任何项目，请先初始化一个项目。',
                'no_progress': '暂无进度记录',
                'progress_entries': '进度条目',
                'created_date': '创建日期',
                'parent_project': '隶属大项目',
                'development_goal': '开发目标',
                'last_updated': '最后更新',
                'progress_records': '进度记录',
                'date': '日期',
                'time': '时间',
                'description': '描述',
                'notes': '附注',
                'today': '今天',
                'yesterday': '昨天',
                'tomorrow': '明天',
                'previous': '上一',
                'next': '下一',
                'week': '周',
                'month': '月',
                'year': '年'
            },
            'en': {
                'title': 'Personal Project Progress Management System',
                'subtitle': 'Manage your research project progress and track development history',
                'home': '🏠 Home',
                'timeline': '📅 Timeline',
                'projects': '📁 Projects',
                'daily_view': '📅 Daily View',
                'weekly_view': '📅 Weekly View',
                'monthly_view': '📅 Monthly View',
                'active_projects': 'Active Projects',
                'total_entries': 'Total Progress Entries',
                'project_categories': 'Project Categories',
                'back_to_home': '← Back to Home',
                'project_list_title': '📁 Project List',
                'project_list_subtitle': 'View detailed information and progress of all projects',
                'timeline_title': '📅 Project Progress Timeline',
                'timeline_subtitle': 'View all project progress in chronological order',
                'daily_view_title': '📅 Daily View',
                'daily_view_subtitle': 'View project progress for a specific date',
                'weekly_view_title': '📅 Weekly View',
                'weekly_view_subtitle': 'View project progress for a specific week',
                'monthly_view_title': '📅 Monthly View',
                'monthly_view_subtitle': 'View project progress for a specific month',
                'no_projects': '📭 No Projects',
                'no_projects_desc': 'No projects have been created yet. Please initialize a project first.',
                'no_progress': 'No progress records',
                'progress_entries': 'Progress Entries',
                'created_date': 'Created Date',
                'parent_project': 'Parent Project',
                'development_goal': 'Development Goal',
                'last_updated': 'Last Updated',
                'progress_records': 'Progress Records',
                'date': 'Date',
                'time': 'Time',
                'description': 'Description',
                'notes': 'Notes',
                'today': 'Today',
                'yesterday': 'Yesterday',
                'tomorrow': 'Tomorrow',
                'previous': 'Previous',
                'next': 'Next',
                'week': 'Week',
                'month': 'Month',
                'year': 'Year'
            }
        }
        
    def generate_pages(self):
        """生成所有页面"""
        try:
            # 确保目录存在
            os.makedirs(self.pages_dir, exist_ok=True)
            
            # 读取所有项目进度
            projects_data = self._load_all_projects()
            
            # 生成主页
            self._generate_main_page(projects_data)
            
            # 生成项目页面
            self._generate_project_pages(projects_data)
            
            # 生成项目列表页面
            self._generate_projects_list_page(projects_data)
            
            # 生成时间线页面
            self._generate_timeline_page(projects_data)
            
            # 生成日视图页面
            self._generate_daily_view_page(projects_data)
            
            # 生成周视图页面
            self._generate_weekly_view_page(projects_data)
            
            # 生成月视图页面
            self._generate_monthly_view_page(projects_data)
            
            print("✅ 页面生成完成！")
            return True
            
        except Exception as e:
            print(f"❌ 页面生成失败: {e}")
            return False
    
    def _load_all_projects(self):
        """加载所有项目数据"""
        projects_data = []
        
        if not os.path.exists(self.projects_dir):
            return projects_data
        
        # 查找所有进度文件
        progress_files = glob.glob(os.path.join(self.projects_dir, "*_progress.json"))
        
        for progress_file in progress_files:
            try:
                with open(progress_file, 'r', encoding='utf-8') as f:
                    project_data = json.load(f)
                    projects_data.append(project_data)
            except Exception as e:
                print(f"⚠️ 读取进度文件失败 {progress_file}: {e}")
        
        return projects_data
    
    def _get_language_script(self):
        """获取语言切换的JavaScript代码"""
        return """
        <script>
        // 语言切换功能
        let currentLang = localStorage.getItem('language') || 'zh';
        
        function switchLanguage(lang) {
            currentLang = lang;
            localStorage.setItem('language', lang);
            updatePageLanguage();
        }
        
        function updatePageLanguage() {
            const elements = document.querySelectorAll('[data-lang]');
            elements.forEach(element => {
                const key = element.getAttribute('data-lang');
                const translations = {
                    'zh': {
                        'title': '个人项目进度管理系统',
                        'subtitle': '管理你的研究项目进度，追踪开发历程',
                        'home': '🏠 主页',
                        'timeline': '📅 时间线',
                        'projects': '📁 项目列表',
                        'daily_view': '📅 日视图',
                        'weekly_view': '📅 周视图',
                        'monthly_view': '📅 月视图',
                        'active_projects': '活跃项目',
                        'total_entries': '总进度条目',
                        'project_categories': '大项目分类',
                        'back_to_home': '← 返回主页',
                        'project_list_title': '📁 项目列表',
                        'project_list_subtitle': '查看所有项目的详细信息和进度',
                        'timeline_title': '📅 项目进度时间线',
                        'timeline_subtitle': '按时间顺序查看所有项目进度',
                        'daily_view_title': '📅 日视图',
                        'daily_view_subtitle': '查看指定日期的项目进度',
                        'weekly_view_title': '📅 周视图',
                        'weekly_view_subtitle': '查看指定周的项目进度',
                        'monthly_view_title': '📅 月视图',
                        'monthly_view_subtitle': '查看指定月的项目进度',
                        'no_projects': '📭 暂无项目',
                        'no_projects_desc': '还没有创建任何项目，请先初始化一个项目。',
                        'no_progress': '暂无进度记录',
                        'progress_entries': '进度条目',
                        'created_date': '创建日期',
                        'parent_project': '隶属大项目',
                        'development_goal': '开发目标',
                        'last_updated': '最后更新',
                        'progress_records': '进度记录',
                        'date': '日期',
                        'time': '时间',
                        'description': '描述',
                        'notes': '附注',
                        'today': '今天',
                        'yesterday': '昨天',
                        'tomorrow': '明天',
                        'previous': '上一',
                        'next': '下一',
                        'week': '周',
                        'month': '月',
                        'year': '年'
                    },
                    'en': {
                        'title': 'Personal Project Progress Management System',
                        'subtitle': 'Manage your research project progress and track development history',
                        'home': '🏠 Home',
                        'timeline': '📅 Timeline',
                        'projects': '📁 Projects',
                        'daily_view': '📅 Daily View',
                        'weekly_view': '📅 Weekly View',
                        'monthly_view': '📅 Monthly View',
                        'active_projects': 'Active Projects',
                        'total_entries': 'Total Progress Entries',
                        'project_categories': 'Project Categories',
                        'back_to_home': '← Back to Home',
                        'project_list_title': '📁 Project List',
                        'project_list_subtitle': 'View detailed information and progress of all projects',
                        'timeline_title': '📅 Project Progress Timeline',
                        'timeline_subtitle': 'View all project progress in chronological order',
                        'daily_view_title': '📅 Daily View',
                        'daily_view_subtitle': 'View project progress for a specific date',
                        'weekly_view_title': '📅 Weekly View',
                        'weekly_view_subtitle': 'View project progress for a specific week',
                        'monthly_view_title': '📅 Monthly View',
                        'monthly_view_subtitle': 'View project progress for a specific month',
                        'no_projects': '📭 No Projects',
                        'no_projects_desc': 'No projects have been created yet. Please initialize a project first.',
                        'no_progress': 'No progress records',
                        'progress_entries': 'Progress Entries',
                        'created_date': 'Created Date',
                        'parent_project': 'Parent Project',
                        'development_goal': 'Development Goal',
                        'last_updated': 'Last Updated',
                        'progress_records': 'Progress Records',
                        'date': 'Date',
                        'time': 'Time',
                        'description': 'Description',
                        'notes': 'Notes',
                        'today': 'Today',
                        'yesterday': 'Yesterday',
                        'tomorrow': 'Tomorrow',
                        'previous': 'Previous',
                        'next': 'Next',
                        'week': 'Week',
                        'month': 'Month',
                        'year': 'Year'
                    }
                };
                
                if (translations[currentLang] && translations[currentLang][key]) {
                    element.textContent = translations[currentLang][key];
                }
            });
            
            // 更新语言切换器状态
            const buttons = document.querySelectorAll('.language-switcher button');
            buttons.forEach(button => {
                button.classList.remove('active');
                if (button.textContent.includes('中文') && currentLang === 'zh') {
                    button.classList.add('active');
                } else if (button.textContent.includes('English') && currentLang === 'en') {
                    button.classList.add('active');
                }
            });
        }
        
        // 页面加载时应用语言设置
        document.addEventListener('DOMContentLoaded', function() {
            updatePageLanguage();
        });
        </script>
        """
    
    def _get_language_switcher_css(self):
        """获取语言切换器的CSS样式"""
        return """
        .language-switcher {
            position: fixed;
            top: 20px;
            right: 20px;
            background: white;
            border-radius: 25px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            padding: 8px;
            z-index: 1000;
        }
        
        .language-switcher button {
            background: none;
            border: none;
            padding: 8px 16px;
            border-radius: 20px;
            cursor: pointer;
            font-weight: 500;
            transition: all 0.3s ease;
            margin: 0 2px;
        }
        
        .language-switcher button.active {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }
        
        .language-switcher button:hover {
            background: #f0f0f0;
        }
        
        .language-switcher button.active:hover {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }
        """
    
    def _generate_main_page(self, projects_data):
        """生成主页"""
        html_content = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title data-lang="title">个人项目进度管理系统</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.6;
            color: #333;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 2rem;
        }}
        
        .header {{
            text-align: center;
            color: white;
            margin-bottom: 3rem;
        }}
        
        .header h1 {{
            font-size: 2.5rem;
            margin-bottom: 1rem;
        }}
        
        .header p {{
            font-size: 1.2rem;
            opacity: 0.9;
        }}
        
        .stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1.5rem;
            margin-bottom: 3rem;
        }}
        
        .stat-card {{
            background: white;
            padding: 1.5rem;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            text-align: center;
        }}
        
        .stat-number {{
            font-size: 2rem;
            font-weight: bold;
            color: #667eea;
        }}
        
        .stat-label {{
            color: #666;
            margin-top: 0.5rem;
        }}
        
        .projects-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 1.5rem;
        }}
        
        .project-card {{
            background: white;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            overflow: hidden;
            transition: transform 0.3s ease;
        }}
        
        .project-card:hover {{
            transform: translateY(-5px);
        }}
        
        .project-header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 1.5rem;
        }}
        
        .project-name {{
            font-size: 1.3rem;
            font-weight: bold;
            margin-bottom: 0.5rem;
        }}
        
        .project-parent {{
            opacity: 0.9;
            font-size: 0.9rem;
        }}
        
        .project-body {{
            padding: 1.5rem;
        }}
        
        .project-goal {{
            color: #666;
            margin-bottom: 1rem;
        }}
        
        .project-stats {{
            display: flex;
            justify-content: space-between;
            margin-bottom: 1rem;
        }}
        
        .project-stat {{
            text-align: center;
        }}
        
        .project-stat-number {{
            font-weight: bold;
            color: #667eea;
        }}
        
        .project-stat-label {{
            font-size: 0.8rem;
            color: #666;
        }}
        
        .latest-progress {{
            background: #f8f9fa;
            padding: 1rem;
            border-radius: 5px;
            border-left: 4px solid #667eea;
        }}
        
        .progress-date {{
            font-size: 0.8rem;
            color: #666;
            margin-bottom: 0.5rem;
        }}
        
        .progress-description {{
            font-weight: 500;
        }}
        
        .nav {{
            background: white;
            padding: 1rem 2rem;
            margin-bottom: 2rem;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }}
        
        .nav a {{
            color: #667eea;
            text-decoration: none;
            margin-right: 2rem;
            font-weight: 500;
        }}
        
        .nav a:hover {{
            text-decoration: underline;
        }}
        
        {self._get_language_switcher_css()}
    </style>
</head>
<body>
    <!-- 语言切换器 -->
    <div class="language-switcher">
        <button onclick="switchLanguage('zh')" class="active">中文</button>
        <button onclick="switchLanguage('en')">English</button>
    </div>
    
    <div class="container">
        <div class="header">
            <h1 data-lang="title">📊 个人项目进度管理系统</h1>
            <p data-lang="subtitle">管理你的研究项目进度，追踪开发历程</p>
        </div>
        
        <div class="nav">
            <a href="index.html" data-lang="home">🏠 主页</a>
            <a href="timeline.html" data-lang="timeline">📅 时间线</a>
            <a href="projects.html" data-lang="projects">📁 项目列表</a>
            <a href="daily.html" data-lang="daily_view">📅 日视图</a>
            <a href="weekly.html" data-lang="weekly_view">📅 周视图</a>
            <a href="monthly.html" data-lang="monthly_view">📅 月视图</a>
        </div>
        
        <div class="stats">
            <div class="stat-card">
                <div class="stat-number">{len(projects_data)}</div>
                <div class="stat-label" data-lang="active_projects">活跃项目</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{sum(len(p.get('progress_entries', [])) for p in projects_data)}</div>
                <div class="stat-label" data-lang="total_entries">总进度条目</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{len(set(p.get('parent_project', '') for p in projects_data))}</div>
                <div class="stat-label" data-lang="project_categories">大项目分类</div>
            </div>
        </div>
        
        <div class="projects-grid">
"""
        
        # 添加项目卡片
        for project in projects_data:
            latest_progress = project.get('progress_entries', [])[-1] if project.get('progress_entries') else None
            
            # 从文件名中提取项目ID
            project_id = None
            for progress_file in glob.glob(os.path.join(self.projects_dir, "*_progress.json")):
                try:
                    with open(progress_file, 'r', encoding='utf-8') as f:
                        file_data = json.load(f)
                        if file_data.get('project_name') == project.get('project_name'):
                            filename = os.path.basename(progress_file)
                            project_id = filename.replace('_progress.json', '')
                            break
                except Exception as e:
                    print(f"⚠️ 读取进度文件失败 {progress_file}: {e}")
            
            if not project_id:
                project_id = 'unknown'
            
            html_content += f"""
            <div class="project-card" onclick="window.location.href='{project_id}.html'" style="cursor: pointer;">
                <div class="project-header">
                    <div class="project-name">{project.get('project_name', 'Unknown')}</div>
                    <div class="project-parent">{project.get('parent_project', 'Unknown')}</div>
                </div>
                <div class="project-body">
                    <div class="project-goal">{project.get('development_goal', 'No goal set')}</div>
                    <div class="project-stats">
                        <div class="project-stat">
                            <div class="project-stat-number">{len(project.get('progress_entries', []))}</div>
                            <div class="project-stat-label">进度条目</div>
                        </div>
                        <div class="project-stat">
                            <div class="project-stat-number">{project.get('created_date', 'Unknown')}</div>
                            <div class="project-stat-label">创建日期</div>
                        </div>
                    </div>
                    {f'''
                    <div class="latest-progress">
                        <div class="progress-date">{latest_progress.get('date', '')} {latest_progress.get('time', '')}</div>
                        <div class="progress-description">{latest_progress.get('description', '')}</div>
                    </div>
                    ''' if latest_progress else '<div class="latest-progress">暂无进度记录</div>'}
                </div>
            </div>
"""
        
        html_content += """
        </div>
    </div>
    
    """ + self._get_language_script() + """
</body>
</html>"""
        
        # 保存主页
        with open(os.path.join(self.pages_dir, "index.html"), 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print("✅ 主页生成完成")
    
    def _generate_project_pages(self, projects_data):
        """生成项目详情页面"""
        for project in projects_data:
            project_name = project.get('project_name', 'Unknown')
            
            # 从文件名中提取项目ID
            project_id = None
            for progress_file in glob.glob(os.path.join(self.projects_dir, "*_progress.json")):
                try:
                    with open(progress_file, 'r', encoding='utf-8') as f:
                        file_data = json.load(f)
                        if file_data.get('project_name') == project_name:
                            # 从文件名中提取项目ID
                            filename = os.path.basename(progress_file)
                            project_id = filename.replace('_progress.json', '')
                            break
                except Exception as e:
                    print(f"⚠️ 读取进度文件失败 {progress_file}: {e}")
            
            if not project_id:
                project_id = 'unknown'
            
            html_content = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{project_name} - 项目进度</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.6;
            color: #333;
            background: #f5f5f5;
        }}
        
        .container {{
            max-width: 800px;
            margin: 0 auto;
            padding: 2rem;
        }}
        
        .header {{
            background: white;
            padding: 2rem;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            margin-bottom: 2rem;
        }}
        
        .project-title {{
            font-size: 2rem;
            color: #333;
            margin-bottom: 1rem;
        }}
        
        .project-meta {{
            color: #666;
        }}
        
        .progress-timeline {{
            background: white;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            overflow: hidden;
        }}
        
        .timeline-item {{
            padding: 1.5rem;
            border-bottom: 1px solid #eee;
            position: relative;
        }}
        
        .timeline-item:last-child {{
            border-bottom: none;
        }}
        
        .timeline-date {{
            font-weight: bold;
            color: #667eea;
            margin-bottom: 0.5rem;
        }}
        
        .timeline-time {{
            color: #666;
            font-size: 0.9rem;
        }}
        
        .timeline-description {{
            margin: 1rem 0;
            font-weight: 500;
        }}
        
        .timeline-notes {{
            background: #f8f9fa;
            padding: 1rem;
            border-radius: 5px;
            border-left: 4px solid #667eea;
            color: #666;
        }}
        
        .back-link {{
            display: inline-block;
            margin-bottom: 1rem;
            color: #667eea;
            text-decoration: none;
            font-weight: 500;
        }}
        
        .back-link:hover {{
            text-decoration: underline;
        }}
    </style>
</head>
<body>
    <div class="container">
        <a href="index.html" class="back-link">← 返回主页</a>
        
        <div class="header">
            <h1 class="project-title">{project_name}</h1>
            <div class="project-meta">
                <p><strong>隶属大项目:</strong> {project.get('parent_project', 'Unknown')}</p>
                <p><strong>开发目标:</strong> {project.get('development_goal', 'No goal set')}</p>
                <p><strong>创建日期:</strong> {project.get('created_date', 'Unknown')}</p>
                <p><strong>最后更新:</strong> {project.get('last_updated', 'Unknown')}</p>
            </div>
        </div>
        
        <div class="progress-timeline">
"""
            
            # 添加进度条目
            progress_entries = project.get('progress_entries', [])
            if progress_entries:
                for entry in reversed(progress_entries):
                    html_content += f"""
            <div class="timeline-item">
                <div class="timeline-date">{entry.get('date', '')}</div>
                <div class="timeline-time">{entry.get('time', '')}</div>
                <div class="timeline-description">{entry.get('description', '')}</div>
                {f'<div class="timeline-notes">{entry.get("notes", "")}</div>' if entry.get('notes') else ''}
            </div>
"""
            else:
                html_content += """
            <div class="timeline-item">
                <p>暂无进度记录</p>
            </div>
"""
            
            html_content += """
        </div>
    </div>
</body>
</html>"""
            
            # 保存项目页面
            project_file = os.path.join(self.pages_dir, f"{project_id}.html")
            with open(project_file, 'w', encoding='utf-8') as f:
                f.write(html_content)
        
        print(f"✅ 项目页面生成完成 ({len(projects_data)} 个项目)")
    
    def _generate_projects_list_page(self, projects_data):
        """生成项目列表页面"""
        html_content = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title data-lang="project_list_title">项目列表 - 个人项目进度管理系统</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.6;
            color: #333;
            background: #f5f5f5;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 2rem;
        }}
        
        .header {{
            background: white;
            padding: 2rem;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            margin-bottom: 2rem;
            text-align: center;
        }}
        
        .header h1 {{
            color: #333;
            margin-bottom: 1rem;
        }}
        
        .projects-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 1.5rem;
        }}
        
        .project-card {{
            background: white;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            overflow: hidden;
            transition: transform 0.3s ease;
            cursor: pointer;
        }}
        
        .project-card:hover {{
            transform: translateY(-5px);
        }}
        
        .project-header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 1.5rem;
        }}
        
        .project-name {{
            font-size: 1.3rem;
            font-weight: bold;
            margin-bottom: 0.5rem;
        }}
        
        .project-parent {{
            opacity: 0.9;
            font-size: 0.9rem;
        }}
        
        .project-body {{
            padding: 1.5rem;
        }}
        
        .project-goal {{
            color: #666;
            margin-bottom: 1rem;
            font-style: italic;
        }}
        
        .project-stats {{
            display: flex;
            justify-content: space-between;
            margin-bottom: 1rem;
        }}
        
        .project-stat {{
            text-align: center;
        }}
        
        .project-stat-number {{
            font-weight: bold;
            color: #667eea;
        }}
        
        .project-stat-label {{
            font-size: 0.8rem;
            color: #666;
        }}
        
        .latest-progress {{
            background: #f8f9fa;
            padding: 1rem;
            border-radius: 5px;
            border-left: 4px solid #667eea;
        }}
        
        .progress-date {{
            font-size: 0.8rem;
            color: #666;
            margin-bottom: 0.5rem;
        }}
        
        .progress-description {{
            font-weight: 500;
        }}
        
        .back-link {{
            display: inline-block;
            margin-bottom: 1rem;
            color: #667eea;
            text-decoration: none;
            font-weight: 500;
        }}
        
        .back-link:hover {{
            text-decoration: underline;
        }}
        
        .empty-state {{
            text-align: center;
            padding: 3rem;
            color: #666;
        }}
        
        {self._get_language_switcher_css()}
    </style>
</head>
<body>
    <!-- 语言切换器 -->
    <div class="language-switcher">
        <button onclick="switchLanguage('zh')" class="active">中文</button>
        <button onclick="switchLanguage('en')">English</button>
    </div>
    
    <div class="container">
        <a href="index.html" class="back-link" data-lang="back_to_home">← 返回主页</a>
        
        <div class="header">
            <h1 data-lang="project_list_title">📁 项目列表</h1>
            <p data-lang="project_list_subtitle">查看所有项目的详细信息和进度</p>
        </div>
        
        <div class="projects-grid">
"""
        
        if projects_data:
            for project in projects_data:
                latest_progress = project.get('progress_entries', [])[-1] if project.get('progress_entries') else None
                
                # 从文件名中提取项目ID
                project_id = None
                for progress_file in glob.glob(os.path.join(self.projects_dir, "*_progress.json")):
                    try:
                        with open(progress_file, 'r', encoding='utf-8') as f:
                            file_data = json.load(f)
                            if file_data.get('project_name') == project.get('project_name'):
                                filename = os.path.basename(progress_file)
                                project_id = filename.replace('_progress.json', '')
                                break
                    except Exception as e:
                        print(f"⚠️ 读取进度文件失败 {progress_file}: {e}")
                
                if not project_id:
                    project_id = 'unknown'
                
                html_content += f"""
            <div class="project-card" onclick="window.location.href='{project_id}.html'">
                <div class="project-header">
                    <div class="project-name">{project.get('project_name', 'Unknown')}</div>
                    <div class="project-parent">{project.get('parent_project', 'Unknown')}</div>
                </div>
                <div class="project-body">
                    <div class="project-goal">"{project.get('development_goal', 'No goal set')}"</div>
                    <div class="project-stats">
                        <div class="project-stat">
                            <div class="project-stat-number">{len(project.get('progress_entries', []))}</div>
                            <div class="project-stat-label" data-lang="progress_entries">进度条目</div>
                        </div>
                        <div class="project-stat">
                            <div class="project-stat-number">{project.get('created_date', 'Unknown')}</div>
                            <div class="project-stat-label" data-lang="created_date">创建日期</div>
                        </div>
                    </div>
                    {f'''
                    <div class="latest-progress">
                        <div class="progress-date">{latest_progress.get('date', '')} {latest_progress.get('time', '')}</div>
                        <div class="progress-description">{latest_progress.get('description', '')}</div>
                    </div>
                    ''' if latest_progress else '<div class="latest-progress" data-lang="no_progress">暂无进度记录</div>'}
                </div>
            </div>
"""
        else:
            html_content += """
            <div class="empty-state">
                <h2 data-lang="no_projects">📭 暂无项目</h2>
                <p data-lang="no_projects_desc">还没有创建任何项目，请先初始化一个项目。</p>
            </div>
"""
        
        html_content += """
        </div>
    </div>
    
    """ + self._get_language_script() + """
</body>
</html>"""
        
        # 保存项目列表页面
        with open(os.path.join(self.pages_dir, "projects.html"), 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print("✅ 项目列表页面生成完成")
    
    def _generate_timeline_page(self, projects_data):
        """生成时间线页面"""
        # 收集所有进度条目
        all_entries = []
        for project in projects_data:
            for entry in project.get('progress_entries', []):
                entry['project_name'] = project.get('project_name', 'Unknown')
                entry['parent_project'] = project.get('parent_project', 'Unknown')
                all_entries.append(entry)
        
        # 按日期排序
        all_entries.sort(key=lambda x: x.get('date', ''), reverse=True)
        
        html_content = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title data-lang="timeline_title">项目进度时间线</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.6;
            color: #333;
            background: #f5f5f5;
        }}
        
        .container {{
            max-width: 800px;
            margin: 0 auto;
            padding: 2rem;
        }}
        
        .header {{
            background: white;
            padding: 2rem;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            margin-bottom: 2rem;
            text-align: center;
        }}
        
        .header h1 {{
            color: #333;
            margin-bottom: 1rem;
        }}
        
        .timeline {{
            background: white;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            overflow: hidden;
        }}
        
        .timeline-item {{
            padding: 1.5rem;
            border-bottom: 1px solid #eee;
            position: relative;
        }}
        
        .timeline-item:last-child {{
            border-bottom: none;
        }}
        
        .timeline-date {{
            font-weight: bold;
            color: #667eea;
            margin-bottom: 0.5rem;
        }}
        
        .timeline-project {{
            color: #666;
            font-size: 0.9rem;
            margin-bottom: 0.5rem;
        }}
        
        .timeline-description {{
            margin: 1rem 0;
            font-weight: 500;
        }}
        
        .timeline-notes {{
            background: #f8f9fa;
            padding: 1rem;
            border-radius: 5px;
            border-left: 4px solid #667eea;
            color: #666;
        }}
        
        .back-link {{
            display: inline-block;
            margin-bottom: 1rem;
            color: #667eea;
            text-decoration: none;
            font-weight: 500;
        }}
        
        .back-link:hover {{
            text-decoration: underline;
        }}
        
        {self._get_language_switcher_css()}
    </style>
</head>
<body>
    <!-- 语言切换器 -->
    <div class="language-switcher">
        <button onclick="switchLanguage('zh')" class="active">中文</button>
        <button onclick="switchLanguage('en')">English</button>
    </div>
    
    <div class="container">
        <a href="index.html" class="back-link" data-lang="back_to_home">← 返回主页</a>
        
        <div class="header">
            <h1 data-lang="timeline_title">📅 项目进度时间线</h1>
            <p data-lang="timeline_subtitle">按时间顺序查看所有项目进度</p>
        </div>
        
        <div class="timeline">
"""
        
        # 添加时间线条目
        if all_entries:
            for entry in all_entries:
                html_content += f"""
            <div class="timeline-item">
                <div class="timeline-date">{entry.get('date', '')} {entry.get('time', '')}</div>
                <div class="timeline-project">{entry.get('project_name', '')} ({entry.get('parent_project', '')})</div>
                <div class="timeline-description">{entry.get('description', '')}</div>
                {f'<div class="timeline-notes">{entry.get("notes", "")}</div>' if entry.get('notes') else ''}
            </div>
"""
        else:
            html_content += """
            <div class="timeline-item">
                <p>暂无进度记录</p>
            </div>
"""
        
        html_content += """
        </div>
    </div>
    
    """ + self._get_language_script() + """
</body>
</html>"""
        
        # 保存时间线页面
        with open(os.path.join(self.pages_dir, "timeline.html"), 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print("✅ 时间线页面生成完成")

    def _generate_daily_view_page(self, projects_data):
        """生成日视图页面"""
        # 获取所有进度条目的日期
        all_dates = set()
        for project in projects_data:
            for entry in project.get('progress_entries', []):
                if entry.get('date'):
                    all_dates.add(entry.get('date'))
        
        # 如果有数据，使用最新的日期；否则使用今天的日期
        if all_dates:
            default_date = max(all_dates)
        else:
            default_date = datetime.now().strftime('%Y-%m-%d')
        
        html_content = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title data-lang="daily_view_title">日视图 - 个人项目进度管理系统</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.6;
            color: #333;
            background: #f5f5f5;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 2rem;
        }}
        
        .header {{
            background: white;
            padding: 2rem;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            margin-bottom: 2rem;
            text-align: center;
        }}
        
        .header h1 {{
            color: #333;
            margin-bottom: 1rem;
        }}
        
        .date-navigation {{
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 1rem;
            margin-bottom: 2rem;
        }}
        
        .date-nav-btn {{
            background: #667eea;
            color: white;
            border: none;
            padding: 0.5rem 1rem;
            border-radius: 5px;
            cursor: pointer;
            font-weight: 500;
            transition: background 0.3s ease;
        }}
        
        .date-nav-btn:hover {{
            background: #5a6fd8;
        }}
        
        .current-date {{
            font-size: 1.2rem;
            font-weight: bold;
            color: #333;
            min-width: 150px;
            text-align: center;
        }}
        
        .daily-progress {{
            background: white;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            overflow: hidden;
        }}
        
        .progress-item {{
            padding: 1.5rem;
            border-bottom: 1px solid #eee;
            position: relative;
        }}
        
        .progress-item:last-child {{
            border-bottom: none;
        }}
        
        .progress-time {{
            font-weight: bold;
            color: #667eea;
            margin-bottom: 0.5rem;
        }}
        
        .progress-project {{
            color: #666;
            font-size: 0.9rem;
            margin-bottom: 0.5rem;
        }}
        
        .progress-description {{
            margin: 1rem 0;
            font-weight: 500;
        }}
        
        .progress-notes {{
            background: #f8f9fa;
            padding: 1rem;
            border-radius: 5px;
            border-left: 4px solid #667eea;
            color: #666;
        }}
        
        .back-link {{
            display: inline-block;
            margin-bottom: 1rem;
            color: #667eea;
            text-decoration: none;
            font-weight: 500;
        }}
        
        .back-link:hover {{
            text-decoration: underline;
        }}
        
        .empty-state {{
            text-align: center;
            padding: 3rem;
            color: #666;
        }}
        
        {self._get_language_switcher_css()}
    </style>
</head>
<body>
    <!-- 语言切换器 -->
    <div class="language-switcher">
        <button onclick="switchLanguage('zh')" class="active">中文</button>
        <button onclick="switchLanguage('en')">English</button>
    </div>
    
    <div class="container">
        <a href="index.html" class="back-link" data-lang="back_to_home">← 返回主页</a>
        
        <div class="header">
            <h1 data-lang="daily_view_title">📅 日视图</h1>
            <p data-lang="daily_view_subtitle">查看指定日期的项目进度</p>
        </div>
        
        <div class="date-navigation">
            <button class="date-nav-btn" onclick="changeDate(-1)">← 前一天</button>
            <div class="current-date" id="currentDate">{default_date}</div>
            <button class="date-nav-btn" onclick="changeDate(1)">后一天 →</button>
        </div>
        
        <div class="daily-progress" id="dailyProgress">
"""
        
        # 获取指定日期的进度条目
        daily_entries = []
        for project in projects_data:
            for entry in project.get('progress_entries', []):
                if entry.get('date') == default_date:
                    entry['project_name'] = project.get('project_name', 'Unknown')
                    entry['parent_project'] = project.get('parent_project', 'Unknown')
                    daily_entries.append(entry)
        
        # 按时间排序
        daily_entries.sort(key=lambda x: x.get('time', ''))
        
        if daily_entries:
            for entry in daily_entries:
                html_content += f"""
            <div class="progress-item">
                <div class="progress-time">{entry.get('time', '')}</div>
                <div class="progress-project">{entry.get('project_name', '')} ({entry.get('parent_project', '')})</div>
                <div class="progress-description">{entry.get('description', '')}</div>
                {f'<div class="progress-notes">{entry.get("notes", "")}</div>' if entry.get('notes') else ''}
            </div>
"""
        else:
            html_content += """
            <div class="empty-state">
                <h2>📭 暂无进度记录</h2>
                <p>这一天还没有任何项目进度记录。</p>
            </div>
"""
        
        html_content += """
        </div>
    </div>
    
    <script>
        // 获取所有可用的日期
        const availableDates = """ + str(sorted(all_dates)) + """;
        let currentDate = new Date('""" + default_date + """');
        
        function changeDate(days) {
            currentDate.setDate(currentDate.getDate() + days);
            updateDateDisplay();
            loadDailyProgress();
        }
        
        function updateDateDisplay() {
            const dateStr = currentDate.toISOString().split('T')[0];
            document.getElementById('currentDate').textContent = dateStr;
        }
        
        function loadDailyProgress() {
            const dateStr = currentDate.toISOString().split('T')[0];
            window.history.pushState({}, '', `?date=${dateStr}`);
            
            // 这里可以添加AJAX请求来动态加载指定日期的进度
            // 目前只是更新URL参数
            location.reload();
        }
        
        window.addEventListener('load', function() {
            const urlParams = new URLSearchParams(window.location.search);
            const dateParam = urlParams.get('date');
            if (dateParam) {
                currentDate = new Date(dateParam);
                updateDateDisplay();
            }
        });
    </script>
    
    """ + self._get_language_script() + """
</body>
</html>"""
        
        # 保存日视图页面
        with open(os.path.join(self.pages_dir, "daily.html"), 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print("✅ 日视图页面生成完成")

    def _generate_weekly_view_page(self, projects_data):
        """生成周视图页面"""
        # 获取当前周的日期范围
        today = datetime.now()
        start_of_week = today - timedelta(days=today.weekday())
        end_of_week = start_of_week + timedelta(days=6)
        
        html_content = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title data-lang="weekly_view_title">周视图 - 个人项目进度管理系统</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.6;
            color: #333;
            background: #f5f5f5;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 2rem;
        }}
        
        .header {{
            background: white;
            padding: 2rem;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            margin-bottom: 2rem;
            text-align: center;
        }}
        
        .header h1 {{
            color: #333;
            margin-bottom: 1rem;
        }}
        
        .week-navigation {{
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 1rem;
            margin-bottom: 2rem;
        }}
        
        .week-nav-btn {{
            background: #667eea;
            color: white;
            border: none;
            padding: 0.5rem 1rem;
            border-radius: 5px;
            cursor: pointer;
            font-weight: 500;
            transition: background 0.3s ease;
        }}
        
        .week-nav-btn:hover {{
            background: #5a6fd8;
        }}
        
        .current-week {{
            font-size: 1.2rem;
            font-weight: bold;
            color: #333;
            min-width: 200px;
            text-align: center;
        }}
        
        .week-calendar {{
            background: white;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            overflow: hidden;
        }}
        
        .week-header {{
            display: grid;
            grid-template-columns: repeat(7, 1fr);
            background: #667eea;
            color: white;
            font-weight: bold;
        }}
        
        .week-day-header {{
            padding: 1rem;
            text-align: center;
            border-right: 1px solid rgba(255, 255, 255, 0.2);
        }}
        
        .week-day-header:last-child {{
            border-right: none;
        }}
        
        .week-days {{
            display: grid;
            grid-template-columns: repeat(7, 1fr);
        }}
        
        .week-day {{
            min-height: 200px;
            border-right: 1px solid #eee;
            border-bottom: 1px solid #eee;
            padding: 1rem;
        }}
        
        .week-day:last-child {{
            border-right: none;
        }}
        
        .week-day:nth-child(7n) {{
            border-bottom: none;
        }}
        
        .day-date {{
            font-weight: bold;
            color: #667eea;
            margin-bottom: 0.5rem;
        }}
        
        .day-progress {{
            font-size: 0.9rem;
        }}
        
        .progress-entry {{
            background: #f8f9fa;
            padding: 0.5rem;
            margin-bottom: 0.5rem;
            border-radius: 3px;
            border-left: 3px solid #667eea;
        }}
        
        .progress-entry:last-child {{
            margin-bottom: 0;
        }}
        
        .progress-time {{
            font-size: 0.8rem;
            color: #666;
        }}
        
        .progress-project {{
            font-weight: 500;
            margin: 0.25rem 0;
        }}
        
        .progress-description {{
            font-size: 0.8rem;
            color: #666;
        }}
        
        .back-link {{
            display: inline-block;
            margin-bottom: 1rem;
            color: #667eea;
            text-decoration: none;
            font-weight: 500;
        }}
        
        .back-link:hover {{
            text-decoration: underline;
        }}
        
        {self._get_language_switcher_css()}
    </style>
</head>
<body>
    <!-- 语言切换器 -->
    <div class="language-switcher">
        <button onclick="switchLanguage('zh')" class="active">中文</button>
        <button onclick="switchLanguage('en')">English</button>
    </div>
    
    <div class="container">
        <a href="index.html" class="back-link" data-lang="back_to_home">← 返回主页</a>
        
        <div class="header">
            <h1 data-lang="weekly_view_title">📅 周视图</h1>
            <p data-lang="weekly_view_subtitle">查看指定周的项目进度</p>
        </div>
        
        <div class="week-navigation">
            <button class="week-nav-btn" onclick="changeWeek(-1)">← 上一周</button>
            <div class="current-week" id="currentWeek">{start_of_week.strftime('%Y-%m-%d')} 至 {end_of_week.strftime('%Y-%m-%d')}</div>
            <button class="week-nav-btn" onclick="changeWeek(1)">下一周 →</button>
        </div>
        
        <div class="week-calendar">
            <div class="week-header">
                <div class="week-day-header">周一</div>
                <div class="week-day-header">周二</div>
                <div class="week-day-header">周三</div>
                <div class="week-day-header">周四</div>
                <div class="week-day-header">周五</div>
                <div class="week-day-header">周六</div>
                <div class="week-day-header">周日</div>
            </div>
            <div class="week-days" id="weekDays">
"""
        
        # 生成一周的日期
        week_dates = []
        for i in range(7):
            date = start_of_week + timedelta(days=i)
            week_dates.append(date.strftime('%Y-%m-%d'))
        
        # 获取一周内的进度条目
        week_entries = {}
        for project in projects_data:
            for entry in project.get('progress_entries', []):
                entry_date = entry.get('date')
                if entry_date in week_dates:
                    if entry_date not in week_entries:
                        week_entries[entry_date] = []
                    entry_copy = entry.copy()
                    entry_copy['project_name'] = project.get('project_name', 'Unknown')
                    entry_copy['parent_project'] = project.get('parent_project', 'Unknown')
                    week_entries[entry_date].append(entry_copy)
        
        # 生成周视图内容
        for i, date in enumerate(week_dates):
            day_name = ['周一', '周二', '周三', '周四', '周五', '周六', '周日'][i]
            date_obj = datetime.strptime(date, '%Y-%m-%d')
            display_date = date_obj.strftime('%m-%d')
            
            html_content += f"""
                <div class="week-day">
                    <div class="day-date">{day_name} {display_date}</div>
                    <div class="day-progress">
"""
            
            if date in week_entries:
                for entry in week_entries[date]:
                    html_content += f"""
                        <div class="progress-entry">
                            <div class="progress-time">{entry.get('time', '')}</div>
                            <div class="progress-project">{entry.get('project_name', '')}</div>
                            <div class="progress-description">{entry.get('description', '')}</div>
                        </div>
"""
            else:
                html_content += """
                        <div class="progress-entry">
                            <div class="progress-description">暂无进度</div>
                        </div>
"""
            
            html_content += """
                    </div>
                </div>
"""
        
        html_content += """
            </div>
        </div>
    </div>
    
    <script>
        let currentWeekStart = new Date('""" + start_of_week.strftime('%Y-%m-%d') + """');
        
        function changeWeek(weeks) {
            currentWeekStart.setDate(currentWeekStart.getDate() + (weeks * 7));
            updateWeekDisplay();
            loadWeekProgress();
        }
        
        function updateWeekDisplay() {
            const endOfWeek = new Date(currentWeekStart);
            endOfWeek.setDate(endOfWeek.getDate() + 6);
            
            const startStr = currentWeekStart.toISOString().split('T')[0];
            const endStr = endOfWeek.toISOString().split('T')[0];
            
            document.getElementById('currentWeek').textContent = `${startStr} 至 ${endStr}`;
        }
        
        function loadWeekProgress() {
            const startStr = currentWeekStart.toISOString().split('T')[0];
            window.history.pushState({}, '', `?week=${startStr}`);
        }
        
        window.addEventListener('load', function() {
            const urlParams = new URLSearchParams(window.location.search);
            const weekParam = urlParams.get('week');
            if (weekParam) {
                currentWeekStart = new Date(weekParam);
                updateWeekDisplay();
            }
        });
    </script>
    
    """ + self._get_language_script() + """
</body>
</html>"""
        
        # 保存周视图页面
        with open(os.path.join(self.pages_dir, "weekly.html"), 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print("✅ 周视图页面生成完成")

    def _generate_monthly_view_page(self, projects_data):
        """生成月视图页面"""
        # 获取当前月份
        today = datetime.now()
        current_month = today.strftime('%Y-%m')
        
        html_content = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title data-lang="monthly_view_title">月视图 - 个人项目进度管理系统</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.6;
            color: #333;
            background: #f5f5f5;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 2rem;
        }}
        
        .header {{
            background: white;
            padding: 2rem;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            margin-bottom: 2rem;
            text-align: center;
        }}
        
        .header h1 {{
            color: #333;
            margin-bottom: 1rem;
        }}
        
        .month-navigation {{
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 1rem;
            margin-bottom: 2rem;
        }}
        
        .month-nav-btn {{
            background: #667eea;
            color: white;
            border: none;
            padding: 0.5rem 1rem;
            border-radius: 5px;
            cursor: pointer;
            font-weight: 500;
            transition: background 0.3s ease;
        }}
        
        .month-nav-btn:hover {{
            background: #5a6fd8;
        }}
        
        .current-month {{
            font-size: 1.2rem;
            font-weight: bold;
            color: #333;
            min-width: 150px;
            text-align: center;
        }}
        
        .month-calendar {{
            background: white;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            overflow: hidden;
        }}
        
        .month-header {{
            display: grid;
            grid-template-columns: repeat(7, 1fr);
            background: #667eea;
            color: white;
            font-weight: bold;
        }}
        
        .month-day-header {{
            padding: 1rem;
            text-align: center;
            border-right: 1px solid rgba(255, 255, 255, 0.2);
        }}
        
        .month-day-header:last-child {{
            border-right: none;
        }}
        
        .month-days {{
            display: grid;
            grid-template-columns: repeat(7, 1fr);
        }}
        
        .month-day {{
            min-height: 120px;
            border-right: 1px solid #eee;
            border-bottom: 1px solid #eee;
            padding: 0.5rem;
            position: relative;
        }}
        
        .month-day:last-child {{
            border-right: none;
        }}
        
        .month-day:nth-child(7n) {{
            border-bottom: none;
        }}
        
        .month-day.other-month {{
            background: #f8f9fa;
            color: #999;
        }}
        
        .month-day.today {{
            background: #e3f2fd;
        }}
        
        .day-number {{
            font-weight: bold;
            color: #333;
            margin-bottom: 0.5rem;
        }}
        
        .day-progress {{
            font-size: 0.8rem;
        }}
        
        .progress-indicator {{
            background: #667eea;
            color: white;
            padding: 0.2rem 0.4rem;
            border-radius: 3px;
            margin-bottom: 0.2rem;
            font-size: 0.7rem;
        }}
        
        .back-link {{
            display: inline-block;
            margin-bottom: 1rem;
            color: #667eea;
            text-decoration: none;
            font-weight: 500;
        }}
        
        .back-link:hover {{
            text-decoration: underline;
        }}
        
        {self._get_language_switcher_css()}
    </style>
</head>
<body>
    <!-- 语言切换器 -->
    <div class="language-switcher">
        <button onclick="switchLanguage('zh')" class="active">中文</button>
        <button onclick="switchLanguage('en')">English</button>
    </div>
    
    <div class="container">
        <a href="index.html" class="back-link" data-lang="back_to_home">← 返回主页</a>
        
        <div class="header">
            <h1 data-lang="monthly_view_title">📅 月视图</h1>
            <p data-lang="monthly_view_subtitle">查看指定月的项目进度</p>
        </div>
        
        <div class="month-navigation">
            <button class="month-nav-btn" onclick="changeMonth(-1)">← 上个月</button>
            <div class="current-month" id="currentMonth">{today.strftime('%Y年%m月')}</div>
            <button class="month-nav-btn" onclick="changeMonth(1)">下个月 →</button>
        </div>
        
        <div class="month-calendar">
            <div class="month-header">
                <div class="month-day-header">周一</div>
                <div class="month-day-header">周二</div>
                <div class="month-day-header">周三</div>
                <div class="month-day-header">周四</div>
                <div class="month-day-header">周五</div>
                <div class="month-day-header">周六</div>
                <div class="month-day-header">周日</div>
            </div>
            <div class="month-days" id="monthDays">
"""
        
        # 生成月历
        year, month = today.year, today.month
        cal = calendar.monthcalendar(year, month)
        
        # 获取当月的进度条目
        month_entries = {}
        for project in projects_data:
            for entry in project.get('progress_entries', []):
                entry_date = entry.get('date')
                if entry_date and entry_date.startswith(f"{year:04d}-{month:02d}"):
                    if entry_date not in month_entries:
                        month_entries[entry_date] = []
                    entry_copy = entry.copy()
                    entry_copy['project_name'] = project.get('project_name', 'Unknown')
                    month_entries[entry_date].append(entry_copy)
        
        # 生成月历内容
        for week in cal:
            for day in week:
                if day == 0:
                    html_content += """
                <div class="month-day other-month">
                    <div class="day-number"></div>
                </div>
"""
                else:
                    date_str = f"{year:04d}-{month:02d}-{day:02d}"
                    is_today = date_str == today.strftime('%Y-%m-%d')
                    today_class = " today" if is_today else ""
                    
                    html_content += f"""
                <div class="month-day{today_class}">
                    <div class="day-number">{day}</div>
                    <div class="day-progress">
"""
                    
                    if date_str in month_entries:
                        for entry in month_entries[date_str]:
                            html_content += f"""
                        <div class="progress-indicator" title="{entry.get('project_name', '')}: {entry.get('description', '')}">
                            {entry.get('project_name', '')[:8]}...
                        </div>
"""
                    
                    html_content += """
                    </div>
                </div>
"""
        
        html_content += """
            </div>
        </div>
    </div>
    
    <script>
        let currentMonth = new Date('""" + today.strftime('%Y-%m-01') + """');
        
        function changeMonth(months) {
            currentMonth.setMonth(currentMonth.getMonth() + months);
            updateMonthDisplay();
            loadMonthProgress();
        }
        
        function updateMonthDisplay() {
            const year = currentMonth.getFullYear();
            const month = currentMonth.getMonth() + 1;
            document.getElementById('currentMonth').textContent = `${year}年${month.toString().padStart(2, '0')}月`;
        }
        
        function loadMonthProgress() {
            const year = currentMonth.getFullYear();
            const month = currentMonth.getMonth() + 1;
            const monthStr = `${year}-${month.toString().padStart(2, '0')}`;
            window.history.pushState({}, '', `?month=${monthStr}`);
        }
        
        window.addEventListener('load', function() {
            const urlParams = new URLSearchParams(window.location.search);
            const monthParam = urlParams.get('month');
            if (monthParam) {
                currentMonth = new Date(monthParam + '-01');
                updateMonthDisplay();
            }
        });
    </script>
    
    """ + self._get_language_script() + """
</body>
</html>"""
        
        # 保存月视图页面
        with open(os.path.join(self.pages_dir, "monthly.html"), 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print("✅ 月视图页面生成完成")

def main():
    generator = PagesGenerator()
    generator.generate_pages()

if __name__ == "__main__":
    main()
