# -*- coding: utf-8 -*-
# __Author__: Sdite
# __Email__ : a122691411@gmail.com

from selenium import webdriver
from getpass import getpass
import time


class Mooc(object):

    def __init__(self, course_id=0, see_spooc=False):
        super(Mooc, self).__init__()
        self.mooc_url = 'https://www.icourse163.org/'       # 慕课账号
        self.see_spooc = see_spooc                          # 布尔值表示看spooc的课程还是mooc课程
        self.course_id = course_id                          # 看慕课中的第几门课程


    def get_login_info(self):
        self.user_name = str(input('请输入慕课账号: '))
        self.password = str(getpass('请输入密码: '))


    def login(self):
        self.driver.find_element_by_xpath(
            '//*[@id="j-slideTop-slideBox-wrapper"]/div/div/div[3]/div/div/div[3]').click()
        time.sleep(2)

        self.driver.switch_to_frame(self.driver.find_elements_by_tag_name('iframe')[0])           # 切换到登录的frame
        self.driver.find_element_by_xpath('//*[@id="cnt-box"]/div[2]/form/div/div[1]/a').click()  # 切换账号密码

        self.driver.find_element_by_xpath('//*[@id="phoneipt"]').send_keys(self.user_name)        # 输入账号
        time.sleep(0.1)
        self.driver.find_element_by_class_name('j-inputtext').send_keys(self.password)            # 输入密码
        self.driver.find_element_by_xpath('//*[@id="submitBtn"]').click()                         # 登录

        self.driver.switch_to_default_content()  # 切换回原来的frame
        time.sleep(1)

    def enter_course(self):
        # 进入我的课程
        self.driver.find_element_by_xpath(
            '//*[@id="j-slideTop-slideBox-wrapper"]/div/div/div[3]/div/div/div[3]/a/span').click()

        time.sleep(1)

        # 是否看的是spooc课程
        if self.see_spooc:
            self.driver.find_element_by_xpath('//*[@id="j-module-tab"]/div/div[2]').click()

        time.sleep(0.5)
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

    def see_video(self):
        # 看视频
        videos = self.driver.find_elements_by_css_selector('.f-icon.lsicon.f-fl')
        video_finish = True

        # 找到没看过的视频开始看视频
        for video in videos:
            title = video.get_attribute('title')
            class_ = video.get_attribute('class')

            if '视频：' in title and 'learned' not in class_:
                video.click()
                video_finish = False
                break

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

    # def do_test(self):
    #     test_finish = False
    #     while not test_finish:
    #         # 进入课件
    #         self.driver.find_element_by_xpath('//*[@id="j-courseTabList"]/li[5]').click()
    #         time.sleep(1.5)
    #         self.open_all_chapters()
    #
    #         tests = self.driver.find_elements_by_css_selector('.quiz')
    #         test_finish = True
    #         for test in tests:
    #             if 'icon-1' in test.find_elements_by_tag_name('div')[0].get_attribute('class'):
    #                 test.click()
    #                 self.driver.find_element_by_css_selector('.u-btn-primary').click()
    #                 test_finish = False
    #                 break
    #
    #         if test_finish:
    #             break
    #
    #         time.sleep(1)
    #
    #         questions = driver.find_elements_by_css_selector('.m-choiceQuestion')
    #         for question in questions:
    #             q = question.text.split('\n')
    #             question_text = q[2]

    def start_learning(self):
        self.driver.switch_to_window(self.driver.window_handles[0])

        # 进入课件
        self.driver.find_element_by_xpath('//*[@id="j-courseTabList"]/li[5]').click()
        time.sleep(1.5)

        self.open_all_chapters()                # 展开所有课程
        self.see_video()                        # 看视频
        # self.do_test()                          # 做题


    def run(self):
        self.get_login_info()                   # 获取登录账号
        self.driver = webdriver.Chrome()        # 打开浏览器
        self.driver.get(url=self.mooc_url)      # 打开慕课

        self.login()                            # 登录
        self.enter_course()                     # 进入课程
        self.start_learning()                   # 开始学习


if __name__ == '__main__':
    # 表示course_id看第一门课程, see_video_or_do_test=0表示看视频，1表示做题
    mooc = Mooc(course_id=0, see_spooc=True)
    mooc.run()
