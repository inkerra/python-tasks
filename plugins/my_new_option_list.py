class MyNewOptionList(Opt):
    @classmethod
    def action(cls, val):
        print "My new option is set to {}".format(val)
    opt = '--actlist'
    value_type = int
    default_value = []
    action_type = 'append'

