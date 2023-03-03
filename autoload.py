import os
import re
import sys
from bs4 import BeautifulSoup
from youtubesearchpython import *




def adder(fpath):
	with open(fpath) as fp:

		soup = BeautifulSoup(fp, "html.parser")
		new_child = r"{% load static %}"
		soup.insert(0, new_child)
		img = soup.find_all("img") 
		link = soup.find_all("link") # for CSS use only
		script = soup.find_all("script")

		regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
		
		
		try:
			for i in link:
				url = re.findall(regex, i.attrs["href"])
				if url == []:
					temp = i.attrs["href"]
					temp2 = r"{% static '" + temp + r"' %}"
					i.attrs["href"] = temp2
		except:
			pass

		try:
			for i in img:
				url = re.findall(regex, i.attrs["src"])
				if url == []:
					temp = i.attrs["src"]
					temp2 = r"{% static '" + temp + r"' %}"
					i.attrs["src"] = temp2
		except:
			pass

		try:
			for i in script:
				url = re.findall(regex, i.attrs["src"])
				if url == []:
					temp = i.attrs["src"]
					temp2 = r"{% static '" + temp + r"' %}"
					i.attrs["src"] = temp2
					# <script data-cfasync="false" src="../../cdn-cgi/scripts/5c5dd728/cloudflare-static/email-decode.min.js"></script>
		except:
			pass
		fp.close()	

	# with open(fpath, "w") as file:
	# 	print(str(soup))
	# 	file.write(str(soup))
	import io
	with io.open(fpath, "w", encoding="utf-8") as f:
		f.write(str(soup))
	return r'Added {% static '' %} in ' + fpath + 	' ...Done' 


# Driver Code
if __name__ == "__main__":
	print('{:^50}'.format('!!! Welcome to Django static tag Add Utility !!!'))
	print("Enter '1'to specify path ")
	print("Enter '2' to autosearch and Edit Which is Awesome")
	print("Enter '0' to exit")
	choice = int(input("Enter Here: "))

	if choice == 1:
		temp = 1
		while temp !=0:
			path = str(input("Please add the file path : "))
			print(adder(path))
			temp = int(input("Please press 1  to add more file or 0 to exit"))
	elif choice ==2:
		ls = os.listdir()
		cwd = os.getcwd()

		for i in ls:
			if i[-4:] == 'html':
				print(adder(os.path.join(os.getcwd(), i)))

	input("enter any key to exit...")