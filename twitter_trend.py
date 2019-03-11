import os
from datetime import datetime, timezone, timedelta
import tweepy
from dotenv import load_dotenv, find_dotenv

env_path = os.path.join(os.path.dirname(__file__), ".env")
if find_dotenv(env_path):
    load_dotenv(dotenv_path=env_path)

CONSUMER_KEY = os.getenv("CONSUMER_KEY")
CONSUMER_SECRET = os.getenv("CONSUMER_SECRET")

if not all([CONSUMER_KEY, CONSUMER_SECRET]):
    raise NameError("API key is not provided")

auth = tweepy.AppAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True)

WOEID_JAPAN = 23424856
JST_TZ = timezone(timedelta(hours=9), name="JST")


def get_trend_data():
    trends_japan = api.trends_place(id=WOEID_JAPAN)[0]

    date_iso = trends_japan["as_of"]
    date_jst_str = convert_iso_datetime_to_jst(date_iso)

    trend_topics = (topic["name"] for topic in trends_japan["trends"])
    trend_ranking = []
    for i, j in enumerate(trend_topics):
        trend_ranking.append({"number": i + 1, "topic_name": j})
        # 50件までしかトレンドを取得できないはずだが、仕様変更に備えて
        # 明確に上限を50件に設定する
        if i > 50:
            break

    trend = {
        "date": date_jst_str,
        "location": "日本",
        "rank": trend_ranking
    }
    return trend


def convert_iso_datetime_to_jst(date_iso, output_format="%Y/%m/%d %H:%M"):
    """ISO8601形式の日付の文字列を日本時間の日付の文字列に変換"""
    date_iso = date_iso.replace("Z", "+00:00")
    date = datetime.fromisoformat(date_iso)
    date_jst = date.astimezone(JST_TZ)
    date_jst_str = date_jst.strftime(output_format)
    return date_jst_str


if __name__ == "__main__":
    trend = get_trend_data()
    print(trend)
