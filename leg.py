import pygame
from pygame.math import Vector2

from color import Color
from utils import *
from entity import Entity
import physics

class Leg():
    def __init__(self, attached_body, length, angle, move_speed, offset=(0, 0), foot_size=5, walk=True):
        self.length = length
        self.attached_body = attached_body
        self.offset = offset
        self.foot_size = foot_size
        
        self.direction = Vector2(angle, 0).normalize()

        self.foot_position = Vector2(
            self.attached_body.get_position().x + (self.direction.x * self.length), 
            self.attached_body.get_position().y + (self.direction.y * self.length)
        )

        self.foot_destination = Vector2(
            self.attached_body.get_position().x + (self.direction.x * self.length), 
            self.attached_body.get_position().y + (self.direction.y * self.length)
        )

        self.angle = angle
        self.move_speed = move_speed

        self.punching = False
        self.walk = walk

        self.attach_position = Vector2(0, 0)

        self.lerping = False

    def render(self, screen):
        #attach_pos = world_to_screen(self.attached_body.physicsget_position() + Vector2(self.get_rel_offset()))

        leg = pygame.draw.line(screen, Color.WHITE, world_to_screen(self.attach_position), world_to_screen(self.foot_position))
        foot = pygame.draw.circle(screen, Color.WHITE, world_to_screen(self.foot_position), self.foot_size, 1)
        attach = pygame.draw.circle(screen, Color.WHITE, world_to_screen(self.attach_position), 2)

        if settings.debug:

            query_info = physics.segment_query_first(self.attach_position, self.attach_position + (self.direction * self.length), 1, category=physics.Categories.WALL)
            pygame.draw.line(screen, Color.RED, world_to_screen(self.attach_position), world_to_screen(self.attach_position + (self.direction * self.length)), 1)

            if query_info is not None:
                pygame.draw.circle(screen, Color.RED, world_to_screen(Vector2(query_info.point)), 4)
            else:
                pygame.draw.circle(screen, Color.BLUE, world_to_screen(Vector2(self.foot_destination)), 4)



    def update(self, dt):

        self.direction = self.attached_body.get_forward().rotate(self.angle)

        if self.punching and self.foot_position.distance_to(self.foot_destination) < 5:
            self.punching = False

        if not self.punching:
            self.move_foot()

        print(self.lerping)
        if self.lerping:
            dist = max(self.foot_position.distance_to(self.foot_destination), 1)
            self.foot_position = self.foot_position.lerp(self.foot_destination, clamp(0, 1, dt * self.move_speed * self.length / dist))
            if dist < 10:
                self.lerping = False

    def move_foot(self):

        self.attach_position = Vector2(self.attached_body.physics_body.position) + Vector2(self.get_rel_offset()) * 1.1

        if self.foot_position.distance_to(self.attach_position) > self.length or self.lerping:
            self.lerping = True
            query_info = physics.segment_query_first(self.attach_position, self.attach_position + (self.direction * self.length), 1, category=physics.Categories.WALL)
            if query_info is None:
                self.foot_destination = Vector2(self.attach_position.x + (self.direction.x * self.length), self.attach_position.y + (self.direction.y * self.length))
            else:
                self.foot_destination = Vector2(query_info.point)

        if not self.walk:
            self.foot_destination = Vector2(self.attach_position.x + (self.direction.x * self.length), self.attach_position.y + (self.direction.y * self.length))

    def get_rel_offset(self):
        forward = self.attached_body.get_forward()
        right = self.attached_body.get_right()
        return (right[0] * self.offset[0] + forward[0] * self.offset[1], right[1] * self.offset[0] + forward[1] * self.offset[1])

    def attach_to(self, body):
        self.attached_body = body

    def punch(self):
        self.punching = True
        self.foot_destination = self.attached_body.get_position() + self.attached_body.get_forward() * self.length * 10