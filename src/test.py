from playwright.sync_api import sync_playwright
import pandas as pd
def crawl_lazada_first_page():
    with sync_playwright() as p:
        # Khởi tạo browser
        browser = p.chromium.launch(headless=False)  # False để quan sát trực tiếp
        page = browser.new_page()

        # Truy cập Lazada (ví dụ trang gợi ý)
        page.goto("https://www.lazada.vn/")

        # Đợi trang load hoàn tất
        page.wait_for_load_state("networkidle")

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

                results.append({
                    "name": name,
                    "price": price,
                    "discount": discount,
                    "url": url
                })

            except Exception as e:
                print("Error parsing product:", e)

        browser.close()
        return results


if __name__ == "__main__":
    data = crawl_lazada_first_page()

    # Xuất ra CSV
    df = pd.DataFrame(data)
    df.to_csv("lazada_products_2.csv", index=False, encoding="utf-8-sig")

    print("✅ Đã lưu kết quả vào lazada_products_2.csv")
