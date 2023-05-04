import sys
import pygame
import random
import math
import bresenham
from sprite import Sprite
from pygame_combat import run_pygame_combat
from pygame_human_player import PyGameHumanPlayer
from landscape import get_landscape, get_combat_bg
from pygame_ai_player import PyGameAIPlayer
from lab7.ga_cities import *
from lab3.travel_cost import *
#pip3 install torch torchvision torchaudio
import torch
#pip install transformers
#Might need to enable long file paths on your PC for this to install properly
#On Windows, open registry editor and go to HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\FileSystem and enable LongPathsEnabled (switch 0 to 1)
from transformers import GPT2Tokenizer, GPT2LMHeadModel

from pathlib import Path

sys.path.append(str((Path(__file__) / ".." / "..").resolve().absolute()))

from lab2.cities_n_routes import get_randomly_spread_cities, get_routes


pygame.font.init()
game_font = pygame.font.SysFont("Comic Sans MS", 15)


def get_landscape_surface(size):
    landscape = get_landscape(size)
    print("Created a landscape of size", landscape.shape)
    pygame_surface = pygame.surfarray.make_surface(landscape[:, :, :3])
    return pygame_surface


def get_combat_surface(size):
    landscape = get_combat_bg(size)
    print("Created a landscape of size", landscape.shape)
    pygame_surface = pygame.surfarray.make_surface(landscape[:, :, :3])
    return pygame_surface


def setup_window(width, height, caption):
    pygame.init()
    window = pygame.display.set_mode((width, height))
    pygame.display.set_caption(caption)
    return window


def displayCityNames(city_locations, city_names):
    for i, name in enumerate(city_names):
        text_surface = game_font.render(str(i) + " " + name, True, (0, 0, 150))
        screen.blit(text_surface, city_locations[i])
#Finds whether two cities are connected
def cityConnected(cities, routeList, current, destination):
    x1 = cities[current][0]
    y1 = cities[current][1]
    x2 = cities[destination][0]
    y2 = cities[destination][1]

    for route in routeList:
        if (x1, y1) in route and (x2, y2) in route:
            return True
        
    return False
#Generates text based off of provided text (uses GPT-2)
def generateText(text, model, tokenizer):
    encoded_input = tokenizer.encode(text, return_tensors='pt')
    output = model.generate(encoded_input, pad_token_id=tokenizer.eos_token_id,
                            repetition_penalty = 2.5, max_length=200)
    entry = tokenizer.decode(output[0], skip_special_tokens=True)
    
    length = len(entry)

    lastPeriod = 0

    for letter in range(length):
        if(entry[letter] == "."):
            lastPeriod = letter
    #Makes sure that there are no incomplete sentences
    finalized = ""

    for letter in range(length):
        if(letter == lastPeriod):
            finalized += entry[letter]
            break
        else:
            finalized += entry[letter]

    return finalized
#Draws the journal onto the screen
def drawJournal(background, color, font, screen, journal, journalNum):
    lineOne = ""

    lineTwo = ""

    lineThree = ""

    lineFour = ""

    lineFive = ""

    lineSix = ""

    lineSeven = ""

    lineEight = ""

    lineNine = ""
    #Formats line size
    for letter in range(len(journal[journalNum])):
        if(letter <= 120):
            lineOne += journal[journalNum][letter]
        elif(letter <= 240):
            lineTwo += journal[journalNum][letter]
        elif(letter <= 360):
            lineThree += journal[journalNum][letter]
        elif(letter <= 480):
            lineFour += journal[journalNum][letter]
        elif(letter <= 600):
            lineFive += journal[journalNum][letter]
        elif(letter <= 720):
            lineSix += journal[journalNum][letter]
        elif(letter <= 840):
            lineSeven += journal[journalNum][letter]
        elif(letter <= 960):
            lineEight += journal[journalNum][letter]
        elif(letter > 960):
            lineNine += journal[journalNum][letter]

    screen.fill(background)

    fontOne = font.render(lineOne, True, color, background)
    fontTwo = font.render(lineTwo, True, color, background)
    fontThree = font.render(lineThree, True, color, background)
    fontFour = font.render(lineFour, True, color, background)
    fontFive = font.render(lineFive, True, color, background)
    fontSix = font.render(lineSix, True, color, background)
    fontSeven = font.render(lineSeven, True, color, background)
    fontEight = font.render(lineEight, True, color, background)
    fontNine = font.render(lineNine, True, color, background)

    screen.blit(fontOne, (20, 20))
    screen.blit(fontTwo, (20, 70))
    screen.blit(fontThree, (20, 120))
    screen.blit(fontFour, (20, 170))
    screen.blit(fontFive, (20, 220))
    screen.blit(fontSix, (20, 270))
    screen.blit(fontSeven, (20, 320))
    screen.blit(fontEight, (20, 370))
    screen.blit(fontNine, (20, 420))

class State:
    def __init__(
        self,
        current_city,
        destination_city,
        travelling,
        encounter_event,
        cities,
        routes,
        inJournal
    ):
        self.current_city = current_city
        self.destination_city = destination_city
        self.travelling = travelling
        self.encounter_event = encounter_event
        self.cities = cities
        self.routes = routes
        self.inJournal = inJournal

if __name__ == "__main__":
    size = width, height = 640, 480
    black = 1, 1, 1
    start_city = 0
    end_city = 9
    n_cities = 10
    sprite_path = "assets/lego.png"
    sprite_speed = 1
    #Sets up model for text generation
    tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
    model = GPT2LMHeadModel.from_pretrained('gpt2')
    #Gets elevation for map
    elevation = get_elevation(size)
    elevation = np.array(elevation)
    elevation = (elevation - elevation.min()) / (elevation.max() - elevation.min())

    landscape_pic = elevation_to_rgba(elevation)
    #Setup and use fitness function to spread cities realistically
    fitness = lambda self, cities, idx: game_fitness(
        cities, idx, elevation=elevation, size=size
    )

    fitness_function, ga_instance = setup_GA(fitness, n_cities, size)

    cities_t = ga_instance.initial_population[0]
    cities_t = solution_to_cities(cities_t, size)
    ga_instance.run()
    cities_t = ga_instance.best_solution()[0]
    cities = solution_to_cities(cities_t, size)
    cities = map(tuple,cities)
    cities = tuple(cities)
    

    screen = setup_window(width, height, "Game World Gen Practice")

    landscape_surface = pygame.surfarray.make_surface(landscape_pic) #get_landscape_surface(size)

    combat_surface = get_combat_surface(size)

    city_names = [
        "Morkomasto",
        "Morathrad",
        "Eregailin",
        "Corathrad",
        "Eregarta",
        "Numensari",
        "Rhunkadi",
        "Londathrad",
        "Baernlad",
        "Forthyr",
    ]

    #Setting city numbers to names for text generation
    city_dict = {}

    for city in range(n_cities):
        city_dict[city] = city_names[city]

    #cities = get_randomly_spread_cities(size, len(city_names))
    routes = get_routes(cities)

    random.shuffle(routes)
    routes = routes[:10]

    player_sprite = Sprite(sprite_path, cities[start_city])

    player = PyGameHumanPlayer()

    """ Add a line below that will reset the player variable to 
    a new object of PyGameAIPlayer class."""

    #player = PyGameAIPlayer()

    state = State(
        current_city=start_city,
        destination_city=start_city,
        travelling=False,
        encounter_event=False,
        cities=cities,
        routes=routes,
        inJournal=False
    )

    #Variables for money and journal
    money = 100
    journal = ["Journal: Use q (left) and w (right) to swap pages. Use x to exit. Journal added to every time a battle ends."]
    journalNum = 0
    text = " "

    print("Press j to open the journal.")

    while True:

        action = player.selectAction(state)

        if chr(action) != "q" and chr(action) != "w" and chr(action) != "x" and chr(action) != "j":
            if 0 <= int(chr(action)) <= 9 and not state.inJournal:
                if int(chr(action)) != state.current_city and not state.travelling:
                    #Make sure cities are connected before moving
                    if cityConnected(cities, routes,state.current_city,int(chr(action))):
                        startCity = cities[state.current_city]
                        state.destination_city = int(chr(action))
                        destination = cities[state.destination_city]
                        player_sprite.set_location(cities[state.current_city])
                        state.travelling = True
                        print(
                            "Travelling from", state.current_city, "to", state.destination_city
                        )
                        #Adding text for traveling for text generation
                        text = text + "I travelled from the city of " + city_dict[state.current_city] + " to " + city_dict[state.destination_city] + " on foot as an elf in a fantasy world."

                        route_coordinate = ((startCity[0],startCity[1]),(destination[0],destination[1]))

                        #lab3 travel_cost.py had the get_route_cost method altered to return a max and min elevation
                        #found on the bresenham path. This allows for the travel cost to be increased based on whether
                        #the player crossed over water or a mountain.
                        maxMinCost = get_route_cost(route_coordinate, elevation)

                        cost = 5
                        
                        #Printing, adding to text generation string, and increasing cost if we cross mountains or water.
                        if (maxMinCost[0] > 0.60):
                            print("Path crossed over a mountain.")
                            text = text + " During this journey, I crossed a mountain."
                            cost += 5
                        if (maxMinCost[1] < 0.35):
                            print("Path crossed over water.")
                            text = text + " During this journey, I crossed over a lake."
                            cost += 5

                        print("The travel cost was: " + str(cost))

                        money -= cost

                        print("Money: " + str(money))

                    else:
                        print("The cities are not connected with a route")

        screen.fill(black)
        screen.blit(landscape_surface, (0, 0))

        for city in cities:
            pygame.draw.circle(screen, (255, 0, 0), city, 5)

        for line in routes:
            pygame.draw.line(screen, (255, 0, 0), *line)

        displayCityNames(cities, city_names)

        #Display journal on
        if not state.travelling and chr(action) == "j" and not state.inJournal:
            state.inJournal = True
            print("Reading journal")
        #Actually draw journal
        if state.inJournal:
            white = (255, 255, 255)
            black = (0, 0, 0)
            font = pygame.font.Font('freesansbold.ttf', 10)

            drawJournal(white, black, font, screen, journal, journalNum)
        #Actions while inside of journal
        if state.inJournal:
            if chr(action) == "q":
                if(journalNum > (0)):
                    journalNum -= 1
            elif chr(action) == "w":
                if(journalNum < (len(journal) - 1)):
                    journalNum += 1
            elif chr(action) == "x":
                state.inJournal = False
                print("Exited journal")

        if state.travelling:
            state.travelling = player_sprite.move_sprite(destination, sprite_speed)
            state.encounter_event = random.randint(0, 1000) < 2
            if not state.travelling:
                print('Arrived at', state.destination_city)
                text = " "

        if not state.travelling:
            encounter_event = False
            alreadyFought = False
            state.current_city = state.destination_city
        #Changed it so you can only encounter 1 bandit per travel to simplify text generation process
        #If we get unlucky and get multiple encounters, it could fill up the journal page with our own text
        #instead of the generated text.
        if state.encounter_event:
            if (alreadyFought == False):
                loss = run_pygame_combat(combat_surface, screen, player_sprite)
                money -= loss
                print("Money: " + str(money))
                state.encounter_event = False

                if(loss == 0):
                    text = text + " On the way, I defeated a bandit."
                else:
                    text = text + " I lost " + str(loss) + " dollars to a bandit that attacked me."
                #Generate text for journal every time a fight ends
                nextEntry = generateText(text, model, tokenizer)

                print("The following journal entry was entered:\n")
                print(nextEntry)

                journal.append(nextEntry)
                text = " "
                alreadyFought = True
        else:
            if not state.inJournal:
                player_sprite.draw_sprite(screen)
        pygame.display.update()
        #Lose if you run out of money
        if money <= 0:
            print('You ran out of money! You lose!')
            break

        if state.current_city == end_city:
            print('You have reached the end of the game!')
            break
