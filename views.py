# -*- coding: utf-8-*-
from model import BookFile
from util.wise_log import operate_log, debug_log
log = debug_log()
op_log = operate_log()

filelist = None

def build_repo(repo_path, filename='origname.json'):
    global filelist
    try:
        filelist = BookFile(repo_path, filename)
    except ValueError:
        raise ValueError('json loads %s error' % filename)

def add(book_path, tar_ext='', is_root=True):
    if is_root:
        # backup first
        op_log.log('add %s to BookList' % book_path)

    if os.path.isfile(book_path):
        orig_name, ext = os.path.splitext(os.path.basename(book_path))
        if ext.endswith(tar_ext):  # add file
            idx_name = '%s%s' % (md5_for_file(book_path), ext)
            if filelist.__add_file(book_path, idx_name):  # success. add file
                filelist.__add_idx(idx_name, orig_name)
                op_log.info('success, add (%s, %s) to booklist' % (orig_name, idx_name))
            else:
                op_log.error('failed, add (%s, %s) to booklist' % (orig_name, idx_name))
        else:
            log.info('ignore %s for target extension is %s' % (book_path, tar_ext))
    elif os.path.isdir(book_path):
        for root, dirs, files in os.walk(book_path):
            for name in dirs:
                filelist.add(os.path.join(root, name), tar_ext, is_root=False)
                # delete empty dirs and log
            for name in files:
                filelist.add(os.path.join(root, name), tar_ext, is_root=False)
    else:
        log.error('%s should be a file or path' % book_path)

    if is_root:
        pass
        # save
