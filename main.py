import wget
import os
import vk_api
import random
import re
import requests
import data
from urlopen import urllib
from urllib.parse import quote
from bs4 import BeautifulSoup
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.upload import VkUpload



class main1:

    session = vk_api.VkApi(token=data.TOKEN)

    longpoll = VkLongPoll(session)

    vk = session.get_api()

    upload = VkUpload(vk)


    def write_msg(self, user_id, message, attachment=None):
        self.session.method('messages.send', {'user_id': user_id, 'message': message, "attachment": attachment, 'random_id': random.randint(100000, 999999)})

    def get_messages_upload_server(self):
        r = self.session.method('photos.getMessagesUploadServer', {'peer_id': 0})
        return r['upload_url']

    def save_photo(self, url):
        try:
            os.remove('photo.png')
        except:
            pass
        filename = wget.download(url)
        os.rename(filename, 'photo.png')

        upload_url = self.get_messages_upload_server()
        file = {'file1': open('photo.png', 'rb')}
        ur = requests.post(upload_url, files=file).json()


        ph = self.session.method('photos.saveMessagesPhoto', {'photo': ur['photo'], 'server': ur['server'], 'hash': ur['hash']})
        attachment = 'photo' + str(ph[0]['owner_id'])+ '_' + str(ph[0]['id'])
        return attachment


    def remove_probels(self, string, symb):
        l = string.split()
        s = symb.join(l)
        return str(s)

    def trying(self, e_text, e_user_id):
        try:
            request = e_text
            mas = (self.session.method('users.get', {'user_ids': e_user_id, 'name_case': 'nom'}))
            name = mas[0].get('first_name')
            last_name = mas[0].get('last_name')
            print('[' + name + ' ' + last_name + '] : ' + str(request))
            self.write_msg(self, e_user_id, request)
        except vk_api.exceptions.ApiError:
            print('Error')

class parser_youtube:

    def start_youtube(self):
        mc = main1()
        while True:
            for event in mc.longpoll.listen():
                if event.type == VkEventType.MESSAGE_NEW:
                    if event.to_me:
                        claret = mc.remove_probels(str(event.text),'+')
                        mas = []
                        sq = 'https://www.youtube.com/results?search_query='+quote(claret)
                        print(sq)
                        doc = urllib.request.urlopen(sq).read().decode('cp1251', errors='ignore')
                        match = re.findall("\?v\=(.+?)\"", doc)
                        if not(match is None):
                            for ii in match:
                                if (len(ii) < 25):
                                    mas.append(ii)
                        mas = dict(zip(mas, mas)).values()
                        mas2 = []
                        for y in mas:
                            mas2.append('https://www.youtube.com/watch?v=' + y)
                        print(mas2)
                        mc.write_msg(event.user_id, 'This is first video on youtube for your request:')
                        mc.write_msg(event.user_id, mas2[0])
                        start_leasten()
                        break

class parser_photo:

    URL = 'https://yandex.by/images/search?text='
    HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0', 'accept': '*/*'}


    def start_photo(self):
        mc = main1()
        while True:
            for event in mc.longpoll.listen():
                if event.type == VkEventType.MESSAGE_NEW:
                    if event.to_me:
                        self.parse(mc.remove_probels(event.text, '%20'))
                        mc.write_msg(event.user_id, 'Your photo:', mc.save_photo(url_src))
                        start_leasten()
                        break


    def get_content(self, html):
        global url_src
        soup = BeautifulSoup(html, 'html.parser')
        items = soup.find_all('img', class_='serp-item__thumb justifier__thumb')
        str_item = str(items.pop(0))
        in1 = str_item.find('src')
        in2 = str_item.find('/>')
        url_src = 'https://'+str_item[in1+5:in2-10]


    def get_html(self, url, params=None):
        r = requests.get(url, headers=self.HEADERS, params=params)
        return r

    def parse(self, req):
        html = self.get_html(self.URL+req)
        if html.status_code == 200:
            self.get_content(html.text)
        else:
            print('ERROR')



def start_leasten():
    mc = main1()
    par_yt = parser_youtube()
    par_ph = parser_photo()
    while True:
        for event in mc.longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW:
                if event.to_me:
                    try:
                        request = event.text
                    except BaseException:
                        print('error for request')

                    if request == '/youtube':
                        mc.write_msg(event.user_id, 'Please write a request for youtube!')
                        par_yt.start_youtube()

                    if request == '/photo':
                        mc.write_msg(event.user_id, 'Please write the name of the photo!')
                        par_ph.start_photo()
                    else:
                        mc.write_msg(event.user_id, event.text)



if __name__ == '__main__':
    start_leasten()
