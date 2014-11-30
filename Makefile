
web:
	python newsclipse/manage.py runserver

reset:
	#python newsclipse/manage.py reset
	curl -H "Content-Type: application/json" -d '{}' http://127.0.0.1:5000/api/nuke

demo:
	curl -H "Content-Type: application/json" -d @demo.json http://127.0.0.1:5000/api/stories

setup:
	curl -H "Content-Type: application/json" -d @demo.json https://newsclipse.herokuapp.com/api/stories

build:
	python newsclipse/manage.py assets build

deploy:
	git push -f heroku master
	curl -H "Content-Type: application/json" -d '{}' https://newsclipse.herokuapp.com/api/nuke
	curl -H "Content-Type: application/json" -d @demo.json https://newsclipse.herokuapp.com/api/stories
