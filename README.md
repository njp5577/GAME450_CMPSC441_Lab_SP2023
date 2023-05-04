Noah Pfeffer

May 3, 2023

Project Report

CMPSC441: AI and Advanced Game Programming



### **Section 1: Abstract**

​	The following project is a series of improvements for a pre-existing game built with Pygame. At its core, the game incorporated map movement through routes to cities, turn-based combat with bandits using a more complex rock-paper-scissor style of gameplay, and a fantasy world aesthetic with an elf as the playable character. The goal of the game is to reach a certain city on the map. In terms of the improvements, a genetic algorithm was first implemented to spread cities out realistically on the game map based on distance and elevation. Then, a function was added to determine whether there was a route from the current city the player was at to the destination city, and that allowed for the restriction of movement based on the generated routes. Next, a money system was added; this includes cost of travel based on the elevation of the terrain and losing money if the player loses to a bandit in combat. If the player loses all of their money through one of the previously mentioned means, then they lose the game. Finally, an additional AI technique was added to game as a standalone task from the other general improvements. In this case, text generation with GPT-2 was used to create a journaling mechanism within the game that the player can view and add to. In summation, the improvements to the game done through the project add more depth to the gameplay and utilize AI techniques to perform complex tasks in an easily implementable fashion.

### **Section 2: List of AI Components**

- Genetic Algorithm
- Perlin Noise
- Text Generation with GPT-2

### **Section 3: Problems Solved**

**a. Genetic Algorithm**

​	Genetic algorithms are a algorithms that can solve complex problems by simulating natural selection. For the project, this comes in handy for randomly dispersing the cities in a way that makes sense given the differing elevations in the landscape. In most cases, the player of the game would expect to see cities that are spaced out on the game map and are not located in unrealistic spots such as in lakes or on top of mountains. Other complex algorithms could be made to simulate this randomness, but genetic algorithms are a simple way to perform this task given the large amount of possible outcomes. Genetic algorithms function by having multiple generations simulate outcomes and using a fitness function to find which individuals' results were the most desirable. Then, the offspring of those desirable individuals receive genes in a way that attempts to replicate functions such as mutation and crossover seen in real-world biology. In the game, desirable traits outlined in the fitness function include a city not being within a certain radius of other cities and a city not being in water or on a mountain. The size of the map, elevations, and number of cities would need to be provided as input to optimize the generations. As the generations progress, the city layout will become more desirable as the fitness of the offspring is optimized through the simulated natural selection. As a result, the game will be left with a best solution as the output that is the culmination of all the generations of city layouts that came before it. Overall, genetic algorithms are useful for dealing with problems that have a large amount of solutions, and the game utilizes it to create random game maps that are pleasing to the player.

**b. Perlin Noise**

​	Perlin Noise is a type of procedural content generation that is commonly used to generate a random looking terrain (in any dimension) that also has a seemingly "natural" smoothness to it. The smoothness is created by utilizing permutations of pseudorandom numbers that are related to nearby pseudorandom numbers. The noise added through the Perlin Noise technique utilizes frequency and amplitude to adjust the results. In the case of the project, octaves are being changed to adjust frequency along with a seed that picks the desired randomness. Preferably for the game map, the player would expect to see a two-dimensional land map with realistic terrain features like mountains, lakes, and so on; however, creating a map like this from scratch takes time and also likely requires some expertise with art development software. Perlin Noise allows for the simple and fast creation of this two-dimensional terrain while also making it appear to be realistic. Since the image is in two dimensions, the noise being added is influencing the colors of the map with random elevation numbers to create brownish white mountains, blue lakes, and green grasslands. To accomplish this, the algorithm also needs to have the size of the map and needs an accompanying plotting function to add the colors to the map. The colors seem to organically transition into each other, which makes for a pleasant-to-view game map that cities can be overlaid onto. After the image is generated with the random elevations, it can be put straight into the game, and the information regarding the elevations on the map can be separately used for other purposes such as travel cost and text generation.

**c. Text Generation with GPT-2**

​	Text generation models are models that are trained on pre-existing text to allow for them to create, edit, or add onto texts. In terms of the game, it did not have to many components that relayed a story, so text generation can be used to fill in the story based on events that happened during gameplay. In the project, GPT-2 was used for text generation. GPT-2 is a transformer-based model that is pretrained on openly available textual data. A transformer model is particularly effective at weighting how meaningful components are in relation to each other and falls under the category of neural networks. In this case, GPT-2 is specifically effective at adding onto text that is given to it. Once implemented, a GPT-2 text generation model was used to create the journal entries within the game based on how the player traversed to the next city (if they encountered any water or mountains) and how their combat with a bandit ended. This text input was created by combining different strings based on events that led up to a given combat encounter. Afterward, the text being generated would come in the form of a tokenized output. The tokenized output is composed of numerical data that relates to the word and sentence pieces of the output. By using these tokens, the model can more easily understand the statistical linguistic relationship between words and sentences making it more effective at creating a viable output in the form of text that is readable and related to the input. After decoding this tokenized output, the game is left with the generated text. In the end, journal entries are created for the player to view and derive story details from as they play through the game.

### **Section 4: AI Component Implementation** Details

**a. Genetic Algorithm**

​	A fitness function was implemented alongside the setup for the algorithm to determine fitness among individuals based on whether they were far enough away from each other and if they were on water or a mountains. Next, the algorithm was added into the game by using it to generate the list of city locations based on the elevation, size of the map, and number of cities. On game startup, the algorithm will run and will determine a solution for city placement. Finally, these city locations are used to draw the dots onto the game map to represent cities that the player can travel to.

**b. Perlin Noise**

​	Perlin noise is used to determine the elevations on the game map and was implemented by running the modular function with map size as the input. The elevations were then used to generate a colored map, which was displayed to the screen. For this project in particular, the elevations were then later used to determine travel cost and to add to the text generation string based on difficult terrain encounter by the player. Since the desired outcome for travel cost was to determine it based on elevation, the maximum and minimum values for elevation were retrieved from the Bresenham path and compared to the values for water and mountains to find whether the player was traversing passed them or not.

**c. Text Generation**

​	To implement text generation, GPT-2 was utilized due to its ability to add onto the existing input. To create this input, a string is compiled using the city the player is traveling from, the city the player is traveling to, whether the player crossed difficult terrain, and whether the player defeated the bandit or not. Extra details such as the fantasy setting and money lost were added to further guide the output. The output also needed to be filtered for incomplete sentences before being added to the journal.

### **Section 5: Appendix**

Section 1: Abstract

Section 2: List of AI Components

Section 3: Problems Solved

​	3a. Genetic Algorithms

​	3b. Perlin Noise

​	3c. Text Generation with GPT-2

Section 4: AI Component Implementation Details

​	4a. Genetic Algorithms

​	4b. Perlin Noise

​	4c. Text Generation with GPT-2

Section 5: Appendix

**Note:** ChatGPT was not used in the completion of this assignment

