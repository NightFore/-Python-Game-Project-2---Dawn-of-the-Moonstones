import sys
import os
import random
import pickle
import pygame
import time
import pygame_textinput

#Setup
pygame.init()
display_width = 800
display_height = 600
gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("Dawn of Moonstones")
clock = pygame.time.Clock()



#Ressources

black = (0,0,0)
green = (0,176,80)
bright_green = (96,255,96)
red = (200,0,0)
bright_red = (255,96,96)
game_ui_color = (245,218,168)
text_ui_color = (104,187,230)
text_action_color = black #Temporary

sky_color = (153,217,234)
ground_color = (34,177,76)


character_player = pygame.image.load(os.path.join("Data", "Image", "character_player_iris.png"))
background_main_menu = pygame.image.load(os.path.join("Data", "Image", "main_menu.jpg"))

def Game_Save():
    with open("savefile", "wb") as f:
        pickle.dump(PlayerIG, f)

    
def Game_Load():
    if os.path.exists("savefile") == True:
        with open("savefile", "rb") as f:
            global PlayerIG
            PlayerIG = pickle.load(f)
        GameStateIG.Game_Event_Load = True
        LvL1()
    else:
        main_menu()  


def quit_game():
    pygame.quit()
    quit()

    


# Game
class GameState:
    def __init__(self, name):
        self.Game_Event_Load = False

        self.Text_Line =    ["", "", "", "", "", "", "", "", ""]
        self.Text_Order = 1
        self.Text_Action =  ["", "", "", "", "", "", "", "", ""]
        self.Game_Event = [False,False,False,False,False,False]
        self.Game_Fight_Attack = [False,False]
        self.State = ""
        self.State_Inventory = False
        self.State_Fight = ""
        self.Escape = ""
        
        self.Player_Status = ["", "", "", "", "", "", "", "", "", "", ""]
        self.Leveling_UP = False
        
        self.textinput = pygame_textinput.TextInput()
        self.Line_x = 0
        self.Minimal = 1
        self.Maximal = 8
        
        self.Variable_x = 0

GameStateIG = GameState("GameState")

def Game_State_Reset(GameState):
    # LvL1
    if GameState == "LvL1":
        GameStateIG.Text_Line = ["", "", "", "", "", "", "", "", ""]
        GameStateIG.Text_Order = 1
        GameStateIG.Game_Event = [False,False,False,False,False,False]
        GameStateIG.Game_Fight_Attack = [False,False]
        GameStateIG.State = ""
        GameStateIG.State_Inventory = False
        GameStateIG.State_Fight = ""
        GameStateIG.Escape == ""
        GameStateIG.Variable_x = 0

        GameStateIG.Leveling_UP = False

    # Fight
    elif GameState == "Fight":
        GameStateIG.Text_Line = ["", "", "", "", "", "", "", "", ""]
        GameStateIG.Game_Fight_Attack = [False,False]
        GameStateIG.Text_Order = 1

    elif GameState == "Equip":
        GameStateIG.Text_Line = ["", "", "", "", "", "", "", "", ""]
        GameStateIG.Text_Order = 0
        GameStateIG.Game_Event[3] = False
        GameStateIG.Variable_x = 2

    elif GameState == "Store":
        GameStateIG.Text_Line = ["",GameStateIG.Text_Line[1],"", "", "", "", "", "", ""]
        
    

def Player_Status():
    # Weapon
    if "Lance" in PlayerIG.curweap:
        GameStateIG.Player_Status[0] = "Lance"
        
    # Character
    GameStateIG.Player_Status[1] = "Name:"
    GameStateIG.Player_Status[2] = "%s"             % PlayerIG.name
    GameStateIG.Player_Status[3] = "Level: %i"      % PlayerIG.level
    GameStateIG.Player_Status[4] = "Experience: %i" % PlayerIG.experience
    GameStateIG.Player_Status[5] = "Gold: %i"       % PlayerIG.gold

    # Status
    GameStateIG.Player_Status[6] = "Health: %i/%i"  % (PlayerIG.health, PlayerIG.maxhealth)
    GameStateIG.Player_Status[7] = "Strength: %i"   % PlayerIG.strength
    GameStateIG.Player_Status[8] = "Speed: %i"      % PlayerIG.speed
    GameStateIG.Player_Status[9] = "Defense: %i"    % PlayerIG.defense
    GameStateIG.Player_Status[10] = "Resistance: %i" % PlayerIG.resistance

    # Player Health
    if PlayerIG.health <= 0:
        PlayerIG.health = 0

    # Leveling UP
    if GameStateIG.Leveling_UP == True:
        LvLUP()






                    
def Game_Action_Choice(Action):
    #Cheat Codes
    if GameStateIG.Text_Line[0] == "Death":
        PlayerIG.health = 1

    if GameStateIG.Text_Line[0] == "whosyourdaddy":
        PlayerIG.experience = 99
        
    # LvL1()
    if Action == "LvL1":
        GameStateIG.Text_Action[1] = "1) Move"
        GameStateIG.Text_Action[2] = "2) Potion"
        GameStateIG.Text_Action[3] = "3) Store"
        GameStateIG.Text_Action[4] = "4) Inventory"
        GameStateIG.Text_Action[5] = "5) Save"
        GameStateIG.Text_Action[6] = "6) Exit"
        
        if GameStateIG.Text_Line[0] == "1" or GameStateIG.Text_Line[0] == "1)" or GameStateIG.Text_Line[0] == "Move":
            GameStateIG.Text_Line[0] = ""
            GameStateIG.State = "Move"
            GameStateIG.Game_Event[0] = False
            GameStateIG.Game_Event[1] = True
            move()
            
        if GameStateIG.Text_Line[0] == "2" or GameStateIG.Text_Line[0] == "2)" or GameStateIG.Text_Line[0] == "Potion":
            GameStateIG.Text_Line[0] = ""
            GameStateIG.State = "Potion"
            GameStateIG.Game_Event[0] = False
            GameStateIG.Game_Event[1] = True
            Potion("LvL1")
            
        if GameStateIG.Text_Line[0] == "3" or GameStateIG.Text_Line[0] == "3)" or GameStateIG.Text_Line[0] == "Store":
            GameStateIG.Text_Line[0] = ""
            GameStateIG.State = "Store"
            GameStateIG.Game_Event[0] = False
            GameStateIG.Game_Event[1] = True
            Store()
            
        if GameStateIG.Text_Line[0] == "4" or GameStateIG.Text_Line[0] == "4)" or GameStateIG.Text_Line[0] == "Inventory":
            GameStateIG.Text_Line[0] = ""
            GameStateIG.State = "Inventory"
            GameStateIG.Game_Event[0] = False
            GameStateIG.Game_Event[1] = True
            Inventory()
            
        if GameStateIG.Text_Line[0] == "5" or GameStateIG.Text_Line[0] == "5)" or GameStateIG.Text_Line[0] == "Save":
            GameStateIG.Text_Line[0] = ""
            GameStateIG.State = "Save"
            GameStateIG.Game_Event[0] = False
            GameStateIG.Game_Event[1] = True
            Game_Save()
            
        if GameStateIG.Text_Line[0] == "6" or GameStateIG.Text_Line[0] == "6)" or GameStateIG.Text_Line[0] == "Exit":
            GameStateIG.Text_Line[0] = ""
            exit()

    # Fight()
    if Action == ("Fight"):
        if GameStateIG.Game_Event[2] == False and GameStateIG.State_Fight == "Fight":
            if GameStateIG.Text_Line[0] == "1" or GameStateIG.Text_Line[0] == "1)" or GameStateIG.Text_Line[0] == "Attack":
                GameStateIG.Text_Line[0] = ""
                GameStateIG.State_Fight = "Attack"
                attack()
                
            if GameStateIG.Text_Line[0] == "2" or GameStateIG.Text_Line[0] == "2)" or GameStateIG.Text_Line[0] == "Defend":
                GameStateIG.Text_Line[0] = ""
                GameStateIG.State_Fight = "Defend"
                Defend()
                
            if GameStateIG.Text_Line[0] == "3" or GameStateIG.Text_Line[0] == "3)" or GameStateIG.Text_Line[0] == "Potion":
                GameStateIG.Text_Line[0] = ""
                GameStateIG.State_Fight = "Potion"
                Potion("Fight")
                
            if GameStateIG.Text_Line[0] == "4" or GameStateIG.Text_Line[0] == "4)" or GameStateIG.Text_Line[0] == "Run":
                GameStateIG.Text_Line[0] = ""
                GameStateIG.State_Fight = "Run"
                Run()

    # Inventory()
    if Action == ("Inventory"):
        if GameStateIG.Text_Line[0] == "1" or GameStateIG.Text_Line[0] == "1)" or GameStateIG.Text_Line[0] == "Equip Weapon":
            GameStateIG.State = "Equip Weapon"
            GameStateIG.State_Inventory = True
            GameStateIG.Game_Event[2] = False
            Equip("Weapon")
            
        if GameStateIG.Text_Line[0] == "2" or GameStateIG.Text_Line[0] == "2)" or GameStateIG.Text_Line[0] == "Equip Armor":
            pass
##            GameStateIG.State = "Equip Armor"
##            GameStateIG.State_Inventory = True
##            GameStateIG.Game_Event[2] = False
##            Equip("Armor")
            
        if GameStateIG.Text_Line[0] == "3" or GameStateIG.Text_Line[0] == "3)" or GameStateIG.Text_Line[0] == "Equip Accessory":
            pass
##            GameStateIG.State = "Equip Accessory"
##            GameStateIG.State_Inventory = True
##            GameStateIG.Game_Event[2] = False
##            Equip("Accessory")
            
        if GameStateIG.Text_Line[0] == "4" or GameStateIG.Text_Line[0] == "4)" or GameStateIG.Text_Line[0] == "Check Items":
            pass
##            GameStateIG.State = "Check Items"
##            GameStateIG.State_Inventory = True
##            GameStateIG.Game_Event[2] = False
##            pass
##            #Items()
            
        if GameStateIG.Text_Line[0] == "5" or GameStateIG.Text_Line[0] == "5)" or GameStateIG.Text_Line[0] == "Cancel":
            LvL1()


# Game UI
def game_ui():
#Line
    #Vertical
    pygame.draw.line(gameDisplay, black, (2.5, 400),     (2.5, 600),     5)
    pygame.draw.line(gameDisplay, black, (152.5, 400),   (152.5, 600),   5)
    pygame.draw.line(gameDisplay, black, (652.5, 400),   (652.5, 600),   5)
    pygame.draw.line(gameDisplay, black, (797.5, 400),   (797.5, 600),   5)

    #Horizontal
    pygame.draw.line(gameDisplay, black, (0, 397.5),    (800, 397.5), 5)
    pygame.draw.line(gameDisplay, black, (650, 497.5),  (800, 497.5), 4)
    pygame.draw.line(gameDisplay, black, (150, 572.5),  (650, 572.5), 5)
    pygame.draw.line(gameDisplay, black, (0, 597.5),    (800, 597.5), 5)
    
#Rectangle
    pygame.draw.rect(gameDisplay, game_ui_color, (5, 400, 145, 195))
    
    pygame.draw.rect(gameDisplay, game_ui_color, (155, 400, 495, 170))
    pygame.draw.rect(gameDisplay, game_ui_color, (155, 575, 495, 20))

    pygame.draw.rect(gameDisplay, game_ui_color, (655, 400, 140, 95))
    pygame.draw.rect(gameDisplay, game_ui_color, (655, 500, 140, 95))

# Line Text
    # Game_Text_Screen
    text_ui(GameStateIG.Text_Line[1], 157.5, 393)
    text_ui(GameStateIG.Text_Line[2], 157.5, 413.5)
    text_ui(GameStateIG.Text_Line[3], 157.5, 434)
    text_ui(GameStateIG.Text_Line[4], 157.5, 454.5)
    text_ui(GameStateIG.Text_Line[5], 157.5, 475)
    text_ui(GameStateIG.Text_Line[6], 157.5, 495.5)
    text_ui(GameStateIG.Text_Line[7], 157.5, 516)
    text_ui(GameStateIG.Text_Line[8], 157.5, 536.5)

    # Game_Action_Choice
    text_action(GameStateIG.Text_Action[1], 6, 400)
    text_action(GameStateIG.Text_Action[2], 6, 425)
    text_action(GameStateIG.Text_Action[3], 6, 450)
    text_action(GameStateIG.Text_Action[4], 6, 475)
    text_action(GameStateIG.Text_Action[5], 6, 500)
    text_action(GameStateIG.Text_Action[6], 6, 525)
    text_action(GameStateIG.Text_Action[7], 6, 550)

    # Character
    text_Player_Status(GameStateIG.Player_Status[1], 656, 400)
    text_Player_Status(GameStateIG.Player_Status[2], 656, 420)
    text_Player_Status(GameStateIG.Player_Status[3], 656, 440)
    text_Player_Status(GameStateIG.Player_Status[4], 656, 460)
    text_Player_Status(GameStateIG.Player_Status[5], 656, 480)

    #Status
    text_Player_Status(GameStateIG.Player_Status[6], 656, 500)
    text_Player_Status(GameStateIG.Player_Status[7], 656, 520)
    text_Player_Status(GameStateIG.Player_Status[8], 656, 540)
    text_Player_Status(GameStateIG.Player_Status[9], 656, 560)
    text_Player_Status(GameStateIG.Player_Status[10], 656, 580)


# Character Image
    if GameStateIG.Player_Status[0] == "Lance":
        gameDisplay.blit(character_player, (640,210))
        

def text_box(events):
    # Temporary background
    gameDisplay.fill((225, 225, 225))
    pygame.draw.rect(gameDisplay, sky_color, [0, 0, 800, 300])
    pygame.draw.rect(gameDisplay, ground_color, [0, 300, 800, 100])

    # Game UI
    game_ui()
        
    # Text Input
    if GameStateIG.textinput.update(events):
        GameStateIG.Text_Line[0] = GameStateIG.textinput.get_text()
        text_line_order()
            
        #Reset Text Input
        GameStateIG.textinput = pygame_textinput.TextInput()
            
    # Display
    gameDisplay.blit(GameStateIG.textinput.get_surface(), (155, 572.5))
    pygame.display.update()

def text_line_order():
    GameStateIG.Line_x = 0
    while GameStateIG.Line_x != GameStateIG.Text_Order:
        GameStateIG.Line_x += 1

    if GameStateIG.Line_x == GameStateIG.Text_Order :
        GameStateIG.Text_Order += 1

        if GameStateIG.Text_Order > GameStateIG.Maximal:
            GameStateIG.Line_x      = GameStateIG.Minimal
            GameStateIG.Text_Order  = GameStateIG.Minimal



#Text
def message_display(text, x, y, Text_Type):
    font = pygame.font.SysFont("comicsansms",50)
    TextSurf, TextRect = Text_Type(text, font)
    TextRect.center = (x, y)
    gameDisplay.blit(TextSurf, TextRect)
    pygame.display.update()

def text_title(text, font):
    textSurface = font.render(text, True, (210,100,240))
    return textSurface, textSurface.get_rect()

def text_title_selection(text, font):
    textSurface = font.render(text, True, (95,165,244))
    return textSurface, textSurface.get_rect()

def text_button(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()

    #Standalone
def text_ui(text, x, y):
    font = pygame.font.SysFont("comicsansms",25)
    aaa1 = font.render(text, 1, text_ui_color)
    gameDisplay.blit(aaa1,  (x,y))
    
def text_action(text, x, y):
    font = pygame.font.SysFont("",35)
    GameStateIG.Text_Line_1 = font.render(text, 1, text_action_color)
    gameDisplay.blit(GameStateIG.Text_Line_1,  (x,y))
    
def text_Player_Status(text, x, y):
    font = pygame.font.SysFont("",25)
    GameStateIG.Text_Line_1 = font.render(text, 1, text_action_color)
    gameDisplay.blit(GameStateIG.Text_Line_1,  (x,y))
    


#Button
def button(msg,x,y,w,h,ic,ac,Text_Type,action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    
    #Rectangle
    if x+w > mouse[0] >x and y+h > mouse[1] > y:
        pygame.draw.rect(gameDisplay, ac,(x,y,w,h))
        if click[0] ==1 and action !=None:
            action() 
    else:
        pygame.draw.rect(gameDisplay, ic,(x,y,w,h))

    #Text
    Text_Type = pygame.font.SysFont("comicsansms",20)
    textSurf, textRect = text_button(msg, Text_Type)
    textRect.center = ((x+(w/2)), (y+(h/2)))

    gameDisplay.blit(textSurf, textRect)
    pygame.display.update()






# Game Properties
weapons = {"Bronze Lance": 40, "Iron Lance":100}

class Player:
    def __init__(self, name):
        self.name = name
        self.maxhealth = 100
        self.health = self.maxhealth
        self.level = 1
        self.strength = 7
        self.speed = 5
        self.defense = 3
        self.resistance = 2
        self.experience = 0
        self.gold = 500
        self.potion = 2
        self.weap = ["Bronze Lance"]
        self.curweap = "Bronze Lance"

    @property
    def attack(self):
        attack = self.strength
        if self.curweap == "Bronze Lance":
            attack += 3

        if self.curweap == "Iron Lance":
            attack += 5

        return attack
    

class Bandit:
    def __init__(self, name):
        self.name = name
        self.maxhealth = 40
        self.health = self.maxhealth
        self.attack = 4
        self.speed = 1
        self.defense = 0
        self.resistance = 0
        self.experiencegain = 20
        self.goldgain = 5
BanditIG = Bandit("Bandit")

class Fighter:
    def __init__(self, name):
        self.name = name
        self.maxhealth = 50
        self.health = self.maxhealth
        self.attack = 6
        self.speed = 3
        self.defense = 2
        self.resistance = 1
        self.experiencegain = 35
        self.goldgain = 25
FighterIG = Fighter("Fighter")







def main_menu():
    gameDisplay.blit(background_main_menu, (0,0))
    message_display("Dawn of the Moonstones", (display_width/2),(display_height*0.2), text_title)
    gameExit = False
    while not gameExit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        button("Start", display_width/2-display_width/16, display_height*0.45-display_height/32, display_width/8, display_height/12, green, red, text_title_selection, game_intro_1)
        button("Load",  display_width/2-display_width/16, display_height*0.60-display_height/32, display_width/8, display_height/12, green, red, text_title_selection, Game_Load)
        button("Exit",  display_width/2-display_width/16, display_height*0.75-display_height/32, display_width/8, display_height/12, green, red, text_title_selection, quit_game)



def game_intro_1():
    gameExit = False
    while not gameExit:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                exit()

# Game Core
        global PlayerIG
        text_box(events)

    # Game Intro 1 :
        # Player Name
        if GameStateIG.Text_Order == 1 or GameStateIG.Text_Order == 2:
            GameStateIG.Text_Line[1] = "What is your name?"
            GameStateIG.Text_Line[2] = "->"
            GameStateIG.Text_Order = 2

        if GameStateIG.Text_Order == 3 and GameStateIG.Text_Line[0] != "":
            PlayerIG = Player(GameStateIG.Text_Line[0])
            game_intro_2()
        
        # Game_Event[1]
        if GameStateIG.Text_Order == 3 and GameStateIG.Text_Line[0] == "" or GameStateIG.Game_Event[1] == True:
            GameStateIG.Text_Line[2] = "That doesn't seem like a real name!"
            GameStateIG.Text_Line[3] = "->"
            GameStateIG.Game_Event[1] = True

            if GameStateIG.Text_Order == 4 or GameStateIG.Game_Event[2] == True:
                GameStateIG.Text_Line[3] = "Please, tell me your name!"
                GameStateIG.Text_Line[4] = "->"
                GameStateIG.Game_Event[2] = True

                if GameStateIG.Text_Order == 5 and GameStateIG.Text_Line[0] == "":
                    GameStateIG.Text_Order = 4

                # Player Name - Game_Event[1]
                elif GameStateIG.Text_Order == 5 and GameStateIG.Text_Line[0] != "":
                    PlayerIG = Player(GameStateIG.Text_Line[0])
                    game_intro_2()
                    


def game_intro_2():
# Game State Reset
    Game_State_Reset("LvL1")
    GameStateIG.Game_Event[0] = True
    
    gameExit = False
    while not gameExit:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                exit()

# Game Core
        text_box(events)

    # Game Intro 2 :
        # Game Event[0]
        if GameStateIG.Text_Order == 1 and GameStateIG.Game_Event[0] == True:
            GameStateIG.Text_Line[1] = ("I see... Then, %s... " % PlayerIG.name)
            GameStateIG.Text_Line[2] = "->"
            GameStateIG.Text_Order = 2

        if GameStateIG.Text_Order == 3 and GameStateIG.Game_Event[0] == True:
            GameStateIG.Text_Line[2] = "You have to wake up!"
            GameStateIG.Text_Line[3] = "->"

        if GameStateIG.Text_Order == 4 and GameStateIG.Game_Event[0] == True:
            GameStateIG.Text_Line[3] = "I will watch over you, but right now..."
            GameStateIG.Text_Line[4] = "->"
            
        if GameStateIG.Text_Order == 5 and GameStateIG.Game_Event[0] == True:
            GameStateIG.Text_Line[4] = "You have a long road awaiting you..."
            GameStateIG.Text_Line[5] = "->"


        # Transition 
        if GameStateIG.Text_Order == 6 and GameStateIG.Game_Event[0] == True:
            Game_State_Reset("LvL1")
            GameStateIG.Text_Order = 2
            GameStateIG.Game_Event[1] = True


        # Game Event[1]
        if GameStateIG.Text_Order == 2 and GameStateIG.Game_Event[1] == True:
            GameStateIG.Text_Line[1] = "Huh? Who was that?"
            GameStateIG.Text_Line[2] = "->"

        if GameStateIG.Text_Order == 3 and GameStateIG.Game_Event[1] == True:
            GameStateIG.Text_Line[2] = "Where am I?"
            GameStateIG.Text_Line[3] = "->"

        if GameStateIG.Text_Order == 4 and GameStateIG.Game_Event[1] == True:
            GameStateIG.Text_Line[3] = "Why am I inside a forest now?"
            GameStateIG.Text_Line[4] = "->"
            
        if GameStateIG.Text_Order == 5 and GameStateIG.Game_Event[1] == True:
            GameStateIG.Text_Line[4] = "I should try to find a way out..."
            GameStateIG.Text_Line[5] = "->"
        
        if GameStateIG.Text_Order == 6 and GameStateIG.Game_Event[1] == True:
            LvL1()



def LvL1():
# Game State Reset
    Game_State_Reset("LvL1")
    GameStateIG.Game_Event[0] = True
    
    gameExit = False
    while not gameExit:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                exit()

# Game Core
        text_box(events)
        Player_Status()

    # Game Action Choice
        # Neutral State
        if GameStateIG.Game_Event[0] == True:
            Game_Action_Choice("LvL1")
            GameStateIG.Text_Line[1] = "What should I do?"    
            GameStateIG.Text_Line[2] = "->"
            GameStateIG.Text_Order = 1
            
        # 1) Move
        if GameStateIG.Game_Event[1] == True and GameStateIG.State == "Move":
            GameStateIG.Text_Line[2] = "You encountered a %s!" % ennemy.name
            GameStateIG.Text_Line[3] = "->"

            if GameStateIG.Text_Order == 2 and GameStateIG.State == "Move":
                GameStateIG.State = "Fight"
                
        # 1) Move - Fight State
        if GameStateIG.Game_Event[1] == True and GameStateIG.State == "Fight":
            Fight()


        # 2) Potion
        if GameStateIG.Game_Event[1] == True and GameStateIG.State == "Potion":
            Potion("LvL1")

        # 3) Store
        if GameStateIG.Game_Event[1] == True and GameStateIG.State == "Store":
            Store()

        # 4) Inventory
        if GameStateIG.Game_Event[1] == True and GameStateIG.State == "Inventory":
            if GameStateIG.Game_Event[3] == False:
                Inventory()

        if GameStateIG.Game_Event[1] == True and GameStateIG.State_Inventory == True:
            if GameStateIG.State == "Equip Weapon":
                Equip("Weapon")
            elif GameStateIG.State == "Equip Armor":
                Equip("Armor")
            elif GameStateIG.State == "Equip Accessory":
                Equip("Accessory")
            elif GameStateIG.State == "Check Items":
                Equip("Items")

        # 5) Save
        if GameStateIG.Game_Event[1] == True and GameStateIG.State == "Save":
            GameStateIG.Text_Line[2] = "Game has been saved!"
            GameStateIG.Text_Line[3] = "->"

            if GameStateIG.Text_Order == 3:
                LvL1()

        # Game_Load :
        if GameStateIG.Game_Event_Load == True:
            GameStateIG.Text_Line[1] = "Game has been loaded!"
            GameStateIG.Text_Line[2] = "->"
            GameStateIG.Game_Event[0] = False

            if GameStateIG.Text_Order == 2:
                GameStateIG.Game_Event_Load = False
                LvL1() 


def move():
    global ennemy
    ennemynum = random.randint(1, 2)
    if ennemynum == 1:
        ennemy = BanditIG
    elif ennemynum == 2:
        ennemy = FighterIG




def Potion(GameState):     
    if GameState == "LvL1":
        # Variable("LvL1")
        if GameStateIG.Game_Event[2] == False:
            GameStateIG.Game_Event[2] = True
            GameStateIG.Text_Order = 1
            GameStateIG.Variable_x = 2
        # Leave Potion("LvL1")
        if GameStateIG.Game_Event[4] == True:
            GameStateIG.Game_Event[3] = False
            LvL1()
            
    if GameState == "Fight":
        # Variable("Fight")
        if GameStateIG.Game_Event[2] == False:
            GameStateIG.Game_Event[2] = True
            Game_State_Reset("Fight")
            GameStateIG.Text_Order = 1
            GameStateIG.Variable_x = 1

        # Leave Potion("Fight")
        if GameStateIG.Game_Event[4] == True:
            GameStateIG.Game_Event[2] = False
            GameStateIG.Game_Event[3] = False
            GameStateIG.State_Fight = ""


# Drinking Potion
    # Neutral/General State
    if PlayerIG.potion > 0 or GameStateIG.Game_Event[3] == True:
        if GameStateIG.Text_Order == 1:
            GameStateIG.Text_Line[GameStateIG.Variable_x] = "You drank a Potion!"
            GameStateIG.Text_Line[GameStateIG.Variable_x+1] = "->"
            
        elif GameStateIG.Text_Order == 2:    
            GameStateIG.Text_Line[GameStateIG.Variable_x+1] = "You recovered 25 HP!"
            GameStateIG.Text_Line[GameStateIG.Variable_x+2] = "->"
            
            if GameStateIG.Game_Event[3] == False:
                # Recovering HP
                PlayerIG.potion -= 1
                PlayerIG.health += 25

                # if Exceeding Max HP
                if PlayerIG.health > PlayerIG.maxhealth:
                    PlayerIG.health = PlayerIG.maxhealth
                GameStateIG.Game_Event[3] = True
                
    # LvL1 State
        elif GameState == "LvL1":
            if GameStateIG.Text_Order == 3:
                GameStateIG.Game_Event[4] = True

    # Fight State
        elif GameState == "Fight":
            # Ennemy Phase
            if GameStateIG.Text_Order == 3:
                GameStateIG.Text_Line[GameStateIG.Variable_x+2] = ""
                GameStateIG.Text_Line[GameStateIG.Variable_x+3] = "%s attacks!" % ennemy.name
                GameStateIG.Text_Line[GameStateIG.Variable_x+4] = "->"
                
            elif GameStateIG.Text_Order == 4:
                GameStateIG.Text_Line[GameStateIG.Variable_x+4] = "You received %i damage!" % ennemy.attack
                GameStateIG.Text_Line[GameStateIG.Variable_x+5] = "->"
                
                # Damage Calculation
                if GameStateIG.Game_Fight_Attack[1] == False:
                    PlayerIG.health -= ennemy.attack
                    GameStateIG.Game_Fight_Attack[1] = True
                    
                # Lose Condition
            if GameStateIG.Text_Order == 5 :
                if PlayerIG.health <= 0:
                    death()
                else:
                    GameStateIG.Game_Event[4] = True


    # Not Enough Potion
    elif PlayerIG.potion == 0:
        if GameStateIG.Text_Order == 1:
            GameStateIG.Text_Line[GameStateIG.Variable_x] = "You don't have any potions!"
            GameStateIG.Text_Line[GameStateIG.Variable_x+1] = "->"
        
        if GameStateIG.Text_Order == 2:
            GameStateIG.Game_Event[4] = True

            

def Store():
    # Welcome Statement
    if GameStateIG.Game_Event[2] == False:
        Game_State_Reset("Store")
        GameStateIG.Text_Order = 1
        GameStateIG.Game_Event[2] = True
        GameStateIG.Game_Event[3] = False

    elif GameStateIG.Game_Event[2] == True and GameStateIG.Game_Event[3] == False:
        GameStateIG.Text_Line[1] = "Hello Traveler!"
        GameStateIG.Text_Line[2] = "->"

    # List of Actions
    if GameStateIG.Text_Order == 2:
        GameStateIG.Game_Event[2] = True
        GameStateIG.Game_Event[3] = False
        
        GameStateIG.Text_Line[2] = "What would you like to buy?"
        GameStateIG.Text_Line[3] = "Bronze Lance (%s Gold)" % weapons["Bronze Lance"]
        GameStateIG.Text_Line[4] = "Iron Lance (%s Gold)" % weapons["Iron Lance"]
        GameStateIG.Text_Line[5] = "Potion (50 Gold)"
        GameStateIG.Text_Line[6] = "Cancel"
        GameStateIG.Text_Line[7] = "->"

    # Text Input
    elif GameStateIG.Text_Order == 3 and GameStateIG.Game_Event[3] == False:
        # Prevent Looping
        GameStateIG.Game_Event[3] = True
        
        # Buy a New Weapon
        if GameStateIG.Text_Line[0] in weapons:
            # Confirming Purchase
            if PlayerIG.gold >= weapons[GameStateIG.Text_Line[0]]:
                PlayerIG.gold -= weapons[GameStateIG.Text_Line[0]]
                PlayerIG.weap.append(GameStateIG.Text_Line[0])
                
                Game_State_Reset("Store")
                GameStateIG.Text_Line[2] = "Thank you for your Purchase!"
                GameStateIG.Text_Line[3] = "->"
                    
            # No Enough Money
            else:
                Game_State_Reset("Store")
                GameStateIG.Text_Line[2] = "Sorry, but you don't have enough Gold!"
                GameStateIG.Text_Line[3] = "->"

        # Leave the Shop
        elif GameStateIG.Text_Line[0] == "Potion":
            PlayerIG.gold >= 50
            PlayerIG.potion += 1
            
            Game_State_Reset("Store")
            GameStateIG.Text_Line[2] = "Thank you for your Purchase!"
            GameStateIG.Text_Line[3] = "->"

        # Leave the Shop
        elif GameStateIG.Text_Line[0] == "Cancel":
            LvL1()

        # Missing Weapon
        else:
            Game_State_Reset("Store")
            GameStateIG.Text_Line[2] = "Sorry but I don't own that sort of Item!"
            GameStateIG.Text_Line[3] = "->"

    # Loop
    elif GameStateIG.Text_Order == 4:
        GameStateIG.Text_Order = 2


            


def Inventory():
    # Welcome Statement
    if GameStateIG.Text_Order == 2 and GameStateIG.Game_Event[2] == False:
        GameStateIG.Game_Event[2] = True
        GameStateIG.Text_Order = 1

    # List of Actions
    elif GameStateIG.Text_Order == 1:
        GameStateIG.Text_Line[1] = "What am I going to do?"
        GameStateIG.Text_Line[2] = "1) Equip Weapon"
        GameStateIG.Text_Line[3] = "2) Equip Armor (Not Included)" # To be Added
        GameStateIG.Text_Line[4] = "3) Equip Accessory (Not Included)" # To be Added
        GameStateIG.Text_Line[5] = "4) Check Items (Not Included)" # To be Added
        GameStateIG.Text_Line[6] = "5) Cancel"
        GameStateIG.Text_Line[7] = "->"

    # Input Action
    elif GameStateIG.Text_Order == 2:
        # Game Action Choice
        Game_Action_Choice("Inventory")

        # Loop
        GameStateIG.Text_Order = 1

        

def Equip(Category):
    # Setup
    if GameStateIG.Game_Event[2] == False:
        Game_State_Reset("Equip")
        GameStateIG.Game_Event[2] = True



    # Exit Equip
    if GameStateIG.Text_Order == 2 and GameStateIG.Text_Line[0] == "Cancel":
        GameStateIG.State = "Inventory"
        GameStateIG.State_Inventory = False
        GameStateIG.Game_Event[2] = False
    # Loop
    elif GameStateIG.Text_Order == 3:
        GameStateIG.Game_Event[2] = False



    # Equip(Weapon)
    elif Category == "Weapon":
        # List of Weapons
        if GameStateIG.Text_Order == 0:
            GameStateIG.Text_Line[1] = "Current Weapon : %s" % PlayerIG.curweap
            for weapon in PlayerIG.weap:
                GameStateIG.Text_Line[GameStateIG.Variable_x] = "%s" % weapon
                GameStateIG.Variable_x += 1
                
            GameStateIG.Text_Line[GameStateIG.Variable_x] = "Cancel"
            GameStateIG.Text_Line[GameStateIG.Variable_x+1] = "->"
            GameStateIG.Text_Order = 1

        # Text Input
        if GameStateIG.Text_Order == 2:
            # Prevent Looping
            if GameStateIG.Game_Event[3] == False:
                
                # Equip Current Weapon
                if GameStateIG.Text_Line[0] == PlayerIG.curweap:
                    GameStateIG.Text_Line = [GameStateIG.Text_Line[0], "", "", "", "", "", "", "", ""]
                    GameStateIG.Text_Line[1] = "You already have equip %s!" % PlayerIG.curweap
                    GameStateIG.Text_Line[2] = "->"

                # Equip New Weapon
                elif GameStateIG.Text_Line[0] in PlayerIG.weap:
                    PlayerIG.curweap = GameStateIG.Text_Line[0]
                    GameStateIG.Text_Line = [GameStateIG.Text_Line[0], "", "", "", "", "", "", "", ""]
                    GameStateIG.Text_Line[1] = "You have equipped %s!" % PlayerIG.curweap
                    GameStateIG.Text_Line[2] = "->"

                # Equip Missing Weapon
                else:
                    GameStateIG.Text_Line[GameStateIG.Variable_x] = ""
                    GameStateIG.Text_Line[GameStateIG.Variable_x+1] = "This weapon isn't in your inventory!"
                    GameStateIG.Text_Line[GameStateIG.Variable_x+2] = "->"
                    
                GameStateIG.Game_Event[3] = True





def Fight():
    Game_Action_Choice("Fight")
    if GameStateIG.Game_Event[2] == False and GameStateIG.State == "Fight":
        Game_State_Reset("Fight")
        GameStateIG.State_Fight = "Fight"
        
        GameStateIG.Text_Line[1] ="%s   vs  %s" % (PlayerIG.name, ennemy.name)
        GameStateIG.Text_Line[2] ="%s's Health: %i/%i" % (PlayerIG.name, PlayerIG.health, PlayerIG.maxhealth)
        GameStateIG.Text_Line[3] ="%s's Health: %i/%i" % (ennemy.name, ennemy.health, ennemy.maxhealth)
        GameStateIG.Text_Line[4] ="Potions: %i" % PlayerIG.potion
        GameStateIG.Text_Line[5] = ""
        GameStateIG.Text_Line[6] = "What should I do?"
        GameStateIG.Text_Line[7] = "->"
        GameStateIG.Text_Order = 1

        GameStateIG.Text_Action[1] = "1) Attack"
        GameStateIG.Text_Action[2] = "2) Defend"
        GameStateIG.Text_Action[3] = "3) Potion"
        GameStateIG.Text_Action[4] = "4) Run"
        GameStateIG.Text_Action[5] = ""
        GameStateIG.Text_Action[6] = ""

    # Win Condition
    if ennemy.health <= 0 and GameStateIG.Game_Event[3] == True:
        win()

    # Lose Condition
    elif PlayerIG.health <= 0 and GameStateIG.Game_Event[3] == True:
        death()


        
    # 1) Attack    
    elif GameStateIG.State_Fight == "Attack":
        attack()
        
    # 2) Defend    
    elif GameStateIG.State_Fight == "Defend":
        Defend()
        
    # 2) Defend    
    elif GameStateIG.State_Fight == "Potion":
        Potion("Fight")
        
    # 4) Attack    
    elif GameStateIG.State_Fight == "Run":
        Run()
            

def attack():
     # Game State Reset
    if GameStateIG.Game_Event[2] == False:
        GameStateIG.Game_Event[2] = True
        Game_State_Reset("Fight")


    # Player Phase
    if GameStateIG.Text_Order == 1:
        GameStateIG.Text_Line[1] ="%s attacks!" % PlayerIG.name
        GameStateIG.Text_Line[2] = "->"
        
    if GameStateIG.Text_Order == 2:
        GameStateIG.Text_Line[2] ="%s takes %i damage!" % (ennemy.name, PlayerIG.attack)
        GameStateIG.Text_Line[3] = "->"
        
        # Damage Calculation
        if GameStateIG.Game_Fight_Attack[0] == False:
            ennemy.health -= PlayerIG.attack
            GameStateIG.Game_Fight_Attack[0] = True
            
        # Win Condition
    if GameStateIG.Text_Order == 3:
        GameStateIG.Text_Line[3] = ""
        if ennemy.health <= 0:
            win()
        else:
            GameStateIG.Text_Order = 4



    # Ennemy Phase
    if GameStateIG.Text_Order == 4:
        GameStateIG.Text_Line[4] = "%s attacks!" % ennemy.name
        GameStateIG.Text_Line[5] = "->"
        
    if GameStateIG.Text_Order == 5:
        GameStateIG.Text_Line[5] = "You received %i damage!" % ennemy.attack
        GameStateIG.Text_Line[6] = "->"
        
        # Damage Calculation
        if GameStateIG.Game_Fight_Attack[1] == False:
            PlayerIG.health -= ennemy.attack
            GameStateIG.Game_Fight_Attack[1] = True
            
        # Lose Condition
    if GameStateIG.Text_Order == 6 :
        if PlayerIG.health <= 0:
            death()

    # Attack Phase End
        else:
            GameStateIG.Game_Event[2] = False
            GameStateIG.State_Fight = ""






def Defend():
    if GameStateIG.Game_Event[2] == False:
        GameStateIG.Game_Event[2] = True
        Game_State_Reset("Fight")


    #Player Phase
    if GameStateIG.Text_Order == 1:
        GameStateIG.Text_Line[1] ="%s is defending himself!" % PlayerIG.name
        GameStateIG.Text_Line[2] = "->"

    if GameStateIG.Text_Order == 2:
        GameStateIG.Text_Line[2] = ""
        GameStateIG.Text_Order = 3


    # Ennemy Phase
    if GameStateIG.Text_Order == 3:
        GameStateIG.Text_Line[3] = "%s attacks!" % ennemy.name
        GameStateIG.Text_Line[4] = "->"
        
    if GameStateIG.Text_Order == 4:
        GameStateIG.Text_Line[4] = "You received %i damage!" % (ennemy.attack/2)
        GameStateIG.Text_Line[5] = "->"
        
        # Damage Calculation
        if GameStateIG.Game_Fight_Attack[1] == False:
            PlayerIG.health -= ennemy.attack/2
            GameStateIG.Game_Fight_Attack[1] = True
            
        # Lose Condition
    if GameStateIG.Text_Order == 5 :
        if PlayerIG.health <= 0:
            death()

    # Defend Phase End
        else:
            GameStateIG.Game_Event[2] = False
            GameStateIG.State_Fight = ""


        


def Run():
# Game State Reset
    if GameStateIG.Game_Event[2] == False:
        GameStateIG.Game_Event[2] = True
        Game_State_Reset("Fight")
        
        #Random Escape Value
        GameStateIG.Escape = random.randint(1, 3)
        
    #Player Phase
        # Success Escape
    if GameStateIG.Escape <= 2:
        if GameStateIG.Text_Order == 1:
            GameStateIG.Text_Line[1] ="You have successfully ran away!"
            GameStateIG.Text_Line[2] = "->"

        if GameStateIG.Text_Order == 2:
            LvL1()
        
        # Failure Escape
             # Ennemy Phase
    elif GameStateIG.Escape > 2:
        if GameStateIG.Text_Order == 1:
            GameStateIG.Text_Line[1] = "The ennemy caught you running away!"
            GameStateIG.Text_Line[2] = "->"
                
        if GameStateIG.Text_Order == 2:
            GameStateIG.Text_Line[2] = "%s attacks!" % ennemy.name
            GameStateIG.Text_Line[3] = "->"
                
        if GameStateIG.Text_Order == 3:
            GameStateIG.Text_Line[3] = "You received %i damage!" % ennemy.attack
            GameStateIG.Text_Line[4] = "->"
                
            # Damage Calculation
            if GameStateIG.Game_Fight_Attack[1] == False:
                PlayerIG.health -= ennemy.attack
                GameStateIG.Game_Fight_Attack[1] = True
                    
            # Lose Condition
        if GameStateIG.Text_Order == 4 :
            if PlayerIG.health <= 0:
                death()

        # Run Phase End
            else:
                GameStateIG.Game_Event[2] = False
                GameStateIG.State_Fight = ""


def win():
    if GameStateIG.Game_Event[3] == False:
        Game_State_Reset("Fight")
        PlayerIG.experience += ennemy.experiencegain
        GameStateIG.Game_Event[3] = True

    if GameStateIG.Text_Order == 1:
        GameStateIG.Text_Line[1] = "You felled %s!" % ennemy.name
        GameStateIG.Text_Line[2] = "->"

    if GameStateIG.Text_Order == 2:
        GameStateIG.Text_Line[2] ="You gained %i Experience!" % ennemy.experiencegain
        GameStateIG.Text_Line[3] = "->"

    if GameStateIG.Text_Order == 3:
        GameStateIG.Text_Line[3] ="You found %i Gold!" % ennemy.goldgain
        GameStateIG.Text_Line[4] = "->"

    if GameStateIG.Text_Order == 4:
        ennemy.health = ennemy.maxhealth
        if PlayerIG.experience < 100:
            LvL1()
        else:
            LvLUP()
            
def death():
    if GameStateIG.Game_Event[3] == False:
        Game_State_Reset("Fight")
        GameStateIG.Game_Event[3] = True

    if GameStateIG.Text_Order == 1:
        GameStateIG.Text_Line[1] = "The %s killed you!" % ennemy.name
        GameStateIG.Text_Line[2] = "->"

    if GameStateIG.Text_Order == 2:
        GameStateIG.Text_Line[2] = "Voice : ..."
        GameStateIG.Text_Line[3] = "->"

    if GameStateIG.Text_Order == 3:
        GameStateIG.Text_Line[3] = "It seems like that..."
        GameStateIG.Text_Line[4] = "->"

    if GameStateIG.Text_Order == 4:
        GameStateIG.Text_Line[4] = "You weren't the Chosen One..."
        GameStateIG.Text_Line[5] = "->"

    if GameStateIG.Text_Order == 5:
        GameStateIG.Text_Line[5] = "..."
        GameStateIG.Text_Line[6] = "->"

    if GameStateIG.Text_Order == 6:
        GameStateIG.Text_Line[6] = "This world is doomed..."
        GameStateIG.Text_Line[7] = "->"

    if GameStateIG.Text_Order == 7:
        GameStateIG.Text_Line[7] = ""
        GameStateIG.Text_Line[8] = "*Returning to Main Menu*"

    if GameStateIG.Text_Order == 8:
        main_menu()
        

def LvLUP():
    # Leveling UP
    if PlayerIG.experience >= 100 or GameStateIG.Leveling_UP == True:
        if GameStateIG.Leveling_UP == False:
            Game_State_Reset("LvL1")
            PlayerIG.level += 1
            PlayerIG.experience -= 100
            GameStateIG.Leveling_UP = True

        if GameStateIG.Text_Order == 1:
            GameStateIG.Text_Line[1] = "You reached Level %i!" % PlayerIG.level
            GameStateIG.Text_Line[2] = "->"

        # Stats Growth
        if GameStateIG.Text_Order == 2:
            x = 2
            if GameStateIG.Game_Event[1] == False:
                HP = random.randint(0,100)
                if HP <= 70:
                    PlayerIG.maxhealth += 1
                    GameStateIG.Text_Line[x] = "You gained 1 HP!"
                    x += 1
                    
                strength = random.randint(0, 100)
                if strength <= 35:
                    PlayerIG.strength += 1
                    GameStateIG.Text_Line[x] = "You gained 1 Strength!"
                    x += 1

                speed = random.randint(0, 100)
                if speed <= 65:
                    PlayerIG.speed += 1
                    GameStateIG.Text_Line[x] = "You gained 1 Speed!"
                    x += 1

                defense = random.randint(0,100)
                if defense <= 30:
                    PlayerIG.defense += 1
                    GameStateIG.Text_Line[x] = "You gained 1 Defense!"
                    x += 1

                resistance = random.randint(0,100)
                if resistance <= 30:
                    PlayerIG.resistance += 1
                    GameStateIG.Text_Line[x] = "You gained 1 Resistance!"
                    x += 1

                GameStateIG.Text_Line[x] = "->"
                GameStateIG.Game_Event[1] = True

        # Return to LvL1()
        if GameStateIG.Text_Order == 3:
            LvL1()
                
main_menu()
