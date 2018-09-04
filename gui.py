from PyQt5 import QtWidgets, uic
import mechanicalsoup
from PyQt5.QtWidgets import *


def focus():
    dlg.lineEdit_2.setFocus()


app = QtWidgets.QApplication([])
dlg = uic.loadUi("test.ui")


def ok_button():
    try:
        zip_code = dlg.lineEdit.text()#gets text from textline GUI
        country = dlg.lineEdit_2.text()
    #gets location info based on zip
        br = mechanicalsoup.StatefulBrowser()
        br.open("http://www.geonames.org/postal-codes/")
        br.get_current_page()
        br.select_form('form[action="/postalcode-search.html?"]')
        br["q"] = f"{country.capitalize()} {zip_code}"
        response = br.submit_selected()

        page = br.get_current_page()
        rows = page.findAll("tr")
        text=rows[3].text
        br.close()
        country = ""
        place = ""

        counter = 0
        new_text=""

        text = [char for char in text if char.isalpha()]
        for char in text:
            if char.istitle() and counter == 0:
                place += char
                counter += 1

            elif not char.istitle() and counter == 1:
                place += char

            elif char.istitle() and counter == 1:
                country += char
                counter += 1

            elif not char.istitle() and counter == 2:
                country += char

            elif char.istitle() and counter == 2:
                counter += 1
    #gets weather info
        br2 = mechanicalsoup.StatefulBrowser()
        br2.open("https://www.google.com/")
        br2.get_current_page()
        br2.select_form('form[action="/search"]')
        br2["q"] = f"weather {country} {place}"
        response2 = br2.submit_selected("btnG")

        page2 = br2.get_current_page()
        text_info=""

        info = page2.findAll("div", class_="e")
        google_location = info[0].find("h3").text
        google_location1 = ""
        for char in google_location:
            if char == "š":
                google_location1 += "s"
            elif char == "Š":
                google_location1 += "S"
            elif char == "č":
                google_location1 += "c"
            elif char == "Č":
                google_location1 += "C"
            elif char == "ć":
                google_location1 += "c"
            elif char == "Ć":
                google_location1 += "C"
            elif char == "ž":
                google_location1 += "z"
            elif char == "Ž":
                google_location1 += "Z"
            else:
                google_location1 += char
        google_temp = info[0].find("span", class_="wob_t").text

        weather = info[0].findAll("tr")

        current_weather = weather[0].find("img")["alt"]
        dlg.label_3.setText(f"{google_location1}: {google_temp}\n{current_weather}")#chages text in textlable
        dlg.lineEdit.setText("")
        dlg.lineEdit_2.setText("")

    except IndexError:
        QMessageBox.information(None, "InputError", "Please enter valid informations!")
        dlg.lineEdit.setFocus()


def cancel_button():
    exit()


dlg.lineEdit.setPlaceholderText("ZIP")
dlg.lineEdit_2.setPlaceholderText("Country")
dlg.lineEdit.setFocus()                         #puts cursor in box
dlg.lineEdit.returnPressed.connect(focus)
dlg.lineEdit_2.returnPressed.connect(ok_button)

dlg.pushButton_2.clicked.connect(ok_button)
dlg.pushButton.clicked.connect(cancel_button)

dlg.show()
app.exec()