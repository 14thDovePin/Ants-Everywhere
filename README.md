Hello!

Currently in this version I have already laid out the foundations for a proper pygame game in general. Main loop, Keyboard control/functions, screen update, game functions, game preference, and game stats.

I've also created an Ant class that has an image template (assets/pointer_slim.png). The object currently have a pretty basic setup for an object moving on the screen. It's movement is defined by acceleration based on the game's timestep that changes it's velocity, has friction, rotates based on it's current vectors and velocity. It also has a basic WASD keyboard movement and a SPACE for breaks.

So far I've already made the game to be able to load in multiple instances of the Ant class and there's already 2 of them in this current version that moves in mirrored axis from one another.

