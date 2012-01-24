'''
Examples from the Python Cookbook Third edition
'''

class Descriptor:
    '''
    Uses a descriptor to set a value
    '''
    def __init__(self, name=None, **opts):
        self.name = name
        for key, value in opts:
            setattr(self, key, value)

    def __set__(self, instance, value):
        setattr(instance, self.name, value)


class Typed(Descriptor):
    '''
    Descriptor for enforcing types
    '''
    expected_type = type(None)

    def __set__(self, instance, value):
        if not isinstance(value, self.expected_type):
            raise TypeError('expected ' + str(self.expected_type))
        super().__set__(instance, value)


class Unsigned(Descriptor):
    '''
    Descriptor for enforcing values
    '''
    def __set__(self, instance, value):
        if value < 0:
            raise ValueError('Expected >= 0')
        super().__set__(instance, value)


class MaxSized(Descriptor):
    '''
    Descriptor for enforcing a max sequence size
    '''
    def __init__(self, name=None, **opts):
        if 'size' not in opts:
            raise TypeError('missing size option')
        self.size = opts['size']
        super().__init__(name, **opts)

    def __set__(self, instance, value):
        if len(value) >= self.size:
            raise ValueError('size must be < ' + str(self.size))
        super().__set__(instance, value)


def check_attributes(**kwargs):
    '''
    Class decorator to apply checks
    
    Example usage:
        @check_attributes(int_ = Typed(int),
                          uint_ = Unsigned())
        class Example:
            pass
    '''
    def decorate(cls):
        for key, value in kwargs.items():
            if isinstance(value, Descriptor):
                value.name = key
                setattr(cls, key, value)
            else:
                setattr(cls, key, value(key))
        return cls
    return decorate


class checkedmeta(type):
    '''
    Metaclass to apply checked attributes

    Example usage:
        class Foo(metaclass=checkedmeta):
            uint_ = Unsigned()
            list_ = MaxSized(size=8)
            def __init__(self, uint_, list_):
                self.uint_ = uint_
                self.list_ = list_
    '''
    def __new__(cls, clsname, bases, dct):
        # Attach attribute names to the descriptors
        for key, value in dct.items():
            if isinstance(value, Descriptor):
                value.name = key
        return type.__new__(cls, clsname, bases, dct)

