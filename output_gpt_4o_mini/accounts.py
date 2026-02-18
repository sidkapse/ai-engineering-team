# accounts.py module for account management in a trading simulation platform
import time

# function to get current fixed share prices for testing purposes
def get_share_price(symbol: str) -> float:
    prices = {
        "AAPL": 150.0,
        "TSLA": 700.0,
        "GOOGL": 2800.0
    }
    return prices.get(symbol, 0.0)

# Account class managing deposits, withdrawals, share transactions, and reporting
class Account:
    # initialize account with id, initial deposit, empty holdings, and transactions list
    def __init__(self, account_id: str, initial_deposit: float) -> None:
        self.account_id = account_id
        self.balance = initial_deposit
        self.initial_deposit = initial_deposit
        self.holdings = {}
        self.transactions = []
    
    # add funds to the account balance ensuring positive amount
    def deposit_funds(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")
        self.balance += amount
    
    # withdraw funds if sufficient balance and positive amount, return success status
    def withdraw_funds(self, amount: float) -> bool:
        if amount <= 0:
            return False
        if self.balance >= amount:
            self.balance -= amount
            return True
        return False
    
    # buy shares if affordable, update holdings and balance, record transaction, return success
    def buy_shares(self, symbol: str, quantity: int) -> bool:
        if quantity <= 0:
            return False
        price_per_share = get_share_price(symbol)
        total_cost = price_per_share * quantity
        if total_cost > self.balance:
            return False
        self.balance -= total_cost
        self.holdings[symbol] = self.holdings.get(symbol, 0) + quantity
        self._record_transaction("BUY", symbol, quantity, price_per_share)
        return True
    
    # sell shares if owned quantity sufficient, update holdings and balance, record transaction, return success
    def sell_shares(self, symbol: str, quantity: int) -> bool:
        if quantity <= 0:
            return False
        owned = self.holdings.get(symbol, 0)
        if owned < quantity:
            return False
        price_per_share = get_share_price(symbol)
        total_revenue = price_per_share * quantity
        self.balance += total_revenue
        self.holdings[symbol] = owned - quantity
        if self.holdings[symbol] == 0:
            del self.holdings[symbol]
        self._record_transaction("SELL", symbol, quantity, price_per_share)
        return True
    
    # calculate total portfolio value as cash balance plus market value of all holdings
    def get_portfolio_value(self) -> float:
        holdings_value = sum(get_share_price(sym) * qty for sym, qty in self.holdings.items())
        return self.balance + holdings_value
    
    # calculate profit or loss compared to initial deposit
    def get_profit_or_loss(self) -> float:
        return self.get_portfolio_value() - self.initial_deposit
    
    # return a copy of current holdings dictionary
    def report_holdings(self) -> dict:
        return dict(self.holdings)
    
    # return a copy of the list of all transactions
    def report_transactions(self) -> list:
        return list(self.transactions)
    
    # internal method to record a transaction with timestamp, action, symbol, qty, and price
    def _record_transaction(self, action: str, symbol: str, quantity: int, price: float) -> None:
        self.transactions.append({
            "timestamp": time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime()),
            "action": action,
            "symbol": symbol,
            "quantity": quantity,
            "price": price
        })