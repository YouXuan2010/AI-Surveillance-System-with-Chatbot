from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from dotenv import load_dotenv
from datetime import datetime
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CallbackQueryHandler
import aiss
import os
import glob
import cv2
import asyncio

# Load environment variables from .env file
load_dotenv()
token = os.getenv('TELEGRAM_BOT_TOKEN')

message_text = ""
video_path = ""

def print_message(update: Update, action: str):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    first_name = update.message.from_user.first_name
    last_name = update.message.from_user.last_name

    message = f"[{timestamp}] Action '{action}' triggered in chat ID {update.effective_chat.id}"

    if first_name and last_name:
        message += f" by {first_name} {last_name}"
    elif first_name:
        message += f" by {first_name}"
    elif last_name:
        message += f" by {last_name}"

    print(message)

def get_latest_video_file(directory):
    video_files = glob.glob(os.path.join(directory, '*.mp4'))
    if not video_files:
        return None
    latest_video_file = max(video_files, key=os.path.getmtime)
    return latest_video_file

def check_camera_status(stream_url):
    cap = cv2.VideoCapture(stream_url)

    if not cap.isOpened():
        return False
    else:
        cap.release()
        return True

# Define a callback function to handle inline keyboard button presses
async def button_callback(update, context):
    query = update.callback_query
    user_response = query.data

    # Check the callback data to determine the user's choice
    if user_response == 'yes':
        # Read the security log from the file
        with open('Security_Logs.txt', 'r') as file:
            security_log = file.read()

        # Send the security log to the user
        await query.answer()
        await query.message.reply_text(text=security_log)
    elif user_response == 'no':
        await query.answer()
        await query.message.reply_text(text="Okay, no problem!")

    # Edit the message to remove the inline keyboard
    await query.message.edit_reply_markup(reply_markup=None)

async def send_message(update, context, timeout=15):
    print_message(update, 'sending_message_to_user')
    
    # Create Bot instance
    bot = context.bot

    # Specify the directory to search for video files
    current_dir = os.path.dirname(os.path.abspath(__file__))
    video_directory = os.path.join(current_dir, "video")

    # Get the latest video file path
    video_file_path = get_latest_video_file(video_directory)

    if video_file_path is None:
        print("No video files found in the directory")
        return
    
    # Send message
    response = await bot.send_message(chat_id=update.effective_chat.id, text="Person Detected in Frame! Sending Video...")

    try:
        # Attempt to send the video within the specified timeout
        # Send video
        with open(video_file_path, 'rb') as video_file:
            await asyncio.wait_for(bot.send_video(chat_id=update.effective_chat.id, video=video_file, width= 1270, height=720), timeout=timeout)
        
        # Define the inline keyboard markup for asking the user
        keyboard = [
            [InlineKeyboardButton("Yes", callback_data='yes'), InlineKeyboardButton("No", callback_data='no')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        # Ask the user if they want to view the current security log
        await bot.send_message(chat_id=update.effective_chat.id, 
                               text="Do you want to view the current security log?", 
                               reply_markup=reply_markup)

    except asyncio.TimeoutError:
        # Handle timeout error
        print("Sending video timed out")
    
async def start_server(update: Update, context):
    global message_text, video_path

    print_message(update, 'start_server')
    
    message = 'Starting the AI security server...'
    await context.bot.send_message(chat_id=update.effective_chat.id, text=message)
    
    # Stsrting the AI security server
    if aiss.main():
        await send_message(update, context)
    else:
        message = 'Failed to start the AI security server, please check the camera and LM Studio server status.'
        await context.bot.send_message(chat_id=update.effective_chat.id, text=message)

        
async def start(update: Update, context):
    print_message(update, 'start')
    response = await context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text='Hello and welcome to your personal AI Surveillance System! Use /help to see the list of supported commands.'
    )

async def help(update: Update, context):
    print_message(update, 'help')
    response = await context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text="""
        The BuiltIn Telegram bot supports the following commands:
- /help: List of supported commands (you are here)
- /first_name: Reports the user's first name
- /last_name: Reports the user's last name
- /start_server: Start the AI security server
- /check_job_status: Checks your job status
- /live: View the live camera feed
        """
    )

async def first_name(update: Update, context):
    print_message(update, 'first_name')
    response = await context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text=f'Your first name is {update.message.from_user.first_name}'
    )
    
async def last_name(update: Update, context):
    print_message(update, 'last_name')
    response = await context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text=f'Your last name is {update.message.from_user.last_name}'
    )
    
async def check_job_status(update: Update, context):
    print_message(update, 'check_job_status')
    message = "You are jobless. Try harder NOOB!"
    await context.bot.send_message(chat_id=update.effective_chat.id, text=message)
    
    # Send sticker image
    photo_path = "Asset/prank.png"
    with open(photo_path, 'rb') as photo:
        await context.bot.send_photo(chat_id=update.effective_chat.id, photo=photo)

async def live(update, context):
    print_message(update, 'live')
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Connecting to the live camera feed...")

    live_stream_url = "http://192.168.0.103:8080/video"

    camera_status = check_camera_status(live_stream_url)
    if camera_status:
        message = "Camera is live. Here is the live feed:\n" + live_stream_url
    else:
        message = "Error: Camera is not working. Please check the camera connection."
    await context.bot.send_message(chat_id=update.effective_chat.id, text=message)


if __name__ == '__main__':
    application = Application.builder().token(token).build()

    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)

    help_handler = CommandHandler('help', help)
    application.add_handler(help_handler)

    first_name_handler = CommandHandler('first_name', first_name)
    application.add_handler(first_name_handler)

    last_name_handler = CommandHandler('last_name', last_name)
    application.add_handler(last_name_handler)

    start_server_handler = CommandHandler('start_server', start_server)
    application.add_handler(start_server_handler)

    check_job_status_handler = CommandHandler('check_job_status', check_job_status)
    application.add_handler(check_job_status_handler)

    live_handler = CommandHandler('live', live)
    application.add_handler(live_handler)

    application.add_handler(CallbackQueryHandler(button_callback))

    application.run_polling()