from Objects import obj
class mthdobj(obj):
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return super().__repr__().replace(')', '%r)' % self.name)

    def evalobj(self, args, lcls):
        if super().evalobj(args, lcls) == None:
            return
        if args.data == self.name:
            lcls.iv.last = args
            return
        return 0.5 #is it 0 or 1?

















