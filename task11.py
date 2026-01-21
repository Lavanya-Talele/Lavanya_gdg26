import tkinter as tk
import turtle

# 1-Logic

def expand_lsystem(axiom, rules_dict, iterations):
    #Replaces letters in the string based on rules.
    current_string = axiom
    for _ in range(iterations):
        next_string = ""
        for char in current_string:
            # Replace if rule exists, else keep the character
            next_string += rules_dict.get(char, char)
        current_string = next_string
    return current_string

def parse_rules(raw_rules):
    #Converts 'F:F+F,X:FF' into {'F': 'F+F', 'X': 'FF'}.
    rules_dict = {}
    if not raw_rules.strip():
        return rules_dict
    pairs = raw_rules.split(",")
    for pair in pairs:
        if ":" in pair:
            key, val = pair.split(":")
            rules_dict[key.strip()] = val.strip()
    return rules_dict

# 2-Drawing

def draw_lsystem(instructions, angle, t_obj, screen_obj):
    #Interprets the string into turtle movements with a stack.
    t_obj.clear()
    t_obj.penup()
    t_obj.home()
    t_obj.setheading(90) # Start pointing UP like a tree
    t_obj.pendown()
    
    stack = [] # The "Backpack" to save positions for [ ]
    step = 5   # Length of one 'F' line
    
    screen_obj.tracer(0, 0) # Instant drawing mode
    
    for i, cmd in enumerate(instructions):
        # Brownie Point: Color Gradient based on progress (Blue to Green)
        ratio = i / len(instructions)
        t_obj.pencolor(0, int(255 * ratio), int(255 * (1 - ratio)))

        if cmd == 'F':
            t_obj.forward(step)
        elif cmd == '+':
            t_obj.right(angle)
        elif cmd == '-':
            t_obj.left(angle)
        elif cmd == '[':
            # Save current state (position and angle)
            stack.append((t_obj.position(), t_obj.heading()))
        elif cmd == ']':
            # Restore to last saved state
            pos, head = stack.pop()
            t_obj.penup()
            t_obj.setposition(pos)
            t_obj.setheading(head)
            t_obj.pendown()

    screen_obj.update() # Show the final drawing

# 3-Button

def on_generate_click():
    # Gets data from UI and starts the process.
    # Getting text from the Entry boxes
    axiom = entry_axiom.get()
    rules_text = entry_rules.get()
    
    try:
        angle = float(entry_angle.get())
        iters = int(entry_iters.get())
    except ValueError:
        print("Please enter numbers for angle and iterations!")
        return

    # Process
    rules_dict = parse_rules(rules_text)
    final_string = expand_lsystem(axiom, rules_dict, iters)
    
    # Draw (Passing our global turtle and screen)
    draw_lsystem(final_string, angle, my_turtle, my_screen)

# 4-GUI

root = tk.Tk()
root.title("L-System Visualizer")

# Drawing Area (Left)
canvas = tk.Canvas(root, width=600, height=600, bg="white")
canvas.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

# Controls Area (Right)
sidebar = tk.Frame(root, width=200, padx=10, pady=10)
sidebar.pack(side=tk.RIGHT, fill=tk.Y)

# UI Widgets (Labels and Entries)
tk.Label(sidebar, text="Axiom:").pack(anchor="w")
entry_axiom = tk.Entry(sidebar)
entry_axiom.insert(0, "X")
entry_axiom.pack(fill="x")

tk.Label(sidebar, text="Rules:").pack(anchor="w")
entry_rules = tk.Entry(sidebar)
entry_rules.insert(0, "X:F[+X][-X]FX, F:FF")
entry_rules.pack(fill="x")

tk.Label(sidebar, text="Angle:").pack(anchor="w")
entry_angle = tk.Entry(sidebar)
entry_angle.insert(0, "25")
entry_angle.pack(fill="x")

tk.Label(sidebar, text="Iterations:").pack(anchor="w")
entry_iters = tk.Entry(sidebar)
entry_iters.insert(0, "4")
entry_iters.pack(fill="x")

btn = tk.Button(sidebar, text="Draw", command=on_generate_click, bg="lightblue")
btn.pack(fill="x", pady=10)

# Setup Turtle to live inside the Tkinter Canvas
my_screen = turtle.TurtleScreen(canvas)
my_screen.colormode(255)
my_turtle = turtle.RawTurtle(my_screen)
my_turtle.hideturtle()

root.mainloop()
