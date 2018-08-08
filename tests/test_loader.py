import os
import pytest

from httprunner import expections,loader

class TestFileLoader:
    def test_load_json_file_format_error(self):
        json_tmp_file_path='tests/data/tmp.json'

        #create empty file
        with open(json_tmp_file_path,'w') as f:
            f.write('')
        
        with pytest.raises(expections.FileFormatError):
            loader.load_json_file(json_tmp_file_path)
        
        os.remove(json_tmp_file_path)

        # create empty json file
        with open(json_tmp_file_path,'w') as f:
            f.write('{}')
        
        with pytest.raises(expections.FileFormatError):
            loader.load_json_file(json_tmp_file_path)
        
        os.remove(json_tmp_file_path)

        # create invaild format json file
        with open(json_tmp_file_path,'w') as f:
            f.write('abc')
        
        with pytest.raises(expections.FileFormatError):
            loader.load_json_file(json_tmp_file_path)
        
        os.remove(json_tmp_file_path)