#!/usr/bin/env python3
"""
简化版的OpenDevin main.py
跳过复杂的运行时依赖，专注于核心LLM功能
适合Windows直接运行
"""

import asyncio
import os
import sys
import argparse
from typing import Optional

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def parse_arguments():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(description='OpenDevin 简化版 - 直接运行核心功能')
    
    # 任务相关参数
    parser.add_argument('-t', '--task', type=str, help='要执行的任务')
    parser.add_argument('-f', '--file', type=str, help='从文件读取任务')
    
    # LLM相关参数
    parser.add_argument('-m', '--model-name', type=str, default='deepseek-chat', 
                       help='使用的模型名称 (默认: deepseek-chat)')
    parser.add_argument('--api-key', type=str, help='API密钥')
    parser.add_argument('--base-url', type=str, default='https://api.deepseek.com',
                       help='API基础URL (默认: https://api.deepseek.com)')
    
    # 其他参数
    parser.add_argument('-d', '--directory', type=str, default='./workspace',
                       help='工作目录 (默认: ./workspace)')
    parser.add_argument('--max-iterations', type=int, default=30,
                       help='最大迭代次数 (默认: 30)')
    parser.add_argument('--temperature', type=float, default=0.1,
                       help='温度参数 (默认: 0.1)')
    parser.add_argument('--debug', action='store_true', help='启用调试模式')
    
    return parser.parse_args()

def read_task_from_file(file_path: str) -> str:
    """从文件读取任务"""
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read().strip()

def setup_environment(args):
    """设置环境变量"""
    # 设置API密钥
    if args.api_key:
        os.environ['LLM_API_KEY'] = args.api_key
    elif not os.environ.get('LLM_API_KEY'):
        print("❌ 错误: 未设置API密钥")
        print("请使用 --api-key 参数或设置环境变量 LLM_API_KEY")
        sys.exit(1)
    
    # 设置其他环境变量
    os.environ['LLM_MODEL'] = args.model_name
    os.environ['LLM_BASE_URL'] = args.base_url
    
    # 创建工作目录
    os.makedirs(args.directory, exist_ok=True)
    
    if args.debug:
        os.environ['DEBUG'] = '1'

async def run_simple_llm_task(task: str, model: str, workspace: str, temperature: float = 0.1):
    """运行简化的LLM任务"""
    try:
        # 导入LLM相关模块
        from opendevin.llm.llm import LLM
        from opendevin.core.config import LLMConfig
        
        print(f"🤖 OpenDevin 简化版")
        print(f"📝 任务: {task}")
        print(f"🔧 模型: {model}")
        print(f"📁 工作目录: {workspace}")
        print(f"🌡️ 温度: {temperature}")
        print("=" * 50)
        print()
        
        # 配置LLM
        llm_config = LLMConfig(
            model=model,
            api_key=os.environ.get('LLM_API_KEY'),
            base_url=os.environ.get('LLM_BASE_URL'),
            temperature=temperature,
            max_output_tokens=4000
        )
        
        llm = LLM(llm_config=llm_config)
        
        # 构建系统提示
        system_prompt = f"""
你是OpenDevin，一个专业的AI软件工程师助手。你的任务是帮助用户完成编程和开发相关的工作。

工作目录: {workspace}
当前任务: {task}

请按照以下格式提供完整的解决方案：

1. 📋 任务分析
   - 理解用户需求
   - 分析技术要求

2. 🛠️ 解决方案
   - 提供详细的实现方案
   - 说明技术选择

3. 💻 代码实现
   - 提供完整的、可运行的代码
   - 包含详细注释
   - 如果需要多个文件，请分别提供

4. 📖 使用说明
   - 如何运行代码
   - 如何使用功能
   - 注意事项

请在代码块前标注文件名，格式：
```python
# 文件名: example.py
你的代码内容
```

请用中文回复，提供专业、完整的解决方案。
"""
        
        print("💭 AI正在分析任务...")
        
        # 调用LLM
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": task}
        ]
        
        response = await llm.acompletion(messages=messages, model=model)
        
        result = response.choices[0].message.content
        
        print("🤖 AI解决方案:")
        print("-" * 50)
        print(result)
        print("-" * 50)
        
        # 提取并创建文件
        await extract_and_create_files(result, workspace)
        
        print(f"\n✅ 任务完成！")
        print(f"📁 查看结果: {os.path.abspath(workspace)}")
        
        return result
        
    except Exception as e:
        print(f"❌ 错误: {e}")
        if os.environ.get('DEBUG'):
            import traceback
            traceback.print_exc()
        
        print("\n💡 可能的解决方案:")
        print("1. 检查API密钥是否正确")
        print("2. 检查网络连接")
        print("3. 确认API配额充足")
        return None

async def extract_and_create_files(response_text: str, workspace: str):
    """从AI响应中提取代码并创建文件"""
    import re
    
    # 查找代码块和文件名
    pattern = r'```(\w+)?\n(?:#\s*文件名:\s*(.+?)\n)?(.*?)\n```'
    matches = re.findall(pattern, response_text, re.DOTALL)
    
    if not matches:
        print("📄 未检测到代码块")
        return
    
    print(f"\n📄 检测到 {len(matches)} 个代码块，正在创建文件...")
    
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
            elif lang == 'bash' or lang == 'sh':
                filename = f"script_{file_count}.sh"
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
            
            # 如果是脚本文件，设置执行权限（Linux/Mac）
            if filename.endswith(('.sh', '.py')) and os.name != 'nt':
                os.chmod(filepath, 0o755)
                
        except Exception as e:
            print(f"  ❌ 创建失败 {filename}: {e}")

async def main():
    """主函数"""
    args = parse_arguments()
    
    # 显示帮助信息
    if len(sys.argv) == 1:
        print("🤖 OpenDevin 简化版")
        print("=" * 50)
        print("用法:")
        print("  python main_simple.py -t '你的任务描述'")
        print("  python main_simple.py -f task.txt")
        print("")
        print("示例:")
        print("  python main_simple.py -t '创建一个Python计算器'")
        print("  python main_simple.py -t '分析这个项目的代码结构' -d ./my_project")
        print("")
        print("参数:")
        print("  -t, --task           任务描述")
        print("  -f, --file           从文件读取任务")
        print("  -m, --model-name     模型名称 (默认: deepseek-chat)")
        print("  --api-key            API密钥")
        print("  --base-url           API地址 (默认: https://api.deepseek.com)")
        print("  -d, --directory      工作目录 (默认: ./workspace)")
        print("  --temperature        温度参数 (默认: 0.1)")
        print("  --debug              启用调试模式")
        print("")
        print("环境变量:")
        print("  LLM_API_KEY          DeepSeek API密钥")
        print("  LLM_MODEL            模型名称")
        print("  LLM_BASE_URL         API地址")
        return
    
    # 确定任务
    if args.file:
        if not os.path.exists(args.file):
            print(f"❌ 文件不存在: {args.file}")
            sys.exit(1)
        task_str = read_task_from_file(args.file)
    elif args.task:
        task_str = args.task
    else:
        print("❌ 错误: 未指定任务")
        print("请使用 -t 参数指定任务或 -f 参数指定任务文件")
        sys.exit(1)
    
    if not task_str.strip():
        print("❌ 错误: 任务内容为空")
        sys.exit(1)
    
    # 设置环境
    setup_environment(args)
    
    # 运行任务
    try:
        await run_simple_llm_task(
            task=task_str,
            model=args.model_name,
            workspace=args.directory,
            temperature=args.temperature
        )
    except KeyboardInterrupt:
        print("\n👋 用户中断，再见!")
    except Exception as e:
        print(f"❌ 运行失败: {e}")
        if args.debug:
            import traceback
            traceback.print_exc()

if __name__ == '__main__':
    asyncio.run(main())