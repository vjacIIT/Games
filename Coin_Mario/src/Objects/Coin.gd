extends Area2D

onready var anim_player: AnimationPlayer = get_node("AnimationPlayer")
# score player gets after picking coin
export var score: = 50


# when player enters coin, fade it out
func _on_Coin_body_entered(body):
	picked()
	
func picked():
	PlayerData.score += score
	anim_player.play("fade_out")