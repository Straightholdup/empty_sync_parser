import json
from . import logger_pack
from .proxy import proxy_pack
from . import db_pack
from . import safe_request_pack
import traceback

class SyncService:
    def __init__(self, config_dir):
        self.config = self.get_config_from_json(config_dir)
        self.check_config_keys()

        self.logger = logger_pack.get_logger(self.config['source'])
        self.proxy_dispatcher = proxy_pack.ProxyDispatcher(self.config["channel"], self.config["source"])
        self.db = db_pack.Database(tender_conn_config=self.config["tender_conn"],
                              monitoring_conn_config=self.config["monitoring_conn"],
                              monitoring_source_name=self.config["source"],
                              logger=self.logger)
        self.safe_requests = safe_request_pack.SafeRequests(proxy_dispatcher=self.proxy_dispatcher, logger=self.logger, ATTEMPTS=5,
                                                  ATTEMPT_DELAY=3)

    def get_config_from_json(self,config_dir):
        with open(config_dir, 'r') as f:
            config = json.loads(f.read())
        return config

    def check_config_keys(self):
        required_keys=[
            "tender_conn",
            "monitoring_conn",
            "channel",
            "source",
        ]
        for key in self.config:
            required_keys.remove(key)
        if required_keys:
            raise Exception("Add following keys to config file: "+", ".join(required_keys))

    def log_config(self):
        config_log_text="CONFIG:\n"+"\n".join([f"{key}: {self.config[key]}" for key in self.config])
        self.logger.info(config_log_text)

    def run(self,main):
        try:
            self.log_config()
            monitoring_status = self.db.getParserStatus()[0]
            if monitoring_status is None:
                self.logger.info('Parser already in progress')

            elif not monitoring_status:
                self.logger.info('Parser started')
                self.db.updateParserStatus(None)

                main()

                self.db.updateParserStatus(True)
                self.logger.info('Parser finished')
            else:
                self.logger.info('Information parsed before')
        except Exception as e:
            self.logger.error(e, traceback.format_exc())
            self.db.updateParserStatus(False)
