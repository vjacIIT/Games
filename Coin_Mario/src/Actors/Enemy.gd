extends Actor
#extends "res://src/Actors/Actor.gd"

# score player gets when enemy dies
export var score: = 100

func _ready():
	# process only in the view will work (even at the starting)
	set_physics_process(false)
	_velocity.x = -speed.x

func _on_StompDetector_body_entered(body):
	# if the player is toching from the sides pr may be touching from below
	if body.global_position.y > get_node("StompDetector").global_position.y:
		return
	# player attacked from above, free up the enemy
	$CollisionShape2D.set_deferred("disabled",true)
	#get_node("CollisionShape2D").disabled = true
	die()

func _physics_process(delta):
	_velocity.y += gravity * delta
	# changing direction of enemy
	if is_on_wall():
		_velocity.x *= -1.0
	_velocity.y = move_and_slide(_velocity, FLOOR_NORMAL).y
	
func die():
	PlayerData.score += score
	queue_free()