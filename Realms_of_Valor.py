# Import necessary modules
import sys, os, pickle, json

clear = lambda: os.system('cls')

# Define global variables
current_room = "south" 

# Define dictionary of rooms
f_rooms = open("rooms.json") 
rooms = json.load(f_rooms)
 
# Define Items for Interactions
f_object_items = open("objects\items.json") 
object_items = json.load(f_object_items)

# Define NPCs
f_npcs = open("npcs.json") 
npcs = json.load(f_npcs)

# Define Inventory
inventory_categories = {
    "keys": [],
    "weapons": [],
    "potions": [],
    "generals": []
}

# Define a function to find npcs in a room
def get_current_room_npc():
    for npc_id, npc in npcs.items():  # iterate over the NPCs in the npcs dictionary 
        if npc["location"] == current_room:  # access the location field using the correct key
            return npc
    return None  # no NPC found in the current room

# Define a function to find npcs by name
def find_npc_by_name(name):
  # Iterate through the NPCs and check their names
  for npc_id, npc in npcs.items():
    if npc["name"] == name:
      # Return the NPC's ID if the names match
      return npc_id
  # Return None if no matching NPC is found
  return None

# Define a function to talk to npcs
def talk_to_npc_by_name(name):
  # Find the NPC's ID using the find_npc_by_name function
  npc_id = find_npc_by_name(name)
  if npc_id is not None:
    # Check if the npc is in the current room
    if current_room == npcs[npc_id]["location"]:
        # Call the talk_to_npc function if the NPC was found and is in this room
        talk_to_npc(npc_id)
    else:
        # Display an error message if the NPC was not found
        print("There is no NPC with the name '" + name + "'.")
  else:
    # Display an error message if the NPC was not found
    print("There is no NPC with the name '" + name + "'.")

# Define a function to talk to a npc
def talk_to_npc(npc_id):
  # Retrieve the NPC data from the dictionary
  npc = npcs[npc_id]
  
  # Display the NPC's name and dialogue
  print("You are talking to " + npc["name"] + ".\n")
  print(npc["dialogue"])
  
  # Display the player's choices
  for i, response in enumerate(npc["responses"]):
    print(str(i+1) + ": " + response["text"])
  
  # Get the player's choice
  choice = int(input())

  print("")
  
  # Execute the chosen response
  callback_name = npc["responses"][choice-1]["callback"]
  callback_function = globals()[callback_name]
  callback_function(npc["responses"][choice-1]["arguments"])

def npc_answer(answer):
    print(answer)

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
        "object_items": object_items,
        "inventory_categories": inventory_categories
    }

    # Open the file in write mode
    with open(filename, "wb") as file:
        # Write the game state to the file using pickle
        pickle.dump(data, file)

# Define a function to load game
def load(filename):
    global current_room, rooms, object_items, inventory_categories

    # Open the file in read mode
    with open(filename, "rb") as file:
        # Read the game state from the file using pickle
        data = pickle.load(file)

    # Assign the values from the dictionary to the corresponding variables
    current_room = data["current_room"]
    rooms = data["rooms"]
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
    
    npc = get_current_room_npc()
    if npc:
        # Print the NPC's description
        print(f"There is a {npc['name']} here.\n")

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
            # Check if the object has an associated item
            if object_name in object_items:
                item = object_items[object_name] 
                print(object_items[object_name]["interaction"])
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
    print("")
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
    elif command[0] == "talk":
        talk_to_npc_by_name(command[1])
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
    print("") 