# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from scrapy.http import Request
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from facebookcrawler.items import FacebookcrawlerItem
import time
import lxml.html
from selenium.webdriver.common.action_chains import ActionChains


import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import re
import urllib
import json

global email,password,locations
#email = 'muzamilqadir2@gmail.com'
#password = 'bsef07m00004'
#locations = "islamabad"

import Tkinter
import tkSimpleDialog

root = Tkinter.Tk()
email = tkSimpleDialog.askstring('Email', 'Please Enter Your Email:')
password = tkSimpleDialog.askstring('Password', 'Please Enter Your Password:')
locations = tkSimpleDialog.askstring('Locations', 'Comma separated values:')
print email
print password
print locations
root.withdraw()

class FacebookspiderSpider(scrapy.Spider):
    name = "facebookspider"
    allowed_domains = ["facebook.com"]
    start_urls = (
        'http://www.facebook.com/',
        )

    def parse(self, response):
        #driver = webdriver.Firefox()
        global email
        global password
        global locations
        #driver = webdriver.PhantomJS(executable_path='C://phantomjs-2.0.0-windows/bin/phantomjs.exe')
        driver = webdriver.PhantomJS()
        #driver = webdriver.Chrome()
        # driver = webdriver.Chrome('./chromedriver.exe')
		#driver = webdriver.Firefox()
        driver.get('https://www.facebook.com/')
        print "here"
        email_elem = driver.find_element_by_name("email")
        email_elem.send_keys(email)
        pass_elem = driver.find_element_by_name("pass")
        pass_elem.send_keys(password)
        pass_elem.send_keys(Keys.RETURN)
        print "hhere"
        time.sleep(5)
        #body = driver.find_element_by_tag_name("body")
        #body.send_keys(Keys.CONTROL + 't')
		
        driver.get("https://www.facebook.com/friends")
        pause = 3
        lastHeight = driver.execute_script("return document.body.scrollHeight")
        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(pause)
            newHeight = driver.execute_script("return document.body.scrollHeight")
            print "scrolling down"
            if newHeight == lastHeight:
                print "broken"
                break
            lastHeight = newHeight

        print("here after scrolling")
        friends = [x.get_attribute("href") for x in driver.find_elements_by_xpath("//div/div[@class='uiProfileBlockContent']/div/div/div/a")]
        locations = locations.split(",")
        sub_params = re.compile('\?.+')
        item = FacebookcrawlerItem()
        for friend in friends:
            # link = friend.get_attribute("href")
            body = driver.find_element_by_tag_name("body")
            body.send_keys(Keys.CONTROL + 't')
            driver.get(sub_params.sub("", friend)+'/about')
            time.sleep(2)
            html = driver.page_source
            lxml_html = lxml.html.fromstring(str(html))
            poslocations = lxml_html.xpath("//div[@data-overviewsection='places']/div//a/text()")
            for location in set(locations):
                for poslocation in set(poslocations):
                    if location in poslocation:
                        name = lxml_html.xpath('//title[@id="pageTitle"]/text()')
                        first_name = last_name = ''
                        if name:
                            name = re.sub('\(\w*\)','',str(name[0])).split()
                            first_name = name[0]
                            if len(name) >= 3:
                                first_name = ' '.join(name[0:1])
                            last_name = name[-1]
                        print first_name
                        print last_name
                        item['FirstName'] = first_name
                        item['LastName'] = last_name
                        # name = lxml_html.xpath('//span[@id="fb-timeline-cover-name"]/text()')
                        # print name
                        phone = lxml_html.xpath('//span[@dir="ltr"]/text()')
                        print phone
                        item['Phone'] = phone
                        email = lxml_html.xpath('//a[contains(text(),"@")]/text()')
                        print email
                        item['Email'] = email
                        print friend
                        item['PageUrl'] = friend
                        item['Location'] = location
                        yield item


        # location = "Lahore"        
        # for location in locations.split(","):
        #     driver.get("https://www.facebook.com/search/results/?init=quick&q={loc}".format(loc=location))
        #     time.sleep(10)
        #     pause = 3
        #     lastHeight = driver.execute_script("return document.body.scrollHeight")
        #     counter = 0
        #     descriptions = driver.find_elements_by_xpath("//div[@id='all_search_results']//div[@class='_glj']")
        #     scroll = True
        #     for description in descriptions:
        #         if "\nCity\n" in description.text:
        #             print("i've found a city")
        #             link = description.find_elements_by_tag_name('a').pop(0)
        #             ActionChains(driver).move_to_element(link).click().perform()
        #             scroll = False
        #             break
        #     if scroll:
        #         driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        #         time.sleep(pause)
        #         newHeight = driver.execute_script("return document.body.scrollHeight")
        #         print "scrolling down"
        #         descriptions = driver.find_elements_by_xpath("//div[@id='all_search_results']//div[@class='_glj']")
        #         for description in descriptions:
        #             if "\nCity\n" in description.text:
        #                 print("i've found a city")
        #                 link = description.find_elements_by_tag_name('a').pop(0)
        #                 ActionChains(driver).move_to_element(link).click().perform()
        #                 break
        #                 # link = description.find_element(By.XPATH('//div[@class="_gll]"/a'))
        #                 # print(link.get_attribute("href"))
        #         if newHeight == lastHeight:
        #             print "broken"
        #             break
        #
        #     print "here after scroll"

            # people_elem = driver.find_elements_by_class_name('phs')
            # descriptions = driver.find_elements_by_xpath("//div[@id='all_search_results']//div[@class='_glj']")
            # for description in descriptions:
            #     if "\nCity\n" in description.text:
            #         print("i've found a city")
            #         link = description.find_elements_by_tag_name('a').pop(0)
            #         break
            #         # link = description.find_element(By.XPATH('//div[@class="_gll]"/a'))
            #         # print(link.get_attribute("href"))
            # ActionChains(driver).move_to_element(link).click().perform()
            # hov = ActionChains(driver).move_to_element(link)
            # hov.perform()
            # link.click()
            # time.sleep(10)

            # people_elem = driver.find_elements_by_xpath("//div[@id='pagelet_search_results_objects']//div[@class='clearfix']/div[@class='_5d-5']")
            # # time.sleep(10)
            # for people_el in people_elem:
            #     notion = people_el.find_element_by_class_name("_pac")
            #     print(notion)
            # hov = ActionChains(driver).move_to_element(people_elem[1])
            # hov.perform()
            # people_elem[1].click()

            # people_elem[1].click()

            # print("ready to open a pop-up")
            # show_more = driver.find_element_by_xpath("//div[@id='contentArea']/div[@id='pagelet_timeline_main_column']/div/div[@id='pagelet_vertex_body']/div[@class='clearfix']/div[@class='_3nj']//div/div/div[@class='_4lv']//div[@class='_438']/a")
            # hov2 = ActionChains(driver).move_to_element(show_more)
            # hov2.perform()
            # show_more.click()
            # time.sleep(10)
            # html = driver.page_source
            # lxml_html = lxml.html.fromstring(str(html))
            # profile_links = lxml_html.xpath("""//div[@class='uiScrollableAreaContent']/div[@class='fbProfileBrowserList fbProfileBrowserListContainer fbProfileBrowserNoMoreItems']/ul[@class='uiList clearfix _5bbv _4kg _704 _4ks']/li[@class='fbProfileBrowserListItem']//div[@class="uiProfileBlockContent"]//a[@aria-haspopup]/@href""")
            # print profile_links
            # profile_links = [link for link in profile_links if link.startswith('https://') ]

            # other way to get the attributes @href
            # if profile_links == []:
            #     profile_links_we = driver.find_elements_by_xpath("""//div[@class='uiScrollableAreaContent']//ul[@class='uiList clearfix _5bbv _4kg _704 _4ks']//div[@class="uiProfileBlockContent"]//div[@class="fsl fwb fcb"]/a[1]""")
                # print("check your xpaths!")
                # print(profile_links_we)
                # for link in profile_links_we:
                #     profile_links.append(link.get_attribute("href"))

            # item = FacebookcrawlerItem()
            # for profile_link in profile_links:
            #     print profile_link
            #     body = driver.find_element_by_tag_name("body")
            #     body.send_keys(Keys.CONTROL + 't')
            #     driver.get(profile_link.replace('?fref=pb&hc_location=profile_browser','')+'/about')
            #     time.sleep(2)
            #     html = driver.page_source
            #     lxml_html = lxml.html.fromstring(str(html))
            #     name = lxml_html.xpath('//title[@id="pageTitle"]/text()')
            #     first_name = last_name = ''
            #     if name:
            #         name = re.sub('\(\w*\)','',str(name[0])).split()
            #         first_name = name[0]
            #         if len(name) >= 3:
            #             first_name = ' '.join(name[0:1])
            #         last_name = name[-1]
            #     print first_name
            #     print last_name
            #     item['FirstName'] = first_name
            #     item['LastName'] = last_name
            #     # name = lxml_html.xpath('//span[@id="fb-timeline-cover-name"]/text()')
            #     # print name
            #     phone = lxml_html.xpath('//span[@dir="ltr"]/text()')
            #     print phone
            #     item['Phone'] = phone
            #     email = lxml_html.xpath('//a[contains(text(),"@")]/text()')
            #     print email
            #     item['Email'] = email
            #     print profile_link
            #     item['PageUrl'] = profile_link
            #     item['Location'] = location
            #     yield item

        
        # f = open('friends2.html','w')
        # f.write(str(profile_links))
        
        driver.quit()



                # pass
