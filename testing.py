# coding: utf-8


class Foo(object):
    def __init__(self, name):

        print('name from Foo.__int__', name)
        self.name = name

    def __new__(cls, *args, **kwargs):
        # 根据类创建对象，并返回
        # 接着执行对应cls的__init__方法，想想 many=True 的流程

        return super().__new__(cls)


print(Foo('foo'))




