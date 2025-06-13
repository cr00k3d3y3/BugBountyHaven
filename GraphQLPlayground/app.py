from flask import Flask, request, render_template, g, redirect, url_for
from flask_graphql import GraphQLView
import sqlite3, os
import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import Column, Integer, String as SQLAString, create_engine
from graphene import ObjectType, String as GrapheneString, List, Schema


# Flask + Graphene setup
app = Flask(__name__)
app.secret_key = "ultrasecret"
DATABASE = "data.db"
Base = declarative_base()
engine = create_engine(f"sqlite:///{DATABASE}")
SessionLocal = scoped_session(sessionmaker(bind=engine))

# ORM models
# SQLAlchemy model
class UserModel(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(SQLAString)
    email = Column(SQLAString)
    role = Column(SQLAString, default="user")


# Graphene types
class User(ObjectType):
    id = GrapheneString()
    username = GrapheneString()
    email = GrapheneString()
    role = GrapheneString()


class Query(ObjectType):
    all_users = List(User)

    def resolve_all_users(root, info):
        # Simulate role-based access control
        role = info.context.get('role', 'user')  # default to 'user'

        cur = get_db().cursor()
        if role != 'admin':
            # Limit result for regular users
            cur.execute("SELECT id, username FROM users")
            return [User(id=str(row[0]), username=row[1]) for row in cur.fetchall()]
        else:
            # Full info for admins
            cur.execute("SELECT id, username, email, role FROM users")
            return [User(id=str(row[0]), username=row[1], email=row[2], role=row[3]) for row in cur.fetchall()]


schema = graphene.Schema(
    query=Query,
    types=[User],
)

# Initialize and seed DB if not exists

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

def init_db():
    if not os.path.exists(DATABASE):
        Base.metadata.create_all(bind=engine)
        session = SessionLocal()
        session.add_all([
            UserModel(username="admin", email="admin@secret.local", role="admin"),
            UserModel(username="guest", email="guest@example.com", role="user"),
        ])
        session.commit()
        session.close()

init_db()

# GraphQL endpoint with GraphiQL IDE
app.add_url_rule(
    '/graphql',
    view_func=GraphQLView.as_view(
        'graphql',
        schema=schema,
        graphiql=True,
        get_context=lambda: {'request': request, 'role': request.cookies.get('role', 'user')}
    )
)

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route("/")
def home():
    return render_template("/index.html")



@app.route('/submit_flag', methods=['GET', 'POST'])
def submit_flag():
    result = ''
    if request.method == 'POST':
        username = request.form['username']
        submitted_flag = request.form['flag']
        cur = get_db().cursor()
        cur.execute("SELECT challenge_name FROM flags WHERE flag_value = ?", (submitted_flag,))
        row = cur.fetchone()
        if row:
            challenge = row[0]
            cur.execute("SELECT * FROM submissions WHERE flag_value = ? AND username = ?", (submitted_flag, username))
            if not cur.fetchone():
                cur.execute("INSERT INTO submissions (username, flag_value, challenge_name) VALUES (?, ?, ?)",
                            (username, submitted_flag, challenge))
                get_db().commit()
                result = f"✅ Flag accepted for challenge: {challenge}"
            else:
                result = "❗️ Flag already submitted."
        else:
            result = "❌ Invalid flag."
    return render_template('submit_flag.html', result=result)


@app.route('/graphql_discovery')
def graphql_discovery():
    return render_template("graphql_discovery.html", hint="Try bruteforcing GraphQL paths using tools or browser dev tools.")


@app.route('/broken_access_tutorial')
def broken_access_tutorial():
    return render_template("broken_access_tutorial.html")


@app.route('/scoreboard')
def scoreboard():
    cur = get_db().cursor()
    cur.execute("SELECT username, challenge_name, timestamp FROM submissions ORDER BY timestamp DESC")
    rows = cur.fetchall()
    return render_template('scoreboard.html', rows=rows)




if __name__ == "__main__":
    app.run(port=80, host="0.0.0.0")
