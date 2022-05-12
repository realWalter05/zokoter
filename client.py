from server import Server
import cv2
import numpy as np
from PIL import ImageChops
from pyscreenshot import grab
import os
import time
import random
import socket


class CardClient:
	def __init__(self):
		print("Client initiated :)")
		self.conn = self.get_server_conn()
		msg = ""
		while msg != "!disconnect": 
			# Receive instructions
			msg_length = self.conn.recv(Server.HEADER).decode(Server.FORMAT)
			if not msg_length:
				return
			msg_length = int(msg_length)
			msg = self.conn.recv(msg_length).decode(Server.FORMAT)

			if msg == "!boardConn":
				print("boardConn")
				new_board_cards = self.detect_difference()
				board_string = " ".join([self.get_card_name(card) for card in new_board_cards])
				print(board_string)
				self.send_msg(board_string)


			elif msg == "!sendcards":
				print("sending cards")
				cards = self.scan_for_cards()
				self.send_msg(cards)

			print(msg)

		
		print("Connection has ended")	
		input("exit on press")


	def get_server_conn(self):
		client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		client.connect(Server.ADDR)
		return client

	def close_server_conn(self):
		self.conn.close()

	def send_msg(self, msg):
		message = (msg).encode(Server.FORMAT)
		msg_length = len(message)
		
		send_length = str(msg_length).encode(Server.FORMAT)
		send_length += b" " * (Server.HEADER - len(send_length))

		self.conn.send(send_length)
		self.conn.send(message)

	def scan_for_cards(self):
		fcard = None
		scard = None
		while not fcard and not scard:
			region = (390, 53, 520, 128) # region = x1 y1 x2 y2
			new_cards = grab(region)
		
			cards_img = self.get_card_images(new_cards)
			fcard = self.get_card_name(cards_img[0], "cards")	
			scard = self.get_card_name(cards_img[1], "cards")
		return fcard + " " + scard


	def detect_difference(self):
		# Specifing the region of the cards
		region = (505, 396, 930, 486) # region = x1 y1 x2 y2
		while True:
			# Grab the image
			last_cards = grab(region)
			# Regrap the image
			#input("Next one on enter: ")
			time.sleep(0.5)
			new_cards = grab(region)
			
			# Get difference
			diff = ImageChops.difference(new_cards, last_cards)
			change_box = diff.getbbox()

			if change_box is not None: 
				# The card region part has changed
				cards_img = self.get_board_card_images(new_cards)
				print("Changed")
				#return cards_img
				#self.get_card_name(cards_img[0])
				#self.get_card_name(cards_img[1])
				#cv2.imwrite("./data/cards/card"+str(random.randint(1, 9999))+".png", cards_img[0])
				#cv2.imwrite("./data/cards/card"+str(random.randint(1, 9999))+".png", cards_img[1])


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
		# Missing player cards Qs
		for image_name in os.listdir("./data/" + directory):
			image = cv2.imread(os.path.join(".\\data\\" + directory + "\\", image_name))

			# Get the difference
			difference = cv2.subtract(image, card_image)    
			result = not np.any(difference)

			if result is True:
				# Image is detected
				card_name = image_name.split(".")[0]
				print("This card is " + card_name)
				return card_name
		return ""


if __name__ == "__main__":
	CardClient()
