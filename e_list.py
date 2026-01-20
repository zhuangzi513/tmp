import akshare as ak
import pandas as pd
import requests
from bs4 import BeautifulSoup
import json
import re
from datetime import datetime

now = datetime.now()
date_str = now.strftime("%Y%m%d")


def get_all_etf_list():
    try:
        df_etf_spot = ak.fund_etf_spot_em()
        df_etf_spot.to_csv('all_etf_list.csv', index=False, encoding='utf-8-sig')
        etf_list = df_etf_spot[['代码', '名称']].copy()
        return etf_list
    except Exception as e:
        print(f"获取列表失败，错误信息：{e}")
        return pd.DataFrame()

class ETFConstituentFetcher:
    """ETF成分股获取综合类"""

    def __init__(self):
        self.list_file_name='all_etf_list.csv'
        self.results = {} 
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })

    def fetch_from_szse(self, etf_code):
         url = f"http://reportdocs.static.szse.cn/files/text/etf/ETF{etf_code}{date_str}.txt"
         print(url)
         save_path=f"ETF{etf_code}{date_str}.txt"
         try:
             response = requests.get(url, timeout=30)
             response.raise_for_status()
             print(response.content)
             if save_path:
                 with open(save_path, 'wb') as f:
                     f.write(response.content)
                 return save_path
             else:
                 return response.content
         except:
             print(f"{etf_code} failed")

    def fetch_from_sse(self, etf_code):
        url = f"https://query.sse.com.cn/etfDownload/downloadETF2Bulletin.do?fundCode={etf_code}"
        save_path=f"ETF{etf_code}{date_str}.xml"
        try:
             response = requests.get(url)
             response.raise_for_status()
             if save_path:
                 with open(save_path, 'wb') as f:
                     f.write(response.content)
                 return save_path
             else:
                 return response.content
        except:
             print(f"{etf_code} failed")


    def fetch_from_fund_company(self, etf_code):
	if etf_code.startwith("51") or etf_code.startwith("58"):
		fetch_from_sse(etf_code)
	elif etf_code.startwith("15")
		fetch_from_szse(etf_code)

    def get_all_constituents(self, etf_code, method="auto"):

        #if method in ["auto", "akshare"]:
        #    try:
        #        self.results["akshare"] = ak.fund_portfolio_hold_em(symbol=etf_code)
        #    except:
        #        pass

        if method in ["auto", "fund_company"]:
            self.results["fund_company"] = self.fetch_from_fund_company(etf_code)

        return self.results


def read_csv(file_name):
    df = pd.read_csv(file_name, sep=',', encoding='utf-8')
    json_object = df.to_dict('records')
    return json_object
    for i, obj in enumerate(json_object):
        print(f"row: {i}")
        print(f"code: {obj.get('代码')}, name: {obj.get('名称')}")

if __name__ == '__main__':
    get_all_etf_list()
    list_file_name='all_etf_list.csv'
    json_objs = read_csv(list_file_name)

    fetcher = ETFConstituentFetcher()
    for i, obj in enumerate(json_objs):
        print(f"row: {i}")
        code = obj.get('代码')
        name = obj.get('名称')
        print(f"code: {code}, name: {name}")
        constituents = fetcher.get_all_constituents(str(code))
        print(constituents['fund_company'])
