import gradio as gr
from accounts import Account

# Create a sample account for demonstration purposes
account = Account(user_id='demo_user', initial_deposit=1000.0)

def create_account(initial_deposit):
    # Create a new account with an initial deposit
    global account
    account = Account(user_id='demo_user', initial_deposit=float(initial_deposit))
    return "Account created successfully."

def deposit_funds(amount):
    # Deposit funds into the account
    account.deposit(float(amount))
    return f"Deposited {amount} to account."

def withdraw_funds(amount):
    # Withdraw funds from the account, ensuring sufficient balance
    if account.withdraw(float(amount)):
        return f"Withdrew {amount} from account."
    else:
        return "Insufficient funds, withdrawal failed."

def buy_shares(symbol, quantity):
    # Buy shares for a given symbol and quantity, ensuring sufficient balance
    if account.buy_shares(symbol, int(quantity)):
        return f"Bought {quantity} shares of {symbol}."
    else:
        return "Insufficient funds to buy shares."

def sell_shares(symbol, quantity):
    # Sell shares for a given symbol and quantity, ensuring sufficient holdings
    if account.sell_shares(symbol, int(quantity)):
        return f"Sold {quantity} shares of {symbol}."
    else:
        return "Insufficient shares to sell."

def get_account_summary():
    # Get a summary of the account
    return account.get_account_summary()

def get_transactions():
    # Get a list of transactions made by the user
    return account.get_transactions()

# Define the Gradio UI interface
with gr.Blocks() as demo:
    gr.Markdown("# Trading Account Management System")
    
    with gr.Tab("Account"):
        initial_deposit_input = gr.Number(label="Initial Deposit")
        create_account_btn = gr.Button("Create Account")
        account_output = gr.Textbox(label="Status", interactive=False)
        create_account_btn.click(create_account, inputs=initial_deposit_input, outputs=account_output)
        
        deposit_input = gr.Number(label="Deposit Amount")
        deposit_btn = gr.Button("Deposit Funds")
        deposit_btn.click(deposit_funds, inputs=deposit_input, outputs=account_output)
        
        withdraw_input = gr.Number(label="Withdraw Amount")
        withdraw_btn = gr.Button("Withdraw Funds")
        withdraw_btn.click(withdraw_funds, inputs=withdraw_input, outputs=account_output)
    
    with gr.Tab("Trading"):
        symbol_input_buy = gr.Textbox(label="Share Symbol", placeholder="AAPL, TSLA, GOOGL etc.")
        quantity_input_buy = gr.Number(label="Quantity to Buy")
        buy_btn = gr.Button("Buy Shares")
        trading_output = gr.Textbox(label="Status", interactive=False)
        buy_btn.click(buy_shares, inputs=[symbol_input_buy, quantity_input_buy], outputs=trading_output)
        
        symbol_input_sell = gr.Textbox(label="Share Symbol", placeholder="AAPL, TSLA, GOOGL etc.")
        quantity_input_sell = gr.Number(label="Quantity to Sell")
        sell_btn = gr.Button("Sell Shares")
        sell_btn.click(sell_shares, inputs=[symbol_input_sell, quantity_input_sell], outputs=trading_output)
        
    with gr.Tab("Reports"):
        summary_btn = gr.Button("Get Account Summary")
        summary_output = gr.Textbox(placeholder="Account summary will appear here", lines=5)
        summary_btn.click(get_account_summary, inputs=None, outputs=summary_output)
        
        transactions_btn = gr.Button("Get Transactions")
        transactions_output = gr.Textbox(placeholder="Transactions log will appear here", lines=5)
        transactions_btn.click(get_transactions, inputs=None, outputs=transactions_output)

# Launch the Gradio interface
demo.launch()