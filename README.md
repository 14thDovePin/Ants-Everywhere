## Ants Everywhere!

This is my very first full project in my repository! This project is heavily inspired from [**_Sebastian Lague's_**](https://www.youtube.com/channel/UCmtyQOKKmrMVaKuRXz02jbQ) [*Ant and Slime simulation*](https://www.youtube.com/watch?v=X-iSQQgOd1A). This simulation is made to mimic the movement of ants. The game is small and simple. Ants move around the window and where ever the mouse points at, the ants will try to evade it as they travel around.

### Keyboard Controls
###### Ant Manual Mode.
* Uparrow - *Accelerate forwards.*
* Downarrow - *Accelerate backwards.*
* Leftarrow - *Rotate left.*
* Rightarrow - *Rotate right.*
* Space - *Brakes.*

###### Others
* Q - *Exit game.*

Made in Python 3.9.1  
Pygame v2.0.1
## Extras

The ants in the game are pointer objects which has various properties and attributes. It has 2 main modes: Manual and Automatic. These 2 modes are movement modes that I've implemented in order to test and recreate the ant's movements respectively. To switch between the 2 modes I've implemented an internal switch that can be set to 1 or 0 depending on your preference. And there's is also another switch to toggle natural Friction brakes on or off.

As the ants move around the screen randomly, they will try to evade the cursor's last known or current position in a 100px radius. The ants itself has it's forward acceleration constant, with a randomized turning and rotating speed and a randomize time interval between each actions. The game itself has a separate file that contains the game preference and it's statistics divided into it's own classes.

The game was made purely in Python. The module used to make it is called pygame, it's the backbone of the project. The program was coded in (OOP) style for easier implementation and modification of the project. I've made this project to help me with my logic working skills and help me improve my abilities. This project taught me a lot more about breaking down big problems into smaller and easier tasks for me to work with. It also taught me that you can solve one problem in many ways, but you only need the way that works best for your project.
