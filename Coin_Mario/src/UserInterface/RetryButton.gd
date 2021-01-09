extends Button

# retry the current scene with score = 0
func _on_RetryButton_button_up():
	PlayerData.score = 0
	# in built in godot
	get_tree().paused = false
	get_tree().reload_current_scene()