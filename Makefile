
web:
	python newsclipse/manage.py runserver

reset:
	python newsclipse/manage.py reset

demo:
	curl -H "Content-Type: application/json" -d @demo.json http://127.0.0.1:5000/api/stories

setup:
	curl -H "Content-Type: application/json" -d @demo.json http://newsclipse.herokuapp.com/api/stories
