'''
Enum for python

Created on Dec 8, 2013

@author: Javier Gonzalez
'''
class Enum:
    ''' Class to create an enumerated type
        
    '''
    
    def __init__(self, enumVars=[]):
        self.incr(enumVars)

    def set(self, var, val):
        '''     
            Set 'var' to value 'val' in enum
        '''
        if var in vars(self).keys():
            raise AttributeError("duplicate var in enum")
        if val in vars(self).values():
            raise ValueError("duplicate value in enum")
        vars(self)[var] = val
        return self
    
    def strs(self, enumVars):
        '''
            Set each of the enumVars to itself (as a string) in the enum
        '''
        for var in self._parse(enumVars):
            self.set(var,var)
        return self
    
    def incr(self, enumVars):
        '''
            Set each of the enumVars to the next in the enum
        '''
        for var in self._parse(enumVars):
            self.set(var, self.next())
        return self
    
    def vals(self, **entries):
        '''
            Set each var=val pair in the enum
        '''    
        for (var,val) in entries.items():
            self.set(var,val)
        return self
    
    def next(self):
        '''
            Next int value to be assigned. Count starts in 0
        '''
        try: return max([x for x in vars(self).values() if type(x)==type(0)]) + 1
        except ValueError: return 0
        
    def _parse(self, enumVars):
        '''
            Convert string in list
        '''
        if type(enumVars) == type(""):
            return enumVars.split()
        else:
            return enumVars
        
