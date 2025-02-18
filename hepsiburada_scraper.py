from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

class HepsiburadaScraper:
    def __init__(self, product_url):
        """Selenium tarayıcı ayarlarını başlatır ve URL'yi yükler."""
        self.url = product_url
        self.options = Options()
        # options.add_argument("--headless")  # Arka planda çalıştırmak için (istersen kaldır)
        self.options.add_argument("--no-sandbox")
        self.options.add_argument("--disable-dev-shm-usage")

        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=self.options)
        self.driver.get(self.url)
        time.sleep(3)
        self.accept_cookies()

    def accept_cookies(self):
        """Hepsiburada'daki çerezleri kabul eder."""
        try:
            cookie_button = self.driver.find_element(By.ID, "onetrust-accept-btn-handler")
            cookie_button.click()
            print("✅ Çerezler kabul edildi!")
            time.sleep(2)
        except:
            print("⚠️ Çerez butonu bulunamadı, devam ediliyor...")

    def get_total_pages(self):
        """Toplam sayfa numarasını döndürür."""
        self.driver.get(self.url)  # Her çağrıldığında sayfayı yenile
        time.sleep(3)

        pages = self.driver.find_elements(By.CLASS_NAME, "hermes-src-universal-components-Pagination-PaginationBar-PageHolder-PageHolder-module__pageHolderPage")
        page_numbers = [int(page.text.strip()) for page in pages if page.text.strip().isdigit()]
        
        if page_numbers:
            return max(page_numbers)  # En büyük sayfa numarasını döndür
        else:
            return 1  # Eğer sayfa numarası bulunamazsa, en azından 1 sayfa olduğunu varsay

    def scrape_reviews(self):
        """Tüm yorumları çeker ve liste olarak döndürür."""
        total_pages = self.get_total_pages()
        all_comments = []

        for page in range(1, total_pages + 1):
            print(f"📄 {page}. sayfadaki yorumlar çekiliyor...")

            # **WebElement'leri tekrar bul!**
            self.driver.get(self.url)  # Sayfayı her tıklama öncesinde yenile
            time.sleep(3)

            # Sayfa numarasına göre butonu bul ve tıkla
            try:
                page_span = self.driver.find_element(By.XPATH, f"//span[contains(@class, 'pageHolderPage') and text()='{page}']")
                page_button = page_span.find_element(By.XPATH, "./parent::*")

                # JavaScript ile sayfa butonuna tıklama işlemi
                self.driver.execute_script("arguments[0].click();", page_button)
                time.sleep(3)
            except:
                print(f"⚠️ {page}. sayfa butonu bulunamadı veya tıklanamadı!")
                break

            # **Yorumları her seferinde yeniden bul!**
            comments = self.driver.find_elements(By.CLASS_NAME, "hermes-src-universal-components-ReviewCard-ReviewCard-module__review")
            for comment in comments:
                all_comments.append(comment.text.strip())

        self.driver.quit()
        return all_comments

# Kullanım Örneği:
if __name__ == "__main__":
    url = "https://www.hepsiburada.com/kiwi-kcc-4327-koltuk-ve-hali-yikama-makinesi-p-HBCV000077WVLU-yorumlari"
    scraper = HepsiburadaScraper(url)
    reviews = scraper.scrape_reviews()

    # Tüm yorumları yazdır
    for i, comment in enumerate(reviews, 1):
        print(f"{i}. Yorum: {comment}")
