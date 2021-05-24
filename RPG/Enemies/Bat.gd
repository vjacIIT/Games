extends KinematicBody2D

const knockspeed = 150
const EnemyDeathEffect = preload("res://Effects/EnemyDeathEffect.tscn")

export var ACCELERATION = 300
export var MAX_SPEED = 50
export var FRICTION = 200 
export var COLLISION_SPACE = 400
export var WANDER_TARGET_RANGE = 10
export var DEATH_SCORE = 10

enum{
	IDLE,
	WANDER,
	CHASE
}

var velocity = Vector2.ZERO
var knockback = Vector2.ZERO
var state = IDLE

onready var stats = $Stats
onready var playerStats = PlayerStats
onready var playerDetectionZone = $PlayerDetectionZone
onready var sprite = $AnimatedSprite
onready var hurtbox = $HurtBox
onready var softCollision = $SoftCollision
onready var wanderController = $WanderController
onready var animationPlayer = $AnimationPlayer

func _ready():
	state = pick_random_state([IDLE, WANDER])

func _physics_process(delta):
	# if the bat is hit by the sword, otherwise knockback = Vector2.ZERO
	knockback = knockback.move_toward(Vector2.ZERO, FRICTION * delta)
	knockback = move_and_slide(knockback)
	match state:
		IDLE:
			velocity = velocity.move_toward(Vector2.ZERO, FRICTION * delta)
			seek_player()
			# if timer is out, then player can choose any of the idle or wander state
			if wanderController.get_time_left() == 0:
				state = pick_random_state([IDLE, WANDER])
				wanderController.set_wander_timer(rand_range(1,3))
		WANDER:
			seek_player()
			# if timer is out, then player can choose any of the idle or wander state
			if wanderController.get_time_left() == 0:
				state = pick_random_state([IDLE, WANDER])
				wanderController.set_wander_timer(rand_range(1,3))
			var direction = global_position.direction_to(wanderController.target_position)
			velocity = velocity.move_toward(direction * MAX_SPEED, ACCELERATION * delta)
			sprite.flip_h = velocity.x < 0
			
			# if bat has reached it's target position
			if global_position.distance_to(wanderController.target_position) <= WANDER_TARGET_RANGE:
				state = pick_random_state([IDLE, WANDER])
				wanderController.set_wander_timer(rand_range(1,3))
				
		CHASE:
			var player = playerDetectionZone.player
			# player detected
			if player != null:
				# direction in which bat needs to run to chase the player
				var direction = (player.global_position - global_position).normalized()
				velocity = velocity.move_toward(direction * MAX_SPEED, ACCELERATION * delta)
				sprite.flip_h = velocity.x < 0
			# player lost by bat
			else:
				state = IDLE
	# if 2 or more bats are colliding to each other
	if softCollision.is_colliding():
		velocity += softCollision.get_push_vector() * delta * COLLISION_SPACE
	velocity = move_and_slide(velocity)

# tries to find player, if yes changes the state to chase
func seek_player():
	if playerDetectionZone.can_see_player():
		state = CHASE
		
func pick_random_state(state_list):
	state_list.shuffle()
	return state_list.pop_front()

func _on_HurtBox_area_entered(area):
	# health changes here, hence set_health is called
	stats.health -= area.damage
	# area (swordHitbox area) has knockback_vector
	knockback = area.knockback_vector * knockspeed
	hurtbox.create_hit_effect()
	hurtbox.start_invincibility(0.5)

# signal emmited by stats when there is no health of bat
func _on_Stats_no_health():
	playerStats.score += 10
	create_death_effect()
	queue_free()

func create_death_effect():
	# taken animated sprite from scene
	var enemyDeathEffect = EnemyDeathEffect.instance()
	# takes the parent and add child to it
	get_parent().add_child(enemyDeathEffect)
	# putting position of enemyDeathEffect as the position of bat
	enemyDeathEffect.global_position = global_position

func _on_HurtBox_invincibility_started():
	animationPlayer.play("Start")

func _on_HurtBox_invincibility_ended():
	animationPlayer.play("Stop")
