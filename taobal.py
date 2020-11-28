# -*- coding:utf8 -*-
import re

from selenium import webdriver
from time import sleep
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

# 引入 ActionChains 类
from selenium.webdriver.common.action_chains import ActionChains
# 引入 Keys 模块
from selenium.webdriver.common.keys import Keys

import copy
dr = webdriver.Chrome()


# 登录
def login(data):
    WebDriverWait(dr, 10, 1).until(
        lambda the_driver: the_driver.find_element_by_id('fm-login-id').is_displayed()
    )
    account = dr.find_element_by_css_selector('#fm-login-id')
    account.send_keys(data['account'])
    dr.find_element_by_css_selector('#fm-login-password').send_keys(data['password'])

    dr.find_element_by_css_selector('.fm-button.fm-submit.password-login').click()

    # 存在滑块时
    check_slider()

    WebDriverWait(dr, 10, 1).until(
        lambda the_driver: the_driver.find_element_by_link_text('官方活动报名').is_displayed()  # 在父亲元件下找到link为Action的子元素
    )
    dr.find_element_by_link_text('官方活动报名').click()
    sleep(1)
    all_handles = dr.window_handles

    for handle in all_handles:
        if handle not in window_list.values():
            dr.switch_to.window(handle)
            window_list['active'] = handle
            star_active('2020天猫冬焕新')


# 验证滑块
def check_slider():
    if dr.find_element_by_css_selector('#login-error').is_displayed():
        el = dr.find_element_by_css_selector('#nc_1_n1z')
        # ------------鼠标滑动操作------------
        action = ActionChains(dr)
        # 第一步：在滑块处按住鼠标左键
        action.click_and_hold(el) \
            .move_by_offset(258, 0) \
            .release()
        # 执行动作
        action.perform()
    if dr.find_element_by_css_selector('.fm-button').is_displayed():
        dr.find_element_by_css_selector('.fm-button').click()


# 到达活动页之后
def star_active(link_name):
    WebDriverWait(dr, 10, 1).until(
        lambda the_driver: the_driver.find_element_by_link_text(link_name).is_displayed()
    )
    dr.find_element_by_link_text(link_name).click()
    all_handles = dr.window_handles
    for handle in all_handles:
        if handle not in window_list.values():
            dr.switch_to.window(handle)
            window_list['active_main'] = handle
            star_setup_price()


# 到达报价页面
def star_setup_price(): 
    WebDriverWait(dr, 10, 1).until(
        lambda the_driver: the_driver.find_element_by_xpath(
            '//div[@class="next-row"]/div/div[@class="next-col"]/div[@class="stepItem"]').is_displayed()
    )
    dr.find_element_by_xpath('//div[@class="next-row"]/div/div[@class="next-col"]/div[@class="stepItem"]/..').click()
    WebDriverWait(dr, 10, 1).until(
        lambda the_driver: the_driver.find_element_by_css_selector(
            'table tr th.next-table-header-node.first div.next-table-cell-wrapper').is_displayed()
    )
    a_links = dr.find_elements_by_css_selector('.next-table-body table tr td.first span a')
    for el in a_links:
        wares_quotation(el)


# 商品报价
def wares_quotation(el):
    el.click()
    all_handles = dr.window_handles
    for handle in all_handles:
        if handle not in window_list.values():
            dr.switch_to.window(handle)
            get_price(el)


# 获取价格
def get_price(el):
    data = {}
    a_links = dr.find_elements_by_css_selector(
        '#J_DetailMeta div.tm-clear div.tb-property div.tb-key dl.tb-prop.tm-sale-prop.tm-clear.tm-img-prop ul li')
    for a in a_links:
        text = a.get_attribute('title')
        pattern = re.compile(r'[【](.+)[】]', re.I)  # 查找【】里的内容
        text = re.findall(pattern, text)[0]
        if text not in data.keys():
            a.click()
            price = dr.find_element_by_css_selector("#J_PromoPrice > dd > div > span.tm-price").get_attribute(
                'textContent')
            data[text] = price
    fill_price(data, el)


# 填写价格
def fill_price(data, el):
    dr.close()
    dr.switch_to.window(window_list['active_main'])
    el.find_element_by_xpath('../../../../../..').find_element_by_css_selector('td.last button[type=button]').click()
    WebDriverWait(dr, 10, 1).until(
        lambda the_driver: the_driver.find_element_by_link_text('批量设置').is_displayed()
    )
    dr.find_element_by_link_text('批量设置').click()
    sleep(1)
    dr.find_element_by_css_selector("#plszZGPrice > span > div:nth-child(1) > div > label:nth-child(1)").click()
    dr.find_element_by_css_selector('#plszZGPrice button.next-btn-primary').click()
    sleep(1)

    for item in data.keys():
        trs = dr.find_elements_by_xpath("//td/*[contains(text(),'" + item + "')]/../..")
        for a in trs:
            c = a.find_element_by_css_selector('.sign-price input')
            dr.execute_script("arguments[0].scrollIntoView();", c)
            sleep(0.2)
            c.clear()
            sleep(0.2)
            c.send_keys(data[item])


# 打开网址
dr.get('https://www.taobao.com/')
window_list = {'home': dr.current_window_handle}
#
toLoginPage = dr.find_element_by_css_selector('#J_SiteNavLogin .site-nav-sign .h')
toLoginPage.click()

login({
    "account": "南极人淘友专卖店:豆芽",
    'password': "mbyd20140520yw"
})
