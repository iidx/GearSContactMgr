#-*- coding: utf-8 -*-
#Author : extr <extr3.0@gmail.com> // special thx to havu
#support korean lang.
import os
import sys
import sqlite3

class SDBConnect:

	def __init__(self):

		if os.path.isfile("sdb.exe"):
			pass
		else:
			print "sdb.exe not found"
			exit()

		if os.path.isfile(".contacts-svc.db"):
			pass
		else:
			e = os.system('sdb.exe root on')
			e = os.system('sdb.exe pull /opt/usr/dbspace/.contacts-svc.db ./')

			if not e == 0:
				print >>sys.stderr, 'error code :',e

		
	def ContactPush(self):
		e = os.system('sdb.exe push ./.contacts-svc.db /opt/usr/dbspace/')

		if not e == 0:
			print >>sys.stderr, 'error code :',e

class AddTables:

	conn = None
	cursor = None
	DataID = None
	ContactID = None
	ContactName = None
	ContactNumber = None


	def __init__(self):

		self.conn = sqlite3.connect(".contacts-svc.db")
		self.cursor = self.conn.cursor()

		self.ContactName = raw_input("Name : ")
		self.ContactName = self.ContactName.decode('cp949').encode('utf-8')
		self.ContactNumber = raw_input("Phone Number : ")

		self.ContactNumber = self.ContactNumber.translate(None, "!@#$%^&*()_+=- ")


	def __del__(self):
		self.conn.close()


	def ContactTable(self):

		TempQuery = "INSERT INTO `contacts`(`contact_id`,`person_id`,`has_phonenumber`,`has_email`,`display_name`,`reverse_display_name`,`display_name_source`,`display_name_language`,`reverse_display_name_language`,`sort_name`,`reverse_sort_name`,`sortkey`,`reverse_sortkey`,`created_ver`,`changed_ver`,`changed_time`,`link_mode`,`image_changed_ver`,`uid`,`ringtone_path`,`vibration`,`message_alert`,`image_thumbnail_path`,`image_path`) "
		TempQuery += "VALUES (NULL,0,1,0,'{0}','{1}',5,2,2,'{2}','{3}',NULL,NULL,0,0,0,0,0,999,NULL,NULL,NULL,NULL,NULL)".format(self.ContactName,self.ContactName,self.ContactName,self.ContactName)
		self.cursor.execute(TempQuery)

		self.cursor.execute("SELECT max(contact_id) FROM contacts")
		self.ContactID = self.cursor.fetchone()

		TempQuery = "UPDATE `contacts` SET `person_id`='{0}' WHERE `_rowid_`='{1}'".format(str(self.ContactID[0]),str(self.ContactID[0]))
		self.cursor.execute(TempQuery)


	def DataTable(self):

		TempQuery = "INSERT INTO `data`(`id`,`contact_id`,`datatype`,`is_my_profile`,`is_primary_default`,`is_default`,`data1`,`data2`,`data3`,`data4`,`data5`,`data6`,`data7`,`data8`,`data9`,`data10`,`data11`,`data12`) "
		TempQuery += "VALUES (NULL,'{0}',1,0,NULL,0,2,'{1}',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL)".format(str(self.ContactID[0]),self.ContactName)
		self.cursor.execute(TempQuery)

		TempQuery = "INSERT INTO `data`(`id`,`contact_id`,`datatype`,`is_my_profile`,`is_primary_default`,`is_default`,`data1`,`data2`,`data3`,`data4`,`data5`,`data6`,`data7`,`data8`,`data9`,`data10`,`data11`,`data12`) "
		TempQuery += "VALUES (NULL,'{0}',8,0,1,1,72,NULL,'{1}','{2}','{3}','{4}',NULL,NULL,NULL,NULL,NULL,NULL)".format(str(self.ContactID[0]),self.ContactNumber,self.ContactNumber,self.ContactNumber,self.ContactNumber)
		self.cursor.execute(TempQuery)

	
	def NameLookupTable(self):

		self.cursor.execute("SELECT max(id) FROM data")
		self.DataID = self.cursor.fetchone()

		TempQuery = "INSERT INTO `name_lookup`(`data_id`,`contact_id`,`name`,`type`) VALUES ('{0}','{1}','{2}',0)".format(str(self.DataID[0]),str(self.ContactID[0]),self.ContactName)
		self.cursor.execute(TempQuery)


	def PersonTable(self):

		TempQuery = "INSERT INTO `persons`(`person_id`,`name_contact_id`,`has_phonenumber`,`has_email`,`created_ver`,`changed_ver`,`ringtone_path`,`vibration`,`message_alert`,`image_thumbnail_path`,`image_path`,`link_count`,`addressbook_ids`,`dirty`,`status`) "
		TempQuery += "VALUES (NULL,'{0}',1,0,9,9,NULL,NULL,NULL,NULL,NULL,1,0,NULL,NULL)".format(str(self.ContactID[0]))
		self.cursor.execute(TempQuery)


	def commit(self):
		self.conn.commit()
		self.conn.close()


if __name__=="__main__":

	print "[!] This program is available only rooting device."

	sdb = SDBConnect()
	
	tbl = AddTables()
	tbl.ContactTable()
	tbl.DataTable()
	tbl.NameLookupTable()
	tbl.PersonTable()
	tbl.commit()

	sdb.ContactPush()
