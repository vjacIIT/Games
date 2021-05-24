extends Control

var hearts = 4 setget set_hearts
var max_hearts = 4 setget set_max_hearts
onready var heartUIFull = $HeartUIFull
onready var heartUIEmpty = $HeartUIEmpty

func set_hearts(value):
	hearts = clamp(value, 0, max_hearts)
	if heartUIFull != null:
		heartUIFull.rect_size.x = hearts * 15

func set_max_hearts(value):
	max_hearts = max(value, 1)
	self.hearts = min(hearts, max_hearts)
	if heartUIEmpty != null:
		heartUIEmpty.rect_size.x = max_hearts * 15
	
func _ready():
	self.max_hearts = PlayerStats.max_health
	self.hearts = PlayerStats.health
	# connect to health_change signal and call the set_hearts function with argument
	var _conn = PlayerStats.connect("health_change", self, "set_hearts")
	var _conn2 = PlayerStats.connect("max_health_changed", self, "set_max_hearts")
