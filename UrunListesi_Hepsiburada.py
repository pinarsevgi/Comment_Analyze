
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time


class UrunListesiAlma:
    def __init__(self, base_url, max_pages=10):
        self.base_url = base_url
        self.max_pages = max_pages
        self.all_products = []
        self.total_reviews = 0
        # **📌 Selenium Tarayıcıyı Başlat**
        options = Options()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    def accept_cookies(self):
        """Çerezleri kabul eder (varsa)."""
        try:
            cookie_button = self.driver.find_element(By.ID, "onetrust-accept-btn-handler")
            cookie_button.click()
            print("✅ Çerezler kabul edildi!")
            time.sleep(2)
        except:
            print("⚠️ Çerez butonu bulunamadı, devam ediliyor...")

    def get_products(self):
        """Ürünleri çeker ve listeye ekler."""
        try:
            product_titles = self.driver.find_elements(By.XPATH, "//h3[@data-test-id='product-card-name']")

            for title in product_titles:
                product_name = title.text.strip()  # Ürün adını al

                try:
                    # **📌 Ürün Linkini Bulma**
                    product_link = title.find_element(By.XPATH, "./ancestor::a").get_attribute("href")
                except:
                    product_link = "Link Bulunamadı"

                try:
                    # **📌 Yorum Sayısını Bulma**
                    review_element = title.find_element(By.XPATH, "./following::div[@data-test-id='review']")
                    review_count = review_element.text.strip()
                except:
                    review_count = "0"  # Eğer yorum bulunamazsa 0 ata

                # **📌 Yorum Sayısını Sayıya Çevir ve Toplamı Güncelle**
                try:
                    reviews_clean = int(review_count.replace(".", "").replace(",", ""))  # 1.512 → 1512, 1,512 → 1512
                    self.total_reviews += reviews_clean
                except ValueError:
                    print(f"⚠️ Hatalı yorum sayısı algılandı ve atlandı: {review_count}")
                    reviews_clean = 0

                self.all_products.append([product_name, reviews_clean, product_link])
        except:
            print("⚠️ Ürün başlıkları bulunamadı!")

    def scrape(self, page_limit=None):
        """
        Hepsiburada'dan ürünleri çeker ve Pandas DataFrame olarak döndürür.
        - page_limit: Kaç sayfanın verisini almak istiyorsan belirtebilirsin.
                      Varsayılan olarak None, yani `self.max_pages` kadar çeker.
        """
        if page_limit is None:
            page_limit = self.max_pages  # Eğer belirtilmezse, varsayılan `max_pages` değeri kullanılır

        for page_num in range(1, page_limit + 1):
            url = f"{self.base_url}&sayfa={page_num}"
            print(f"\n🌍 Sayfa {page_num} Yükleniyor: {url}")

            # Sayfayı aç
            self.driver.get(url)
            time.sleep(5)  # **Sayfanın yüklenmesini bekle**

            # **Çerezleri kabul et (ilk sayfada)**
            if page_num == 1:
                self.accept_cookies()

            # **Ürünleri çek**
            self.get_products()

        # **📌 Tarayıcıyı kapat**
        self.driver.quit()

        # **📌 Sonuçları Pandas DataFrame'e Çevir**
        df = pd.DataFrame(self.all_products, columns=["Product_Name", "Comment_Count", "Link"])

        # **📌 Toplam Yorum ve Ürün Sayısını Yazdır**
        print(f"\n🔢 Toplam Yorum Sayısı: {self.total_reviews}")
        print(f"📦 Toplam Ürün Sayısı: {len(self.all_products)}")

        # **📌 DataFrame'i Return Et**
        return df


# **📌 Kullanım**
if __name__ == "__main__":
    base_url = input("Lütfen Hepsiburada ürün listesinin URL'sini girin: ").strip()
    scraper = UrunListesiAlma(base_url)

    # Kullanıcı kaç sayfa çekeceğini belirleyebilir
    page_limit = 2  # int(input("Kaç sayfa verisini almak istiyorsunuz? (Varsayılan: 5) ") or 5)

    product_df = scraper.scrape(page_limit=page_limit)

    # **📌 Sonuçları Tabloda Yazdır**
    print("\n✅ Ürünler Tablosu:")
    print(product_df.to_string(index=False))  # Daha düzenli yazdırma
