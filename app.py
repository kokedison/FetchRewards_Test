from flask import jsonify, request, render_template
import datetime
from functools import wraps
from marshmallow import ValidationError
from werkzeug.exceptions import BadRequest

from . import app, db, auth
from .models import Transaction, User
from .schema import TransactionSchema, SpendPointsSchema


@auth.verify_token
def verify_token(token):
    '''
    Verify that the incoming request has the expected token.
    '''
    if token:
        userID = User.decode_auth_token(token)
        return User.query.filter_by(id=userID).first()
    
    return None

@auth.error_handler
def auth_error(status):
    '''
    Authorization error handler.
    '''
    return "Access Denied.", status

def requiredParams(schema):
    '''
    Decorator for checking parameters match the provided schema
    '''
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            try:
                schema.load(request.get_json())
            except ValidationError as err:
                error = {
                    "status": "error",
                    "messages": err.messages
                }
                return jsonify(error), 400
            except BadRequest as err:
                error = {
                    "status": "error",
                    "messages": "Payload must be a valid JSON"
                }
                print(type(err))
                print(err)
                return jsonify(error), 400
                
            return fn(*args, **kwargs)
 
        return wrapper
    return decorator

@app.route('/transactions', methods=['POST'])
@auth.login_required
@requiredParams(TransactionSchema())
def addTransaction():
    '''
    Add one new transaction
    '''
    newTransaction = Transaction(
        payer = request.json['payer'],
        points = request.json['points'],
        remainingPoints = request.json['points'],
        timestamp = datetime.datetime.strptime(request.json['timestamp'], '%Y-%m-%dT%H:%M:%SZ'),
        user = auth.current_user()
    )
    db.session.add(newTransaction)
    db.session.commit()         

    return jsonify({'status': 'success', 'message': 'New transaction added.'})

@app.route('/transactions/multiple', methods=['POST'])
@auth.login_required
@requiredParams(TransactionSchema(many=True))
def addMultipleTransactions():
    '''
    Add multiple transactions into database
    '''
    
    for t in request.json:
        newTransaction = Transaction(
            payer = t['payer'],
            points = t['points'],
            remainingPoints = t['points'],
            timestamp = datetime.datetime.strptime(t['timestamp'], '%Y-%m-%dT%H:%M:%SZ'),
            user = auth.current_user()
        )
        db.session.add(newTransaction)
    db.session.commit()          
    
    return jsonify([t.to_dict() for t in Transaction.query.filter_by(userID=auth.current_user().id).all()])

@app.route('/spend', methods=['POST'])
@auth.login_required
@requiredParams(SpendPointsSchema())
def spendPoints():
    '''
    Spend user's points
    '''
    points = int(request.json['points'])

    payersRecord = {}
    transactions = Transaction.query.filter(Transaction.userID==auth.current_user().id, 
                                    Transaction.remainingPoints != 0).order_by(Transaction.timestamp).all()
    
    for t in transactions:
        if t.payer not in payersRecord:
            payersRecord[t.payer] = 0

        if t.remainingPoints >= points:
            payersRecord[t.payer] -= points
            t.remainingPoints -= points
            break
        else:
            payersRecord[t.payer] -= t.remainingPoints
            points -= t.remainingPoints
            t.remainingPoints = 0
    else:
        if points != 0:
            return {'status': 'error', 'message': 'Not enough points to spend.'}, 400

    res = []
    for payer, points in payersRecord.items():
        transaction = Transaction(payer=payer, 
                                  points=points, 
                                  remainingPoints = 0,
                                  timestamp=datetime.datetime.now(), 
                                  user=auth.current_user())
        db.session.add(transaction)
        res.append({'payer': payer, 'points': points})
    
    db.session.commit()

    res.sort(key=lambda x: x['points'], reverse=True)
    return jsonify(res)


@app.route('/balance', methods=['GET'])
@auth.login_required
def getBalance():
    '''
    Get user's balance from different payers
    '''
    transactions = Transaction.query.filter_by(userID=auth.current_user().id).all()
    payersRecord = {}

    for t in transactions:
        payersRecord[t.payer] = payersRecord.get(t.payer, 0) + t.points

    return jsonify(payersRecord)


@app.route('/api/docs')
def get_docs():
    print('sending docs')
    return render_template('swaggerui.html')

if __name__ == '__main__':
    app.run()