from flask import Flask
import threading
import os
import time
import asyncio

app = Flask(__name__)

@app.route('/')
def home():
    return "🔥 TIMEX AI Bot is Running!"

@app.route('/health')
def health():
    return "OK", 200

def run_bot():
    """Run Telegram bot in background"""
    try:
        # Import and run your bot
        import sqli
        # sqli.main() if you have main function
        print("✅ Bot thread started!")
    except Exception as e:
        print(f"❌ Bot error: {e}")

if __name__ == '__main__':
    # Start bot in background
    bot_thread = threading.Thread(target=run_bot)
    bot_thread.daemon = True
    bot_thread.start()
    
    print("🚀 Flask server starting...")
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
