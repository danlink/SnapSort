import re

#===============================================================================
# Wertet das Jahr in einem documentDate im Format YYYY-MM-DD aus,
# findet die erste Jahreszahl im inputString und ersetzt diese durch die
# ggf. um delta Jahre korrigierte Jahreszahl aus dem documentDate
#===============================================================================
def changeYear(inputString, documentDate="", delta=0):
    matchOutput = re.search(r"\b\d{4}\b", inputString)
    if matchOutput and matchOutput.group():
        if documentDate != "":
            extract = re.search(r"(?P<year>\d{4})(-(?P<month>\d{2}))?(-(?P<day>\d{2}))?", documentDate) 
            if extract and extract.group("year") and (1900 <= int(extract.group("year")) <= 2100):
                year = int(extract.group("year"))
                newYear = year + delta
            else:
                return inputString
        else:
            year = int(matchOutput.group())
            newYear = year + delta
        outputString = inputString.replace(matchOutput.group(), str(newYear)) # Erstetzt das erste Vorkommen im Eingabestring durch neuen Monatsnamen
        return outputString
    else:
        return inputString


#===============================================================================
# Wertet den Monat in einem documentDate im Format YYYY-MM-DD aus,
# findet einen Monatsname im inputString und ersetzt diesen durch den
# ggf. um delta Monate korrigierten Monat aus dem documentDate
#===============================================================================
def changeMonth(inputString, documentDate="", delta=0):
    listOfMonths = ("Januar", "Februar", "März", "April", "Mai", "Juni", "Juli", "August", "September", "Oktober", "November", "Dezember")
   
    matchOutput = re.search(r"(Januar|Februar|März|April|Mai|Juni|Juli|August|September|Oktober|November|Dezember)", inputString)
    if matchOutput and (matchOutput.group() in listOfMonths):
        if documentDate != "":
            extract = re.search(r"(?P<year>\d{4})(-(?P<month>\d{2}))?(-(?P<day>\d{2}))?", documentDate)
            if extract and extract.group("month") and (1 <= int(extract.group("month")) <= 12):
                monthIndex = int(extract.group("month"))-1
                newMonthIndex = (monthIndex + delta) % 12
            else:
                return inputString
        else:
            monthIndex = listOfMonths.index(matchOutput.group())
            newMonthIndex = (monthIndex + delta) % 12
        outputString = inputString.replace(matchOutput.group(), listOfMonths[newMonthIndex]) # Erstetzt das erste Vorkommen im Eingabestring durch neuen Monatsnamen
        return outputString
    else:
        return inputString

#===============================================================================
# Wertet das Quartal in einem documentDate im Format YYYY-MM-DD aus,
# findet eine Quartalsbezeichnung im inputString und ersetzt diese durch die
# ggf. um delta Quartale korrigierte Angabe aus dem documentDate
#===============================================================================
def changeQuarter(inputString, documentDate="", delta=0):
    listOfQuarters = ("Q1", "Q2", "Q3", "Q4")  
       
    matchOutput = re.search(r"(Q1|Q2|Q3|Q4)", inputString)
    if matchOutput and (matchOutput.group() in listOfQuarters):
        if documentDate != "":
            extract = re.search(r"(?P<year>\d{4})(-(?P<month>\d{2}))?(-(?P<day>\d{2}))?", documentDate)
            if extract and extract.group("month") and (1 <= int(extract.group("month")) <= 12):
                quarterIndex = (int(extract.group("month")) - 1) // 3
                newQuarterIndex = (quarterIndex + delta) % 4
            else:
                return inputString
        else:
            quarterIndex = listOfQuarters.index(matchOutput.group())
            newQuarterIndex = (quarterIndex + delta) % 4
        outputString = inputString.replace(matchOutput.group(), listOfQuarters[newQuarterIndex]) # Erstetzt das erste Vorkommen im Eingabestring durch neuen Monatsnamen
        return outputString
    else:
        return inputString