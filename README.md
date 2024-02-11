### MERCADONA TICKETS ###

This is a program which target is to analyze all online Mercadona tickets (Mercadona is a grocery store chain from 
Spain).

The program is made with sqlalchemy and creates their own SQLLite3 database, you can change by another database
easily.


# INSTALL

You only have to install the requirements file and then start the program:

```
pip3 install -r requirements.txt
python3 main.py [a mercadona ticket PDF file]
```

# TO DO

Still many things to add, like a way to read the ticket correctly, with current version 1.0 the program can't separate
quantity from articles names and could be errors with some articles that begins with a number.

Tests are made but still a lot of work pending here.

I want to add graphs with matplotlib that shows the articles most frquently buyed, the articles that cost more, and 
more stats.

This program is not intended to be a big project, but I liked to make a program for this and control my own expenses on
Mercadona stores, there are a lot of room to improve this program from this initial point, but I have another projects 
in mind right now and I wanted to upload this program before switch to other most ambitious projects.

Still there is room to extend the program for tickets of another grocery stores, maybe with a OCR from mobile photos
from other tickets that are not in electronic format.
