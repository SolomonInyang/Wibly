from pygame.math import Vector2
import random

from creature import Creature
from body import Body

class Enemy(Creature):
    def __init__(self, position, rotation=90, scale=1, size=50, speed=100, turn_speed=5):
        Creature.__init__(self, position, rotation, scale, size, speed, turn_speed)

        self.head = Body(self, self.position, self.rotation, self.size, self.size, head=True)

        self.bodies = [
            self.head
        ]

        for i in range(4):
            b = Body(self, self.position, self.rotation, self.size, self.size/2)
            b.attach_to(self.bodies[i])
            self.bodies.append(b)

        for body in self.bodies:
            body.add_leg(self.size, 15, 20, (body.width/2, 0))
            body.add_leg(self.size, -15, 20, (-body.width/2, 0))

        self.wander_time = 2
        self.timer = 0

        self.displacement = Vector2(0, 0)

    def update(self, dt):
        self.timer += dt

        if self.timer >= self.wander_time:
            self.timer = 0
            if random.random() > 0.5:
                self.displacement = Vector2(random.random()-0.5, random.random()-0.5).normalize()
            else:
                self.displacement = Vector2(0, 0)

        self.move_body(dt, self.displacement)