from abc import ABCMeta
from collections import deque
from datetime import timedelta


class ResourceBase(metaclass=ABCMeta):
    """Base class to add and keep state of resource availability"""
    def __init__(self, timeout_in_seconds=1.0):
        self.available = True
        self.locker = ''
        self.queue = deque()
        self.timeout_in_seconds = timedelta(seconds=timeout_in_seconds)

        def lock_reource(self):
            self.available = False

        def resource_locked(self):
            return not self.available

        def add_locker(locker):
            self.locker = locker

        def add_request(self, request):
            """
            Add request to queue
            @params: request is dict that has caller_id, created_at
            """
            try:
                request['created_at'] += self.timeout_in_seconds
                self.queue.appendleft(request)
            except KeyError:
                print('request param has no created_at field')
            except TypeError:
                print('created_at field must be of datetime type')

        def remove_request(self, request):
            try:
                self.queue.pop()
            except IndexError:
                print('Queue is empty')

        def request_queue_empty(self):
            return bool(self.queue)

        def last_request_time(self):
            return self.queue[-1] if self.queue else None
