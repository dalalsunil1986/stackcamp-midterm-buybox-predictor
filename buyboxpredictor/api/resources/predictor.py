from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required

import json
import numpy as np
from app.buyboxpredictor.lib import Predictor

class PredictorResource(Resource):

    method_decorators = [jwt_required]
    
    def post(self):
        predictor = Predictor()
        inputs = request.json

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
        