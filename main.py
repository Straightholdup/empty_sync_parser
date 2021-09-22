# CONFIG FILE SHOULD LOOK LIKE
# {
#   "tender_conn": "dbname='?' user='?' host='?.?.?.?' password='?' port=? options = '-c search_path=?'",
#   "monitoring_conn": "dbname='?' user='?' host='?.?.?.?' password='?' port=? options = '-c search_path=?'",
#   "channel": "?.?.?.?:?",
#   "source": "'?'"
# }

# CONFIG FILE default for tenders
# {
#   "tender_conn": "dbname='parsing' user='data_migrator' host='192.168.1.25' password='Z4P6PjEHnJ5nPT' port=5432 options = '-c search_path=tender'",
#   "monitoring_conn": "dbname='parsing' user='data_migrator' host='192.168.1.25' password='Z4P6PjEHnJ5nPT' port=5432 options = '-c search_path=monitoring'",
#   "channel": "192.168.1.169:24000",
#   "source": "'?'"
# }

from service import sync_parser_app
import os

dirname = os.path.dirname(__file__)
sync_service = sync_parser_app.SyncParserApp(config_dir=os.path.join(dirname, 'config.json'))

def main():
    pass

if __name__ == "__main__":
    sync_service.run(main)

