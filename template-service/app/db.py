import os

from sqlmodel import Session, SQLModel, create_engine, select

from .models import Template

# Load the Postgres DSN (connection string) from environment variables
PG_DSN = os.getenv("PG_DSN")

# Create the SQLAlchemy engine that connects to your database
engine = create_engine(PG_DSN)  # type: ignore


# create tables if they don't exist
def init_db():
    SQLModel.metadata.create_all(engine)
    print("Database initialized and tables created (if not exist).")


# close the database connection cleanly
def close_db_connection():
    engine.dispose()
    print("Database connection closed.")


# Session function
def getSession():
    with Session(engine) as session:
        yield session


# get template by ID
def getTemplateById(session: Session, id: str):
    query = select(Template).where(Template.template_id == id)
    return session.exec(query).first()


# write template to database
def writeTemplate(session: Session, template: Template):
    session.add(template)
    session.commit()
    session.refresh(template)
