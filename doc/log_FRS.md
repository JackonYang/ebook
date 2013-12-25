Log
===

operate info log
----------------

record user's writing operation

1. add: raw filename, md5 code, timestamp.

    ignore orig path, for multi file path maybe exists and it costs too much to record it. What's more, it has little value. only to revert or analysis local file distribution.

2. del file from repo: md5 code, timestamp.

    ignore filename, for it has been recored while adding.

3. rename: log nothing, for we do not care about it.

4. copy file to repo: ignore, for necessary info is logged in add raw filename.

5. del file from local disk: ignore, for necessary info is logged in del file from repo.
