import oss2
from itertools import islice


class ConnectOss(object):
    def __init__(self, access_id, access_key, bucket_name):
        """验证权限"""
        self.auth = oss2.Auth(access_id, access_key)
        self.endpoint = 'http://oss-cn-hangzhou.aliyuncs.com'
        self.bucket = oss2.Bucket(self.auth, self.endpoint, bucket_name=bucket_name)

    def get_bucket_list(self):
        """列举当前endpoint下所有的bucket_name"""
        service = oss2.Service(self.auth, self.endpoint)
        bucket_list = [b.name for b in oss2.BucketIterator(service)]
        return bucket_list

    def get_all_file(self, prefix):
        """获取指定前缀下所有文件"""
        for b in islice(oss2.ObjectIterator(self.bucket, prefix=prefix), 10):
            yield b.key


def read_file(self, path):
    try:
        file_info = self.bucket.get_object(path).read()
        return file_info
    except Exception as e:
        print(e, '文件不存在')


def download_file(self, path, save_path):
    result = self.bucket.get_object_to_file(path, save_path)
    if result.status == 200:
        print('下载完成')


def upload_file(self, path, local_path):
    result = self.bucket.put_object_from_file(path, local_path)
    if result.status == 200:
        print('上传完成')


if __name__ == '__main__':
    access_id = ''
    access_key = ''
    bucket_name = ''
    co = ConnectOss(access_id, access_key, bucket_name)
    print(co.get_all_file(prefix=""))
    for i in co.get_all_file(prefix=""):
        print(i)
