import math
import arcade
import random as r

screenwidth = 1200
screenheight = 800

floortexture = r"C:\Users\Danie\Desktop\CS2pycharm\ProjectPart2(Game)\m-008.jpg"
playertexture = r"C:\Users\Danie\Desktop\CS2pycharm\ProjectPart2(Game)\playersprite.png"
bullettexture = r"C:\Users\Danie\Desktop\CS2pycharm\ProjectPart2(Game)\bulletsprite.png"
enemytexture = r"C:\Users\Danie\Desktop\CS2pycharm\ProjectPart2(Game)\enemysprite.png"
enemy2texture = r"C:\Users\Danie\Desktop\CS2pycharm\ProjectPart2(Game)\enemy2sprite.png"
startscreentexture = r"C:\Users\Danie\Desktop\CS2pycharm\ProjectPart2(Game)\backgroundimage.png"
gameoverscreentexture = r"C:\Users\Danie\Desktop\CS2pycharm\ProjectPart2(Game)\gameover.png"
title = 'Vanquisher'
full_screen = False
isWindowResizable = False
playerscale = 0.10
enemyscale = 0.13
itemscale = 0.01
enemyspeed = 0.35
bulletspeed = 10


class StartScreenView(arcade.View):
    def on_show_view(self):
        self.background = arcade.load_texture(startscreentexture)

    def on_draw(self):
        self.clear()
        arcade.draw_lrwh_rectangle_textured(0, 0, screenwidth, screenheight, self.background)
        arcade.draw_text('Vanquisher', (screenwidth // 2) - 100, screenheight - 100, color=arcade.color.AQUAMARINE, font_size=30, bold=True)
        arcade.draw_text('Press Space To Begin', screenwidth * .3, screenheight // 2, color=arcade.color.GOLD, font_size=40, bold=True, italic=True)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.SPACE:
            gameview = SurvivorGameView()
            gameview.setup()
            self.window.show_view(gameview)


class GameOverView(arcade.View):
    def on_show_view(self):
        self.background = arcade.load_texture(gameoverscreentexture)

    def on_draw(self):
        self.clear()
        arcade.draw_lrwh_rectangle_textured(0, 0, screenwidth, screenheight, self.background)
        arcade.draw_text('Game Over', (screenwidth // 2) - 400, screenheight // 2 + 50, color=arcade.color.DARK_RED, font_size=100, italic=True)
        arcade.draw_text('Press Space To Restart', (screenwidth // 2) - 100, screenheight * .2, color=arcade.color.BLUEBERRY, font_size=30)
        arcade.draw_text(f'Final Score: {finalscore}', screenwidth * .6, screenheight - 100, color=arcade.color.NEON_FUCHSIA, font_size=20)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.SPACE:
            gameview = StartScreenView()
            self.window.show_view(gameview)


#   This method is used to initialize variables(typically before assigning them)
#   Some variables must be assigned to avoid issues with starting new rounds
class SurvivorGameView(arcade.View):
    def __init__(self):
        super().__init__()
        self.pos1 = None
        self.pos2 = None
        self.pos3 = None
        self.pos4 = None
        self.score = 0
        self.round = 0
        self.enemynum1 = None
        self.enemynum2 = None
        self.ammo = None
        self.hasmousebeenclicked = False
        self.isdead = False
        self.playerSpritevelx = 0
        self.playerSpritevely = 0
        self.background_image = None
        self.playerList = None
        self.enemyList = None
        self.itemList = None
        self.playerSprite = None
        self.enemySprite = None
        self.weapon = None
        self.paused = False

#       This method is where the majority of variables are defined.
    def setup(self):
        self.enemynum1 = 25
        self.enemynum2 = 25
        self.ammo = 15
        self.background_image = arcade.load_texture(floortexture)

#       Sprite-lists
        self.itemList = arcade.SpriteList()
        self.playerList = arcade.SpriteList()
        self.enemyList = arcade.SpriteList()

#       Define variables as sprites
#       Adds these defined variables to their sprite-lists
        self.playerSprite = arcade.Sprite(playertexture, playerscale)
        self.playerSprite.center_x = screenwidth / 2
        self.playerSprite.center_y = screenheight / 2
        self.playerList.append(self.playerSprite)

        self.weapon = arcade.Sprite(bullettexture, itemscale)
        self.itemList.append(self.weapon)

#       These variables are used to set bounds, so that enemies won't spawn on top of the player
        self.pos1 = int(self.playerSprite.center_x - 300.0)
        self.pos2 = int(self.playerSprite.center_x + 300.0)
        self.pos3 = int(self.playerSprite.center_y - 100.0)
        self.pos4 = int(self.playerSprite.center_y + 100.0)

#       This loop reduces ammo based off the round until the ammo reaches its minimum of 5
        for num in range(self.round):
            if self.ammo == 5:
                pass
            else:
                self.ammo -= 5

#       Both of these loops populate the enemy sprite-list, with their respective sprites
#       A lot of the sprites generated will lay within the bounds so the continue statement accounts for that, producing 25 sprites from each loop
        while self.enemynum1 > 0:
            self.enemySprite = arcade.Sprite(enemytexture, enemyscale)
            self.enemySprite.position = (r.randrange(0, screenwidth), r.randrange(0, screenheight))
            if (((self.enemySprite.center_x < self.pos1) or (self.enemySprite.center_x > self.pos2)) and ((self.enemySprite.center_y < self.pos3) or (self.enemySprite.center_y > self.pos4))) :
                self.enemyList.append(self.enemySprite)
                self.enemynum1 -= 1
            else:
                continue

        while self.enemynum2 > 0:
            self.enemySprite = arcade.Sprite(enemy2texture, enemyscale)
            self.enemySprite.position = (r.randrange(0, screenwidth), r.randrange(0, screenheight))
            if (((self.enemySprite.center_x < self.pos1) or (self.enemySprite.center_x > self.pos2)) and ((self.enemySprite.center_y < self.pos3) or (self.enemySprite.center_y > self.pos4))) :
                self.enemyList.append(self.enemySprite)
                self.enemynum2 -= 1
            else:
                continue

#   Draws to the window(mostly used for our sprite-lists in this case)
    def on_draw(self):
        self.clear()

        arcade.draw_lrwh_rectangle_textured(0, 0, screenwidth, screenheight, self.background_image)
        arcade.draw_text(f'Score: {self.score}', (screenwidth // 2) - 50, screenheight - 35, font_size = 20, color=arcade.color.BLACK)
        arcade.draw_text(f'Ammo: {self.ammo}/15', screenwidth * .1, screenheight - 35, font_size = 20, color=arcade.color.RED, bold=True)

        self.playerList.draw()
        self.enemyList.draw()
        self.itemList.draw()

#   This method is used to position sprites and other things that require updates every frame(ie enemy/loot position)
    def on_update(self, delta_time: float, spatialhashing = True):
        if self.isdead:
            gameview = GameOverView()
            self.window.show_view(gameview)
            global finalscore
            finalscore = self.score
        if self.paused:
            return
        else:
            self.itemList.update()
            self.enemyList.update()
            self.playerList.update()

            self.playerSprite.center_x += self.playerSpritevelx * delta_time
            self.playerSprite.center_y += self.playerSpritevely * delta_time

            if not self.hasmousebeenclicked:
                self.weapon.center_x = self.playerSprite.center_x
                self.weapon.center_y = self.playerSprite.center_y

            for enemy in self.enemyList:
                if enemy.center_x < self.playerSprite.center_x:
                    enemy.center_x += min(enemyspeed, self.playerSprite.center_x - enemy.center_x)
                elif enemy.center_x > self.playerSprite.center_x:
                    enemy.center_x -= min(enemyspeed, enemy.center_x - self.playerSprite.center_x)

            for enemy in self.enemyList:
                if enemy.center_y < self.playerSprite.center_y:
                    enemy.center_y += min(enemyspeed, self.playerSprite.center_y - enemy.center_y)
                elif enemy.center_y > self.playerSprite.center_y:
                    enemy.center_y -= min(enemyspeed, enemy.center_y - self.playerSprite.center_y)

            enemyColisionList = arcade.check_for_collision_with_list(self.playerSprite, self.enemyList)
            for enemy in enemyColisionList:
                self.isdead = True
            bulletCollsionList = arcade.check_for_collision_with_list(self.weapon, self.enemyList)
            for enemy in bulletCollsionList:
                enemy.remove_from_sprite_lists()
                self.score += 1

            if len(self.enemyList) == 0:
                self.round += 1
                self.setup()

#   Deals with mouse input
    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        if self.paused:
            return
        if self.ammo < 1:
            return
#       A lot of code for this is very derivative of the arcade library, I wasn't sure how to do the math for assigning the bullet angle
        self.ammo -= 1
        self.hasmousebeenclicked = True
        self.weapon.center_x = self.playerSprite.center_x
        self.weapon.center_y = self.playerSprite.center_y
        gapx = x - self.weapon.center_x
        gapy = y - self.weapon.center_y
        bulletAngle = math.atan2(gapy, gapx)
        self.weapon.angle = math.degrees(bulletAngle)
        self.weapon.change_x = math.cos(bulletAngle) * bulletspeed
        self.weapon.change_y = math.sin(bulletAngle) * bulletspeed

#    Deals with input on key press
    def on_key_press(self, key, modifiers):
        if key == arcade.key.LEFT or key == arcade.key.A:
            self.playerSpritevelx = -300
        if key == arcade.key.RIGHT or key == arcade.key.D:
            self.playerSpritevelx = 300
        if key == arcade.key.UP or key == arcade.key.W:
            self.playerSpritevely = 300
        if key == arcade.key.DOWN or key == arcade.key.S:
            self.playerSpritevely = -300
        if key == arcade.key.ESCAPE:
            arcade.close_window()
        if key == arcade.key.P:
            self.paused = not self.paused

#    This method deals with input from releasing keys
    def on_key_release(self, key, modifiers: int):
        if key == arcade.key.LEFT or key == arcade.key.A:
            self.playerSpritevelx = 0
        if key == arcade.key.RIGHT or key == arcade.key.D:
            self.playerSpritevelx = 0
        if key == arcade.key.UP or key == arcade.key.W:
            self.playerSpritevely = 0
        if key == arcade.key.DOWN or key == arcade.key.S:
            self.playerSpritevely = 0

def main():
    window = arcade.Window(screenwidth, screenheight, title, full_screen, isWindowResizable)
    startview = StartScreenView()
    window.show_view(startview)
    arcade.run()


if __name__ == '__main__':
    main()



