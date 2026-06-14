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
    
    # 1. 作品タイトル
    work_title = soup.find('h1').text.strip()
    
    # 2. エピソードリンクの抽出
    all_links = soup.find_all('a')
    episode_links = [link for link in all_links if '/episodes/' in link.get('href', '')]
    
    if not episode_links:
        raise Exception("エピソードリンクが見つかりません")

    # 最新話のリンク
    latest_link = episode_links[-1]
    
    # 3. 日付を探す（リンクと同じ親ブロック（divやliなど）から遡って探す）
    # リンク要素の親から遡って time を探す
    time_tag = latest_link.find_parent().find('time')
    
    # それでも見つからない場合、念のためページ全体から探す
    if not time_tag:
        time_tag = soup.find('time')
        
    episode_title = latest_link.text.strip()
    episode_date = time_tag['datetime'] if time_tag and time_tag.has_attr('datetime') else "2026-06-14T20:00:00+09:00"
    
    return work_title, episode_title, episode_date

def generate_rss(work_title, episode_title, episode_date):
    fg = FeedGenerator()
    fg.title(work_title)
    fg.link(href=WORK_URL)
    fg.description("カクヨム更新通知")
    
    fe = fg.add_entry()
    fe.title(episode_title)
    fe.updated(episode_date)
    fe.link(href=WORK_URL)
    fe.description(f"更新日: {episode_date}")
    
    fg.rss_file(RSS_FILE)

if __name__ == "__main__":
    t, e, d = fetch_kakuyomu()
    generate_rss(t, e, d)
