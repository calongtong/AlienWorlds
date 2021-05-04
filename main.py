# Auto Almost Everything
# Youtube Channel https://www.youtube.com/channel/UC4cNnZIrjAC8Q4mcnhKqPEQ
# Facebook Community https://www.facebook.com/autoalmosteverything
# Github Source Code https://github.com/autoalmosteverything?tab=repositories
# Please read README.md carefully before use

import time
import winsound
import urllib.parse as urlparse
from captcha import Captcha
from selenium import webdriver  # python -m pip install selenium
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from win10toast import ToastNotifier  # python -m pip install win10toast

# Browser config
chromedriver_path = '.\\chromedriver.exe'  # <-- Change to your Chrome WebDriver path, replace "\" with "\\".
opts = Options()
opts.binary_location = 'C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe'  # <-- Change to your Chromium browser path, replace "\" with "\\".
opts.add_experimental_option('excludeSwitches', ['enable-automation'])
opts.add_experimental_option('useAutomationExtension', False)
# opts.add_argument('--proxy-server=%s' % 'YourProxy')  # <-- Remove comment this line then replace 'YourProxy' by proxy string, such as 18.222.190.66:81.

browser = webdriver.Chrome(options=opts, executable_path=chromedriver_path)
browser.set_page_load_timeout(60)
browser.set_window_position(0, 0)
browser.set_window_size(854, 720)

autoCaptcha = False  # <-- Change to True if you want to use 2captcha to solve the captcha. I am working on it.
if autoCaptcha:
    # Replace by your 2Captcha API Key -->
    rc = Captcha('Your2CaptchaAPIKey')
    # <-- Replace by your 2Captcha API Key

# App config
app = 'Alien Worlds'
loginPath = 'https://all-access.wax.io'
gamePath = 'https://play.alienworlds.io'

waxio_cookies = [
    {
        'name': 'token_id',
        # Replace by your token id -->
        'value': 'YourTokenId',
        # <-- Replace by your token id
        'domain': 'all-access.wax.io',
        'path': '/',
    },
    {
        'name': 'session_token',
        # Replace by your session token -->
        'value': 'YourSessionToken',
        # <-- Replace by your session token
        'domain': '.wax.io',
        'path': '/',
    },
]


# Notification
def Notification(app, content):
    try:
        toast = ToastNotifier()
        toast.show_toast(app, content, duration=6)
    except:
        pass


# Draw on canvas
def CanvasDraw(xoffset, yoffset):
    canvas = browser.find_element_by_xpath("//canvas[contains(@id, '#canvas')]")
    action = ActionChains(browser)
    action.move_to_element(canvas)
    action.move_by_offset(xoffset=xoffset, yoffset=yoffset)
    action.click()
    action.perform()


# Claim TLM
def ClaimTLM():
    # Login
    browser.get(loginPath)
    time.sleep(1)
    for cookie in waxio_cookies:
        browser.delete_cookie(cookie['name'])
        browser.add_cookie(cookie)
    browser.get(loginPath)
    time.sleep(1)

    # Claim TLM
    browser.get(gamePath)
    time.sleep(16)
    CanvasDraw(0, 90)  # Click to Login button
    time.sleep(24)
    while True:
        try:
            CanvasDraw(270, -100)  # Click to Mine button
            time.sleep(4)
            CanvasDraw(0, 190)  # Click to Mine button
            time.sleep(240)
            CanvasDraw(0, 50)  # Click to Claim button
            time.sleep(8)

            # Claim page --->
            backPage = browser.current_window_handle
            if len(browser.window_handles) > 1:
                target_tag = None
                for handle in browser.window_handles:
                    if handle != backPage:
                        browser.switch_to.window(handle)
                        if loginPath in browser.current_url:
                            target_tag = handle
                            break
                browser.switch_to.window(target_tag)

            if autoCaptcha:
                while True:
                    try:
                        recaptcha = browser.find_element_by_xpath("//iframe[contains(@title, 'reCAPTCHA')]")
                        sitekey = ''
                        for query in urlparse.urlparse(recaptcha.get_attribute('src')).query.split('&'):
                            if 'k=' in query:
                                sitekey = query.split('=')[1]
                        token = rc.reCaptcha(sitekey, browser.current_url)
                        # TODO
                        # this.___grecaptcha_cfg.clients[0].C.C.callback
                        # browser.execute('___grecaptcha_cfg.clients[0].C.C.callback("%s")' % token)
                        # print('tracking')
                        break
                    except:
                        pass
                    time.sleep(1)
            else:
                winsound.Beep(999, 500)
                Notification(app, 'Please solve captcha!')
                time.sleep(90)

            browser.switch_to.window(backPage)
            # <--- Claim page

            time.sleep(60)
            CanvasDraw(190, 170)  # Click to Home button
        except Exception as ex:
            print('%s has exception:\n%s!' % (app, ex))
            Notification(app, '%s has exception:\n%s!' % (app, ex))
        finally:
            time.sleep(180)


ClaimTLM()
browser.quit()

# Please Like Facebook, Subscribe to Youtube channel, Give stars to Git repositories to support us!
# Contact me: autoalmosteverything.2021@gmail.com
