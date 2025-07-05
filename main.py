import configparser
import sys
import os
from telegram.ext import Application, CommandHandler, MessageHandler, filters

# 将src目录添加到Python路径中
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src import bot_logic

def main() -> None:
    """启动机器人"""
    config = configparser.ConfigParser()
    config.read('config.ini')
    token = config['telegram']['bot_token']

    # 使用 Application.builder() 创建机器人
    application = Application.builder().token(token).build()

    # 注册命令处理器
    application.add_handler(CommandHandler("start", bot_logic.start))
    application.add_handler(CommandHandler("help", bot_logic.help_command))
    application.add_handler(CommandHandler("approvegroup", bot_logic.approve_group))
    application.add_handler(CommandHandler("addadmin", bot_logic.add_admin))
    application.add_handler(CommandHandler("setlogchannel", bot_logic.set_log_channel))

    # 注册消息处理器
    
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, bot_logic.message_handler))

    # 启动机器人
    application.run_polling()

if __name__ == '__main__':
    main()
