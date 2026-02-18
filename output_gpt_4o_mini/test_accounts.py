# import unittest and the Account class from accounts module for testing
import unittest
from accounts import Account, get_share_price

# test case class for the Account class functionalities
class TestAccount(unittest.TestCase):
    # setup runs before each test method to create a fresh Account instance
    def setUp(self):
        self.account = Account("test123", 1000.0)
    
    # test get_share_price returns correct fixed prices for known symbols and 0.0 for unknown
    def test_get_share_price(self):
        self.assertEqual(get_share_price("AAPL"), 150.0)
        self.assertEqual(get_share_price("TSLA"), 700.0)
        self.assertEqual(get_share_price("GOOGL"), 2800.0)
        self.assertEqual(get_share_price("UNKNOWN"), 0.0)
    
    # test deposit_funds increases balance properly and rejects non-positive amounts
    def test_deposit_funds(self):
        self.account.deposit_funds(500.0)
        self.assertEqual(self.account.balance, 1500.0)
        with self.assertRaises(ValueError):
            self.account.deposit_funds(0)
        with self.assertRaises(ValueError):
            self.account.deposit_funds(-100)
    
    # test withdraw_funds returns True if funds sufficient and reduces balance, else False
    def test_withdraw_funds(self):
        self.assertTrue(self.account.withdraw_funds(200.0))
        self.assertEqual(self.account.balance, 800.0)
        self.assertFalse(self.account.withdraw_funds(2000.0))  # insufficient funds
        self.assertFalse(self.account.withdraw_funds(0))  # zero amount
        self.assertFalse(self.account.withdraw_funds(-50))  # negative amount
    
    # test buy_shares succeeds if affordable, adjusts holdings and balance, rejects invalid quantity
    def test_buy_shares(self):
        result = self.account.buy_shares("AAPL", 2)  # cost 2*150=300, balance 1000
        self.assertTrue(result)
        self.assertEqual(self.account.holdings.get("AAPL"), 2)
        self.assertAlmostEqual(self.account.balance, 700.0)
        result = self.account.buy_shares("TSLA", 2)  # cost 1400, balance 700 (fail)
        self.assertFalse(result)
        result = self.account.buy_shares("GOOGL", 0)  # zero quantity fail
        self.assertFalse(result)
        result = self.account.buy_shares("GOOGL", -1)  # negative quantity fail
        self.assertFalse(result)
    
    # test sell_shares works only if enough shares owned, updates holdings and balance, rejects invalid qty
    def test_sell_shares(self):
        self.account.buy_shares("AAPL", 3)
        result = self.account.sell_shares("AAPL", 2)
        self.assertTrue(result)
        self.assertEqual(self.account.holdings.get("AAPL"), 1)
        expected_balance = 1000 - 3*150 + 2*150
        self.assertAlmostEqual(self.account.balance, expected_balance)
        result = self.account.sell_shares("AAPL", 2)  # trying to sell more than owned
        self.assertFalse(result)
        result = self.account.sell_shares("TSLA", 1)  # no shares owned
        self.assertFalse(result)
        self.assertFalse(self.account.sell_shares("AAPL", 0))  # zero quantity fail
        self.assertFalse(self.account.sell_shares("AAPL", -1))  # negative quantity fail
    
    # test selling all shares removes the symbol from holdings
    def test_sell_all_shares_removes_holding(self):
        self.account.buy_shares("TSLA", 1)
        self.assertIn("TSLA", self.account.holdings)
        self.account.sell_shares("TSLA", 1)
        self.assertNotIn("TSLA", self.account.holdings)
    
    # test get_portfolio_value calculates cash plus current market value of holdings
    def test_get_portfolio_value(self):
        self.account.buy_shares("AAPL", 2)  # buy 2 AAPL at 150 each
        value = self.account.get_portfolio_value()
        expected_value = self.account.balance + 2 * get_share_price("AAPL")
        self.assertAlmostEqual(value, expected_value)
    
    # test get_profit_or_loss returns portfolio value minus initial deposit
    def test_get_profit_or_loss(self):
        self.account.buy_shares("AAPL", 2)
        expected_profit_or_loss = self.account.get_portfolio_value() - self.account.initial_deposit
        self.assertAlmostEqual(self.account.get_profit_or_loss(), expected_profit_or_loss)
    
    # test report_holdings returns a copy of holdings dict matching current holdings
    def test_report_holdings(self):
        self.account.buy_shares("AAPL", 1)
        holdings_report = self.account.report_holdings()
        self.assertEqual(holdings_report, self.account.holdings)
        holdings_report["AAPL"] = 100  # modify copy
        self.assertNotEqual(self.account.holdings["AAPL"], 100)  # original unchanged
    
    # test report_transactions returns a copy list of all transactions matching actual transactions
    def test_report_transactions(self):
        self.account.buy_shares("AAPL", 1)
        self.account.sell_shares("AAPL", 1)
        transactions_report = self.account.report_transactions()
        self.assertEqual(transactions_report, self.account.transactions)
        transactions_report.append({})
        self.assertNotEqual(len(transactions_report), len(self.account.transactions))  # original unchanged

# run the tests if this script is executed
if __name__ == "__main__":
    unittest.main()