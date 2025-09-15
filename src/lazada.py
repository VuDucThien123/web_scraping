from playwright.sync_api import sync_playwright
import pandas as pd
import time

def crawl_lazada(limit):
    with sync_playwright() as p:
        # init browser
        browser = p.chromium.launch(headless=False)  # False to view direct
        page = browser.new_page()

        # Truy cập Lazada (ví dụ trang gợi ý)
        page.goto("https://www.lazada.vn/")

        # Loop: scroll + button "TẢI THÊM"
        for i in range(limit):
            try:
                # scroll the bottom of page
                page.mouse.wheel(0, 5000)
                time.sleep(5)

                # check button "TẢI THÊM"
                load_more_btn = page.locator("text=TẢI THÊM")
                if load_more_btn.is_visible():
                    load_more_btn.click()
                    print(f"Đã bấm 'Tải thêm' lần {i + 1}")
                    time.sleep(3)
                else:
                    print("Không còn nút 'Tải thêm'")
                    break
            except Exception as e:
                print("Lỗi khi tải thêm:", e)
                break
        # scroll bottom of page, wait load full
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        page.wait_for_selector("img[src]", timeout=8000)

        # get list product
        products = page.locator("a.pc-custom-link.jfy-item").all()

        results = []

        for product in products:
            try:
                # name
                name = product.get_attribute("name")

                # URL
                url = product.get_attribute("href")
                if url and url.startswith("//"):
                    url = "https:" + url

                # price
                price = product.locator(".hp-mod-price .price").inner_text(timeout=1000)

                #  discount
                try:
                    discount = product.locator(".hp-mod-price-first-line .hp-mod-discount").inner_text(timeout=1000)
                except:
                    discount = "No discount"

                # product image
                try:
                    image = product.locator("img").get_attribute("src")
                except:
                    image = "No image"


                # Rating
                try:
                    rating_style = product.locator(".card-jfy-rating-layer.top-layer").get_attribute("style")
                    # "width: 96%;" -> 96
                    rating_percent = rating_style.split(":")[-1].replace("%;", "").replace("%", "").strip()
                except:
                    rating_percent = "No rating"

                # Comment count
                try:
                    comments = product.locator(".card-jfy-ratings-comment").inner_text()
                except:
                    comments = "No comments"

                results.append({
                    "name": name,
                    "price": price,
                    "discount": discount,
                    "url": url,
                    "image": image,
                    "rating": rating_percent,
                    "comments": comments,
                })

            except Exception as e:
                print("Error parsing product:", e)

        browser.close()
        return results


if __name__ == "__main__":
    limit = int(input("input limit: "))
    data = crawl_lazada(limit)

    # export CSV
    df = pd.DataFrame(data)
    df.to_csv("lazada_product.csv", index=False, encoding="utf-8-sig")
    print("Đã lưu kết quả vào lazada_product.csv")
