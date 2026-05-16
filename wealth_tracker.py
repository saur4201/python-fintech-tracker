import yfinance as yf
from tabulate import tabulate

def fetch_live_portfolio(portfolio):
    """
    Fetches live prices for a given portfolio and calculates profit/loss.
    """
    tracked_portfolio = []
    total_initial_cost = 0.0
    total_current_value = 0.0

    print("Fetching live market data...\n")

    for asset in portfolio:
        ticker_symbol = asset["ticker"]
        shares_owned = asset["shares"]
        avg_buy_price = asset["buy_price"]

        try:
            # Fetch live ticker data using yfinance
            ticker = yf.Ticker(ticker_symbol)
            
            # Get the most recent closing or live price
            # fast_info gives quick access to the latest price point
            live_price = ticker.fast_info['last_price']
            
            # Fallback if fast_info fails
            if live_price is None or live_price <= 0:
                history = ticker.history(period="1d")
                if not history.empty:
                    live_price = history['Close'].iloc[-1]
                else:
                    raise ValueError("No price data found")

            # Financial Calculations
            initial_cost = shares_owned * avg_buy_price
            current_value = shares_owned * live_price
            net_profit_loss = current_value - initial_cost
            
            # Calculate percentage change
            percentage_gain_loss = (net_profit_loss / initial_cost) * 100 if initial_cost > 0 else 0.0

            # Accumulate totals
            total_initial_cost += initial_cost
            total_current_value += current_value

            # Format row data for display
            tracked_portfolio.append([
                ticker_symbol.upper(),
                f"{shares_owned:,.4f}" if asset["is_crypto"] else f"{shares_owned:,.2f}",
                f"${avg_buy_price:,.2f}",
                f"${live_price:,.2f}",
                f"${current_value:,.2f}",
                f"${net_profit_loss:+,.2f} ({percentage_gain_loss:+.2f}%)"
            ])

        except Exception as e:
            print(f"⚠️ Error fetching data for {ticker_symbol}: {e}")
            continue

    # Final summary calculations
    overall_profit_loss = total_current_value - total_initial_cost
    overall_percentage = (overall_profit_loss / total_initial_cost) * 100 if total_initial_cost > 0 else 0.0

    # Display the results in a clean table format
    headers = ["Asset Ticker", "Units/Shares", "Avg Buy Price", "Live Price", "Current Value", "Profit / Loss"]
    print(tabulate(tracked_portfolio, headers=headers, tablefmt="grid"))
    
    print("\n" + "="*50)
    print("PORTFOLIO SUMMARY")
    print("="*50)
    print(f"Total Invested Amount: ${total_initial_cost:,.2f}")
    print(f"Total Current Value:  ${total_current_value:,.2f}")
    print(f"Overall Profit/Loss:  ${overall_profit_loss:+,.2f} ({overall_percentage:+.2f}%)")
    print("="*50)

if __name__ == "__main__":
    # Define your portfolio here. 
    # Use standard stock tickers (e.g., 'AAPL', 'MSFT').
    # For Crypto, use the Yahoo Finance convention: <Symbol>-USD (e.g., 'BTC-USD', 'ETH-USD').
    my_portfolio = [
        {"ticker": "AAPL", "shares": 10, "buy_price": 150.00, "is_crypto": False},
        {"ticker": "MSFT", "shares": 5, "buy_price": 280.00, "is_crypto": False},
        {"ticker": "BTC-USD", "shares": 0.05, "buy_price": 45000.00, "is_crypto": True},
        {"ticker": "ETH-USD", "shares": 0.5, "buy_price": 25000.00, "is_crypto": True}
    ]

    fetch_live_portfolio(my_portfolio)
