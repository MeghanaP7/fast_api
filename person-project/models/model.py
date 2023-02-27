import sqlalchemy

# Creating a table
person_metadata = sqlalchemy.MetaData()
person = sqlalchemy.Table(
"person",
person_metadata,
sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True),
sqlalchemy.Column("name", sqlalchemy.String(length=250), nullable=True),
sqlalchemy.Column("city", sqlalchemy.String(length=250), nullable=True),
sqlalchemy.Column("salary", sqlalchemy.Integer, nullable=True)
)