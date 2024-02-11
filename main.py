import sys

import ticket_text
import tickets_db


tt = ticket_text.TicketText()
db = tickets_db.TicketsDB()


class MercadonaTicket:
    def __init__(self):
        return

    def main(self, filename: str) -> None:
        """
        Function to control the flow of the program

        :param filename: str
        :return: None
        """
        ticket = tt.open_pdf_ticket(filename)
        ticket_data = tt.analyze_ticket(ticket)
        print("TICKET_DATA:")
        print(ticket_data)
        db.store_db_ticket(ticket_data)

        return


if __name__ == "__main__":
    mt = MercadonaTicket()

    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        print("You have to provide a PDF file as argument!")
        exit()

    mt.main(filename)
