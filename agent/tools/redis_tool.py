import redis
import os
from langchain_core.tools import tool

@tool
def redis_health_check() -> str:
    """检查 Redis 健康状态：连接、内存、连接数、key 数量、慢查询数"""
    try:
        r = redis.Redis(
            host=os.getenv("REDIS_HOST", "localhost"),
            port=int(os.getenv("REDIS_PORT", 6379)),
            decode_responses=True,
            socket_timeout=5
        )
        info = r.info()
        hits = info.get("keyspace_hits", 0)
        misses = info.get("keyspace_misses", 0)
        total = hits + misses
        hit_rate = f"{hits / total * 100:.2f}%" if total > 0 else "N/A"

        result = f"""
Redis 健康检查
- 版本: {info.get('redis_version')}
- 连接状态: 正常
- 已用内存: {info.get('used_memory_human')}
- 当前连接数: {info.get('connected_clients')}
- 命中率: {hit_rate}
- key数量: {r.dbsize()}
- 慢查询数: {len(r.slowlog_get(10))}
"""
        return result
    except Exception as e:
        return f"Redis 连接失败: {e}"
