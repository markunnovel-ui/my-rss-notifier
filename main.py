import requests
from bs4 import BeautifulSoup
from feedgen.feed import FeedGenerator
import datetime

# 設定
WORK_URL = "https://kakuyomu.jp/works/2912051601556641467"
RSS_FILE = "rss.xml"

def fetch_kakuyomu():
    response = requests.get(WORK_URL)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # 作品タイトル取得
    work_title = soup.find('h1', class_='WorkTitle').text.strip()
    
    # 最新話取得
    latest_episode = soup.find('li', class_='EpisodeList-item').find('a')
    episode_title = latest_episode.find('span', class_='EpisodeList-episodeTitle').text.strip()
    episode_date = latest_episode.find('time').get('datetime')
    
    return work_title, episode_title, episode_date

def generate_rss(work_title, episode_title, episode_date):
    fg = FeedGenerator()
    fg.title(work_title)
    fg.link(href=WORK_URL)
    fg.description(f"最新話: {episode_title}")
    
    fe = fg.add_entry()
    fe.title(episode_title)
    fe.updated(episode_date)
    fe.description(f"更新日時: {episode_date}")
    
    fg.rss_file(RSS_FILE)

if __name__ == "__main__":
    t, e, d = fetch_kakuyomu()
    generate_rss(t, e, d)
