tool
extends Button

export(String, FILE) var next_scene_path = ""

func _on_PlayButton_button_up():
	var _next_scene = get_tree().change_scene(next_scene_path)

func _get_configuration_warning():
	return "next_scene_path must be set" if next_scene_path == "" else ""
