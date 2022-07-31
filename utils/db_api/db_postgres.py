from gino import Gino
from sqlalchemy import (Column, Integer, BigInteger, String,
                        ForeignKey, Boolean)

from data.config import DB_USER, DB_PASS, IP

db = Gino()


class Role(db.Model):
    __tablename__ = 'role'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(100), unique=True, nullable=False)

    def __repr__(self):
        return f"Role(id='{self.id}', title='{self.title}'"


class User(db.Model):
    __tablename__ = 'users'

    chat_id = Column(BigInteger, primary_key=True)
    role_id = Column(Integer, ForeignKey('role.id'))
    full_name = Column(String(100), unique=True)
    email = Column(String(100), nullable=False)
    online = Column(Boolean, default=True)
    kodland_id = Column(Integer, ForeignKey('kodland_users.id'))

    def __repr__(self):
        return f"User(id='{self.chat_id}', fullname='{self.full_name}')"


class KodlandUser(db.Model):
    __tablename__ = 'kodland_users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(100), nullable=False)
    login = Column(String(100), nullable=False)
    password = Column(String(100), nullable=False)
    role_id = Column(Integer, ForeignKey('role.id'))


async def authorization_kodland(login, password):
    kodland_user = await KodlandUser.query.where(KodlandUser.login == login).gino.first()
    if kodland_user is not None:
        return kodland_user.password == password
    return False


async def check_role_by_user_id(user_id, role_title):
    user = await User.get(user_id)
    role = await Role.query.where(Role.title == role_title).gino.first()
    return user.role_id == role.id


async def create_user(user_id, full_name, kodland_user):
    await User.create(chat_id=user_id, role_id=kodland_user.role_id, full_name=full_name,
                      email=kodland_user.email, kodland_id=kodland_user.id)


async def get_user_by_id(user_id):
    return await User.get(user_id)


async def get_user_by_kodland_user_id(kodland_user_id):
    return await User.query.where(User.kodland_id == kodland_user_id).gino.first()


async def get_kodland_user_by_login(login):
    return await KodlandUser.query.where(KodlandUser.login == login).gino.first()


async def get_kodland_user_by_email(email):
    return await KodlandUser.query.where(KodlandUser.email == email).gino.first()


async def get_role_by_id(role_id):
    return await Role.get(role_id)


async def get_role_by_title(title):
    return await Role.query.where(Role.title == title).gino.first()


async def get_support_users():
    support_role_id = await get_role_by_title("support")
    return await User.query.where(User.role_id == support_role_id.id).gino.all()


async def fill_kodland_users():
    await KodlandUser.create(email="a.shishkin@kodland.team", login="ashishkin", password="12345", role_id=1)
    await KodlandUser.create(email="test@kodland.team", login="qwe", password="12345", role_id=2)


async def fill_roles():
    await Role.create(title='support')
    await Role.create(title='teacher')
    await Role.create(title='student')


async def create_db():
    await db.set_bind(f'postgresql://{DB_USER}:{DB_PASS}@{IP}/supportDB')
    await db.gino.drop_all()
    await db.gino.create_all()
    await fill_roles()
    await fill_kodland_users()
