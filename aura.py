# main.py
# Пример Kivy-приложения Aura Counter с аватаром, звуками и сохранением.
# Требуется: pip install kivy

import json, os
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.core.audio import SoundLoader

SAVE_FILE="aura_data.json"

players={
"Костя":{"color":[1,.3,.3,1],"aura":0},
"Матвей":{"color":[.3,.6,1,1],"aura":0},
"Дима":{"color":[.2,1,.4,1],"aura":0},
"Дима 2.0":{"color":[1,.7,.2,1],"aura":0},
"Владисрал":{"color":[1,.3,.8,1],"aura":0},
}

images={
"Костя":"assets/images/kostya.png",
"Матвей":"assets/images/matvey.png",
"Дима":"assets/images/dima.png",
"Дима 2.0":"assets/images/dima2.png",
"Владисрал":"assets/images/vladisral.png",
}

def load():
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE,"r",encoding="utf-8") as f:
            data=json.load(f)
            for k,v in data.items():
                if k in players: players[k]["aura"]=v

def save():
    with open(SAVE_FILE,"w",encoding="utf-8") as f:
        json.dump({k:v["aura"] for k,v in players.items()},f,ensure_ascii=False,indent=2)

class Aura(App):
    def build(self):
        load()
        self.plus=SoundLoader.load("assets/sounds/plus.wav")
        self.minus=SoundLoader.load("assets/sounds/minus.wav")
        self.sel="Костя"
        root=BoxLayout(orientation="vertical",padding=10,spacing=10)
        self.img=Image(source=images[self.sel],size_hint=(1,.4))
        root.add_widget(self.img)
        self.lbl=Label(font_size=26)
        root.add_widget(self.lbl)
        for n in players:
            b=Button(text=n)
            b.bind(on_release=lambda _,x=n:self.pick(x))
            root.add_widget(b)
        row=BoxLayout()
        for t,v in [("+100",100),("+1000",1000),("+5000",5000),("-100",-100),("-1000",-1000),("-5000",-5000)]:
            b=Button(text=t)
            b.bind(on_release=lambda _,x=v:self.change(x))
            row.add_widget(b)
        root.add_widget(row)
        self.update()
        return root
    def pick(self,n):
        self.sel=n
        self.update()
    def change(self,v):
        players[self.sel]["aura"]+=v
        (self.plus if v>0 else self.minus) and ((self.plus if v>0 else self.minus).play())
        save()
        self.update()
    def update(self):
        self.img.source=images[self.sel]
        self.img.reload()
        self.lbl.text=f"{self.sel}\nАура: {players[self.sel]['aura']}"
        self.lbl.color=players[self.sel]["color"]

Aura().run()
