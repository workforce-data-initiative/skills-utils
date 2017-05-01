from moto import mock_s3
import boto
import os
import tempfile
from skills_utils.s3 import download, upload, upload_dict


@mock_s3
def test_download():
    s3_conn = boto.connect_s3()
    bucket_name = 'test-bucket'
    bucket = s3_conn.create_bucket(bucket_name)
    key = boto.s3.key.Key(
        bucket=bucket,
        name='apath/akey'
    )
    key.set_contents_from_string('test')
    s3_path = 'test-bucket/apath/akey'

    with tempfile.NamedTemporaryFile(mode='w+') as f:
        download(s3_conn, f.name, s3_path)
        f.seek(0)
        assert f.read() == 'test'


@mock_s3
def test_upload():
    s3_conn = boto.connect_s3()
    bucket_name = 'test-bucket'
    bucket = s3_conn.create_bucket(bucket_name)

    with tempfile.NamedTemporaryFile(mode='w+') as f:
        f.write('test')
        f.seek(0)
        s3_path = 'test-bucket/apath/akey'
        upload(s3_conn, f.name, s3_path)
        key = boto.s3.key.Key(
            bucket=bucket,
            name='apath/akey/{}'.format(os.path.basename(f.name))
        )
        s = key.get_contents_as_string()
        assert s.decode('utf-8') == 'test'


@mock_s3
def test_upload_dict():
    s3_conn = boto.connect_s3()
    bucket_name = 'test-bucket'
    bucket = s3_conn.create_bucket(bucket_name)
    path = 'apath/'
    key = boto.s3.key.Key(
        bucket=bucket,
        name='{}/keyone.json'.format(path)
    )
    key.set_contents_from_string('old contents')

    data_to_sync = {
        'keyone': {'stuff': 'new contents'},
        'keytwo': {'stuff2': 'new contents2'},
    }

    upload_dict(s3_conn, 'test-bucket/apath', data_to_sync)

    assert key.get_contents_as_string().decode('utf-8')\
        == '{"stuff": "new contents"}'
