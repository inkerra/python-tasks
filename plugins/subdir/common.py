from opt_plugin.plugin import MetaOpt, Opt

class MyNewActionSub(Opt):
    @classmethod
    def action(cls):
        print "Action from nested plugin"
    opt = '--subdir'
    action_type = 'store_true'

class D123(object):
    def __str__(self):
        return "D123 from subdir"
