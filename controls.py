# -*- coding: utf-8-*-
import os
from model import FlatFile
from util.util import md5_for_file
from util.util import open_file
from util.wise_log import operate_log, debug_log
log = debug_log()
op_log = operate_log()

filelist = None

def build_repo(repo_path, idx_file='index.json'):
    global filelist
    try:
        filelist = FlatFile(repo_path, idx_file)
    except ValueError:
        raise ValueError('json loads %s error' % idx_file)

def get_filelist(matches='*.*'):
    return filelist.get_filelist()

def get_rawname(idx_file):
    return filelist.get_rawname(idx_file)

def open_file(filename):
    open_file(controls.get_filepath(filename))

def add(book_path, tar_ext='.pdf', del_orig=False, is_root=True):
    if is_root:
        # backup first
        op_log.info('add %s to BookList' % book_path)

    if os.path.isfile(book_path):
        orig_name, ext = os.path.splitext(os.path.basename(book_path))
        if ext.endswith(tar_ext):  # add file
            idx_name = '%s%s' % (md5_for_file(book_path), ext)
            if filelist.add_file(book_path, idx_name, del_orig):  # success. add file
                filelist.add_idx(idx_name, orig_name)
                op_log.info('success, add (%s, %s) to booklist' % (orig_name, idx_name))
            else:
                op_log.error('failed, add (%s, %s) to booklist' % (orig_name, idx_name))
        else:
            log.info('ignore %s for target extension is %s' % (book_path, tar_ext))
    elif os.path.isdir(book_path):
        for root, dirs, files in os.walk(book_path):
            for name in dirs:
                add(os.path.join(root, name), tar_ext, del_orig=del_orig, is_root=False)
                # delete empty dirs and log
            for name in files:
                add(os.path.join(root, name), tar_ext, del_orig=del_orig, is_root=False)
    else:
        log.error('%s should be a file or path' % book_path)

    if is_root:
        filelist.save()

build_repo('a')
add('/media/document/lean-read/media')
