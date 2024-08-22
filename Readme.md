# Dokumentace k zápočtovému programu z programování I

**Autor:** Tadeáš Tomiška

Cílem mého zápočtového programu bylo vytvořit v jazyce Python aplikaci na řešení sudoku. Aplikace nejprve načte
uživatelem zadané hodnoty, zkontroluje správnost vstupu, tj. jestli uživatel zadal pouze číslice v rozsahu 1-9 
a jestli se na nějakém řádku, sloupci či čtverci 3x3 nevyskytují dvě stejné číslice. Je-li vstup korektní, 
aplikace začne řešit sudoku. 

K řešení aplikace využívá množiny. Pro každé políčko eviduje všechny možné číslice, které se v něm mohou
vyskytnout, a pokud má nějaká množina velikost jedna, aplikace obsah množiny zapíše do políčka. Pokud se na 
nějakém políčku vyskytne prázdná množina, úloha nemá řešení. V případě, že mají všechny množiny velikost větší
než jedna, přichází na řadu řešení pomocí rekurze. Na výstupu uživatel obdrží vyřešené sudoku nebo souřadnice
políčka, na kterém došlo k chybě.

Práce na projektu mě opravdu bavila, ale bylo mi líto, že mým programem bude pouze kód v Pythonu. Proto jsem 
se rozhodl umístit svůj program na webové stránky. Program jsem také vylepšil, takže si nyní uživatel může 
zahrát sudoku. Pokud si při hraní neví rady, může si nechat ukázat řešení. Pokud řeší sudoku a není si jistý, 
jestli někde neudělal chybu, může si nechat zkontrolovat řešení. Pole se špatnými hodnotami zčervenají a při
návratu z kontroly zpět k řešení se jejich obsah vymaže. Pole s vygenerovaným zadáním mají také atribut 
`readonly`, aby je uživatel nemohl při řešení přepisovat.

Přikládám program v Pythonu, tři webové stránky a obrázek na pozadí. Program je nutné spustit na lokálním 
serveru, ale úplně stejný kód je i na výše uvedené webové stránce.
