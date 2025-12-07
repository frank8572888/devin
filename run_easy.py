#!/usr/bin/env python3
"""
超简单的OpenDevin运行器 - 直接在代码中设置问题
适合不想每次手动输入命令的用户
"""

import os
import sys
import asyncio

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# ================================
# 🎯 在这里设置你的问题和配置
# ================================

# 你的DeepSeek API密钥
API_KEY = "your-deepseek-api-key-here"  # 请替换为你的实际API密钥

# 你想要AI帮你做的事情（可以修改这里）
TASK = "创建一个简单的Python计算器，支持加减乘除运算"

# 可选配置
MODEL = "deepseek-chat"                    # 使用的模型
WORKSPACE = "./workspace"                  # 工作目录
TEMPERATURE = 0.1                          # 创造性程度 (0-1)
MAX_TOKENS = 4000                         # 最大输出长度

# 是否自动创建文件（如果AI生成了代码）
AUTO_CREATE_FILES = True

# ================================
# 🚀 运行配置完成，下面是程序代码
# ================================

def setup_environment():
    """设置环境"""
    os.environ['LLM_API_KEY'] = API_KEY
    os.environ['LLM_MODEL'] = MODEL
    os.environ['LLM_BASE_URL'] = 'https://api.deepseek.com'
    
    # 创建工作目录
    os.makedirs(WORKSPACE, exist_ok=True)
    
    # 检查API密钥
    if API_KEY == "your-deepseek-api-key-here":
        print("❌ 请先设置你的DeepSeek API密钥！")
        print("在代码顶部修改 API_KEY 变量")
        return False
    
    return True

async def run_task():
    """执行任务"""
    try:
        from opendevin.llm.llm import LLM
        from opendevin.core.config import LLMConfig
        
        print("🤖 OpenDevin 超简单运行器")
        print("=" * 50)
        print(f"📝 任务: {TASK}")
        print(f"🔧 模型: {MODEL}")
        print(f"📁 工作目录: {WORKSPACE}")
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
你是一个专业的AI编程助手。用户给你一个任务，你需要分析并提供完整的解决方案。

工作目录: {WORKSPACE}
任务: {TASK}

请按以下格式回复：

1. 任务分析：简要分析这个任务的要求
2. 解决方案：提供详细的实现方案
3. 代码实现：如果需要编写代码，请提供完整的代码
4. 使用说明：如何使用你创建的代码

如果需要创建文件，请在代码块前注明文件名，格式如下：
```python
# 文件名: calculator.py
你的代码内容
```

请用中文回复。
"""
        
        print("💭 AI正在思考中...")
        
        # 调用LLM
        response = await llm.acompletion(
            messages=[{"role": "user", "content": prompt}],
            model=MODEL
        )
        
        result = response.choices[0].message.content
        
        print("🤖 AI助手回复:")
        print("-" * 50)
        print(result)
        print("-" * 50)
        
        # 自动创建文件
        if AUTO_CREATE_FILES and "```" in result:
            print("\n📄 检测到代码，正在自动创建文件...")
            await create_files_from_response(result)
        
        print(f"\n✅ 任务完成！")
        print(f"📁 查看结果: {os.path.abspath(WORKSPACE)}")
        
    except Exception as e:
        print(f"❌ 错误: {e}")
        print("\n💡 可能的解决方案:")
        print("1. 检查API密钥是否正确")
        print("2. 检查网络连接")
        print("3. 安装必要依赖: pip install litellm fastapi python-dotenv")

async def create_files_from_response(response_text):
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
                filename = f"generated_code_{file_count}.py"
            elif lang == 'javascript':
                filename = f"generated_code_{file_count}.js"
            elif lang == 'html':
                filename = f"generated_code_{file_count}.html"
            elif lang == 'css':
                filename = f"generated_code_{file_count}.css"
            else:
                filename = f"generated_code_{file_count}.txt"
        else:
            filename = filename.strip()
        
        # 创建文件
        filepath = os.path.join(WORKSPACE, filename)
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(code.strip())
            print(f"  ✅ 已创建: {filename}")
        except Exception as e:
            print(f"  ❌ 创建失败 {filename}: {e}")

def main():
    """主函数"""
    print("🚀 启动中...")
    
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