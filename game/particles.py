# might not want to load sprites here
# from . import resources

class Particles:
    '''Base class for all particles'''
    # particles x, y
    # particles velocity x, y

    # particles container to be pre loaded
        # (-1, - 1 to be impossible for the screen to load?)
        # randomly generated inside of an area
    # particles container to moved/updated to be used
        # velocity added and randomly diviated for each particles

# might be moved into asteroid.py later
class Dust(Particles):
    '''Particles to be tied with asteroids'''
    # dust sprites
    # particles dencity
    # particles spawn's
    # particles velocity's
