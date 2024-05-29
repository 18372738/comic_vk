import os
import random
import requests
from urllib.parse import urljoin, urlsplit, unquote
from shutil import rmtree
from pathlib import Path
from environs import Env


def upload_comic_image(image_url, path):
    response = requests.get(image_url)
    with open(path, 'wb') as file:
        file.write(response.content)


def link_random_comic():
    number_of_comics = 2938
    random_number = random.randint(1, number_of_comics)
    url = f'https://xkcd.com/{random_number}/info.0.json'
    response = requests.get(url)
    response.raise_for_status()
    return response.json()





def get_upload_url_server(vk_token, group_id):
    url = 'https://api.vk.com/method/photos.getWallUploadServer'
    params = {
        'access_token': vk_token,
        'group_id': group_id,
        'v': 5.131,
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    server_link = response.json()['response']['upload_url']
    return server_link


def upload_image_server(server_link, path):
    with open(path, 'rb') as file:
        url = server_link
        files = {
            'photo': file,
            }
        response = requests.post(url, files=files)
        response.raise_for_status()
    return response.json()


def save_image_in_album(vk_token, group_id, photo, server, hash):
    url = 'https://api.vk.com/method/photos.saveWallPhoto'
    params = {
        'access_token': vk_token,
        'group_id': group_id,
        'photo': photo,
        'server': server,
        'hash': hash,
        'v': 5.131,
    }
    response = requests.post(url, params=params)
    response.raise_for_status()
    return response.json()


def upload_wall_image(vk_token, group_id, message, owner_id, media_id):
    url = 'https://api.vk.com/method/wall.post'
    params = {
        'access_token': vk_token,
        'owner_id': f'-{group_id}',
        'from_group': 0,
        'message': message,
        'attachments': f'photo{owner_id}_{media_id}',
        'v': 5.131,
    }
    response = requests.post(url, params=params)
    response.raise_for_status()
    return response.json()



if __name__ == '__main__':
    env = Env()
    env.read_env()

    vk_token = env.str('VK_TOKEN')
    group_id = env('GROUP_ID')


    Path('image').mkdir(parents=True, exist_ok=True)

    try:
        comic_link = link_random_comic()
        comic_comment = comic_link['alt']
        image_url = comic_link['img']
        path = urlsplit(image_url)
        filename = unquote(path.path).split('/')[-1]
        path = os.path.join('image/', filename)
        upload_comic_image(image_url, path)
        server_link = get_upload_url_server(vk_token, group_id)
        server = upload_image_server(server_link, path)

        photo_param = server['photo']
        server_param = server['server']
        hash_param = server['hash']
        link_image = save_image_in_album(vk_token, group_id, photo_param, server_param, hash_param)

        owner_id = link_image['response'][0]['owner_id']
        media_id = link_image['response'][0]['id']
        upload_wall_image(vk_token, group_id, comic_comment, owner_id, media_id)
    finally:
        rmtree('image')
