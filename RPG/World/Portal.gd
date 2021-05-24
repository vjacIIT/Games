tool
extends Area2D

onready var animationPlayer = $AnimationPlayer
export var next_scene: PackedScene

func _get_configuration_warning():
	return "The next Scene is empty" if not next_scene else ""

func teleport():
	animationPlayer.play("fade_in")
	yield(animationPlayer, "animation_finished")
	var _new_tree = get_tree().change_scene_to(next_scene)

func _on_Portal_body_entered(_body):
	teleport()
