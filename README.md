Hello!  5/11/2021

Currently in this version I have already laid out the foundations for a proper pygame game in general. Main loop, Keyboard control/functions, screen update, game functions, game preference, and game stats.

I've also created an Ant class that has an image template (assets/pointer_slim.png). The object currently have a pretty basic setup for an object moving on the screen. It's movement is defined by acceleration based on the game's timestep that changes it's velocity, has friction, rotates based on it's current vectors and velocity. It also has a basic WASD keyboard movement and a SPACE for breaks.

So far I've already made the game to be able to load in multiple instances of the Ant class and there's already 2 of them in this current version that moves in mirrored axis from one another.


What's up?  5/12/2021

Current'y I've updated some preference and object grouping and added a bit of random distribution to the objects inside this group. Right now the game starts with 90 ants that are rotated in a 360 degree formation.

I have updated the movement of the Ant class so that they will accelerate towards the direction they are facing rather than the direction that the user defines using the arrow keys. This will surely help in the automation and in randomizing the movements of each object. I've also added a property for the Ant class to completely disable their natural friction. This is good for just viewing the objects in motion as they create some pretty cool looking patterns on the screen.

So far I'm quite satisfied with the result but I still have some plans to improve and make this thing better and more ant like. 

What I will implement next is a random distribution of each object and I will try to simulate pheremone trails just like ants do in real life. I'll try working more on the code and try to make it even more efficient and robust as I can.