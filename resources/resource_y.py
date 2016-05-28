from .resource_base import ResourceBase


class ResourceY(ResourceBase):
    def __new__(cls):
        """Singelton Implementation"""
        if not hasattr(cls, 'instance'):
            cls.instance = super(ResourceY, cls).__new__(cls)
        return cls.instance
