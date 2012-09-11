class MyNewOption(Opt):
    @classmethod
    def action(cls, val):
        print "My new option is set to {}".format(val)
    opt = '--act2'
    value_type = int
    default_value = 0

