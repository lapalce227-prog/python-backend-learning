# # 定义一个类（图纸）
# class Dog:
#     # 类属性：所有实例共享
#     species = "犬科"
#ls week1/
#     # __init__ 是构造方法，创建对象时自动调用
#     # self 代表当前对象本身，必须是第一个参数
#     def __init__(self, name, age):
#         # 实例属性：每个对象独有
#         self.name = name
#         self.age = age
#
#     # 实例方法：通过对象调用
#     def bark(self):
#         return f"{self.name}：汪汪汪！"
#
#     def info(self):
#         return f"{self.name}, {self.age}岁, {self.species}"
#
#
# # 创建对象（按图纸造产品）
# dog1 = Dog("旺财", 3)
# dog2 = Dog("小白", 1)
#
# print(dog1.bark())     # 旺财：汪汪汪！
# print(dog2.info())     # 小白, 1岁, 犬科
# print(dog1.species)    # 犬科（类属性通过实例访问）
# print(Dog.species)     # 犬科（类属性通过类访问）

class Calculator:
    # 类属性
    history = []

    def __init__(self, brand):
        self.brand = brand  # 实例属性

    # 实例方法：第一个参数是 self（当前对象）
    # 能访问实例属性和类属性
    def add(self, a, b):
        result = a + b
        Calculator.history.append(f"{self.brand}: {a}+{b}={result}")
        return result

    # 类方法：第一个参数是 cls（当前类）
    # 只能访问类属性，不能访问实例属性
    # 常用于"替代构造方法"
    @classmethod
    def show_history(cls):
        return cls.history

    @classmethod
    def from_string(cls, info):
        """替代构造方法：从字符串创建对象"""
        brand = info.split("-")[0]
        return cls(brand)  # 等价于 Calculator(brand)

    # 静态方法：没有 self 也没有 cls
    # 不能访问类属性和实例属性
    # 只是逻辑上属于这个类的普通函数
    @staticmethod
    def is_valid_number(value):
        return isinstance(value, (int, float))


# 使用
calc = Calculator("卡西欧")
calc.add(1, 2)

# 类方法可以通过类或实例调用
print(Calculator.show_history())  # ['卡西欧: 1+2=3']

# 替代构造方法
calc2 = Calculator.from_string("德州仪器-TI84")
print(calc2.brand)  # 德州仪器

# 静态方法
print(Calculator.is_valid_number(3.14))  # True
print(Calculator.is_valid_number("abc"))  # False