extends Node2D

var playerStats = PlayerStats
onready var animationPlayer = $AnimationPlayer

func _on_HurtBox_body_entered(body):
	animationPlayer.play("fade_out")
	playerStats.health+=1
