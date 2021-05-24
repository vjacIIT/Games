extends Control

onready var score_label = $ScoreLabel

func _ready():
	score_label.text = score_label.text % [PlayerStats.score]
