import requests
from bs4 import BeautifulSoup
from feedgen.feed import FeedGenerator

WORK_URL = "https://kakuyomu.jp/works/2912051601556641467"
RSS_FILE = "rss.xml"

def fetch_kakuyomu():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
    }
    response = requests.get(WORK_URL, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # 1. 作品タイトル：h1タグから取得
    work_title = soup.find('h1').text.strip()
    
    # 2. 最新エピソード：エピソードリストの最後を取得
    # カクヨムのエピソードリストは <li class="widget-episodeList-episode"> 
    episodes = soup.find_all('li', class_='widget-episodeList-episode')
    latest_episode = episodes[-1] # 一番最後（最新）
    
    episode_title = latest_episode.find('a').text.strip()
    # 日付は time タグの datetime 属性にある
    episode_date = latest_episode.find('time')['datetime']
    
    return work_title, episode_title, episode_date

def generate_rss(work_title, episode_title, episode_date):
    fg = FeedGenerator()
    fg.title(work_title)
    fg.link(href=WORK_URL)
    fg.description("カクヨム更新通知")
    
    fe = fg.add_entry()
    fe.title(episode_title)
    fe.updated(episode_date)
    fe.link(href=WORK_URL) # 簡易的に作品URLをリンクにする
    fe.description(f"更新日: {episode_date}")
    
    fg.rss_file(RSS_FILE)

if __name__ == "__main__":
    t, e, d = fetch_kakuyomu()
    generate_rss(t, e, d)
