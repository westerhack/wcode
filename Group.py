import re, copy
from Objects import nullobj, obj, arrayobj
from Objects import objregexes
class group(list):
    def __init__(self, data = None, pobj = None, control = None, args = [], parens = ('', '')):
        super().__init__(args)
        self.data = data
        self.control = control
        self.parens = parens
        self.baseobj = self.getobj() if pobj == None else pobj

    def __repr__(self):
        ret = 'group('
        if self.data != None:
            ret += 'data= {}, '.format(repr(self.data))
        if self.baseobj != nullobj:
            ret += 'pobj= {}, '.format(repr(self.baseobj))
        if len(self):
            ret += 'args= {}, '.format(super().__repr__())
        if self.parens != ('', ''):
            ret += 'parens= {}, '.format(repr(self.parens))
        return (ret != 'group(' and ret[:-2] or ret) + ')'

    def __str__(self):
        # if self.datastr in self.control.delims['arraysep']:
        #     if __debug__:
        #         assert len(self) == 0
        #     return ''.join((str(self.parens[0]), self.datastr, str(self.parens[1])))
        if not len(self):
            return ''.join((str(self.parens[0]), self.datastr, str(self.parens[1])))
        if self.datastr in self.control.opers['binary']:
            if __debug__:
                assert len(self.parens) == 2, repr(self)
            return self.parens[0] + (' ' + self.datastr +' ').join(str(e) for e in self) + str(self.parens[1])
        return ''.join((self.datastr, str(self.parens[0]), ', '.join(str(x) for x in self), str(self.parens[1])))

    def __bool__(self):
        """ False if this thing's baseobj is a nullobj. """
        return not isinstance(self.baseobj, nullobj)
    
    def __getitem__(self, item):
        if isinstance(item, slice):
            return group(data = self.data,
                         pobj = self.baseobj,
                         control = self.control,
                         args = super().__getitem__(item),
                         parens = self.parens,)
        return super().__getitem__(item)

    def linestr(self):
        class _int():
            def __init__(self):
                self.pos = 0
            def __iadd__(self, other):
                self.pos += other
            def __int__(self):
                return self.pos
        linep = _int()
        def _linestr(self, indent):
            if not self.data or not len(self):
                return str(self)
            isendl = self.datastr in self.control.delims['endline'][0]
            lines = []
            for l in self:
                if not l:
                    continue
                if isendl:
                    linep.__iadd__(1)
                ls = _linestr(l, indent + 1)
                if isendl:
                    lines.append('\n{:^3}|  {}{}'.format(int(linep), '\t' * (indent), ls))
                else:
                    lines.append(ls)
            ret = self.parens[0] + ('' if isendl else ' ' + self.datastr + ' ').join(lines)
            if isendl and self.parens[1]:
                linep.__iadd__(1)
                ret += '\n{:^3}|  {}'.format(len(linep), '\t' * (indent-2))
            ret += self.parens[1]
            return ret
        return _linestr(self, 0)

    def getobj(self):
        # print(list(self),list(self) == [])
        if self.data == None and self.parens != ('', ''):
            return arrayobj()
        if self.data == None:
            return nullobj()
        if __debug__:
            assert isinstance(self.data, str), "'%s' has to be of type str, not '%s'" %(self.data, type(self.data))
        for key in objregexes:
            if re.fullmatch(key.format(quote = self.control.allquotes,
                                       escape = self.control.escape), self.datastr):
                return objregexes[key]()
        if self.data in self.control.allkws:
            return self.control.allkws[self.data]
        return obj()

    def evalgrp(self, lcls):
        return self.baseobj.evalobj(self, lcls)

    def deepcopy(self):
        return copy.deepcopy(self)

    def __deepcopy__(self, memo):
        return group(data = copy.deepcopy(self.data, memo),
                     pobj = copy.deepcopy(self.baseobj, memo),
                     control = self.control,
                     args = copy.deepcopy(list(self), memo),
                     parens = copy.deepcopy(self.parens, memo))

    @property
    def datastr(self):
        return '' if self.data == None else str(self.data)

    def updatedata(self, datagroup, funcname):
        self.data = datagroup.data

    def scrubstr(self, control):
        ret = self.datastr
        if ret and ret[0] in self.control.allquotes:
            if __debug__:
                assert ret[-1] in self.control.allquotes #can't have unmatched quotes
            ret = ret[1:-1]
        for k, v in control.escapechars.items():
            ret = ret.replace(k, v)
        return ret