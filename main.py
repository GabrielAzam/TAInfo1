from kivy.config import Config
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock
from random import randrange
from kivy.graphics import Color
from kivy.core.window import Window
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout

Config.set('graphics', 'width', 750)
Config.set('graphics', 'height', 550)
Config.set('graphics', 'resizable', 0)


class Bloc(Widget):

    score = NumericProperty(0)


class SerpentComplet(Widget):
    def erase(self):
        self.clear_widgets()
        self.canvas.clear()


class Tete(Widget):

    score = NumericProperty(0)
    score1 = 0

    def move(self, serpent, move_x, move_y):
        c = len(serpent)
        c = c - 1
        while c != 0:
            serpent[c][0]=serpent[c-1][0]
            serpent[c][1]=serpent[c-1][1]
            c += -1
        serpent[0][0] += move_x
        serpent[0][1] += move_y
        self.pos = serpent[0]

        return serpent

    def restart(self):
        self.pos = [350, 250]

    def contact(self, serpent, fruit):
        c = len(serpent)
        c = c-1
        collide = False

        if self.pos == fruit.pos:
            collide = True
            x = serpent[c][0]-serpent[c-1][0]
            y = serpent[c][1] - serpent[c-1][1]

            if x > 0 and y == 0:
                coord_x = serpent[c][0]+50
                coord_y = serpent[c][1]
                serpent.append([coord_x, coord_y])

            if x < 0 and y == 0:
                coord_x = serpent[c][0]-50
                coord_y = serpent[c][1]
                serpent.append([coord_x, coord_y])

            if x == 0 and y > 0:
                coord_x = serpent[c][0]
                coord_y = serpent[c][1]+50
                serpent.append([coord_x, coord_y])

            if x == 0 and y < 0:
                coord_x = serpent[c][0]
                coord_y = serpent[c][1]-50
                serpent.append([coord_x, coord_y])
        return collide, serpent


class Fruit(Widget):


    def nouveau_fruit(self, serpent):
        x = randrange(2, 15)
        y = randrange(2, 11)
        x = x * 50
        y = y * 50
        coord = [x, y]
        while coord in serpent :
            x = randrange(2, 15)
            y = randrange(2, 11)
            x = x * 50
            y = y * 50
            coord = [x, y]
        self.pos = Vector(*coord)


class SnakeGame(Widget):
    fruit = ObjectProperty(None)
    serp = []
    tete = ObjectProperty(None)
    serp_complete = SerpentComplet()
    direction = "up"

    def __init__(self, **kwargs):
        super(SnakeGame, self).__init__(**kwargs)
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)
        self.defaite=False
        self.compteur=0

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if keycode[1] == 'left':
            self.turn_left()
        elif keycode[1] == 'right':
            self.turn_right()
        elif keycode[1] == 'up':
            self.turn_up()
        elif keycode[1] == 'down':
            self.turn_down()
        return True

    def turn_left(self):
        self.direction="left"

    def turn_right(self):
        self.direction="right"

    def turn_up(self):
        self.direction="up"

    def turn_down(self):
        self.direction="down"

    def first_fruit(self):
        x = randrange(2, 15)
        y = randrange(2, 11)
        x = x * 50
        y = y * 50
        coord = [x,y]
        self.fruit.pos = Vector(*coord)

    def create_body(self):
        coord_tete = [350,250]
        self.serp.append(coord_tete)
        pos_x = coord_tete[0]
        pos_y = coord_tete[1]
        bod1 = [pos_x, pos_y-50]
        bod2 = [pos_x, pos_y-100]
        self.serp.append(bod1)
        self.serp.append(bod2)
        Color(1, 1, 1)
        self.serp_complete.add_widget(Bloc(pos=(bod1[0], bod1[1]), size=(50, 50)))
        self.serp_complete.add_widget(Bloc(pos=(bod2[0], bod2[1]), size=(50, 50)))

    def restart(self):
        self.serp = []
        coord_tete = [350, 250]
        self.serp.append(coord_tete)
        pos_x = coord_tete[0]
        pos_y = coord_tete[1]
        bod1 = [pos_x, pos_y - 50]
        bod2 = [pos_x, pos_y - 100]
        self.serp.append(bod1)
        self.serp.append(bod2)
        Color(1, 1, 1)
        self.serp_complete.add_widget(Bloc(pos=(bod1[0], bod1[1]), size=(50, 50)))
        self.serp_complete.add_widget(Bloc(pos=(bod2[0], bod2[1]), size=(50, 50)))

    def update(self, dt):
        if not self.defaite:
            if self.direction == "left":
                self.serp = self.tete.move(self.serp, -50, 0)
            elif self.direction == "right":
                self.serp = self.tete.move(self.serp, 50, 0)
            elif self.direction == "up":
                self.serp = self.tete.move(self.serp, 0, 50)
            elif self.direction == "down":
                self.serp = self.tete.move(self.serp, 0, -50)
            self.serp_complete.erase()
            c = 1
            while c != len(self.serp):
                self.serp_complete.add_widget(Bloc(pos=(self.serp[c][0], self.serp[c][1]), size=(50, 50)))
                c += 1
            collide, self.serp=self.tete.contact(self.serp, self.fruit)
            if collide==True:
                self.fruit.nouveau_fruit(self.serp)
                self.tete.score+=1
                Tete.score1+=1
            self.defaite = False
            if self.tete.x < self.x:
                self.defaite = True
            if self.tete.top > self.top:
                self.defaite = True
            if self.tete.y < self.y:
                self.defaite = True
            if self.tete.x > self.width:
                self.defaite = True
            for i in range(1, len(self.serp)):
                if self.serp[i] == self.tete.pos:
                    self.defaite = True
        else:
            self.compteur += 1
            box = BoxLayout(orientation='vertical')
            box.add_widget(Label(text="Vous avez fait un score de "+str(Tete.score1)))
            self.popup = Popup(title='Fin de la partie !', content=box, size_hint=(None, None),
                               size=(300, 300), auto_dismiss=False)

            self.popup.open()
            Clock.schedule_once(self.close, 1)

    def close(self, dt):
        Window.close()


class SnakeApp(App):
    def build(self):

        game = SnakeGame()
        game.first_fruit()
        game.create_body()
        Clock.schedule_interval(game.update, 1.0 / 4.0)
        return game


if __name__ == '__main__':
    SnakeApp().run()
