#PASSWORD-MANAGER. MOSTRA LE PASSWORD IN MANIERA GRAFICA GRAZIE ALL'UTILIZZO DELLA LIBRERIA TKINTER
#UTILE PER CHI VUOLE TENERE LE PROPRIE PASSWORD IN UN POSTO SICURO, FACENDOLE RICORDARE COMODAMENTE AL PROPRIO PC
#RESO FACILE E INTUITIVO, CON LOGHI CREATI DA ME

from tkinter import *  # LIBRERIA PER GRAPHICAL USER INTERFACE (GUI)
from tkinter import messagebox
import pyperclip as pyclip  # LIBRERIA PER COPIARE UN TESTO
import beepy  # LIBRERIA PER EFFETTI SONORI
import os  # LIBRERIA PER CONTROLLARE IL TERMINALE
import os.path
from bs4 import BeautifulSoup
import requests
from cryptography.fernet import Fernet
import smtplib
from random import randint
from validate_email import validate_email
import json
from functools import partial
from selenium import webdriver

versione_attuale = "PasswordManager1.0.4.3"

Percorso = os.getcwd()

if os.path.exists(f"{Percorso}\\chiave_password.key") == False:
    chiave_password = Fernet.generate_key()
    file_chiave = open('chiave_password.key', 'wb')
    file_chiave.write(chiave_password)
    file_chiave.close()

    file_chiave = open("chiave_password.key", "rb")
    chiave = file_chiave.read()
    fernet = Fernet(chiave)     #FERNET ASSICURA CHE IL FILE CRIPTATO NON POSSA VENIR LETTO SENZA LA CHIAVE, CRIPTA IN AES (Advanced Encryption Standard)

else:
    file_chiave = open("chiave_password.key", "rb")
    chiave = file_chiave.read()
    fernet = Fernet(chiave)


if os.path.exists(f"{Percorso}\\xscx.txt") == True:
    apertura = open("xscx.txt", "rb")
    data = apertura.read()
    data = fernet.decrypt(data)
    apertura.close()

    apertura_2 = open("pw_manager_pw.json", "wb")
    apertura_2.write(data)
    apertura_2.close()



def password_manager():
    # IMPOSTAZIONE GRAFICA DEL PROGRAMMA (APERTURA, TITOLO, ICONA, DIMENSIONI E COLORE SFONDO)
    finestra = Tk()
    finestra.title("PASSWORD MANAGER by Giulio")  # TITOLO DEL PROGRAMMA
    finestra.iconbitmap(f"{Percorso}\\Immagini\\Lucchetto.ico")  # ICONA DEL PROGRAMMA
    finestra.geometry("905x500+500+250")  # DIMENSIONI DEL PROGRAMMA
    finestra.configure(bg="white")  # BG, COLORE BACKGROUND (SFONDO) DEL PROGRAMMA
    finestra.resizable(False, False)  # NON PERMETTE DI INGRANDIRE/RIMPICCIOLIRE IL PROGRAMMA (FALSO PER PER COORDINATE X E Y)

    def aggiungi():
        schermata_aggiunta = Tk()
        schermata_aggiunta.configure(bg="white")
        schermata_aggiunta.geometry("350x245+800+400")
        schermata_aggiunta.title("Aggiungi nuove credenziali")

        social = Entry(schermata_aggiunta, fg="black")
        social.place(x=180, y=30)

        inserisci_social_testo = Label(schermata_aggiunta, text="Inserisci il social:", bg="white", fg="black")
        inserisci_social_testo.place(x=10, y=30)

        inserisci_email_testo = Label(schermata_aggiunta, text="Inserisci l'e-mail:", bg="white", fg="black")
        inserisci_email_testo.place(x=10, y=80)

        emailxx = Entry(schermata_aggiunta, fg="black")
        emailxx.place(x=180, y=80)

        inserisci_password_testo = Label(schermata_aggiunta, text="Inserisci la password:", bg="white", fg="black")
        inserisci_password_testo.place(x=10, y=130)

        passwordxx = Entry(schermata_aggiunta, fg="black", show="*")
        passwordxx.place(x=180, y=130)

        def salvataggio():
            social_preso = social.get()
            email_presa = emailxx.get()
            passw_presa = passwordxx.get()

            if social_preso == "" or email_presa == "" or passw_presa == "":
                messagebox.showwarning(message="Devi compilare tutti i campi, riprova.")
                aggiungi()
                return

            social.delete(0, END)
            emailxx.delete(0, END)
            passwordxx.delete(0, END)

            dizionario = {}

            dizionario[f"{social_preso}"] = {

                "Social": f"{social_preso}",
                "E-mail": f"{email_presa}",
                "Password": f"{passw_presa}"
            }

            with open("pw_manager_pw.json", "a") as file_json:
                json.dump(dizionario, file_json, indent=4)

            bottonetutto_ok = Label(schermata_aggiunta, text="Fatto!", bg="yellow", fg="black")
            bottonetutto_ok.place(x=155, y=215)

        bottonesalva = Button(schermata_aggiunta, text="Salva le credenziali", command=salvataggio)
        bottonesalva.place(x=120, y=180)

    add = Button(finestra, text="Aggiungi delle credenziali", command=aggiungi)
    add.place(x=100, y=220)

    def visualizza():
        # SCHERMATA VISUALIZZA

        file_aperto = os.path.exists("pw_manager_pw.json")

        if file_aperto == True:
            while os.path.getsize(f"{Percorso}\\pw_manager_pw.json") < 5:
                file_aperto == False
                os.remove("pw_manager_pw.json")
                os.remove("xscx.txt")
                messagebox.showwarning(title="Errore", message="Il file non esiste, devi prima aggiungere delle credenziali")
                continue

        file_aperto = os.path.exists("pw_manager_pw.json")

        def modifica():

            def ricerca_e_modifica():

                apertura_file = open("pw_manager_pw.json", "r")
                lettura_file = apertura_file.read()
                lettura_file = lettura_file.replace("}{", ",")
                lettura_json = json.loads(lettura_file)

                da_modificare_preso = social_da_modificare.get()
                da_modificare_preso = da_modificare_preso.lower()
                social_da_modificare.delete(0, END)

                lista_controllo = []
                for eleme in lettura_json:
                    lista_controllo.append(eleme.lower())

                if da_modificare_preso == "":
                    messagebox.showwarning(message="Devi scrivere il Social")
                    return

                if da_modificare_preso not in lista_controllo:
                    messagebox.showerror(message="Devi inserire un nome valido!")
                    return

                social_da_modificare_label.destroy()
                social_da_modificare.destroy()
                comando_invio.destroy()
                esempio_scritto.destroy()
                da_modificare_preso = da_modificare_preso.capitalize()

                cosa_sto_cambiando = Label(finestra_modifica, text=f"{da_modificare_preso}", font=10, bg="white")
                cosa_sto_cambiando.pack()

                try:
                    def cambia_email():
                        cambia_label.configure(text="Inserisci la tua nuova E-mail:")
                        cambia_label.place(x=100, y=90)

                        cambia_email = Entry(finestra_modifica, width=30, justify="center")
                        cambia_email.place(x=80, y=125)

                        def prendi_testo_email():
                            email_presa = cambia_email.get()
                            email_vecchia = lettura_json[f"{da_modificare_preso}"]["E-mail"]

                            lettura_json[f"{da_modificare_preso}"]["E-mail"] = f"{email_presa}"

                            riapertura_file = open("pw_manager_pw.json", "w")
                            json.dump(lettura_json, riapertura_file, indent=4)

                            etichetta_fatto = messagebox.showinfo(title="Cambio Email", message="Fatto!\n\n" + f"{email_vecchia}" + " → " + f"{email_presa}")
                            finestra_modifica.destroy()
                            finestra_visualizza.destroy()

                        bottone_invio_ = Button(finestra_modifica, text="Invio", command=prendi_testo_email, bg="red")
                        bottone_invio_.place(x=155, y=150)

                    def cambia_pass():

                        cambia_label.configure(text="Inserisci la tua nuova Password:")
                        cambia_label.place(x=90, y=90)

                        cambia_pass = Entry(finestra_modifica, width=30)
                        cambia_pass.place(x=80, y=125)

                        def prendi_testo_pass():
                            pass_presa = cambia_pass.get()
                            pass_vecchia = lettura_json[f"{da_modificare_preso}"]["Password"]

                            lettura_json[f"{da_modificare_preso}"]["Password"] = f"{pass_presa}"

                            riapertura_file = open("pw_manager_pw.json", "w")
                            json.dump(lettura_json, riapertura_file, indent=4)

                            etichetta_fatto = messagebox.showinfo(title="Cambio Password", message="Fatto!\n\n" + f"{pass_vecchia}" + " → " + f"{pass_presa}")
                            finestra_modifica.destroy()
                            finestra_visualizza.destroy()

                        bottone_invio_ = Button(finestra_modifica, text="Invio", command=prendi_testo_pass, bg="red")
                        bottone_invio_.place(x=155, y=150)

                    cambia_label = Label(finestra_modifica)

                    bottone_radio_email = Button(finestra_modifica, text="Cambia E-Mail", command=cambia_email, bg="white")
                    bottone_radio_email.place(x=30, y=40)

                    bottone_radio_pass = Button(finestra_modifica, text="Cambia Password", command=cambia_pass, bg="white")
                    bottone_radio_pass.place(x=210, y=40)



                except KeyError:
                    messagebox.showerror(message="Inserisci un nome valido!")

            finestra_modifica = Tk()
            finestra_modifica.title("Modifica le tue credenziali")
            finestra_modifica.geometry("350x300+700+400")
            finestra_modifica.configure(bg="white")

            social_da_modificare_label = Label(finestra_modifica, text="Inserisci il nome del Social che intendi modificare:", bg="white")
            social_da_modificare_label.pack()

            social_da_modificare = Entry(finestra_modifica)
            social_da_modificare.pack()

            comando_invio = Button(finestra_modifica, text="Invio", command=ricerca_e_modifica)
            comando_invio.pack()

            esempio_scritto = Label(finestra_modifica, text="Esempio: 'Facebook'", bg="white")
            esempio_scritto.pack()

        def cancella():

            def cancellatura():

                def si(social_da_cancellare):

                    riapertura_file = open("pw_manager_pw.json", "r")
                    rilettura_file = riapertura_file.read()
                    rilettura_file = rilettura_file.replace("}{", ",")
                    rilettura_json = json.loads(rilettura_file)

                    del rilettura_json[f"{social_da_cancellare}"]

                    riapertura_file = open("pw_manager_pw.json", "w")
                    json.dump(rilettura_json, riapertura_file, indent=4)

                    messagebox.showinfo(title="Cancella", message=f"{social_da_cancellare}" + " è stato cancellato!")


                    finestra_cancella.destroy()
                    finestra_visualizza.destroy()


                def no():
                    finestra_cancella.destroy()
                    cancella()

                apertura_file = open("pw_manager_pw.json", "r")
                lettura_file = apertura_file.read()
                lettura_file = lettura_file.replace("}{", ",")
                lettura_json = json.loads(lettura_file)

                social_da_cancellare_preso = social_da_cancellare.get()
                social_da_cancellare_preso = social_da_cancellare_preso.lower()
                social_da_cancellare.delete(0, END)

                lista_controllo = []
                for eleme in lettura_json:
                    lista_controllo.append(eleme.lower())

                if social_da_cancellare_preso == "":
                    messagebox.showwarning(message="Devi scrivere il Social")
                    return

                if social_da_cancellare_preso not in lista_controllo:
                    messagebox.showerror(message="Devi inserire un nome valido!")
                    return

                social_da_cancellare_label.destroy()
                social_da_cancellare.destroy()
                comando_invio.destroy()
                esempio_scritto.destroy()
                social_da_cancellare_preso = social_da_cancellare_preso.capitalize()


                vuoi_cancellare = Label(finestra_cancella, text="Vuoi cancellare " + f"{social_da_cancellare_preso}" + "?", bg="white", font=10)
                vuoi_cancellare.pack(pady=20)

                bottone_si = Button(finestra_cancella, text="  Sì  ", command=partial(si, social_da_cancellare_preso))
                bottone_si.place(x=90, y=85)

                bottone_no = Button(finestra_cancella, text=" No ", command=no)
                bottone_no.place(x=220, y=85)

            finestra_cancella = Tk()
            finestra_cancella.title("Cancella le tue credenziali")
            finestra_cancella.geometry("350x300+700+400")
            finestra_cancella.configure(bg="white")

            social_da_cancellare_label = Label(finestra_cancella, text="Inserisci il nome del Social che intendi cancellare:", bg="white")
            social_da_cancellare_label.pack()

            social_da_cancellare = Entry(finestra_cancella)
            social_da_cancellare.pack()

            comando_invio = Button(finestra_cancella, text="Invio", command=cancellatura)
            comando_invio.pack()

            esempio_scritto = Label(finestra_cancella, text="Esempio: 'Facebook'", bg="white")
            esempio_scritto.pack()




        def visualizza_prescelto(nome_social, dizionario_social):

            def copia_email():
                pyclip.copy(credenziali_scelte_["E-mail"])

            def copia_password():
                pyclip.copy(credenziali_scelte_["Password"])

            bottone_copia_email = Button(finestra_visualizza, text="Copia E-mail", command=copia_email)
            bottone_copia_email.place(x=120, y=250)

            bottone_copia_password = Button(finestra_visualizza, text="Copia Password", command=copia_password)
            bottone_copia_password.place(x=230, y=250)


            credenziali_scelte_ = dizionario_social[f"{nome_social}"]
            credenziali_scelte = str(credenziali_scelte_)
            credenziali_scelte = credenziali_scelte.replace(",", "\n")
            credenziali_scelte = credenziali_scelte.replace("{", " ")
            credenziali_scelte = credenziali_scelte.replace("}", "")
            credenziali_scelte = credenziali_scelte.replace("'", "")



            etichetta_mostra_password.configure(bg="yellow", fg="black", text=credenziali_scelte, width=30, height=4)




        if file_aperto == True:

            etichetta_principale.configure(bg="white", fg="white")
            finestra_visualizza = Tk()
            finestra_visualizza.title("Le tue password")
            finestra_visualizza.geometry("400x300+760+380")
            finestra_visualizza.configure(bg="white")


            apertura_file = open("pw_manager_pw.json", "r")
            lettura_file = apertura_file.read()
            lettura_file = lettura_file.replace("}{", ",")
            transformazione_json = json.loads(lettura_file)

            y_coord = 5
            for elemento in transformazione_json:
                y_coord = y_coord + 40
                bottone_visualizza = Button(finestra_visualizza, text=f"{elemento}", command=partial(visualizza_prescelto, elemento, transformazione_json))
                bottone_visualizza.place(x=20, y=y_coord)
                spazio_vuoto = Label(finestra_visualizza).pack()


            etichetta_mostra_password = Label(finestra_visualizza, bg="white", fg="white", width=20, height=3)
            etichetta_mostra_password.place(x=110, y=170)

            copertura_di_un_grigio_strano = Label(finestra_visualizza, bg="white", width=1, height=4)
            copertura_di_un_grigio_strano.place(x=190, y=0)

            bottone_modifica = Button(finestra_visualizza, text="Modifica", command=modifica)
            bottone_modifica.place(x=310, y=45)


            bottone_cancella = Button(finestra_visualizza, text="Cancella", command=cancella)
            bottone_cancella.place(x=310, y=85)



        if file_aperto == False:
            messagebox.showwarning(title="Errore", message="Il file non esiste, devi prima aggiungere delle credenziali")

    view = Button(finestra, text="Visualizza e modifica le credenziali", command=visualizza)
    view.place(x=100, y=270)


    def meteo():
        # BEAUTIFULSOUP PER LE CONDIZIONI METEO GENERALI
        source_condizioni = requests.get("https://weather.com/it-IT/tempo/oggi/l/8c7985d741c74efeb91bcabe9285b59a60ded1a6125fe57f9902c73fcb85b789").text  # CON LA LIBRERIA REQUESTS "SCARICA" I DATI DEL LINK DAT, TRASFORMANDOLI IN FORMATO TESTO CON IL COMANDO .text
        soup_condizioni = BeautifulSoup(source_condizioni, "html.parser")  # LA LIBRERIA BEAUTIFULSOUP SERVE PER "PARSARE" (ANALIZZARE) DATI DA SITIWEB, IN QUESTO CASO DELLE STRINGHE DI TESTO. "lxml" è L'ANALIZZATORE UTILIZZATO, CHE APPUNTO RIESCE A LEGGERE IL FILE .html
        condizioni = soup_condizioni.find(class_="CurrentConditions--phraseValue--2xXSr")
        condizioni = condizioni.text
        condizioni_stringa = str(condizioni)

        # BEAUTIFULSOUP PER LA TEMPERATURA MINIMA E MASSIMA
        source = requests.get("https://www.meteo.it/meteo/sulmona-66098").text
        soup_temperature = BeautifulSoup(source, "html.parser")

        temperatura1 = soup_temperature.find("span", class_="temperature")
        temperatura_min = str(temperatura1.text)

        temperatura2 = temperatura1.nextSibling.text
        temperatura_max = str(temperatura2)

        variabile_temperatura = StringVar()
        variabile_temperatura.set("Condizioni previste oggi: " + condizioni_stringa + "\n\nLa minima temperatura è di: " + temperatura_min + "\nmentre la massima è di: " + temperatura_max)

        # BEAUTIFULSOUP PER VEDERE CHE GIORNO è OGGI
        source_giorno = requests.get("https://www.datadioggi.it/").text
        soup_giorno = BeautifulSoup(source_giorno, "html.parser")

        giorno_non_stringa = soup_giorno.find(class_="date-to-be-copied red")
        giorno = "Meteo di: " + giorno_non_stringa.text.lower()

        messagebox.showinfo(title=giorno, message="Condizioni previste oggi: " + condizioni_stringa + "\n\nLa minima temperatura è di: " + temperatura_min + "\nmentre la massima è di: " + temperatura_max)

    bottone_meteo = Button(finestra, text="Meteo di oggi", command=meteo)
    bottone_meteo.place(x=100, y=320)

    def mostra_istruzioni():
        #os.startfile("istruzioni.txt")
        bxx_ = webdriver.Chrome("C:\\Windows\\chromedriver.exe")
        bxx_.get("https://www.reddit.com")


    istruzioni = Button(finestra, text="Vedi le istruzioni", command = mostra_istruzioni)
    istruzioni.place(x=100,y=370)

    def auto_updater():

        url_sito = requests.get("http://www.maverickfgm.com").text
        conversione_url_sito = BeautifulSoup(url_sito, "html.parser")

        link_pwgenerale = conversione_url_sito.find(class_="link_pwgenerale").text.strip()
        link_pwgenerale_download = conversione_url_sito.find(class_="link_pwgenerale_download").text.strip()

        source_download = requests.get(link_pwgenerale)
        source_download = source_download.text
        soup_download = BeautifulSoup(source_download, "html.parser")

        nome_versione_programma = soup_download.find(class_="dl-btn-label").text
        nome_versione_programma = str(nome_versione_programma.strip())

        if nome_versione_programma == versione_attuale:
            # popup_aggiornamento = alert(title="AutoUpdater", text="Il programma è aggiornato\n\n          Version 1.0.0.6")
            messagebox.showinfo(message="Il programma è aggiornato\n\n          Version 1.0.4.3")



        else:
            percorso_attuale = os.getcwd()
            percorso_download = os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop')
            os.chdir(percorso_download)

            r = requests.get(link_pwgenerale_download)

            open(f"{nome_versione_programma}", "wb").write(r.content)  # WB STA PER WRITE IN BINARY, CIOè IL FILE VIENE LETTO COME FILE DI TESTO BINARIO, IN MODO CHE NON VIENE CAMBIATO NESSUN DATO AL SUO INTERNO
            os.rename(f"{percorso_download}\\{nome_versione_programma}", f"{nome_versione_programma}.rar")

            messagebox.showinfo(message="La nuova versione è stata scaricata in: " + percorso_download)
            # popup_download = alert(title="AutoUpdater", text="La nuova versione è stata scaricata in: " + percorso_download)

            os.chdir(percorso_attuale)

    def password_dimenticata():

        finestra_pass_dimenticata = Tk()
        finestra_pass_dimenticata.geometry("400x120+700+350")
        finestra_pass_dimenticata.resizable(False, False)
        finestra_pass_dimenticata.title("Reimpostazione Password")

        file_contente_email = open("file_email.txt", "r")
        email = file_contente_email.read()

        numero_casuale = randint(100000, 999999)
        numero_casuale = str(numero_casuale)
        corpo_testo = numero_casuale + "\n" + "Inserisci questo codice nel programma"

        connessione_server = smtplib.SMTP("smtp.gmail.com", 587)  # CONNESSIONE AL SERVER STMP (CON SERVIZIO INCLUSO (IN QUESTO CASO GMAIL)) E SPECIFICARE LA PORTA DI SERVIZIO (IN QUESTO CASO LA PORTA DI GMAIL è 587

        connessione_server.ehlo()  # AVVIA LA CONNESSIONE AL SERVER
        connessione_server.starttls()  # AVVIA UN CANALE CRIPTATO IN MODO CHE CONNESSIONE, LOGIN, E CONTENUTO VENGANO CRITTOGRAFATI
        connessione_server.login("passmanager.lost@gmail.com", "passwordmanagerpassword00")  # EFFETTUO IL LOGIN CON LE MIE CREDENZIALI (RISPETTIVMANETE EMAIL, PASSWORD)
        connessione_server.sendmail("passmanager.lost@gmail.com", email, corpo_testo)  # DICHIARARE MITTENTE, DESTINATARIO, CONTENUTO DEL MESSAGGIO)

        connessione_server.quit()  # CHIUDO LA CONNESSIONE CON IL SERVER

        def recupero_password():
            codice_testo = entrata_codice_testo.get()
            entrata_codice_testo.delete(0, END)

            if codice_testo == numero_casuale:
                if os.path.exists("key.key"):
                    os.remove("key.key")
                if os.path.exists("password_intro.txt"):
                    os.remove("password_intro.txt")
                if os.path.exists("file_email.txt"):
                    os.remove("file_email.txt")


                messagebox.showinfo(title="PasswordManager", message="Perfetto! Riavvia il programma")
                finestra.destroy()
                finestra_pass_dimenticata.destroy()
                finestra_password_iniziale.destroy()




            else:
                etichettaerrore_codice = Label(finestra_pass_dimenticata, text="Codice Errato", bg="red", fg="black")
                etichettaerrore_codice.place(x=300, y=58)

        conferma_invio = Label(finestra_pass_dimenticata, text="Un codice è stato inviato a:\n" + email, fg="black")
        conferma_invio.pack()
        inserisci_codice_testo = Label(finestra_pass_dimenticata, text="Inserisci qui il tuo codice: ", fg="black")
        inserisci_codice_testo.place(x=0, y=60)

        entrata_codice_testo = Entry(finestra_pass_dimenticata)
        entrata_codice_testo.place(x=150, y=60)

        bottone_invio_codice = Button(finestra_pass_dimenticata, text="Invio", command=recupero_password)
        bottone_invio_codice.place(x=190, y=85)

        # BLOCCO PER L'ENTRATA INIZIALE (NECESSITA DI UNA PASSWORD E NON MOSTRA QUELLE RICHIESTE)

    # FUNZIONE CHE LEGGE SE LA PASSWORD è GIUSTA, E, SE SBAGLIATA, MOSTRA MESSAGGIO DI ERRORE
    def valore():

        file = open("key.key", "rb")
        key = file.read()
        file.close()

        file = open("password_intro.txt", "rb")
        filex = file.read()
        file.close()

        f = Fernet(key)

        decriptata = f.decrypt(filex)
        decriptata = decriptata.decode()

        passw = stringapassword.get()  # REGISTRA IL VALORE INSERITO NELLA STRINGA

        if passw == decriptata:
            etichettanera_intro.destroy()  # I COMANDI SEGUENTI, RIMUOVONO IL BLOCCO DEL PROGRAMMA CHE NON PERMETTE DI VISUALIZZARE LE PASSWORD (OVVIAMENTE VENGONO TOLTI SOLO SE LA PASSWORD è GIUSTA)
            stringapassword.destroy()
            bottonepassword.destroy()
            etichettaerrore.destroy()
            etichettanera_intro_alta_sx.destroy()
            etichettanera_intro_alta_dx.destroy()
            etichettanera_intro_alta_sopralogo.destroy()
            copertura_etichetta_versione.destroy()
            hai_dimenticato_password.destroy()

            # beepy.beep(sound=1)

        else:

            etichettaerrore.configure(bg="red")  # SE LA PASSWORD è SBAGLIATA, MOSTRA UN MESSAGGIO DI ERRORE
            stringapassword.delete(0, END)  # CANCELLA IL TESTO PRECEDENTEMENTE INSERITO IN AUTOMATICO
            hai_dimenticato_password.configure(bg="yellow")
            hai_dimenticato_password.place(x=380, y=400)

            # beepy.beep(sound=2)

    # INTERFACCE GRAFICHE PRINCIPALI DEL PROGRAMMA: LOGO E SOTTOTITOLO

    etichetta_principale = Label(finestra, bg="white", fg="white", width=50, height=4)
    etichetta_principale.place(x=350, y=415)

    logoprincipale = PhotoImage(file=f"{Percorso}\\Immagini\\passwordmanager.png")  # UTILIZZANDO LA FUNZIONE PHOTOIMAGE DI TKINTER, IMPORTO IL LOGO CHE HO CREATO PER IL PROGRAMMA, DEFINENDO IL SUO PERCORSO
    logoprincipalelabel = Label(finestra, image=logoprincipale, bg="white")  # DOPO AVERLO IMPORTATO, LO CONVERTO IN UN "OGGETTO" DI TKINTER
    logoprincipalelabel.place(x=275, y=20)  # DOPO AVERLO CONVERTITO, GLI ASSEGNO DELLE COORDINATE
    etichettaivana = Label(finestra, text="Ciao, di quale password necessiti?", bg="white", font="bold")
    etichettaivana.place(x=330, y=100)

    i_tuoi_comandi = Label(finestra, text="I tuoi comandi:", bg="white", fg="black", font=5)
    i_tuoi_comandi.place(x=55, y=190)

    puntino1 = Label(finestra, text="•", bg="white", fg="black", font=5)
    puntino1.place(x=85, y=220)

    puntino2 = Label(finestra, text="•", bg="white", fg="black", font=5)
    puntino2.place(x=85, y=270)

    puntino3 = Label(finestra, text="•", bg="white", fg="black", font=5)
    puntino3.place(x=85, y=320)

    puntino4 = Label(finestra, text="•", bg="white", fg="black", font=5)
    puntino4.place(x=85, y=370)

    """linea_sx_comandi = Label(finestra, bg="black", height=10)
    linea_sx_comandi.place(x=85, y=230)"""

    logo_lucchetto = PhotoImage(file=f"{Percorso}\\Immagini\\felice.png")
    logo_lucchetto_label = Label(finestra, image=logo_lucchetto, bg="white")
    logo_lucchetto_label.place(x=535, y=270)


    logo_lucchetto_triste = PhotoImage(file=f"{Percorso}\\Immagini\\triste.png")
    logo_lucchetto_triste_label = Label(finestra, image=logo_lucchetto_triste, bg="white")
    logo_lucchetto_triste_label.place(x=650, y=100)

    con_password_manager = Label(finestra, text="Con Password Manager: ",  bg="white", fg="green")
    con_password_manager.place(x=500,y=375)

    senza_password_manager = Label(finestra, text="Senza Password Manager: ", bg="white", fg="red")
    senza_password_manager.place(x=495, y=190)

    logo_ok = PhotoImage(file=f"{Percorso}\\Immagini\\OK.png")
    logo_ok_label = Label(finestra, image=logo_ok, bg="white")
    logo_ok_label.place(x=540, y=395)

    logo_non_ok = PhotoImage(file=f"{Percorso}\\Immagini\\non_ok.png")
    logo_non_ok_label = Label(finestra, image=logo_non_ok, bg="white")
    logo_non_ok_label.place(x=540, y=210)

    clicca_qui = Label(finestra, bg="white", fg="grey", text="Clicca qui per controllare l'ultima versione → ")
    clicca_qui.place(x=610, y=472)

    # SCHERMO NERO INIZIALE CHE "NASCONDE LE PASSWORD"
    etichettanera_intro = Label(finestra, height=300, width=200, bg="black")  # UNO SFONDO NERO CHE COPRE IL REALE FUNZIONAMENTO DEL PROGRAMMA, VIENE RIMOSSO SOLO SE LA PASSWORD è GIUSTA. INOLTRE NON PERMETTE DI CLICCARE NESSUN TASTO (CHE SI CELA SOTTO IL SUO SFONDO)
    etichettanera_intro.place(x=0, y=80)

    etichettanera_intro_alta_sx = Label(finestra, height=5, width=30, bg="black")
    etichettanera_intro_alta_sx.place(x=0, y=0)

    etichettanera_intro_alta_dx = Label(finestra, height=5, width=35, bg="black")
    etichettanera_intro_alta_dx.place(x=680, y=0)

    etichettanera_intro_alta_sopralogo = Label(finestra, height=1, width=100, bg="black")
    etichettanera_intro_alta_sopralogo.place(x=0, y=0)

    stringapassword = Entry(finestra, width=30, bg="white", show="*")  # STRINGA DI TESTO (Entry) CHE PERMETTE DI INSERIRE IL TESTO, COMANDO DI TKINTER
    stringapassword.place(x=370, y=260)

    # BOTTONE DI INVIO CHE LEGGE IL TESTO INSERITO NELLA STRINGA PASSWORD, RISPETTANDO LA FUNZIONE "valore()"
    bottonepassword = Button(finestra, text="Invio", bg="yellow", command=valore, activebackground="red")
    bottonepassword.place(x=445, y=300)

    # CREAZIONE DEL MESSAGGIO DI ERRORE SE LA PASSWORD INSERITE è SBAGLIATA, AL MOMENTO ANCORA INVISIBILE.
    etichettaerrore = Label(finestra, text="Password Errata", bg="black")
    etichettaerrore.place(x=417, y=220)

    hai_dimenticato_password = Button(finestra, text="Hai dimenticato la password?", command=password_dimenticata, bg="black")
    hai_dimenticato_password.place(x=33380, y=41300)

    # CREAZIONE DEL NUMERO VERSIONE PROGRAMMA MOSTRATO IN BASSO A DESTRA
    download_logo = PhotoImage(file=f"{Percorso}\\Immagini\\download_logo.png")
    download_logo_button = Button(finestra, image=download_logo, bg="white", command=auto_updater)
    download_logo_button.place(x=860, y=465)

    copertura_etichetta_versione = Label(finestra, bg="black", height=2, width=6)
    copertura_etichetta_versione.place(x=860, y=465)


    # COMANDO DI TKINTER PER MANTENERE IL PROGRAMMA SEMPRE APERTO, SENZA IL PROGRAMMA SI CHIUDEREBBE ALL'ISTANTE
    finestra.mainloop()


def password_intro_presa():
    password = scrittura_password.get()
    email = scrittura_email.get()

    validazione_email = validate_email(f"{email}",verify=True)  # verify= True, VERIFICA SE L'EMAIL è CONTENUTA IN UN SERVER SMTP E L'EMAIL ESISTE REALMENTE

    if password == "":
        messagebox.showwarning(title="PasswordManager", message="Devi inserire una password")
        return

    if email == "":
        messagebox.showwarning(title="PasswordManager", message="Devi inserire un' e-mail")
        return




    elif len(password) <= 5:
        messagebox.showwarning(title="PasswordManager", message="Password troppo corta, riprova. \n(Almeno 5 caratteri)")
        return

    if validazione_email == False:
        messagebox.showwarning(title="PasswordManager", message="Inserisci un'e-mail valida")
        return


    else:

        scrittura_password.delete(0, END)
        scrittura_email.delete(0, END)

        def continuazione():

            file = open("key.key", "rb")
            key = file.read()
            file.close()

            password_encoded = password.encode()

            f = Fernet(key)
            encriptata = f.encrypt(password_encoded)

            file_email = open("file_email.txt", "w")
            file_email.write(email)

            file = open("password_intro.txt", "wb")
            file.write(encriptata)

            decriptata = f.decrypt(encriptata)
            decriptata = decriptata.decode()

            file.close()

        if os.path.exists("key.key") == False:
            key = Fernet.generate_key()

            file = open("key.key", "wb")
            file.write(key)
            file.close()

            continuazione()

            messagebox.showinfo(title="PasswordManager", message="Perfetto! Credenziali registrate!")
            finestra_password_iniziale.destroy()
            password_manager()


        else:
            continuazione()


file_aperto = os.path.exists("password_intro.txt")

if file_aperto == False:

    finestra_password_iniziale = Tk()
    finestra_password_iniziale.title("Password Manager")
    finestra_password_iniziale.geometry("270x110+850+400")

    testo_inserisci = Label(finestra_password_iniziale, text="Inserisci la password che desideri al tuo login: ")
    testo_inserisci.pack()
    scrittura_password = Entry(finestra_password_iniziale)
    scrittura_password.pack()

    testo_inserisci_email = Label(finestra_password_iniziale, text="Inserisci la tua email: ")
    testo_inserisci_email.pack()
    scrittura_email = Entry(finestra_password_iniziale)
    scrittura_email.pack()

    bottone_invio_password = Button(finestra_password_iniziale, text="Invio", command=password_intro_presa)
    bottone_invio_password.pack()

    finestra_password_iniziale.mainloop()

else:
    password_manager()

if os.path.exists("pw_manager_pw.json") == False:
    pass

else:
    apertura_file = open("pw_manager_pw.json", "rb")
    contenuto = apertura_file.read()

    contenuto = fernet.encrypt(contenuto)

    apertura_file_critto = open("xscx.txt", "wb")
    apertura_file_critto.write(contenuto)

    apertura_file.close()
    apertura_file_critto.close()

    os.remove("pw_manager_pw.json")
