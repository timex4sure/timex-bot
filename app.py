from flask import Flask
import threading
import os
import time

app = Flask(__name__)

@app.route('/')
def home():
    return "🔥 TIMEX AI Bot is Running!"

@app.route('/health')
def health():
    return "OK", 200

def run_bot():
    """Run your Telegram bot in background"""
    try:
        # Import your bot code
        import sqli
        # sqli.main() if you have main function
    except Exception as e:
        print(f"Bot error: {e}")

if __name__ == '__main__':
    # Start bot in background thread
    bot_thread = threading.Thread(target=run_bot)
    bot_thread.daemon = True
    bot_thread.start()
    
    # Run Flask server
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
