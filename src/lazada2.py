import requests
import json
import pandas as pd
url = "https://www.lazada.vn/tag/%C4%90i%E1%BB%87n-tho%E1%BA%A1i-di-%C4%91%E1%BB%99ng/?ajax=true&catalog_redirect_tag=true&from=hp_categories&isFirstRequest=true&page=1&q=%C4%90i%E1%BB%87n%20tho%E1%BA%A1i%20di%20%C4%91%E1%BB%99ng&service=all_channel&spm=a2o4n.tm80151110.cate_1.1.55e9KEbfKEbfJ6&src=all_channel"

payload = {}
headers = {
  'accept': 'application/json, text/plain, */*',
  'accept-language': 'vi,vi-VN;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5',
  'priority': 'u=1, i',
  'referer': 'https://www.lazada.vn/',
  'sec-ch-ua': '"Chromium";v="140", "Not=A?Brand";v="24", "Google Chrome";v="140"',
  'sec-ch-ua-mobile': '?0',
  'sec-ch-ua-platform': '"Windows"',
  'sec-fetch-dest': 'empty',
  'sec-fetch-mode': 'cors',
  'sec-fetch-site': 'same-origin',
  'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36',
  'x-csrf-token': 'e5e8e7b7aeee1',
  'Cookie': '__wpkreporterwid_=91b40581-ad2d-48a7-ac13-deef8d68d98a; G_AUTHUSER_H=0; t_fv=1744192978107; t_uid=BdWM89weukMbg4WyalpW6a9YMDrMHclM; lzd_cid=229ebc31-6f01-43be-a7e0-e7a885b1dd75; cna=wTN9IB70Yh0CARtMuyCuaTfn; miidlaz=miidgk2chh1j41ka5mu6ffv; hng=VN|vi|VND|704; userLanguageML=vi; lzd_click_id=clkgg5qhu1j41kbndgud21; __itrace_wid=7d71006a-4159-47c3-9f6c-4a4b1c2de1cc; lwrid=AgGZPC7ROJ0kOjz8%2FbuMX39uIwDz; _tb_token_=e5e8e7b7aeee1; xlly_s=1; lwrtk=AAIEaMQR/lQ5Z7U8kyyrJ0Io0v1vJYQL5m2YhO0gZgEsyhY9nRkcfEs=; LZD_WEB_TRACER_ROOT_SPAN_ID=4ed49c419604b8e0; LZD_WEB_TRACER_TRACE_ID=12df39c7dd0e4c5b8e759ff08cf26f35; EGG_SESS=S_Gs1wHo9OvRHCMp98md7Iyryk4doTKk9hVhCdPaRY1buSfYkFbY4DKLX8kL0hB7hs_mJQzsbKkIfwT4IL0kQZsPy9sccY_p64e-mjnIhuq1Yn9ZmLdyPiHFTtpGHRIIe3lWyaMhKV9pskDmE1bywHim8KOcVhxCMZq5VvwuZsE=; G_ENABLED_IDPS=google; lzd_login_lastlogintype=GOOGLE; lzd_sid=16a9051bd608ee27b74713bf8e04eea9; lzd_uid=200152389230; lzd_b_csg=80f838f0; sgcookie=E10066yz8kf8xqxwcFj%2Fx6k97C5LBYnJMyKXMdsTwlNzUeVCqNZe5RUK88ujLQRHmCjtolJA%2Bvqt2QKReHt3O6%2FJEcjlJr47pJ%2FxGC3%2B14nugVk%3D; lzd_uti=%7B%22fpd%22%3A%229999-99-99%22%2C%22lpd%22%3A%229999-99-99%22%2C%22cnt%22%3A%220%22%7D; t_sid=KrEHmMEXyEaFaXyXMOxd0rofD500mjfk; utm_origin=https://www.google.com/; utm_channel=SEO; _m_h5_tk=9b61c7dfb499ae583ad010c28558632e_1757674517953; _m_h5_tk_enc=2d95735f943b151b7c708b4b6411f2c3; isg=BPLyJMeGzs6DDPIbRzbLoTJqQzjUg_YdyI6Xw7zPpKWqT5FJpBLoLXHsP_NzP261; epssw=10*n1bss6MDWuqkkRxassss0gunoRPg6q3yumARFOxJUN5ssWu3-PasYZd66ss36DsrUNxQO-xessu6eD3DaERVlCpdd5pe6BK03YhskdV_rrsaXR5unCssBprYOyFyMDuBpoW4sdFOOZHCtOWOOf8NzFPMNvIhf0RuIPeDOe-xG5XyfmvQOkQ9ywfx54W0gvA38Pz66k5isRHQOecwtMMDOaXtOhANJ3WdMRFNc6-QOU3IGQv2tWrb67VNs1rRcGXabzq7UmK-i9JZ1IXewzX-ma1sNCspsCKUPkynLVGPh1e-yx4DuyTUOv-jPUMr4Arm3esrbHJo3bDY9-msla..; tfstk=gNyKupbjUNb38-YevzfGERG-06sgv1qUbyrXE40HNPUT4zU3t2q52YELy8jUV0V8Woaw-2wh8uaT2PRHEMkC2YELy8jEd0V8WoqSqwlIFlZsVmOC8zfFNYHUIWvo-wk8VrDRoZXcnkrtLY_cow8YRUHjcpgWrXg65Ym8osdGJkrEUh7gK4CbY3pWTOmSFzMs5mnIFeiSAGHsc0HWdb9B1FgZVYMSR0Gs50oXOHMSOGEs70MSPzGCXAgZVYg7PYMOz1gyOqv8OugESXLfEK9bBDhKyB09ekyXnX0bAVp5l8mpPqZIWUT-kHjQ9lEhJKriL-4xmyX6prE707GTeF_xzRE_d7ZwJaiaNyDs-x1BXv2UASG7haR7kvU-GJG9VpHsB4Mtf-skgV2t-zwK1ivxZAwmGvNG_wcopmU7LyKJFrZgmJlaeZLszWmqC0ePcQ3-Ng54n-KyHE0xqBsOXQRrOcRt7Lwolf5MUc3cjDRyafCwEBeoMQRr6LntoGm2aQlOT'
}

response = requests.request("GET", url, headers=headers, data=payload)

# Parse JSON
data = response.json()   # thay vì res.text

# Lấy list sản phẩm
items = data.get("mods", {}).get("listItems", [])

results = []
for item in items:
    product = {
        "name": item.get("name"),
        "nid": item.get("nid"),
        "image": item.get("image"),
        "priceShow": item.get("priceShow"),
        "voucher": item.get("icons", [{}])[0].get("text") if item.get("icons") else None,
        "ratingScore": item.get("ratingScore"),
        "review": item.get("review"),
        "location": item.get("location"),
        "sellerName": item.get("sellerName"),
        "brandName": item.get("brandName"),
        "originalPrice": item.get("originalPrice"),
        "inStock": item.get("inStock"),
        "itemUrl": "https:" + item.get("itemUrl") if item.get("itemUrl") else None,
    }
    results.append(product)

# Xuất ra DataFrame để dễ nhìn và lưu csv
df = pd.DataFrame(results)
print(df.head())

df.to_csv("lazada_product_2.csv", index=False, encoding="utf-8-sig")
