from selenium import webdriver
from operator import itemgetter
from selenium.common.exceptions import NoSuchElementException
from country_codes import country_to_code
options = webdriver.ChromeOptions()
# this argument stores cookies so to eliminate the need for logging in again.
options.add_argument("--user-data-dir=GoogleChromeUserData")
options.add_argument("--profile-directory=Default")
options.add_argument("--disable-notifications")

#make sure you enter the path to your own chrome driver
driver = webdriver.Chrome(executable_path="./chromedriver.exe",options=options)

class RedditPostScraper():
    def __init__(self,post):
        self.post=post
        self.post_class = post.get_attribute("class")
        self.post_id = post.get_attribute("id")

    def get_title(self):
        try:
            return self.post.find_element_by_xpath(
                f"//div[@class='_2FCtq-QzlfuN-SwVMUZMM3 _3wiKjmhpIpoTE2r5KCm2o6 {self.post_id}']/div/a/div/h3").text
        except:
            pass

    def get_vots(self):
        try:
            return self.post.find_element_by_xpath(
                f"//div[@class='{self.post_class}']/div/div/div[@class='_1rZYMD_4xY3gRcSS3p8ODO _3a2ZHWaih05DgAOtvu6cIo']").text
        except:
            pass

    def get_community(self):
        try:
            return self.post.find_element_by_xpath(
                    f"//div[@class='{self.post_class}']/div/div/div/div/div[@class='_2mHuuvyV9doV3zwbZPtIPG']").text
        except:
            pass

    def get_image_src(self):
        try:
            return self.post.find_element_by_xpath(
                f"//div[@class='{self.post_class}']/div[2]/div[3]/div/div[2]/div/a/div/div/img").get_attribute("src")
        except:
            pass
    def get_video_src(self):
        try:
            return self.post.find_element_by_xpath(
                f"//div[@class='{self.post_class}']/div[2]/div[3]/div/div[2]/div/video").get_attribute("src")
        except:
            pass

    def as_object(self):
        return {
            "title": self.get_title(),
            "votes": self.get_vots(),
            "community": self.get_community(),
            "image_src": self.get_image_src(),
            "video_src": self.get_video_src(),
            "id":self.post_id
        }
#-------------------------------------------------------------------------------------
class RedditScraper():

    def top_3_from_country(self,country):
        if not country in country_to_code:
            return []
        driver.get(f'https://www.reddit.com/r/popular/?geo_filter={country_to_code[country]}')
        posts_wrapper = driver.find_element_by_class_name("rpBJOHq2PR60pnwJlUyP0")
        posts = posts_wrapper.find_elements_by_xpath("//div//div//div[contains(@class,'Post')]")
        posts_to_filter = list(map(lambda post:RedditPostScraper(post).as_object(),posts))
        posts_with_imgs = list(filter(lambda p : p['image_src'] is not None and p['votes']
                                                 is not None,posts_to_filter))
        return posts_with_imgs[:3]



#print(RedditScraper().top_3_from_country("United States"))
