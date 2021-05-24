extends Node2D

var stats = PlayerStats
onready var animationPlayer = $AnimationPlayer
export var COIN_SCORE = 5

func _on_HurtBox_body_entered(_body):
	animationPlayer.play("fade_out")
	stats.score += COIN_SCORE
