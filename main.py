width = 1200
height = int((width * (9 / 16)))

if __name__ == "__main__":
	from gamecontroller import GameController
	
	GameController(width, height)
