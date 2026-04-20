"""
银行账户系统 - 第1周周一实践作业
学习目标：类与对象、实例方法、类方法、静态方法、property、错误处理
"""

import uuid
from datetime import datetime


class BankAccount:
    """银行账户类"""

    # =============================================
    # 初始化方法
    # =============================================
    def __init__(self, owner, initial_balance=0):
        """
        创建银行账户

        参数:
            owner: 账户持有人姓名
            initial_balance: 初始余额，默认为0
        """
        # 先验证初始余额是否合法
        if not self.is_valid_amount(initial_balance) and initial_balance != 0:
            raise ValueError(f"初始余额不合法: {initial_balance}")
        if initial_balance < 0:
            raise ValueError("初始余额不能为负数")

        self.owner = owner                          # 公开属性：持有人姓名
        self._balance = initial_balance              # 保护属性：余额（不让外部直接改）
        self.__account_id = str(uuid.uuid4())[:8]    # 私有属性：账户ID（外部无法直接访问）
        self.transactions = []                       # 交易记录列表

    # =============================================
    # 实例方法
    # =============================================
    def deposit(self, amount):
        """
        存款

        参数:
            amount: 存款金额，必须为正数
        """
        # 验证金额
        if not self.is_valid_amount(amount):
            raise ValueError(f"存款金额不合法: {amount}")

        # 执行存款
        self._balance += amount

        # 记录交易
        self.transactions.append({
            "type": "deposit",
            "amount": amount,
            "balance_after": self._balance,
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

        print(f"✅ 存款成功: +{amount}元, 当前余额: {self._balance}元")

    def withdraw(self, amount):
        """
        取款

        参数:
            amount: 取款金额，必须为正数且不能超过余额
        """
        # 验证金额
        if not self.is_valid_amount(amount):
            raise ValueError(f"取款金额不合法: {amount}")

        # 检查余额是否充足
        if amount > self._balance:
            raise ValueError(
                f"余额不足! 当前余额: {self._balance}元, 尝试取款: {amount}元"
            )

        # 执行取款
        self._balance -= amount

        # 记录交易
        self.transactions.append({
            "type": "withdraw",
            "amount": amount,
            "balance_after": self._balance,
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

        print(f"✅ 取款成功: -{amount}元, 当前余额: {self._balance}元")

    def transfer(self, other_account, amount):
        """
        转账到另一个账户

        参数:
            other_account: 目标账户（另一个BankAccount对象）
            amount: 转账金额
        """
        # 验证目标账户类型
        if not isinstance(other_account, BankAccount):
            raise TypeError("目标账户必须是BankAccount类型")

        # 验证金额
        if not self.is_valid_amount(amount):
            raise ValueError(f"转账金额不合法: {amount}")

        # 检查余额
        if amount > self._balance:
            raise ValueError(
                f"余额不足! 当前余额: {self._balance}元, 尝试转账: {amount}元"
            )

        # 执行转账：自己减钱，对方加钱
        self._balance -= amount
        other_account._balance += amount

        # 记录自己的交易
        self.transactions.append({
            "type": "transfer_out",
            "amount": amount,
            "to": other_account.owner,
            "balance_after": self._balance,
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

        # 记录对方的交易
        other_account.transactions.append({
            "type": "transfer_in",
            "amount": amount,
            "from": self.owner,
            "balance_after": other_account._balance,
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

        print(
            f"✅ 转账成功: {self.owner} → {other_account.owner} {amount}元"
        )

    def get_balance(self):
        """查询余额"""
        return self._balance

    def show_transactions(self):
        """显示所有交易记录"""
        if not self.transactions:
            print(f"📋 {self.owner}的交易记录为空")
            return

        print(f"\n📋 {self.owner}的交易记录:")
        print("-" * 50)
        for i, t in enumerate(self.transactions, 1):
            # 根据交易类型显示不同的信息
            if t["type"] == "deposit":
                desc = f"存款 +{t['amount']}元"
            elif t["type"] == "withdraw":
                desc = f"取款 -{t['amount']}元"
            elif t["type"] == "transfer_out":
                desc = f"转出 -{t['amount']}元 → {t['to']}"
            elif t["type"] == "transfer_in":
                desc = f"转入 +{t['amount']}元 ← {t['from']}"
            else:
                desc = f"未知操作"

            print(f"  {i}. [{t['time']}] {desc} | 余额: {t['balance_after']}元")
        print("-" * 50)

    # =============================================
    # 类方法
    # =============================================
    @classmethod
    def from_dict(cls, data):
        """
        从字典创建账户（替代构造方法）

        参数:
            data: 字典，如 {"owner": "张三", "balance": 1000}

        用法:
            acc = BankAccount.from_dict({"owner": "张三", "balance": 1000})
        """
        owner = data.get("owner")
        balance = data.get("balance", 0)

        if not owner:
            raise ValueError("字典中必须包含 'owner' 字段")

        # cls 就是 BankAccount，调用 cls() 等于调用 BankAccount()
        return cls(owner, balance)

    # =============================================
    # 静态方法
    # =============================================
    @staticmethod
    def is_valid_amount(amount):
        """
        验证金额是否合法

        合法条件：是数字类型（int或float）且大于0

        参数:
            amount: 待验证的金额

        返回:
            True/False
        """
        # isinstance 检查 amount 是不是 int 或 float 类型
        # 注意：bool 是 int 的子类，所以要排除 bool
        if isinstance(amount, bool):
            return False
        return isinstance(amount, (int, float)) and amount > 0

    # =============================================
    # 魔术方法（加分挑战）
    # =============================================
    def __str__(self):
        """
        print(account) 时调用
        给用户看的友好信息
        """
        return f"💳 {self.owner}的账户 | 余额: {self._balance}元"

    def __repr__(self):
        """
        调试时显示的信息
        在终端直接输入 account 回车时显示
        """
        return f"BankAccount(owner='{self.owner}', balance={self._balance})"


# =============================================
# 测试代码
# =============================================
if __name__ == "__main__":
    print("=" * 50)
    print("  银行账户系统测试")
    print("=" * 50)

    # 1. 创建账户
    print("\n--- 创建账户 ---")
    acc1 = BankAccount("张三", 1000)
    acc2 = BankAccount("李四", 500)
    print(acc1)  # 触发 __str__
    print(acc2)

    # 2. 存款
    print("\n--- 存款测试 ---")
    acc1.deposit(500)
    print(f"张三余额: {acc1.get_balance()}")  # 1500

    # 3. 取款
    print("\n--- 取款测试 ---")
    acc1.withdraw(200)
    print(f"张三余额: {acc1.get_balance()}")  # 1300

    # 4. 转账
    print("\n--- 转账测试 ---")
    acc1.transfer(acc2, 300)
    print(f"张三余额: {acc1.get_balance()}")  # 1000
    print(f"李四余额: {acc2.get_balance()}")  # 800

    # 5. 交易记录
    acc1.show_transactions()
    acc2.show_transactions()

    # 6. 类方法
    print("\n--- 类方法测试 ---")
    acc3 = BankAccount.from_dict({"owner": "王五", "balance": 2000})
    print(f"王五余额: {acc3.get_balance()}")  # 2000
    print(acc3)

    # 7. 错误处理
    print("\n--- 错误处理测试 ---")
    try:
        acc1.withdraw(99999)
    except ValueError as e:
        print(f"❌ 错误捕获: {e}")

    try:
        acc1.deposit(-100)
    except ValueError as e:
        print(f"❌ 错误捕获: {e}")

    try:
        acc1.deposit("一百块")
    except ValueError as e:
        print(f"❌ 错误捕获: {e}")

    # 8. 静态方法
    print("\n--- 静态方法测试 ---")
    print(f"100 是否合法: {BankAccount.is_valid_amount(100)}")    # True
    print(f"-50 是否合法: {BankAccount.is_valid_amount(-50)}")    # False
    print(f"'abc' 是否合法: {BankAccount.is_valid_amount('abc')}")  # False

    # 9. repr（调试信息）
    print("\n--- __repr__ 测试 ---")
    print(repr(acc1))  # BankAccount(owner='张三', balance=1000)

    print("\n✅ 所有测试通过!")
# ```
#
# ### 这段代码教你的核心知识点
#
# ```
# 1. __init__        → 第15行：初始化对象，设置属性
# 2. 实例方法        → deposit/withdraw/transfer：操作对象数据
# 3. 类方法          → from_dict：用 @classmethod 实现替代构造方法
# 4. 静态方法        → is_valid_amount：用 @staticmethod 实现工具函数
# 5. 访问控制        → self.owner / self._balance / self.__account_id
# 6. 错误处理        → raise ValueError + try/except
# 7. __str__         → print时的友好输出
# 8. __repr__        → 调试时的技术输出
# ```
#
# ### 怎么跑这段代码
#
# ```bash
# # 1. 把代码保存为 bank_system.py
# # 2. 打开终端，进入文件所在目录
# # 3. 运行：
# python bank_system.py
# ```