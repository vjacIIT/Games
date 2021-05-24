extends Area2D

# checks if 2 areas are colliding or not
func is_colliding():
	var areas = get_overlapping_areas()
	return areas.size() > 0
	
# if 2 areas or bats are colliding then we need to seperate them out
func get_push_vector():
	var areas = get_overlapping_areas()
	var push_vector = Vector2.ZERO
	if is_colliding():
		var area = areas[0]
		push_vector = area.global_position.direction_to(global_position)
		push_vector = push_vector.normalized()
	return push_vector
