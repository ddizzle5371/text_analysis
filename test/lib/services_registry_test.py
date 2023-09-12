from src.lib.service_registry import ServiceRegistry
from threading import Thread
from unittest import mock
import pytest

@mock.patch("src.lib.service_registry.redis.Redis")
def test_singleton_instance(mock_create):
    mock_create.return_value = True
    instances = []

    def create_instance():
        instances.append(ServiceRegistry('localhost', '6379'))

    threads = [Thread(target=create_instance) for _ in range(5)]

    for t in threads:
        t.start()
    for t in threads:
        t.join()

    assert all(instance is instances[0] for instance in instances)
