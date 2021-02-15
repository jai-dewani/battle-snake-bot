import os
import random

import cherrypy

"""
This is a simple Battlesnake server written in Python.
For instructions see https://github.com/BattlesnakeOfficial/starter-snake-python/README.md
"""
def extract_snakes(data):
    snakes = []
    for snake in data["board"]["snakes"]:
        for loc in snake["body"]:
            snakes.append([loc["x"], loc["y"]])
    return snakes
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

def check_other_snake(snakes, x, y): 
    # print("Snakes: ", snakes, x, y)
    for snake in snakes:
        if snake[0]==x and snake[1]==y:
            return False 
    return True 

class Battlesnake(object):
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def index(self):
        # This function is called when you register your Battlesnake on play.battlesnake.com
        # It controls your Battlesnake appearance and author permissions.
        # TIP: If you open your Battlesnake URL in browser you should see this data
        return {
            "apiversion": "1",
            "author": "",  # TODO: Your Battlesnake Username
            "color": "#888888",  # TODO: Personalize
            "head": "default",  # TODO: Personalize
            "tail": "default",  # TODO: Personalize
        }

    @cherrypy.expose
    @cherrypy.tools.json_in()
    def start(self):
        # This function is called everytime your snake is entered into a game.
        # cherrypy.request.json contains information about the game that's about to be played.
        data = cherrypy.request.json

        print("START")
        return "ok"

    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def move(self):
        # This function is called on every turn of a game. It's how your snake decides where to move.
        # Valid moves are "up", "down", "left", or "right".
        # TODO: Use the information in cherrypy.request.json to decide your next move.
        data = cherrypy.request.json
        board_dim = [data['board']["height"],data['board']['width']]
        snakes = extract_snakes(data)

        you = data["you"]
        you_head = [you["head"]["x"], you["head"]["y"]]
        you_body = you["body"]
        you_length = you["length"]
        
        # Choose a random direction to move in
        possible_moves = [[0,1], [0,-1], [-1,0], [1,0]]
        random.shuffle(possible_moves)
        for move in possible_moves:
            x,y = you_head[0]+move[0], you_head[1]+move[1]
            print(f"MOVE: {move}")
            temp1 = check_wall(board_dim,x,y)
            temp2 = check_other_snake(snakes,x,y)
            print(temp1,temp2)
            if temp1 and temp2:
                print(f"FINAL MOVE: {move}")
                return {"move":assign_move(move)}
        move = random.choice(possible_moves)
        # print(f"Data:{data}")
        print(f"RANDOM MOVE: {move}")
        return {"move": assign_move(move)}

    
        
    @cherrypy.expose
    @cherrypy.tools.json_in()
    def end(self):
        # This function is called when a game your snake was in ends.
        # It's purely for informational purposes, you don't have to make any decisions here.
        data = cherrypy.request.json

        print("END")
        return "ok"

    


if __name__ == "__main__":
    server = Battlesnake()
    cherrypy.config.update({"server.socket_host": "0.0.0.0"})
    cherrypy.config.update(
        {"server.socket_port": int(os.environ.get("PORT", "80")),}
    )
    print("Starting Battlesnake Server...")
    cherrypy.quickstart(server)
