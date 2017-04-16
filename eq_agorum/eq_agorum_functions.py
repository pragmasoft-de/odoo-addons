# -*- coding: utf-8 -*-
##############################################################################
#
#    Odoo Addon, Open Source Management Solution
#    Copyright (C) 2014-now Equitania Software GmbH(<http://www.equitania.de>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

import requests
from requests.exceptions import ConnectionError
import json
import urllib



class eq_agorum_functions:
	
	def __init__(self, agorum_settings):
		self.agorum_settings = agorum_settings
	
	
	def login(self, settings):
		"""
		Executes a login in Agorum
		@param settings: dictionary that contains the login data and optionally the token
		@return login_result: contains session, success status and a message if an error occurred 
		"""
		
		user = settings['agorum_user']
		if ('agorum_token' in settings and settings['agorum_token']):
			login_vals = {
							'username': user,
		              	  	'token': settings['agorum_token']
		             	}
		else:
			login_vals = {
							'username': user,
			              	'password': settings['agorum_password']
						}
		
		header = {}#{'content-type': 'application/json'}
		request_params = login_vals#json.dumps(login_vals)
		message = ''
		error_found = False
		success = False
		sessionID = ''
		
		try:
			request_res = requests.post(self.agorum_settings.session_service + 'login.json', data=request_params, headers=header)
			jsonRes = request_res.json()
		except ConnectionError, e:
			error_found = True
			message = 'ConnectionError: ' + str(e.message)	
		except Exception, e:
			error_found = True
			message = 'Error: ' +  str(e.message)
			return 
		
		if (not error_found and jsonRes):
			success = jsonRes['success']
			if (success):
				sessionID =jsonRes['sessionId']
		
		return login_result(user, sessionID, success, message)
		
	def create_token(self, settings):
		"""
		Creates a token that can be used to create a session for a User without the password
		@param settings: dictionary that contains the login data and the the value for asUser that determines the user's rights
		@return create_token_result: contains token, success status and a message if an error occurred
		"""
		
		try:
			login_result = self.login(settings)
		except Exception, e:
			print 'Error during login: ' + e.message
		
		if (not login_result or not login_result.success):
			#TODO: Error
			return create_token_result('', false, 'Login failed')
		
		
		message = ''
		header = {'content-type': 'application/json'}

		params = {
				'asUser': settings['as_user'],
		        'sessionId': login_result.sessionID# jsonRes['sessionId']
				}
		request_params = json.dumps(params)
		
		
		try:
			request_res = requests.post(self.agorum_settings.session_service + 'token.json', data=request_params, headers=header)
			jsonRes = request_res.json()
			
		except ConnectionError, e:
			#Todo
			return 
		
		success = False
		token = ''
		if (jsonRes):
			success = jsonRes['success']
			if (success):
				token =jsonRes['token']
		return create_token_result(token, success, message)
	
	
	def start_transaction(sessionID):
		"""
		Starts a transaction for the session
        @param sessionID: SessionID for Agorum
        @return transaction_id: the id of the new transaction
		"""
		
		header = {'content-type': 'application/json',}
		
		body = {
		        "sessionId": sessionID,
		         "timeout": -1, 
		         "properties": "transactionId",
		        }
		data_args = json.dumps(body)        
		
		url = self.agorum_settings.session_service + 'transaction.json'
		request_res = requests.post(url, data=data_args, headers=header)
		res_json = request_res.json()
		
		transaction_id = ''
		if (res_json and res_json['success']):
		    transaction_id = res_json['transactionId']
		return transaction_id
		    
	def end_transaction(transactionID, sessionID):
		"""
		Ends a transaction for the session
		@param transactionID
        @param sessionID: SessionID for Agorum
        @return true if the transaction was found and could be closed
		"""
		
		header = {'content-type': 'application/json',}
		
		body = {
		        "sessionId": sessionID,
		         "transactionId": transactionID, 
		        }
		data_args = json.dumps(body)
		
		url = self.agorum_settings.session_service + 'transaction.json'
		request_res = requests.delete(url, data=data_args, headers=header)
		res_json = request_res.json()
		if (res_json):
		    return res_json['success']
		return False
	
	def set_metadata(self, uuid, meta_data, sessionID):
		"""
		Sets the metadata for the document with the given uuid
		@param uuid: uuid of the document
        @param meta_data: the metadata
        @param sessionID: SessionID for Agorum
		"""
		
		header = {
		          'content-type': 'application/json',
		          'Accept': 'application/json'
		         }
		
		data_args = {
		             'sessionId': sessionID,
		            'data': meta_data 
		            }
		data_args_json = json.dumps(data_args)
		
		url = self.agorum_settings.object_service + 'uuid%3A%2F%2F' + uuid
		test = ''
		
		try:
			requestRes = requests.put(url, headers=header, data=data_args_json)
			json_res = requestRes.json()
		except ConnectionError, con_err:
			#Todo
			pass
		except Exception, exc:
			pass
			    	
		success = json_res['success']
	    
	def file_exists(self, uuid, sessionID):
		"""
		Checks in Agorum for a file with the given uuid
		@param uuid: uuid of the document
        @param sessionID: SessionID for Agorum
		"""
		
		header = {
				 	'content-type': 'application/json',
	              	'Accept': 'application/json'
				}
	    
	    
		url_params = {
		              'properties':['id','name'],
		              'sessionId': sessionID,
		              'handler':'object'
		              }
	    
		url = self.agorum_settings.object_service + 'uuid%3A%2F%2F' + uuid
		#requestTxt = json.dumps(url_params)
		found_id = 0;
		
		request_res = requests.get(url, params=url_params, headers=header)
		json_res = request_res.json()
		success = json_res['success']
		
		res_data = json_res['data']
		if (res_data):
		    found_id = res_data['id']
		 
		
		return found_id > 0
	   
	    
	    
	    
	def get_file(self, uuid, sessionID):
		"""
		Downloads a file from Agorum
		@param uuid: uuid of the document
        @param sessionID: SessionID for Agorum
        @return: get_file_result: contains the file's content, the success status and a message if an error occurred
		"""
		
		success = False
		message = ''
		file_content = None
		header = {
					'content-type': 'application/json',
					'Accept': 'application/json'
		         }
		
		url_params = {
		              'sessionId': sessionID,
		              }
		url = self.agorum_settings.object_service + 'download/uuid%3A%2F%2F' + uuid
		
		try:
			request_result = requests.get(url, params=url_params, headers=header)
			success = True
			file_content = request_result.content
			#if the document was found, the content-type is text/plain and request_result.content contains the file's data
			if ('content-type' in request_result.headers):
				content_type = request_result.headers['content-type']
				if ('application/json' in content_type):
					res_json = request_result.json()
					if (res_json):
						success = res_json['success']
						message = res_json['message']
			
		except ConnectionError, conError:
			message = 'ConnectionError in get_file: ' + str(conError)
		except Exception, exc:
			message = 'Error in get_file: ' + str(exc)
		return get_file_result(file_content, success, message)

	
	def upload_file(self, file_values, sessionID):
		"""
		Uploads a file to Agorum
		@param file_values: dictionary that contains the file's data and its name
		@param sessionID: SessionID for Agorum
		@return upload_file_result: contains the uuid of the document in Agorum, the success status and a message if an error occurred 
		"""
		
		header = {
				 	'content-type': 'multipart/form-data',
		         }
		
		target_dir = self.agorum_settings.target_directory
		if (not target_dir):
			#TODO: Error
			pass
		
		url_params = {
		              'sessionId': sessionID,
		              'target': target_dir
		              }
		
		file_data = file_values['file_data']
		filename = file_values['filename']
		
		success = False
		message = ''
		res_uuid = '';
		try:
			files = [('name', filename), ('file', file_data)]
			
			#files = urllib.urlencode(files)
			
			#alt
			#files = {'file': (filename.encode("utf-8"), file_data)}
			
			url = self.agorum_settings.object_service + 'upload'
			files_content = json.dumps(files)
			requestRes = requests.post(url, params=url_params, headers=header, files=files)
			requestRes_json = requestRes.json()
			
			if (requestRes_json):
				if (requestRes_json['success']):
					success = True
					res_uuid = requestRes_json['uuid']
				else:
					message = requestRes_json['message']
					
		except ConnectionError, conError:
			message = 'ConnectionError in upload_file' + str(conError)
		except Exception, exc:
			message = 'Error in upload_file' + str(exc)
			
		return upload_file_result(res_uuid, success, message)
	    
	    #Todo: return res_uuid + id for attachment
    	
	def update_file(self, uuid, file_values, sessionID):
		"""
		Updates an existing file in Agorum
		"""
		header = {
				'content-type': 'multipart/form-data',
		         }
		
		url_params = {
		              'sessionId': sessionID,
		              }
		
		file_text = ''#Todo
		filename = 'Test1.pdf'#Todo
		#files = [('FILE', filename.encode("utf-8"), body)]
		files = {'file': (filename.encode("utf-8"), file_text)}
		
		url = self.agorum_settings.object_service + 'upload/uuid%3A%2F%2F' + uuid
		
		#requestRes = requests.post(url, params=url_params, headers=header, files=files)
		
		
	def delete_file(self, uuid, sessionID):
		"""
		Deletes an existing file in Agorum
		"""
		header = {
				#'content-type': 'multipart/form-data',
				'Accept': 'application/json'
		         }
		
		url_params = {
		              'sessionId': sessionID,
		              }
		
		message = ''
		success = False
		object_found = False
		
		
		url = self.agorum_settings.object_service + 'uuid%3A%2F%2F' + uuid
		
		try:
			requestRes = requests.delete(url, params=url_params, headers=header)
			requestRes_json = requestRes.json()
			
			
			if (requestRes_json):
				if (requestRes_json['success']):
					success = True
					object_found = True
				else:
					errorClass = requestRes_json['errorClass'] if requestRes_json['errorClass']  else 0
					errorCode = requestRes_json['errorCode'] if requestRes_json['errorCode']  else 0
					errorKey = requestRes_json['errorKey'] if requestRes_json['errorKey']  else 0
					
					if ((errorClass == 2) and (errorCode == 1) and (errorKey == 0)):
						object_found = False
					
					message = requestRes_json['message']
		except ConnectionError, conError:
			message = 'ConnectionError in delete file' + str(conError)
		except Exception, exc:
			message = 'Error in delete_file' + str(exc)
				
		return file_delete_result(uuid, success, message, object_found)
	

	def create_folder(self, sessionID, folder_name):
		header = {
					'content-type': 'application/json',
					'Accept': 'application/json'
		         }
		
		target_dir = self.agorum_settings.target_directory
		if (not target_dir):
			#TODO: Error
			pass
		
		success = False
		error_messages = []
		folders = folder_name.split('/')
		if (folders and len(folders) > 0):
			cur_target_dir = target_dir
			for folder in folders:
				folder_data = {
						'name':folder,
						'target':cur_target_dir,
						'createtarget':True
						}
			
				data_args = {
				             'sessionId': sessionID,
				             'handler':'folder',
				            'data': folder_data 
				            }
				data_args_json = json.dumps(data_args)
				
				url = self.agorum_settings.object_service
				
				try:
					requestRes = requests.post(url, headers=header, data=data_args_json)
					json_res = requestRes.json()
					
					if (requestRes_json['success']):
						success = True	
					
				except ConnectionError, con_err:
					error_messages.append('ConnectionError in create_folder' + str(con_err))
				except Exception, exc:
					error_messages.append('Error in create_folder' + str(con_err))
								
				cur_target_dir = cur_target_dir + '/' + folder							
		
		"""
		folder_data = {
					'name':folder_name,
					'target':target_dir,
					'createtarget':True
					}
		
		data_args = {
		             'sessionId': sessionID,
		             'handler':'folder',
		            'data': folder_data 
		            }
		data_args_json = json.dumps(data_args)
		
		
		url = self.agorum_settings.object_service
		
		
		#try:
		requestRes = requests.post(url, headers=header, data=data_args_json)
		json_res = requestRes.json()
		#except ConnectionError, con_err:
			#Todo
			#pass
		#except Exception, exc:
		#	pass
	 	"""

class agorum_settings:
	def __init__(self, session_service, object_service, target_directory, user, pw, token):
		self.session_service = session_service
		self.object_service = object_service
		self.target_directory = target_directory
		self.token = token
		self.user = user
		self.pw = pw

class base_result:
	def __init__(self, success, message):
		self.success = success
		self.message = message	 

 
class login_result(base_result):
	def __init__(self, user, sessionID, success, message):
		base_result.__init__(self, success, message)
		self.user = user
		self.sessionID = sessionID
		
class create_token_result(base_result):
	def __init__(self, token, success, message):
		base_result.__init__(self, success, message)
		self.token = token
		
class get_file_result(base_result):
	def __init__(self, content, success, message):
		base_result.__init__(self, success, message)
		self.content = content
		
class upload_file_result(base_result):
	def __init__(self, uuid, success, message):
		base_result.__init__(self, success, message)
		self.uuid = uuid
		
class file_exists_result(base_result):		
	def __init__(self, id, file_exists, success, message):
		base_result.__init__(self, success, message)
		self.file_exists = file_exists
		self.id = id
		
class file_delete_result(base_result):		
	def __init__(self, uuid, success, message, object_found):
		base_result.__init__(self, success, message)
		self.uuid = uuid
		self.object_found = object_found
		
class start_transaction_result(base_result):		
	def __init__(self, sessionID, transaction_id, success, message):
		base_result.__init__(self, success, message)
		self.sessionID = sessionID
		self.transaction_id = transaction_id