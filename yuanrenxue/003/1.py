import httpx


headers = {
    "sec-ch-ua-platform": "\"macOS\"",
    "x-requested-with": "XMLHttpRequest",
    "user-agent": "yuanrenxue",
    "accept": "application/json, text/javascript, */*; q=0.01",
    "sec-ch-ua": "\"Not:A-Brand\";v=\"8\", \"Chromium\";v=\"156\", \"Google Chrome\";v=\"156\"",
    "sec-ch-ua-mobile": "?0",
    "sec-fetch-site": "same-origin",
    "sec-fetch-mode": "cors",
    "sec-fetch-dest": "empty",
    "referer": "https://match.yuanrenxue.cn/match/3",
    "accept-encoding": "gzip, deflate, br, zstd",
    "accept-language": "zh-CN,zh;q=0.9",
    "priority": "u=0, i",
}
cookies = {
    "Hm_lvt_f80b2b389f44bbfb3bfe1704817d44e0": "1793624216",
    "HMACCOUNT": "08BEF2A03FF17943",
    "sessionid": "uctlufdiqdf9666w4q02wtg4sy13ra2z",
    "m": "1b52258c299ef7d6fdb3bdd992294702|1793624413830",
    "Hm_lpvt_f80b2b389f44bbfb3bfe1704817d44e0": "1793707059"
}
url = 'https://match.yuanrenxue.cn/api/question/3'
before_url = 'https://match.yuanrenxue.cn/api2/3'
params = {
    "page": "3",
    "pageSize": "10",
    "kw": ""
}
sum = 0
for i in range(1, 6):
    params['page'] = str(i)
    with httpx.Client(http2=True, cookies=cookies, verify="charles.pem", proxy="http://127.0.0.1:8888") as client:
        response = client.get(before_url, headers=headers)
        response = client.get(url, headers=headers, params=params)
        for i in response.json()['data']:
            sum += i

print(sum)
