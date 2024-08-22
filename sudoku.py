#pro nahrání na web:
from flask import Flask, render_template, request
import random

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def zapoctak():

      
      if request.method == "POST":
      #uživatel po nás něco chce :D
            
            if request.form['action'] == 'Ukázat řešení':
                  #pouze vypíšeme obsah reseni.txt
                  vysledek = [[0]*9 for x in range(9)]
                  reseni = open("reseni.txt")

                  a = 0
                  b = 0
                  for x in reseni:
                        vysledek[a][b] = x
                        b = b + 1
                        if b > 8:
                              a = a + 1
                              b = 0
                  return render_template('kontrola.html', sudoku = vysledek, kontrola = [["spravne"]*9 for _ in range(9)], zprava = None)


            if request.form['action'] == 'Nové zadání' or request.form['action'] == 'Chci si zahrát sudoku':
                  #generujeme zadání
                  zadani = generovat()
                  for x in range(9):
                        for y in range(9):
                              if zadani[x][y] == 0:
                                    zadani[x][y] = ""

                  return render_template('zadani.html', sudoku = zadani, zprava = None)

            
            if request.form['action'] == 'Pokračovat v řešení':
                  #otevřeme uživatelovo řešení a správné řešení, shodující se hodnoty necháme,
                  #neshodující se hodnoty smažeme
                  uzivatelovo_reseni = open("uzivatelovo_reseni.txt")
                  reseni = open("reseni.txt")
                  vysledek =[[0]*9 for _ in range(9)]
                  
                  a = 0
                  b = 0
                  for x in uzivatelovo_reseni:
                        x = x.split("\n")
                        vysledek[a][b] = x[0]
                        b = b + 1
                        if b > 8:
                              a = a + 1
                              b = 0

                  a = 0
                  b = 0
                  for x in reseni:
                        x = x.split("\n")
                        if x[0] != vysledek[a][b]:
                              vysledek[a][b] = ""
                        b = b + 1
                        if b > 8:
                              a = a + 1
                              b = 0

                  return render_template('zadani.html', sudoku = vysledek,
                                    zprava = "Chyby v řešení byly smazány")
            

            if request.form['action'] == 'Zpět na úvod' or request.form['action'] == 'Smazat':
                  #vrátíme úvodní stránku
                  return render_template('sudoku.html', sudoku = [[""]*9 for _ in range(9)], zprava = None)

            
            for a in range(9):
                  for b in range(9):
                        vars()["pole_" + str(a+1) + str(b+1)] = request.form["pole_" + str(a+1) + str(b+1)]
    
            if request.form['action'] == 'Vyřešit':
                  #zacina_sranda
                  reseni = [[0]*9 for _ in range(9)]
                  zaskodnik = False

                  #zjistíme hodnoty ve formuláři
                  for a in range(9):
                        for b in range(9):
                              x = "pole_" + str(a+1) + str(b+1)
                              if vars()[x] != "":
                                    if vars()[x] in "123456789":
                                          reseni[a][b] = int(vars()[x])
                                    else:
                                          zaskodnik = True
                                          i = str(a+1)
                                          j = str(b+1)

                  if zaskodnik:
                        for a in range(9):
                              for b in range(9):
                                    x = "pole_" + str(a+1) + str(b+1)
                                    reseni[a][b] = vars()[x]
                        return render_template('sudoku.html', sudoku = reseni, zprava = "Neplatná hodnota na pozici {} {}".format(i,j))
                  
                  
                  #uděláme kontrolu, že v řádku, sloupci či čtverci nejsou 2 stejné číslice
                  vysledek = overeni_2(reseni)
                  if vysledek != "ok":
                        for a in range(9):
                              for b in range(9):
                                    x = "pole_" + str(a+1) + str(b+1)
                                    reseni[a][b] = vars()[x]
                        return render_template('sudoku.html', sudoku = reseni, zprava = vysledek)

                  #zde probíhá hlavní výpočet
                  vysledek, reseni = hlavni_funkce(reseni)
                  return render_template('sudoku.html', sudoku = reseni, zprava = vysledek)


            if request.form['action'] == 'Zkontrolovat':
                  #porovnáme uživatelo řešení se správným řešením, pokud se nějaké hodnoty
                  #neshodují, označíme příslušnou buňku červeně
                  kontrola = [["spatne"]*9 for _ in range(9)]
                  reseni = open("reseni.txt")
                  uzivatelovo_reseni = open("uzivatelovo_reseni.txt", "w")
                  uzivatel = [[0]*9 for _ in range(9)]

                  for a in range(9):
                        for b in range(9):
                              x = "pole_" + str(a+1) + str(b+1)
                              print (vars()[x], file=uzivatelovo_reseni)
                              uzivatel[a][b] = vars()[x]
                  uzivatelovo_reseni.close

                  a = 0
                  b = 0
                  z = 0
                  for x in reseni:
                        x = x.split("\n")
                        if uzivatel[a][b] == x[0]:
                              kontrola[a][b] = "spravne"
                              z = z + 1

                        if uzivatel[a][b] == "":
                              kontrola[a][b] = "spravne"
                        b = b + 1
                        if b > 8:
                              a = a + 1
                              b = 0
                  reseni.close

                  return render_template('kontrola.html', sudoku = uzivatel, kontrola = kontrola, zprava = z)
      
      #při prvním načtení vrátíme úvodní stránku
      return render_template('sudoku.html', sudoku = [[""]*9 for _ in range(9)], zprava = None)


#ověření, že v řádku, sloupci či čtverci nejsou 2 stejné číslice
def overeni_2(sudoku):
        #řádky
        for i in range(9):
            seznam = [0]*9
            for j in range(9):
                  if sudoku[i][j] != 0:
                        if seznam[sudoku[i][j]-1] == 0:
                              seznam[sudoku[i][j]-1] = 1
                        else:
                              return "Chyba na pozici {} {}".format(i+1, j+1)

        #sloupce
        for j in range(9):
            seznam = [0]*9
            for i in range(9):
                  if sudoku[i][j] != 0:
                        if seznam[sudoku[i][j]-1] == 0:
                              seznam[sudoku[i][j]-1] = 1
                        else:
                              return "Chyba na pozici {} {}".format(i+1, j+1)

        #ctverce
        a = 0
        while a < 7:
            seznam = [0] * 9
            for i in range(a,a+3):
                  for j in range(0,3):
                        if sudoku[i][j] != 0:
                              if seznam[sudoku[i][j]-1] == 0:
                                    seznam[sudoku[i][j]-1] = 1
                              else:
                                    return "Chyba na pozici {} {}".format(i+1, j+1)
            
            seznam = [0] * 9
            for i in range(a,a+3):
                  for j in range(3,6):
                        if sudoku[i][j] != 0:
                              if seznam[sudoku[i][j]-1] == 0:
                                    seznam[sudoku[i][j]-1] = 1
                              else:
                                    return "Chyba na pozici {} {}".format(i+1, j+1)
            
            seznam = [0] * 9
            for i in range(a,a+3):
                  for j in range(6,9):
                        if sudoku[i][j] != 0:
                              if seznam[sudoku[i][j]-1] == 0:
                                    seznam[sudoku[i][j]-1] = 1
                              else:
                                    return "Chyba na pozici {} {}".format(i+1, j+1)
            
            a = a + 3
        return "ok"


#vytvoříme si množiny, které obsahují všechny přípustné hodnoty pro každé políčku
def inicializace(sudoku):
        #řádky
        pomocny_seznam_1 = [0]*9
        for i in range(9):
            vysledek = {1,2,3,4,5,6,7,8,9}
            for j in range(9):
                  if sudoku[i][j] != 0:
                        mnozina = {0}
                        mnozina.update({sudoku[i][j]})
                        vysledek = vysledek - mnozina
            pomocny_seznam_1[i] = vysledek

        #sloupce
        pomocny_seznam_2 = [0]*9
        for j in range(9):
            vysledek = {0,1,2,3,4,5,6,7,8,9}
            for i in range(9):
                  if sudoku[i][j] != 0:
                        mnozina = {0}
                        mnozina.update({sudoku[i][j]})
                        vysledek = vysledek - mnozina
            pomocny_seznam_2[j] = vysledek
            
            for k in range(9):
                  if sudoku[k][j] == 0:
                        sudoku[k][j] = pomocny_seznam_2[j].intersection(pomocny_seznam_1[k])

        #ctverce
        a = 0
        while a < 7:
            b = 0
            while b < 7:
                vysledek = {0}
                for i in range(a,a+3):
                    for j in range(b,b+3):
                        if type(sudoku[i][j]) is int:
                            vysledek.update({sudoku[i][j]})
                
                for i in range(a,a+3):
                    for j in range(b,b+3):
                        if type(sudoku[i][j]) != int:
                            sudoku[i][j] = sudoku[i][j] - vysledek
                b = b + 3
            a = a + 3

#následující 3 funkce voláme, když má nějaké políčko množinu o velikosti 1, v takovém
#případě doplníme políčko a z ostatních množin, které mají s daným políčkem společný
#řádek, sloupec nebo čtverec číslo smažeme
def radek(x,promenna,sudoku):
      for i in range(9):
            if type(sudoku[x][i]) != int:
                  sudoku[x][i] = sudoku[x][i] - {promenna}

def sloupec(y,promenna,sudoku):
      for i in range(9):
            if type(sudoku[i][y]) != int:
                  sudoku[i][y] = sudoku[i][y] - {promenna}

def ctverec(x,y,promenna,sudoku):
      if x % 3 == 0:
            if y % 3 == 0:
                  for i in range(x,x+3):
                        for j in range(y,y+3):
                              if type(sudoku[i][j]) != int:
                                    sudoku[i][j] = sudoku[i][j] - {promenna}
            
            elif y % 3 == 1:
                  for i in range(x,x+3):
                        for j in range(y-1,y+2):
                              if type(sudoku[i][j]) != int:
                                    sudoku[i][j] = sudoku[i][j] - {promenna}

            elif y % 3 == 2:
                  for i in range(x,x+3):
                        for j in range(y-2,y+1):
                              if type(sudoku[i][j]) != int:
                                    sudoku[i][j] = sudoku[i][j] - {promenna}
#_________________________
      elif x % 3 == 1:
            if y % 3 == 0:
                  for i in range(x-1,x+2):
                        for j in range(y,y+3):
                              if type(sudoku[i][j]) != int:
                                    sudoku[i][j] = sudoku[i][j] - {promenna}
            
            elif y % 3 == 1:
                  for i in range(x-1,x+2):
                        for j in range(y-1,y+2):
                              if type(sudoku[i][j]) != int:
                                    sudoku[i][j] = sudoku[i][j] - {promenna}

            elif y % 3 == 2:
                  for i in range(x-1,x+2):
                        for j in range(y-2,y+1):
                              if type(sudoku[i][j]) != int:
                                    sudoku[i][j] = sudoku[i][j] - {promenna}
#_______________________
      elif x % 3 == 2:
            if y % 3 == 0:
                  for i in range(x-2,x+1):
                        for j in range(y,y+3):
                              if type(sudoku[i][j]) != int:
                                    sudoku[i][j] = sudoku[i][j] - {promenna}
            
            elif y % 3 == 1:
                  for i in range(x-2,x+1):
                        for j in range(y-1,y+2):
                              if type(sudoku[i][j]) != int:
                                    sudoku[i][j] = sudoku[i][j] - {promenna}

            elif y % 3 == 2:
                  for i in range(x-2,x+1):
                        for j in range(y-2,y+1):
                              if type(sudoku[i][j]) != int:
                                    sudoku[i][j] = sudoku[i][j] - {promenna}

#následující 3 funkce nám pomůžou řešit složitější sudoku, jejich účel je následující:
#vysvětlím na řádku: funkce zjistí, jaká čísla chybí na daném řádku, to ví díky
#množinám, které obsahuje každé políčko, postupně potom odečte od každého políčka
# všechny množiny na daném řádku, pokud má potom množina velikost 1, číslo v množině
#doplníme do políčka. Obdobný postup použijeme i pro sloupec a čtverec. Každé políčko
#tedy vyzkoušíme třikrát

def slozity_radek(sudoku):
      x = 0
      uspech = False
      while x < 9:
            seznam = [0]*9
            for y in range(9):
                  if type(sudoku[x][y]) != int:
                        for i in sudoku[x][y]:
                              seznam[i-1] += 1 

            if 1 in seznam:
                  uspech = True
                  for y in range(9):
                        if type(sudoku[x][y]) != int:
                              if (seznam.index(1)+1) in sudoku[x][y]:
                                    sudoku[x][y] = seznam.index(1) + 1
                                    radek(x,sudoku[x][y],sudoku)
                                    sloupec(y,sudoku[x][y],sudoku)
                                    ctverec(x,y,sudoku[x][y],sudoku)
            x += 1
      return uspech


def slozity_sloupec(sudoku):
      y = 0
      uspech = False
      while y < 9:
            seznam = [0]*9
            for x in range(9):
                  if type(sudoku[x][y]) != int:
                        for i in sudoku[x][y]:
                              seznam[i-1] += 1 

            if 1 in seznam:
                  uspech = True
                  for x in range(9):
                        if type(sudoku[x][y]) != int:
                              if (seznam.index(1)+1) in sudoku[x][y]:
                                    sudoku[x][y] = seznam.index(1) + 1
                                    radek(x,sudoku[x][y],sudoku)
                                    sloupec(y,sudoku[x][y],sudoku)
                                    ctverec(x,y,sudoku[x][y],sudoku)
            y += 1
      return uspech


def slozity_ctverec(sudoku):
      a = 0
      uspech = False
      while a < 7:
            b = 0
            while b < 7:
                seznam = [0]*9
                for x in range(a,a+3):
                    for y in range(b,b+3):
                        if type(sudoku[x][y]) != int:
                              for i in sudoku[x][y]:
                                  seznam[i-1] += 1 
                              
                if 1 in seznam:
                    uspech = True
                    for x in range(a,a+3):
                        for y in range(b,b+3):
                              if type(sudoku[x][y]) != int:
                                    if (seznam.index(1)+1) in sudoku[x][y]:
                                          sudoku[x][y] = seznam.index(1) + 1
                                          radek(x,sudoku[x][y],sudoku)
                                          sloupec(y,sudoku[x][y],sudoku)
                                          ctverec(x,y,sudoku[x][y],sudoku)
                b = b + 3
            a = a + 3
      return uspech

#řešíme sudoku, dokud se nestane, že velikost všech množin je větší než 1
def vypocet(sudoku):
      pojistka = True
      while pojistka:
            minimum = ({1,2,3,4,5,6,7,8,9,10},10,10)
            pojistka = False
            for i in range(9):
                  for j in range(9):
                        if type(sudoku[i][j]) != int and len(sudoku[i][j]) == 1:
                              sudoku[i][j] = sudoku[i][j].pop()
                              pojistka = True
                              radek(i,sudoku[i][j],sudoku)
                              sloupec(j,sudoku[i][j],sudoku)
                              ctverec(i,j,sudoku[i][j],sudoku)
                        
                        elif type(sudoku[i][j]) != int and len(sudoku[i][j]) < len(minimum[0]):
                              minimum = (sudoku[i][j],i,j)
                              if len(minimum[0]) == 0:
                                    return minimum

            if not pojistka:
                  a = slozity_radek(sudoku)
                  if a == True:
                        pojistka = True
                  
                  a = slozity_sloupec(sudoku)
                  if a == True:
                        pojistka = True
                  
                  a = slozity_ctverec(sudoku)
                  if a == True:
                        pojistka = True
      return minimum

#jednoduchá funkce na zapsání hodnot z jednoho seznamu do druhého
def zapis(a,b):
    for  x in range(9):
            for y in range(9):
                a[x][y] = b[x][y]


#pokud se stane, že po provedení funkce výpočet mají všechny množiny velikost větší než
#2, přichází na řadu rekurze, která již potom doplní celé sudoku, pokud tedy existuje řešení
def rekurze(sudoku, stav):
      zaloha = [[0]*9 for _ in range(9)]
      zapis(zaloha,sudoku)
      for x in list(stav[0])[::-1]:
            zapis(sudoku,zaloha)
            sudoku[stav[1]][stav[2]] = x
            radek(stav[1],sudoku[stav[1]][stav[2]],sudoku)
            sloupec(stav[2],sudoku[stav[1]][stav[2]],sudoku)
            ctverec(stav[1],stav[2],sudoku[stav[1]][stav[2]],sudoku)
            novy_stav = vypocet(sudoku)
            if novy_stav[1] == 10:
                  return True

            if len(novy_stav[0]) != 0:
                  a = rekurze(sudoku, novy_stav)
                  if a:
                        return True
                  zapis(sudoku,zaloha)
      return False

#Hlavní funkce pouze spojuje všechny funkce dohromady
def hlavni_funkce(sudoku):
      inicializace(sudoku)
      stav = vypocet(sudoku)
      if stav[1] == 10:
            return ("Vyřešeno", sudoku)
      
      elif len(stav[0]) == 0:
                  for x in range(9):
                        for y in range(9):
                              if type(sudoku[x][y]) != int:
                                    sudoku[x][y] = ""
                  return ("Úloha Nemá řešení, problém na pozici {} {}".format(stav[1]+1, stav[2]+1), sudoku)
      
      else: 
            
            while len(stav[0]) > 2:
                  #to je proto, aby v případě hodně prázdného zadání zbytečně nevolali hned
                  # rekurzi a taky získáme díky metodě random vždy jiné řešení
                  a = list(stav[0])
                  sudoku[stav[1]][stav[2]] = random.choice(a)
                  radek(stav[1],sudoku[stav[1]][stav[2]],sudoku)
                  sloupec(stav[2],sudoku[stav[1]][stav[2]],sudoku)
                  ctverec(stav[1],stav[2],sudoku[stav[1]][stav[2]],sudoku)
                  stav = vypocet(sudoku)

            vysledek = rekurze(sudoku, stav)

            if not vysledek:
                  for x in range(9):
                        for y in range(9):
                              if type(sudoku[x][y]) != int:
                                    sudoku[x][y] = ""
                  return ("Úloha nemá řešení", sudoku)

            return ("Vyřešeno", sudoku)

#funkce generující zadání, taky používáme metodu random pro neopakující se zadání
def generovat():
      sudoku = [[0]*9 for _ in range(9)]
      zaloha = [[0]*9 for _ in range(9)]
      reseni = open("reseni.txt", "w")
      _,sudoku = hlavni_funkce(sudoku)

      for x in range(9):
            for y in range(9):
                  print(sudoku[x][y], file=reseni)
      zapis(zaloha,sudoku)
      seznam = [(0,0),(0,1),(0,2),(0,3),(0,4),(0,5),(0,6),(0,7),(0,8),(1,0),(1,1),(1,2),(1,3),(1,4),(1,5),(1,6),(1,7),(1,8),(2,0),(2,1),(2,2),(2,3),(2,4),(2,5),(2,6),(2,7),(2,8),(3,0),(3,1),(3,2),(3,3),(3,4),(3,5),(3,6),(3,7),(3,8),(4,0),(4,1),(4,2),(4,3),(4,4),(4,5),(4,6),(4,7),(4,8),(5,0),(5,1),(5,2),(5,3),(5,4),(5,5),(5,6),(5,7),(5,8),(6,0),(6,1),(6,2),(6,3),(6,4),(6,5),(6,6),(6,7),(6,8),(7,0),(7,1),(7,2),(7,3),(7,4),(7,5),(7,6),(7,7),(7,8),(8,0),(8,1),(8,2),(8,3),(8,4),(8,5),(8,6),(8,7),(8,8)]

      while len(seznam) > 0:
            x = random.choice(seznam)
            y = seznam.index(x)
            seznam.pop(y)
            a = x[0]
            b = x[1]
            if zaloha[a][b] != 0:
                  pojistka = sudoku[a][b]
                  zaloha[a][b] = 0
                  zapis(sudoku,zaloha)
                  inicializace(sudoku)
                  stav = vypocet(sudoku)
                  if stav[1] != 10:
                        zaloha[a][b] = pojistka
      
      return zaloha

if __name__ == '__main__':
    app.run(debug=True)