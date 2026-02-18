import unittest
from accounts import Account

class TestAccount(unittest.TestCase):
    # Test account initialization
    def test_initialization(self):
        account = Account('user123', 1000.0)
        self.assertEqual(account.user_id, 'user123')
        self.assertEqual(account.balance, 1000.0)
        self.assertEqual(account.holdings, {})
        self.assertEqual(account.transactions, [])

    # Test deposit method
    def test_deposit(self):
        account = Account('user123', 1000.0)
        account.deposit(500.0)
        self.assertEqual(account.balance, 1500.0)

    # Test withdraw method for successful transaction
    def test_withdraw_success(self):
        account = Account('user123', 1000.0)
        result = account.withdraw(200.0)
        self.assertTrue(result)
        self.assertEqual(account.balance, 800.0)

    # Test withdraw method for unsuccessful transaction
    def test_withdraw_failure(self):
        account = Account('user123', 1000.0)
        result = account.withdraw(1200.0)
        self.assertFalse(result)
        self.assertEqual(account.balance, 1000.0)

    # Test buying shares successfully
    def test_buy_shares_success(self):
        account = Account('user123', 1000.0)
        result = account.buy_shares('AAPL', 5)
        self.assertTrue(result)
        self.assertEqual(account.balance, 250.0)
        self.assertEqual(account.holdings['AAPL'], 5)

    # Test buying shares with insufficient balance
    def test_buy_shares_insufficient_balance(self):
        account = Account('user123', 200.0)
        result = account.buy_shares('AAPL', 5)
        self.assertFalse(result)
        self.assertEqual(account.balance, 200.0)
        self.assertNotIn('AAPL', account.holdings)

    # Test selling shares successfully
    def test_sell_shares_success(self):
        account = Account('user123', 1000.0)
        account.buy_shares('AAPL', 5)
        result = account.sell_shares('AAPL', 2)
        self.assertTrue(result)
        self.assertEqual(account.balance, 550.0)
        self.assertEqual(account.holdings['AAPL'], 3)

    # Test selling shares with insufficient holdings
    def test_sell_shares_insufficient_holdings(self):
        account = Account('user123', 1000.0)
        account.buy_shares('AAPL', 5)
        result = account.sell_shares('AAPL', 10)
        self.assertFalse(result)
        self.assertEqual(account.holdings['AAPL'], 5)

    # Test get_portfolio_value
    def test_get_portfolio_value(self):
        account = Account('user123', 1000.0)
        account.buy_shares('AAPL', 2)
        account.buy_shares('TSLA', 1)
        value = account.get_portfolio_value()
        expected_value = account.balance + account.get_share_price('AAPL') * 2 + account.get_share_price('TSLA') * 1
        self.assertEqual(value, expected_value)

    # Test get_profit_or_loss
    def test_get_profit_or_loss(self):
        account = Account('user123', 1000.0)
        account.buy_shares('AAPL', 5)
        account.sell_shares('AAPL', 3)
        profit_or_loss = account.get_profit_or_loss()
        self.assertEqual(profit_or_loss, account.get_portfolio_value() - 1000.0)

    # Test get_holdings
    def test_get_holdings(self):
        account = Account('user123', 1000.0)
        account.buy_shares('AAPL', 5)
        holdings = account.get_holdings()
        self.assertEqual(holdings, {'AAPL': 5})

    # Test get_transactions
    def test_get_transactions(self):
        account = Account('user123', 1000.0)
        account.buy_shares('AAPL', 2)
        account.sell_shares('AAPL', 1)
        transactions = account.get_transactions()
        self.assertEqual(len(transactions), 2)
        self.assertEqual(transactions[0]['type'], 'buy')
        self.assertEqual(transactions[1]['type'], 'sell')

    # Test get_account_summary
    def test_get_account_summary(self):
        account = Account('user123', 1000.0)
        account.buy_shares('AAPL', 2)
        account.sell_shares('AAPL', 1)
        summary = account.get_account_summary()
        self.assertEqual(summary['user_id'], 'user123')
        self.assertEqual(summary['balance'], account.balance)
        self.assertEqual(summary['holdings']['AAPL'], 1)

if __name__ == '__main__':
    unittest.main()