from .resource_base import ResourceBase


class ResourceX(ResourceBase):
    def __new__(cls):
        """Singelton Implementation"""
        if not hasattr(cls, 'instance'):
            cls.instance = super(ResourceX, cls).__new__(cls)
        return cls.instance
