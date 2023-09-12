from threading import Lock
import redis


class ServiceRegistry:
    """
    Redis client wrapper that ensures instantiation of a single instance of ServiceRegistry.
    Each operation is synchronized with lock.
    """
    _instance = None
    _lock = Lock()

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super(ServiceRegistry, cls).__new__(cls)
        return cls._instance

    def __init__(self, host: str, port: str):
        self.redis_client = redis.Redis(host=host, port=port)

    def set(self, service_name: str, service_url: str):
        with self._lock:
            self.redis_client.set(service_name, service_url)

    def get(self, service_name: str):
        with self._lock:
            return self.redis_client.get(service_name)

    def delete(self, service_name: str):
        with self._lock:
            self.redis_client.delete(service_name)

    def list_all(self):
        with self._lock:
            return {k: self.redis_client.get(k) for k in self.redis_client.keys()}
