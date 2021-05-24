extends Control

const duration = 2
const DIED_MESSAGE = "You Died"

onready var scene_tree = get_tree()
onready var pauseOverlay: ColorRect = $PauseOverlay
onready var score_label = $Label
onready var pause_title = $PauseOverlay/Title
onready var timer = $Timer


var paused = false setget set_paused

func _ready():
	var _conn = PlayerStats.connect("score_updated", self, "change_score")
	var _conn2 = PlayerStats.connect("no_health", self, "player_died")
	change_score(0)

func player_died():
	# so that the pause screen doesn't come instantaneously at the time of death of player
	timer.start(duration)

func _on_Timer_timeout():
	# after waiting for duration sec, pause screen pops up
	self.paused = true
	pause_title.text = DIED_MESSAGE

func _unhandled_input(event):
	if event.is_action_pressed("pause") and pause_title.text != DIED_MESSAGE:
		self.paused = not paused
		# when this function is running none of the other input keys will work
		scene_tree.set_input_as_handled()

func change_score(value):
	score_label.text = "Score: %s" % value

func set_paused(value):
	paused = value
	scene_tree.paused = value
	pauseOverlay.visible = value
