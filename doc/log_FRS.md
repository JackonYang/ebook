Log
===

operation log
-------------

record user's writing operation

#### LEVEL-INFO

1. add: raw filename, md5 code, timestamp.

    ignore origin path, reason: there can be multi path of a file and it is a little tricky to record and retrieve it.
    the only 2 usage that I can imagine is to revert adding or analysis local file distribution.

2. del file from repo: md5 code, timestamp.

    ignore filename, reason: it has been recored while adding.

3. rename: log nothing, reason: we do not care about its history.

4. copy file to repo: ignore, reason: necessary info is logged while adding raw filename.

5. del file from local disk: ignore, reason: if VIP deleted, we can retrieve it from repo by rawname.
