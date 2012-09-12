from opt_plugin.plugin import MetaOpt, Opt

class MyNewOption(Opt):
    @classmethod
    def action(cls, val):
        print "My new option is set to {}".format(val)
    opt = '--act2'
    value_type = int
    default_value = 0

class D123(object):
    def __str__(self):
        return "D123"
        
class D1234(object):
    def __str__(self):
        return "D1234"
