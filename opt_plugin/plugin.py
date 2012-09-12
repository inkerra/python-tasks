class MetaOpt(type):
    all_data = []
    def __new__(cls, name, bases, dct):
        is_interface = False
        for i in dct.items():
            if i[0] == 'opt':
                opt = i[1]
        new_cls = super(MetaOpt, cls).__new__(cls, name, bases, dct)
        if not is_interface:
            MetaOpt.all_data.append((opt, new_cls))
        return new_cls

class Opt(object):
    """ interface for Action classes """
    __metaclass__ = MetaOpt

    @classmethod
    def action(cls, *vals):
        pass
    opt = '--act'

