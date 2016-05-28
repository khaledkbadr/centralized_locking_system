from abc import ABCMeta
from collections import deque
from datetime import timedelta


class ResourceBase(metaclass=ABCMeta):
    """Base class to add and keep state of resource availability"""
    locked = False  # true if resource is locked
    acquirer = None  # holds the id of the client holds the resource
    queue = deque()  # hold multiple requests to lock resource if it's already been locked

    def __init__(self, timeout_in_seconds=30.0):
        self.timeout_in_seconds = timedelta(seconds=timeout_in_seconds)

    @classmethod
    def lock_resource(cls, acquirer):
        """Lock resource to specific client"""
        cls.locked = True
        cls.acquirer = acquirer

    @classmethod
    def release_resource(cls, acquirer):
        """Release the resource"""
        if acquirer == cls.acquirer:
            cls.locked = False
            cls.acquirer = None
            return True
        return False

    @classmethod
    def get_acquirer(cls):
        """Get the client which holds the resource"""
        return cls.acquirer

    @classmethod
    def resource_locked(cls):
        """Check if resource is locked"""
        return cls.locked

    @classmethod
    def add_request(cls, caller_id):
        """Add request to queue"""
        cls.queue.appendleft(caller_id)

    @classmethod
    def remove_request(cls, caller_id):
        try:
            # Remove request if queue is not empty and the caller is next
            if cls.queue and caller_id == cls.queue[-1]:
                cls.queue.pop()
            else:
                # Remove caller's request if it was not next
                cls.queue.remove(caller_id)
        except IndexError:
            print('Queue is empty')

    @classmethod
    def next(cls):
        # Return next client to obtain the lock to the resource
        return cls.queue[-1]
