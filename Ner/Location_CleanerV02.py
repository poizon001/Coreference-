import json, ast
import requests
import json
from collections import Counter

def location(address,key):
	url = 'https://maps.googleapis.com/maps/api/geocode/json?address='
	api_key = str(key)
	fullurl = url + address + '&key=' + api_key
	r = requests.get(fullurl)

	data = json.loads(r.text)
	
	if len(data['results'])!=0:
		add = data['results'][0]['address_components']
		res = {}
		res['status']=data['status']
		for ele in add:
			if ele['types'] == [u'locality', u'political']:
				res['locality'] = ele['long_name']
			elif ele['types'] == [u'administrative_area_level_3', u'political']:
				res['administrative_area_level_3'] = ele['long_name']
			elif ele['types'] == [u'administrative_area_level_2', u'political']:
				res['administrative_area_level_2'] = ele['long_name']
			elif ele['types'] == [u'administrative_area_level_1', u'political']:
				res['administrative_area_level_1'] = ele['long_name']
			elif ele['types'] == [u'country', u'political']:
				res['country'] = ele['long_name']
		return res
	else:
		res={}
		res['status']=data['status']
		return res

if __name__=="__main__":
	###Input Files
	ff=['Hong Kong protests']
	####Output Files Address
	APi_Result=open('OutputV07.txt','w')
	###########Key files
	key_detail_list=open('Api_Keys.txt','r').read().split('\n')
	count=0
	key_id=0
	key=str(key_detail_list[key_id])
	# address='Montbeliard, France'
	# print location(address,key)


	
	for each in ff:
		key=str(key_detail_list[key_id])
		result=[]
		keyList=[]
		count+=1
		res=location(each.encode('utf-8'),key)
		print res
		if res['status']=='OK':
			pass
		elif res['status']=='OVER_QUERY_LIMIT':
			key_id+=1
			key=str(key_detail_list[key_id])
			print key
			res=location(each.encode('utf-8'),key)

		# result.append(each.encode('utf-8'))
		# if len(res)!=0:
		# 	for key,value in res.iteritems():
		# 		keyList.append(key)
		# 	if 'locality' in keyList:
		# 		locality=res['locality']
		# 	elif 'administrative_area_level_1' in keyList:

		# 		locality=res['administrative_area_level_1']
		# 	elif 'administrative_area_level_2' in keyList:
		# 		locality=res['administrative_area_level_2']
		# 	elif 'administrative_area_level_3' in keyList:
		# 		locality=res['administrative_area_level_3']
		# 	elif 'country' in keyList:
		# 		locality=res['country']

		# 	if 'administrative_area_level_1' in keyList:
		# 		state=res['administrative_area_level_1']
		# 	elif 'administrative_area_level_2' in keyList:
		# 		state=res['administrative_area_level_2']
		# 	elif 'administrative_area_level_3' in keyList:
		# 		state=res['administrative_area_level_3']
		# 	elif 'country' in keyList:
		# 		state=res['country']

		# 	if 'country' in keyList:
		# 		country=res['country']
		# 	else:
		# 		country='N/A'

		# 	result.append(locality.upper().encode('utf-8'))
		# 	result.append(state.upper().encode('utf-8'))
		# 	result.append(country.upper().encode('utf-8'))
		# 	print result
		# 	print >> APi_Result,'|'.join(result).decode('ascii','ignore').encode('utf-8')
		# else:
		# 	pass
	# except:
	# 	pass