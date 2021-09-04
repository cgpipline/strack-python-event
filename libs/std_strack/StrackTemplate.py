# coding=utf8
# Copyright (c) 2019 CineUse

import lucidity
from std_strack.build_full_template_path import build_full_template_path


class StrackTemplate(lucidity.Template):
    def __init__(self, code, pattern, rule="", anchor=lucidity.Template.ANCHOR_END,
                 default_placeholder_expression='[\w_\-]+|[.\-_]?',
                 duplicate_placeholder_mode=lucidity.Template.RELAXED,
                 template_resolver=None):
        super(StrackTemplate, self).__init__(code, pattern, anchor=anchor,
                                             default_placeholder_expression=default_placeholder_expression,
                                             duplicate_placeholder_mode=duplicate_placeholder_mode,
                                             template_resolver=template_resolver)

        self.__rule = rule

    def __repr__(self):
        return super(StrackTemplate, self).__repr__()

    @property
    def rule(self):
        return self.__rule

    @rule.setter
    def rule(self, value):
        if not isinstance(value, basestring):
            raise TypeError("expected string or buffer, but got a %s object." % type(value).__name__)
        self.__rule = value

    @property
    def pattern(self):
        return self._pattern

    @pattern.setter
    def pattern(self, value):
        if not isinstance(value, basestring):
            raise TypeError("expected string or buffer, but got a %s object." % type(value).__name__)
        self._pattern = value

    @classmethod
    def build_file_type_template(cls, template_code, project_info, file_type_info, extension_filter=None):
        full_pattern = build_full_template_path(project_info, template_code)
        if not full_pattern:
            return
        full_pattern = full_pattern.replace('\\', '/')
        template_code = '%s_%s_path' % (template_code, file_type_info.get('code'))
        obj = cls(template_code, full_pattern)
        obj.file_type = file_type_info
        return obj


if __name__ == '__main__':
    template = StrackTemplate('code', '{a.b}/{a.c}')
    print template.pattern
    print template.keys()
    from std_py.AdvFormatter import AdvFormatter
    fmt = AdvFormatter()
    print fmt.format(template.pattern, **{'a.c': 'adb'})
