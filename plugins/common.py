from opt_plugin.plugin import MetaOpt, Opt

class MyNewAction(Opt):
    @classmethod
    def action(cls):
        print "common plugin action"
    opt = '--act1'
