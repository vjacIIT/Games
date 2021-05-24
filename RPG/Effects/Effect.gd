extends AnimatedSprite

func _ready():
	# used to connect animation_finished to the function below
	var _connection = self.connect("animation_finished", self, "_on_animation_finished")
	play("Animate")

# signal triggered at the end of animation "Animate"
func _on_animation_finished():
	queue_free()
