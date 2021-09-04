# coding: utf-8

from std_py.AdvFormatter import AdvFormatter


def build_strack_path(template_path, **kwargs):
    fmt = AdvFormatter()
    item_path = fmt.format(template_path, **kwargs)
    item_path = item_path.replace('\\', '/')
    return item_path
