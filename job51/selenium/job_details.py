import time
import re
import csv
import random
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver import Chrome
from selenium.webdriver import ChromeOptions

"""
    前程无忧的岗位详情爬取
    selenium：自动化爬取
"""
# option=Options()
# option.add_argument('--headless')
# driver = webdriver.Chrome(chrome_options=option)
option = ChromeOptions()
# option.add_argument('--disable-infobars')  # 不显示 chrome正受到自动测试软件的控制。
# option.add_argument('--no-sandbox')  # 解决DevToolsActivePort文件不存在的报错
# option.add_argument(
#     'user-agent="Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"')
option.add_experimental_option('excludeSwitches',['enable-automation'])
driver = Chrome(options=option)
driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
   'source': 'Object.defineProperty(navigator, "webdriver", {get: () => undefined})'
})
driver.get('https://www.51job.com/')
input = driver.find_element_by_xpath('//input[@id="kwdselectid"]')
keyword = '智能制造'
input.clear()
input.send_keys(keyword)
time.sleep(1)
driver.find_element_by_xpath('//div[contains(@class,"ush")]/button').click()
handle = driver.current_window_handle
time.sleep(5)
input2 = driver.find_element_by_xpath('//input[@id="jump_page"]')
input2.clear()
input2.send_keys('49')
time.sleep(1)
driver.find_element_by_class_name('og_but').click()
has_next = True
while has_next:
    time.sleep(random.uniform(5,10))
    list = driver.find_elements_by_xpath('//div[@class="j_joblist"]/div')
    for li in list:
        row = {}
        curr = li.find_element_by_xpath('//ul/li[@class="on"]/div').text
        print("-------current page is %s---------" % curr)
        print(driver.title)
        driver.implicitly_wait(2)
        time.sleep(1)
        links = li.find_element_by_xpath('./a').click()
        driver.switch_to.window(driver.window_handles[-1])
        print(driver.title)
        word = keyword
        if '滑动验证页面' in driver.title:
            wait = WebDriverWait(driver,10)
            source = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'.nc-container .nc_scale span')))
            # driver.find_elements_by_css_selector('#nc_1_n1z')
            box = driver.find_element_by_class_name('nc_scale')
            width = box.value_of_css_property('width')
            move_width =  re.findall(r'(.*?)px',width)[0]
            try:
                ActionChains(driver).drag_and_drop_by_offset(source, move_width, 0).perform()
                driver.refresh()
            except Exception:
                driver.refresh()
                continue
        else:
            try:
                time.sleep(random.uniform(1.5,3.5))
                position = driver.find_element_by_xpath('//div[@class="tBorderTop_box"]/div[contains(@class,"job_msg")]').text
                other = driver.find_element_by_xpath(
                    '//div[@class="tHeader tHjob"]/div[1]/div[1]').text.split('\n')
                print(other)
                temp=other[4].strip().split('|')
                print(temp)
                end=other[5:-1]
                ware=",".join(end)
                print(ware)
                file = open(
                    'C:/Users/85278/PycharmProjects/mySpider/scrapy_spider/job51/data/%s_positionDesc.csv' % keyword,
                    'a', encoding='gbk')
                ans=position.split('任职')
                writer = csv.DictWriter(file,
                                        fieldnames=['name', 'salary', 'cp_name', 'work_place', 'exp', 'edu', 'demand',
                                                    'pub-date', 'enjoin', 'position_desc','requirements'])
                writer.writerow({'name': other[0], 'salary': other[1], 'cp_name': other[2], 'work_place': temp[0], 'exp': temp[1], 'edu': temp[2], 'demand': temp[3], 'pub-date': temp[4],
                                'enjoin':ware,'position_desc': ans[0],'requirements':ans[1]})
                file.close()
            except Exception:
                position = ''
            time.sleep(random.uniform(2.5,4.5))
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
                   ##writer
            print(position)
    time.sleep(2)
    # driver.execute_script('window.scrollTo(0,6775)')
    next = driver.find_element_by_xpath('//ul/li[@class="next"]/a')
    if 'bk next' in next.get_attribute('class'):
        has_next = False
    else:
        next.click()
        time.sleep(5)
driver.quit()