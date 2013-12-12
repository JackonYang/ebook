# -*- coding: utf-8-*-

import hashlib

def md5_for_file(filename, block_size=256*128, hr=True):
    '''
    Block size directly depends on the block size of your filesystem
    to avoid performances issues
    Here I have blocks of 4096 octets (Default NTFS)
    '''
    md5 = hashlib.md5()
    with open(filename,'rb') as f: 
        for chunk in iter(lambda: f.read(block_size), b''): 
            md5.update(chunk)
    if hr:
        return md5.hexdigest()
    return md5.digest()

if __name__ == '__main__':
    print md5_for_file(u'/media/document/lean-read/media/books/迷人的科学风采费曼传.pdf')
    print md5_for_file('/media/document/lean-read/media/books/迷人的科学风采费曼传.pdf')
