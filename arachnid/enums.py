from enum import Enum, auto


class Delay(Enum):
    NONE = tuple(x for x in range(0,1))
    LOW = tuple(x for x in range(1,6))
    MEDIUM = tuple(x for x in range(4,11))
    HIGH = tuple(x for x in range(1,21))


class Amount(Enum):
    NONE = auto()
    LOW = auto()
    MEDIUM = auto()
    HIGH = auto()


class Agent(Enum):
    GOOGLE = "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"
    BING = "Mozilla/5.0 (compatible; Bingbot/2.0; +http://www.bing.com/bingbot.htm)"
    YAHOO = "Mozilla/5.0 (compatible; Yahoo! Slurp; http://help.yahoo.com/help/us/ysearch/slurp)"
    DUCKDUCKGO = "DuckDuckBot/1.0; (+http://duckduckgo.com/duckduckbot.html)"
    BAIDU = "Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)"
    YANDEX = "Mozilla/5.0 (compatible; YandexBot/3.0; +http://yandex.com/bots)"
    FIREFOX = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:10.0) Gecko/20100101 Firefox/10.0"
    ANDROID = "Mozilla/5.0 (Linux; U; Android 4.4.2; en-us; SCH-I535 Build/KOT49H) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30"

