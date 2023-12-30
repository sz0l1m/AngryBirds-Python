import pymunk


def calculate_collision(arbiter: pymunk.Arbiter, space: pymunk.Space, data):
    shape_1, shape_2 = arbiter.shapes
    match (shape_1.collision_type, shape_2.collision_type):
        case (1, 3):
            space.remove(shape_2.body, shape_2)
            return False
        case (2, 3):
            if arbiter.total_ke > 50000000:
                space.remove(shape_2.body, shape_2)
        case (3, 4):
            if arbiter.total_ke > 50000000:
                space.remove(shape_1.body, shape_1)
    return True


def create_handlers(space: pymunk.Space):
    handlers = [space.add_collision_handler(i, j)
                for i in range(1, 4) for j in range(i + 1, 5)]
    for handler in handlers:
        handler.begin = calculate_collision
        handler.post_solve = calculate_collision
    return handlers
