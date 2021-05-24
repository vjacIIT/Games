extends Node2D

const GrassEffect = preload("res://Effects/GrassEffect.tscn")

func create_grass_effect():
	# taken animated sprite from scene
	var grassEffect = GrassEffect.instance()
	# takes the parent and add child to it
	get_parent().add_child(grassEffect)
	# putting position of grassEffect as the position of grass
	grassEffect.global_position = global_position

func _on_HurtBox_area_entered(_area):
	create_grass_effect()
	queue_free()
