#! /usr/bin/env python
#Â encoding: utf-8
#
# Res andy
import xml.etree.ElementTree as ET,sys

###########################################################
#  • Always backup your map before launching this script  #
#  • Do that even so this script does its backup as well  # 
#  • Place this file directly into the map folder         # 
#  • Please report any errors to andys@deltaflyer.cz      #
#  • You can contact me on unofficial IRC ME channel too  #
#  • join #medieval-engineers on irc.esper.net               #
###########################################################

#too lazy to study namespaces in python, lets load the namespace line into string and place it into newly created file later
origfile = open('SANDBOX_0_0_0_.sbs').read()
backupfile = open('SANDBOX_0_0_0_.orig',"w")
backupfile.write(origfile)
backupfile.close
windows = 0
if len(origfile.split("\r\n")) == 1: #fix if this script is run in windows and set the flag
	windows = 1
	header = origfile.split("\n")[1]
else:
	header = origfile.split("\r\n")[1]


tree = ET.parse('SANDBOX_0_0_0_.sbs') #creates XML tree from sandbox.sbc file
root = tree.getroot() #creates XML root from the tree

a = 0 #helper to backnotate to root in XML remove function (it does not automatically)
deleted = 0 #definition of deleted twigs, just for our info
Objects = [] #list of npcs to remove

for child in root: #Let's list all subelements in root
	if child.tag == "SectorObjects": #if the element is Itentity list
		ObjectId = a #save its position in root to this integer
		for Object in child: #iterate every Object
			if Object.attrib.values()[0] != "MyObjectBuilder_CubeGrid": continue
			for element in Object:
				if element.tag == "CubeBlocks":
					for Block in element[0]:
						if Block.tag == "SubtypeName":
							if Block.text == "ScrapWoodBranches": 
								Objects.append(Object) #Add Object to Objects list
	a += 1

for child in Objects: #for every Object
	root[ObjectId].remove(child) #remove node
	deleted += 1 #and increase counter
		

print "deleted %s branches" %deleted #gloat about how we're good
tree = ET.ElementTree(root)
tree.write('SANDBOX_0_0_0_.sbs', encoding='utf-8', xml_declaration=True) #save the file

filethelper = "" #helping string
worldR = open('SANDBOX_0_0_0_.sbs',"r") #open world file for reading
filet = worldR.read().split("\n") #read its content and split it by line (without newline character)
worldR.close() #close the file so we can write into it
filet[1] = header #replace the namespace line with the backup from the begining of the file
for line in filet: #iterate through every line in file
	if windows == 1:
		filethelper += line+"\n" #mangle it together with DOS newline
	else:
		filethelper += line+"\r\n" #mangle it together with FORCED DOS newline
worldW = open('SANDBOX_0_0_0_.sbs',"w") #open worldfile for write
worldW.write(filethelper) #write it                                 
worldW.close() #close it
#quit
