import os
import pytest

from api import PetFriends
from settings import valid_email, valid_password

pf = PetFriends()

def test_successful_adding_pet_photo_with_valid_data(pet_photo='images/cat03.jpg'):
    """Проверяем возможность добавления фотографии к профилю питомца без фото"""

    # Получаем ключ auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Добавляем нового питомца методом "без фото" (create_pet_simple) и затем добавляем к этому питомцу фото
    pf.create_pet_simple(auth_key, 'Бублик', 'Кот', 8)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    status, result = pf.add_photo_of_pet(auth_key, my_pets['pets'][0]['id'], pet_photo)

    # Проверяем, что статус ответа = 200 и в поле pet_photo ответа есть данные
    assert status == 200
    assert len(result['pet_photo']) > 0

def test_unsuccessful_get_api_key_with_invalid_password(email=valid_email, password = 'test'):
    """Проверяем, что запрос API ключа с корректным email и некорректным паролем возвращает ошибку 403
    и не возвращает сам ключ"""
    status, result = pf.get_api_key(email, password)

    # Проверяем, что сервер вернул ошибку 403 и не прислал ключ API (key)
    assert status == 403
    assert 'key' not in result

def test_unsuccessful_get_api_key_with_empty_data(email='', password=''):
    """Проверяем, что запрос API ключа с пустыми полями email и password возвращает ошибку 403
    и не возвращает сам ключ"""
    status, result = pf.get_api_key(email, password)

    # Проверяем, что сервер вернул ошибку 403 и не прислал ключ API (key)
    assert status == 403
    assert 'key' not in result

def test_unsuccessful_get_all_pets_with_invalid_key(filter=''):
    """Проверяем, что запрос списка всех питомцев с пустым API-ключом возвращает ошибку 403 и не возвращает
    список питомцев"""
    auth_key = {'key': ''}
    status, result = pf.get_list_of_pets(auth_key, filter)

    # Проверяем, что сервер вернул ошибку 403 и не прислал список питомцев
    assert status == 403
    assert 'pets' not in result

def test_unsuccessful_create_pet_without_photo_with_invalid_data(name=None, animal_type='Котопёс', age=10):
    """Проверяем, что при отправке в поле 'name' типа данных, отличного от string (например, None),
    сервер возвращает ошибку 400 и питомец не добавляется"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.create_pet_simple(auth_key, name, animal_type, age)

    # Проверяем, что статус ответа 400 и питомец не добавился
    assert status == 400
    assert 'animal_type' not in result

def test_add_photo_to_my_pet_with_photo(pet_photo = 'images/cat03.jpg', pet_photo_new='images/cat123.jpg'):
    """Проверяем возможность добавления фотографии к питомцу, у которого уже есть фото"""
    # Получаем ключ auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Получаем полный путь к двум изображениям питомца и сохраняем в переменные pet_photo и pet_photo_new
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    pet_photo_new = os.path.join(os.path.dirname(__file__), pet_photo_new)

    # Создаём нового питомца с фото pet_photo и затем пробуем добавить к этому питомцу новое фото pet_photo_new
    _, result = pf.add_new_pet(auth_key, 'Борис', 'Кот', '15', pet_photo)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    status, result_new = pf.add_photo_of_pet(auth_key, my_pets['pets'][0]['id'], pet_photo_new)

    # Проверяем, что статус ответа = 200 и фото питомца изменилось на новое
    assert status == 200
    assert result['pet_photo'] != result_new['pet_photo']

def test_unsuccessful_pet_creation_with_invalid_key(name = 'Фалафель', animal_type = 'Пёс', age = 0):
    """Проверяем, что при попытке создать питомца с пустым ключом API сервер вернет ошибку 403
    и не создаст питомца"""
    auth_key = {'key': ''}
    status, result = pf.create_pet_simple(auth_key, name, animal_type, age)

    # Проверяем, что статус ответа = 403 и питомец не был создан
    assert status == 403
    assert 'name' not in result

def test_unsuccessful_delete_self_pet_with_invalid_key():
    """Проверяем, что удалить своего питомца с пустым ключом API невозможно - сервер вернет ошибку 403
    и питомец не будет удален"""
    # Получаем ключ auth_key, запрашиваем список своих питомцев, создаем доп.переменную с пустым ключом авторизации
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    auth_key_invalid = {'key': ''}

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Киндер", "Попугай", "1", "images/cat123.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id первого питомца из списка и отправляем запрос на удаление питомца с пустым ключом auth_key
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key_invalid, pet_id)

    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем что статус ответа = 403 и в списке питомцев остался id питомца, которого мы пытались удалить
    assert status == 403
    assert my_pets['pets'][0]['id'] == pet_id



"""ДАЛЬШЕ ИДУТ ТЕСТЫ, КОТОРЫЕ ВЫЯВИЛИ БАГИ - СЕРВЕР ВЕДЕТ СЕБЯ НЕ ТАК, КАК ОЖИДАЛОСЬ ПО ДОКУМЕНТАЦИИ:
1) есть возможность изменять чужих питомцев
2) есть возможность удалять чужих питомцев
3) при создании питомца с файлом неподдерживаемого формата в качестве фото - нет ожидаемой ошибки 400, питомец создается, но без фото
4) при отправке пустого обязательного поля (возраст) питомец успешно создается, хотя ожидалась ошибка 400
5) при попытке добавить файл фото некорректного формата к питомцу без фото возвращает неописанную ошибку сервера 500 вместо ожидаемой 400
"""
@pytest.mark.xfail
def test_unsuccessful_update_info_of_not_self_pet(name='Булочкин', animal_type='Кот', age=8):
    """Проверяем, что невозможно внести изменения в питомца, который не в списке своих питомцев.
    Сервер должен вернуть ошибку 403 и изменения не должны быть внесены"""
    # Получаем ключ auth_key и запрашиваем список всех питомцев и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, all_pets = pf.get_list_of_pets(auth_key, "")
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    # Проверяем, что последний добавленный в all_pets питомец не принадлежит нам, и пробуем его изменить
    if all_pets['pets'][0] not in my_pets.values():
        pet_id = all_pets['pets'][0]['id']
        status, _ = pf.update_pet_info(auth_key, pet_id, name, animal_type, age)
    # иначе - берем первого с конца питомца и пробуем удалить его
    else:
        pet_id = all_pets['pets'][-1]['id']
        status, _ = pf.update_pet_info(auth_key, pet_id, name, animal_type, age)

    # Ещё раз запрашиваем список всех питомцев и проверяем, что питомец не был изменен
    _, all_pets = pf.get_list_of_pets(auth_key, "")

    assert status == 403
    assert name not in all_pets['pets'].values()

@pytest.mark.xfail
def test_unsuccessful_delete_of_not_my_pet():
    """Проверяем, что невозможно удалить не собственного питомца из списка all_pets - сервер
    должен вернуть ошибку 403"""
    # Получаем ключ auth_key и запрашиваем список всех питомцев и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, all_pets = pf.get_list_of_pets(auth_key, "")
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем, что последний добавленный в all_pets питомец не принадлежит нам, и пробуем его удалить
    if all_pets['pets'][0] not in my_pets.values():
        pet_id = all_pets['pets'][0]['id']
        status, _ = pf.delete_pet(auth_key, pet_id)
    # иначе - берем первого с конца питомца и пробуем удалить его
    else:
        pet_id = all_pets['pets'][-1]['id']
        status, _ = pf.delete_pet(auth_key, pet_id)

    # Ещё раз запрашиваем список всех питомцев и проверяем, что питомец не был удален
    _, all_pets = pf.get_list_of_pets(auth_key, "")

    assert status == 403
    assert pet_id in all_pets.values()

@pytest.mark.xfail
def test_unsuccessful_create_pet_with_invalid_photo_format(name='Батон', animal_type='Котик', age='5', pet_photo='images/data_.xls'):
    """Проверяем, что при добавлении питомца с файлом неподдерживаемого формата (не JPG, JPEG или PNG) сервер вернет
    ошибку 400 и питомец не будет добавлен"""

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Пытаемся добавить питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Ожидаем, что в ответе будет статус 400 и питомец будет добавлен без фото
    assert status == 400
    assert result['name'] == name

@pytest.mark.xfail
def test_unsuccessful_pet_create_with_empty_age_field(name='Дворняга', animal_type='Собака', age='', pet_photo='images/cat03.jpg'):
    """Проверяем, что питомец с пустым обязательным полем age не будет добавлен и сервер вернет ошибку 400"""

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 400
    assert name not in result

@pytest.mark.xfail
def test_unsuccessful_adding_pet_photo_with_invalid_data(pet_photo='images/data_.xls'):
    """Проверяем, что фото ненадлежащего формата (не JPG, JPEG или PNG) не будет добавлено
    в профиль питомца и сервер вернет ошибку 400"""

    # Получаем ключ auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Добавляем нового питомца методом "без фото" (create_pet_simple) и затем добавляем к этому питомцу фото
    pf.create_pet_simple(auth_key, 'Вазавадас', 'Кот', 666)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    status, result = pf.add_photo_of_pet(auth_key, my_pets['pets'][0]['id'], pet_photo)

    # Проверяем, что статус ответа = 400 и в поле pet_photo ответа данных нет
    assert status == 400
    assert len(result['pet_photo']) == 0