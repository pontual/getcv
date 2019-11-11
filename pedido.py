import locale
import requests
from secrets import GET_URL, PASSWORD

ENTER_DESC = "$ Enter desc (%) "
desc = None
ct = 0
labels = {8: 'SPEC. EIGHT',
          9: 'EXTRA NINE',
          10: 'EXTRA TEN',
          11: 'EXTRA ELEVEN',
          7: 'SPEC. SEVEN',
          6: 'STANDARD',
          15: "FIFTEEN",
          20: "TWENTY",
          25: "TWENTY-FIVE",
          30: "THIRTY",
          40: "FORTY",
          50: "FIFTY",
          0: 'ZERO'}

if __name__ == "__main__":
    locale.setlocale(locale.LC_ALL, 'Portuguese_Brazil.1252')

    while desc is None:
        try:
            desc = input(ENTER_DESC)
            if desc == "q":
                print("Quitting.")
                exit(0)
            desc = int(desc)
        except ValueError:
            print("desc not valid.")
            desc = None
        ct = 0
        grand_tot = 0
        summary = ""

    while True:
        inp = input("Qtd cod or q, 0/r ({} items, -{}%) {}: ".format(ct, desc, labels[desc]))
        if inp == 'r' or inp == '0':
            print()
            print(summary)
            print(">>> {} items. Grand tot {}".format(ct, locale.currency(round(grand_tot, 4), grouping=True)))
            print()
            print("Resetting.")
            desc = None
            while desc is None:
                try:
                    desc = input(ENTER_DESC)
                    if desc == "q":
                        print("Quitting.")
                        exit(0)
                    desc = int(desc)
                except ValueError:
                    print("desc not valid.")
                    desc = None
            ct = 0
            grand_tot = 0
            summary = ""
            continue
        
        if inp == '':
            continue

        if inp == 'q':
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
        if cv is None or "--" in cv:
            print("Cod", cod, "not found or out of stock")
        else:
            p, q = cv.split(" / ")
            p = int(p)
            item = round((1 - desc / 100) * p * 0.03, 4)
            subtot = round(item * qtde, 4)
            ct += 1
            grand_tot += subtot
            summary_line = "{} {:.04f} (-%{})".format(
                cod.ljust(9),
                item, desc)
            item_line = "> it {:.04f} (-%{}) s.tot {}, g.tot {} it {:.04f} (-%{}) ".format(
                item, desc,
                locale.currency(subtot, grouping=True),
                locale.currency(grand_tot, grouping=True),
                item, desc)
            summary += summary_line + "\n"
            
            print()
            print(item_line)
            print()
            

    print()
    print(summary)
    print()
    print(">>> {} items. Grand tot {}".format(ct, locale.currency(round(grand_tot, 4), grouping=True)))
    print()
