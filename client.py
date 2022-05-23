import cv2
import numpy as np
from PIL import ImageChops
from pyscreenshot import grab
import os
import time
import socket

HEADER = 64
FORMAT = "UTF-8"

class CardClient:
	def __init__(self):
		print("Client initiated :)")
		self.conn = self.get_server_conn()
		msg = ""
		while msg != "!disconnect": 
			# Receive instructions
			msg_length = self.conn.recv(HEADER).decode(FORMAT)
			if not msg_length:
				return
			msg_length = int(msg_length)
			msg = self.conn.recv(msg_length).decode(FORMAT)

			if msg == "!boardConn":
				new_card_string = None
				while new_card_string is None:
					print("boardConn")
					new_board_cards = self.detect_difference()
					new_board_array = [self.get_card_name(card, "board_cards") for card in new_board_cards]

					falty = False
					for idx, card in enumerate(new_board_array):
						# Detect invalid scan
						if not card:
							continue
						for i in range(idx):
							if not new_board_array[i]:
								falty = True

					if falty or len([x for x in new_board_array if x]) != len(set([x for x in new_board_array if x])):
						# Check for valid scan
						print("falty")
						continue

					new_card_string = ""
					for card in new_board_cards:	
						card_name = self.get_card_name(card, "board_cards")
						if not card_name:
							continue

						if not new_card_string:
							new_card_string = card_name
							continue					
						new_card_string = new_card_string + " " + card_name 

				print(new_card_string)
				self.send_msg(new_card_string)


			elif msg == "!sendcards":
				print("sending cards")
				cards = self.scan_for_cards()
				self.send_msg(cards)

			print(msg)
		
		print("Connection has ended")	
		input("exit on press")


	def get_server_conn(self):
		client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		user_input_ip = input("Host machine IP: ") # IP Address of the host machine, vm must be in bridged connection mode (10.0.0.54 should be it on ether)
		client.connect((user_input_ip, 7849))
		return client

	def close_server_conn(self):
		self.conn.close()

	def send_msg(self, msg):
		message = (msg).encode(FORMAT)
		msg_length = len(message)
		
		send_length = str(msg_length).encode(FORMAT)
		send_length += b" " * (HEADER - len(send_length))

		self.conn.send(send_length)
		self.conn.send(message)

	def scan_for_cards(self):
		fcard = None
		scard = None
		recheck = True

		while not fcard or not scard:
			region = (390, 53, 520, 128) # region = x1 y1 x2 y2
			new_cards = grab(region)
		
			cards_img = self.get_card_images(new_cards)
			fcard = self.get_card_name(cards_img[0], "cards")	
			scard = self.get_card_name(cards_img[1], "cards")

			if fcard == "NaN" or fcard == "NaN":
				# Rechecking for no cards
				if recheck:
					fcard = None
					scard = None
					recheck = False
					time.sleep(2)
					continue
			recheck = True

		if fcard == "NaN" and scard == "NaN":
			return ""

		return fcard + " " + scard


	def detect_difference(self):
		# Specifing the region of the cards
		region = (505, 396, 930, 486) # region = x1 y1 x2 y2
		while True:
			# Grab the image
			last_cards = grab() # TODO region for grabbing, maybe the game table
			# Regrap the image
			#input("Next one on enter: ")
			new_cards = grab()
			
			# Get difference
			diff = ImageChops.difference(new_cards, last_cards)
			change_box = diff.getbbox()
			if change_box is not None: # TODO Percentage would be better, only one which is triggered by card change
				# Cooldown to get images even if this functions activated while they were only moving and not settled
				time.sleep(1)
				new_cards = grab(region)

				cards_img = self.get_board_card_images(new_cards)
				print(f"Changed")
				last_cards = None
				new_cards = None
				change_bog = None
				diff = None
				return cards_img


	def get_card_images(self, im):
		# Getting the dimensions
		width, height = im.size

		# Crop the card-part of the image
		first_half = im.crop((6, 0, 64, height))
		second_half = im.crop((69, 0, 127, height))

		# Converting to opencv format
		first_half_numpy = np.array(first_half)				
		second_half_numpy = np.array(second_half)				
		cv_first_half = first_half_numpy.astype(np.uint8)	
		cv_second_half = second_half_numpy.astype(np.uint8)	

		return [cv_first_half, cv_second_half]			


	def get_board_card_images(self, im):
		# Getting the dimensions
		width, height = im.size

		# Crop the card-part of the image
		card00 = im.crop((5, 0, 82, height))
		card01 = im.crop((89, 0, 166, height))
		card02 = im.crop((174, 0, 251, height))
		card03 = im.crop((259, 0, 336, height))
		card04 = im.crop((344, 0, 421, height))

		# Converting to opencv format
		card00_numpy = np.array(card00)				
		card01_numpy = np.array(card01)	
		card02_numpy = np.array(card02)				
		card03_numpy = np.array(card03)
		card04_numpy = np.array(card04)				
									
		cv_card00 = card00_numpy.astype(np.uint8)	
		cv_card01 = card01_numpy.astype(np.uint8)	
		cv_card02 = card02_numpy.astype(np.uint8)	
		cv_card03 = card03_numpy.astype(np.uint8)	
		cv_card04 = card04_numpy.astype(np.uint8)										

		return [cv_card00, cv_card01, cv_card02, cv_card03, cv_card04]	

	def get_card_name(self, card_image, directory):
		most_accr = 1000000
		card = ""
		for image_name in os.listdir("./data/" + directory):
			image = cv2.imread(os.path.join(".\\data\\" + directory + "\\", image_name))

			# Get the difference
			difference = cv2.subtract(image, card_image)    

			b, g, r = cv2.split(difference)
			accur = cv2.countNonZero(b) + cv2.countNonZero(g) + cv2.countNonZero(r)				
			if accur < most_accr:
				most_accr = accur
				card = card_name = image_name.split(".")[0]
		if most_accr < 801:
			print("This card is: " + card)
			return card
		return ""


if __name__ == "__main__":
	CardClient()
