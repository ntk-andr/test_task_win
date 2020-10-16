import json

import redis
import zbar
import zbar.misc


def imread(image_filename):
    '''Example image-reading function that tries to use freeimage, skimage, scipy or pygame to read in an image'''

    try:
        from freeimage import read as read_image
    except ImportError:
        read_image = None

    if read_image is None:
        try:
            from skimage.io import imread as read_image
        except ImportError:
            pass

    if read_image is None:
        try:
            from scipy.misc import imread as read_image
        except ImportError:
            pass

    if read_image is None:
        try:
            import pygame.image
            import pygame.surfarray

            def read_image(image_filename):
                image_pygame_surface = pygame.image.load(image_filename)
                return pygame.surfarray.array3d(image_pygame_surface)
        except ImportError:
            raise ImportError('for this example freeimage, skimage, scipy, or pygame are required for image reading')

    image = read_image(image_filename)
    if len(image.shape) == 3:
        image = zbar.misc.rgb2gray(image)
    return image


def get_info_barcode(image_filename: str):
    scanner = zbar.Scanner()
    with open(image_filename, 'rb') as image:
        image_as_numpy_array = imread(image)
        results = scanner.scan(image_as_numpy_array)
        if not results:
            return {
                'data': 'Штрихкод не найден'
            }
        for result in results:
            result = {
                'type': result.type,
                'data': result.data.decode('ascii'),
                'quality': result.quality
            }
            # print(result)
            return result
            # return f"type: {result.type}, data: {result.data.decode('ascii')} quality: {result.quality}"


def save_in_redis(hash_key, fields: dict, r: redis):
    key = list(fields)[0]
    value = list(fields.values())[0]
    try:
        r.hset(hash_key, key, value)
    except Exception as ex:
        print(ex)
        print(hash_key)
        print(key)
        print(value)


def get_info_from_redis(hash_key, r: redis):
    return r.hgetall(hash_key)


def get_chat_id(chat_id, postfix):
    return f'{chat_id}_{postfix}'


if __name__ == '__main__':
    image_path = f'./images/134261293-1602688344-file_13.jpg'
    get_info_barcode(image_filename=image_path)
