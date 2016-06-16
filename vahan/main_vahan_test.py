import cv2
import os
import glob
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import numpy as np
#from create_txt_all_png import create_missed_txt


def string_match(s1):
	list=[]
	list_png=[]
	list_png_idx=[]
	list_txt_file=[]
	list_txt_content=[]


#-------------------sort png and txt files---------------------------------
	for f in sorted(glob.glob("book/*.png")):
		list_png.append(f)
	#print list_png[1]
	#print 'list of png images',len(list_png)


	for f in sorted(glob.glob("book/*.txt")):
		list_txt_file.append(f)

	#create_missed_txt(list_png,list_txt_file)


	for i in range(len(list_txt_file)):
		file=open(list_txt_file[i],'r')
		text=file.read().rstrip('\n')
		list_txt_content.append(text)

	list_txt_content = [element.lower() for element in list_txt_content]
	#print list_txt_content


#------------List the coordinates in txt file----------------------
	for f in (glob.glob("book/*.png")):
		list.append(f)
	#print list

	list_png_idx=[list.index(f) for f in sorted(glob.glob("book/*.png"))]
	#print list_png_idx

	with open('out/file_in.txt', 'r') as f:
		coordinates = [line.strip().split(' ') for line in f]
	#print 'coordinates',coordinates
	
	for i in range(0,len(coordinates)):
		coordinates[i]=[int(x) for x in coordinates[i]]
	#print coordinates


#--------------------- check for maximum width block and split--------------------

	width_len = []
	width_part_left=[]
	width_part_right=[]

	for i in range(0,len(coordinates)):
		if 500<coordinates[i][2]<700:
			 width_len.append(list_txt_content[i])

	for i in range(0,len(width_len)):
		width_part_left.append(width_len[i].split(':'))
	#print width_part_left

	if any(s1 in s for s in width_part_left):
		count=0
		for s in width_part_left:
			if s1 in s:
				print s1+' :'+width_part_left[count][1]
			count=count+1
			

	else:
		#------------------------find accuracy and match using fuzzy wuzzy---------------------------------------------
		accuracy_list=[]
			
		for i in range(0,len(list_txt_content)):
			accuracy=fuzz.ratio(s1,list_txt_content[i])
			accuracy_list.append(accuracy)
		#print accuracy_list
		#accuracy_list=[int(num) for num in accuracy_list]	
		#maximum=max(accuracy_list)	
		'''		
		numpy_array=np.array(accuracy_list)
		maximum=numpy_array.max()
		print maximum'''
		maximum_list=[]
		maximum_list_coord=[]
		for i in range(0,len(accuracy_list)):
			if accuracy_list[i]>= 75:
				maximum_list.append(accuracy_list[i])
				maximum_list_coord.append(coordinates[i])
		#print maximum_list
		#print maximum_list_coord

		if len(maximum_list)== 0:
			print 'Content is not in the list'
			exit(0)

		elif len(maximum_list)==1:
			idx_no=0

		else:
			if len(maximum_list_coord)> 1:
				for i in range(0,len(maximum_list_coord)):
				#if 10<coordinates[idx_no_list[i]][0]<150 or 650<coordinates[idx_no_list[i]][0]<950:

					if 10<maximum_list_coord[i][0]<150: #or 650<coordinates[idx_no_list[i]][0]<950:
						idx_no=i
				#print i

				
#---------------------------find image's corresponding coordinates to left--------------------
		image=cv2.imread("out/image.jpg")
		#print image_cord
		cv2.rectangle(image,(maximum_list_coord[idx_no][0], maximum_list_coord[idx_no][1]),(maximum_list_coord[idx_no][0]+maximum_list_coord[idx_no][2], maximum_list_coord[idx_no][1]+maximum_list_coord[idx_no][3]),(0,255,0),3)
		#cv2.imwrite('sort_coordinates/i1.png',image)
		width=maximum_list_coord[idx_no][2]	
		x=maximum_list_coord[idx_no][0]+width
		y=maximum_list_coord[idx_no][1]
		
		
		for i in range(0,len(coordinates)):
			#if (y-20)<coordinates[i][1]<(y+20) and (x+5)<coordinates[i][0]<(x+50):
			if (y-30)<coordinates[i][1]<(y+30) and x<coordinates[i][0]<x+250 :
				#print 'one',coordinates[i]
				c_idx=i
				cv2.rectangle(image,(coordinates[i][0], coordinates[i][1]),(coordinates[i][0]+coordinates[i][2], coordinates[i][1]+coordinates[i][3]),(0,0,255),3)

		cv2.imwrite('out/i6.png',image)
		print s1+' :'+ list_txt_content[c_idx].upper()
		

'''		idx_no_list=[]

		if maximum >= 80:
			for i in range(0,len(list_txt_content)):
				if maximum==accuracy_list[i] :
					idx_no_list.append(i)
			#print 'String match found : ',list_txt_content[idx_no]
			#print 'index no :',idx_no
			#print 'str coordinate:',coordinates[idx_no]
			print idx_no_list
		else:
			print 'Content is not in the list'
			exit(0)
#--------------- check if more than one word matches with the database------------------------------
		if len(idx_no_list)>1:
			for i in range(0,len(idx_no_list)):
				#if 10<coordinates[idx_no_list[i]][0]<150 or 650<coordinates[idx_no_list[i]][0]<950:
				if coordinates[idx_no_list[i]][0]<150 :
					idx_no=idx_no_list[i]
				print coordinates[idx_no_list[i]][0]
			print idx_no
			
		else:
			idx_no=idx_no_list[0]


			
	#---------------------------find image's corresponding coordinates to left--------------------
		image=cv2.imread("out/image.jpg")
		image_cord=[]
		image_cord=coordinates[idx_no]
		#print image_cord
		cv2.rectangle(image,(coordinates[idx_no][0], coordinates[idx_no][1]),(coordinates[idx_no][0]+coordinates[idx_no][2], coordinates[idx_no][1]+coordinates[idx_no][3]),(0,255,0),3)
		#cv2.imwrite('sort_coordinates/i1.png',image)
		width=coordinates[idx_no][2]	
		x=coordinates[idx_no][0]+width
		y=coordinates[idx_no][1]
		#print sort_mycoordinates[idx_no][1]
		#print type(sort_mycoordinates[idx_no][1])
		#print image_cord[idx_no][2]

		s=[]
		for i in range(0,len(coordinates)):
			#if (y-20)<coordinates[i][1]<(y+20) and (x+5)<coordinates[i][0]<(x+50):
			if (y-30)<coordinates[i][1]<(y+30) and x<coordinates[i][0]<x+250 :
				#print 'one',coordinates[i]
				c_idx=i
				cv2.rectangle(image,(coordinates[i][0], coordinates[i][1]),(coordinates[i][0]+coordinates[i][2], coordinates[i][1]+coordinates[i][3]),(0,0,255),3)

		cv2.imwrite('out/i6.png',image)
		print s1+' :'+ list_txt_content[c_idx]
		

				#s.append(i)	
		#print s0
		#print sort_mycoordinates[i]'''
		
		
	

s1=[]
s1=['no','name','financers','chassis no','engine no','marker model','company','manufacturer','validity']
#s1=str(raw_input('Enter the string : '))
#string_match(s1)

for i in range(0,len(s1)):
	string_match(s1[i])
