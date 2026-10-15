import requests
import sys

def check_nginx():
    try:
        # 我们从宿主机 8080 端口访问 Nginx 容器
        response = requests.get("http://localhost:8080", timeout=5)
        
        if response.status_code == 200:
            print("✅ Nginx 连接成功！")
            print(f"HTTP 状态码: {response.status_code}")
            # 检查网页标题，验证返回的是不是真正的 Nginx
            if "Welcome to nginx" in response.text or "nginx" in response.text.lower():
                print("页面标题: Welcome to nginx!")
            else:
                print("页面内容未包含 Nginx 特征信息")
        else:
            print(f"❌ Nginx 返回异常状态码: {response.status_code}")
    except Exception as e:
        print(f"❌ Nginx 连接失败: {e}")
        sys.exit(1)

if __name__ == "__main__":
    check_nginx()
