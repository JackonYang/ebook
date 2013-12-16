import os
import controls
import desktop_ui

repo_path = 'demo_repo'
cache_path = os.path.join(os.path.expanduser('~'), 'download')

controls.build_repo(repo_path)
print 'repo built: %s' % repo_path
controls.add(cache_path, 'pdf', depth=1)
print 'pdf files under %s added' % cache_path
desktop_ui.main(repo_path)
