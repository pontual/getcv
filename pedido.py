import requests
from secrets import GET_URL, PASSWORD

if __name__ == "__main__":
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
            print("item", item, "tot", subtot)
            grand_tot += subtot

    print("Grand tot", round(grand_tot, 4))
