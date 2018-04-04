#!usr/bin/python
# -*- coding: utf-8 -*-
# 控制器

from listingword import core
from exceltool import iosys
import time


def run():
    iof = iosys()
    one = core()
    words = iof.readExcel_en()
    translation = iof.readExcel_zh()
    fileName = time.strftime("%Y-%m-%d", time.localtime())

    tl = 0  # 统计 没有翻译的单词数量
    # 下载翻译
    if len(translation) == 0:
        for word in words:
            html = one.getHtml(word)
            bs = one.getbs(html)
            zh = one.getZH_translation(bs)
            if zh == '-1':
                tl += 1
            translation.append(zh)
            
        iof.writeExcel(translation)
        if tl > 0:
            print('[WARNING]: 有{num}个单词没有翻译,需要手动填写!'.format(num=tl))
            exit()

    for i in range(len(words)):
        if translation[i] == '-1':
            tl += 1

    if tl > 0:
        print('[WARNING]: 有{num}个单词没有翻译,需要手动填写!'.format(num=tl))
        exit()
    for i in range(len(words)):
        print(words[i], translation[i])
        one.launch(words[i], fileName+'-{num}'.format(num=(i//10)+1), translation[i])
        print('...............', ((i+1)/float('%.1f' % len(words)))*100, '%')


if __name__ == '__main__':
    run()
