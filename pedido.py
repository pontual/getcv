import locale
import requests
from secrets import GET_URL, PASSWORD

ENTER_DESC = "$ Enter desc (%) "
desc = None
ct = 0

if __name__ == "__main__":
    locale.setlocale(locale.LC_ALL, 'Portuguese_Brazil.1252')

    while desc is None:
        try:
            desc = int(input(ENTER_DESC))
        except ValueError:
            print("desc not valid.")
        ct = 0
        grand_tot = 0

    while True:
        inp = input("Qtde, cod, 0/q to quit, r to reset ({} items so far, -{}%): ".format(ct, desc))
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
            ct = 0
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
            ct += 1
            grand_tot += subtot

            print()
            print(" >>>>>> subtot {}, grand tot {} item {:.04f} (-%{}) ".format(
                locale.currency(subtot, grouping=True),
                locale.currency(grand_tot, grouping=True),
                item, desc))
            print()
            

    print()
    print(">>> {} items. Grand tot {}".format(ct, locale.currency(round(grand_tot, 4), grouping=True)))
    print()
