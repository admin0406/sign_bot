import time

from selenium import webdriver

url = 'https://consumer.huawei.com/cn/'
br = webdriver.Chrome()
br.get(url)
br.maximize_window()
time.sleep(2)
br.refresh()
tx = br.find_elements_by_xpath('//ul[@class="clearfix nav-cnt"]/li/a')
for i in tx:
    print(i.get_attribute('title'))
