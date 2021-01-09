extends Node
# any other script in the project will be able to access it

signal score_updated
signal player_died

# every time score changes in any script: set_score is called
var score: = 0 setget set_score
var deaths: = 0 setget set_deaths

# resets when gamer does playAgain in EndScreen
func reset():
	score = 0
	deaths = 0

func set_score(value: int):
	score = value
	emit_signal("score_updated")
	return
	
func set_deaths(value: int):
	deaths = value
	emit_signal("player_died")
	return