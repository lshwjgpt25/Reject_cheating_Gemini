import configparser
import datetime
from telegram import Update, ChatPermissions
from telegram.ext import CallbackContext
from . import data_manager
from . import gemini_analyzer
from .logger_config import logger

async def help_command(update: Update, context: CallbackContext) -> None:
    """Displays a help message with all available commands."""
    help_text = """
    <b>反外挂机器人命令帮助</b>

    /help - 显示此帮助信息。

    <b>管理员命令:</b>
    /approvegroup &lt;group_id&gt; - 批准一个群组，在该群组中启用机器人功能。
    /addadmin &lt;user_id&gt; - 添加一个新的机器人管理员。
    /addsuperadmin &lt;user_id&gt; - 添加一个新的超级管理员 (仅限config.ini中配置的超级管理员)。
    /setlogchannel &lt;channel_username&gt; - 为当前群组设置一个日志频道，用于接收踢人通知。
    /setwarninglimit &lt;count&gt; - 设置警告次数，达到次数后自动封禁。设置为0则禁用警告功能。

    <i>注意: 机器人会自动分析发送消息少于200条成员的发言，并根据AI判断结果自动移除疑似外挂/作弊者。</i>
    """
    await update.message.reply_text(help_text, parse_mode='HTML')


async def start(update: Update, context: CallbackContext) -> None:
    """处理 /start 命令"""
    user = update.effective_user
    chat = update.effective_chat

    if chat.type != 'private':
        config = configparser.ConfigParser()
        config.read('config.ini')
        super_admin_id = config['telegram']['super_admin_id']
        
        # Add logging here
        approved_groups = data_manager.load_approved_groups()
        logger.info(f"Start command received in group: {chat.id}")
        logger.info(f"Approved groups: {approved_groups}")

        if chat.id not in approved_groups: # Check if the group is approved
            await context.bot.send_message(
                chat_id=super_admin_id,
                text=f"机器人已在新的群组中启动.\n"
                     f"群组名称: {chat.title}\n"
                     f"群组 ID: {chat.id}\n"
                     f"请使用 /approvegroup {chat.id} 命令来批准此群组。"
            )
            await update.message.reply_text("此群组需要管理员批准才能启用反外挂功能。")
        else:
            await update.message.reply_text("此群组已批准，反外挂功能已启用。") # New message for approved groups

async def approve_group(update: Update, context: CallbackContext) -> None:
    """处理 /approvegroup 命令"""
    user_id = update.effective_user.id
    admins = data_manager.load_admins()
    
    config = configparser.ConfigParser()
    config.read('config.ini')
    super_admin_id = config['telegram']['super_admin_id']
    super_admins = data_manager.load_super_admins()

    if user_id != int(super_admin_id) and user_id not in admins and user_id not in super_admins:
        await update.message.reply_text("只有机器人管理员或超级管理员才能使用此命令。")
        return

    try:
        group_id = int(context.args[0])
        approved_groups = data_manager.load_approved_groups()
        if group_id not in approved_groups:
            approved_groups.append(group_id)
            data_manager.save_approved_groups(approved_groups)
            await update.message.reply_text(f"群组 {group_id} 已被批准。")
        else:
            await update.message.reply_text(f"群组 {group_id} 已在批准列表中。")
    except (IndexError, ValueError):
        await update.message.reply_text("用法: /approvegroup <group_id>")

async def add_admin(update: Update, context: CallbackContext) -> None:
    """处理 /addadmin 命令"""
    user_id = update.effective_user.id
    admins = data_manager.load_admins()

    config = configparser.ConfigParser()
    config.read('config.ini')
    super_admin_id = config['telegram']['super_admin_id']
    super_admins = data_manager.load_super_admins()

    if user_id != int(super_admin_id) and user_id not in super_admins:
        await update.message.reply_text("只有超级管理员才能使用此命令。")
        return

    try:
        new_admin_id = int(context.args[0])
        if new_admin_id not in admins:
            admins.append(new_admin_id)
            data_manager.save_admins(admins)
            await update.message.reply_text(f"用户 {new_admin_id} 已被添加为管理员。")
        else:
            await update.message.reply_text(f"用户 {new_admin_id} 已经是管理员。")
    except (IndexError, ValueError):
        await update.message.reply_text("用法: /addadmin <user_id>")

async def add_super_admin(update: Update, context: CallbackContext) -> None:
    """处理 /addsuperadmin 命令，只有config.ini中的super_admin可以添加其他super_admin"""
    user_id = update.effective_user.id

    config = configparser.ConfigParser()
    config.read('config.ini')
    super_admin_id_from_config = int(config['telegram']['super_admin_id'])

    if user_id != super_admin_id_from_config:
        await update.message.reply_text("只有在config.ini中配置的超级管理员才能使用此命令。")
        return

    try:
        new_super_admin_id = int(context.args[0])
        super_admins = data_manager.load_super_admins()
        if new_super_admin_id not in super_admins:
            super_admins.append(new_super_admin_id)
            data_manager.save_super_admins(super_admins)
            await update.message.reply_text(f"用户 {new_super_admin_id} 已被添加为超级管理员。")
        else:
            await update.message.reply_text(f"用户 {new_super_admin_id} 已经是超级管理员。")
    except (IndexError, ValueError):
        await update.message.reply_text("用法: /addsuperadmin <user_id>")

async def set_log_channel(update: Update, context: CallbackContext) -> None:
    """设置日志频道"""
    user_id = update.effective_user.id
    chat_id = update.message.chat_id
    admins = data_manager.load_admins()

    config = configparser.ConfigParser()
    config.read('config.ini')
    super_admin_id = config['telegram']['super_admin_id']
    super_admins = data_manager.load_super_admins()

    if user_id != int(super_admin_id) and user_id not in admins and user_id not in super_admins:
        await update.message.reply_text("只有机器人管理员或超级管理员才能使用此命令。")
        return

    try:
        channel_username = context.args[0]
        # Get chat ID from username
        chat_info = await context.bot.get_chat(channel_username)
        channel_id = chat_info.id

        group_channel_map = data_manager.load_group_channel_map()
        group_channel_map[str(chat_id)] = channel_id
        data_manager.save_group_channel_map(group_channel_map)
        await update.message.reply_text(f"群组 {chat_id} 的日志频道已设置为 {channel_username} (ID: {channel_id})。")
    except (IndexError, ValueError):
        await update.message.reply_text("用法: /setlogchannel <channel_username>")
    except Exception as e:
        await update.message.reply_text(f"设置日志频道失败: {e}\n请确保机器人是该频道的管理员，并且用户名正确。")

async def set_warning_limit(update: Update, context: CallbackContext) -> None:
    """设置警告次数限制"""
    user_id = update.effective_user.id
    admins = data_manager.load_admins()

    config = configparser.ConfigParser()
    config.read('config.ini')
    super_admin_id = config['telegram']['super_admin_id']
    super_admins = data_manager.load_super_admins()

    if user_id != int(super_admin_id) and user_id not in admins and user_id not in super_admins:
        await update.message.reply_text("只有机器人管理员或超级管理员才能使用此命令。")
        return

    try:
        limit = int(context.args[0])
        if limit < 0:
            await update.message.reply_text("警告次数不能为负数。")
            return
        
        warning_settings = data_manager.load_warning_settings()
        warning_settings['warning_limit'] = limit
        warning_settings['enabled'] = (limit > 0)
        data_manager.save_warning_settings(warning_settings)
        
        if limit == 0:
            await update.message.reply_text("警告功能已禁用。")
        else:
            await update.message.reply_text(f"警告次数已设置为 {limit} 次。")
            
    except (IndexError, ValueError):
        await update.message.reply_text("用法: /setwarninglimit <count>")



async def message_handler(update: Update, context: CallbackContext) -> None:
    """处理文本消息"""
    chat_id = update.message.chat_id
    user_id = update.message.from_user.id
    message_text = update.message.text

    approved_groups = data_manager.load_approved_groups()
    if chat_id not in approved_groups:
        return

    user_message_counts = data_manager.load_user_message_counts()
    group_id = str(chat_id)
    user_id_str = str(user_id)

    if group_id not in user_message_counts:
        user_message_counts[group_id] = {}
    if user_id_str not in user_message_counts[group_id]:
        user_message_counts[group_id][user_id_str] = 0
    
    user_message_counts[group_id][user_id_str] += 1
    data_manager.save_user_message_counts(user_message_counts)

    if user_message_counts[group_id][user_id_str] < 200:
            analysis_result = gemini_analyzer.analyze_message(message_text)
            if analysis_result.get("is_cheater"):
                reason = analysis_result.get("reason", "无具体原因")
                
                warning_settings = data_manager.load_warning_settings()
                user_warnings = data_manager.load_user_warnings()
                
                user_id_str = str(user_id)
                current_warnings = user_warnings.get(user_id_str, 0)

                if warning_settings['enabled'] and current_warnings < warning_settings['warning_limit']:
                    # Issue a warning
                    user_warnings[user_id_str] = current_warnings + 1
                    data_manager.save_user_warnings(user_warnings)
                    
                    warning_message = f"用户 {user_id}，您因涉嫌作弊/外挂收到警告。原因: {reason}。这您的第 {user_warnings[user_id_str]} 次警告。达到 {warning_settings['warning_limit']} 次警告将被禁言。"
                    await update.message.reply_text(warning_message)
                    logger.info(f"用户 {user_id} 在群组 {chat_id} 中收到警告。原因: {reason} (第 {user_warnings[user_id_str]} 次警告)")
                    
                    log_message = f"用户 {user_id} 在群组 {chat_id} 中收到警告。原因: {reason} (第 {user_warnings[user_id_str]} 次警告)"
                    group_channel_map = data_manager.load_group_channel_map()
                    if str(chat_id) in group_channel_map:
                        channel_id = group_channel_map[str(chat_id)]
                        await context.bot.send_message(chat_id=channel_id, text=log_message)

                else:
                    # Mute user if warnings are disabled or limit is reached
                    log_message = f"用户 {user_id} 在群组 {chat_id} 中因涉嫌作弊/外挂已被禁言30天。原因: {reason}"
                    logger.info(log_message)
                    try:
                        until_date = datetime.datetime.now() + datetime.timedelta(days=30)
                        await context.bot.restrict_chat_member(
                            chat_id,
                            user_id,
                            permissions=ChatPermissions(can_send_messages=False),
                            until_date=until_date
                        )
                        await update.message.reply_text(f"""用户 {user_id} 因涉嫌作弊/外挂已被禁言30天。
原因: {reason}""")
                        
                        # Reset warnings after mute
                        if user_id_str in user_warnings:
                            del user_warnings[user_id_str]
                            data_manager.save_user_warnings(user_warnings)

                        group_channel_map = data_manager.load_group_channel_map()
                        if str(chat_id) in group_channel_map:
                            channel_id = group_channel_map[str(chat_id)]
                            await context.bot.send_message(chat_id=channel_id, text=log_message)

                    except Exception as e:
                        logger.error(f"无法踢出用户 {user_id} 或转发日志: {e}")
