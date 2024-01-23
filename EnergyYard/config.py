import time


def UnixTime():

    current_timestamp = int(time.time())

    return current_timestamp


user_agents = ["Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36",
               "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.72 Safari/537.36",
               "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10) AppleWebKit/600.1.25 (KHTML, like Gecko) Version/8.0 Safari/600.1.25",
               "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:33.0) Gecko/20100101 Firefox/33.0",
               "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36",
               "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36",
               "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/600.1.17 (KHTML, like Gecko) Version/7.1 Safari/537.85.10",
               "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko",
               "Mozilla/5.0 (Windows NT 6.3; WOW64; rv:33.0) Gecko/20100101 Firefox/33.0",
               "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.104 Safari/537.36"
               ]


_1668_headers = {
    'authority': 'widget.1688.com',
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'en-US,en;q=0.9',
    'cache-control': 'no-cache',
    'content-type': 'application/x-www-form-urlencoded;charset=UTF-8',
    'origin': 'https://widget.1688.com',
    'pragma': 'no-cache',
    'referer': 'https://widget.1688.com/front/ajax/bridge.html?target=brg-29155',
    'sec-ch-ua': '"Chromium";v="112", "Google Chrome";v="112", "Not:A-Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
}

_1668_data = {
    'namespace': 'cateMarketOfferList',
    'widgetId': 'cateMarketOfferList',
    'methodName': 'execute',
    'params': '{"sceneId":"2153","curPage":1,"pageSize":200,"sortType":null,"descendOrder":null,"priceStart":null,"priceEnd":null,"province":"","city":""}',
    'sceneId': '2153',
    'curPage': '1',
    'pageSize': '200',
    'sortType': 'null',
    'descendOrder': 'null',
    'priceStart': 'null',
    'priceEnd': 'null',
    'province': '',
    'city': '',
    '__mbox_csrf_token': f'PLUw7eze4UGDEE8m_{str(UnixTime())}',
    '_input_charset': 'utf-8',
}

_1668_cookies = {
    '__cn_logon__': 'false',
    'cna': 'chQfHJjJfwACAWcRU7qW9+DF',
    'taklid': 'cfa3396b344a4410af49165bb148ac29',
    'tfstk': 'cyWGBoDbv1R6M6eARN9_ePj7oNWcaED2rtWCLkrqJ1JJPkS6bsASTb7GJkYgPPlf.',
    '__mwb_logon_id__': 'undefined',
    '_csrf_token': str(UnixTime()),
    'cookie2': '1490a1329026e2767a40f2408518a9ea',
    't': '5c400143ccd617be1de4f768c8c8e379',
    '_tb_token_': 'ff3f5b78eeb67',
    'alicnweb': 'touch_tb_at%3D1679660898386',
    '_m_h5_tk': '474be4ebe06b7567baef3281e6e02476_1681468750991',
    '_m_h5_tk_enc': 'c3c9615a06205f4e57f8c1fc5455e886',
    '__mbox_csrf_token': f'PLUw7eze4UGDEE8m_{str(UnixTime())}',
    'l': 'fBIHTV9ITAagxjXbKOfwPurza77OSIRAguPzaNbMi9fPOyfw5JzfW1gsY6YeC3MNF6PyR3kOuRA9BeYBqIcidj4dCgpMGIMmnmOk-Wf..',
    'isg': 'BDU16LKevc00FN7QAWT47tOuRLHvsunE1sz1v7da8az7jlWAfwL5lEMM2Eq4zgF8',
}


default_headers = {
    'cache-control': 'no-cache',
    'if-modified-since': 'Mon, 26 Jul 1997 05:00:00 GMT',
    'sec-fetch-mode': 'cors',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
    'x-xsrf-token': '64981f13-d594-4db2-a9d0-2fbd830c393b',
    'Cookie': 'g2usersessionid=7d90a88ea25ffafd5ad77a7459772725; G2JSESSIONID=6012FC270370D42558092FF96C47C378-n1; incap_ses_49_242093=CzZzaZoQgH5cWLLcRhWuAJPadWQAAAAAfQhunqyNS/0EitrpysyKpQ==; nlbi_242093=djWVbVk58TIp+QTpJDHybgAAAAC5somYcaEhg48d0V2J6eTp; visid_incap_242093=m7w/LeN5S0CV2Ol2lVJ62YXadWQAAAAAQUIPAAAAAACb/4Zx+zripQEDKUx1xgYS'
}
