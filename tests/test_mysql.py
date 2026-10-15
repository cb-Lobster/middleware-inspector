import pymysql
import sys

def check_mysql():
    try:
        # 连本地 3306 端口，密码是我们在 docker-compose.yml 里设置的 test123
        conn = pymysql.connect(
            host='localhost',
            port=3306,
            user='root',
            password='test123',
            connect_timeout=5
        )
        print("✅ MySQL 连接成功！")

        cursor = conn.cursor()

        # 定义个小函数快速查状态
        def get_status(name):
            cursor.execute(f"SHOW STATUS LIKE '{name}'")
            row = cursor.fetchone()
            return row[1] if row else "N/A"

        def get_var(name):
            cursor.execute(f"SHOW VARIABLES LIKE '{name}'")
            row = cursor.fetchone()
            return row[1] if row else "N/A"

        print(f"当前连接数: {get_status('Threads_connected')}")
        print(f"最大连接数: {get_var('max_connections')}")
        print(f"运行时长: {get_status('Uptime')} 秒")
        print(f"慢查询总数: {get_status('Slow_queries')}")
        print(f"已处理查询: {get_status('Questions')}")

        conn.close()
    except Exception as e:
        print(f"❌ MySQL 连接失败: {e}")
        sys.exit(1)

if __name__ == "__main__":
    check_mysql()
