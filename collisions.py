import pymunk


def calculate_collision(arbiter, space, data):
    pass


def create_handlers(space: pymunk.Space):
    handlers = [space.add_collision_handler(i, j)
                for i in range(1, 4) for j in range(i + 1, 5)]
    for handler in handlers:
        handler.post_solve = calculate_collision
    return handlers
