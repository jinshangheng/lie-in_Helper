import requests
import http.cookiejar as cookiejar
import yaml

class Opener:
    def __init__(self):
        with open("config.yml", encoding="utf-8") as f:
            config_dict = yaml.safe_load(f)
            self.username = config_dict["username"]
            self.password = config_dict["password"]
            self.user_agent = config_dict["user_agent"]
            self.url_login = config_dict["url_login"]
            self.url_target = config_dict["url_target"]
        self.session = requests.session()
        self.session.cookies = cookiejar.LWPCookieJar(filename="cookies.txt")

    def login(self):
        print(f"开始模拟登陆:{self.url_login}...")
        data = {
            "username": self.username,
            "password": self.password
        }
        headers = {
            "Referer": self.url_login,
            "User-Agent": self.user_agent
        }
        res = self.session.post(self.url_login, data=data, headers=headers)
        print(f"模拟登陆的状态码:{res.status_code}")
        print(f"text:{res.text}")
        self.session.cookies.save()

    def is_login(self):
        headers = {
            "Referer": self.url_login,
            "User-Agent": self.user_agent
        }
        res = self.session.get(self.url_target, headers=headers, allow_redirects=False)
        print(f"登陆状态:{res.status_code}")
        if res.status_code != 200:
            return False
        else:
            return True

    def access_target(self):
        headers = {
            "Referer": self.url_login,
            "User-Agent": self.user_agent
        }
        is_login = self.is_login()
        print(f"是否登陆:{is_login}")
        if is_login == False:
            print("cookies失效，或第一次登陆，重新登陆")
            print("登陆过程将自动进行...")
            self.login()
        self.session.cookies.load()
        res = self.session.get(self.url_target, headers=headers, allow_redirects=False)
        if res.status_code == 200:
            print("网课登陆成功")
        else:
            print(f"网课登陆失败，错误代码:{res.status_code}")

if __name__ == "__main__":
    opener = Opener()
    opener.access_target()
        