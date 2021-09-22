import requests
import traceback
import time

class SafeRequests:
    def __init__(self, proxy_dispatcher,logger,ATTEMPTS,ATTEMPT_DELAY):
        self.proxy_dispatcher=proxy_dispatcher
        self.logger=logger
        self.ATTEMPTS=ATTEMPTS
        self.ATTEMPT_DELAY=ATTEMPT_DELAY

    def syncProxyTryGetRequest(self,url):
        attempt = 0
        proxy=self.proxy_dispatcher.syncGetProxy()
        proxies = {'https': proxy}
        self.logger.info(f"\nSync request with proxy and attempts\nURL: {url}\tmax attempts: {self.ATTEMPTS}\tproxy{proxy}")

        while True:
            try:
                res = requests.get(url,proxies=proxies)
                return res
            except Exception as e:
                if not attempt < self.ATTEMPTS:
                    self.logger.error(e,traceback.format_exc())
                    raise e

                self.logger.warning(e,traceback.format_exc())
                attempt += 1
                time.sleep(self.ATTEMPT_DELAY)
