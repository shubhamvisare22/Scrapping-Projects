import json 


headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'en-US,en;q=0.9',
    'Content-Type': 'application/json',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    'sec-ch-ua-platform': '"Windows"',
    'x-api-correlation-id': '798c34c0-c081-2dd9-d53c-55b5868b0662',
    'x-api-key': '9347724c-b351-4b15-92c9-a7ef130a603f',
    'x-ecom-session-id': 'aa4ea481-c4b6-56a0-c0e1-16ce886d6752',
    'x-page-unique-id': 'aHR0cHM6Ly93d3cuYWxsc3VycGx1cy5jb20vZW5lcmd5LWVxdWlwbWVudA=',
    'x-user-id': '-1',
    'x-user-timezone': 'Asia/Calcutta',
}

payload = json.dumps({"categoryIds": "", "businessId": "AD", "searchText": "*", "isQAL": False, "locationId": None, "model": "", "makebrand": "", "auctionTypeId": None, "page": 1, "displayRows": 100, "sortField": "bestfit", "sortOrder": "desc", "sessionId": "497d15b1-b9c6-efb5-f960-ecefa17172f6", "requestType": "search", "responseStyle": "productsOnly", "facets": [
    "categoryName", "auctionTypeID", "condition", "saleEventName", "sellerDisplayName", "product_pricecents", "isReserveMet", "hasBuyNowPrice", "sellerType", "doWarehouse", "region", "currencyTypeCode", "categoryName", "tierId"], "facetsFilter": ["{!tag=product_category_external_id}product_category_external_id:\"t3\""], "timeType": "", "sellerTypeId": None, "accountIds": []})

main_url = "https://maestro.lqdt1.com/search/list"
