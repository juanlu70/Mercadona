from sqlalchemy import Column, Integer, String, Float, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os


Base = declarative_base()


class Tickets(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, nullable=False)
    address = Column(String(255))
    datetime = Column(String(10))
    id_number = Column(Integer)
    net_total = Column(Float)
    vat_10 = Column(Float)
    vat_21 = Column(Float)
    vat_0 = Column(Float)
    vat_total = Column(Float)
    total = Column(Float)


class TicketLines(Base):
    __tablename__ = "ticket_lines"

    id = Column(Integer, primary_key=True, nullable=False)
    ticket_id = Column(Integer)
    amount = Column(Integer)
    article = Column(String(255))
    unit_price = Column(Float)
    total_price = Column(Float)


class TicketsDB:
    def __init__(self):
        path = os.path.dirname(os.path.abspath(__file__))
        self.db_file = os.path.join(path, "mercadona.db")

        return

    def store_header(self, ticket_data: dict) -> None:
        engine = create_engine('sqlite:///' + self.db_file, echo=False)
        Base.metadata.create_all(bind=engine)
        session = sessionmaker(bind=engine)
        session = session()

        ticket = Tickets(
            address=ticket_data['address'],
            datetime=ticket_data['datetime'],
            id_number=ticket_data['id_number'],
            net_total=ticket_data['net_total'],
            vat_10=ticket_data['VAT_10'],
            vat_21=ticket_data['VAT_21'],
            vat_0=ticket_data['VAT_0'],
            vat_total=ticket_data['VAT_total'],
            total=ticket_data['total']
        )
        session.add(ticket)
        session.commit()

        return

    def store_lines(self, ticket_data: dict) -> None:
        engine = create_engine('sqlite:///' + self.db_file, echo=False)
        Base.metadata.create_all(bind=engine)
        session = sessionmaker(bind=engine)
        session = session()

        last_ticket = session.query(Tickets).order_by(Tickets.id).first()

        for row in ticket_data['lines']:
            data = TicketLines(
                ticket_id=last_ticket.id,
                amount=row['amount'],
                article=row['article'],
                unit_price=row['unit_price'],
                total_price=row['total_price']
            )
            session.add(data)
        session.commit()

        return

    def store_db_ticket(self, ticket_data: dict) -> None:
        self.store_header(ticket_data)
        self.store_lines(ticket_data)

        return
