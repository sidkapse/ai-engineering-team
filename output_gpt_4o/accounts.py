# Account Management System Module

class Account:
    def __init__(self, user_id: str, initial_deposit: float) -> None:
        # Initialize account with user ID, initial deposit, and set balance
        self.user_id = user_id
        self.balance = initial_deposit
        self.holdings = {}
        self.transactions = []
        self.initial_deposit = initial_deposit

    def deposit(self, amount: float) -> None:
        # Deposit funds into the account
        self.balance += amount

    def withdraw(self, amount: float) -> bool:
        # Attempt to withdraw funds from the account
        if amount <= self.balance:
            self.balance -= amount
            return True
        return False

    def buy_shares(self, symbol: str, quantity: int) -> bool:
        # Buy shares if funds are sufficient
        price = self.get_share_price(symbol)
        cost = price * quantity
        if cost <= self.balance:
            self.balance -= cost
            self.holdings[symbol] = self.holdings.get(symbol, 0) + quantity
            self.record_transaction('buy', symbol, quantity, price)
            return True
        return False

    def sell_shares(self, symbol: str, quantity: int) -> bool:
        # Sell shares if quantity owned is sufficient
        if symbol in self.holdings and self.holdings[symbol] >= quantity:
            price = self.get_share_price(symbol)
            revenue = price * quantity
            self.holdings[symbol] -= quantity
            self.balance += revenue
            self.record_transaction('sell', symbol, quantity, price)
            if self.holdings[symbol] == 0:
                del self.holdings[symbol]
            return True
        return False

    def get_portfolio_value(self) -> float:
        # Calculate total portfolio value based on current share prices
        total_value = self.balance
        for symbol, quantity in self.holdings.items():
            total_value += self.get_share_price(symbol) * quantity
        return total_value

    def get_profit_or_loss(self) -> float:
        # Calculate profit or loss based on initial deposit
        return self.get_portfolio_value() - self.initial_deposit

    def get_holdings(self) -> dict:
        # Return current holdings of the user
        return self.holdings.copy()

    def get_transactions(self) -> list:
        # Return a list of all transactions made by the user
        return self.transactions.copy()

    def get_account_summary(self) -> dict:
        # Return a summary of the account
        return {
            'user_id': self.user_id,
            'balance': self.balance,
            'holdings': self.get_holdings(),
            'portfolio_value': self.get_portfolio_value(),
            'profit_or_loss': self.get_profit_or_loss()
        }

    def record_transaction(self, transaction_type: str, symbol: str, quantity: int, price: float) -> None:
        # Record a transaction in the transactions list
        self.transactions.append({
            'type': transaction_type,
            'symbol': symbol,
            'quantity': quantity,
            'price': price
        })

    @staticmethod
    def get_share_price(symbol: str) -> float:
        # Return fixed prices for testing
        prices = {
            'AAPL': 150.0,
            'TSLA': 600.0,
            'GOOGL': 2800.0
        }
        return prices.get(symbol, 0.0)

# Test basic functionality
account = Account(user_id='user123', initial_deposit=1000.0)
account.deposit(500.0)
account.buy_shares('AAPL', 5)
account.sell_shares('AAPL', 2)
account.withdraw(200.0)
summary = account.get_account_summary()
transactions = account.get_transactions()
print(summary)
print(transactions)