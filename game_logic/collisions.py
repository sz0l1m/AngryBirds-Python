import pymunk


def calculate_collision(arbiter: pymunk.Arbiter, space: pymunk.Space, data):
    """
    Depending on which bodies has collided it decides whether the body should be removed
    from pymunk's space taking kinetic energy of the collision into account.
    """
    shape_1, shape_2 = arbiter.shapes
    match (shape_1.collision_type, shape_2.collision_type):
        case (1, 3):
            if arbiter.total_ke > 3000000:
                space.remove(shape_2.body, shape_2)
                return False
        case (2, 3):
            if arbiter.total_ke > 40000000:
                space.remove(shape_2.body, shape_2)
        case (3, 4) | (3, 5) | (3, 6):
            if arbiter.total_ke > 23000000:
                space.remove(shape_1.body, shape_1)
        case (3, 3):
            if arbiter.total_ke > 23000000:
                space.remove(shape_1.body, shape_1)
                space.remove(shape_2.body, shape_2)
        case (2, 5) | (4, 5) | (5, 5) | (5, 6):
            if arbiter.total_ke > 300000000:
                space.remove(shape_2.body, shape_2)
        case (5, 6):
            if arbiter.total_ke > 300000000:
                space.remove(shape_1.body, shape_1)
    return True


def create_handlers(space: pymunk.Space):
    """
    Creates collision handlers for every combination of collision types.
    Adds calculate_collision function as a callback function for begin and post_solve
    events of each of pymunk's collision handlers.
    """
    handlers = [space.add_collision_handler(i, j)
                for i in range(1, 6) for j in range(i + 1, 6)]
    for handler in handlers:
        handler.begin = calculate_collision
        handler.post_solve = calculate_collision
    return handlers


def rolling_resistance(space: pymunk.Space):
    """
    Creates rolling resistance for bird and pigs which slows down
    their horizontal speed when their vertical speed is zero.
    """
    for body, shape in zip(space.bodies, space.shapes):
        if shape.collision_type == 1 or shape.collision_type == 3:
            if round(body.velocity[1]) == 0:
                if body.velocity[0] >= 3:
                    body.velocity -= (3, 0)
                elif body.velocity[0] > 0:
                    body.velocity = (0, 0)
                elif body.velocity[0] <= -3:
                    body.velocity += (3, 0)
                elif body.velocity[0] < 0:
                    body.velocity = (0, 0)
