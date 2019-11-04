import locale
import requests
from secrets import GET_URL, PASSWORD

ENTER_DESC = " $ Enter desc (%) "
desc = None

if __name__ == "__main__":
    locale.setlocale(locale.LC_ALL, 'Portuguese_Brazil.1252')

    while desc is None:
        try:
            desc = int(input(ENTER_DESC))
        except ValueError:
            print("desc not valid.")    
        grand_tot = 0

    while True:
        inp = input("Enter qtde and cod, 0/q to quit, r to reset: ")
        if inp == 'r':
            print()
            print("Resetting.")
            desc = None
            while desc is None:
                try:
                    desc = int(input(ENTER_DESC))
                except ValueError:
                    print("desc not valid.")    
            print()
            grand_tot = 0
            continue
        
        if inp == '':
            continue

        if inp == '0' or inp == 'q':
            break

        if len(inp.split()) != 2:
            # assume only codigo was entered
            print("Assuming 1 pc.")
            qtde = 1
            cod = inp

        else:
            qtde, cod = inp.split()
            qtde = int(qtde)
        
        response = requests.get(GET_URL + f"?c={cod}&s={PASSWORD}")
        cv = response.json()['cv']
        if cv is None:
            print("Cod", cod, "not found")
        else:
            p, q = cv.split(" / ")
            p = int(p)
            item = round((1 - desc / 100) * p * 0.03, 4)
            subtot = round(item * qtde, 4)
            grand_tot += subtot

            print()
            print(" >>>>>> item -%{}: {:.04f} subtot {}, grand tot {}".format(desc, item, locale.currency(subtot, grouping=True), locale.currency(grand_tot, grouping=True)))
            print()
            

    print()
    print(">>> Grand tot {}".format(locale.currency(round(grand_tot, 4), grouping=True)))
    print()
