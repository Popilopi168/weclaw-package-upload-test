import os
from dotenv import load_dotenv

# 加载脚本刚刚自动生成的 .env 文件
load_dotenv()

api_key = os.getenv("API_KEY")

print("====================================")
print("🚀 WeClaw Bot 启动成功！。")
print("这是本地测试版本")
print(f"🔑 检测到注入的 API Key: {api_key[:5]}********")
print("====================================")