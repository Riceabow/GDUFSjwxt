import pandas
import pandas as pd
import requests
from bs4 import BeautifulSoup

# import execjs

session = requests.session()


def calculate_gpa(grade):
    grade = int(grade)
    if grade >= 90:
        return 4.0  # A+
    elif grade >= 85:
        return 3.7  # A
    elif grade >= 82:
        return 3.3  # A-
    elif grade >= 78:
        return 3.0  # B+
    elif grade >= 75:
        return 2.7  # B
    elif grade >= 72:
        return 2.3  # B-
    elif grade >= 68:
        return 2.0  # C+
    elif grade >= 65:
        return 1.7  # C
    elif grade >= 62:
        return 1.3  # C-
    elif grade >= 58:
        return 1.0  # D+
    else:
        return 0.0  # F


class jwxt:
    use_id = ''
    password = ''
    cookie = ''
    dataStr = ''
    encode = ''  # 如果需要加解密的话额外处理，广外这个教务系统没有加解密，明文传输的
    verify_code = ''
    df = pandas.DataFrame([])

    def __init__(self, id, psw):
        self.use_id = id
        self.password = psw

    def get_login_cookies(self):  # 获取全局cookies
        header = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
            "Cache-Control": "no-cache",
            "Host": "jxgl.gdufs.edu.cn",
            "Connection": "keep-alive",
            "Referer": "https://www.gdufs.edu.cn/",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0"

        }
        # url = "https://jxgl.gdufs.edu.cn/jsxsd/"
        url = "https://jxgl.gdufs.edu.cn/jsxsd/xk/LoginToXkLdap"
        response = session.get(url=url, headers=header, timeout=1000)  # ses已经获得了cookies
        self.dataStr = response.text
        # print("dataStr为：" + self.dataStr)
        self.fun_code()
        cookies = session.cookies.get_dict()  # 获得临时的cookies
        print(cookies)
        cookies = str(cookies).replace("{", '').replace("'", '').replace(":", '=').replace('}', '').replace(",", ";")
        cookies = cookies.replace(" ", '')
        self.cookie = cookies
        print('cookie为：' + cookies)
        return cookies

    # def get_js(self):  # python 调用JS加密 返回 加密后的结果，可以用execjs库直接运行对应加解密的js函数
    #     with open(r'教务系统加密.js', encoding='utf-8') as f:
    #         js = execjs.compile(f.read())
    #         return js.call('encode', self.dataStr, self.use_id, self.password)

    def fun_code(self):  # 获取验证码并保存到本地，返回验证码图片文件名
        url_verifycode = 'https://jxgl.gdufs.edu.cn/jsxsd/verifycode.servlet'
        cookie = {"Cookie": self.cookie}
        response = session.get(url_verifycode, cookies=cookie)
        with open('verifycode.jpg', 'wb') as f:
            f.write(response.content)
            f.close()
        return 'verifycode.jpg'

    def login(self):
        self.get_login_cookies()
        self.verify_code = input("请输入验证码：")
        # image = ReadImage()
        header = {

            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
            "Cache-Control": "no-cache",
            "Content-Length": "55",
            "Content-Type": "application/x-www-form-urlencoded",  # 接收类型
            "Cookie": self.cookie,
            "Host": "jxgl.gdufs.edu.cn",
            "Origin": "https://jxgl.gdufs.edu.cn",
            "Connection": "keep-alive",
            "Referer": "https://jxgl.gdufs.edu.cn/jsxsd/",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0"
        }
        PostData = {
            'USERNAME': self.use_id,
            'PASSWORD': self.password,
            'RANDOMCODE': self.verify_code
        }
        url = 'https://jxgl.gdufs.edu.cn/jsxsd/xk/LoginToXkLdap'
        msg = session.post(url, headers=header, data=PostData, timeout=1000)
        # 处理重定向 (前面的请求加上参数 allow_redirects=False)
        # if msg.status_code == 302:  # 检查是否发生重定向
        #     location = msg.headers['Location']  # 获取重定向的URL
        #     # 这里可以根据需要处理重定向的逻辑，例如再次发送请求到重定向后的URL
        #     # 或者保存重定向的URL以便后续使用
        #     print(f"发生重定向，重定向后的URL是: {location}")
        print(msg.url)
        print(msg.status_code)
        # print(msg.text)

    def QScoreList(self):
        header = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
            "Cache-Control": "no-cache",
            "Content-Length": "33",
            "Content-Type": "application/x-www-form-urlencoded",  # 接收类型
            "Cookie": self.cookie,
            "Host": "jxgl.gdufs.edu.cn",
            "Origin": "https://jxgl.gdufs.edu.cn",
            "Connection": "keep-alive",
            "Referer": "https://jxgl.gdufs.edu.cn/jsxsd/kscj/cjcx_query?Ves632DSdyV=NEW_XSD_XJCJ",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0"
        }
        PostData = {
            "kksj": "",
            "kcxz": "",
            "kcmc": "",
            "fxkc": 0,
            "xsfs": "all"
        }
        url = 'https://jxgl.gdufs.edu.cn/jsxsd/kscj/cjcx_list'
        msg = session.post(url, headers=header, data=PostData, timeout=1000)
        print(msg.url)
        # print(msg.status_code)
        self.dataStr = msg.text
        # print(msg.text)

    # 定义绩点计算函数

    def save_scores(self):
        data = []
        soup = BeautifulSoup(self.dataStr, 'html.parser')
        table = soup.find(id='dataList')

        Theader = table.find_all('th')
        head = [element.text.strip() for element in Theader]  #
        # data.append(head)

        rows = table.find_all('tr')  # 找到所有的行标签<tr>
        for row in rows:
            cols = row.find_all('td')  # 找到该行中的所有列标签<td>
            if cols:
                cols = [element.text.strip() for element in cols]  # 提取列数据并去除前后空格
                data.append(cols)  # 将列数据添加到列表中

        self.df = pd.DataFrame(data, columns=head)
        # 应用绩点计算函数到DataFrame的每一行
        self.df['绩点'] = self.df['成绩'].apply(calculate_gpa)
        self.df.to_csv('data/all_scores.csv', encoding="utf-8", index=False, header=True)


