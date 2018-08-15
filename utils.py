# dependencies
import json, os, sys
import pygame as pg
# project and library pathes
PATH = {
    "go": os.path.dirname(__file__),
    "sysimg": os.path.dirname(__file__) + "\\images",
    "root": os.getcwd(),
    "assets" : os.getcwd() + "\\assets",
    "images" : os.getcwd() + "\\assets\\images",
    "maps": os.getcwd() + "\\assets\\maps",
    "tilesets": os.getcwd() + "\\assets\\tilesets",
    "identities": os.getcwd() + "\\assets\\identities"
}
IMG = {
    "noimage": pg.image.load(PATH["sysimg"] + "\\noimage.png"),
    "windowbg": pg.image.load(PATH["sysimg"] + "\\bg01.png"),
    "windowicon": pg.image.load(PATH["sysimg"] + "\\ente.png")
}
# console
def prettyPrint(data, sort=False, tabs=4):
    """Pretty print dict."""
    if data.__class__ is dict:
        print(json.dumps(data, sort_keys=sort, indent=tabs))
    else:
        print("Nothing to pretty-print.")
# class and object functions
def masterClass(object , masterclass):# bool
    """Check if object's master class matches the given one."""
    if object.__class__.__bases__[0] is masterclass:
        bool = True
    else:
        bool = False

    return bool
# files & directories
def isPath(path):# bool
    """Return True if the given path exists."""
    if os.path.isfile(path) or os.path.exists(path):
        bool = True
    else:
        bool = False

    return bool
def loadAssets(path):# list
    """Walk the assets-directory and open each json file. Plus appending
    file name and file path to the json file."""
    list = []

    for dirs in os.walk(path):
        for each in dirs[2]:
            if each.split(".")[1] == "json":
                config = loadJSON(dirs[0] + "\\" + each)
                list.append(config)
            # if directory has an image
            elif each.split(".")[1] == "png":
                config = {
                    "name": each.split(".")[0],
                    "filename": each,
                    "type": "image",
                    "filepath": dirs[0]
                }
                list.append(config)

    return list
def loadJSON(path):# dict
    """Load and convert a JSON file."""
    with open(path) as text:
        content = "".join(text.readlines())
        js = json.loads(content)
        js.update({"name": path.split("\\")[-2]})
        js.update({"filepath": path})

    return js
# dictionary operations
def validateDict(config={}, defaults={}):# dict
    """Validate a dictionary by given defaults. Params must be dict."""
    validated = {}

    for each in defaults:
        try:
            validated[each] = config[each]
        except KeyError:
            validated[each] = defaults[each]

    return validated
# pygame lib
def createBackground(background, rect, bgrepeat=""):# pygame.surface
    """Create a background surface depending on what type was given."""
    surface = pg.Surface(rect.size)
    # background's class type doesn't matter
    if type(background) is tuple:
        surface = pg.Surface(rect.size)
        surface.fill(background)
    elif type(background) is str:
        object = pg.image.load(background).convert()

    if masterClass(background, pg.Surface) or type(background) is pg.Surface:
        if bgrepeat == "x":
            surface = repeatX(background, rect)
        elif bgrepeat == "y":
            surface = repeatY(background, rect)
        elif bgrepeat == "xy":
            surface = repeatXY(background, rect)
        else:
            surface = background

    return surface
def createTiledMap(config, tiles):# dict
    """drawing tiles on a pygame surface and return it in a dict together with
    a list of wall rects."""
    tilesize = tiles[0].image.get_rect().size

    blocks = []
    surface = pg.Surface(
        (
            config["width"] * tilesize[0],
            config["height"] * tilesize[1]
        ),
        pg.SRCALPHA)

    i = 0
    for row in range(config["height"]):
        y = row * tilesize[1]
        for line in range(config["width"]):
            x = line * tilesize[0]
            # clean tile
            if config["data"][i] != 0:
                tile = tiles[config["data"][i] - 1]
                surface.blit(tile.image, (x, y))

            i += 1

    return {
        "image": surface,
        "blocks": blocks
        }
def getEvents():# pygame.events
    """Get pygame events."""
    return pg.event.get()
def getDisplay(size, **kwargs):# pygame.display.surface
    """Create a window display and return it. Customisation possible."""
    for key, value in kwargs.items():
        if key == "resizable":
            if value is True:
                display = pg.display.set_mode(size , pg.RESIZABLE)
            else:
                display = pg.display.set_mode(size)

    return display
def getPressedKeys():# pygame.event.keys
    """Get pygame.event's pressed-keys."""
    return pg.key.get_pressed()
def windowIcon(path):
    """Create an icon for the window from a png file."""
    if type(path) is pg.Surface:
        icon = path
    elif type(path) is str:
        icon = pg.image.load(path)

    icon = pg.transform.scale(icon , (32 , 32))
    pg.display.set_icon(icon)
def windowTitle(title):
    """Set the window's caption."""
    pg.display.set_caption(title)
def draw(object, destination, position=(0, 0)):# pygame.surface
    """Drawing a single or multiple objects to the destination surface. Then
    return it."""
    if type(position) is str:
        if position == "center":
            try:
                osize = object.get_rect().size
            except AttributeError:
                osize = object.image.get_rect().size
            dsize = destination.get_rect().size

            x = int(dsize[0] / 2) - int(osize[0] / 2)
            y = int(dsize[1] / 2) - int(osize[1] / 2)
            position = (x, y)
    elif type(position) is pg.Rect:
        position = position.topleft

    if type(object) is tuple:
        destination.fill(object, destination.get_rect())
    elif object.__class__.__bases__[0] is pg.Surface or type(object) is pg.Surface:
        destination.blit(object, position)
    elif object.__class__.__bases__[0] is pg.sprite.Sprite:
        destination.blit(object.image, position)
    elif object.__class__ is pg.sprite.Group:
        for sprite in object:
            destination.blit(sprite.image, sprite.rect.topleft)
    elif type(object) is list:
        for each in object:
            draw(each, destination, position)

    return destination
def drawBorder(rect, config):# pygame surface
    """Drawing a border to a surface and return it."""
    size, line, color = config
    surface = pg.Surface(rect.size, pg.SRCALPHA)

    pg.draw.lines(
        surface,
        color,
        False,
        [
            (0, 0),
            (0, rect.height - 1),
            (rect.width - 1, rect.height - 1),
            (rect.width - 1, 0),
            (0, 0)
        ],
        size
    )

    return surface
def perPixelAlpha(image, opacity=255):# pygame.surface
    """Convert per pixel alpha from image."""
    image.convert_alpha()
    alpha_img = pg.Surface(image.get_rect().size , pg.SRCALPHA)
    alpha_img.fill((255 , 255 , 255 , opacity))
    image.blit(alpha_img , (0 , 0) , special_flags = pg.BLEND_RGBA_MULT)

    return image
def getFrames(image, framesize):# list
    """return a list of frames clipped from an image."""
    frames = []

    rows = int(image.get_rect().height / framesize[1])
    cells = int(image.get_rect().width / framesize[0])
    rect = pg.Rect((0, 0), framesize)

    # running each frame
    for row in range(rows):
        y = row * framesize[1]
        rect.top = y
        for cell in range(cells):
            x = cell * framesize[0]
            rect.left = x

            image.set_clip(rect)
            clip = image.subsurface(image.get_clip())

            frames.append(clip)
    del(clip, rect)

    return frames
def scale(surface, factor):# pygame.surface
    """Scaling the surface by an int-factor."""
    width = int(surface.get_rect().width * factor)
    height = int(surface.get_rect().height * factor)

    scaled = pg.transform.scale(surface, (width, height))

    return scaled
def repeatX(image, parent, pos=(0, 0)):# pygame.surface
    """Return a surface with x-line repeated image blitting."""
    child = image.get_rect()
    surface = pg.Surface(parent.size, pg.SRCALPHA)

    for each in range(int(parent.width / child.width) + 1):
        surface.blit(image, (each * child.width, pos[0]))

    return surface
def repeatY(image, parent, pos=(0, 0)):# pygame.surface
    """Return a surface with y-line repeated image blitting."""
    child = image.get_rect()
    surface = pg.Surface(parent.size, pg.SRCALPHA)

    for each in range(int(parent.height / child.height) + 1):
        surface.blit(image, (pos[1], each * child.height))

    return surface
def repeatXY(image, parent, bg_position=(0, 0)):# pygame.surface
    """Return a surface with x and y-line repeated image blitting."""
    child = image.get_rect()
    surface = pg.Surface(parent.size, pg.SRCALPHA)

    for j in range(int(parent.width / child.width) + 1):
        for i in range(int(parent.height / child.height) + 1):
            surface.blit(image, (j * child.width, i * child.width))

    return surface