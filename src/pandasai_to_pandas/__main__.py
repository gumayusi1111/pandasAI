import os
from dotenv import load_dotenv
from .app import app

def main():
    """
    Main entry point for the application.
    """
    # Load environment variables
    load_dotenv(override=True)
    
    # Check for API keys
    api_key = os.getenv("DEEPSEEK_API_KEY")
    api_base = os.getenv("DEEPSEEK_API_BASE")
    
    if not api_key or not api_base:
        print("警告：未能从 .env 文件加载 DEEPSEEK_API_KEY 或 DEEPSEEK_API_BASE。")
        print("请确保 .env 文件在脚本当前工作目录，并包含正确的配置。")
        print("例如：")
        print('DEEPSEEK_API_KEY="sk-your_proxy_key_here"')
        print('DEEPSEEK_API_BASE="https://dseek.aikeji.vip/v1/"')
    
    # Create temp uploads directory if it doesn't exist
    temp_path = os.path.join(os.path.dirname(__file__), 'temp_uploads')
    os.makedirs(temp_path, exist_ok=True)
    
    # Run the app
    host = os.getenv("HOST", "127.0.0.1")
    port = int(os.getenv("PORT", 5000))
    debug = os.getenv("DEBUG", "False").lower() in ("true", "1", "t")
    
    print(f"Starting PandasAI to Pandas Converter on http://{host}:{port}")
    app.run(host=host, port=port, debug=debug)

if __name__ == "__main__":
    main() 