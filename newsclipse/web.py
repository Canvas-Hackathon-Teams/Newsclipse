from flask import render_template
from restpager import Pager

from newsclipse.core import app
from newsclipse.util import obj_or_404


@app.route('/')
def home():
    #pager = Pager(search_block(q))
    return render_template("index.html") #, pager=pager)
