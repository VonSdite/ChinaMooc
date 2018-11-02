# -*- coding: utf-8 -*-
# __Author__: Sdite
# __Email__ : a122691411@gmail.com

from selenium import webdriver
from selenium.webdriver.support.select import Select
from getpass import getpass
import time


class Mooc(object):

    def __init__(self, course_id=0, see_spooc=True):
        super(Mooc, self).__init__()
        self.mooc_url = 'https://www.icourse163.org/'       # 慕课账号
        self.flash_open_url = 'chrome://settings/content/siteDetails?site=%s' % self.mooc_url # flash打开的链接
        self.see_spooc = see_spooc                          # 布尔值表示看spooc的课程还是mooc课程
        self.course_id = course_id                          # 看慕课中的第几门课程


    def run(self):
        try:
            self.get_login_info()  # 获取登录账号
            self.driver = webdriver.Chrome()  # 打开浏览器
            self.allow_flash()  # 允许使用flash
            self.driver.get(url=self.mooc_url)      # 打开慕课

            self.login()                            # 登录
            self.enter_course()                     # 进入课程
            self.start_learning()                   # 开始学习
        except:
            print('[失败]: 网络不稳定，请重试或更换网络')

    def allow_flash(self):
        def expand_shadow_element(element):
            shadow_root = self.driver.execute_script('return arguments[0].shadowRoot', element)
            return shadow_root

        # 打开chrome设置页面
        self.driver.get(self.flash_open_url)

        # 允许flash
        root1 = expand_shadow_element(self.driver.find_element_by_css_selector('body > settings-ui'))
        root2 = expand_shadow_element(root1.find_element_by_css_selector('#main'))
        root3 = expand_shadow_element(root2.find_element_by_css_selector('settings-basic-page'))
        root4 = expand_shadow_element(root3.find_element_by_css_selector('#advancedPage > settings-section.expanded > settings-privacy-page'))
        root5 = expand_shadow_element(root4.find_element_by_css_selector('#pages > settings-subpage > site-details'))
        root6 = expand_shadow_element(root5.find_element_by_css_selector('#plugins'))
        root7 = root6.find_element_by_css_selector('#permission')
        Select(root7).select_by_index(1)

    def get_login_info(self):
        self.user_name = str(input('请输入慕课账号: '))
        self.password = str(getpass('请输入密码: '))


    def login(self):
        self.driver.find_element_by_xpath(
            '//*[@id="j-slideTop-slideBox-wrapper"]/div/div/div[3]/div/div/div[3]').click()
        time.sleep(2)

        self.driver.switch_to.frame(self.driver.find_elements_by_tag_name('iframe')[0])           # 切换到登录的frame

        # 切换账号密码
        click_object = self.driver.find_element_by_css_selector('.u-tab.f-cb').find_element_by_css_selector('.tab0')
        self.driver.execute_script('arguments[0].click()', click_object)
        time.sleep(0.1)

        self.driver.find_element_by_xpath('//*[@id="phoneipt"]').send_keys(self.user_name)        # 输入账号
        time.sleep(0.3)
        self.driver.find_element_by_class_name('j-inputtext').send_keys(self.password)            # 输入密码
        self.driver.find_element_by_xpath('//*[@id="submitBtn"]').click()                         # 登录

        self.driver.switch_to.default_content()                                                   # 切换回原来的frame
        time.sleep(1.5)

    def enter_course(self):
        # 进入我的课程
        self.driver.find_element_by_xpath(
            '//*[@id="j-slideTop-slideBox-wrapper"]/div/div/div[3]/div/div/div[3]/a/span').click()

        time.sleep(1)

        # 是否看的是spooc课程
        if self.see_spooc:
            self.driver.find_element_by_xpath('//*[@id="j-module-tab"]/div/div[2]').click()

        time.sleep(1.3)
        # 打开课程
        self.driver.find_elements_by_xpath(
            '//*[@id="j-coursewrap"]/div/div[1]/div')[self.course_id].click()
        self.driver.close()
        time.sleep(1.5)

    def open_all_chapters(self):
        # 展开所有章节
        chapters = self.driver.find_elements_by_class_name('j-up')
        for chapter in chapters:
            try:
                chapter.click()
            except:
                pass

    def enter_not_learn(self, type):
        # 进入课件
        self.driver.find_element_by_xpath('//*[@id="j-courseTabList"]/li[5]').click()
        time.sleep(1.5)
        self.open_all_chapters()

        element = self.driver.find_elements_by_css_selector('.f-icon.lsicon.f-fl')

        # 找到没看过的视频开始看视频
        for e in element:
            title = e.get_attribute('title')
            class_ = e.get_attribute('class')

            if type in title and 'learned' not in class_:
                e.click()
                return False
        return True

    def see_video(self):
        video_finish = self.enter_not_learn(type='视频')

        if not video_finish:
            while True:
                try:
                    double_speed = self.driver.find_element_by_css_selector('.m-popover.m-popover-rate') \
                        .find_element_by_xpath('./ul/li[6]')
                    self.driver.execute_script('arguments[0].click()', double_speed)
                    break
                except:
                    pass

            while True:
                try:
                    try:
                        # 当看完视频时，才不会抛出异常，可以被直接break，否则不会break
                        self.driver.find_element_by_css_selector('.success.icon-成功')
                        break
                    except:
                        # 弹出选择问题解决
                        self.driver.find_element_by_css_selector('.u-btn.u-btn-default.submit.j-submit').click()
                        time.sleep(0.1)
                        self.driver.find_element_by_css_selector('.u-btn.u-btn-default.cont.j-continue').click()
                except:
                    time.sleep(3)
        print('[成功]: 视频已全看完(不一定包括直播)')

    def read_rich_text(self):
        while not self.enter_not_learn(type='富文本'):
            time.sleep(0.5)
        print('[成功]: 富文本已全看完')

    def read_document(self):
        while not self.enter_not_learn(type='文档'):
            while True:
                try:
                    time.sleep(10)  # 给flash足够的加载时间
                    box = self.driver.find_element_by_css_selector('.j-unitctBox.unitctBox')
                    self.driver.execute_script('arguments[0].style.height="100000px"', box)
                    break
                except:
                    pass

        print('[成功]: 文档已全看完')

    def start_learning(self):
        self.driver.switch_to.window(self.driver.window_handles[0])
        time.sleep(1)

        self.see_video()                        # 看视频
        self.read_rich_text()                   # 看富文本
        self.read_document()                    # 看文档


if __name__ == '__main__':
    # 表示course_id看第一门课程
    mooc = Mooc(course_id=0, see_spooc=True)
    mooc.run()
