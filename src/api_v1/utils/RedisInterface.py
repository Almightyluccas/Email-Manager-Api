import redis
from .config import redis_host, redis_port, redis_password


class RedisInterface:

    def __init__(self):
        self.redis_client = redis.StrictRedis(
            host=redis_host,
            port=redis_port,
            password=redis_password,
            decode_responses=True
        )

    def __enter__(self):
        print('user connected to redis database')
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.redis_client.close()
        print('user has logged out of redis')

    def get_fetched_email_ids(self, email):
        key = f"fetched_uid:{email}"
        ids = self.redis_client.hget(key, 'uids')
        return ids.split() if ids else []

    def put_fetched_email_ids(self, email: str, ids: set):
        try:
            key = f"fetched_uid:{email}"
            self.redis_client.hdel(key, 'uids')

            ids_str = [str(uid) for uid in ids]
            self.redis_client.hset(key, 'uids', ' '.join(ids_str))

            return 'Fetched email IDs updated successfully'
        except Exception as e:
            return f'Error: {str(e)}'
