from logging import getLogger

from fdfs_client.client import Fdfs_client

from mallServe.settings import FASTDFS

logger = getLogger(__file__)


class FastDFSManager:
    def __init__(self, conf=None):
        if conf is None:
            conf = FASTDFS
        self.client = Fdfs_client(conf)

    def upload(self, file: str):
        result = self.client.upload_by_filename(file)
        logger.info(f"{result}")
        return result["Remote file_id"]

    def download(self, url: str):
        self.client.download_to_file(url, b'%s' % url)

    def remove(self, url: str):
        result = self.client.delete_file(b'%s' % url)
        logger.info(f"{result}")
        return result[0]


f = FastDFSManager()
print(f.upload('./token.py'))
