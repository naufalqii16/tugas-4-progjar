import os
import json
import base64
from glob import glob

class FileInterface:
    def __init__(self):
        os.chdir('files/')

    def list(self, params=[]):
        try:
            filelist = glob('*.*')
            return dict(status='OK', data=filelist)
        except Exception as e:
            return dict(status='ERROR', data=str(e))

    def get(self, params=[]):
        try:
            filename = params[0]
            if filename == '':
                return None
            with open(f"{filename}", 'rb') as fp:
                isifile = base64.b64encode(fp.read()).decode()
            return dict(status='OK', data_namafile=filename, data_file=isifile)
        except Exception as e:
            return dict(status='ERROR', data=str(e))

    def upload(self, params=None):
        if params is None:
            return dict(status='ERROR', data='Harap masukkan parameter yang sesuai')
        try:
            file_base64 = params[0]
            file_name = params[1]
            print(f"file base64: {file_base64}")
            decode_file = base64.b64decode(file_base64)
            if not file_base64 or not file_name:
                return dict(status='ERROR', data='Harap masukkan parameter yang sesuai')
            with open(file_name, 'wb') as dest_f:
                dest_f.write(decode_file)
            return dict(status='OK', message='File berhasil diunggah', data_namafile=file_name)
        except Exception as e:
            return dict(status='ERROR', data=str(e))

    def delete(self, params=None):
        if params is None:
            return dict(status='ERROR', data='Harap masukkan parameter yang sesuai')
        try:
            file_name = params[0]
            if not file_name:
                return dict(status='ERROR', data='Harap masukkan parameter yang sesuai')
            if not os.path.exists(file_name):
                return dict(status='ERROR', data='File tidak ditemukan')
            os.remove(file_name)
            return dict(status='OK', message='File berhasil dihapus', data_namafile=file_name)
        except Exception as e:
            return dict(status='ERROR', data=str(e))

if __name__ == '__main__':
    f = FileInterface()
