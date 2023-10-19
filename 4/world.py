import config
from shape import shape_object

class World:
    def __init__(self) -> None:
        self.objects = []
        self.collision_objects = []


    def add_shape(self, position, vertices):
        new_shape = shape_object(position, vertices) 
        self.objects.append(new_shape)
        return new_shape


    def handle_collisions(self):
        for i, shape1 in enumerate(self.collision_objects):
            for j in range(i+1, len(self.collision_objects)):
                shape2 = self.collision_objects[j]
                if shape1 is not shape2 and shape1.handle_collisions(shape2):
                    return self.update()


    def update_objects(self):
        for i in self.objects:
            i.update()


    def update(self):
        self.update_objects()

        for obj in self.objects:
            obj.velocity = [0, 0]


    def draw(self, surface):
        for obj in self.objects:
            obj.draw(surface)

