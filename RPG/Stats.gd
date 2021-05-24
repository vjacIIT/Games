extends Node

export var max_health = 1 setget set_max_health

var health = max_health setget set_health
var score = 0 setget set_score

signal no_health
signal health_change(value)
signal max_health_changed(value)
signal score_updated(value)

func set_max_health(value):
	max_health = value
	self.health = min(health, max_health)
	emit_signal("max_health_changed", max_health)

# called whenever health changes
func set_health(value):
	health = value
	emit_signal("health_change", health)
	if health <= 0:
		emit_signal("no_health")

func set_score(value):
	score = value
	emit_signal("score_updated", score)

func reset_score():
	score = 0

func _ready():
	self.health = max_health
