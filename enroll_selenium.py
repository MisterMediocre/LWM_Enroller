from selenium import webdriver
from selenium.webdriver.common.keys import Keys 
import time
import datetime

import sys
import io
from keras.models import load_model
import cv2;
import numpy as np;
import keras;
from skimage import io;



#driver = webdriver.Safari()
driver = webdriver.PhantomJS("/Applications/phantomjs")
driver.maximize_window()
driver.implicitly_wait(5)

username = sys.argv[1]
password = sys.argv[2]
facility = sys.argv[3]

print("Username: ", username)

driver.get('https://www.lordswm.com')
print(driver.current_url)
username_field = driver.find_element_by_name('login')
username_field.send_keys(username)
password_field = driver.find_element_by_name('pass')
password_field.send_keys(password)
password_field.send_keys(Keys.RETURN)

print(driver.current_url)
time.sleep(2)
print(driver.current_url)

print(driver.current_url)
driver.get("https://www.lordswm.com/object-info.php?id=" + str(facility))
time.sleep(2)
print(driver.current_url)


try:
	captcha_image = driver.find_element_by_name('imgcode')
	imglink = captcha_image.get_attribute('src')
	print(imglink)
	img = io.imread(imglink)
	a = np.asarray(img)
	a = a[:,:,0]
	a = a/255
	a = 1-a
	print(a.shape)
	print("Image ready")


	def decode(c):
		if(c<10): return str(c)[1]
		else: return chr(c-10 + ord('a'))

	l = 10
	r = 230
	s = int((r-l)/6)
	model = keras.models.load_model('captcha_model.h5');
	captcha = ""
	for i in range(6):
		img = np.array(a[:, l + i*s-10: l + (i+1)*s + 10])
		c = decode(model.predict(img.reshape(-1, 60, 56, 1)).argmax(axis = 1));
		captcha = captcha + c;
	print(captcha)


	captcha_field = driver.find_element_by_name('code')
	captcha_field.send_keys(captcha)
	captcha_field.send_keys(Keys.RETURN)

	print(driver.current_url)
	time.sleep(2)
	print(driver.current_url)

	bodyText = driver.find_element_by_tag_name('body').text
	import urllib.request
	if "Invalid" in bodyText:
		urllib.request.urlretrieve(imglink, "images/more/" + captcha+ ".jpg")
		print("Wrong Captcha")
	elif "success" in bodyText:
		urllib.request.urlretrieve(imglink, "images/annotated/" + captcha+ ".jpg")
		print("Right Captcha")
		f = open("log.txt", "a")
		f.write(str(datetime.datetime.now()) + " " + facility + " " + username + "\n" )

finally:
	driver.quit()



#map_icon = driver.find_element_by_partial_link_text('Map')
#driver = webdriver.Safari()

#print(map_icon.get_attribute("a"))



