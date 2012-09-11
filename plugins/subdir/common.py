class MyNewAction(Opt):
    @classmethod
    def action(cls):
        print "Action from nested plugin"
    opt = '--subdir'
    action_type = 'store_true'

