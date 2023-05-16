from abc import ABC, abstractmethod
import pytest

def test_ABC():

    class myABC(ABC):
        def __init__(self, dummy):
            print('myABC')
            ABC.__init__(self)



    class A(myABC):
        def __init__(self, test):
            print("A")
            self.A = True
            super().__init__(test)

        @abstractmethod
        def foo(self):
            pass


    class B(myABC):
        def __init__(self, test):
            print('B')
            self.B = True
            super().__init__(test)

        @abstractmethod
        def bar(self):
            pass


    class AB(A,B):
        def __init__(self, test):
            print('C')
            self.C = True
            super().__init__(test)

        def foo(self):
            print('foo')

        def bar(self):
            print('bar')


    ab = AB('test')
    assert ab.A and ab.B and ab.C


    class AA(A):
        def foo(self):
            print('foo')

    AA('test')

    class BB(B):
        def bar(self):
            print('bar')

    BB('test')


    class D(B):
        def __init__(self, test):
            print('D')
            self.D = True
            super().__init__(test)

    class AD(A,D):
        def __init__(self, test):
            print('E')
            self.E = True
            super().__init__(test)

        def foo(self):
            print('foo')

        def bar(self):
            print('bar')

    ad = AD('test')
    assert ad.A and ad.B and ad.D and ad.E

    with pytest.raises(TypeError):
        A('test') # abstract method exisists

    with pytest.raises(TypeError):
        B('test') # abstract method exisists

    with pytest.raises(TypeError):
        D('test') # abstract method exisists
