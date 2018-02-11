from moto import mock_s3_deprecated, mock_s3
import boto
import json
import os
import tempfile
from skills_utils.s3 import download, upload, upload_dict, list_files, S3BackedJsonDict


@mock_s3_deprecated
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


@mock_s3_deprecated
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


@mock_s3_deprecated
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


@mock_s3_deprecated
def test_list_files():
    s3_conn = boto.connect_s3()
    bucket_name = 'test-bucket'
    bucket = s3_conn.create_bucket(bucket_name)
    key = boto.s3.key.Key(
        bucket=bucket,
        name='apath/test.json'
    )
    key.set_contents_from_string('some contents')
    s3_path ='test-bucket/apath/'
    files = list_files(s3_conn, s3_path)
    assert files == ['test.json']


@mock_s3_deprecated
@mock_s3
def test_S3BackedJSONDict_basic():
    s3_conn = boto.connect_s3()
    bucket_name = 'test-bucket'
    bucket = s3_conn.create_bucket(bucket_name)

    # 1. Ensure that a new file is correctly created and saved to
    storage_one = S3BackedJsonDict(path='test-bucket/apath') 
    storage_one['key1'] = 'value1'
    storage_one['key2'] = {'nestedkey2': 'value2'}
    storage_one.save()
    key = boto.s3.key.Key(
        bucket=bucket,
        name='apath.json'
    )
    assert json.loads(key.get_contents_as_string().decode('utf-8'))\
        == {'key1': 'value1', 'key2': {'nestedkey2': 'value2'}}

    # 2. Ensure that an existing file is correctly read, updated, and saved to
    storage_two = S3BackedJsonDict(path='test-bucket/apath') 
    assert 'key1' in storage_two
    assert storage_two['key1'] == 'value1'
    storage_two['key3'] = 'value3'
    storage_two.save()
    assert json.loads(key.get_contents_as_string().decode('utf-8'))\
        == {'key1': 'value1', 'key2': {'nestedkey2': 'value2'}, 'key3': 'value3'}

    # 3. Ensure that, in the same thread, updating and saving an old one gets new changes too
    storage_one['key4'] = 'value4'
    storage_one.save()
    assert json.loads(key.get_contents_as_string().decode('utf-8'))\
        == {'key1': 'value1', 'key2': {'nestedkey2': 'value2'}, 'key3': 'value3', 'key4': 'value4'}

    # 4. test autosave - this will be the fourth update of this object
    storage_one.SAVE_EVERY_N_UPDATES = 4
    storage_one['key5'] = 'value5'
    assert json.loads(key.get_contents_as_string().decode('utf-8'))\
        == {'key1': 'value1', 'key2': {'nestedkey2': 'value2'}, 'key3': 'value3', 'key4': 'value4', 'key5': 'value5'}

    # 5. test length checking
    assert len(storage_one) == 5

    # 6. test iteration
    assert sorted(
        [(key, value) for key, value in storage_one.items()],
        key=lambda x: x[0]
    ) == [
        ('key1', 'value1'),
        ('key2', {'nestedkey2': 'value2'}),
        ('key3', 'value3'),
        ('key4', 'value4'),
        ('key5', 'value5')
    ]
