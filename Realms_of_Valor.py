# Import necessary modules
import sys, os, pickle

clear = lambda: os.system('cls')

# Define global variables
current_room = "south" 

# Define dictionary of rooms
rooms = {
    "south": {
        "description": "You are in a dark room. There is a door to the north and a door to the east.",
        "information": "You almost can't see much in this room. On your right is a desk\nbut overall, you can't tell how the room looks like.",
        "exits": ["north", "east"],
        "items": [],
        "objects": [{"name": "desk", "used": False}],
        "hint": "Look around the room for clues.",
        "requirement": [],
        "requirement_message": ""
    },
    "north": {
        "description": "You are in a bright room. There is a door to the south and a door to the west.",
        "information": "You can clearly see everything in here.\nThere is a bookshelf in this room.",
        "exits": ["south", "west"],
        "items": [{"name": "east_door_key", "category": "keys"}],
        "objects": [{"name": "bookshelf", "used": False}],
        "hint": "Search the bookshelf for a clue.",
        "requirement": [], 
        "requirement_message": ""
    },
    "east": {
        "description": "You are in a damp room. There is a door to the west and a door to the north.",
        "information": "The room is oddly damp and there is not much in it.\nThere is a chair and a torch on the other side.",
        "exits": ["west", "north"],
        "items": [{"name": "torch", "category": "generals"}],
        "objects": [{"name": "chair", "used": False}],
        "hint": "Try sitting in the chair to see if it helps.",
        "requirement": [{"name": "east_door_key", "category": "keys"}],
        "requirement_message": "In order to open this door you need an east door key."
    },
    "west": {
        "description": "You are in a cold room. There is a door to the east and a door to the north.",
        "information": "The room feels very cold and you slightly start to freeze.\nThere is a samll table on your right.",
        "exits": ["east", "north"],
        "items": [],
        "objects": [{"name": "table", "used": False}],
        "hint": "Maybe try to take a look onto the table.",
        "requirement": [],
        "requirement_message": ""
    }
}

object_interactions = {
    "desk": "You search the desk and find a pencil.",
    "bookshelf": "You browse the bookshelf and find a book on ancient history.",
    "chair": "You sit in the chair and feel more relaxed.",
    "table": "You examine the table and find a piece of paper with a puzzle on it."
}

object_items = {
    "desk": {"name": "pencil", "category": "generals"},
    "bookshelf": {"book": "pencil", "category": "generals"},
    "chair": {"name": "cushion", "category": "generals"},
    "table": {"name": "paper", "category": "generals"},
}

inventory_categories = {
    "keys": [],
    "weapons": [],
    "potions": [],
    "generals": []
}

# Define a function to add items to the inventory
def add_to_inventory(item):
    # Check if the item is in the inventory_categories dictionary
    for category, items in inventory_categories.items():
        if item in items:
            return
    # Add the item to the appropriate category based on the item's category
    inventory_categories[item["category"]].append(item)

# Define function to save game
def save(filename):
    # Create a dictionary to store the game state
    data = {
        "current_room": current_room,
        "rooms": rooms,
        "object_interactions": object_interactions,
        "object_items": object_items,
        "inventory_categories": inventory_categories
    }

    # Open the file in write mode
    with open(filename, "wb") as file:
        # Write the game state to the file using pickle
        pickle.dump(data, file)

# Define a function to load game
def load(filename):
    if not os.path.exists(filename):
            print("Save file not found.")
            return

    global current_room, rooms, object_interactions, object_items, inventory_categories

    # Open the file in read mode
    with open(filename, "rb") as file:
        # Read the game state from the file using pickle
        data = pickle.load(file)

    # Assign the values from the dictionary to the corresponding variables
    current_room = data["current_room"]
    rooms = data["rooms"]
    object_interactions = data["object_interactions"]
    object_items = data["object_items"]
    inventory_categories = data["inventory_categories"]

# Define function to print room description and available exits
def print_room(room):
    print(room["description"])
    print("Exits:", ", ".join(room["exits"]))

# Define function to move to a new room
def move(direction):
    global current_room
    # Get the current room and the room in the specified direction
    current_room_data = rooms[current_room]
    next_room_data = rooms[direction]

    # Check if the room in the specified direction is a valid exit
    if direction in current_room_data["exits"]:
        # Check if there is a requirement for entering the room
        if next_room_data["requirement"]:
            # Get the item required to enter the room
            required_item = next_room_data["requirement"][0]
            # Check if the required item is in the inventory
            if required_item in inventory_categories[required_item["category"]]:
                # Change the current room to the room in the specified direction
                current_room = direction
                print_room(rooms[current_room])
            else:
                # Print the requirement message
                print(next_room_data["requirement_message"])
        else:
            # Change the current room to the room in the specified direction
            current_room = direction
            print_room(rooms[current_room])
    else:
        print("You can't go that way.")

# Define function to pick up an item
def take(item):
    for room_item in rooms[current_room]["items"]:
        if room_item["name"] == item:
            # Remove the item from the room's items list
            rooms[current_room]["items"].remove(room_item)
            # Add the item to the inventory
            add_to_inventory(room_item)  # Pass the item dictionary to the add_to_inventory function
            print(f"You took the {item}.")
            return
    print(f"There is no {item} to take.")

# Define function to use an item
def use(item_name):
    # Check if the item is in the inventory_categories dictionary
    for category, items in inventory_categories.items():
        for item in items:
            if item["name"] == item_name:
                # Remove the item from the inventory_categories dictionary
                inventory_categories[category].remove(item)
                print(f"You used the {item_name}.")
                return
    # If the item is not found, display a message
    print(f"You don't have the {item_name}.")

# Define function to examine surroundings and gather information about the environment
def look():
    print("------ LOOK -------")
    print(rooms[current_room]["description"], "\n")
    print(rooms[current_room]["information"], "\n") 
    print("Exits:", ", ".join(rooms[current_room]["exits"])) 
    print("-------------------")

# Define function to search for items in the room
def search():
    print("------ SEARCH FOR ITEMS -------")
    if len(rooms[current_room]["items"]) == 0:
        print("There are no items to take.")
        print("-------------------------------")
        return
    print("You found the following items:")
    for item in rooms[current_room]["items"]:
        print("- " + item["name"])
        print("-------------------------------")

# Define a function to print the inventory
def print_inventory():
    # Print out the items in each category
    print("------ INVENTORY -------")
    for category, items in inventory_categories.items():
        print(f"{category.title()}:")
        for item in items:
            print(f"- {item['name']}")
    print("------------------------")

# Define function to interact with objects in the current room
def interact(object_name):
    # Find the object in the list of objects for the current room
    for obj in rooms[current_room]["objects"]:
        if obj["name"] == object_name:
            # Check the used flag for the object
            if obj["used"]:
                print("You have already interacted with this object.")
                return
            # Set the used flag to True
            obj["used"] = True
            # Check if the object has an interaction message
            if object_name in object_interactions:
                print(object_interactions[object_name])
            # Check if the object has an associated item
            if object_name in object_items:
                item = object_items[object_name] 
                add_to_inventory(item)
            else:
                print("You didn't find anything.")
            return
    print("There is no object with that name in this room.")

# Clear Terminal before Start
clear()

# Start message for Story Stuff
print("------ STORY -------")
print("As a battle mage, you have spent years honing your skills in the art of magic.\nWhen you hear about a rare gem hidden deep in a cave, you know that you must retrieve it.\nThe gem is said to grant unimaginable power to whoever possesses it,\nand you are determined to be the one to claim it.")
print("--------------------")
print_room(rooms[current_room])

# Define main game loop
while True:
    command = input("> ").split()
    if command[0] == "go" or command[0] == "walk" or command[0] == "move":
        move(command[1])
    elif command[0] == "take":
        take(command[1])
    elif command[0] == "use":
        use(command[1])
    elif command[0] == "look":
        look()
    elif command[0] == "search" or command[0] == "explore":
        search()
    elif command[0] == "inventory":
        print_inventory()
    elif command[0] == "interact":
        interact(command[1])
    elif command[0] == "load":
        load("save.dat")
        print("Game loaded.")
        clear() 
        print_room(rooms[current_room])
    elif command[0] == "save":
        save("save.dat")
        print("Game saved.")
    elif command[0] == "quit":
        sys.exit()
    else:
        print("I don't understand that command.")
