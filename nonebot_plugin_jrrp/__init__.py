from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent, GROUP, Message, MessageSegment
from nonebot.plugin import on_command
from nonebot.params import CommandArg
from typing import List
import time

jrrp = on_command("jrrp", aliases = {"j"}, permission=GROUP, priority=50)
message: List[dict] = [
	{
		"expr": "jrrp == 100",
		"start": "！！！！！你今天的人品值是：",
		"end": "！100！100！！！！！"
	},
	{
		"expr": "jrrp == 99",
		"end": "！但不是 100……"
	},
	{
		"expr": "jrrp >= 90",
		"end": "！好评如潮！"
	},
	{
		"expr": "jrrp >= 60",
		"end": "！是不错的一天呢！"
	},
	{
		"expr": "jrrp > 50",
		"end": "！还行啦还行啦。"
	},
	{
		"expr": "jrrp == 50",
		"end": "！五五开……"
	},
	{
		"expr": "jrrp >= 40",
		"end": "！还……还行吧……？"
	},
	{
		"expr": "jrrp >= 11",
		"end": "！呜哇……"
	},
	{
		"expr": "jrrp >= 1",
		"end": "……（没错，是百分制）"
	},
	{
		"expr": "True",
		"end": "……"
	}
]
@jrrp.handle()
async def _h(bot: Bot, event: GroupMessageEvent, args: Message = CommandArg()):
    words = args.extract_plain_text()
    if not words:
        session = event.get_session_id()
        id = session.split('_')[2]
    if words:
        id = words
    jrrp_num = get_jrrp(str(id))
    result = get_msg(jrrp_num)
    reply = MessageSegment.reply(event.message_id)
    await jrrp.send(reply + result)

def rol(num: int, k: int, bits: int = 64):
    b1 = bin(num << k)[2:]
    if len(b1) <= bits:
        return int(b1, 2)
    return int(b1[-bits:], 2)

def get_hash(string: str):
    num = 5381
    num2 = len(string) - 1
    for i in range(num2 + 1):
        num = rol(num, 5) ^ num ^ ord(string[i])
    return num ^ 12218072394304324399

def get_jrrp(string: str):
    now = time.localtime()
    num = round(abs((get_hash("".join([
        "asdfgbn",
        str(now.tm_yday),
        "12#3$45",
        str(now.tm_year),
        "IUY"
    ])) / 3 + get_hash("".join([
        "QWERTY",
        string,
        "0*8&6",
        str(now.tm_mday),
        "kjhg"
    ])) / 3) / 527) % 1001)
    if num >= 970:
        num2 = 100
    else:
        num2 = round(num / 969 * 99)
    return num2

def get_msg(jrrp):
    start: str = "你今天的人品值是："
    end: str = "……"
    for msg_obj in message:
        if eval(msg_obj["expr"]):
            start = msg_obj.get("start") if msg_obj.get("start") else start
            end = msg_obj.get("end") if msg_obj.get("end") else end
            lumsg = start + str(jrrp) + end
            return lumsg
