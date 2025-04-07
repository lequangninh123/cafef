import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

def crawl_cafef_foreign_net():
    url = "https://cafef.vn/du-lieu/lich-su-giao-dich-vnindex-3.chn#data"
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Tìm bảng dữ liệu khối ngoại (cần inspect HTML để xác định selector)
    table = soup.select_one("table#tableData")
    rows = table.find_all("tr")[2:]  # Bỏ qua header
    
    data = []
    for row in rows:
        cols = row.find_all("td")
        date_str = cols[0].text.strip()
        net_value = float(cols[2].text.replace(",", "").strip())
        
        # Chuyển đổi ngày từ "dd/mm/yyyy" sang datetime
        date = datetime.strptime(date_str, "%d/%m/%Y")
        timestamp = int(date.timestamp())
        
        data.append([timestamp, net_value])
    
    df = pd.DataFrame(data, columns=["timestamp", "net_value"])
    df.to_csv("foreign_net_values.csv", index=False)
    return df

if __name__ == "__main__":
    crawl_cafef_foreign_net()