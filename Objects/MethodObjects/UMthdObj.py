from Objects import mthdobj, arrayobj
class umthdobj(mthdobj):
    def __init__(self, name):
        super().__init__(name)

    def _evalargs(self, args, lcls):
        ret = super()._evalargs(args, lcls)
        if ret != NotImplemented:
            return ret
        # if not isinstance(args, lcls)
        lcls2pass = lcls.onlyfuncs()
        name, params, body = list(lcls.iv.last.deepcopy())
        print(name, params, body, sep = '\t|\t')
        if __debug__:
            assert isinstance(lcls.iv.last.baseobj, umthdobj),\
                "evalobj of a umthdobj uses the last value as the function to execute!"
            assert args, "cannot evaluate a function with a base type of '{}'!".format(type(args))
            assert len(args) == 1, "Args needs to be an array!".format(args)
            args = args[0]
            assert not (len(args) or len(params)) or len(args) == len(params), "Expected '{}' ({}), got '{}' ({})"\
                .format(params, len(params), args, len(args))

        for argp in range(len(params)): #setting the args
            args[argp].evalgrp(lcls)
            lcls2pass[str(params[argp])] = lcls.iv.last

        body.deepcopy().evalgrp(lcls2pass)
        del lcls.iv.last
        if lcls2pass.iv.ret:
            lcls.iv.last = lcls2pass.iv.ret
