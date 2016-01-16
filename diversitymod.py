import shutil, os, ConfigParser
import xml.etree.ElementTree as ET
import time
import psutil
from string import ascii_uppercase, digits
from Tkinter import *
from tkFileDialog import askopenfilename
from random import seed, randint, choice, shuffle
from PIL import Image, ImageFont, ImageDraw, ImageTk
from binascii import crc32
from subprocess import call


##
##Constants
##
items_xml = ET.parse('resources/items.xml')

items_info = items_xml.getroot()



##
## Get Steam path ( lines from http://code.activestate.com/recipes/578689-get-a-value-un-windows-registry/ )
##

import _winreg

def regkey_value(path, name="", start_key = None):
    if isinstance(path, str):
        path = path.split("\\")
    if start_key is None:
        start_key = getattr(_winreg, path[0])
        return regkey_value(path[1:], name, start_key)
    else:
        subkey = path.pop(0)
    with _winreg.OpenKey(start_key, subkey) as handle:
        assert handle
        if path:
            return regkey_value(path, name, handle)
        else:
            desc, i = None, 0
            while not desc or desc[0] != name:
                desc = _winreg.EnumValue(handle, i)
                i += 1
            return desc[1]

SteamPath = regkey_value(r"HKEY_CURRENT_USER\Software\Valve\Steam", "SteamPath")

##
## end of copied stuff
##

def delItemPool(id):
    id = str(id)
    if id.isdigit():
        for xmlPool in item_pools_info:
            for item in xmlPool:
                if item.attrib['Id'] == id:
                    xmlPool.remove(item)



def selectall(event = None):
    sentry.select_range(0, 'end')
    return 'break'

def newRandomSeed():
    global seedIsRNG
    seed()
    seedIsRNG = ''.join(choice(ascii_uppercase + digits) for _ in range(6))
    entryseed.set(seedIsRNG)
    
def installDiversityMod():
    
    item_pools_xml = ET.parse('resources/itempools.xml')
    players_xml = ET.parse('resources/players.xml')
    item_pools_info = item_pools_xml.getroot()
    players_info = players_xml.getroot()
    
    # trim the whitespace on the string if there is any
    s = entryseed.get()
    entryseed.set(s.strip().encode('ascii','replace'))
    # if no seed entered, generate one
    if entryseed.get() == '':
        newRandomSeed()
    # set the RNG seed
    global dmseed
    dmseed = entryseed.get()
    seed(crc32(dmseed))
    
    # set background to indicate that current entry is active
    sentry.configure(bg = '#d8fbf8')
    
    # valid_items is the list of all passive items in the game EXCLUDING the 22 on the no-list
    valid_items = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 17, 18, 19, 20, 21, 27, 28, 32, 46, 48, 50, 51, 52, 53, 54, 55, 57, 60, 62, 63, 64, 67, 68, 69, 
    70, 71, 72, 73, 74, 75, 76, 79, 80, 81, 82, 87, 88, 89, 90, 91, 94, 95, 96, 98, 99, 100, 101, 103, 104, 106, 108, 109, 110, 112, 113, 114, 115, 116, 117, 118, 
    120, 121, 122, 125, 128, 129, 131, 132, 134, 138, 139, 140, 141, 142, 143, 144, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 159, 161, 162, 163, 165, 167, 
    168, 169, 170, 172, 173, 174, 178, 179, 180, 182, 183, 184, 185, 187, 188, 189, 190, 191, 193, 195, 196, 197, 198, 199, 200, 201, 202, 203, 204, 205, 206, 207, 
    208, 209, 210, 211, 212, 213, 214, 215, 216, 217, 218, 219, 220, 221, 222, 223, 224, 225, 227, 228, 229, 230, 231, 232, 233, 234, 236, 237, 240, 241, 242, 243, 
    244, 245, 246, 247, 248, 249, 250, 251, 252, 254, 255, 256, 257, 259, 260, 261, 262, 264, 265, 266, 267, 268, 269, 270, 271, 272, 273, 274, 275, 276, 277, 278, 
    279, 280, 281, 299, 300, 301, 302, 303, 304, 305, 306, 307, 308, 309, 310, 311, 312, 313, 314, 315, 316, 317, 318, 319, 320, 321, 322, 327, 328, 329, 330, 331, 
    332, 333, 335, 336, 337, 340, 341, 342, 343, 345, 350, 353, 354, 356, 358, 359, 360, 361, 362, 363, 364, 365, 366, 367, 368, 369, 370, 371, 372, 373, 374, 375, 
    376, 377, 378, 379, 380, 381, 384, 385, 387, 388, 389, 390, 391, 392, 393, 394, 395, 397, 398, 399, 400, 401, 402, 403, 404, 405, 407, 408, 409, 410, 411, 412, 
    413, 414, 415, 416, 417, 418, 420, 423, 424, 425, 426, 429, 430, 431, 432, 433, 435, 436, 438, 440]
    
    # random permutation of valid items list
    itemIDs = list(valid_items)
    shuffle(itemIDs)
    
    spaceitem = ['105,','45,', '', '34,', '36,', '', '', '', '', '', '284,', '357,', '349,']
    if d6start.get():
        spaceitem = ['105,','105,', '105,', '105,', '105,', '105,', '105,', '105,', '105,', '', '105,', '105,', '105,']
        
    
    


    # clear out the files
    # remove all the files and folders EXCEPT packed and dmtmpfolder
    for resourcefile in os.listdir(resourcepath):
        if resourcefile != 'packed' and resourcefile != dmtmpfolder and resourcefile != 'config.ini' :
            if os.path.isfile(os.path.join(resourcepath, resourcefile)):
                os.unlink(os.path.join(resourcepath, resourcefile))
            elif os.path.isdir(os.path.join(resourcepath, resourcefile)):
                shutil.rmtree(os.path.join(resourcepath, resourcefile))
    
    # write players file
    if os.path.isfile(resourcepath + '/players.xml'):
        os.remove(resourcepath + '/players.xml')

    shutil.copy(currentpath + '/resources/players.xml', resourcepath + '/players.xml')
    counter = 0
    for player in players_info:
        if player.attrib['name'] == 'Black Judas' or player.attrib['name'] == 'Lazarus II':
            pass
        elif player.attrib['name'] == 'Keeper' or player.attrib['name'] == 'Eden':
            defaultItems = str(player.get('items'))
            player.set('items', str(itemIDs[0]) + ', ' + str(itemIDs[1]) + ', ' + str(itemIDs[2]))
            counter += 1
        
        else:
            defaultItems = str(player.get('items'))
            player.set('items', defaultItems + ', ' + spaceitem[counter] + str(itemIDs[0]) + ', ' + str(itemIDs[1]) + ', ' + str(itemIDs[2]))
            counter += 1
    
    players_xml.write(resourcepath + '/players.xml')
    
    file = open("diversity_seed.txt", "w")
    file.write(dmseed)
    
            
    # make the graphics and install them
    # create gfx folder structure
    os.makedirs(resourcepath + '/gfx/ui/main menu/')
    # open menu graphics & write the seed on them
    characterimg = Image.open(currentpath + "/resources/charactermenu.png")
    titleimg = Image.open(currentpath + "/resources/titlemenu.png")
    splashimg = Image.open(currentpath + "/resources/splashes.png")
    characterdraw = ImageDraw.Draw(characterimg)
    titledraw = ImageDraw.Draw(titleimg)
    smallfont = ImageFont.truetype(os.getcwd() + "/fonts/comicbd.ttf", 10)
    largefont = ImageFont.truetype(os.getcwd() + "/fonts/comicbd.ttf", 16)
    w, h = characterdraw.textsize("Diversity Mod v" + str(version) + " Seed", font = smallfont)
    w2, h2 = characterdraw.textsize(str(entryseed.get()), font = largefont)
    w3, h3 = characterdraw.textsize("(random)", font = smallfont)
    characterdraw.text((240-w/2, 21), "Diversity Mod v" + str(version) + " Seed", (54, 47, 45), font = smallfont)
    characterdraw.text((240-w2/2, 31), str(entryseed.get()), (54, 47, 45), font = largefont)
    try:
        if entryseed.get() == seedIsRNG:
            characterdraw.text((240-w3/2, 49), "(random)", (54, 47, 45), font = smallfont)
    except NameError:
        print 'error?'
    titledraw.text((435,240), "v" + str(version), (54, 47, 45), font = largefont)
    characterimg.save(resourcepath + '/gfx/ui/main menu/charactermenu.png')
    titleimg.save(resourcepath + '/gfx/ui/main menu/titlemenu.png')
    splashimg.save(resourcepath + '/gfx/ui/main menu/splashes.png')
    
    #Copy itempools.xml to resources and remove, soy/libra from pools when present in the start, and blood rights from pools when Isaac's heart is present
    shutil.copyfile(currentpath + '/resources/itempools.xml', resourcepath + '/itempools.xml')
    for x in range(0,3):
        if(itemIDs[x] == 330 or itemIDs[x] == 304):
            delItemPool(330)
            delItemPool(304)
        if(itemIDs[x] == 276):
            delItemPool(186)
    
    item_pools_xml.write(resourcepath + '/itempools.xml')
    # clear out the files
    shutil.copyfile(currentpath + '/resources/items.xml', resourcepath + '/items.xml')
    
    os.makedirs(resourcepath + '/rooms/')
    shutil.copyfile(currentpath + '/resources/rooms/00.special rooms.stb', resourcepath + '/rooms/00.special rooms.stb')
    shutil.copyfile(currentpath + '/resources/rooms/04.catacombs.stb', resourcepath + '/rooms/04.catacombs.stb')
    shutil.copyfile(currentpath + '/resources/rooms/05.depths.stb', resourcepath + '/rooms/05.depths.stb')
    shutil.copyfile(currentpath + '/resources/rooms/06.necropolis.stb', resourcepath + '/rooms/06.necropolis.stb')
    shutil.copyfile(currentpath + '/resources/rooms/07.womb.stb', resourcepath + '/rooms/07.womb.stb')
    shutil.copyfile(currentpath + '/resources/rooms/08.utero.stb', resourcepath + '/rooms/08.utero.stb')
    shutil.copyfile(currentpath + '/resources/rooms/09.sheol.stb', resourcepath + '/rooms/09.sheol.stb')
    shutil.copyfile(currentpath + '/resources/rooms/12.chest.stb', resourcepath + '/rooms/12.chest.stb')

    # update gui stuffs
    dm.update_idletasks()
    
    # if Rebirth is running, kill it (returns an ugly error if Rebirth is not running, but just ignore it I guess)
#    try:
    #    print("Attempting to kill Isaac ...\n")
    for p in psutil.process_iter():
        if p.name() == 'isaac-ng.exe':
            call(['taskkill', '/im', 'isaac-ng.exe', '/f'])
#    except OSError:
    #    print("There was an error closing Rebirth.")

    # re/start Rebirth
#    try:
    if os.path.exists(resourcepath+"/../../../../steam.exe"):
#            print("Found steam ...")
        call([resourcepath + '/../../../../steam.exe', '-applaunch', '250900'])
    elif os.path.exists(resourcepath + "/../isaac-ng.exe"):
#            print("No Steam, but found isaac-ng.exe ...")
        call(resourcepath + '/../isaac-ng.exe')
#    except OSError:
#        print("Starting Rebirth failed.\nPress Enter to close.")
    
def closeDiversityMod():
    # remove all the files and folders EXCEPT packed and dmtmpfolder
    for resourcefile in os.listdir(resourcepath):
        if resourcefile != 'packed' and resourcefile != dmtmpfolder :
            if os.path.isfile(os.path.join(resourcepath, resourcefile)):
                os.unlink(os.path.join(resourcepath, resourcefile))
            elif os.path.isdir(os.path.join(resourcepath, resourcefile)):
                shutil.rmtree(os.path.join(resourcepath, resourcefile))
                
    # copy all the files and folders EXCEPT the 'packed' folder to dmtmpfolder
    for dmtmpfile in os.listdir(os.path.join(resourcepath, dmtmpfolder)):
        if os.path.isfile(os.path.join(resourcepath, dmtmpfolder, dmtmpfile)):
            shutil.copyfile(os.path.join(resourcepath, dmtmpfolder, dmtmpfile), os.path.join(resourcepath, dmtmpfile))
        elif os.path.isdir(os.path.join(resourcepath, dmtmpfolder, dmtmpfile)):
            shutil.copytree(os.path.join(resourcepath, dmtmpfolder, dmtmpfile), os.path.join(resourcepath, dmtmpfile))
    # remove the temporary directory we created
    shutil.rmtree(os.path.join(resourcepath, dmtmpfolder))
    sys.exit()
    
def setcustompath():
    # open file dialog
    isaacpath = askopenfilename()
    # check that the file is isaac-ng.exe and the path is good
    if isaacpath [-12:] == "isaac-ng.exe" and os.path.exists(isaacpath[0:-12] + 'resources'):
        if not customs.has_section('options'):
            customs.add_section('options')
        customs.set('options', 'custompath', isaacpath [0:-12] + 'resources')
        with open('options.ini', 'wb') as configfile:
            customs.write(configfile)
        feedback.set("Your Diversity Mod path has been correctly set.\nClose this window and restart Diversity Mod.")
    else:
        feedback.set("That file appears to be incorrect. Please try again to find isaac-ng.exe")
    dm.update_idletasks()

def checkInstalled(*args):
    if 'dmseed' in globals():
        # set background to indicate that current entry is active
        if entryseed.get() == dmseed:
            sentry.configure(bg = '#d8fbf8')
        else:
            sentry.configure(bg = '#f4e6e6')


version = 1.00
    
# dm is the gui, entryseed is the rng seed, feedback is the message for user
dm = Tk()
entryseed = StringVar()
entryseed.trace("w", checkInstalled)
feedback = StringVar()
d6start = BooleanVar()
# just the gui icon and title
dm.iconbitmap("images/poop.ico")
dm.title("Diversity Mod v" + str(version))

# import options
customs = ConfigParser.RawConfigParser()
customs.read('options.ini')

# check and set the paths for file creation, exit if not found
currentpath = os.getcwd()
# first check custom path
if customs.has_option('options', 'custompath') and os.path.exists(customs.get('options', 'custompath')):
    resourcepath=customs.get('options', 'custompath')
# then check steam path
elif os.path.isdir(SteamPath + "/steamapps/common/The Binding of Isaac Rebirth/resources"):
    resourcepath = SteamPath + "/steamapps/common/The Binding of Isaac Rebirth/resources"
else: # if neither, then go through the motions of writing and saving a new path to options
    feedback.set("")
    Message(dm, justify = CENTER, font = "font 10", text = "Diversity Mod was unable to find your resources directory.\nNavigate to the program isaac-ng.exe in your Steam directories.", width = 600).grid(row = 0, pady = 10)
    Message(dm, justify = CENTER, font = "font 12", textvariable = feedback, width = 600).grid(row = 1)
    Button(dm, font = "font 12", text = "Navigate to isaac-ng.exe", command = setcustompath).grid(row = 2, pady = 10)
    Message(dm, justify = LEFT, font = "font 10", text = "Example:\nC:\Program Files (x86)\Steam\steamapps\common\The Binding of Isaac Rebirth\isaac-ng.exe", width = 800).grid(row = 3, padx = 15, pady = 10)
    mainloop()
    
# check if you're inside the resources path. give warning and close if necessary.
if os.path.normpath(resourcepath).lower() in os.path.normpath(currentpath).lower():
    Message(dm, justify = CENTER, font = "font 12", text = "Diversity Mod is in your resources directory.\nMove it elsewhere before running.", width = 600).grid(row = 0, pady = 10)
    mainloop()
    sys.exit()
    
# create a menubar
menubar = Menu(dm)
dropmenu = Menu(menubar, tearoff = 0)
dropmenu.add_checkbutton(label = "All characters start with D6", variable = d6start)
menubar.add_cascade(label = "Options", menu = dropmenu)
d6start.set(True)

# display the menu
dm.config(menu = menubar)

# create a folder to temporarily hold files until Diversity Mod is done
seed()
dmtmpfolder = '../resources_tmp' + str(randint(1000000000,9999999999))
if not os.path.exists(os.path.join(resourcepath, dmtmpfolder)):
    os.mkdir(os.path.join(resourcepath, dmtmpfolder))

# copy all the files and folders EXCEPT the 'packed' folder to dmtmpfolder
for resourcefile in os.listdir(resourcepath):
    if resourcefile != 'packed' and resourcefile != dmtmpfolder:
        try:
            if os.path.isfile(os.path.join(resourcepath, resourcefile)):
                shutil.copyfile(os.path.join(resourcepath, resourcefile), os.path.join(resourcepath, dmtmpfolder, resourcefile))
            elif os.path.isdir(os.path.join(resourcepath, resourcefile)):
                shutil.copytree(os.path.join(resourcepath, resourcefile), os.path.join(resourcepath, dmtmpfolder, resourcefile))
        except Exception, e:
            print e


# central gui box
dmbox = LabelFrame(dm, text = "", padx = 5, pady = 5)
dmbox.grid(row = 1, column = 0, columnspan = 2, pady = 20)
# text entry for seed
Label(dmbox, text = "Enter seed (case sensitive)", font = "font 14").grid(row = 0, column = 0, pady = 10)
sentry = Entry(dmbox, justify = CENTER, font = "font 32 bold", width = 15, textvariable = entryseed)
sentry.configure(bg = '#f4e6e6')
sentry.bind("<Return>", (lambda event: installDiversityMod()))
sentry.bind("<Control-a>", selectall)
#sentry.selectall(self, "<Control-a>")
sentry.grid(row = 1, padx = 7, columnspan = 2, pady = 5)
# button to choose a new random seed
dmrandimage = Image.open("images/d100.png")
dmrandicon = ImageTk.PhotoImage(dmrandimage)
Button(dmbox, image = dmrandicon, font = "font 12", command = newRandomSeed).grid(row = 0, column = 1, padx = 7, sticky = E)

# button to install mod and restart Rebirth
dmiconimage = Image.open("images/rainbow.png")
dmicon = ImageTk.PhotoImage(dmiconimage)
Button(dm, image = dmicon, text = '   Start Diversity Mod   ', compound = "left", command = installDiversityMod, font = "font 16").grid(row = 3, pady = 7, columnspan = 2)

# simple instruction display for user
Message(dm, justify = CENTER, text = "\nRebirth will open when you click Start.", font = "font 13", width = 475).grid(row = 4, column = 0, columnspan = 2, padx = 20)
Message(dm, justify = CENTER, text = "Start again and again with new seeds for more Diversity.", font = "font 13", width = 475).grid(row = 5, column = 0, columnspan = 2, padx = 20)
Message(dm, justify = CENTER, text = "Keep this program open while playing.", font = "font 13", width = 475).grid(row = 6, column = 0, columnspan = 2, padx = 20)
Message(dm, justify = CENTER, text = "Rebirth returns to normal when this program is closed.\n\n", font = "font 13", width = 500).grid(row = 7, column = 0, columnspan = 2, padx = 20)

# uninstall mod files when the window is closed
dm.protocol("WM_DELETE_WINDOW", closeDiversityMod)

mainloop( )
