# 第1周学习总结 · Python核心

> 2026年4月 · Python后端实习冲刺第1周
> 目标：掌握Python核心知识，为FastAPI打下地基

---

## 📊 本周数据

- **学习天数：** 7天
- **每日时长：** 4-5小时
- **完成代码：** 5个文件
- **LeetCode：** 15+道
- **核心知识点：** 7大模块

---

## 🎯 本周目标 vs 实际产出

| 目标 | 完成情况 |
|------|---------|
| 掌握OOP核心 | ✅ 写了银行系统 + 2个子类 |
| 写出3个装饰器 | ✅ @timer, @retry, @cache |
| 理解生成器 | ✅ 斐波那契、ID生成器 |
| 掌握类型注解 | ✅ 代码全部加了类型注解 |
| 理解async异步 | ✅ 懂原理，能讲清楚场景 |
| Git + Linux基础 | ✅ 搭建GitHub仓库 |
| LeetCode 15道 | ✅ 完成 |

---

## 📚 核心知识点

### 1. OOP面向对象

**四大特性：**

- **封装**：把数据和方法打包在类里，通过访问控制隐藏内部
- **继承**：子类复用父类代码，用 `super()` 调用父类方法
- **多态**：同名方法在不同对象上有不同行为
- **抽象**：只暴露必要接口，隐藏实现细节

**三种方法：**

```python
class Example:
    def instance_method(self):    # 实例方法：访问self
        pass
    
    @classmethod
    def class_method(cls):         # 类方法：访问类，做工厂方法
        pass
    
    @staticmethod
    def static_method():           # 静态方法：工具函数
        pass
```

**访问控制：**

```python
self.name       # public - 公开
self._email     # protected - 约定不要外部修改
self.__password # private - 名称改写，外部访问不了
```

**关键代码：银行账户系统**

```python
class BankAccount:
    def __init__(self, owner: str, initial_balance: float = 0) -> None:
        self.owner: str = owner
        self._balance: float = initial_balance
        self.transactions: list[dict] = []

    def deposit(self, amount: float) -> None:
        if not isinstance(amount, (int, float)) or amount <= 0:
            raise ValueError(f"存款金额不合法: {amount}")
        self._balance += amount
        self.transactions.append({
            "type": "deposit",
            "amount": amount
        })


class SavingsAccount(BankAccount):
    def __init__(self, owner: str, initial_balance: float = 0, interest_rate: float = 0.03):
        super().__init__(owner, initial_balance)
        self.interest_rate: float = interest_rate

    def withdraw(self, amount: float) -> None:
        actual_amount = amount + 2  # 手续费
        super().withdraw(actual_amount)
```

---

### 2. 魔术方法

**让你的类像Python内置类型一样好用：**

```python
class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):         # print时
        return f"Vector({self.x}, {self.y})"

    def __add__(self, other):  # + 运算
        return Vector(self.x + other.x, self.y + other.y)

    def __eq__(self, other):   # == 比较
        return self.x == other.x and self.y == other.y

    def __len__(self):         # len()
        return 2

    def __getitem__(self, i):  # 下标访问
        if i == 0: return self.x
        if i == 1: return self.y


v1 = Vector(3, 4)
v2 = Vector(1, 2)
print(v1 + v2)       # Vector(4, 6)
print(v1 == v2)      # False
print(len(v1))       # 2
print(v1[0])         # 3
```

---

### 3. 装饰器

**本质：接收函数、返回新函数的高阶函数**

**万能模板：**

```python
from functools import wraps

def 装饰器名(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # 前置逻辑
        result = func(*args, **kwargs)
        # 后置逻辑
        return result
    return wrapper
```

**带参数装饰器（三层嵌套）：**

```python
def decorator_with_args(参数):     # 第1层：接收装饰器参数
    def decorator(func):            # 第2层：真正的装饰器
        @wraps(func)
        def wrapper(*args, **kwargs):  # 第3层：包装逻辑
            return func(*args, **kwargs)
        return wrapper
    return decorator
```

**关键点：**
- `*args, **kwargs` 接受任意参数
- `@wraps(func)` 保留原函数元信息
- `return result` 保留返回值

**实战：3个实用装饰器**

```python
# @timer 计时
def timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        print(f"{func.__name__} 耗时: {time.time() - start:.2f}秒")
        return result
    return wrapper

# @retry 重试
def retry(max_attempts=3):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts:
                        raise
        return wrapper
    return decorator

# @cache 缓存
def cache(func):
    cached = {}
    @wraps(func)
    def wrapper(*args, **kwargs):
        key = str(args) + str(kwargs)
        if key in cached:
            return cached[key]
        result = func(*args, **kwargs)
        cached[key] = result
        return result
    return wrapper
```

---

### 4. 生成器

**核心：`yield` 让函数变成生成器，用一个算一个，极省内存**

**特性：**
- 调用生成器函数不立即执行，返回生成器对象
- `next()` 触发执行，遇到 yield 暂停
- 再次 `next()` 从暂停处继续
- 只能顺序遍历一次

**实战：**

```python
# 斐波那契数列
def fibonacci(n):
    a, b = 0, 1
    for _ in range(n):
        yield a
        a, b = b, a + b

# 无限ID生成器
def id_generator(prefix):
    count = 1
    while True:
        yield f"{prefix}-{count:04d}"
        count += 1

# 大文件逐行读取
def read_large_file(filename):
    with open(filename) as f:
        for line in f:
            yield line.strip()
```

**生成器 vs 列表：**

| | 列表 | 生成器 |
|--|------|--------|
| 内存 | 一次性占用 | 用到才算 |
| 访问 | 随机访问 | 只能顺序 |
| 遍历 | 可反复 | 只一次 |

---

### 5. 类型注解

**Python运行时不检查类型，但FastAPI等框架会利用注解做验证。**

```python
from typing import List, Dict, Optional

# 基础
name: str = "张三"
age: int = 25

# 函数
def greet(name: str, age: int = 0) -> str:
    return f"Hello {name}"

def print_msg(msg: str) -> None:   # 无返回值用None
    print(msg)

# 复杂类型
def find_users(age: int) -> List[str]:
    pass

def find_user(id: int) -> Optional[str]:  # 可能为None
    pass
```

**类型注解作用：**
1. 提升代码可读性
2. IDE智能补全
3. 便于团队协作
4. FastAPI/Pydantic运行时数据验证

---

### 6. async异步

**核心：** async解决I/O密集型任务的并发问题，让等待时间重叠。

**基础语法：**

```python
import asyncio

async def fetch(name):         # 定义异步函数（协程）
    await asyncio.sleep(1)      # 等待异步操作
    return f"{name}的数据"

async def main():
    # 并发执行多个任务（关键）
    results = await asyncio.gather(
        fetch("A"),
        fetch("B"),
        fetch("C"),
    )

asyncio.run(main())            # 顶层启动
```

**关键理解：**

```
同步处理3个请求：每个等1秒 → 总计3秒
异步处理3个请求：一起等1秒 → 总计1秒（等待时间重叠）
```

**三种并发方案对比：**

| 方案 | 适合场景 |
|------|---------|
| **async** | I/O密集（API、DB、文件） |
| **多线程** | I/O密集 + 兼容同步代码 |
| **多进程** | CPU密集（计算、图像处理） |

---

### 7. Git工作流

**三个区域：**
```
工作区 → git add → 暂存区 → git commit → 本地仓库 → git push → 远程
```

**常用命令：**

```bash
git init                    # 初始化
git status                  # 查看状态
git add .                   # 添加改动
git commit -m "说明"         # 提交
git push                    # 推送

git branch                  # 查看分支
git checkout -b feature     # 创建并切换分支
git merge feature           # 合并分支
```

**Feature Branch工作流：**
1. 从main分出新分支
2. 开发新功能
3. 推送到远程
4. 发起Pull Request
5. Code Review
6. 合并到main
7. 删除feature分支

---

### 8. Linux核心

**权限模型：**
```
-rwxr-xr-x
数字：r=4, w=2, x=1
755 = rwxr-xr-x（脚本常用）
644 = rw-r--r--（文件常用）
```

**管道：**
```bash
ps aux | grep python | wc -l
# 统计python进程数量
```

**常用命令：**

```bash
ls -la                      # 列表+隐藏文件
cd /path                    # 切换目录
mkdir -p a/b/c              # 创建多级目录
rm -r folder                # 删除目录
cp source dest              # 复制
mv old new                  # 移动/重命名
cat/less/tail file          # 查看文件
grep "pattern" file         # 搜索
ps aux | grep name          # 找进程
kill -9 PID                 # 杀进程
lsof -i :8000               # 查端口
```

---

## 💻 LeetCode题目清单

| 编号 | 题目 | 难度 | 涉及知识 |
|------|------|------|---------|
| #1 | 两数之和 | 简单 | 哈希表 |
| #20 | 有效的括号 | 简单 | 栈 |
| #21 | 合并两个有序链表 | 简单 | 链表 + 双指针 |
| #49 | 字母异位词分组 | 中等 | 哈希表 + 字符串 |
| #53 | 最大子数组和 | 中等 | 动态规划 |
| #70 | 爬楼梯 | 简单 | 动态规划 |
| #121 | 买卖股票最佳时机 | 简单 | 一次遍历 |
| #141 | 环形链表 | 简单 | 快慢指针 |
| #155 | 最小栈 | 中等 | 辅助栈 |
| #206 | 反转链表 | 简单 | 链表 + 三指针 |
| #217 | 存在重复元素 | 简单 | 集合 |
| #242 | 有效的字母异位词 | 简单 | 排序/哈希 |

**核心思路总结：**
- **哈希表题**：查找O(1) → 两数之和、重复元素、字母异位词
- **双指针**：链表反转、合并链表、快慢指针判环
- **栈题**：括号匹配、最小栈
- **动态规划入门**：爬楼梯、最大子数组

---

## 🎓 学到的思考方式

### 1. 面向对象的思考方式

**从"一堆函数"到"一组类"：**

```
面向过程思维：
balance = 1000
deposit(balance, 100)     ← 数据到处传
withdraw(balance, 50)

面向对象思维：
acc = Account(1000)        ← 数据和操作绑在一起
acc.deposit(100)
acc.withdraw(50)
```

### 2. 装饰器的思考方式

**从"每个函数都加相同代码"到"抽成装饰器复用"：**

```
不用装饰器：
def f1(): start=...; result=do_f1(); print(time); return result
def f2(): start=...; result=do_f2(); print(time); return result
# 每个函数都重复写计时代码

用装饰器：
@timer
def f1(): do_f1()

@timer
def f2(): do_f2()
# 写一次@timer，到处用
```

### 3. 生成器的思考方式

**从"一次性装内存"到"流式处理"：**

```
传统思维：
data = load_all_data()     ← 10GB数据全进内存
for item in data:
    process(item)

生成器思维：
for item in stream_data(): ← 一次一条
    process(item)
```

### 4. 异步的思考方式

**从"一个一个等"到"一起等待"：**

```
同步思维：
打电话预约医生A（等回复）→ 挂断 → 打给医生B（等回复）→ ...

异步思维：
给医生A/B/C同时发短信 → 做别的事 → 谁回复就处理谁
```

---

## 🎯 能力自评

**这周我能做到的：**

- ✅ 独立设计一个含继承、多态的类系统
- ✅ 手撕基础装饰器（不看资料）
- ✅ 看懂并修改带参数的装饰器
- ✅ 写简单的生成器
- ✅ 给代码加完整类型注解
- ✅ 讲清楚async的使用场景和原理
- ✅ 用Git管理代码并推送GitHub
- ✅ 在命令行熟练使用Linux基础命令

**还需要加强的：**

- ⚠️ 复杂装饰器手撕（带状态的、三层嵌套的）
- ⚠️ async的实际代码写法（下周FastAPI会强化）
- ⚠️ LeetCode中等难度题
- ⚠️ 面试时的表达（回答要完整、结构化）

---

## 📌 下周规划

**第2周：数据库（MySQL + Redis）**

- Day8-9: MySQL基础 + SQL进阶（JOIN/GROUP BY）
- Day10: 索引优化 + Pydantic（FastAPI前置）
- Day11: Redis缓存
- Day12: Python连接数据库（SQLAlchemy）
- Day13-14: 学生管理系统项目（MySQL + Redis）

**第3周才开始学FastAPI（实际项目开发）**

---

## 💡 给未来自己的话

**1. 不要焦虑进度。** 第1周已经做了很多事，不用和别人比，只和昨天的自己比。

**2. 不要死记代码。** 编程是"用"出来的，不是"背"出来的。做项目多用几次自然就记住了。

**3. 关注GitHub积累。** 每周提交，一年后回头看会很有成就感。

**4. 基础大于框架。** Python基础扎实了，FastAPI只是一周就能上手的东西。

**5. AI是学习助手不是替代品。** 让AI帮你讲解、审查、出题，但代码还是自己写。

---

## 🔗 相关链接

- GitHub仓库：https://github.com/lapalce227-prog/python-backend-learning
- 学习计划：8周实习冲刺 v3（FastAPI + AI Agent版）

---

*Generated on 2026-04-20 · Week 1 Complete · Next: MySQL basics*
