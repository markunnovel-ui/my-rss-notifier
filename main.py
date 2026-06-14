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
    
    # 1. 作品タイトルを検索（id="workTitle" が確実）
    work_title_el = soup.find('h1', id='workTitle')
    if not work_title_el:
        raise Exception("作品タイトルが見つかりません")
    work_title = work_title_el.text.strip()
    
    # 2. 「最新エピソード」のリンクを直接検索
    # カクヨムの最新話は「js-episode-list」クラス内の最初にあることが多い
    episode_list = soup.find('ol', class_='js-episode-list')
    latest_episode = episode_list.find_all('li', class_='widget-episodeList-episode')[-1]
    
    if not latest_episode:
        raise Exception("最新エピソードが見つかりません")

    # タイトル（リンク内のテキスト）と日付を取得
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
