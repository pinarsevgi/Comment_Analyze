# Comment_Analyze
 
## HepsiburadaScraper 

`hepsiburada_scraper_v2.py` içinde aşağıdaki fonksiyonlar kullanılmıştır;
* `accept_cookies`  : URL açıldıktan sonra tüm cookiesleri kabul etmek için yazılmıştır. çalışırken hata veriyor tekrar bakılacak
* `get_total_page`  : Birden fazla sayfada yorum var ise sayfalar arasında dolaşmak için hazırlandı.
* `scrap_viewer`    : Tüm yorumları liste olarak toplamaktadır. 


### Calisma_v1
`hepsiburada_scraper_v2` Class'ı kullanılarak istenilen URL içindeki yorumların alınması yapılmıştır.
yorumlar dataFrame çevrilmiştir ve `\n`yerine boşluk gelecek şekide düzenlenmiştir. 

```javascript
data2=pd.DataFrame(reviews2,columns=["Comments"])
```

#\n alanları boşuk ile değiştir \n tipi str değilse hata vermesin
```javascript
data2["Comments"]=data2["Comments"].apply(lambda x: x.replace("\n", " ") if isinstance(x,str) else x) 
data2
```
