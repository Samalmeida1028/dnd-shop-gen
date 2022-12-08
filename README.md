# dnd-shop-gen

### Currently, this is a project to generate simple shops with an inventory saved to a JSON object file

Most of the functionality is in **main.py**

When running it, the user is presented with a simple terminal.
Arguments are currently delimited by a comma in the terminal to allow for names that include spaces.
Type "help" to get a list of the currently supported commands.

Currently the item list has about 90 items with types, the base value is in CP (copper pieces), and is based off of my campaign. Those values can be easily changed in the JSON, I'll add an update item price function later
## Functions

The terminal right now allows users to create specific shops, generate random shops in a region, add new shop regions, add items
to shop regions, and enter shops and buy and sell specific items

**Because everything is saved in JSON format, you can go into the text file and edit the parameters, and as long as the format
is maintained, it will change in the program when you restart it**

_this also means you can use all save data as JSON objects_

**If you need to add items, then under "Scripts" there is an item adder script that can be used currently**

### Update:
added the ability to add items through the terminal!

## TODO (in terminal app)
- Remove shops, remove items from shops, remove regions, and remove items from regions
- Rename Shops
- add update shops to randomly update and change shops
- add update item price
- add update item rarity
- add update item region
- (more item stuff)

## TODO (General)

- Add better comments
- Add more documentation :D
