from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    if data:
        return jsonify(data)

######################################################################
# GET A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    if data:
        # for every picture in the data
        for pic in data:
            if pic['id']==id:
                return jsonify(pic)
        return jsonify(message="Picture with id "+str(id)+" not found"), 404


######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    # get the request data
    n_pic=request.json
    if data:
        # for every picture in the data
        for pic in data:
            # if the pic already exists
            if n_pic["id"]==pic["id"]:
                return jsonify({"Message": f"picture with id {pic['id']} already present"}), 302
        # add the picture to the data
        data.append(n_pic)
        return jsonify(id=n_pic["id"], message="Picture with id "+str(n_pic["id"])+" was added to the collection"), 201

######################################################################
# UPDATE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    n_pic=request.json
    if data:
        # for every picture in the data
        for i in range(len(data)):
            if data[i]["id"]==id:
                data[i]=n_pic
                return jsonify(message="Picture updated"), 201
        return jsonify({"message": "picture not found"}), 404

######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    if data:
        # for every picture in the data
        for i in range(len(data)):
            if data[i]["id"]==id:
                del data[i]
                return jsonify(message="Picture deleted"), 204
        return jsonify({"message": "picture not found"}), 404

                
