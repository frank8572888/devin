#!/usr/bin/env python3
"""
简化的OpenDevin运行脚本 - 适用于Windows直接运行
这个脚本避免了复杂的依赖问题，专注于核心功能
"""

import os
import sys
import asyncio
import argparse
from typing import Optional

# 添加项目路径到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def setup_environment():
    """设置环境变量"""
    # 设置默认配置
    os.environ.setdefault('LLM_MODEL', 'deepseek-chat')
    os.environ.setdefault('LLM_BASE_URL', 'https://api.deepseek.com')
    
    # 检查API密钥
    if not os.environ.get('LLM_API_KEY'):
        print("❌ 错误: 未设置LLM_API_KEY环境变量")
        print("请设置你的DeepSeek API密钥:")
        print("Windows PowerShell: $env:LLM_API_KEY = 'your-api-key'")
        print("Windows CMD: set LLM_API_KEY=your-api-key")
        sys.exit(1)

def parse_args():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(description='简化的OpenDevin运行器')
    parser.add_argument('-t', '--task', required=True, help='要执行的任务')
    parser.add_argument('-m', '--model', default='deepseek-chat', help='使用的模型')
    parser.add_argument('-d', '--directory', default='./workspace', help='工作目录')
    parser.add_argument('--api-key', help='API密钥 (也可以通过环境变量设置)')
    parser.add_argument('--debug', action='store_true', help='启用调试模式')
    return parser.parse_args()

async def run_simple_agent(task: str, model: str = 'deepseek-chat', workspace: str = './workspace'):
    """运行简化的代理"""
    try:
        # 导入必要的模块
        from opendevin.llm.llm import LLM
        from opendevin.core.config import LLMConfig
        
        print(f"🚀 启动OpenDevin简化版")
        print(f"📝 任务: {task}")
        print(f"🤖 模型: {model}")
        print(f"📁 工作目录: {workspace}")
        print("-" * 50)
        
        # 创建工作目录
        os.makedirs(workspace, exist_ok=True)
        
        # 配置LLM
        llm_config = LLMConfig(
            model=model,
            api_key=os.environ.get('LLM_API_KEY'),
            base_url=os.environ.get('LLM_BASE_URL', 'https://api.deepseek.com'),
            temperature=0.1,
            max_output_tokens=4000
        )
        
        llm = LLM(llm_config=llm_config)
        
        # 简单的对话循环
        print("💭 正在思考...")
        
        # 构建提示
        prompt = f"""
你是一个AI编程助手。用户给你一个任务，你需要分析任务并提供解决方案。

工作目录: {workspace}
任务: {task}

请分析这个任务，并提供详细的解决方案。如果需要编写代码，请提供完整的代码示例。
如果需要创建文件，请说明文件名和内容。

请用中文回复。
"""
        
        # 调用LLM
        response = await llm.acompletion(
            messages=[{"role": "user", "content": prompt}],
            model=model
        )
        
        print("🤖 AI助手回复:")
        print("-" * 50)
        print(response.choices[0].message.content)
        print("-" * 50)
        
        # 询问是否需要执行代码
        if "```" in response.choices[0].message.content:
            print("\n💡 检测到代码块，是否需要我帮你创建文件? (y/N)")
            user_input = input().strip().lower()
            
            if user_input in ['y', 'yes', '是', '需要']:
                await create_files_from_response(response.choices[0].message.content, workspace)
        
        print(f"\n✅ 任务完成! 工作目录: {workspace}")
        
    except Exception as e:
        print(f"❌ 错误: {e}")
        if args.debug:
            import traceback
            traceback.print_exc()

async def create_files_from_response(response_text: str, workspace: str):
    """从响应中提取代码并创建文件"""
    import re
    
    # 查找代码块
    code_blocks = re.findall(r'```(\w+)?\n(.*?)\n```', response_text, re.DOTALL)
    
    for i, (lang, code) in enumerate(code_blocks):
        # 尝试从代码中推断文件名
        filename = f"generated_code_{i+1}"
        
        if lang == 'python':
            filename += '.py'
        elif lang == 'javascript':
            filename += '.js'
        elif lang == 'html':
            filename += '.html'
        elif lang == 'css':
            filename += '.css'
        else:
            filename += '.txt'
        
        # 检查代码中是否有文件名提示
        lines = code.split('\n')
        for line in lines[:5]:  # 检查前5行
            if '# 文件名:' in line or '# filename:' in line:
                suggested_name = line.split(':')[-1].strip()
                if suggested_name:
                    filename = suggested_name
                break
        
        filepath = os.path.join(workspace, filename)
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(code.strip())
            print(f"📄 已创建文件: {filepath}")
        except Exception as e:
            print(f"❌ 创建文件失败 {filepath}: {e}")

if __name__ == '__main__':
    args = parse_args()
    
    # 设置API密钥
    if args.api_key:
        os.environ['LLM_API_KEY'] = args.api_key
    
    # 设置调试模式
    if args.debug:
        os.environ['DEBUG'] = '1'
    
    # 设置环境
    setup_environment()
    
    print("🎯 OpenDevin 简化运行器")
    print("=" * 50)
    
    # 运行
    try:
        asyncio.run(run_simple_agent(
            task=args.task,
            model=args.model,
            workspace=args.directory
        ))
    except KeyboardInterrupt:
        print("\n👋 用户中断，再见!")
    except Exception as e:
        print(f"❌ 运行失败: {e}")
        if args.debug:
            import traceback
            traceback.print_exc()