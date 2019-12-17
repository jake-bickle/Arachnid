import os
import json
from enum import Enum, auto

this_dir = os.path.dirname(os.path.abspath(__file__))
useragents_file = os.path.normpath(f"{this_dir}/../data/useragents.json")
with open(useragents_file) as f:
    useragents = json.load(f)


class Agent(Enum):
    GOOGLE = useragents["googlebot"]["value"]
    BING = useragents["bingbot"]["value"]
    YAHOO = useragents["yahoobot"]["value"]
    DUCKDUCKGO = useragents["duckduckgobot"]["value"]
    BAIDU = useragents["baidubot"]["value"]
    YANDEX = useragents["yandexbot"]["value"]
    FIREFOX = useragents["firefox"]["value"]
    ANDROID = useragents["android"]["value"]


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
