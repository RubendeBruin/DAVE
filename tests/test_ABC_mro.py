from abc import ABC, abstractmethod
import pytest


class super_black_hole():
    def __init__(self, *args, **kwargs):
        pass

if __name__ == '__main__':


    class A(super_black_hole, ABC):
        def __init__(self, test):
            print("A")
            self.A = True
            super().__init__(test)

        @abstractmethod
        def foo(self):
            pass

    class B(super_black_hole):
        def __init__(self, test):
            print('B')
            self.B = True
            super().__init__(test)

    class C(super_black_hole):
        def __init__(self, test):
            print('C')
            self.C = True
            super().__init__(test)

    class AandBandC_noAbstract(A,B,C):
        def __init__(self, test):
            super().__init__(test)

    class AandBandC(A,B,C):
        def __init__(self, test):
            super().__init__(test)

        def foo(self):
            pass


    abc = AandBandC('test') #  <--- fails as it should
    assert abc.A and abc.B and abc.C


def test_ABC():


    class A(super_black_hole, ABC):
        def __init__(self, test):
            print("A")
            self.A = True
            super().__init__(test)

        @abstractmethod
        def foo(self):
            pass


    class B(super_black_hole, ABC):
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

    class F(super_black_hole):
        def __init__(self, test):
            print('F')
            self.F = True
            super().__init__(test)

    ad = AD('test')
    assert ad.A and ad.B and ad.D and ad.E

    with pytest.raises(TypeError):
        A('test') # abstract method exisists

    with pytest.raises(TypeError):
        B('test') # abstract method exisists

    with pytest.raises(TypeError):
        D('test') # abstract method exisists

    class ADF(AD,F):
        def __init__(self, test):
            super().__init__(test)

    print(ADF.__mro__)

    adf = ADF('test')
    assert adf.A and adf.B and adf.D and adf.F

def test_getters_and_setters():
    """Asserts that the property of the mixin class is called"""

    class Base(super_black_hole):
        def __init__(self, test):
            super().__init__(test)
            self._value = ""

        def m(self):
            self._value += "0"

    class A(Base):
        def __init__(self, test):
            super().__init__(test)

        def m(self):
            self._value += "A"
            super().m()

    class B(Base):
        def __init__(self, test):
            super().__init__(test)

        def m(self):
            self._value += "B"
            super().m()

    class C(A,B):
        def __init__(self, test):
            super().__init__(test)

        def m(self):
            self._value += "C"
            super().m()


    c = C('test')
    c.m()
    assert 'A' in c._value
    assert 'B' in c._value
    assert 'C' in c._value
    assert '0' in c._value
