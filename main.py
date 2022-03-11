from multiprocessing import Pool
from time import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from pathlib import Path
import shutil
import os
import argparse


EXTENSION_PATH = lambda x: Path(f"User Data/User Data {x}/Default/Local Extension Settings/"
                                f"nkbihfbeogaeaoehlefnkodbefgpgknn")
PASSWORD = 'vFc9azMtqds7vFeg'
LINK = 'chrome-extension://nkbihfbeogaeaoehlefnkodbefgpgknn/home.html#initialize/welcome'


def run_process(profile):
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-data-dir={Path(os.getcwd(), 'User Data', f'User Data {profile}')}")
    driver = webdriver.Chrome(chrome_options=options)
    try:
        driver.get(LINK)
        wait = WebDriverWait(driver, 10)
        wait.until(ec.element_to_be_clickable((By.XPATH, '//button[text()="Начать работу"]'))).click()
        wait.until(ec.element_to_be_clickable((By.XPATH, '//button[text()="Создать кошелек"]'))).click()
        wait.until(ec.element_to_be_clickable((By.XPATH, '//button[text()="Я согласен"]'))).click()
        wait.until(ec.element_to_be_clickable((By.XPATH, '//input')))
        inputs = driver.find_elements(By.XPATH, '//input')
        inputs[0].send_keys(PASSWORD)
        inputs[1].send_keys(PASSWORD)
        driver.find_element(By.CSS_SELECTOR, '.first-time-flow__checkbox').click()
        driver.find_element(By.XPATH, '//button[text()="Создать"]').click()
        wait.until(ec.element_to_be_clickable((By.XPATH, '//button[text()="Далее"]')))
        driver.find_element(By.XPATH, '//button[text()="Далее"]').click()
        wait.until(ec.element_to_be_clickable(
            (By.XPATH, '//div[text()="Нажмите здесь, чтобы раскрыть секретные слова"]'))).click()
        phrase = driver.find_element(By.XPATH, '//div[@class="reveal-seed-phrase__secret-words notranslate"]').text
        with open(Path(os.getcwd(), 'result.txt'), 'a', encoding='utf-8') as f:
            f.write(phrase + '\n')
        phrase = phrase.split()
        driver.find_element(By.XPATH, '//button[text()="Далее"]').click()
        wait.until(ec.element_to_be_clickable((By.XPATH, '//div[@class="confirm-seed-phrase__selected-seed-words"]')))
        for word in phrase:
            driver.find_element(By.XPATH, f'//div[text()="{word}"]').click()
        driver.find_element(By.XPATH, '//button[text()="Подтвердить"]').click()
        wait.until(ec.element_to_be_clickable((By.XPATH, '//button[text()="Выполнено"]'))).click()
        print('Account is created')
    except Exception as e:
        print(e)
    finally:
        driver.close()
        driver.quit()

        path = EXTENSION_PATH(profile)
        for f in os.listdir(path):
            os.remove(Path(path, f))


def createProfiles(count):
    for n in range(1, count + 1):
        if os.path.exists(Path(os.getcwd(), 'User Data', f'User Data {n}')):
            shutil.rmtree(Path(os.getcwd(), 'User Data', f'User Data {n}'))
        shutil.copytree(Path(os.getcwd(), 'User Data', 'User Data'), Path(os.getcwd(), 'User Data', f'User Data {n}'))
        print(f"Profile {n} is created")


def rmProfiles(count):
    for n in range(1, count + 1):
        shutil.rmtree(Path(os.getcwd(), 'User Data', f'User Data {n}'))


def startReg(process_count):
    print('Copy Profiles')
    createProfiles(process_count)
    p = Pool(processes=process_count)
    print('Start process')
    while True:
        p.map(run_process, range(1, process_count + 1))


def main():
    process_count = int(input('Enter the number of processes: '))
    lab_count = int(input('Enter the number of labs: '))
    createProfiles(process_count)
    start_time = time()
    p = Pool(processes=process_count)
    p.map(run_process, range(1, process_count * lab_count + 1))
    end_time = time()
    elapsed_time = end_time - start_time
    print(f"Elapsed run time: {elapsed_time} seconds")
    rmProfiles(process_count)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--process', type=int, default=3)
    args = parser.parse_args()
    startReg(args.process)
    rmProfiles(args.proces)

