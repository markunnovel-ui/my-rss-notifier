import requests
from bs4 import BeautifulSoup
from feedgen.feed import FeedGenerator

# 設定
WORK_URL = "https://kakuyomu.jp/works/2912051601556641467"
RSS_FILE = "rss.xml"

def fetch_kakuyomu():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
    }
    response = requests.get(WORK_URL, headers=headers)
    response.raise_for_status() 
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # ページタイトル（作品名）を取得
    # カクヨムのタイトルは <h1 id="workTitle"> 内にあります
    work_title_el = soup.find('h1', id='workTitle')
    # 最新エピソードのリストを取得
    episode_list = soup.find('div', class_='widget-episodeList')
    latest_episode = episode_list.find('li', class_='widget-episodeList-episode')
    
    if not work_title_el or not latest_episode:
        raise Exception("カクヨムのHTML構造を特定できませんでした。URLを確認してください。")

    work_title = work_title_el.text.strip()
    
    # エピソードタイトルと日付
    episode_title = latest_episode.find('a').text.strip()
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
