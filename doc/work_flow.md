Work Flow
=========

Add File
========

copy file and add Meta info.

Steps
-----

1. check file existance
2. build meta info
3. cp src_file dst_file
4. add meta info to repo

Add Path
========

Ignore Rule
-----------

#### Identifier

1. filename

    file size makes it more precise
2. file extension
3. md5 code

#### validator

1. user config, just like `.gitginore`

    file/path name
    file extension
2. sensitive information

    both name and md5 check
3. ignore deleted file by default
    md5 only

#### Steps

1. check path existance

    1. redirect to add file if it is a file
    2. return if not exists
2. get file/sub-path list
3. validate each file/sub-path.

    1. ignore list check by filename
    2. sensitive information check by filename
    3. generate md5 for file
    4. sensitive information check by md5
    5. deleted list check by md5
4. add files and path

    1. if path, recursive call and count all added files,
    2. if file, call add file function. pass md5 to add file funcion to avoid regeneration.
5. count added files
