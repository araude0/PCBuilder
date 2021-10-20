import time
import requests
from bs4 import BeautifulSoup
import pandas as pd

esti = []

def getPcode(page):
    pCodeList = []
    for i in range(1, page + 1):
        print(i, "페이지 입니다")
        headers = {
            "Referer": "http://prod.danawa.com/list/?cate=11312468",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Safari/537.36"
        }
        params = {"page": i, "listCategoryCode": 12468, "categoryCode": 12468, "physicsCate1": 862,
                  "physicsCate2": 887, "physicsCate3": 0, "physicsCate4": 0, "viewMethod": "LIST",
                  "sortMethod": "",
                  "listCount": 30, "group": 11, "depth": 3, "brandName": "", "makerName": "", "searchOptionName": "",
                  "sDiscountProductRate": 0, "sInitialPriceDisplay": "N",
                  "sPowerLinkKeyword": "CPU 쿨러", "oCurrentCategoryCode": "a:3:{i:1;i:97;i:2;i:747;i:3;i:12468;}",
                  "innerSearchKeyword": "",
                  "listPackageType": 3, "categoryMappingCode": 13228, "priceUnit": 0, "priceUnitValue": 0,
                  "priceUnitClass": "",
                  "cmRecommendSort": "N", "cmRecommendSortDefault": "N", "bundleImagePreview": "N", "nPackageLimit": 5,
                  "nPriceUnit": 0, "bMakerDisplayYN": "Y", "isDpgZoneUICategory": "N", "isAssemblyGalleryCategory": "N",
                  "sProductListApi": "search"}
        res = requests.post("http://prod.danawa.com/list/ajax/getProductList.ajax.php", headers=headers, data=params)

        soup = BeautifulSoup(res.text, "html.parser")
        a = soup.findAll("li", {"class": "prod_item prod_layer"})

        for j in a:
            w = j.find(class_="price_sect").text.replace("가격정보 더보기","").replace("\n","").replace("\t","")
            x = j.find(class_="spec_list").text + " / "
            y = j.find(class_= "prod_name").text + " / "
            y = y.replace("\n","").replace("\t","")
            x = x.replace("\n","").replace("\t","")
            z = y + x + w
            esti.append(z.split(" / "))
            print(esti)

    return

getPcode(10)

data =  pd.DataFrame(esti)
data.to_csv('cooler.csv', encoding = 'cp949')

