from multiprocessing.connection import Client
import cv2
import numpy as np
from PIL import ImageChops
from pyscreenshot import grab
from scipy import misc
import os
import time


class Client:
	def __init__(self):
		print("Client initiated :)")
		#self.detect_card_image("card")
		self.detect_difference()
		#self.conn = self.get_server_conn()
		#self.send_cards()
		#self.close_server_conn()

	def get_server_conn(self):
		address = ('localhost', 6000)
		conn = Client(address, authkey=b'&oi}Po5e6')
		return conn

	def close_server_conn(self):
		self.conn.close()

	def send_cards(self):
		self.conn.send("cards")
		self.conn.send(self.get_cards())

	def get_cards(self):
		cards = "Ah As"
		return cards

	def detect_difference(self):
		# Specifing the region of the cards
		region = (385, 40, 525, 140)
		while True:
			print("in here")
			im = grab(region)
			time.sleep(1)
			new_im = grab(region)
			diff = ImageChops.difference(new_im, im)
			bbox = diff.getbbox()
			if bbox is not None: 
				# Convert image to grayscale
				numpy_im = np.array(new_im)				
				cv_im = numpy_im.astype(np.uint8)				
				
				cards_img = self.split_image(cv_im)
				print("card img 0")
				self.detect_card_image(cards_img[0], "number0")
				print("card img 1")				
				self.detect_card_image(cards_img[1], "number1")

	def split_image(self, img):
		height = img.shape[0]
		width = img.shape[1]
		
		# Cut the image in half
		width_cutoff = width // 2
		first_half = img[:, :width_cutoff]
		second_half = img[:, width_cutoff:]
	
		return [first_half, second_half]	
				

	def detect_card_image(self, card_image, name):
		print("detecting")
		img = card_image
		for suit_image_name in os.listdir("./data/suit_images"):
			suit_image = cv2.imread(os.path.join(".\\data\\suit_images\\", suit_image_name), cv2.IMREAD_UNCHANGED)

			# Create template to increase accuracy as grayscale from alpha channel and make 3 channels			
			hh, ww = suit_image.shape[:2]
			tmplt_mask = suit_image[:,:,3]
			tmplt_mask = cv2.merge([tmplt_mask,tmplt_mask,tmplt_mask])
			
			# Extract template without alpha channel from tmplt
			tmplt2 = suit_image[:,:,0:3]
			
			# Do template matching
			match = cv2.matchTemplate(img,tmplt2,cv2.TM_CCORR_NORMED, mask=tmplt_mask)
			min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(match)
			
			if max_val > .9:
				# we discovered suit
				suit_dictionary = {
					"hearts.png" : 0,
					"spades.png" : 1,
					"diamonds.png" : 2,
					"clubs.png" : 3,
				}
				suit = suit_dictionary[suit_image_name]
				print(suit_image_name, max_val)

				value_img = card_image[10:40, 8:40]	
				gray = cv2.cvtColor(value_img, cv2.COLOR_BGR2GRAY)
				thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
				for value_image_name in os.listdir("./data/value_images"):
					value_image = cv2.imread(os.path.join(".\\data\\value_images\\", value_image_name), cv2.IMREAD_UNCHANGED)
					grays = cv2.cvtColor(value_img, cv2.COLOR_BGR2GRAY)
#
					match = cv2.matchTemplate(thresh, grays, cv2.TM_CCOEFF_NORMED)
					min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(match)
					print(max_val, min_val)
					print(min_loc, max_loc)
					print(value_image_name)
					print("-----------")



if __name__ == "__main__":
	Client()
