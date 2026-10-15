import redis
import sys

def check_redis():
    try:
        # 连接本机的 Redis（端口映射到了 6379）
        r = redis.Redis(host='localhost', port=6379, decode_responses=True, socket_timeout=5)
        # 发送 PING 命令
        if r.ping():
            print("✅ Redis 连接成功！")
            
            # 获取一些核心信息
            info = r.info()
            print(f"版本: {info.get('redis_version')}")
            print(f"运行模式: {info.get('redis_mode')}")
            print(f"已用内存: {info.get('used_memory_human')}")
            print(f"当前连接数: {info.get('connected_clients')}")
            print(f"Key 数量: {r.dbsize()}")
            
            # 测试读写
            r.set("test_key", "hello_from_ops_agent")
            print(f"测试读取: {r.get('test_key')}")
    except Exception as e:
        print(f"❌ Redis 连接失败: {e}")
        sys.exit(1)

if __name__ == "__main__":
    check_redis()
