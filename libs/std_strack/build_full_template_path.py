# coding=utf8


import os

from std_strack.get_platform_disk import get_platform_disk


def build_full_template_path(tos, project_info, template_code, platform=None):
    """
        Get specified item's full path.
        If local is True, use user disk instead of project disk.
    Args:
        project_info:
        template_code:
        platform:
    Returns:

    """
    template_filter = [['project_id', '=', project_info.get('id')]]
    dir_template_list = tos.select('dir_template', template_filter).get('rows')
    dir_template_dict = {dir_template.get('id'): dir_template for dir_template in dir_template_list}
    if not dir_template_dict:
        return

    template_path = ''
    current_disk_id = 0
    current_parent_id = 0
    for dir_template in dir_template_list:
        code = dir_template.get('code')
        if code == template_code:
            current_parent_id = dir_template.get('parent_id')
            current_disk_id = dir_template.get('disk_id') or 0
            template_path = dir_template.get('pattern')
            break

    parent_id_list = []
    while True:
        current_dir_template = dir_template_dict.get(current_parent_id)
        parent_id = current_dir_template.get('parent_id')
        pattern = current_dir_template.get('pattern')
        template_path = '%s/%s' % (pattern, template_path)
        if parent_id in parent_id_list:
            raise ValueError('Bad Dir Template.')
        current_parent_id = parent_id
        parent_id_list.append(parent_id)
        if not current_parent_id:
            break

    disk_dir = get_platform_disk(tos, current_disk_id, platform)

    # get real template path from server
    full_path = os.path.join(disk_dir, template_path).replace("\\", "/")
    return full_path
