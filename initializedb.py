from . import db
from .models import User

if __name__ == '__main__':
    db.drop_all()
    db.create_all()
    db.session.add(User())
    db.session.add(User())    
    db.session.commit()
    
    for user in User.query.all():
        print(f'auth_token: {user.encode_auth_token(user.id)}')
