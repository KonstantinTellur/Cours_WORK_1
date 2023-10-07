from pprint import pprint
import json
import requests
import configparser
from tqdm import tqdm

class VKUser:
    def __init__(self):
        self.token = config['DEFAULT']['VK_TOKEN']
        self.vk_user_id = input('Введите свой ID пользователя VK или короткое имя (screen_name): ')
        self.id_album = input("Введите ID альбома: ")
        self.count = input('Введите количество фотографий: ')
        self.photo_dict = {}

    def get_photo(self):
        URL = 'https://api.vk.com/method/users.get'
        params = {'access_token': self.token,
                  'user_ids': self.vk_user_id,
                  'v': 5.131}
        user = requests.get(URL, params=params).json()
        URL = 'https://api.vk.com/method/photos.get'
        params = {'owner_id': user['response'][0]['id'], 
                  'album_id': self.id_album,
                  'count': self.count,
                  'extended': 1,
                  'access_token': self.token,
                  'v': 5.131}
        vk_sizes = {'s': 1, 'm': 2, 'o': 3, 'p': 4, 'q': 5, 'r': 6, 'x': 7, 'y': 8, 'z': 9, 'w': 10}
        res_get_photo = requests.get(URL, params=params).json()
        if 'response'in res_get_photo:
            for file in res_get_photo['response']['items']:
                file_url = max(file['sizes'], key=lambda x: vk_sizes[x['type']])
                names = file['likes']['count']
                if names in self.photo_dict.keys():
                    self.photo_dict[f"{names}_{file['date']}"] =  file_url['url']
                else:
                    self.photo_dict[names] =  file_url['url']
        else:
            print("Отсутствует ключ 'response' в словаре res_get_photo.")
        return
        # res_get_photo = requests.get(URL, params=params).json()
        # for file in res_get_photo['response']['items']:
        #     file_url = max(file['sizes'], key=lambda x: vk_sizes[x['type']])
        #     names = file['likes']['count']
        #     if names in self.photo_dict.keys():
        #         self.photo_dict[f"{names}_{file['date']}"] =  file_url['url']
        #     else:
        #         self.photo_dict[names] =  file_url['url']
        # return
    
    def get_json(self, file):
        with open('result_json.json', 'w') as f:
            json.dump(file, f, ensure_ascii=False, indent=2)
         
class YandexDisk():
    def __init__(self, poligon):
        self.poligon = poligon

    def get_headers(self):
        
        return {
            'Content-Type': 'application/json',
            'Authorization': 'OAuth {}'.format(self.poligon)
        }           
    
    def create_get_folder(self, photo_dict):
        folder_name = input(f'Введите название папки Яндекс Диска для загрузки фото: ')
        url_disk = 'https://cloud-api.yandex.net/v1/disk/resources'
        headers = {'Content-Type': 'application/json', 'Authorization': f'OAuth {self.poligon}'}
        params_folder = {'path': folder_name}
        response_folder = requests.put(url_disk, params=params_folder, headers=headers)
        if response_folder.status_code == 409:
            flag = input('Папка с указанным названием уже существует. Желаете создать новую папку с другим именем? Введите да или нет: ')
            if flag.lower() == 'да'.lower():
                self.create_get_folder(photo_dict)
                return
            if flag.lower() == 'нет'.lower():
                print(f'Фотографии будут загружены в папку "{folder_name}".')
            else:
                print(f'Вы ввели некорректную команду. Работа программы будет прервана. Вернитесь к выбору названия папки.')    
                # self.create_get_folder(photo_dict)
                return
        upload_url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        headers = self.get_headers()
        for name, size in tqdm(photo_dict.items(), desc='Processing photos', unit='photo'):            
            params_upload = {'path': f'{folder_name}/{name}.jpg','url': size}
            response_upload = requests.post(upload_url, headers=headers, params=params_upload)   
        if response_upload.status_code == 202:
            print(f'Фотографии загружены в папку "{folder_name}".')
        else:
            print (f'Произошла ошибка.')    
            return   
            
if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('settings.ini')
    # config.sections()
    poligon = config['DEFAULT']['POLIGON_YA']
    vk = VKUser()
    vk.get_photo()
    vk.get_json(vk.photo_dict)
    ya = YandexDisk(poligon=poligon)
    ya.create_get_folder(vk.photo_dict)