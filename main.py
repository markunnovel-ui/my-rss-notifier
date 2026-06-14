import requests
from bs4 import BeautifulSoup

WORK_URL = "https://kakuyomu.jp/works/2912051601556641467"

def fetch_kakuyomu():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
    }
    response = requests.get(WORK_URL, headers=headers)
    print(f"ステータスコード: {response.status_code}")
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # ページの一部を表示して確認
    print("--- ページタイトルの確認 ---")
    print(soup.title.text if soup.title else "タイトル取得失敗")
    
    # ページ内にあるすべてのh1タグを表示して確認
    print("--- ページ内のh1タグ一覧 ---")
    for h1 in soup.find_all('h1'):
        print(h1.text.strip())

if __name__ == "__main__":
    fetch_kakuyomu()
