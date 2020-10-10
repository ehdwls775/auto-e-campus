from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import re
import time
import json


class ec:
    URL = 'https://e-campus.gnu.ac.kr'
    URI_LECTURE = 'http://e-campus.gnu.ac.kr/lms/myLecture/doListView.dunet'
    URI_SCHEDULE = 'http://e-campus.gnu.ac.kr/lms/mypage/schedule/doListView.dunet'

    LECTURE_XPATH = '//*[@id="rows1"]/table/tbody/tr[{0}]/td[{1}]'
    LECTURE_TABLE_XPATH = '//*[@id="rows1"]/table/tbody/tr'

    driver = None
    logging = True
    name = 'Invalid E-Campus'
    wait_time = 0.2
    state = -1
    refresh_delay = 60

    schedule = []

    id = ''
    pw = ''

    def init_identification(self, username:str, password:str):
        self.id = username
        self.pw = password

    def get_state(self) -> str:
        if self.state == -1:
            return 'undefined'
        elif self.state == 0:
            return 'main'
        elif self.state == 1:
            return 'lectue_list'
        elif self.state == 2:
            return 'lecture_main'
        elif self.state == 3:
            return 'videos'
        else:
            return 'not implemented : ' + str(self.state)

    def set_state(self, state: str):
        if state == 'main':
            self.state = 0
        elif state == 'lecture_list':
            self.state = 1
        elif state == 'lecture_main':
            self.state = 2
        elif state == 'videos':
            self.state = 3
        else:
            self.state = 4

    def __init__(self, name, logging=True):
        self.name = name
        self.logging = logging

    def log(self, msg):
        if self.logging:
            print('{0}::{1}'.format(self.name, msg))

    def init_browser(self, headless):

        if not self.is_valid():
            self.release_browser()

        options = Options()
        options.add_argument("--disable-features=EnableEphemeralFlashPermission")
        options.add_argument("--window-size=480x720")
        options.add_argument("disable-gpu")

        if headless:
            options.add_argument("--headless")

        preferences = {
            "profile.default_content_setting_values.plugins": 1,
            "profile.content_settings.plugin_whitelist.adobe-flash-player": 1,
            "profile.content_settings.exceptions.plugins.*,*.per_resource.adobe-flash-player": 1,
            "PluginsAllowedForUrls": self.URL
        }
        options.add_experimental_option("prefs", preferences)

        self.driver = webdriver.Chrome("chromedriver", options=options)
        self.driver.implicitly_wait(1)

        return self.driver

    def create_browser(self):
        return self.init_browser(False)

    def create_headless_browser(self):
        return self.init_browser(True)

    def release_browser(self):
        if self.is_valid():
            self.driver.quit()

    def is_valid(self):
        return self.driver is not None

    def move_page(self, uri):
        self.driver.get(uri)
        self.driver.implicitly_wait(self.wait_time)
        self.log('move page to {0}'.format(uri))

        return self.driver.current_window_handle

    def open_main(self):
        self.set_state('main')
        return self.move_page(ec.URL)

    def sign_in(self):
        self.log('start sign in...')

        self.close_all_popups()

        self.driver.find_element_by_xpath('//*[@id="pop_login"]').click()
        self.driver.find_element_by_xpath('//*[@id="id"]').send_keys(self.id)
        self.driver.find_element_by_xpath('//*[@id="pass"]').send_keys(self.pw)
        self.driver.find_element_by_xpath('//*[@id="login_img"]').click()
        self.driver.implicitly_wait(self.wait_time * 5)

        self.close_all_popups()

        print('=' * 24)
        'document.querySelector("#header_top > div > span > strong")'

        # ele = self.safe_find_element_by_xpath('//*[@id="header_top"]/div/span/strong')
        ele = self.driver.find_element_by_css_selector('#header_top > div > span > strong')
        if ele is not None:
            name = ele.text.split(' ')[0]
            self.log('Welcome, {0}'.format(name))

        # ele = self.safe_find_element_by_xpath('//*[@id="header_top"]/div/span/span/span')
        ele = self.driver.find_element_by_css_selector('#header_top > div > span > span > span')
        if ele is not None:
            unread = int(ele.text)
            self.log('You have {0} unread message!'.format(unread))

        print('=' * 24)
        self.close_all_popups()

        self.driver.find_element_by_xpath('//*[@id="ko"]/img').click()
        self.driver.implicitly_wait(self.wait_time)

        self.close_all_popups()

    def open_lecture_list_page(self):
        self.move_page(ec.URI_LECTURE)
        self.close_all_popups()
        self.set_state('lecture_list')
        pass

    def close_popup(self, xpath):
        popup = self.safe_find_element_by_xpath(xpath, False)

        if popup is not None and popup.is_displayed():
            popup.click()

            self.driver.implicitly_wait(self.wait_time)
            self.log('pop up closed :: {0}'.format(xpath))

    def close_all_popups(self):
        self.close_popup('//*[@id="close_14260781"]/img')  # info
        self.close_popup('//*[@id="close_14277838"]/img')  # attendance notice
        self.close_popup('//*[@id="change_close"]/span')  # password change
        self.close_popup('//*[@id="close_14261406"]/img')  # mid term notice
        self.close_popup('//*[@id="close_18271279"]/img')  # manual for student
        self.close_popup('//*[@id="close_14297619"]/img')  # notice

    def safe_find_element_by_xpath(self, xpath, logging=True):
        try:
            web_element = self.driver.find_element_by_xpath(xpath)
            return web_element
        except:
            if logging:
                self.log('safe find : something is wrong at {0}.'.format(xpath))
            return None

    def safe_text_by_xpath(self, xpath):
        found = self.safe_find_element_by_xpath(xpath)
        if found is not None:
            return str(found.text)

        return 'not found'

    def get_lecture_count(self) -> int:
        return len(self.driver.find_elements_by_xpath(ec.LECTURE_TABLE_XPATH))

    def get_lecture_semester(self, index) -> str:
        return self.safe_text_by_xpath(ec.LECTURE_XPATH.format(index, 1))

    def get_lecture_college(self, index) -> str:
        return self.safe_text_by_xpath(ec.LECTURE_XPATH.format(index, 2))

    def get_lecture_association(self, index) -> str:
        return self.safe_text_by_xpath(ec.LECTURE_XPATH.format(index, 3))

    def get_lecture_name(self, index) -> str:
        return self.safe_text_by_xpath(ec.LECTURE_XPATH.format(index, 4))

    def get_lecture_online(self, index) -> str:
        return self.safe_text_by_xpath(ec.LECTURE_XPATH.format(index, 5))

    def get_lecture_professor(self, index) -> str:
        return self.safe_text_by_xpath(ec.LECTURE_XPATH.format(index, 6))

    def get_lecture_credit(self, index) -> float:
        return float(self.safe_find_element_by_xpath(ec.LECTURE_XPATH.format(index, 7)).text)

    def get_lecture_exam(self, index) -> str:
        return self.safe_text_by_xpath(ec.LECTURE_XPATH.format(index, 8))

    def get_lecture_parsed_name(self, index) -> (str, str):
        raw = self.get_lecture_name(index)
        spl = raw.split('\n ')
        return spl[0], spl[1]

    def move_to_lecture(self, index):
        link = self.safe_find_element_by_xpath(ec.LECTURE_XPATH.format(index, 9))

        if link is None:
            self.log('move_to_lecture : invalid lecture link')
            return None

        link.click()
        self.driver.implicitly_wait(2)
        self.set_state('lecture_main')

        portal = self.safe_find_element_by_xpath('//*[@id="leftSnb"]/li[3]/a')

        if portal is None:
            self.log('move_to_lecture : invalid lecture list')
            return None

        portal.click()
        self.driver.implicitly_wait(self.wait_time)
        self.set_state('lecture_list')

        return self.driver.current_window_handle

    def start_watch(self):

        is_watching_video = False

        # create schedule
        self.log('crawling lectures to build schedules...')
        self.open_lecture_list_page()

        self.log('lecture count : {0}'.format(self.get_lecture_count()))
        lecture_count = self.get_lecture_count()
        for i in range(1, lecture_count + 1):

            self.open_lecture_list_page()

            lecture_info = {'semester': self.get_lecture_semester(i), 'college': self.get_lecture_college(i),
                            'association': self.get_lecture_association(i), 'name': self.get_lecture_name(i),
                            'online': self.get_lecture_online(i), 'professor': self.get_lecture_professor(i),
                            'exam': self.get_lecture_exam(i), 'class_name': self.get_lecture_parsed_name(i)[0],
                            'class_code': self.get_lecture_parsed_name(i)[1],
                            'videos': [], }

            self.driver.implicitly_wait(1)
            self.move_to_lecture(i)
            table = self.driver.find_elements_by_xpath('//*[@id="con"]/table/tbody/tr')

            week = 0
            times = 1

            current_week = 0
            current_time = 0

            indexes = []

            # video info crawl logic
            for j in range(1, len(table) + 1):
                childs = self.driver.find_elements_by_xpath('//*[@id="con"]/table/tbody/tr[{0}]/td'.format(j))

                if len(childs) < 2:
                    week += 1
                    times = 1
                    continue
                else:
                    indexes.append(j)
                    times += 1

            vs = lecture_info['videos']
            lecture_name = lecture_info['class_name'].replace(' ', '').replace('[', '').replace(']', '')

            self.log('강의 보기 시작 : {0}'.format(lecture_name))

            # videos play logic
            for index in indexes:
                status_xpath = '//*[@id="con"]/table/tbody/tr[{0}]/td[5]'.format(index)
                status_text = self.safe_find_element_by_xpath(status_xpath).text

                attendance_admit_xpath = '//*[@id="con"]/table/tbody/tr[{0}]/td[3]'.format(index)
                atten_admit_text = self.safe_find_element_by_xpath(attendance_admit_xpath).text

                if status_text == '출석완료' or status_text == 'Complete':
                    self.log('already completed : [{0}] {1}'.format(lecture_name, atten_admit_text))
                    continue
                elif status_text == '' or status_text is None:
                    self.log('no video skip : [{0}] {1}'.format(lecture_name, atten_admit_text))
                    continue
                elif status_text == '결석':
                    self.log('outdated : [{0}] {1}'.format(lecture_name, atten_admit_text))
                    continue

                video_link_xpath = '//*[@id="con"]/table/tbody/tr[{0}]/td[6]/a[1]'.format(index)
                open_video = self.safe_find_element_by_xpath(video_link_xpath, False)

                if open_video is None or open_video.text != '강의보기':

                    self.log('비디오 링크가 없음: [{0}] {1}'.format(lecture_name, atten_admit_text))
                    continue
                else:
                    self.log('비디오 링크 : {0}'.format(open_video.text))

                hours_xpath = '//*[@id="con"]/table/tbody/tr[{0}]/th'.format(index)
                hours_element = self.safe_find_element_by_xpath(hours_xpath)

                if hours_element is None:
                    continue

                hours_text = str(hours_element.text)

                if hours_text[0] == '1':
                    current_week += 1

                current_time = int(hours_text[0])

                mw = self.driver.current_window_handle

                self.log('open video : [{0}] {1} {2}_{3}'.format(lecture_name, atten_admit_text,current_week, current_time))

                open_video.click()
                self.driver.implicitly_wait(1)
                self.driver.switch_to.window(mw)

                while True:
                    self.driver.refresh()
                    self.driver.implicitly_wait(1)

                    pt2 = self.safe_find_element_by_xpath(status_xpath)
                    if pt2 is None or pt2.text == '':
                        continue

                    if pt2.text == '출석완료' or pt2.text == '결석':
                        self.log('done! move to next video : [{0}] {1}'.format(lecture_info['class_name'], atten_admit_text))
                        break

                    self.log('progress : {0}'.format(pt2.text))
                    time.sleep(self.refresh_delay)

        self.log('scheduling done!')
        self.driver.quit()

    def get_addresses(self):
        is_watching_video = False

        # create schedule
        self.log('crawling lectures to build schedules...')
        self.open_lecture_list_page()

        self.log('lecture count : {0}'.format(self.get_lecture_count()))
        lecture_count = self.get_lecture_count()
        for i in range(1, lecture_count + 1):

            self.open_lecture_list_page()

            lecture_info = {'semester': self.get_lecture_semester(i), 'college': self.get_lecture_college(i),
                            'association': self.get_lecture_association(i), 'name': self.get_lecture_name(i),
                            'online': self.get_lecture_online(i), 'professor': self.get_lecture_professor(i),
                            'exam': self.get_lecture_exam(i), 'class_name': self.get_lecture_parsed_name(i)[0],
                            'class_code': self.get_lecture_parsed_name(i)[1],
                            'videos': [], }

            self.driver.implicitly_wait(1)
            self.move_to_lecture(i)
            table = self.driver.find_elements_by_xpath('//*[@id="con"]/table/tbody/tr')

            week = 0
            times = 1

            indexes = []

            # video info crawl logic
            for j in range(1, len(table) + 1):
                childs = self.driver.find_elements_by_xpath('//*[@id="con"]/table/tbody/tr[{0}]/td'.format(j))

                if len(childs) < 2:
                    week += 1
                    times = 1
                    continue
                else:
                    indexes.append(j)
                    times += 1

            vs = lecture_info['videos']

            self.log('start watching : {0}'.format(lecture_info['class_name']))

            json_name = lecture_info['class_name'].replace(' ', '').replace('[', '').replace(']', '')
            json_file_name = 'rtmp_{0}.json'.format(json_name)

            linkes = {}

            try:
                with open(json_file_name) as json_file_read:
                    linkes = json.load(json_file_read)
            except:
                pass

            current_week = 0
            current_time = 0

            # videos play logic
            for index in indexes:

                xxp = '//*[@id="con"]/table/tbody/tr[{0}]/td[5]'.format(index)
                pt = self.safe_find_element_by_xpath(xxp).text

                txp = '//*[@id="con"]/table/tbody/tr[{0}]/td[3]'.format(index)
                tt = self.safe_find_element_by_xpath(xxp).text

                # 링크가 없을 때 만
                if pt == '' or pt is None:
                    self.log('no video skip : [{0}] {1}'.format(lecture_info['class_name'], tt))
                    continue

                wxp = '//*[@id="con"]/table/tbody/tr[{0}]/td[6]/a[1]'.format(index)
                open_video = self.safe_find_element_by_xpath(wxp, False)

                if open_video is None:
                    self.log('no video link : [{0}] {1}'.format(lecture_info['class_name'], tt))
                    continue

                ttp = '//*[@id="con"]/table/tbody/tr[{0}]/th'.format(index)
                ttts = self.safe_find_element_by_xpath(ttp)

                if ttts is None:
                    continue

                ttt = str(ttts.text)

                if ttt[0] == '1':
                    current_week += 1

                current_time = int(ttt[0])

                # 키가 있는 경우는 스킵
                key = '{0}_{1}'.format(current_week, current_time)
                if key in linkes.keys() and linkes[key] != None and linkes[key] != '':
                    continue

                mw = self.driver.current_window_handle

                self.log('open video : [{0}] {1}'.format(lecture_info['class_name'], tt))

                # 열기
                open_video.click()
                self.driver.implicitly_wait(1)

                time.sleep(1)

                window_popup = self.driver.window_handles[1]
                self.driver.switch_to.window(window_popup)
                source = self.driver.page_source

                # convert to regex
                begin = str(source).find('rtmp://')
                end = str(source).find('media.mp4')

                key = '{0}_{1}'.format(current_week, current_time)
                link = source[begin:end + 9]

                if link is not None and len(link) > 0:
                    self.log('{0} : {1}'.format(key, link))
                    linkes[key] = link

                self.driver.switch_to.window(mw)

                time.sleep(1)


            with open(json_file_name, 'w') as json_file:
                json.dump(linkes, json_file, indent=4)

        self.log('scheduling done!')
        self.driver.quit()
