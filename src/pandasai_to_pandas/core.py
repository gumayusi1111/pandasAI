import os
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv
from pandasai import Agent
from pandasai.llm.local_llm import LocalLLM
import logging
import re

# Configure logging
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv(override=True)
API_KEY = os.getenv("DEEPSEEK_API_KEY")
API_BASE = os.getenv("DEEPSEEK_API_BASE")  # Should be "https://dseek.aikeji.vip/v1/"

# Dictionary of file readers for different formats
FILE_READERS = {
    'csv': pd.read_csv,
    'xlsx': pd.read_excel,
    'xls': pd.read_excel,
    'json': pd.read_json,
    'parquet': pd.read_parquet,
    'feather': pd.read_feather,
    'pickle': lambda f: pd.read_pickle(f),
    'pkl': lambda f: pd.read_pickle(f)
}

def clean_pandasai_code(code):
    """
    清理PandasAI生成的代码，移除结果格式化部分。
    
    Args:
        code (str): PandasAI生成的代码
        
    Returns:
        str: 清理后的pandas代码
    """
    if not code:
        return code
    
    # 用简单的字符串分割检查并移除result字典
    if "result = {" in code:
        lines = code.split("\n")
        result_line_index = -1
        
        # 查找包含result字典的行
        for i, line in enumerate(lines):
            if "result = {" in line:
                result_line_index = i
                break
        
        if result_line_index >= 0:
            # 保留result行之前的代码
            cleaned_code = "\n".join(lines[:result_line_index])
            
            # 如果代码最后一行是数据处理逻辑，添加print语句来代替result输出
            last_line = cleaned_code.strip().split("\n")[-1]
            
            # 检查最后一行是否包含一个变量赋值，我们可以打印这个变量
            if "=" in last_line and not last_line.strip().startswith("#") and not any(keyword in last_line for keyword in ["if", "for", "while", "def", "class"]):
                var_name = last_line.split("=")[0].strip()
                if var_name and not var_name.startswith("#"):
                    cleaned_code += f"\n\n# 打印结果\nprint({var_name})"
            
            cleaned_code += "\n\n# 注意: 已移除PandasAI结果格式化代码。\n# 上面的代码是标准Pandas代码，可以直接在Python环境中运行。"
            return cleaned_code.strip()
    
    # 如果没有找到result字典，返回原始代码
    return code

def generate_pandas_code(csv_file_path, query, model_name="deepseek-chat"):
    """
    Generate pandas code using PandasAI.
    
    Args:
        csv_file_path (str): Path to the data file (CSV, Excel, JSON, etc.)
        query (str): Natural language query
        model_name (str): Model name, either "deepseek-chat" or "deepseek-r1"
        
    Returns:
        dict: Result containing the generated code and metadata
    """
    result = {
        'timestamp': datetime.now().isoformat(),
        'code': None,
        'error': None,
        'tokens': 0  # 添加tokens字段
    }
    
    # Validate model name
    valid_models = ["deepseek-chat", "deepseek-r1"]
    if model_name not in valid_models:
        result['error'] = f"Invalid model name. Choose from: {', '.join(valid_models)}"
        return result
    
    # Check API keys
    if not API_KEY or not API_BASE:
        result['error'] = "API key or base URL not found in environment variables"
        return result
    
    # Use sample data if no file is provided
    if not csv_file_path or not os.path.exists(csv_file_path):
        logger.info("使用示例数据集")
        # Create a sample dataset
        sample_df_data = {
            "产品名称": ["笔记本", "手机", "平板", "手表", "耳机", "游戏机", "显示器"],
            "销量": [120, 250, 180, 300, 450, 90, 150],
            "单价": [5000, 3000, 2000, 1500, 500, 2500, 1800],
            "类别": ["电子", "电子", "电子", "穿戴", "音频", "娱乐", "电子"]
        }
        df = pd.DataFrame(sample_df_data)
    else:
        # Load data based on file extension
        try:
            file_ext = os.path.splitext(csv_file_path)[1][1:].lower()
            
            if file_ext in FILE_READERS:
                logger.info(f"使用 {file_ext} 格式读取文件")
                reader_func = FILE_READERS[file_ext]
                df = reader_func(csv_file_path)
            else:
                # Default to CSV if extension not recognized
                logger.warning(f"未知文件格式 '{file_ext}'，尝试以 CSV 格式读取")
                df = pd.read_csv(csv_file_path)
                
            logger.info(f"成功加载数据: {df.shape[0]} 行, {df.shape[1]} 列")
            
        except Exception as e:
            logger.error(f"加载文件时出错: {str(e)}")
            result['error'] = f"Error loading file: {str(e)}"
            return result
    
    # Initialize LLM and PandasAI Agent
    try:
        logger.info(f"使用模型 {model_name} 初始化 LLM")
        llm = LocalLLM(
            api_key=API_KEY,
            api_base=API_BASE,
            model=model_name
        )
        
        pandas_ai_agent = Agent([df], config={"llm": llm, "verbose": False, "save_logs": False})
        
        # Run the query
        logger.info(f"发送查询: '{query}'")
        response = pandas_ai_agent.chat(query)
        
        # Get the generated code
        if hasattr(pandas_ai_agent, 'last_code_executed'):
            # Clean the code to remove PandasAI result formatting
            raw_code = pandas_ai_agent.last_code_executed
            cleaned_code = clean_pandasai_code(raw_code)
            
            result['code'] = cleaned_code
            result['raw_code'] = raw_code  # 保存原始代码，以便调试
            
            # 估算tokens数量 (简单估算，每个字符约0.25 tokens，每行代码约5 tokens)
            if cleaned_code:
                char_count = len(cleaned_code)
                line_count = cleaned_code.count('\n') + 1
                estimated_tokens = int(char_count * 0.25 + line_count * 5)
                result['tokens'] = estimated_tokens
                logger.info(f"生成的代码估计包含 {estimated_tokens} tokens")
            
            logger.info("成功生成并清理代码")
        else:
            result['error'] = "No code was generated"
            logger.warning("未生成代码")
            
    except Exception as e:
        logger.error(f"代码生成出错: {str(e)}")
        result['error'] = f"Error during code generation: {str(e)}"
    
    return result