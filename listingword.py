#!usr/bin/python
# -*- coding: utf-8 -*-

import json
import os
from urllib.parse import quote

import requests
from bs4 import BeautifulSoup
from pydub import AudioSegment


class core():
    def __init__(self):
        self.word = ''

    def getHtml(self, word):
        self.word = word
        try:
            r = requests.get('http://www.iciba.com/'+self.word)
            return r.text
        except Exception as e:
            print(e)

    def getbs(self, html):
        bs = BeautifulSoup(html, 'lxml')
        return bs

    def getEN_mp3(self):

        # sound = bs.find_all(class_='new-speak-step')
        # sound_url = sound[1].get('ms-on-mouseover').split("'")
        # mp3 = requests.get(sound_url[1])
        url = 'https://dict.youdao.com/dictvoice?audio={word}&type=2'.format(
            word=self.word)
        mp3 = requests.get(url)
        with open('en.mp3', 'wb') as f:
            f.write(mp3.content)
            f.close()
            # print('download ok...')

    def getZH_translation(self, bs):
        # 获取中文解释
        tex = ''
        try:
            ul = bs.find(class_='base-list switch_part')
            if ul is None:
                print('[ERROR] {locate}没有找到翻译！'.format(locate=self.word))
                return '-1'  # 返回 -1 便于控制器统计未找到的翻译
            li = ul.find_all('li')
            for li2 in li:
                span = li2.p.find_all('span')
                for text in span:
                    tex += text.string
        except Exception as e:
            print(e)

        return tex

    def getZN_mp3(self, usrToken, text):
        cuid = 'taoxianpeng123'
        tok = str(usrToken)
        tex = text
        url = 'http://tsn.baidu.com/text2audio'
        # print(tok)
        get_mp3_url = url+'?tex=' + \
            quote(tex)+'&lan=zh&cuid='+cuid+'&ctp=1&tok='+tok

        zhmp3 = requests.get(get_mp3_url)

        with open('zh.mp3', 'wb') as f:
            f.write(zhmp3.content)
            f.close()
            # print('zh-mp3 download ok ...')

    def __getToken(self):
        # 获取token认证
        url_token = 'https://openapi.baidu.com/oauth/2.0/token'
        api_key = 'R26ZZakxixaQbIDGrPkUwOTc'
        secret_key = '10d76d90116385e126d95e1c277c538c'
        get_token_url = url_token+'?'+'grant_type=client_credentials&client_id=' + \
            api_key+'&client_secret='+secret_key
        token = requests.get(get_token_url)
        r = json.loads(token.text)
        # print(r['access_token'])
        return r['access_token']

    def combine(self, song1, song2, song3):
        if os.path.exists(song1+'.mp3') and os.path.exists(song2+'.mp3'):
            song1 = AudioSegment.from_mp3(song1+'.mp3')
            song2 = AudioSegment.from_mp3(song2+'.mp3')

            # db1 = song1.dBFS
            # db2 = song2.dBFS

            # dbplus = db1 - db2

            # if dbplus < 0:
            #     song1 += abs(dbplus)
            # elif dbplus > 0:
            #     song1 += abs(dbplus)

            song = song1 + song2
            song.export(song3+'.mp3', format='mp3')

            print('预合并完毕 ...')
            return '预合并完毕 ...'

    def combineToMP3(self, fileName):
        if not os.path.exists(fileName+'.mp3'):
            self.combine('en', 'zh', fileName)
        else:
            self.combine('en', 'zh', 'word')
            self.combine(fileName, 'word', fileName)
        print('合成完毕 ...')
        return('合成完毕 ...')

    def launch(self, word, fileName, zh):
        self.getEN_mp3()
        # zh = self.getZH_translation(bs)
        # 翻译从控制器中获取
        self.word = word
        token = self.__getToken()
        self.getEN_mp3()
        self.getZN_mp3(token, zh)
        self.combineToMP3(fileName)


if __name__ == '__main__':
    # one = core()
    # words = input('输入单词:').split(' ')
    # for word in words:
    #     html = one.getHtml(word)
    #     bs = one.getbs(html)
    #     one.getEN_mp3(bs)
    #     zh = one.getZH_translation(bs)
    #     token = one.getToken()
    #     one.getZN_mp3(token,zh)
    #     one.combineToMP3()
    pass
