import redis

def check_redis_connection(host='redis', port=6379):
    try:
        client = redis.Redis(host=host, port=port)
        # Ping returns True if Redis server responds
        if client.ping():
            print("✅ Redis is reachable!")
            return True
        else:
            print("❌ Redis did not respond to ping.")
            return False
    except redis.ConnectionError:
        print("❌ Could not connect to Redis server.")
        return False

if __name__ == "__main__":
    check_redis_connection()
