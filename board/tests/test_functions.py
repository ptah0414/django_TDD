
from django.test import TestCase
from selenium import webdriver
from selenium.webdriver.common.by import By



class TestModels(TestCase):
    def setUp(self):
        self.browser = webdriver.Chrome('c:/chromedriver.exe')

    def tearDown(self):
        self.browser.quit()

    def test_start_test(self):
        self.browser.get('http://127.0.0.1:8000/accounts/login/')
        id_input_tag = self.browser.find_element(By.XPATH, '/html/body/section/div/form/div[1]/div[2]/div[1]/input')
        pw_input_tag = self.browser.find_element(By.XPATH, '/html/body/section/div/form/div[1]/div[2]/div[2]/input')
        id_input_tag.send_keys('najeth120@naver.com')
        pw_input_tag.send_keys('qwer1234!')
        login_btn_tag = self.browser.find_element(By.ID, 'submitButton')
        login_btn_tag.click()

        register_btn_tag = self.browser.find_element(By.XPATH, '/html/body/nav/div/div/ul/li[3]/a')
        register_btn_tag.click()

        title_input_tag = self.browser.find_element(By.XPATH, '/html/body/section/div/form/div[1]/input')
        contents_input_tag = self.browser.find_element(By.XPATH, '/html/body/section/div/form/div[2]/div[3]/div[3]')
        register_btn_tag = self.browser.find_element(By.XPATH, '/html/body/section/div/form/div[3]/button')
        title_input_tag.send_keys('test')
        contents_input_tag.send_keys('test')
        register_btn_tag.click()

        main_btn_tag = self.browser.find_element(By.XPATH, '/html/body/nav/div/div/ul/li[1]/a')
        main_btn_tag.click()

        first_post = self.browser.find_element(By.XPATH, '/html/body/section/div/div[2]/div[1]/div/div')

        title = first_post.find_element(By.CLASS_NAME,'portfolio-caption-heading')
        writer = first_post.find_element(By.CLASS_NAME, 'portfolio-caption-subheading')

        self.assertEqual('test', title.text)
        self.assertEqual('najeth120', writer.text)
