import google.generativeai as genai
import configparser
import json
from .logger_config import logger

def analyze_message(message: str) -> dict:
    """
    使用Gemini分析消息，判断是否为外掛玩家.

    Args:
        message: 要分析的讯息.

    Returns:
        包含分析结果的字典.
    """
    config = configparser.ConfigParser()
    config_path = 'config.ini'
    config.read(config_path)
    api_key = config['gemini']['api_key']

    genai.configure(api_key=api_key)
    model_name = 'gemini-2.5-flash'
    model = genai.GenerativeModel(model_name)

    prompt = f"""
    你是一个Telegram群组的管理员，你的任务是判断一个新成员的发言是否像是游戏外挂/作弊的广告或相关讨论。不要轻易下定论，比如你开挂吗这一类调侃，否认性的问答，你不用认为是外挂，并且请你结合上下文分析该用户是不是外挂玩家，有确切的证据可以证明。
    请分析以下消息，并以JSON格式返回你的判断。
    JSON格式必须包含两个字段：
    1. "is_cheater": 布尔值，如果认为是外挂/作弊相关，则为true，否则为false。
    2. "reason": 字符串，简要说明你判断的理由。

    消息内容: "{message}"
    """

    logger.info(f"向 Gemini API ({model_name}) 发送请求。提示: {prompt}")

    try:
        response = model.generate_content(prompt)
        logger.info(f"收到 Gemini API 的响应: {response.text}")
        cleaned_response = response.text.strip().replace("```json", "").replace("```", "")
        return json.loads(cleaned_response)
    except Exception as e:
        logger.error(f"调用 Gemini API 或解析 JSON 时出错: {e}")
        return {"is_cheater": False, "reason": "调用API或解析响应时发生错误。"}
