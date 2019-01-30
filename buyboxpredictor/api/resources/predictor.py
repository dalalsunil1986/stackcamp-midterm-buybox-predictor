import os
from flask import request, current_app
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required

import json
import numpy as np
from buyboxpredictor.lib import Predictor
import werkzeug
from werkzeug.utils import secure_filename


class PredictorResource(Resource):

    method_decorators = [jwt_required]

    def validate_inputs(self):        

        parser = reqparse.RequestParser()
        parser.add_argument('seller_positive_feedback_rating', required=True, type=float, help='Data must be a float.')
        parser.add_argument('feedback_count', required=True, type=int, help='Data must be integer.')
        parser.add_argument('is_fullfilled_by_amazon', required=True, type=bool, help='Data must be boolean.')
        parser.add_argument('price', required=True, type=float, help='Data must be float.')
        parser.add_argument('maximum_hours', required=True, type=float, help='Data must be float.')
        parser.add_argument('is_featured_merchant', required=True, type=bool, help='Data must be boolean.')
        parser.add_argument('shipping_price', required=True, type=float, help='Data must be float.')

        return parser

    def post(self):

        parser = self.validate_inputs()

        inputs = parser.parse_args()

        predictor = Predictor()

        data_inputs = []

        try:
            data_inputs.append(inputs["seller_positive_feedback_rating"])
            data_inputs.append(inputs["feedback_count"])
            data_inputs.append(inputs["is_fullfilled_by_amazon"])
            data_inputs.append(inputs["price"])        
            data_inputs.append(inputs["maximum_hours"])
            data_inputs.append(inputs["is_featured_merchant"])
            data_inputs.append(inputs["shipping_price"])        
        except:
            return {"error:":self.error_msg_bad_input}, 400

        try:
            result = predictor.predict(data_inputs)

            msg = "Item is Impossible to be on the BuyBox."
            if result == True:
                msg = "Item is Possible to be on the BuyBox."

            return {"result": result, "msg": msg}, 201

        except:

            return {"error:":self.error_msg_internal_server_error}, 400

    error_msg_bad_input = """
        Bad inputs. Make sure your input has these variables with the following order : 
        - seller_positive_feedback_rating
        - feedback_count
        - is_fullfilled_by_amazon
        - price
        - maximum_hours
        - is_featured_merchant
        - shipping_price
    """

    error_msg_internal_server_error = """
        Something wrong on the API Server. Contact API Developer.
    """
        
class UploadPredictorModel(Resource):

    method_decorators = [jwt_required]    

    def allowed_file(self,filename):
        ALLOWED_EXTENSIONS = set(['h5'])
        return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    def post(self):
        inputs = request.files

        model_file = inputs['model_file']

        if model_file.filename == '':
            return {"error:":"File not found."}, 400

        if model_file.filename != 'buybox_predictor_model.h5':
            return {"error:":"File name must be : buybox_predictor_model.h5"}, 400
        
        if model_file and self.allowed_file(model_file.filename):
            filename = secure_filename(model_file.filename)
            
            try:
                model_file.save(os.path.join(current_app.root_path+'/lib/', filename))
                return {"success":"Model uploaded successfully."}, 200
            except:
                return {"error":"Failed to upload your model."}, 501
        else:
            return {"error:":"File extensions must be : .h5"}, 400
            
            




