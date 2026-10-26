from datetime import date, timedelta
from pathlib import Path
from uuid import uuid5, NAMESPACE_URL
from datetime import datetime, timezone

OUT = Path("docs/festivos.ics")
OUT.parent.mkdir(parents=True, exist_ok=True)
events = []
def event(title, day, recurrence=False, description="", uid_title=None):
    uid = str(uuid5(NAMESPACE_URL, "almeria-festivos:"+(uid_title or title)+":"+str(day)))
    end = day + timedelta(days=1)
    lines = ["BEGIN:VEVENT", "UID:"+uid+"@calendario-festivos-almeria", "DTSTAMP:20261026T000000Z",
             "DTSTART;VALUE=DATE:"+day.strftime("%Y%m%d"),
             "DTEND;VALUE=DATE:"+end.strftime("%Y%m%d"),
             "SUMMARY:"+title.replace(",",r"\,")]
    if recurrence: lines.append("RRULE:FREQ=YEARLY")
    if description: lines.append("DESCRIPTION:"+description.replace(",",r"\,"))
    lines.append("END:VEVENT")
    events.extend(lines)
fixed = [
 ("Todos los Santos 🎉",11,1,2026),("Día de la Constitución ⚖️",12,6,2026),
 ("Inmaculada Concepción ⛪️",12,8,2026),("Nochebuena 🎅🏼",12,24,2026),
 ("Navidad 🎅🏼",12,25,2026),("Nochevieja 🎊",12,31,2026),
 ("Año Nuevo 🎊",1,1,2027),("Día de Andalucía 🎉",2,28,2027),
 ("Día del Padre 🎉",3,19,2027),("Día del Trabajador 🎉",5,1,2027),
 ("San Juan 🎉",6,23,2027),("Virgen del Carmen 🎉",7,16,2027),
 ("Asunción de la Virgen 🎉",8,15,2027),
 ("Fiesta Nacional 🇪🇸",10,12,2027),("Reyes Magos 🎉",1,6,2027)]
for name,m,d,y in fixed: event(name,date(y,m,d),True,"Celebración anual; no implica festivo laboral.")
# Local holidays: only officially confirmed years. Add new years after verification.
local = [
 ("San Marcos 🐂",date(2027,4,26)),
 ("San Isidro Labrador 🎉",date(2027,6,28)),
 ("Santa Ana y Virgen del Carmen ⛪️",date(2027,7,26)),
 ("Virgen del Rosario 🌹",date(2027,10,7))]
for name,day in local:
    legacy_title = {"San Marcos 🐂":"El Ejido — San Marcos 🐂",
                    "San Isidro Labrador 🎉":"El Ejido — San Isidro Labrador 🎉",
                    "Santa Ana y Virgen del Carmen ⛪️":"Roquetas — Santa Ana y Virgen del Carmen ⛪️",
                    "Virgen del Rosario 🌹":"Roquetas — Virgen del Rosario 🌹"}[name]
    event(name,day,False,"Festivo local aprobado para este año.",uid_title=legacy_title)
def easter(y):
    a=y%19;b=y//100;c=y%100;d=b//4;e=b%4;f=(b+8)//25;g=(b-f+1)//3
    h=(19*a+b-d-g+15)%30;i=c//4;k=c%4;l=(32+2*e+2*i-h-k)%7
    m=(a+11*h+22*l)//451;month=(h+l-7*m+114)//31
    day=(h+l-7*m+114)%31+1
    return date(y,month,day)
for y in range(2027,2127):
    e=easter(y)
    for name,offset in [
        ("Miércoles de Ceniza", -46),("Domingo de Ramos",-7),
        ("Lunes Santo",-6),("Martes Santo",-5),("Miércoles Santo",-4),
        ("Jueves Santo",-3),("Viernes Santo",-2),("Sábado Santo",-1),
        ("Domingo de Resurrección",0)]:
        event(name,e+timedelta(days=offset),False,"Fecha religiosa; el carácter laboral depende del calendario oficial.")
content="BEGIN:VCALENDAR\r\nVERSION:2.0\r\nPRODID:-//Calendario Almeria//ES\r\nCALSCALE:GREGORIAN\r\nMETHOD:PUBLISH\r\nX-WR-CALNAME:Festivos Roquetas y El Ejido\r\n"+ "\r\n".join(events)+"\r\nEND:VCALENDAR\r\n"
OUT.write_bytes(content.encode("utf-8"))
print(f"Generados {len(events)} renglones en {OUT}")
