import functions_framework
from flask import jsonify, request
import yfinance as yf
from datetime import datetime, timezone

@functions_framework.http
def get_earnings_dates(request):
    request_json = request.get_json(silent=True)
    symbols = request_json.get('symbols', [])
    results = {}

    for symbol in symbols:
        try:
            ticker = yf.Ticker(symbol)
            df = ticker.get_earnings_dates(limit=12)
            df = df.reset_index()
            df['Earnings Date'] = df['Earnings Date'].dt.tz_convert(None)

            # Filter for future dates
            now = datetime.now()
            future_df = df[df['Earnings Date'] > now]
            if not future_df.empty:
                next_row = future_df.iloc[0]
                date = next_row['Earnings Date'].strftime('%Y-%m-%d')
                time = next_row['Time']
                results[symbol] = f"{date} ({time})"
            else:
                results[symbol] = "No upcoming date"
        except Exception as e:
            results[symbol] = f"Error: {str(e)}"
    return jsonify(results)
