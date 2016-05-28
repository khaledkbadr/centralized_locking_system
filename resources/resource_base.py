from abc import ABCMeta
from collections import deque
from datetime import timedelta


class ResourceBase(metaclass=ABCMeta):
    """Base class to add and keep state of resource availability"""
    locked = False
    acquirer = None
    queue = deque()

    def __init__(self, timeout_in_seconds=10.0):
        self.timeout_in_seconds = timedelta(seconds=timeout_in_seconds)

    @classmethod
    def lock_resource(cls, acquirer):
        cls.locked = True
        cls.acquirer = acquirer

    @classmethod
    def get_acquirer(cls):
        return cls.acquirer

    @classmethod
    def resource_locked(cls):
        return cls.locked

    @classmethod
    def add_request(cls, caller_id):
        """Add request to queue"""
        cls.queue.appendleft(caller_id)

    @classmethod
    def remove_request(cls, caller_id):
        try:
            if caller_id == deque[-1]:
                cls.queue.pop()
            else:
                cls.queue.remove(caller_id)
        except IndexError:
            print('Queue is empty')

    @classmethod
    def request_queue_empty(cls):
        return bool(cls.queue)

    @classmethod
    def last_request_time(cls):
        return cls.queue[-1] if cls.queue else None

    @classmethod
    def next(cls):
        return cls.queue[-1]
