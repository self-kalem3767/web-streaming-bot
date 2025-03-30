import random
from DrissionPage import ChromiumPage, Chromium
from DrissionPage import ChromiumOptions
from DrissionPage.common import Settings
import requests, csv, time, json
from lxml.html import fromstring

def browser_setup():
    driver = ChromiumPage()
    return driver

def reads_user_creds():
    with open('creads.json', encoding='UTF-8') as file:
        userdata = json.load(file)
    return userdata

def random_account_pickup(data):
    credentials = random.choice(data)
    return credentials['usermail'], credentials['password']

def login_to_audiomack(driver, username, password):
    driver.get('https://audiomack.com/')
    driver.wait.load_start()
    signin_btn = driver.ele('xpath: //a/p[text() = "Sign In"]')
    signin_btn.click()
    time.sleep(1)
    driver.ele('xpath: //p[text() = "Continue with Email"]').click()
    time.sleep(1)
    login_mail = driver.ele('xpath: //input[@type="email"]')
    if login_mail:
        login_mail.input(username)
        driver.wait.load_start()
    continue_btn = driver.ele('xpath: //button[@type="submit"]')
    continue_btn.click()
    password_btn = driver.ele('xpath: //input[@type="password"]')
    password_btn.input(password)
    time.sleep(1)
    toggle_btn = driver.ele('xpath: //button[contains(@class, "FieldPasswordToggle")]')
    toggle_btn.click()
    time.sleep(2)
    submit_btn = driver.ele('xpath: //button[@type="submit"]')
    submit_btn.click()
    time.sleep(3)
    print(f'Login successful to account: {username}')

def get_and_stream_song(driver, song_link, username):
    login_check_status = driver.ele('xpath: //div[contains(@class, "NavbarRightItems")]//a/p[text() = "Sign In"]')
    if login_check_status:
        login_to_audiomack()
        time.sleep(2)

    main_tag = driver.ele('xpath: //div[@id="__next"]')
    
    driver.get(song_link)
    driver.wait.load_start()
    time.sleep(15)
    if main_tag:
        try: 
            song_play_btn = driver.ele('xpath: //div[contains(@class, "WaveformPlayer")]//button[contains(@class, "play-pause-button")]')
            if song_play_btn:
                song_play_btn.click()
            print(f'Song is streaming now for account: {username}')
        
        except Exception as err:
            print(f'Error while playing song: {username} - {err}')
            return

        time_sec = 60
        song_timing = driver.ele('xpath: //div[contains(@class, "WaveformPlayer")]//button[contains(@class, "play-pause-button")]/../..//following-sibling::div//span[2]').text.strip()
        f_part = song_timing.split(':')[0]
        s_part = song_timing.split(':')[1]
        song_stream_duration = int(f_part) * time_sec + int(s_part) - random.randint(1, 10)
        print(f'Sreaming for {song_stream_duration} from Account: {username})')
        time.sleep(song_stream_duration)

def run():
    driver = browser_setup()
    userdata = reads_user_creds()
    username, password = random_account_pickup(userdata)
    login_to_audiomack(driver, username, password)
    song_link = input('Enter Song Link: ')
    get_and_stream_song(driver, song_link, username)
    driver.quit()
    
    
if __name__ == "__main__":
    run()