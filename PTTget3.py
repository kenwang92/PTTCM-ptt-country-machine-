import curses
import requests
import time
from bs4 import BeautifulSoup
import re

print('國家機器啟動')

class color:
    numless10 = '\033[32m'
    numuch10 = '\033[33m'
    numboom = '\033[31m'
    numx = '\033[33m'
    numrst = '\033[0m'

screen = curses.initscr()#初始化視窗
curses.curs_set(0)#光標不可見
screen.keypad(1)
h,w = screen.getmaxyx()
k = 0
curses.start_color()#初始化顏色
curses.init_pair(1,curses.COLOR_BLACK,curses.COLOR_WHITE)
curses.init_pair(2,curses.COLOR_GREEN,curses.COLOR_BLACK)#推文數小於10
curses.init_pair(3,curses.COLOR_YELLOW,curses.COLOR_BLACK)#推文數大於10
curses.init_pair(4,curses.COLOR_RED,curses.COLOR_BLACK)#爆文
curses.init_pair(5,curses.COLOR_BLUE,curses.COLOR_BLACK)#x...沒有灰色用藍色

r = requests.Session()#拿cookie

need = {
    'from':'/bbs/Gossiping/index.html',
    'yes':'yes'
}#因為用post所以要header

fake = r.post('https://www.ptt.cc/ask/over18?from=%2Fbbs%2FGossiping%2Findex.html',need)
soup = BeautifulSoup(fake.text,'html.parser')

global UPandDOWN
UPandDOWN = soup.find_all('a',{"class":"btn wide"})
UPnum = re.findall(r'\d+',str(UPandDOWN))#找出每次上一頁按鈕不同部份(不同部份在href中index後面的一串數字))
UPnum = UPnum[1]
global error
global error2
error = 0
error2 = 0
howto = '說明 上一頁(←) 下一頁(→) 離開(q) 標題抓取錯誤:{}個 推文數抓取錯誤:{}個'.format(error,error2)
top = '國家機器'
#記得抓第一頁
screen.attron(curses.color_pair(1))
screen.addstr(0,0,' ' * (w // 2 - 2))
screen.addstr(0,int(w // 2 - len(top)),top)
screen.addstr(0,int(w // 2 + len(top)),' ' * (w // 2 - len(top)))
screen.attroff(curses.color_pair(1))

for soup in soup.find_all('div',{"class":"r-ent"}):
    if soup.find('div','author').string == '-':#是否被刪文
        pass
    else:
        if soup.find('span'):#判斷有沒有得抓推文數,有的話抓推文數,標題和連結
            spanstr = soup.find('span').string
            if(spanstr.isdigit()):
                if (int(spanstr) < 10):#推文數小於10用綠色,大於用黃色
                    screen.attron(curses.color_pair(2))#添加顏色屬性
                    try:
                        screen.addstr('  {} '.format(soup.find('span').string))
                    except curses.error:
                        error2 += 1
                    screen.attroff(curses.color_pair(2))#關閉顏色屬性
                    #沒放try,會error,好像是字串太長,但放try可以顯示?
                    try:
                        screen.addstr('{} https://www.ptt.cc{}\n'.format(soup.find('a').string,soup.find('a')['href']))
                    except curses.error:
                        error += 1
                else:
                    screen.attron(curses.color_pair(3))#添加顏色屬性
                    try:
                        screen.addstr(' {} '.format(soup.find('span').string))
                    except curses.error:
                        error2 += 1
                    screen.attroff(curses.color_pair(3))#關閉顏色屬性
                    #沒放try,會error,好像是字串太長,但放try可以顯示?
                    try:
                        screen.addstr('{} https://www.ptt.cc{}\n'.format(soup.find('a').string,soup.find('a')['href']))
                    except curses.error:
                        error += 1
            else:#爆文或X...要紅色或灰色
                if (spanstr == '爆'):#推文數為爆用紅色,x..用灰色
                    screen.attron(curses.color_pair(4))#添加顏色屬性
                    try:
                        screen.addstr('爆 {} https://www.ptt.cc{}\n'.format(soup.find('a').string,soup.find('a')['href']))
                    except curses.error:
                        error2 += 1
                    screen.attroff(curses.color_pair(4))#關閉顏色屬性
                    #沒放try,會error,好像是字串太長,但放try可以顯示?
                    try:
                        screen.addstr('{} https://www.ptt.cc{}\n'.format(soup.find('a').string,soup.find('a')['href']))
                    except curses.error:
                        error += 1
                else:
                    screen.attron(curses.color_pair(5))#添加顏色屬性
                    try:
                        screen.addstr(' {} '.format(spanstr))
                    except curses.error:
                        error2 += 1
                    screen.attroff(curses.color_pair(5))#關閉顏色屬性
                    #沒放try,會error,好像是字串太長,但放try可以顯示?
                    try:
                        screen.addstr('{} https://www.ptt.cc{}\n'.format(soup.find('a').string,soup.find('a')['href']))
                    except curses.error:
                        error += 1
        else:
            try:
                screen.addstr('    {} https://www.ptt.cc{}\n'.format(soup.find('a').string,soup.find('a')['href']))
            except curses.error:
                error += 1
screen.attron(curses.color_pair(1))
screen.addstr(h-1,0,howto)
howlen = len(howto) + 24
screen.addstr(h-1,howlen,' ' * (w - 1 - howlen))
screen.attroff(curses.color_pair(1))
screen.refresh()
k = screen.getch()

def pttgetUP():
    global UPnum
    url = 'https://www.ptt.cc/bbs/Gossiping/index' + UPnum + '.html'
    global req
    req = r.get(url)
    global soup2
    soup2 = BeautifulSoup(req.text,'html.parser')
    global UPandDOWN
    UPandDOWN = soup2.find_all('a',{"class":"btn wide"})
    for c in soup2.find_all('div',{"class":"r-ent"}):
        if c.find('div','author').string == '-':#是否被刪文
            pass
        else:
            if c.find('span'):#判斷有沒有得抓推文數,有的話抓推文數,標題和連結
                spanstr2 = c.find('span').string
                if(spanstr2.isdigit()):
                    if (int(spanstr2) < 10):#推文數小於10用綠色,大於用黃色
                        screen.attron(curses.color_pair(2))#添加顏色屬性
                        try:
                            screen.addstr('  {} '.format(c.find('span').string))
                        except curses.error:
                            error2 += 1
                        screen.attroff(curses.color_pair(2))#關閉顏色屬性
                        #沒放try,會error,好像是字串太長,但放try可以顯示?
                        try:
                            screen.addstr('{} https://www.ptt.cc{}\n'.format(c.find('a').string,c.find('a')['href']))
                        except curses.error:
                            error += 1
                    else:
                        screen.attron(curses.color_pair(3))#添加顏色屬性
                        try:
                            screen.addstr(' {} '.format(c.find('span').string))
                        except curses.error:
                            error2 += 1
                        screen.attroff(curses.color_pair(3))#關閉顏色屬性
                        #沒放try,會error,好像是字串太長,但放try可以顯示?
                        try:
                            screen.addstr('{} https://www.ptt.cc{}\n'.format(c.find('a').string,c.find('a')['href']))
                        except curses.error:
                            error += 1
                else:#爆文或X...要紅色或灰色
                    if (spanstr2 == '爆'):#推文數為爆用紅色,x..用灰色
                        screen.attron(curses.color_pair(4))#添加顏色屬性
                        try:
                            screen.addstr(' 爆 ')
                        except curses.error:
                            error2 += 1
                        screen.attroff(curses.color_pair(4))#關閉顏色屬性
                        #沒放try,會error,好像是字串太長,但放try可以顯示?
                        try:
                            screen.addstr('{} https://www.ptt.cc{}\n'.format(c.find('a').string,c.find('a')['href']))
                        except curses.error:
                            error += 1
                    else:
                        screen.attron(curses.color_pair(5))#添加顏色屬性
                        try:
                            screen.addstr(' {} '.format(spanstr2))
                        except curses.error:
                            error2 += 1
                        screen.attroff(curses.color_pair(5))#關閉顏色屬性
                        #沒放try,會error,好像是字串太長,但放try可以顯示?
                        try:
                            screen.addstr('{} https://www.ptt.cc{}\n'.format(c.find('a').string,c.find('a')['href']))
                        except curses.error:
                            error += 1
            else:
                try:
                    screen.addstr('    {} https://www.ptt.cc{}\n'.format(c.find('a').string,c.find('a')['href']))
                except curses.error:
                    error += 1
    screen.attron(curses.color_pair(1))
    screen.addstr(h-1,0,howto)
    howlen = len(howto) + 24
    screen.addstr(h-1,howlen,' ' * (w - 1 - howlen))
    screen.attroff(curses.color_pair(1))
    screen.refresh()#寫入
    #取下次要用的按紐值
    global DOWNnum
    UPnum = re.findall(r'\d+',str(UPandDOWN))
    UPnum = UPnum[1]
    try:
        DOWNnum = re.findall(r'\d+',str(UPandDOWN))
        DOWNnum = DOWNnum[2]
    except IndexError:
        pass
    global k
    k = screen.getch()

def pttgetDOWN():
    global url
    global DOWNnum
    url = 'https://www.ptt.cc/bbs/Gossiping/index' + DOWNnum + '.html'
    global req
    req = r.get(url)
    global soup
    soup = BeautifulSoup(req.text,'html.parser')
    global UPandDOWN
    UPandDOWN = soup.find_all('a',{"class":"btn wide"})
    global c
    for c in soup.find_all('div',{"class":"r-ent"}):
        if c.find('div','author').string == '-':#是否被刪文
            pass
        else:
            if c.find('span'):#判斷有沒有得抓推文數,有的話抓推文數,標題和連結
                spanstr3 = c.find('span').string
                if(spanstr3.isdigit()):
                    if (int(spanstr3) < 10):#推文數小於10用綠色,大於用黃色
                        screen.attron(curses.color_pair(2))#添加顏色屬性
                        try:
                            screen.addstr('  {} '.format(c.find('span').string))
                        except curses.error:
                            error2 += 1
                        screen.attroff(curses.color_pair(2))#關閉顏色屬性
                        #沒放try,會error,好像是字串太長,但放try可以顯示?
                        try:
                            screen.addstr('{} https://www.ptt.cc{}\n'.format(c.find('a').string,c.find('a')['href']))
                        except curses.error:
                            error += 1
                    else:
                        screen.attron(curses.color_pair(3))#添加顏色屬性
                        try:
                            screen.addstr(' {} '.format(c.find('span').string))
                        except curses.error:
                            error2 += 1
                        screen.attroff(curses.color_pair(3))#關閉顏色屬性
                        #沒放try,會error,好像是字串太長,但放try可以顯示?
                        try:
                            screen.addstr('{} https://www.ptt.cc{}\n'.format(c.find('a').string,c.find('a')['href']))
                        except curses.error:
                            error += 1
                else:#爆文或X...要紅色或灰色
                    if (spanstr3 == '爆'):#推文數為爆用紅色,x..用灰色
                        screen.attron(curses.color_pair(4))#添加顏色屬性
                        try:
                            screen.addstr(' 爆 ')
                        except curses.error:
                            error2 += 1
                        screen.attroff(curses.color_pair(4))#關閉顏色屬性
                        #沒放try,會error,好像是字串太長,但放try可以顯示?
                        try:
                            screen.addstr('{} https://www.ptt.cc{}\n'.format(c.find('a').string,c.find('a')['href']))
                        except curses.error:
                            error += 1
                    else:
                        screen.attron(curses.color_pair(5))#添加顏色屬性
                        try:
                            screen.addstr(' {} '.format(spanstr3))
                        except curses.error:
                            error2 += 1
                        screen.attroff(curses.color_pair(5))#關閉顏色屬性
                        #沒放try,會error,好像是字串太長,但放try可以顯示?
                        try:
                            screen.addstr('{} https://www.ptt.cc{}\n'.format(c.find('a').string,c.find('a')['href']))
                        except curses.error:
                            error += 1
            else:
                try:
                    screen.addstr('    {} https://www.ptt.cc{}\n'.format(c.find('a').string,c.find('a')['href']))
                except curses.error:
                    error += 1
    screen.attron(curses.color_pair(1))
    screen.addstr(h-1,0,howto)
    howlen = len(howto) + 24
    screen.addstr(h-1,howlen,' ' * (w - 1 - howlen))
    screen.attroff(curses.color_pair(1))
    screen.refresh()#寫入
    #取下次要用的按紐值
    UPnum = re.findall(r'\d+',str(UPandDOWN))
    UPnum = UPnum[1]
    try:
        DOWNnum = re.findall(r'\d+',str(UPandDOWN))
        DOWNnum = DOWNnum[2]
    except IndexError:
        pass
    global k
    k = screen.getch()

def title():
    screen.clear()
    screen.attron(curses.color_pair(1))
    screen.addstr(0,0,' ' * (w // 2 - 2))
    screen.addstr(0,int(w // 2 - len(top)),top)
    screen.addstr(0,int(w // 2 + len(top)),' ' * (w // 2 - len(top)))
    screen.attroff(curses.color_pair(1))

while(k != ord('q')):#因為getch()返回的是unicode要轉回字元
    if(k == curses.KEY_LEFT):
        title()
        pttgetUP()
    elif(k == curses.KEY_RIGHT):
        title()
        pttgetDOWN()
curses.endwin()
curses.curs_set(1)
print('urlout錯誤: {}'.format(error))
print('numout錯誤: {}'.format(error2))
print('上一頁：',UPnum)
try:
    print('下一頁：',DOWNnum)
except NameError:
    pass