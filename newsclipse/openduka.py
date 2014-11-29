class Openduka:
    """A thing that does a thing."""
    #We should hide this!
    key = 12345
    
    def lookup(term):
    	key = '86a6b32f398fe7b3e0a7e13c96b4f032'
		# payload = {'key': key, 'term': 'KENYA NATIONAL EXAMINATIONS COUNCIL'}
		payload = {'key': key, 'term': term}
		r = requests.get("http://www.openduka.org/index.php/api/search", params=payload)
		ids = r.json()
		# print ids
		payload = {'key': key, 'id': ids[0]['ID']}
		r = requests.get("http://www.openduka.org/index.php/api/entity", params=payload)
		connections = r.json()
		data = connections['data']
		for typeSet in data:
			print "new typeset!"
			dataset_types= typeSet['dataset_type']
			for types in dataset_types:
				print types.keys()
				print " "
		# return a card object for every datatype, this card object should an evidence type format.
		pass