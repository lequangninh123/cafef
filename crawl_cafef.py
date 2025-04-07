import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

def crawl_carref_foreign_net():
    url = "https://cafef.vn/du-lieu/lich-su-giao-dich-vnindex-3.chn#data"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # Check for HTTP errors
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Updated table selector - try these alternatives:
        table = soup.find('table', {'id': 'tableData'}) or \
                soup.find('table', {'class': 'dataTable'}) or \
                soup.select_one('div.table-responsive table')
        
        if not table:
            raise ValueError("Could not find the data table in HTML")
            
        rows = table.find_all('tr')[2:]  # Skip headers
        
        data = []
        for row in rows:
            cols = row.find_all('td')
            if len(cols) >= 3:  # Ensure enough columns
                date_str = cols[0].text.strip()
                net_value = cols[2].text.replace(',', '').strip()
                
                try:
                    date = datetime.strptime(date_str, "%d/%m/%Y")
                    data.append([date.strftime("%Y-%m-%d"), float(net_value)])
                except ValueError as e:
                    print(f"Skipping malformed row: {e}")
        
        df = pd.DataFrame(data, columns=["date", "net_value"])
        df.to_csv("foreign_net_values.csv", index=False)
        return df
        
         # Ensure data exists before saving
        if len(data) > 0:
            df = pd.DataFrame(data, columns=["date", "net_value"])
            df.to_csv("foreign_net_values.csv", index=False)
            print("✅ Successfully saved data to CSV")
            return True
        else:
            print("⚠️ No data found to save")
            return False
            
    except Exception as e:
        print(f"❌ Crawling failed: {e}")
        return False

if __name__ == "__main__":
    success = crawl_carref_foreign_net()
    exit(0 if success else 1)  # Exit with error code if failed