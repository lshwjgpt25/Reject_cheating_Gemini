import json
import os
from typing import List, Dict, Any

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')
ADMINS_FILE = os.path.join(DATA_DIR, 'admins.json')
GROUPS_FILE = os.path.join(DATA_DIR, 'approved_groups.json')
MESSAGE_COUNTS_FILE = os.path.join(DATA_DIR, 'user_message_counts.json')
CHANNEL_MAP_FILE = os.path.join(DATA_DIR, 'group_channel_map.json')
SUPER_ADMINS_FILE = os.path.join(DATA_DIR, 'super_admins.json')
WARNING_SETTINGS_FILE = os.path.join(DATA_DIR, 'warning_settings.json')
USER_WARNINGS_FILE = os.path.join(DATA_DIR, 'user_warnings.json')
def load_admins() -> List[int]:
    """加载管理员ID列表"""
    if not os.path.exists(ADMINS_FILE):
        return []
    with open(ADMINS_FILE, 'r') as f:
        return json.load(f)

def save_admins(admins: List[int]) -> None:
    """保存管理员ID列表"""
    with open(ADMINS_FILE, 'w') as f:
        json.dump(admins, f, indent=4)

def load_approved_groups() -> List[int]:
    """加载已批准的群组ID列表"""
    if not os.path.exists(GROUPS_FILE):
        return []
    with open(GROUPS_FILE, 'r') as f:
        return json.load(f)

def save_approved_groups(groups: List[int]) -> None:
    """保存已批准的群组ID列表"""
    with open(GROUPS_FILE, 'w') as f:
        json.dump(groups, f, indent=4)

def load_user_message_counts() -> Dict[str, Any]:
    """加载用户消息计数"""
    if not os.path.exists(MESSAGE_COUNTS_FILE):
        return {}
    with open(MESSAGE_COUNTS_FILE, 'r') as f:
        return json.load(f)

def save_user_message_counts(message_counts: Dict[str, Any]) -> None:
    """保存用户消息计数"""
    with open(MESSAGE_COUNTS_FILE, 'w') as f:
        json.dump(message_counts, f, indent=4)

def load_group_channel_map() -> Dict[str, int]:
    """加载群组到频道的映射"""
    if not os.path.exists(CHANNEL_MAP_FILE):
        return {}
    with open(CHANNEL_MAP_FILE, 'r') as f:
        return json.load(f)

def save_group_channel_map(mapping: Dict[str, int]) -> None:
    """保存群组到频道的映射"""
    with open(CHANNEL_MAP_FILE, 'w') as f:
        json.dump(mapping, f, indent=4)

def load_super_admins() -> List[int]:
    """加载超级管理员ID列表"""
    if not os.path.exists(SUPER_ADMINS_FILE):
        return []
    with open(SUPER_ADMINS_FILE, 'r') as f:
        return json.load(f)

def save_super_admins(super_admins: List[int]) -> None:
    """保存超级管理员ID列表"""
    with open(SUPER_ADMINS_FILE, 'w') as f:
        json.dump(super_admins, f, indent=4)

def load_warning_settings() -> Dict[str, Any]:
    """加载警告设置"""
    if not os.path.exists(WARNING_SETTINGS_FILE):
        return {'enabled': False, 'warning_limit': 0}
    with open(WARNING_SETTINGS_FILE, 'r') as f:
        return json.load(f)

def save_warning_settings(settings: Dict[str, Any]) -> None:
    """保存警告设置"""
    with open(WARNING_SETTINGS_FILE, 'w') as f:
        json.dump(settings, f, indent=4)

def load_user_warnings() -> Dict[str, int]:
    """加载用户警告次数"""
    if not os.path.exists(USER_WARNINGS_FILE):
        return {}
    with open(USER_WARNINGS_FILE, 'r') as f:
        return json.load(f)

def save_user_warnings(user_warnings: Dict[str, int]) -> None:
    """保存用户警告次数"""
    with open(USER_WARNINGS_FILE, 'w') as f:
        json.dump(user_warnings, f, indent=4)
