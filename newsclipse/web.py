from flask import render_template
from restpager import Pager

from newsclipse.core import app
from newsclipse.util import obj_or_404
from newsclipse.queue import extract, lookup


@app.route('/')
def home():
    extract.delay('huhu')
    #pager = Pager(search_block(q))
    return render_template("index.html")
