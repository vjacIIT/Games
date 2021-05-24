extends Button

var stats = PlayerStats

func _on_RetryButton_button_up():
	stats.score = 0
	stats.health = max(stats.health, 1)
	get_tree().paused = false
	var _currScene = get_tree().reload_current_scene()
