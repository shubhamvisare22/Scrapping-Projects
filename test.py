import requests
import json

class SurplusScrapper:
    
    def __init__(self):
        self.seller_name_list = []
        self.asset_name_list = []
        self.seller_phone_list = []
        self.seller_email_list = []
        self.acoount_id_list = []
        self.asset_id_list = []
        self.asset_auction_start_list = []
        self.asset_auction_end_list = []
        
        self.headers = {
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
        
        self.payload = json.dumps({"categoryIds":"","businessId":"AD","searchText":"*","isQAL":False,"locationId":None,"model":"","makebrand":"","auctionTypeId":None,"page":1,"displayRows":100,"sortField":"bestfit","sortOrder":"desc","sessionId":"497d15b1-b9c6-efb5-f960-ecefa17172f6","requestType":"search","responseStyle":"productsOnly","facets":["categoryName","auctionTypeID","condition","saleEventName","sellerDisplayName","product_pricecents","isReserveMet","hasBuyNowPrice","sellerType","doWarehouse","region","currencyTypeCode","categoryName","tierId"],"facetsFilter":["{!tag=product_category_external_id}product_category_external_id:\"t3\""],"timeType":"","sellerTypeId":None,"accountIds":[]})
    
    def make_request(self, url):
        response = requests.request("POST", url, headers=self.headers, data=self.payload)
        return response
         
    
    def MainScript(self):
        main_url = "https://maestro.lqdt1.com/search/list"
        response = self.make_request(main_url)
        response = json.loads(response.content)
        
        self.acoount_id_list = [i['accountId'] for i in response['assetSearchResults'] ]
        self.asset_id_list = [i['assetId'] for i in response['assetSearchResults'] ]

        #  Scrapping starts from here. 
        for i,j in zip(self.acoount_id_list, self.asset_id_list):
            asset_url = f'https://maestro.lqdt1.com/assets/{j}/{i}/false'
            
            asset_response = self.make_request(asset_url)
            asset_response = json.loads(asset_response.content)
            
            asset_name_list = asset_response['assetShortDesc']
            self.asset_name_list.append(asset_name_list.strip() if asset_name_list else '-')
            
            asset_auction_start = asset_response['assetAuctionStartDate']
            self.asset_auction_start_list.append(asset_auction_start.split('T')[0].strip() if asset_auction_start else '-' )
            
            asset_auction_end = asset_response['assetAuctionEndDate']
            self.asset_auction_end_list.append(asset_response['assetAuctionEndDate'].split('T')[0].strip() if asset_auction_end else '-' )
            
            seller_name_list = asset_response['sellerContactName']
            self.seller_name_list.append(seller_name_list if seller_name_list else '-')
            
            asset_seller_email_list = asset_response['sellerContactEmail']
            self.seller_email_list.append(asset_seller_email_list if asset_seller_email_list else '-')
            
            seller_phone_list_number = asset_response['sellerContactPhone']
            self.seller_phone_list.append(self.seller_phone_list if seller_phone_list_number else '-' )
            
           
            
        return 


if __name__ == '__main__':
    scrapper = SurplusScrapper()
    scrapper.MainScript()
    
    