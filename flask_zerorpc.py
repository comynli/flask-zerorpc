# coding=utf-8

import zerorpc
import logging
import functools

__author__ = 'comyn'


class Wraps(object):
    def __init__(self, func, app):
        self._app = app
        self._func = func
        for attr in functools.WRAPPER_ASSIGNMENTS:
            setattr(self, attr, getattr(func, attr))
        for attr in functools.WRAPPER_UPDATES:
            getattr(self, attr).update(getattr(func, attr))

    def __call__(self, *args, **kwargs):
        with self._app.app_context():
            return self._func(*args, **kwargs)

    def __get__(self, instance, type_instance=None):
        if instance is None:
            return self
        return self.__class__(self._func.__get__(instance, type_instance))


class Handler(object):
    def __init__(self, app):
        self._app = app
        self._functions = dict()

    def _register(self, func):
        self._functions[func.__name__] = Wraps(func, self._app)
        self.__dict__[func.__name__] = Wraps(func, self._app)


class ZeroRPC(object):
    def __init__(self, app=None):
        if app:
            self.app = app
            self.init_app(app)
        self._client = None
        self.methods = []

    def init_app(self, app):
        self.app = app
        self.logger = logging.getLogger('zerorpc')
        self.logger.parent = self.app.logger
        self.server_endpoint = app.config.get('ZERORPC_SERVER_ENDPOINT')
        self.client_endpoint = app.config.get('ZERORPC_CLIENT_ENDPOINT')
        self._handler = Handler(app)
        app.extensions['zerorpc'] = self

    def start(self):
        if not self.server_endpoint:
            self.logger.error('ZERORPC_SERVER_ENDPOINT not defined')
            return
        server = zerorpc.Server(self._handler)
        server.bind(self.server_endpoint)
        server.run()

    @property
    def client(self):
        if not self.client_endpoint:
            self.logger.error('ZERORPC_CLIENT_ENDPOINT not defined')
            return
        if not self._client:
            self._client = zerorpc.Client()
            self._client.connect(self.client_endpoint)
        return self._client


    def register(self, func):
        self._handler._register(func)

