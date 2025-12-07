#!/usr/bin/env python3
"""
预设任务运行器 - 支持多个预设任务，一键切换
"""

import os
import sys
import asyncio

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# ================================
# 🎯 配置区域
# ================================

# 你的DeepSeek API密钥
API_KEY = "your-deepseek-api-key-here"  # 请替换为你的实际API密钥

# ================================
# 📋 预设任务列表 - 在这里添加你常用的任务
# ================================

PRESET_TASKS = {
    "calculator": {
        "name": "Python计算器",
        "task": "创建一个Python计算器程序，支持基本的加减乘除运算，包含用户界面",
        "workspace": "./workspace/calculator"
    },
    
    "todo": {
        "name": "待办事项应用",
        "task": "创建一个简单的待办事项管理应用，支持添加、删除、标记完成功能，使用Python和简单的GUI",
        "workspace": "./workspace/todo_app"
    },
    
    "web_scraper": {
        "name": "网页爬虫",
        "task": "创建一个Python网页爬虫，可以抓取指定网站的数据并保存到CSV文件",
        "workspace": "./workspace/web_scraper"
    },
    
    "file_organizer": {
        "name": "文件整理器",
        "task": "创建一个文件整理工具，可以根据文件类型自动整理指定文件夹中的文件",
        "workspace": "./workspace/file_organizer"
    },
    
    "password_generator": {
        "name": "密码生成器",
        "task": "创建一个安全的密码生成器，支持自定义长度和字符类型，包含GUI界面",
        "workspace": "./workspace/password_generator"
    },
    
    "weather_app": {
        "name": "天气查询应用",
        "task": "创建一个天气查询应用，可以查询指定城市的天气信息，使用免费的天气API",
        "workspace": "./workspace/weather_app"
    },
    
    "code_analyzer": {
        "name": "代码分析器",
        "task": "分析当前目录下的Python代码，找出潜在的问题、改进建议和代码质量评估",
        "workspace": "./workspace/code_analysis"
    },
    
    "readme_generator": {
        "name": "README生成器",
        "task": "为当前项目生成一个详细的README.md文件，包含项目描述、安装说明、使用方法等",
        "workspace": "./workspace"
    },
    
    "custom": {
        "name": "自定义任务",
        "task": "",  # 这个会在运行时询问
        "workspace": "./workspace/custom"
    }
}

# ================================
# 🎯 选择要运行的任务 - 修改这里来切换任务
# ================================

# 当前选择的任务（修改这个值来切换任务）
CURRENT_TASK = "calculator"  # 可选值见上面的 PRESET_TASKS 键名

# 其他配置
MODEL = "deepseek-chat"
TEMPERATURE = 0.1
MAX_TOKENS = 4000
AUTO_CREATE_FILES = True

# ================================
# 🚀 程序代码
# ================================

def show_available_tasks():
    """显示所有可用的任务"""
    print("📋 可用的预设任务:")
    print("-" * 50)
    for key, task in PRESET_TASKS.items():
        print(f"  {key:15} - {task['name']}")
    print("-" * 50)
    print(f"当前选择: {CURRENT_TASK}")
    print(f"要切换任务，请修改代码中的 CURRENT_TASK 变量")
    print()

def setup_environment():
    """设置环境"""
    os.environ['LLM_API_KEY'] = API_KEY
    os.environ['LLM_MODEL'] = MODEL
    os.environ['LLM_BASE_URL'] = 'https://api.deepseek.com'
    
    # 检查API密钥
    if API_KEY == "your-deepseek-api-key-here":
        print("❌ 请先设置你的DeepSeek API密钥！")
        print("在代码顶部修改 API_KEY 变量")
        return False
    
    # 检查任务是否存在
    if CURRENT_TASK not in PRESET_TASKS:
        print(f"❌ 任务 '{CURRENT_TASK}' 不存在！")
        show_available_tasks()
        return False
    
    return True

async def run_task():
    """执行选定的任务"""
    try:
        from opendevin.llm.llm import LLM
        from opendevin.core.config import LLMConfig
        
        # 获取当前任务配置
        task_config = PRESET_TASKS[CURRENT_TASK]
        task_name = task_config['name']
        task_description = task_config['task']
        workspace = task_config['workspace']
        
        # 如果是自定义任务，询问用户
        if CURRENT_TASK == "custom":
            print("🎯 自定义任务模式")
            task_description = input("请输入你的任务描述: ").strip()
            if not task_description:
                print("❌ 任务描述不能为空")
                return
        
        # 创建工作目录
        os.makedirs(workspace, exist_ok=True)
        
        print("🤖 OpenDevin 预设任务运行器")
        print("=" * 50)
        print(f"📝 任务: {task_name}")
        print(f"📄 描述: {task_description}")
        print(f"🔧 模型: {MODEL}")
        print(f"📁 工作目录: {workspace}")
        print("=" * 50)
        print()
        
        # 配置LLM
        llm_config = LLMConfig(
            model=MODEL,
            api_key=API_KEY,
            base_url='https://api.deepseek.com',
            temperature=TEMPERATURE,
            max_output_tokens=MAX_TOKENS
        )
        
        llm = LLM(llm_config=llm_config)
        
        # 构建提示
        prompt = f"""
你是一个专业的AI编程助手。用户选择了一个预设任务，你需要提供完整的解决方案。

任务名称: {task_name}
任务描述: {task_description}
工作目录: {workspace}

请按以下格式提供完整的解决方案：

1. 📋 需求分析
   - 分析任务的具体要求
   - 列出主要功能点

2. 🏗️ 技术方案
   - 选择合适的技术栈
   - 说明实现思路

3. 💻 代码实现
   - 提供完整的、可运行的代码
   - 代码要有详细注释
   - 如果需要多个文件，请分别提供

4. 📖 使用说明
   - 如何运行代码
   - 如何使用功能
   - 注意事项

请在每个代码块前标注文件名，格式：
```python
# 文件名: main.py
你的代码内容
```

请用中文回复，提供专业、完整的解决方案。
"""
        
        print("💭 AI正在分析任务并生成解决方案...")
        
        # 调用LLM
        response = await llm.acompletion(
            messages=[{"role": "user", "content": prompt}],
            model=MODEL
        )
        
        result = response.choices[0].message.content
        
        print("🤖 AI解决方案:")
        print("-" * 50)
        print(result)
        print("-" * 50)
        
        # 自动创建文件
        if AUTO_CREATE_FILES and "```" in result:
            print("\n📄 正在自动创建文件...")
            await create_files_from_response(result, workspace)
        
        print(f"\n✅ 任务 '{task_name}' 完成！")
        print(f"📁 查看结果: {os.path.abspath(workspace)}")
        
        # 显示下一步建议
        print(f"\n💡 下一步:")
        print(f"1. 查看生成的文件: {workspace}")
        print(f"2. 运行代码测试功能")
        print(f"3. 根据需要修改代码")
        
    except Exception as e:
        print(f"❌ 错误: {e}")
        print("\n💡 可能的解决方案:")
        print("1. 检查API密钥是否正确")
        print("2. 检查网络连接")
        print("3. 安装必要依赖: pip install litellm fastapi python-dotenv")

async def create_files_from_response(response_text, workspace):
    """从AI响应中自动创建文件"""
    import re
    
    # 查找代码块和文件名
    pattern = r'```(\w+)?\n(?:#\s*文件名:\s*(.+?)\n)?(.*?)\n```'
    matches = re.findall(pattern, response_text, re.DOTALL)
    
    file_count = 0
    
    for lang, filename, code in matches:
        # 如果没有指定文件名，自动生成
        if not filename.strip():
            file_count += 1
            if lang == 'python':
                filename = f"main_{file_count}.py"
            elif lang == 'javascript':
                filename = f"script_{file_count}.js"
            elif lang == 'html':
                filename = f"index_{file_count}.html"
            elif lang == 'css':
                filename = f"style_{file_count}.css"
            else:
                filename = f"file_{file_count}.txt"
        else:
            filename = filename.strip()
        
        # 创建文件
        filepath = os.path.join(workspace, filename)
        
        try:
            # 确保目录存在
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(code.strip())
            print(f"  ✅ 已创建: {filename}")
        except Exception as e:
            print(f"  ❌ 创建失败 {filename}: {e}")

def main():
    """主函数"""
    print("🚀 OpenDevin 预设任务运行器")
    print()
    
    # 显示可用任务
    show_available_tasks()
    
    # 设置环境
    if not setup_environment():
        return
    
    # 运行任务
    try:
        asyncio.run(run_task())
    except KeyboardInterrupt:
        print("\n👋 用户中断，再见!")
    except Exception as e:
        print(f"❌ 运行失败: {e}")

if __name__ == '__main__':
    main()