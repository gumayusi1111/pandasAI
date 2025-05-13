import os
import pandas as pd
from dotenv import load_dotenv
from pandasai import Agent
from pandasai.llm.local_llm import LocalLLM

# --------------------------- 脚本开始 ---------------------------

def analyze_my_data(csv_file_path: str, question_to_ask: str):
    """
    使用 PandasAI 加载 CSV 数据、提问并打印结果和生成的代码。
    """
    # 1. 加载环境变量 (从中转服务获取 API Key 和 Base URL)
    load_dotenv(override=True) 
    api_key = os.getenv("DEEPSEEK_API_KEY")
    api_base = os.getenv("DEEPSEEK_API_BASE") # 应为 "https://dseek.aikeji.vip/v1/"
    model_name = "deepseek-chat" # 或 "deepseek-chat"

    if not api_key or not api_base:
        print("错误：未能从 .env 文件加载 DEEPSEEK_API_KEY 或 DEEPSEEK_API_BASE。")
        print("请确保 .env 文件在脚本当前工作目录，并包含正确的配置。")
        print("例如：")
        print('DEEPSEEK_API_KEY="sk-your_proxy_key_here"')
        print('DEEPSEEK_API_BASE="https://dseek.aikeji.vip/v1/"')
        return

    print(f"--- PandasAI 分析开始 ---")
    print(f"使用 API Base: {api_base}")
    print(f"使用模型: {model_name}")

    # 2. 从 CSV 文件加载数据
    try:
        print(f"\n正在从 '{csv_file_path}' 加载数据...")
        df = pd.read_csv(csv_file_path)
        print("数据加载成功。DataFrame 前3行：")
        print(df.head(3))
    except FileNotFoundError:
        print(f"错误：文件 '{csv_file_path}' 未找到。请检查文件路径。")
        return
    except Exception as e:
        print(f"加载数据 '{csv_file_path}' 时发生错误: {e}")
        return

    # 3. 初始化 LLM 和 PandasAI Agent
    try:
        print("\n正在初始化 LLM 和 PandasAI Agent...")
        llm = LocalLLM(
            api_key=api_key,
            api_base=api_base,
            model=model_name
        )
        
        pandas_ai_agent = Agent([df], config={"llm": llm, "verbose": False, "save_logs": False})
        print("PandasAI Agent 初始化成功。")

    except Exception as e:
        print(f"初始化 LLM 或 PandasAI Agent 时发生错误: {e}")
        import traceback
        traceback.print_exc()
        return

    # 4. 提出问题并获取结果
    print(f"\n向 PandasAI 提出问题: \"{question_to_ask}\"")
    try:
        response = pandas_ai_agent.chat(question_to_ask)

        print("\n>>> PandasAI 的回答：")
        print(response)

        if hasattr(pandas_ai_agent, 'last_code_executed'):
            print("\n>>> PandasAI 生成的 Pandas 代码：")
            print(pandas_ai_agent.last_code_executed)
        else:
            print("\n未能获取到 last_code_executed 属性。")

    except Exception as e:
        print(f"PandasAI 处理查询时发生错误: {e}")
        import traceback
        traceback.print_exc()

    print("\n--- PandasAI 分析结束 ---")

# --------------------------- 主程序执行部分 ---------------------------
if __name__ == '__main__':
    # ----------- 您需要修改以下两行 -----------
    # 1. 指定您的 CSV 文件路径
    my_data_file = 'your_data.csv'  # <--- 将 'your_data.csv' 替换为您实际的 CSV 文件名和路径

    # 2. 输入您想对数据提出的问题
    my_question = '哪个类别的产品总销量最高？' # <--- 替换为您想问的问题
    # ----------- 修改结束 -----------

    # (可选) 自动创建一个示例 CSV 文件用于快速测试（如果指定的文件不存在）
    if not os.path.exists(my_data_file):
        print(f"提示: 文件 '{my_data_file}' 未找到，将创建一个示例 'sample_data.csv' 用于演示。")
        my_data_file = 'sample_data.csv' # 如果您的文件不存在，脚本会使用这个并创建它
        if not os.path.exists(my_data_file): # 避免重复创建
            sample_df_data = {
                "产品名称": ["笔记本", "手机", "平板", "手表", "耳机", "游戏机", "显示器"],
                "销量": [120, 250, 180, 300, 450, 90, 150],
                "单价": [5000, 3000, 2000, 1500, 500, 2500, 1800],
                "类别": ["电子", "电子", "电子", "穿戴", "音频", "娱乐", "电子"]
            }
            pd.DataFrame(sample_df_data).to_csv(my_data_file, index=False)
            print(f"已创建示例文件 '{my_data_file}'。")

    analyze_my_data(csv_file_path=my_data_file, question_to_ask=my_question)

# --------------------------- 脚本结束 ---------------------------