# tasks_config.py

CHORES_LIST = [
    # Format: (Name, Kategorie, Intervall, Punkte)
    
    # --- KITCHEN ---
    ("Dishes", "Kitchen", 1, 1),
    ("Wipe Counter", "Kitchen", 1, 1),
    ("Vacuum", "Kitchen", 7, 2),
    ("Mop", "Kitchen", 7, 2),
    ("Feeding Stations", "Kitchen", 7, 2),
    ("Take out Trash", "Kitchen", 7, 2),
    ("Wipe Appliances", "Kitchen", 14, 2),
    ("Dishwasher Clean", "Kitchen", 30, 3),
    ("Washingmachine Clean", "Kitchen", 30, 3),
    ("Oven Clean", "Kitchen", 30, 3),
    ("Fridge Clean", "Kitchen", 30, 3),
    ("Snack Cupboard", "Kitchen", 90, 4),
    ("Pantry Shelf", "Kitchen", 90, 4),
    ("Windows", "Kitchen", 180, 5),
    ("Doors", "Kitchen", 180, 5),
    ("Reorganize Cupboards", "Kitchen", 180, 5),

    # --- LIVING ROOM ---
    ("Floor reset", "Living Room", 1, 1),
    ("Litterbox", "Living Room", 3, 2),
    ("Vacuum", "Living Room", 7, 2),
    ("Mop", "Living Room", 7, 2),
    ("Couch reset", "Living Room", 7, 2),
    ("Tables reset", "Living Room", 7, 2),
    ("Take out Trash", "Living Room", 7, 2),
    ("Cat Tree/ Furniture reset", "Living Room", 14, 2),
    ("Windows", "Living Room", 180, 5),
    ("Doors", "Living Room", 180, 5),
    ("Bookshelf reset", "Living Room", 180, 5),

    # --- BATHROOM ---
    ("Floor reset", "Bathroom", 1, 1),
    ("Litterbox", "Bathroom", 3, 2),
    ("Vacuum", "Bathroom", 7, 2),
    ("Mop", "Bathroom", 7, 2),
    ("Wipe Furniture and Mirror", "Bathroom", 7, 2),
    ("Scrub Toilet", "Bathroom", 7, 2),
    ("Clean Sink (and Strainer)", "Bathroom", 7, 2),
    ("Scrub Bathtub and Anti-Slip Mat", "Bathroom", 7, 2),
    ("Mirror Cabinet Shelf reset", "Bathroom", 7, 2),
    ("Take out Trash", "Bathroom", 7, 2),
    ("Sort out Shampoos and Showergels", "Bathroom", 30, 3),
    ("Mirror Cabinet reorganize", "Bathroom", 120, 4),
    ("Tall Cabinet reorganize", "Bathroom", 120, 4),
    ("Doors", "Bathroom", 180, 5),

    # --- BEDROOM ---
    ("Floor reset", "Bedroom", 1, 1),
    ("Laundry", "Bedroom", 1, 1),
    ("Litterbox", "Bedroom", 3, 2),
    ("Vacuum", "Bedroom", 7, 2),
    ("Mop", "Bedroom", 7, 2),
    ("Take out Trash", "Bedroom", 7, 2),
    ("Mirrors", "Bedroom", 14, 2),
    ("Change Bedsheets", "Bedroom", 30, 3),
    ("Dresser Top reset", "Bedroom", 30, 3),
    ("Windows", "Bedroom", 180, 5),
    ("Doors", "Bedroom", 180, 5),

    # --- HALLWAY ---
    ("Floor reset", "Hallway", 1, 1),
    ("Litterbox", "Hallway", 3, 2),
    ("Vacuum", "Hallway", 7, 2),
    ("Mop", "Hallway", 7, 2),
    ("Bench reset", "Hallway", 7, 2),

    # --- OFFICE ---
    ("Floor reset", "Office", 1, 1),
    ("Litterboxes", "Office", 3, 4),
    ("Vacuum", "Office", 7, 2),
    ("Mop", "Office", 7, 2),
    ("Take out Trash", "Office", 7, 2),
    ("Desk reset", "Office", 7, 2),
    ("Cat Furniture reset", "Office", 14, 2),
    ("Windows", "Office", 180, 5),
    ("Doors", "Office", 180, 5),

# --- ALL ROOMS ---
    ("Vacuum Bot", "General", 3, 1)
]

# Format: (Name, Kategorie, Intervall, Punkte, Is_Personal, For_User)
PERSONAL_CHORES = [ 
    ("Take Pills", "Daily", 1, 1, True, "Both"),
    ("Brush Teeth (Morning)", "Daily", 1, 1, True, "Both"),
    ("Brush Teeth (Night)", "Daily", 1, 1, True, "Both"),
    ("Wash Face with Cleanser", "Daily", 1, 2, True, "Both"),
    ("Cream Face", "Daily", 1, 1, True, "Both"),
    ("Shower (Body)", "Weekly", 7, 2, True, "Both"),
    ("Wash Hair", "Weekly", 7, 3, True, "Both"),
    ("Toenails", "2-Weeks", 14, 1, True, "Both"),
    ("Fingernails", "2-Weeks", 14, 1, True, "Both"),
    ("Shave Armpits", "2-Weeks", 14, 1, True, "Both"),
    ("Eyebrows", "2-Weeks", 14, 1, True, "Both"),
    # Bonus/Individual
    ("Shave Legs", "Bonus", 0, 4, True, "Eda"),
    ("Shave Beard", "Bonus", 0, 3, True, "Melih"),
    ("Shave Bikini", "Bonus", 0, 5, True, "Both"),
    ("Shower (Full)", "Bonus", 0, 4, True, "Both"),
    ("Body Peeling", "Bonus", 0, 4, True, "Both"),
    ("Body Lotion", "Bonus", 0, 3, True, "Both"),
    ("Scalp Oil Massage", "Bonus", 0, 3, True, "Both"),
    ("Face Peeling", "Bonus", 0, 2, True, "Both") 
]