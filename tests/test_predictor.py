import json

def test_predict_item_on_buybox(client, admin_headers):
    resp = client.post('/api/v1/predict', headers=admin_headers, json={
        "seller_positive_feedback_rating":98.0,
        "feedback_count":85,
        "is_fullfilled_by_amazon":True,
        "price":25.60,
        "maximum_hours":0.0,
        "is_featured_merchant":True,
        "shipping_price":0.00
    })

    data = json.loads(resp.data)

    assert resp.status_code == 201
    assert data["result"] == True

def test_predict_item_is_not_on_buybox(client, admin_headers):
    resp = client.post('/api/v1/predict', headers=admin_headers, json={
        "seller_positive_feedback_rating":80.0,
        "feedback_count":503,
        "is_fullfilled_by_amazon":False,
        "price":22.94,
        "maximum_hours":0.0,
        "is_featured_merchant":True,
        "shipping_price":3.99
    })

    data = json.loads(resp.data)

    assert resp.status_code == 201
    assert data["result"] == False