tool
extends Area2D

onready var anim_player: AnimationPlayer = get_node("AnimationPlayer")
export var next_scene: PackedScene

func _on_Portal2D_body_entered(body):
	teleport()

func _get_configuration_warning() -> String:
	return "the next scene property can't be empty" if not next_scene else ""
	
func teleport() -> void:
	# fade (make black), then change scene to make new level
	anim_player.play("fade_in")
	# wait for a signal for animation to get finished
	yield(anim_player, "animation_finished")
	# then change scene
	get_tree().change_scene_to(next_scene)
