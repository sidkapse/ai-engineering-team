# import necessary modules and backend Account class and get_share_price function
import gradio as gr
from accounts import Account, get_share_price

# initialize a global variable for a single Account instance, initially None
account = None

# function to create a new account with a given initial deposit
def create_account(initial_deposit):
    global account
    if initial_deposit <= 0:
        return "Initial deposit must be greater than zero.", "", "", "", "", ""
    account = Account("user1", initial_deposit)
    return (f"Account created with initial deposit ${initial_deposit:.2f}.",
            "", "", "", "", "")

# function to deposit funds into the account
def deposit(amount):
    if account is None:
        return "Please create an account first.", ""
    try:
        account.deposit_funds(amount)
        return f"Deposited ${amount:.2f}. New balance: ${account.balance:.2f}.", ""
    except Exception as e:
        return str(e), ""

# function to withdraw funds from the account
def withdraw(amount):
    if account is None:
        return "Please create an account first.", ""
    if amount <= 0:
        return "Withdrawal amount must be positive.", ""
    success = account.withdraw_funds(amount)
    if success:
        return f"Withdrew ${amount:.2f}. New balance: ${account.balance:.2f}.", ""
    else:
        return "Insufficient funds for withdrawal.", ""

# function to buy shares of a symbol with given quantity
def buy(symbol, quantity):
    if account is None:
        return "Please create an account first.", ""
    symbol = symbol.upper()
    if symbol not in ["AAPL", "TSLA", "GOOGL"]:
        return "Invalid symbol. Choose AAPL, TSLA, or GOOGL.", ""
    if quantity <= 0:
        return "Quantity must be greater than zero.", ""
    success = account.buy_shares(symbol, quantity)
    if success:
        return (f"Bought {quantity} shares of {symbol} "
                f"at ${get_share_price(symbol):.2f} each. "
                f"New balance: ${account.balance:.2f}."), ""
    else:
        return "Insufficient funds to buy shares.", ""

# function to sell shares of a symbol with given quantity
def sell(symbol, quantity):
    if account is None:
        return "Please create an account first.", ""
    symbol = symbol.upper()
    if symbol not in ["AAPL", "TSLA", "GOOGL"]:
        return "Invalid symbol. Choose AAPL, TSLA, or GOOGL.", ""
    if quantity <= 0:
        return "Quantity must be greater than zero.", ""
    success = account.sell_shares(symbol, quantity)
    if success:
        return (f"Sold {quantity} shares of {symbol} "
                f"at ${get_share_price(symbol):.2f} each. "
                f"New balance: ${account.balance:.2f}."), ""
    else:
        return "Not enough shares to sell.", ""

# function to get current account summary: holdings, portfolio value, profit/loss, and transactions
def get_summary():
    if account is None:
        return "", "", "", ""
    holdings = account.report_holdings()
    holdings_str = "Holdings:\n" + "\n".join(
        [f"{sym}: {qty}" for sym, qty in holdings.items()]) if holdings else "Holdings: None"
    portfolio_value = account.get_portfolio_value()
    profit_loss = account.get_profit_or_loss()
    profit_loss_str = f"Profit/Loss: ${profit_loss:.2f}"
    transactions = account.report_transactions()
    if not transactions:
        transactions_str = "No transactions yet."
    else:
        lines = ["Timestamp | Action | Symbol | Quantity | Price"]
        for tx in transactions:
            line = (f"{tx['timestamp']} | {tx['action']} | {tx['symbol']} | "
                    f"{tx['quantity']} | ${tx['price']:.2f}")
            lines.append(line)
        transactions_str = "\n".join(lines)
    summary = (f"Current Balance: ${account.balance:.2f}\n"
               f"Total Portfolio Value: ${portfolio_value:.2f}\n{profit_loss_str}")
    return holdings_str, summary, transactions_str, ""

# create Gradio interface components and layout
with gr.Blocks() as demo:
    gr.Markdown("# Trading Simulation Account Management Demo")
    
    with gr.Row():
        initial_deposit_input = gr.Number(label="Initial Deposit ($)", value=1000, precision=2)
        create_btn = gr.Button("Create Account")
    create_output = gr.Textbox(label="Account Status", interactive=False)
    
    with gr.Row():
        deposit_input = gr.Number(label="Deposit Amount ($)", value=0, precision=2)
        deposit_btn = gr.Button("Deposit Funds")
    deposit_output = gr.Textbox(label="Deposit Status", interactive=False)
    
    with gr.Row():
        withdraw_input = gr.Number(label="Withdraw Amount ($)", value=0, precision=2)
        withdraw_btn = gr.Button("Withdraw Funds")
    withdraw_output = gr.Textbox(label="Withdraw Status", interactive=False)
    
    with gr.Row():
        buy_symbol = gr.Dropdown(["AAPL", "TSLA", "GOOGL"], label="Buy Shares: Symbol")
        buy_quantity = gr.Number(label="Quantity to Buy", value=0, precision=0)
        buy_btn = gr.Button("Buy Shares")
    buy_output = gr.Textbox(label="Buy Status", interactive=False)
    
    with gr.Row():
        sell_symbol = gr.Dropdown(["AAPL", "TSLA", "GOOGL"], label="Sell Shares: Symbol")
        sell_quantity = gr.Number(label="Quantity to Sell", value=0, precision=0)
        sell_btn = gr.Button("Sell Shares")
    sell_output = gr.Textbox(label="Sell Status", interactive=False)
    
    holdings_display = gr.Textbox(label="Holdings", interactive=False, lines=5)
    summary_display = gr.Textbox(label="Account Summary", interactive=False, lines=4)
    transactions_display = gr.Textbox(label="Transactions", interactive=False, lines=10)
    
    # bind buttons to respective functions with outputs connected to UI elements
    create_btn.click(create_account, inputs=initial_deposit_input,
                     outputs=[create_output, holdings_display, summary_display, transactions_display, deposit_output, withdraw_output])
    deposit_btn.click(deposit, inputs=deposit_input, outputs=[deposit_output, summary_display]).then(get_summary, inputs=None, outputs=[holdings_display, summary_display, transactions_display, sell_output])
    withdraw_btn.click(withdraw, inputs=withdraw_input, outputs=[withdraw_output, summary_display]).then(get_summary, inputs=None, outputs=[holdings_display, summary_display, transactions_display, sell_output])
    buy_btn.click(buy, inputs=[buy_symbol, buy_quantity], outputs=[buy_output, summary_display]).then(get_summary, inputs=None, outputs=[holdings_display, summary_display, transactions_display, sell_output])
    sell_btn.click(sell, inputs=[sell_symbol, sell_quantity], outputs=[sell_output, summary_display]).then(get_summary, inputs=None, outputs=[holdings_display, summary_display, transactions_display, sell_output])

# run the demo app
demo.launch()