#!/usr/bin/env python3

import requests
import re
from bs4 import BeautifulSoup


s = requests.session()

base_url = 'http://zzzcks.guet.edu.cn'
dic = ['A', 'B', 'C', 'D']
answer_list1 = ['rbtl0', 'rbtl1', 'rbtl2', 'rbtl3', 'rbtl4', 'rbtl5', 'rbtl6', 'rbtl7', 'rbtl8', 'rbtl9', 'rbtl10', 'rbtl11', 'rbtl12', 'rbtl13', 'rbtl14', 'rbtl15', 'rbtl16', 'rbtl17', 'rbtl18', 'rbtl19', 'rbtl20', 'rbtl21', 'rbtl22', 'rbtl23', 'rbtl24', 'rbtl25', 'rbtl26', 'rbtl27', 'rbtl28', 'rbtl29', 'rbtl30', 'rbtl31', 'rbtl32', 'rbtl33', 'rbtl34', 'rbtl35', 'rbtl36', 'rbtl37', 'rbtl38', 'rbtl39', 'rbtl40', 'rbtl41', 'rbtl42', 'rbtl43', 'rbtl44', 'rbtl45', 'rbtl46', 'rbtl47', 'rbtl48', 'rbtl49']


def init_db():
    # get data from answer
    with open('answer.txt', 'r') as f:
        data = f.read()
    k = re.findall(r'\d+\.\d+、.+', data)
    v = re.findall(r':[A-Z]', data)
    # clear data
    k = [s[s.index('、')+1:] for s in k]
    v = [a[1:] for a in v]
    
    return dict(zip(k, v))


def login(url, username, password):
    r = s.get(base_url)
    soup = BeautifulSoup(r.text, 'html.parser')
    __VIEWSTATE = soup.find(id='__VIEWSTATE')['value']
    __VIEWSTATEGENERATOR = soup.find(id='__VIEWSTATEGENERATOR')['value']
    __EVENTVALIDATION = soup.find(id='__EVENTVALIDATION')['value']
    payload = {'__VIEWSTATE': __VIEWSTATE, '__VIEWSTATEGENERATOR': __VIEWSTATEGENERATOR, '__EVENTVALIDATION': __EVENTVALIDATION, 'TextBox1': username, 'TextBox2': password, 'ImageButton1.x': 39, 'ImageButton1.y': 25}

    r = s.post(url+'/login.aspx', data=payload, allow_redirects=False)
    #print("login code:", r.status_code)


def get_test():
    r = s.get(base_url+'/choice.aspx', allow_redirects=False)
    soup = BeautifulSoup(r.text, 'html.parser')
    __VIEWSTATE = soup.find(id='__VIEWSTATE')['value']
    __VIEWSTATEGENERATOR = soup.find(id='__VIEWSTATEGENERATOR')['value']
    __EVENTVALIDATION = soup.find(id='__EVENTVALIDATION')['value']
    payload = {'__VIEWSTATE': __VIEWSTATE, '__VIEWSTATEGENERATOR': __VIEWSTATEGENERATOR, '__EVENTVALIDATION': __EVENTVALIDATION, 'RadioButtonList1': 1, 'ImageButton1.x': 74, 'ImageButton1.y': 26}

    s.post(base_url+'/choice.aspx', data=payload, allow_redirects=False)
    r = s.get(base_url+'/test.aspx', allow_redirects=False)
    if r.status_code == 302:
        return ''
    else:
        return r.text


def get_score(payload1, html):
    soup = BeautifulSoup(html, 'html.parser')
    __VIEWSTATE = soup.find(id='__VIEWSTATE')['value']
    __VIEWSTATEGENERATOR = soup.find(id='__VIEWSTATEGENERATOR')['value']
    __EVENTVALIDATION = soup.find(id='__EVENTVALIDATION')['value']
    payload2 = {'ImageButton1.x': 67, 'ImageButton1.y': 39, '__VIEWSTATE': __VIEWSTATE, '__VIEWSTATEGENERATOR': __VIEWSTATEGENERATOR, '__EVENTVALIDATION': __EVENTVALIDATION}

    payload = dict(payload1, **payload2)
    headers = {"DNT": "1", "Referer": "http://zzzcks.guet.edu.cn/test.aspx", "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Mobile Safari/537.36"}
    s.post(base_url+'/test.aspx', data=payload, headers=headers, allow_redirects=False)
    r = s.get(base_url+'/Result.aspx', headers=headers, allow_redirects=False)
    soup = BeautifulSoup(r.text, 'html.parser')
    score = soup.find(id='lbl_score').string
    return int(score)


def auto_answer():
    login(base_url, '1500340227', '1500340227')
    html_doc = get_test()

    # The test is finished
    if html_doc == '':
        html_doc = s.get(base_url+'/result.aspx').text
        soup = BeautifulSoup(html_doc, 'html.parser')
        score = soup.find(id='lbl_score').string
        return int(score)
    # The test need to answer
    else:
        soup = BeautifulSoup(html_doc, 'html.parser')
        answer_list2 = []
        
        for td in soup.find_all('td'):
            q = td.find('font').get_text()
            q = q.strip()
            q = q[q.index('.')+1:]
            # search db
            answer = False
            for key, value in db.items():
                if q in key:
                    answer_list2.append(value)
                    answer = True
                    break
            if not answer:
                with open('/dev/urandom', 'rb') as f:
                    rand = ord(f.read(1))
                answer_list2.append(dic[rand%4])

        answer_list = dict(zip(answer_list1, answer_list2))
        score = get_score(answer_list, html_doc)
        return score


if __name__ == "__main__":
    db = init_db()
    while True:
        score = auto_answer()
        if score >= 80:
            print("[+] Finished, your score is {}".format(score))
            exit()
