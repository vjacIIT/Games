extends KinematicBody2D

export var ACCELERATION = 100
export var MAX_SPEED = 150
export var FRICTION = 400
export var ROLL_SPEED = 150

const PlayerHurtSound = preload("res://Player/PlayerHurtSound.tscn")
const DeathEffect = preload("res://Effects/EnemyDeathEffect.tscn")

enum {
	MOVE,
	ROLL,
	ATTACK
}

var state = MOVE
var velocity = Vector2.ZERO
var roll_velocity = Vector2.DOWN
# PlayerStats has been made global in project settings 
var stats = PlayerStats

onready var animationPlayer = $AnimationPlayer
onready var animationTree = $AnimationTree
onready var animationState = animationTree.get("parameters/playback")
onready var swordHitbox = $HitboxPivot/SwordHitbox
onready var hurtbox = $HurtBox
onready var blinkAnimationPlayer = $BlinkAnimationPlayer

func _ready():
	# stats emits the signal no_health, we have connected it to queue_free (to remove the player)
	stats.connect("no_health", self, "player_no_health")
	animationTree.active = true
	# used to store the direction where our sword is swinging
	swordHitbox.knockback_vector = roll_velocity

func _physics_process(delta):
	match state:
		MOVE:
			move_state(delta)
		ROLL:
			roll_state(delta)
		ATTACK:
			attack_state(delta)

func move_state(delta):
	var input_vector = Vector2.ZERO
	# for the direction to move
	input_vector.x = Input.get_action_strength("ui_right") - Input.get_action_strength("ui_left")
	input_vector.y = Input.get_action_strength("ui_down") - Input.get_action_strength("ui_up")
	input_vector = input_vector.normalized()
	if input_vector != Vector2.ZERO:
		roll_velocity = input_vector
		swordHitbox.knockback_vector = roll_velocity
		# connects blend position according to input_vector, i.e. direction we are trying to move
		# blend position determines which child node animation (i.e. either right run, left run ...) to run
		animationTree.set("parameters/Idle/blend_position", input_vector)
		animationTree.set("parameters/Run/blend_position", input_vector)
		animationTree.set("parameters/Attack/blend_position", input_vector)
		animationTree.set("parameters/Roll/blend_position", input_vector)
		animationState.travel("Run")
		velocity = velocity.move_toward(input_vector * MAX_SPEED, ACCELERATION * delta)
	else:
		animationState.travel("Idle")
		velocity = velocity.move_toward(Vector2.ZERO, FRICTION * delta)
	
	#print(velocity)
	velocity = move_and_slide(velocity)
	
	# done only once even when you continue holding the attack key
	if Input.is_action_just_pressed("attack"):
		state = ATTACK
	
	if Input.is_action_just_pressed("roll"):
		state = ROLL

func attack_state(_delta):
	velocity = Vector2.ZERO
	animationState.travel("Attack")
	
func roll_state(_delta):
	velocity = roll_velocity * ROLL_SPEED
	animationState.travel("Roll")
	velocity = move_and_slide(velocity)
	
# called at the end of attack animation via a signal
func attack_animation_finished():
	state = MOVE
	
# called at the end of roll animation via signal
func roll_animation_finished():
	velocity = velocity/1.25
	state = MOVE

# signal emmited by stats when there is no health of bat
func player_no_health():
	create_death_effect()
	queue_free()

func create_death_effect():
	# taken animated sprite from scene
	var deathEffect = DeathEffect.instance()
	# takes the parent and add child to it
	get_parent().add_child(deathEffect)
	# putting position of enemyDeathEffect as the position of bat
	deathEffect.global_position = global_position

# when bat enters the player
func _on_HurtBox_area_entered(area):
	stats.health-=area.damage
	# player is invincible for 0.5s
	hurtbox.start_invincibility(0.5)
	hurtbox.create_hit_effect()
	var playerHurtSound = PlayerHurtSound.instance()
	get_tree().current_scene.add_child(playerHurtSound)

func _on_HurtBox_invincibility_started():
	blinkAnimationPlayer.play("Start")

func _on_HurtBox_invincibility_ended():
	blinkAnimationPlayer.play("Stop")
