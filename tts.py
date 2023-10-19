import pyttsx3

engine = pyttsx3.init()
engine.setProperty('rate',150)
engine.setProperty('volume',1)
engine.setProperty('voice','espeak')

engine.say("วันนี้ทื้องฟ้า อากาศแจ่มใส")

engine.runAndWait()
