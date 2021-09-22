import asyncio
from . import proxy_pb2
from . import proxy_pb2_grpc
import grpc


class ProxyDispatcher:
    def __init__(self, channel_url, source):
        self.channel_url = channel_url
        self.source = source
        self._initProxies()
        self._current_proxy_index = 0
        self._lock = asyncio.Lock()

    def _initProxies(self):
        channel = grpc.insecure_channel(self.channel_url)
        stub = proxy_pb2_grpc.ProxyApiStub(channel)
        self.proxies = stub.GetProxies(proxy_pb2.ProxyRequest(count=30, source=self.source)).Proxies

    def syncGetProxy(self):
        if self._current_proxy_index >= len(self.proxies):
            self._current_proxy_index = 0

        current_proxy = self.proxies[self._current_proxy_index]
        proxy_str = 'http://' + str(current_proxy.username) + ':' + str(
            current_proxy.password) + '@' + str(
            current_proxy.address) + ':' + str(current_proxy.port)
        self._current_proxy_index += 1

        return proxy_str