from model import FileMeta

mng = FileMeta.init_mng('../book_repo/meta.json')
for book in mng.get_all():
     print unicode(book)
mng.save()
