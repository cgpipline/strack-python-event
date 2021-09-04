# coding=utf8

import importlib
import os


# 返回指定文件中的action函数
def mod_load(script_name):
    name = os.path.splitext(script_name)[0]
    module_name = importlib.import_module(name)
    # 动态导入相应模块
    func = module_name.action
    return module_name, func


