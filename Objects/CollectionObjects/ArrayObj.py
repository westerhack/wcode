from Objects import collectionobj
class arrayobj(collectionobj):
    _pyobj = list
    def evalobj(self, args, lcls):
        # ret = super().evalobj(args, lcls)
        # if ret != NotImplemented:
            # return ret
        for arg in args:
            arg.evalgrp(lcls)