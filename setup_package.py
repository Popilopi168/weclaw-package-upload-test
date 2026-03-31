import os
import subprocess
import platform
from pathlib import Path

def setup_openclaw_package(api_key: str = None, mac_permission_confirmed: bool = False) -> str:
    """
    [核心意图识别说明书]
    当用户想要下载、安装、配置我们的 package 或初始化本地开发环境时，必须调用此工具。
    
    参数说明:
    - api_key (str, optional): 用户的 API Key。如果用户在聊天中未提供，则为空。
    - mac_permission_confirmed (bool, optional): 用户是否已经确认开启了 Mac 的辅助功能权限。默认为 False。
    """
    
    repo_url = "https://github.com/Popilopi168/weclaw-package-upload-test"
    target_dir = "weclaw-package-upload-test"
    work_dir = Path(target_dir)

    # ==========================================
    # 第一步：处理 Mac 权限 (拦截与交互)
    # ==========================================
    if platform.system() == "Darwin" and not mac_permission_confirmed:
        # 直接用 AppleScript 帮用户打开 Mac 的隐私设置界面
        try:
            apple_script = 'open "x-apple.systempreferences:com.apple.preference.security?Privacy_Accessibility"'
            subprocess.run(apple_script, shell=True, check=False)
        except Exception:
            pass 
        
        # 将控制权交还给 LLM，让它去跟用户沟通
        return (
            "STATUS: PAUSED. "
            "请以助手的口吻告诉用户：'为了让自动化工具正常工作，我已经为您打开了 Mac 的系统设置。"
            "请在【隐私与安全性 -> 辅助功能】中为终端（或当前应用）开启权限。开启完成后，请回复我【已开启】。'"
        )

    # ==========================================
    # 第二步：处理 API Key (路由逻辑)
    # ==========================================
    if not api_key:
         return (
             "STATUS: PAUSED. "
             "请告诉用户：'权限确认完毕！最后一步，我需要您的 API Key 来完成环境配置。"
             "请直接在聊天框中将 Key 发送给我。'"
         )

    # ==========================================
    # 第三步：Clone & uv 配置 Python 环境
    # ==========================================
    try:
        # 1. 拉取代码库
        if not os.path.exists(target_dir):
            print("🔄 [System] 正在拉取代码库...") 
            subprocess.run(["git", "clone", repo_url], check=True, capture_output=True)
        else:
            print("✅ [System] 代码库已存在，跳过 Clone。")

        # 2. 极速配置依赖 (使用 uv)
        print("⚡ [System] 正在使用 uv 创建虚拟环境并安装依赖...")
        
        # uv venv 会在当前目录下创建 .venv
        subprocess.run(["uv", "venv"], cwd=work_dir, check=True, capture_output=True)
        
        # uv pip 会自动识别并使用刚刚创建的 .venv
        subprocess.run(["uv", "pip", "install", "-r", "requirements.txt"], cwd=work_dir, check=True, capture_output=True)

        # 3. 路由 API Key
        print("🔑 [System] 正在配置环境变量 .env ...")
        env_path = work_dir / ".env"
        with open(env_path, "w") as f:
            f.write(f"API_KEY={api_key}\n")
            f.write("ENV=development\n") # 可以顺手配点其他的

        # ==========================================
        # 第四步：成功反馈
        # ==========================================
        return (
            "STATUS: SUCCESS. "
            "配置全部完成！请用热情专业的语气告诉用户：代码已成功拉取，Python 环境和依赖已通过 uv 极速配置完毕，"
            "API Key 也已安全写入 `.env` 文件。现在已经可以使用weclaw了。"
        )

    except subprocess.CalledProcessError as e:
        error_msg = e.stderr.decode('utf-8') if e.stderr else str(e)
        return f"STATUS: FAILED. 运行系统命令出错。请告诉用户安装失败，并简述错误日志：{error_msg}"
    except Exception as e:
        return f"STATUS: FAILED. 发生未知错误：{str(e)}"