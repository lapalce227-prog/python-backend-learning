class BankAccount:
    def __init__(self ,owner : str,initial_balance : float = 0 ) -> None :
        self.owner : str  = owner
        self._balance : float  = initial_balance
        self.transactions : list[dict] = []

    def deposit(self, amount : float) -> None :
        if not isinstance(amount , (int, float)) or amount <= 0:
            raise ValueError(f"存款金额不合法: {amount}")

        self._balance += amount
        self.transactions.append({
            "type": "deposit",
            "amount": amount
        })
        print(f"存款成功: +{amount}元, 余额: {self._balance}元")

    def withdraw(self, amount : float) -> None :
        if not isinstance(amount, (int, float)) or amount <= 0:
            raise ValueError(f"取款金额不合法: {amount}")

        if amount > self._balance:
            raise ValueError(f"余额不足! 余额: {self._balance}元, 取款: {amount}元")

        self._balance -= amount
        self.transactions.append({
            "type": "withdraw",
            "amount": amount
        })
        print(f"取款成功: {-amount}元, 余额: {self._balance}元")

    def transfer(self, other_account : "BankAccount" , amount : float) -> None :
        if not isinstance(other_account, BankAccount):
            raise TypeError("目标账户必须是BankAccount类型")

        if not isinstance(amount, (int, float)) or amount <= 0:
            raise ValueError(f"转账金额不合法: {amount}")

        if amount > self._balance:
            raise ValueError(f"余额不足! 余额: {self._balance}元, 转账: {amount}元")

        self._balance -= amount
        other_account._balance += amount

        self.transactions.append({
            "type": "transfer_out",
            "amount": amount,
            "to": other_account.owner
        })
        other_account.transactions.append({
            "type": "transfer_in",
            "amount": amount,
            "from": self.owner
        })
        print(f"转账成功: {self.owner} → {other_account.owner} {amount}元")

    def get_balance(self) -> float :
        return self._balance

    def show_transactions(self) -> None:
        print(f"\n{self.owner}的交易记录:")
        for i, t in enumerate(self.transactions, 1):
            print(f"  {i}. {t}")

# if __name__ == "__main__":
#     acc1 = BankAccount("张三", 1000)
#     acc2 = BankAccount("李四", 500)
#
#     acc1.deposit(500)
#     acc1.withdraw(200)
#     acc1.transfer(acc2, 300)
#
#     print(f"张三余额: {acc1.get_balance()}")
#     print(f"李四余额: {acc2.get_balance()}")
#
#     acc1.show_transactions()
#     acc2.show_transactions()

class SavingsAccount(BankAccount):
    """储蓄账户"""

    def __init__(self, owner : str, initial_balance: float =0, interest_rate :float =0.03):
        super().__init__(owner, initial_balance)
        self.interest_rate: float = interest_rate

    def apply_interest(self) -> None:
        """计算并添加利息"""
        interestmoney  : float  = self._balance * self.interest_rate
        self._balance += interestmoney
        self.transactions.append({
            "type": "interest",
            "amount": interestmoney
        })
        print(f"利息到账：+{interestmoney}元,余额为{self._balance}元")

    def withdraw(self, amount : float) -> None :
        """取款（额外收2元手续费）"""
        actual_amount = amount + 2
        super().withdraw(actual_amount)


class CreditAccount(BankAccount):
    """信用账户"""

    def __init__(self, owner : str, initial_balance : float =0, credit_limit : float =5000):
        super().__init__(owner, initial_balance)
        self.credit_limit : float =credit_limit

    def withdraw(self, amount : float) -> None :
        if not isinstance(amount, (int, float)) or amount <= 0:
            raise ValueError(f"取款金额不合法: {amount}")

        if amount > self.available_credit():
            raise ValueError(f"超出额度! 可用: {self.available_credit()}元, 取款: {amount}元")

        self._balance -= amount
        self.transactions.append({
            "type": "withdraw",
            "amount": amount
        })
        print(f"取款成功: -{amount}元, 余额: {self._balance}元")

    def available_credit(self):
        """返回可用额度"""
        return self._balance + self.credit_limit

if __name__ == "__main__":
    savings = SavingsAccount("张三", 10000, 0.05)
    savings.apply_interest()
    print(f"余额: {savings.get_balance()}")  # 10500

    savings.withdraw(1000)
    print(f"余额: {savings.get_balance()}")  # 9498

    credit = CreditAccount("李四", 1000, 5000)
    print(f"可用额度: {credit.available_credit()}")  # 6000

    credit.withdraw(3000)
    print(f"余额: {credit.get_balance()}")  # -2000
    print(f"可用额度: {credit.available_credit()}")  # 3000