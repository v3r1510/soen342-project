from flask import Flask, request, jsonify, Blueprint


bp = Blueprint('controller', __name__, url_prefix='/')


#this will be the link between the back and the front end, get posts html request etc, now i sleep 