import random
def extract_snakes(data):
    snakes = []
    for snake in data["board"]["snakes"]:
        for loc in snake["body"]:
            snakes.append([loc["x"], loc["y"]])
    return snakes

def extract_snakes_head(data):
    snake_heads = []
    for snake in data["board"]["snakes"]:
        if snake["id"]!=data["you"]["id"]:
            head = snake["head"]
            snake_heads.append([head["x"], head["y"]])
    return snake_heads
    
def distance(a,b):
    return abs(a[0]-b[0]) + abs(a[1]-b[1])

def assign_move(move):
    if move==[0,1]:
        return "up"
    elif move==[0,-1]:
        return "down"
    elif move==[1,0]:
        return "right"
    elif move==[-1,0]:
        return "left"

def check_wall(board_dim, x,y):
    # print("wall: ",board_dim,x,y)
    X,Y = board_dim
    if 0<=x<X and 0<=y<Y:
        return True 
    return False

def check_other_snake(snakes,snake_heads,x, y): 
    # print("Snakes: ", snakes, x, y)
    for snake in snakes:
        if snake[0]==x and snake[1]==y:
            return False 
    for head in snake_heads:
        if distance(head,[x,y])<=1:
            return False
    return True 

def return_value(move,shout):
    return {
        "move":assign_move(move),
        "shout":shout
    }

def move(data):
    board_dim = [data['board']["height"],data['board']['width']]
    snakes = extract_snakes(data)
    snake_heads = extract_snakes_head(data)

    food_temp = data["board"]["food"]
    foods = []
    for food in food_temp:
        foods.append([food["x"],food["y"]])
    


    you = data["you"]
    you_head = [you["head"]["x"], you["head"]["y"]]
    you_body = you["body"]
    you_length = you["length"]
    
    # Choose a random direction to move in
    directions = [[0,1], [0,-1], [-1,0], [1,0]]
    possible_moves = []
    for move in directions:
        x,y = you_head[0]+move[0], you_head[1]+move[1]
        # print(f"MOVE: {move}")
        temp1 = check_wall(board_dim,x,y)
        temp2 = check_other_snake(snakes,snake_heads,x,y)
        print(temp1,temp2)
        if temp1 and temp2:
            possible_moves.append(move)
    
    for move in possible_moves:
        x,y = you_head[0]+move[0], you_head[1]+move[1]
        for food in foods:
            if distance([x,y],food)==0:
                print(f"FINAL MOVE: {move}")
                return return_value(move,"POSSBILE: " + " ".join(f"[{x[0]} {x[1]}]" for x in possible_moves))
    if len(possible_moves)>0:
        move = random.choice(possible_moves)
        print(f"RANDOM POSSBILE MOVE: {move} out of {possible_moves}")
        return {"move": assign_move(move)}
    else:
        move = random.choice(directions)
        print(f"RANDOM MOVE: {move}")
        return {"move": assign_move(move)}

