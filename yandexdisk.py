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