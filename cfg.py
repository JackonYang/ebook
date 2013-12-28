import codecs


_cfg_file = 'cfg_path.ini'
def get_cfg():
    cfg = {}
    cfg_name = ''
    cfg_value = set()
    try:
        with codecs.open(_cfg_file, 'r', encoding='utf8') as f:
            for line in f.readlines():
                item = clean(line)
                if not item:
                    pass
                elif item.startswith('[') and item.endswith(']'):
                    if cfg_name:
                        cfg[cfg_name] = cfg_value
                    cfg_name = item[1:-1]
                    cfg_value = set()
                else:
                    cfg_value.add(item)
            else:
                cfg[cfg_name] = cfg_value
    except IOError:
        pass
    return cfg


def clean(line):
    line = line.strip()
    if line.startswith('#'):
        return ""
    return line
