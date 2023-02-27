import sqlalchemy

metadata = sqlalchemy.MetaData()
contact_form = sqlalchemy.Table(
    "contact_form",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True),
    sqlalchemy.Column("name", sqlalchemy.String(length=50), nullable=True),
    sqlalchemy.Column("mobile", sqlalchemy.String(length=10), nullable=False),
    sqlalchemy.Column("email", sqlalchemy.String(length=100), nullable=False),
    sqlalchemy.Column("message", sqlalchemy.String(length=1000), nullable=False),
    #sqlalchemy.Column("ip_address", sqlalchemy.String(length=100), nullable=False),
    sqlalchemy.Column("browser_type", sqlalchemy.String(length=255), nullable=False),
    sqlalchemy.Column("created_date", sqlalchemy.DateTime, nullable=False)
)
