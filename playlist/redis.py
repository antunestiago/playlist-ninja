import redis


class RedisClient:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.redis_conn = redis.Redis(host='localhost', port=6379, db=0)
        return cls._instance

    def set_music_state(self, music_id: str, state):
        self.redis_conn.set(music_id, state)
        self.show_all_values()

    def get_music_state(self, music_id):
        return self.redis_conn.get(music_id)

    def show_all_values(self):
        keys = self.redis_conn.keys()
        for key in keys:
            value = self.redis_conn.get(key)
            print(f'{key.decode()}: {value.decode()}')