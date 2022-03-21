#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Гайд по скачиванию картинок: https://towardsdatascience.com/image-scraping-with-python-a96feda8af2d
# Док. Selenium: https://www.selenium.dev/selenium/docs/api/py/index.html
# Google Search Parameters: https://moz.com/blog/the-ultimate-guide-to-the-google-search-parameters

import requests

from pathlib import Path
from selenium import webdriver


def scroll_to_end(wd):
    wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    
    
def load_more_button(wd):
    try:
        more_button = wd.find_element_by_css_selector(".mye4qd")
        more_button.click()
    except Exception:
        pass
    

def search_images(wd:webdriver, query:str, limit_images:int):
    """
    wd: объект webdriver (Selenium)
    query: поисковой запрос
    limit_images: количество картинок для скачивания
    """

    # построение url к google
    search_url = "https://www.google.com/search?safe=off&tbm=isch&q={q}&sclient=img"
    wd.get(search_url.format(q=query))
    
    # поиск картинок
    image_urls = set()
    image_count = 0
    results_start = 0
    
    while image_count < limit_images:
        # скролим вниз страницы
        scroll_to_end(wd)
        # найденные картинки
        raw_images = wd.find_elements_by_css_selector("img.Q4LuWd")
        number_results = len(raw_images)

        for img in raw_images[results_start:number_results]:
            # кликаем на каждую картинку
            try:          
                img.click()
            except Exception:
                continue
                
            # извлекаем и сохраняем ссылку на картинку
            actual_images = wd.find_elements_by_css_selector('img.n3VNCb')
            for actual_image in actual_images:
                url = actual_image.get_attribute('src')
                if url and url.startswith('http'):
                    image_urls.add(url)
                    
            # проверка выхода из цикла
            image_count = len(image_urls)
            if image_count >= limit_images:
                break
        else:
            # кликаем по кнопке "еще картинки" если она есть
            load_more_button(wd)
        
        # смещаем положение начальной точки среза 
        results_start = number_results
    return list(image_urls)[:limit_images]


def downoload_image(folder_path:str, url:str, num:int):
    """
    folder_path: путь сохранения картинки
    url: url-адрес картинки для скачивания
    num: номер картинки 
    """
    try:
        image_content = requests.get(url).content 
        file_path = folder_path / f'image_{num}.jpg'
  
        with open(file_path, 'wb') as f:
            f.write(image_content)
            
    except Exception as e:
        print(f"ОШИБКА - не загружается {url} - {e}")
     
    
def search_and_download_images(search_term:str, driver_path:str, target_path='./images', limit_images=5):
    """
    search_term: поисковой запрос к google.com
    driver_path: путь к драйверу браузера
    target_path: папка куда сохраняются картинки
    limit_images: количество скачиваемых картинок
    """
    # Создание путей для сохранения картинок
    target_folder = Path(target_path) / search_term

    if not target_folder.exists():
        Path.mkdir(target_folder, parents=True)
        
    # поиск картинок в google с помощью Selenium
    with webdriver.Chrome(executable_path=driver_path) as wd:
        wd.implicitly_wait(3)
        list_urls = search_images(wd=wd, query=search_term, limit_images=limit_images)
        
    # сохранение картинок на компьютер
    for num, url in enumerate(list_urls, 1):
        downoload_image(folder_path=target_folder, url=url, num=num)
        
    print(f"{search_term}. Скачено {len(list(target_folder.glob('*.jpg')))}/{len(list_urls)}")
    print('-' * 50)  
    
if __name__ == '__main__':
    queries = ['Кэтрин Лэнгфорд']
    for q in tqdm(queries):
        search_and_download_images(search_term=q, driver_path='./chromedriver.exe', target_path='./images', limit_images=5)