extends AudioStreamPlayer2D

func _ready():
	var _conn = connect("finished", self, "queue_free")
