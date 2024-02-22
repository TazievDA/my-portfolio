import vk_api


def get_user_photos(personal_token, search_id):
    vk = vk_api.VkApi(token=personal_token)
    try:
        photos = vk.method('photos.get', {'owner_id': search_id, 'album_id': 'profile', 'extended': 1})
        return photos.get('items')
    except vk_api.exceptions.VkApiError:
        return []


def get_top_photos_by_likes(personal_token, search_id):
    photos = get_user_photos(personal_token, search_id)
    photos.sort(key=lambda x: x.get('likes', {}).get('count'), reverse=True)
    return photos[0:3]


def get_photos_links(personal_token, search_id):
    photos = get_top_photos_by_likes(personal_token, search_id)
    links = []
    ids = []
    for photo in photos:
        links.append(photo.get('sizes')[-1].get('url'))
        ids.append(photo.get('id'))
    return list(zip(links, ids))
