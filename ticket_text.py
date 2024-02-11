import PyPDF2 as pdf2
import re


class TicketText:
    def __init__(self):
        self.exception_line = 0
        self.multiple_row = ""

        return

    def open_pdf_ticket(self, filename: str) -> str:
        """
        Function to open the PDF ticket and get the content text

        :param filename: str
        :return: str
        """
        ticket = ""

        # -- open PDF file --
        with open(filename, "rb") as fp:
            pdf = pdf2.PdfReader(fp)

            for page in pdf.pages:
                ticket += page.extract_text()

        return ticket

    def get_ticker_header(self, ticket: str, ticket_data: dict) -> dict:
        """
        Function to get ticket header data

        :param ticket: str
        :param ticket_data: dict
        :return: dict
        """
        lines = ticket.split("\n")

        tmp = lines[4].split(" ")
        datetime = tmp[0]+" "+tmp[1]
        tmp = lines[5].split(" ")
        id_number = tmp[2]

        ticket_data['address'] = lines[1]+" - "+lines[2]
        ticket_data['datetime'] = datetime
        ticket_data['id_number'] = id_number

        return ticket_data

    def get_ticker_footer(self, ticket: str, ticket_data: dict) -> dict:
        """
        Function to get ticket footer values like VAT and totals

        :param ticket: str
        :param ticket_data: dict
        :return: dict
        """
        ticket = ticket.replace(",", ".")
        for row in ticket.split("\n"):
            if row.find("10%") == 0:
                tmp = row.split(" ")
                ticket_data['VAT_10'] = tmp[1]
            if row.find("21%") == 0:
                tmp = row.split(" ")
                ticket_data['VAT_21'] = tmp[1]
            if row.find("0%") == 0:
                tmp = row.split(" ")
                ticket_data['VAT_0'] = tmp[1]
            if row.find("TOTAL (€)") == 0:
                tmp = row.split(" ")
                ticket_data['total'] = tmp[2]
            if ticket_data['VAT_0'] != "" and row.find("TOTAL") == 0:
                tmp = row.split(" ")
                ticket_data['net_total'] = tmp[1]
                ticket_data['VAT_total'] = tmp[2]

        return ticket_data

    def get_article_details(self, row: str) -> dict:
        """
        Function to get article details from each row individually
        :param row: str
        :return: dict
        """
        ticket_row = {
            'amount': 0,
            'article': "",
            'unit_price': 0.00,
            'total_price': 0.00
        }
        row = row.replace(",", ".")

        # -- get article details and set article in different lines --
        tmp = row.split(" ")
        if len(tmp) == 1:
            self.exception_line = 1

        # -- articles that begin with a number and could fail --
        if self.exception_line == 0:
            # -- this part is for normal article lines --
            if row.find("200 SERVIL. BLANCAS") > 0 \
                    or row.find("12 HUEVOS GRANDES") > 0:
                amount = tmp[0][0]
                tmp[0] = tmp[0][1:]
            else:
                amount = re.split(r'\D', tmp[0])[0]
                tmp[0] = tmp[0].replace(amount, "")
            ticket_row['amount'] = int(amount)

            # -- get article unit_price, total price and name --
            ticket_row['total_price'] = float(tmp[-1])
            if int(amount) > 1:
                ticket_row['unit_price'] = float(tmp[-2])
                for item in range(0, len(tmp) - 2):
                    ticket_row['article'] += tmp[item] + " "
            else:
                ticket_row['unit_price'] = float(tmp[-1])
                for item in range(0, len(tmp) - 1):
                    ticket_row['article'] += tmp[item] + " "
            ticket_row['article'] = ticket_row['article'].strip()
        else:
            # -- this part is for compound article lines --
            if len(row.split(" ")) > 1:
                self.exception_line = 0
                tmp = row.split(" ")
                print("TMP:")
                print(tmp)
            self.multiple_row += row + " "

        return ticket_row

    def get_ticket_lines(self, ticket: str, ticket_data: dict) -> dict:
        """
        Function to get all ticket article details lines

        :param ticket: str
        :param ticket_data: dict
        :return: dict
        """
        get_lines = 0

        # -- loop to capture real ticket lines --
        ticket = ticket.replace(",", ".")
        for row in ticket.split("\n"):
            # -- stop ticket lines capture --
            if row.find("TOTAL") == 0 or row.find("ENTRADA") == 0:
                get_lines = 0

            # -- define empty ticket line before processing and make initial cleaning --
            if get_lines == 1:
                # -- add article line to ticket lines --
                ticket_row = self.get_article_details(row)
                ticket_data['lines'].append(ticket_row)

            # -- init ticket lines capture --
            if row.find("Descripción") == 0:
                get_lines = 1

        return ticket_data

    def analyze_ticket(self, ticket: str) -> dict:
        """
        Function to get all details from the ticket

        :param ticket: str
        :return: dict
        """
        ticket_data = {
            'address': "",
            'datetime': "",
            'id_number': "",
            'net_total': 0.00,
            'VAT_10': 0.00,
            'VAT_21': 0.00,
            'VAT_0': 0.00,
            'VAT_total': 0.00,
            'total': 0.00,
            'lines': []
        }

        # DEBUG #######################
        for i in ticket.split("\n"):
            print(i)
        print("----------------------")
        # DEBUG #######################

        # -- get different parts of the ticket values --
        ticket_data = self.get_ticker_header(ticket, ticket_data)
        ticket_data = self.get_ticker_footer(ticket, ticket_data)
        ticket_data = self.get_ticket_lines(ticket, ticket_data)

        return ticket_data
