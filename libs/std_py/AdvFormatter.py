# coding=utf8


from string import Formatter


class AdvFormatter(Formatter):
    def get_value(self, key, args, kwargs):
        try:
            if isinstance(key, basestring):
                return kwargs.get(key)
            elif isinstance(key, int):
                return args[key] or None
            else:
                return super(AdvFormatter, self).get_value(key, args, kwargs)
        except:
            return None

    def get_field(self, field_name, args, kwargs):
        first, rest = field_name._formatter_field_name_split()

        obj = self.get_value(first, args, kwargs)
        if not obj:
            return '{%s}' % field_name, first
        # loop through the rest of the field_name, doing
        #  getattr or getitem as needed
        for is_attr, i in rest:
            if isinstance(i, basestring):
                obj = obj.get(i)
            elif isinstance(i, int):
                obj = obj[i]
            else:
                obj = obj
        return obj, first


if __name__ == '__main__':
    string = "{number_of_sheep.a} sheep {has} run away"
    other_dict = {'number_of_sheep': {'a': 1}}
    fmt = AdvFormatter()
    print fmt.format(string, **other_dict)
