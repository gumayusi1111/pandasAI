# test_direct_openai_official.py (请将此内容保存到您的 1.py 文件并运行)
import os
import openai
from dotenv import load_dotenv
import pathlib

print(f"--- Direct OpenAI Library Test (TARGETING OFFICIAL DEEPSEEK API) ---")
print(f"Python script's current working directory: {os.getcwd()}")

env_path_to_try = pathlib.Path(os.getcwd()) / ".env"
print(f"Attempting to load .env file from: {env_path_to_try}")
# 确保 override=True 以便 .env 文件中的设置能够覆盖任何已存在的同名 shell 环境变量
loaded_successfully = load_dotenv(dotenv_path=env_path_to_try, override=True)

if loaded_successfully:
    print(f".env file loaded successfully from {env_path_to_try}.")
else:
    print(f"警告：未能从 {env_path_to_try} 加载 .env 文件。")

# 从 .env 文件加载您的 API Key
api_key_from_env = os.getenv("DEEPSEEK_API_KEY")

# --- <<< 关键修改：直接使用 DeepSeek 官方 API Base URL >>> ---
base_url_for_official_test = "https://api.deepseek.com/" 

print(f"DEEPSEEK_API_KEY loaded from env: {'********' if api_key_from_env else 'NOT LOADED'}")
print(f"Using OFFICIAL DeepSeek API Base URL: {base_url_for_official_test}")

if not api_key_from_env:
    print("严重错误：未能从环境变量加载 API Key。程序退出。")
    exit()

# --- <<< 关键修改：使用一个官方确认的 DeepSeek 模型名称 >>> ---
# 常见的官方模型有 'deepseek-chat' (用于通用对话) 或 'deepseek-coder'。
# 我们先用 'deepseek-chat'。如果失败，您可以尝试您之前用的 'deepseek-r1' (如果确定它是官方名称)。
model_to_test_official = "deepseek-chat" 
print(f"Using OFFICIAL Model Name: {model_to_test_official}")

try:
    print(f"OpenAI library version: {openai.__version__}")

    # --- <<< 关键修改：对于官方API，通常不需要或应移除自定义请求头 >>> ---
    # 官方API通常对User-Agent等不那么敏感。
    custom_headers_for_official = {} # 从空字典开始，不设置自定义请求头
    # 如果需要，可以尝试添加一个通用的 User-Agent:
    # custom_headers_for_official = {"User-Agent": "MyPythonTestScript/1.0"}

    print(f"Using custom headers for OpenAI client (for official API): {custom_headers_for_official}")

    client = openai.OpenAI(
        api_key=api_key_from_env,
        base_url=base_url_for_official_test, # 使用官方 Base URL
        default_headers=custom_headers_for_official # 传递空的或最小化的自定义请求头
    )

    print(f"OpenAI client configured with base_url: {client.base_url}")
    # openai 库会自动在其后附加 /v1/chat/completions
    print(f"The library will attempt to POST to a path like '{str(client.base_url).rstrip('/')}/v1/chat/completions'")

    completion_response = client.chat.completions.create(
        model=model_to_test_official,
        messages=[
            {"role": "user", "content": f"Hello DeepSeek official API from OpenAI library test!"}
        ]
    )

    if hasattr(completion_response, 'choices'):
        print("\n来自 DeepSeek 官方 API (通过 OpenAI library) 的回答：")
        print(completion_response.choices[0].message.content)
        print("--- 官方 API 测试成功 ---")
    else:
        print("\n警告：对官方 API 的调用返回了未预期的对象类型。")
        print("原始响应对象：")
        print(completion_response)

except openai.AuthenticationError as e:
    print(f"\n官方 API 测试 - 认证错误 (例如 401): {e.status_code} - {e.message}")
    if hasattr(e, 'body') and e.body: print(f"错误详情 (body): {e.body}")
    print("这表示您的 API Key 对于 DeepSeek 官方 API 无效，或者对请求的模型无效。")
except openai.NotFoundError as e: 
    print(f"\n官方 API 测试 - 未找到错误 (404): {e.status_code} - {e.message}")
    if hasattr(e, 'body') and e.body: print(f"错误详情 (body): {e.body}")
    print("这可能意味着模型名称对于官方 API 不正确，或者 API 路径错误（可能性较小）。")
except openai.RateLimitError as e: # 捕获官方API可能返回的速率限制错误
    print(f"\n官方 API 测试 - 速率限制错误: {e.status_code} - {e.message}")
    if hasattr(e, 'body') and e.body: print(f"错误详情 (body): {e.body}")
except openai.APIConnectionError as e:
    print(f"\n官方 API 测试 - API 连接错误: {e}")
    print("无法连接到 DeepSeek 官方 API。请检查网络或确认 URL 是否正确。")
except openai.APIStatusError as e: 
    print(f"\n官方 API 测试 - API 状态错误 (代码: {e.status_code}): {e.message}")
    if hasattr(e, 'body') and e.body: print(f"错误详情 (body): {e.body}")
except Exception as e:
    print(f"\n官方 API 测试 - 发生意外错误: {type(e).__name__} - {e}")
    import traceback
    traceback.print_exc()
finally:
    print(f"--- End of Direct OpenAI Library Test (OFFICIAL DEEPSEEK API) ---")