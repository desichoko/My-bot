import telebot
import asyncio
import aiohttp
import re
import time

# New bot token
BOT_TOKEN = "7798867064:AAE_KMx5hZ9rE_i4hD2GfXPZwjkij6wWh_c"
bot = telebot.TeleBot(BOT_TOKEN)

# Country flags dictionary
COUNTRY_FLAGS = {
    "FRANCE": "🇫🇷", "UNITED STATES": "🇺🇸", "BRAZIL": "🇧🇷", "NAMIBIA": "🇳🇦",
    "INDIA": "🇮🇳", "GERMANY": "🇩🇪", "THAILAND": "🇹🇭", "MEXICO": "🇲🇽", "RUSSIA": "🇷🇺",
}

def extract_bin(bin_input):
    match = re.match(r'(\d{6,16})', bin_input)
    if not match:
        return None
    bin_number = match.group(1)
    return bin_number.ljust(16, 'x') if len(bin_number) == 6 else bin_number

async def lookup_bin(bin_number):
    url = f"https://drlabapis.onrender.com/api/bin?bin={bin_number[:6]}"
    print(f"Calling BIN API: {url}")
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=10) as response:
                print(f"API Response Status: {response.status}")
                if response.status == 200:
                    bin_data = await response.json()
                    print(f"API Response Data: {bin_data}")
                    country_name = bin_data.get('country', 'NOT FOUND').upper()
                    return {
                        "bank": bin_data.get('issuer', 'NOT FOUND').upper(),
                        "card_type": bin_data.get('type', 'NOT FOUND').upper(),
                        "network": bin_data.get('scheme', 'NOT FOUND').upper(),
                        "tier": bin_data.get('tier', 'NOT FOUND').upper(),
                        "country": country_name,
                        "flag": COUNTRY_FLAGS.get(country_name, "🏳️")
                    }
                else:
                    return {"error": f"API error: {response.status}"}
    except Exception as e:
        print(f"API Error: {e}")
        return {"error": str(e)}

async def generate_cc_async(bin_number):
    url = f"https://drlabapis.onrender.com/api/ccgenerator?bin={bin_number}&count=10"
    print(f"Calling CC Generator API: {url}")
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=10) as response:
                print(f"CC API Response Status: {response.status}")
                if response.status == 200:
                    raw_text = await response.text()
                    print(f"CC API Response Data: {raw_text}")
                    return raw_text.strip().split("\n")
                else:
                    return {"error": f"API error: {response.status}"}
    except Exception as e:
        print(f"CC API Error: {e}")
        return {"error": str(e)}

def format_bin_response(bin_number, bin_info):
    if isinstance(bin_info, dict) and "error" in bin_info:
        return f"❌ ERROR: {bin_info['error']}"

    formatted_text = "⚡️━━━━━ Valid BIN ☂️ ━━━━━⚡️\n\n"
    formatted_text += f"⚡️ BIN ➜ <code>{bin_number[:6]}</code>\n"
    formatted_text += f"⚡️ VBV Status ➜ ✅ Non(Auto)-Vbv ✅\n"
    formatted_text += f"⚡️ Bank ➜ {bin_info.get('bank', 'NOT FOUND')}\n"
    formatted_text += f"🌍 Country ➜ {bin_info.get('flag', '🏳️')} {bin_info.get('country', 'NOT FOUND')}\n"
    formatted_text += f"💳 Info ➜ {bin_info.get('network', 'NOT FOUND')} {bin_info.get('card_type', 'NOT FOUND')} ({bin_info.get('tier', 'NOT FOUND')})\n"
    formatted_text += "\n🔥══════ Elite Divider ══════🔥\n"
    formatted_text += "⚡️ Sigma BIN Checker Elite ⚡️\n"
    formatted_text += "💸 Powered by Sigma Elite 🔥\n"
    formatted_text += "💲 Chat: @ExoNexxusTG\n"
    formatted_text += "💲 Owner: @ExoNexxusTG"
    return formatted_text

def format_cc_response(data, bin_number, bin_info):
    if isinstance(data, dict) and "error" in data:
        return f"❌ ERROR: {data['error']}"
    if not data:
        return "❌ NO CARDS GENERATED."

    formatted_text = "⚡️━━━━━ Valid BIN ☂️ ━━━━━⚡️\n\n"
    formatted_text += f"⚡️ BIN ➜ <code>{bin_number[:6]}</code>\n"
    formatted_text += f"⚡️ VBV Status ➜ ✅ Non(Auto)-Vbv ✅\n"
    formatted_text += f"⚡️ Bank ➜ {bin_info.get('bank', 'NOT FOUND')}\n"
    formatted_text += f"🌍 Country ➜ {bin_info.get('flag', '🏳️')} {bin_info.get('country', 'NOT FOUND')}\n"
    formatted_text += f"💳 Info ➜ {bin_info.get('network', 'NOT FOUND')} {bin_info.get('card_type', 'NOT FOUND')} ({bin_info.get('tier', 'NOT FOUND')})\n"
    formatted_text += "\n🔥══════ Elite Divider ══════🔥\n"
    formatted_text += f"💲 Generated Cards ({len(data)}):\n\n"
    for card in data:
        formatted_text += f"<code>{card.upper()}</code>\n"
    formatted_text += "\n🔥══════ Elite Divider ══════🔥\n"
    formatted_text += "⚡️ Sigma BIN Checker Elite ⚡️\n"
    formatted_text += "💸 Powered by Sigma Elite 🔥\n"
    formatted_text += "💲 Chat: @ExoNexxusTG\n"
    formatted_text += "💲 Owner: @ExoNexxusTG"
    return formatted_text

async def gather_bin_data(bin_number):
   (Auto)-Vbv ✅
    bin_info = await lookup_bin(bin_number)
    return format_bin_response(bin_number, bin_info)

async def gather_cc_data(bin_number):
    cc_data = await generate_cc_async(bin_number)
    bin_info = await lookup_bin(bin_number)
    return format_cc_response(cc_data, bin_number, bin_info)

def process_bin(bin_number):
    try:
        return asyncio.run(gather_bin_data(bin_number))
    except Exception as e:
        print(f"Process BIN Error: {e}")
        return f"❌ ERROR PROCESSING REQUEST: {e}"

def generate_cc(bin_number):
    try:
        return asyncio.run(gather_cc_data(bin_number))
    except Exception as e:
        print(f"Generate CC Error: {e}")
        return f"❌ ERROR PROCESSING REQUEST: {e}"

@bot.message_handler(func=lambda message: message.text.startswith(("/gen", ".gen")))
def gen_command(message):
    try:
        command_parts = message.text.split(' ', 1)
        print(f"Received GEN command: {message.text}")
        if len(command_parts) < 2:
            bot.send_message(message.chat.id, "❌ PLEASE PROVIDE A BIN.", parse_mode="Markdown")
            return

        bin_number = extract_bin(command_parts[1])
        print(f"Extracted BIN for GEN: {bin_number}")
        if not bin_number:
            bot.send_message(message.chat.id, "❌ INVALID BIN FORMAT.", parse_mode="Markdown")
            return

        result = generate_cc(bin_number)
        bot.send_message(message.chat.id, result, parse_mode="HTML")

    except Exception as e:
        print(f"Gen Command Error: {e}")
        bot.send_message(message.chat.id, f"❌ ERROR: {e}")

@bot.message_handler(func=lambda message: message.text.startswith(("/bin", ".bin")))
def bin_command(message):
    try:
        command_parts = message.text.split(' ', 1)
        print(f"Received BIN command: {message.text}")
        if len(command_parts) < 2:
            bot.send_message(message.chat.id, "❌ PLEASE PROVIDE A BIN.", parse_mode="Markdown")
            return

        bin_number = extract_bin(command_parts[1])
        print(f"Extracted BIN: {bin_number}")
        if not bin_number:
            bot.send_message(message.chat.id, "❌ INVALID BIN FORMAT.", parse_mode="Markdown")
            return

        result = process_bin(bin_number)
        bot.send_message(message.chat.id, result, parse_mode="HTML")

    except Exception as e:
        print(f"Bin Command Error: {e}")
        bot.send_message(message.chat.id, f"❌ ERROR: {e}")

def main():
    print("BOT IS RUNNING...")
    while True:
        try:
            bot.infinity_polling(timeout=60, long_polling_timeout=60)
        except Exception as e:
            print(f"BOT POLLING ERROR: {e}")
            time.sleep(5)

if __name__ == "__main__":
    main()