Diversity Mod for The Binding of Isaac: Afterbirth
-----------------------------------------------
version 1.00

Created by DuneAught (twitter: @duneaught)
with much help from awerush, Hyphenated, Inschato, pears, Zamiel & #isaac on SpeedRunsLive
Updated to Afterbirth compatibility by InvaderTim

To play The Binding of Isaac: Afterbirth with Diversity Mod, just run diversitymod.exe. You do not have to move any files or uninstall other mods.
**Ctrl-a now works in the seed selection.**

Download here: https://github.com/TimStavrakos/diversitymod/releases


Description
-----------

All characters, start with the D6 except Eden, who gets a random space-use item as usual, Keepr who gets Wooden Penny, and Eve, who gets Razor Blade.

All characters start with **the same, as of v0.14,** 3 additional random passive items, keeping their original items and resources.

Mom's Knife & Epic Fetus are removed from their respective item pools. They may be assigned as random starting items, but they will not appear in game during a playthrough.

The Special Item status is removed from the game.

Room modifications are taken directly from Balls of Steel Weekly mod 1.2:

* All Donation Machines have been removed.
* Angel Rooms that offer only soul hearts or eternal hearts have been removed, so Angel Rooms are guaranteed to have one pedestal and an Angel statue.
* Mimics and Doppelgangers spawn off center so the player is not hit upon entering the room.
* Some enemies that spawn close to doors are moved toward the center of the room to prevent unavoidable damage.


The Diversity Mod Program
-------------------------

The Diversity Mod program generates and installs mod files when you click "Start Diversity Mod". Then it restarts The Binding of Isaac: Afterbirth game.

Characters are assigned random starting items based on a user provided seed. If no seed is provided, a random seed will be generated.

When the Diversity Mod program is opened, other installed Afterbirth mods are moved to a temporary folder next to the Rebirth resources folder.

The Diversity Mod program must remain open for the mod to work, because it restores previously installed mods when closed.

If Rebirth is not in the default Steam location, the Diversity Mod program will prompt the user for the path to the Rebirth game files.

The Diversity Mod program will not work if it is inside the Rebirth resources folder.


Known Issues
------------

* The program is not currently compatible with Linux/Mac.
* When the program closes unexpectedly, it leaves mod files installed. To fix, see: http://pastebin.com/mfreKXXT

Setup
-----
Use pyinstaller: https://github.com/pyinstaller/pyinstaller/releases

Put pyinstaller.exe and pyinstaller.py in diversity mod directory.

Open directory in console.

In console, type: "pyinstaller.exe --onefile --windowed diversitymod.py"

Run seup.py.


Random Passive Starting Items
-----------------------------

If any character gets Isaac's Heart as a random starting item, Blood Rights is removed from the Treasure Room pool.

If any character gets Soymilk as a random starting item, Libra is removed from the Treasure Room pool.

Some passive items are EXCLUDED from the random starting items. Characters cannot start with two of the same item. Blue Baby, Azazel, and The Lost have additional exclusions.

### Exclusions for All Characters

* 15 - <3
* 16 - Raw Liver
* 22 - Lunch
* 23 - Dinner
* 24 - Dessert
* 25 - Breakfast
* 26 - Rotten Meat
* 29 - Moms Underwear
* 30 - Moms Heels
* 31 - Moms Lipstick
* 92 - Super Bandage
* 119 - Blood Bag
* 176 - Stem Cells
* 194 - Magic 8 Ball
* 226 - Black Lotus
* 238 - Key Piece #1
* 239 - Key Piece #2
* 253 - Magic Scab
* 258 - Missing No.
* 334 - The Body
* 339 - Safety Pin
* 344 - Match Book
* 346 - A Snack
* 355 - Mom's Pearls
* 428 - PJs


Version History
---------------

For full version history, see: https://github.com/TimStavrakos/diversitymod/releases
