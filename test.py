import ticket_text


tt = ticket_text.TicketText()


def test_open_pdf_ticket():
    text = tt.open_pdf_ticket("20231130 Mercadona 50,56 €.pdf")['datetime']
    assert text == "30/11/2023 19:52"
