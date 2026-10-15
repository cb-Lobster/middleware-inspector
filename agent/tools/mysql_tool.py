import os
import pymysql
from langchain_core.tools import tool

@tool
def mysql_health_check() -> str:
    """检查 MySQL 健康状态：连通性、当前/最大连接数、运行时长、慢查询总数、累计查询数。"""
    host = os.getenv("MYSQL_HOST", "localhost")
    port = int(os.getenv("MYSQL_PORT", 3306))
    user = os.getenv("MYSQL_USER", "root")
    password = os.getenv("MYSQL_PASSWORD", "test123")

    conn = None
    try:
        conn = pymysql.connect(
            host=host, port=port, user=user,
            password=password, connect_timeout=5,
        )
        cursor = conn.cursor()

        def get_status(name):
            cursor.execute("SHOW STATUS LIKE %s", (name,))
            row = cursor.fetchone()
            return row[1] if row else "N/A"

        def get_var(name):
            cursor.execute("SHOW VARIABLES LIKE %s", (name,))
            row = cursor.fetchone()
            return row[1] if row else "N/A"

        return (
            "MySQL 健康检查\n"
            f"- 连接状态: 正常 ({host}:{port})\n"
            f"- 当前连接数: {get_status('Threads_connected')}\n"
            f"- 最大连接数: {get_var('max_connections')}\n"
            f"- 运行时长: {get_status('Uptime')} 秒\n"
            f"- 慢查询总数: {get_status('Slow_queries')}\n"
            f"- 已处理查询: {get_status('Questions')}"
        )
    except Exception as e:
        return f"MySQL 连接失败 ({host}:{port}): {e}"
    finally:
        if conn:
            conn.close()
