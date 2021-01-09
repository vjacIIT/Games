extends Control
# toggling the pause menu (visibility) to see the retry, MainScreen and quit buttons

onready var scene_tree: = get_tree()
onready var pause_overlay: ColorRect = get_node("PauseOverlay")
onready var score: Label = get_node("Label")
onready var pause_title: Label = get_node("PauseOverlay/Title")
var paused: = false setget set_paused
const DIED_MESSAGE = "You died"

func _ready():
	# score_updated signal created at PlayerData.gd
	PlayerData.connect("score_updated", self, "update_interface")
	# similar case as above
	PlayerData.connect("player_died", self, "_on_PlayerData_player_died")
	update_interface()

func _on_PlayerData_player_died():
	self.paused = true
	pause_title.text = DIED_MESSAGE

func _unhandled_input(event):
	# if we are dead then we should not be able to press escape
	if event.is_action_pressed("pause") and pause_title.text!=DIED_MESSAGE:
		# toggle the paused, self used to call set_paused function
		self.paused = !paused
		# not propagate the events if you are in paused menu
		scene_tree.set_input_as_handled()

func update_interface():
	score.text = "Score: %s" % PlayerData.score

func set_paused(value: bool):
	paused = value
	scene_tree.paused = paused
	pause_overlay.visible = paused