from opt_plugin.plugin import MetaOpt, Opt

class MyNewOptionList(Opt):
    @classmethod
    def action(cls, val):
        print "My new option list is set to {}".format(val)
    opt = '--actlist'
    value_type = int
    default_value = []
    action_type = 'append'

class D321(object):
    def __str__(self):
        return "D321"
