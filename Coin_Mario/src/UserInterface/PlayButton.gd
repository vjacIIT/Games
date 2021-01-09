tool
extends Button

# tells godot that file path is needed in the string
export(String, FILE) var next_scene_path: = ""

func _on_ChangeSceneButton_button_up():
	# if someone comes here after clicking of MainScreen in paused menu
	get_tree().paused = false
	get_tree().change_scene(next_scene_path)

func _get_configuration_warning():
	return "next_scene_path must be set" if next_scene_path == "" else ""