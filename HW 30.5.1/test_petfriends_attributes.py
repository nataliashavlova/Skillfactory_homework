import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture(autouse=True)
def driver():
    driver = webdriver.Chrome('C:/Users/shavl/PycharmProjects/webdriver/chromedriver.exe')
    # Переходим на страницу авторизации
    driver.get('https://petfriends.skillfactory.ru/login')
    # ЯВНОЕ ОЖИДАНИЕ ОТОБРАЖЕНИЯ ПОЛЕЙ EMAIL И ПАРОЛЯ НА СТРАНИЦЕ
    wait_email = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, 'email')))
    wait_pass = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, 'pass')))
    assert wait_email and wait_pass, "Поля формы логина не отображаются или страница слишком медленно грузится"
    # Вводим email
    driver.find_element(By.ID, 'email').send_keys('testik-test@testik.ru')
    # Вводим пароль
    driver.find_element(By.ID, 'pass').send_keys('test123')
    # Нажимаем на кнопку входа в аккаунт
    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()

    driver.maximize_window()
    yield driver

    driver.quit()


def test_show_all_pets(driver):
    """Этот тест проверяет, что на странице "все питомцы" все поля заполнены и все фото загружены"""
    # Проверяем, что мы оказались на главной странице пользователя
    assert driver.find_element(By.TAG_NAME, 'h1').text == "PetFriends"

    # Создаем переменные для наборов данных, найденных на странице
    # НЕЯВНЫЕ ОЖИДАНИЯ каждого элемента атрибутов питомцев
    driver.implicitly_wait(10)
    images = driver.find_elements(By.XPATH, '//div[@class="text-center align-self-center align-middle"]/img[@class="card-img-top"]')
    names = driver.find_elements(By.XPATH, '//div[@class="card-body"]/h5[@class="card-title"]')
    descriptions = driver.find_elements(By.XPATH, '//div[@class="card-body"]/p[@class="card-text"]')

    for i in range(len(names)):
        assert images[i].get_attribute('src') != ''
        assert names[i].text != ''
        assert descriptions[i].text != ''
        assert ", " in descriptions[i]
        parts = descriptions[i].text.split(", ")
        assert len(parts[0]) > 0
        assert len(parts[1]) > 0


def test_all_my_pets_are_displayed(driver):
    """Этот тест проверяет, что отображаемое количество питомцев в разделе "мои питомцы" совпадает
     с отображаемым на странице количеством питомцев"""
    # Переходим на страницу с моими питомцами
    driver.find_element(By.XPATH, '//*[@id="navbarNav"]/ul/li[1]/a').click()

    # Находим счетчик своих питомцев на сайте
    pets_number = driver.find_element(By.XPATH, '//div[@class=".col-sm-4 left"]').text.split('\n')[1].split(': ')[1]

    # ЯВНОЕ ОЖИДАНИЕ ПОЯВЛЕНИЯ ТАБЛИЦЫ С МОИМИ ПИТОМЦАМИ
    wait_table = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//table[@class="table table-hover"]')))
    assert wait_table, "Таблица с питомцами слишком долго грузится или не отображается"

    # Считаем отображаемых в таблице питомцев
    pets_count = len(driver.find_elements(By.XPATH, '//table[@class="table table-hover"]/tbody/tr'))

    # Проверяем, что счетчик питомцев на сайте равен вручную посчитанным питомцам
    assert int(pets_number) == pets_count

def test_at_least_half_of_pets_have_photo(driver):
    """Этот тест проверяет, что хотя бы у половины питомцев на странице "мои питомцы" есть фотография"""
    # Переходим на страницу с моими питомцами
    driver.find_element(By.XPATH, '//*[@id="navbarNav"]/ul/li[1]/a').click()

    # Находим счетчик своих питомцев на сайте
    pets_number = driver.find_element(By.XPATH, '//div[@class=".col-sm-4 left"]').text.split('\n')[1].split(': ')[1]

    # Находим всех своих питомцев с фото
    # ДОБАВЛЯЕМ НЕЯВНОЕ ОЖИДАНИЕ ПАРАМЕТРА ФОТО
    driver.implicitly_wait(10)
    pets_with_photo = driver.find_elements(By.XPATH, '//img[starts-with(@src, "data:image/")]')

    # Проверяем, что хотя бы половина моих питомцев - с фото
    assert int(pets_number)//2 <= len(pets_with_photo)

def test_all_pets_have_attributes(driver):
    """Этот тест проверяет, что у всех питомцев на странице "мои питомцы" заполнен
    каждый атрибут (возраст, имя, порода)"""
    # Переходим на страницу с моими питомцами
    driver.find_element(By.XPATH, '//*[@id="navbarNav"]/ul/li[1]/a').click()

    # Находим счетчик своих питомцев на сайте
    # С ДОБАВЛЕНИЕМ НЕЯВНОГО ОЖИДАНИЯ ОТОБРАЖЕНИЯ ИМЕНИ ПОЛЬЗОВАТЕЛЯ НА СТРАНИЦЕ КАК ИНДИКАТОРА ЗАГРУЗКИ БЛОКА С ДАННЫМИ АККАУНТА
    wait_acc_name = WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element((By.XPATH, '//div[@class=".col-sm-4 left"]'),"ufufufu"))
    assert wait_acc_name, "Страница 'Мои питомцы' слишком долго грузится или не отображается блок с информацией об аккаунте"
    pets_number = int(driver.find_element(By.XPATH, '//div[@class=".col-sm-4 left"]').text.split('\n')[1].split(': ')[1])

    # Собираем данные о моих питомцах в переменные по типу информации, собрав сначала все текстовые данные из таблицы
    # моих питомцев, и затем растащив их по отдельным переменным
    pet_names = []
    pet_breeds = []
    pet_ages = []
    pets_data = driver.find_elements(By.XPATH, '//tr/td[not(@class="smart_cell")]')

    # В цикле множитель и шаг 3, потому что у каждого питомца 3 текстовых поля, удовлетворяющих локатору xpath
    for i in range (0, pets_number*3-2, 3):
        pet_names.append(pets_data[i].text)
        pet_breeds.append(pets_data[i+1].text)
        pet_ages.append(pets_data[i+2].text)

    # Проверяем, что у всех питомцев есть имя, возраст и порода
    for i in range (0, pets_number):
        assert pet_names[i] != "" and pet_breeds[i] != "" and int(pet_ages[i])

def test_all_pets_have_unique_names(driver):
    """Этот тест проверяет, что каждый питомец на странице "мои питомцы" имеет уникальное имя"""
    # Переходим на страницу с моими питомцами
    driver.find_element(By.XPATH, '//*[@id="navbarNav"]/ul/li[1]/a').click()
    # Находим счетчик своих питомцев на сайте
    pets_number = int(driver.find_element(By.XPATH, '//div[@class=".col-sm-4 left"]').text.split('\n')[1].split(': ')[1])

    pet_names = []
    for i in range (1, pets_number+1):
        pet_names.append(driver.find_element(By.XPATH, f'//table[@class="table table-hover"]/tbody/tr[{i}]/td[1]').text)

    assert len(pet_names) == len(list(set(pet_names)))

def test_all_pets_attributes_are_unique(driver):
    """Этот тест проверяет, что в списке моих питомцев все из них имеют уникальный набор атрибутов,
    т.е. у них уникальное сочетание имени, породы и возраста"""
    # Переходим на страницу с моими питомцами
    driver.find_element(By.XPATH, '//*[@id="navbarNav"]/ul/li[1]/a').click()
    # Находим счетчик своих питомцев на сайте
    pets_number = int(driver.find_element(By.XPATH, '//div[@class=".col-sm-4 left"]').text.split('\n')[1].split(': ')[1])

    # Находим всех своих питомцев в таблице
    my_pets = list()
    duplicated_pets = list()
    pets_data = driver.find_elements(By.XPATH, '//tbody/tr[not(@scope="row" or @class="smart_cell")]')

    # В цикле множитель и шаг 3, потому что у каждого питомца 3 текстовых поля, удовлетворяющих локатору xpath
    for i in range (0, pets_number):
        parts = pets_data[i].text.replace('\n×', '').split('\t')
        if parts not in my_pets:
            my_pets.append(parts)
        else:
            duplicated_pets.append(parts)

    assert pets_number == len(my_pets), f'Среди питомцев есть дублирующиеся:\n{duplicated_pets}'