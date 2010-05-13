# encoding: utf-8

"""A dictionary with case-insensitive access."""


from .object import NoDefault


__all__ = ['CaseInsensitiveDict']


class CaseInsensitiveDict(dict):
    def __init__(self, default=None, *args, **kw):
        self._o = {}
        
        if default is None:
            default = dict()
            default.update(kw)
        
        for i, j in default.iteritems():
            self[i] = j
        
        super(CaseInsensitiveDict, self).__init__()
    
    def items(self):
        return [(self._o[k], v) for k, v in self.iteritems()]
    
    def __setitem__(self, k, v):
        nk = k.lower() if isinstance(k, basestring) else k
        self._o[nk] = k
        super(CaseInsensitiveDict, self).__setitem__(nk, v)
    
    def __getitem__(self, k):
        nk = k.lower() if isinstance(k, basestring) else k
        return super(CaseInsensitiveDict, self).__getitem__(nk)