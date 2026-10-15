import os
import requests
from langchain_core.tools import tool

@tool
def nginx_health_check() -> str:
    """检查 Nginx 健康状态：通过 HTTP 请求验证可访问性，并确认返回的是 Nginx 默认页。"""
    url = os.getenv("NGINX_URL", "http://localhost:8080")

    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            is_nginx = ("Welcome to nginx" in response.text) or ("nginx" in response.text.lower())
            page_note = "页面标题: Welcome to nginx!" if is_nginx else "页面内容未包含 Nginx 特征信息"
            return (
                "Nginx 健康检查\n"
                f"- 连接状态: 正常 ({url})\n"
                f"- HTTP 状态码: {response.status_code}\n"
                f"- {page_note}"
            )
        else:
            return f"Nginx 健康检查未通过 ({url}): HTTP 状态码 {response.status_code}"
    except Exception as e:
        return f"Nginx 连接失败 ({url}): {e}"
