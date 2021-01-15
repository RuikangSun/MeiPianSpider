import requests
import os
from urllib import request
from bs4 import BeautifulSoup

url = 'https://www.meipian.cn/3d7onlet'    # 默认爬取作者自拍照，你没看错，是自拍照
path = 'C:\\'    # 默认存C盘

def InputUrl():    # 获取输入的需要爬取的链接
    global url
    url = input('请输入目标美篇地址，例如“https://www.meipian.cn/3d7onlet”\n')
    
def InputPath(TargetPath = ''):    # 路径结尾无斜杠
    if TargetPath == '':
        TargetPath = input(r'请输入保存路径（结尾无斜杠）' + '\n')
    TargetPath = TargetPath + '\\'    # 为路径添加斜杠
    global path
    path = TargetPath
    return TargetPath

def GetText(TargetUrl = url):    # 获取TargetUrl链接对应的页面，若TargetUrl为空，则获取url页面
    global url 
    url = TargetUrl
    r = requests.get(url)
    r.encoding = 'utf-8'
    soup = BeautifulSoup(r.text,'html.parser')
    return soup    # 内容

def GetTitle(TargetUrl = url):    # 获取TargetUrl链接对应的标题，若TargetUrl为空，则获取url标题
    global url , title
    url = TargetUrl
    title = GetText(url).title.text    # 标题
    return title

def GetUrlList(TargetUrl = url):
    global url
    url = TargetUrl
    item = GetText(TargetUrl).find_all('img')
    #print(item)  
    UrlList = []
    RealImgCounter = 0    # 有用的图片计数器，包括内容等
    FakeImgCounter = 0    # 无用的图片计数器，包括美篇图标等
    for i in item:    # 美篇有两种图片地址形式，表现在HTML5中的两类代码
        if '-mobile' in str(i):    # “-mobile”结尾为有用的图片
            head1, sep1, tail1 = str(i).partition('src="')    # 去除HTML5格式
            head2, sep2, tail2 = tail1.partition('-mobile')    # 获取高清图片地址
            UrlList.append(head2)
            RealImgCounter += 1
        elif 'meipian-watermark' in str(i):    # “meipian-watermark”结尾也是有用的图片
            head3, sep3, tail3 = str(i).partition('show-img="')    # 去除HTML5格式
            head4, sep4, tail24 = tail3.partition('?meipian-watermark')    # 获取高清图片地址
            UrlList.append(head4)
            RealImgCounter += 1
        else:    # 剩下的就是没用的图片
            FakeImgCounter += 1
    return [UrlList, RealImgCounter, FakeImgCounter]    # 返回图片地址列表与图片计数器

def PrintTitle(TargetUrl = url):    # 打印输出标题
    global url
    url = TargetUrl
    print(GetTitle(url) + '\n')

def PrintResult(TargetUrl = url):    # 打印输出可读结果
    global url
    url = TargetUrl
    print('共找到' + str(GetUrlList(TargetUrl)[1] + GetUrlList(TargetUrl)[2]) + '张照片，其中有意义的照片共' + str(GetUrlList(TargetUrl)[1]) + '张。\n')

def SaveImg(TargetUrl = url , SaveLog = 0):    # 保存图片，可选保存日志
    global url, path
    url = TargetUrl
    if path:
        path = path + "\\{0}\\".format(GetTitle(TargetUrl))    # py文件路径创建文件夹，勿放桌面！
    else:
        path = os.getcwd() + "\\{0}\\".format(GetTitle(TargetUrl))    # py文件路径创建文件夹，勿放桌面！
    print(path)
    try:     # 尝试创建文件夹
        os.makedirs(path)
    except:
        print('创建文件夹失败')
    finally:    # 逐一保存图片
        i = 1
        if SaveLog == 1:    # 保存txt日志
            file = open('{0}\\URLS.txt'.format(path),'w',encoding='utf-8');
            for ImgUrl in GetUrlList(TargetUrl)[0]:
                file.write(ImgUrl + '\n');
            file.write('\n#标题：' + title + '\n')
            file.write('#来源：' + url + '\n')
            file.close();       
            print('已将图片地址保存在txt文件中')
            for ImgUrl in GetUrlList(TargetUrl)[0]:
                request.urlretrieve(ImgUrl, path + "\{0}.jpg".format(i))
                print('已下载{0}张图片中的第{1}张'.format(GetUrlList(TargetUrl)[1],i))
                i += 1
        else:
            for ImgUrl in GetUrlList(TargetUrl)[0]:
                request.urlretrieve(ImgUrl, path + "\{0}.jpg".format(i))
                print('已下载{0}张图片中的第{1}张'.format(GetUrlList(TargetUrl)[1],i))
                i += 1

def main():
    PrintTitle()
    PrintResult()
    SaveImg()

if __name__ == '__main__':
    main()