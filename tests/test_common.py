from skills_utils.common import safe_get

def test_nested_dict():
	test_dict = {'layer1':{'layer2':{'layer3':{'layer4': 'this is layer 4'}}}}
	assert safe_get(test_dict, 'layer1', 'layer2', 'layer3', 'layer4') ==  'this is layer 4'
