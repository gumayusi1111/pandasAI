import os
import json
from flask import Flask, render_template, request, jsonify, send_from_directory
from collections import deque
import pandas as pd
import logging
import time

from .core import generate_pandas_code

# Configure logging
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)

# 历史记录文件路径
HISTORY_FILE = os.path.join(os.path.dirname(__file__), 'data', 'history.json')

# 确保数据目录存在
os.makedirs(os.path.dirname(HISTORY_FILE), exist_ok=True)

# 从文件加载历史记录，如果文件不存在则创建空列表
def load_history():
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
                return deque(json.load(f), maxlen=15)
        except Exception as e:
            logger.error(f"加载历史记录失败: {str(e)}")
    return deque(maxlen=15)

# 保存历史记录到文件
def save_history():
    try:
        with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
            json.dump(list(HISTORY), f, ensure_ascii=False, indent=2)
    except Exception as e:
        logger.error(f"保存历史记录失败: {str(e)}")

# 加载历史记录
HISTORY = load_history()

# Supported file formats
SUPPORTED_FORMATS = {
    'csv': pd.read_csv,
    'xlsx': pd.read_excel,
    'xls': pd.read_excel,
    'json': pd.read_json,
    'parquet': pd.read_parquet,
    'feather': pd.read_feather,
    'pickle': lambda f: pd.read_pickle(f),
    'pkl': lambda f: pd.read_pickle(f)
}

@app.route('/')
def index():
    """Render the main page"""
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    """Generate pandas code from natural language query and CSV data"""
    try:
        # Get form data
        model_name = request.form.get('model')
        query = request.form.get('query')
        is_test = request.form.get('is_test') == 'true'
        
        # Log model selection
        logger.info(f"模型已选择: {model_name} {'(测试模式)' if is_test else ''}")
        
        # Get file if it was uploaded
        csv_file = None
        file_name = None
        if 'csv_file' in request.files:
            file = request.files['csv_file']
            if file.filename != '':
                # Save the file temporarily
                temp_path = os.path.join(os.path.dirname(__file__), 'temp_uploads')
                os.makedirs(temp_path, exist_ok=True)
                filepath = os.path.join(temp_path, file.filename)
                file.save(filepath)
                csv_file = filepath
                file_name = file.filename
                
                # Log file upload
                file_ext = file.filename.split('.')[-1].lower()
                logger.info(f"文件已上传: {file.filename} (格式: {file_ext})")
        
        # Generate pandas code
        result = generate_pandas_code(csv_file, query, model_name)
        
        # Save to history
        history_item = {
            'timestamp': result['timestamp'],
            'query': query,
            'model': model_name,
            'code': result['code'],
            'file': file_name,
            'tokens': result.get('tokens', 0)
        }
        HISTORY.appendleft(history_item)
        
        # 保存历史记录到文件
        save_history()
        
        # Clean up temporary file
        if csv_file and os.path.exists(csv_file):
            os.remove(csv_file)
            
        return jsonify(result)
    
    except Exception as e:
        logger.error(f"生成代码时出错: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/history', methods=['GET'])
def get_history():
    """Get the query history"""
    return jsonify(list(HISTORY))

@app.route('/clear_history', methods=['POST'])
def clear_history():
    """Clear the query history"""
    HISTORY.clear()
    # 清空后保存空历史记录到文件
    save_history()
    logger.info("历史记录已清除")
    return jsonify({'status': 'success'})

@app.route('/supported_formats', methods=['GET'])
def get_supported_formats():
    """Get the list of supported file formats"""
    return jsonify(list(SUPPORTED_FORMATS.keys()))

# 图表功能已禁用，不再提供图表文件服务
# @app.route('/exports/charts/<path:filename>')
# def serve_chart(filename):
#     """Serve generated chart images"""
#     charts_dir = os.path.join(os.getcwd(), 'exports', 'charts')
#     return send_from_directory(charts_dir, filename)

if __name__ == '__main__':
    # Create temp uploads directory if it doesn't exist
    temp_path = os.path.join(os.path.dirname(__file__), 'temp_uploads')
    os.makedirs(temp_path, exist_ok=True)
    
    # Run the app
    app.run(debug=True, port=8080) # 使用8080端口而不是默认的5000 