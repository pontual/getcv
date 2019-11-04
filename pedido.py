import locale
import requests
from secrets import GET_URL, PASSWORD

if __name__ == "__main__":
    locale.setlocale(locale.LC_ALL, 'Portuguese_Brazil.1252')
    
    desc = int(input("Enter desc "))
    grand_tot = 0

    while True:
        inp = input("Enter a qtde and codigo, 0 or q to stop ")
        if inp == '':
            continue

        if inp == '0' or inp == 'q':
            break

        if len(inp.split()) != 2:
            print("invalid input. try again")
            continue
        
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
            print()
            print(" >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> item {} tot {}".format(item, locale.currency(subtot, grouping=True)))
            print()
            
            grand_tot += subtot

    print()
    print(">>> Grand tot {}".format(locale.currency(round(grand_tot, 4), grouping=True)))
    print()
