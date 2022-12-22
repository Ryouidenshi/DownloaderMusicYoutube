import getpass
import json
import os
import re
import sys
import youtube_dl

version = '1.6.1'
limit = 100000


def auth(cookies):
    if cookies is None:
        cookie_sid = getpass.getpass(
            prompt='Cookie:SID: <<-- https://music.youtube.com/ => DevTools => Application => Cookies => Value\n')
        if not cookie_sid:
            sys.exit("exit: empty cookie")
        cookie_hsid = getpass.getpass(prompt='Cookie:HSID:')
        if not cookie_hsid:
            sys.exit("exit: empty cookie")
        cookie_ssid = getpass.getpass(prompt='Cookie:SSID')
        if not cookie_ssid:
            sys.exit("exit: empty cookie")
        cookie_apisid = getpass.getpass(prompt='Cookie:APISID:')
        if not cookie_apisid:
            sys.exit("exit: empty cookie")
        cookie_sapisid = getpass.getpass(prompt='Cookie:SAPISID:')
        if not cookie_sapisid:
            sys.exit("exit: empty cookie")
        cookie_secure = getpass.getpass(prompt='Cookie:__Secure-3PAPISID:')
        if not cookie_secure:
            sys.exit("exit: empty cookie")
        cookie = '; '.join([
            'SID=' + cookie_sid,
            'HSID=' + cookie_hsid,
            'SSID=' + cookie_ssid,
            'APISID=' + cookie_apisid,
            'SAPISID=' + cookie_sapisid,
            '__Secure-3PAPISID=' + cookie_secure
        ])
    else:
        cookie = ''
        with open(cookies, 'r') as fp:
            for line in fp:
                if not re.match(r'^\#', line) and line.strip():
                    lf = line.strip().split('\t')
                    if cookie:
                        cookie += '; '
                    cookie += lf[5] + '=' + lf[6]
    with open(os.path.expanduser("~/.ymusic.json"), 'w') as f:
        json.dump({
            'User-Agent': 'Mozilla/5.0 (X11; CrOS aarch64 13020.54.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.77 Safari/537.36',
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.5',
            'Content-Type': 'application/json',
            'X-Goog-AuthUser': '0',
            'x-origin': 'https://music.youtube.com',
            'Cookie': cookie
        }, f)


def sync():
    os.system('adb push --sync ./* /sdcard/Music')


def download(id, title=None):
    SAVE_PATH = '/'.join(os.getcwd().split('/')[:3]) + '/Downloads'
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': SAVE_PATH + '/%(title)s.%(ext)s',
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        infoUrlGiven = ydl.extract_info("https://www.youtube.com/watch?v=" + id)

    if re.match(r"^https://", id):
        id = id.split('v=')[1].split('&')[0]
    if title is None:
        title = infoUrlGiven['title']

    print('[youtube-music] Starting: ' + title)

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download(['https://www.youtube.com/watch?v=' + id])


def main(command, path):
    if command in ('-h', '--help'):
        print('\n'.join([
            '-h                     Показать документацию',
            '--auth                 Авторизация',
            '--load-cookies FILE    Использовать куки-файлы',
            '-o                     Скачать песню',
        ]))
    elif command == '-o':
        download(path)
    elif command == '--load-cookies':
        auth(path)
    elif command == '--auth':
        auth(None)


def selectData():
    print('--------------------------------\n')
    print('Выберите функцию:\n'
          '1 - Скачать песню\n'
          '2 - Посмотреть документацию\n')
    print('--------------------------------\n')
    answer = input()
    if answer == '1':
        print('--------------------------------\n')
        print('ВВедите ссылку на песню\n')
        print('--------------------------------\n')
        path = input()
        splitedPath = path.split('=')
        main('-o', splitedPath[1])
    elif answer == '2':
        main('-h', '')
        selectData()
    else:
        print('--------------------------------\n')
        print('Такого варианта ответа нет, попробуйте ещё раз.\n')
        print('--------------------------------\n')
        selectData()


if __name__ == "__main__":
    selectData()
