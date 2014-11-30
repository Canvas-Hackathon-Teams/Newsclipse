import requests

def openDukaLookup(term):
	#TODO: please export this as a env variable
	key = '86a6b32f398fe7b3e0a7e13c96b4f032'
	# payload = {'key': key, 'term': 'KENYA NATIONAL EXAMINATIONS COUNCIL'}
	payload = {'key': key, 'term': term}
	r = requests.get("http://www.openduka.org/index.php/api/search", params=payload)
	ids = r.json()
	
	if len(ids) > 0:

		entId = ids[0]['ID']
		payload = {'key': key, 'id': entId}
		r = requests.get("http://www.openduka.org/index.php/api/entity", params=payload)
		connections = r.json()
		data = connections['data']
		returnLinks = []
		for typeSet in data:
			# print "new typeset!"
			dataset_types= typeSet['dataset_type']
			for types in dataset_types:
				label = types.keys()[0]
				link = "http://www.openduka.org/index.php/homes/tree/%s" % entId
				returnLinks.append({
									"type":label,
									"amount":len(label),
									"link":link
									})
				#return a array of objects
				# return a card object for every datatype, this will be a part of a person or company card
		return returnLinks
	else: 
		return False
		
		

# openduka = Openduka()
# openduka.lookup('KENYA NATIONAL EXAMINATIONS COUNCIL')