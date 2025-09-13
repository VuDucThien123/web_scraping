from playwright.sync_api import sync_playwright
import pandas as pd
import time

def crawl_lazada(limit):
    with sync_playwright() as p:
        # Khởi tạo browser
        browser = p.chromium.launch(headless=False)  # False để quan sát trực tiếp
        page = browser.new_page()

        # Truy cập Lazada (ví dụ trang gợi ý)
        page.goto("https://www.lazada.vn/")

        # Lặp lại: cuộn xuống + bấm "Tải thêm"
        for i in range(limit):
            try:
                # Cuộn xuống cuối trang
                page.mouse.wheel(0, 5000)
                time.sleep(5)

                # Kiểm tra nút "Tải thêm"
                load_more_btn = page.locator("text=TẢI THÊM")
                if load_more_btn.is_visible():
                    load_more_btn.click()
                    print(f"👉 Đã bấm 'Tải thêm' lần {i + 1}")
                    time.sleep(3)
                else:
                    print("⚠️ Không còn nút 'Tải thêm'")
                    break
            except Exception as e:
                print("Lỗi khi tải thêm:", e)
                break
        # Cuộn xuống cuối trang chờ load hết
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        page.wait_for_selector("img[src]", timeout=8000)

        # Lấy danh sách sản phẩm
        products = page.locator("a.pc-custom-link.jfy-item").all()

        results = []

        for product in products:
            try:
                # Lấy tên sản phẩm
                name = product.get_attribute("name")

                # Lấy URL sản phẩm (thêm https nếu thiếu)
                url = product.get_attribute("href")
                if url and url.startswith("//"):
                    url = "https:" + url

                # Lấy giá
                price = product.locator(".hp-mod-price .price").inner_text(timeout=1000)

                # Lấy discount (nếu có)
                try:
                    discount = product.locator(".hp-mod-price-first-line .hp-mod-discount").inner_text(timeout=1000)
                except:
                    discount = "No discount"

                # Ảnh sản phẩm
                try:
                    image = product.locator("img").get_attribute("src", timeout=2000)
                except:
                    image = "No image"


                # Rating (lấy % trong style width)
                try:
                    rating_style = product.locator(".card-jfy-rating-layer.top-layer").get_attribute("style")
                    # ví dụ: "width: 96%;" -> lấy 96
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
    limit = int(input("Nhap limit: "))
    data = crawl_lazada(limit)

    # Xuất ra CSV
    df = pd.DataFrame(data)
    df.to_csv("lazada_products_2.csv", index=False, encoding="utf-8-sig")

    print("✅ Đã lưu kết quả vào lazada_products_2.csv")
