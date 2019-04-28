from requests import Session

s = Session()

headers = {
    "accept": "application/json, text/javascript, */*; q=0.01",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7",
    "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
    "dnt": "1",
    "origin": "https://www.jufaanli.com",
    "referer": "https://www.jufaanli.com/usercenter_login",
    "user-agent": "jufaanli/3.0.1 (iPhone; iOS 10.3.2; Scale/2.00)v",
    "x-requested-with": "XMLHttpRequest",
}
url = "https://www.jufaanli.com/home/User/login"
checksum = "https://www.jufaanli.com/home/User/checksumUser"
checkin = "https://www.jufaanli.com/home/User/checkinLogin"

data = {
    "user": "17051800155",
    "password": "jufaanli",
    "is_remember": 1
}
res = s.post(url, headers=headers, data=data)
# check = s.post(checksum, headers=headers)
print(s.cookies)