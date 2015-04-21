__author__ = 'picklepete'

from time import sleep
from datetime import datetime

import pygame
import picamera
import tweepy
import settings


class WeddingBooth(object):
    """
    The stand always has a default image ("Come and take a photo!")
    1) Wedding guest presses a button on the stand
    2) We immediately display a holding image, counting down from 5...4..3...2...1...
    3) We take a photo of them, leave it on screen for a few seconds.
    4) We immediately display a thank you note, wait a few seconds.
    5) We reset.
    """
    def __init__(self):
        self.screen = self.init_pygame()
        self.camera = picamera.PiCamera()

    def init_pygame(self):
        pygame.init()
        size = (pygame.display.Info().current_w, pygame.display.Info().current_h)
        pygame.display.set_caption('Photo Booth Pics')
        pygame.mouse.set_visible(False)
        return pygame.display.set_mode(size, pygame.FULLSCREEN)

    def display_image(self, path):
        img = pygame.image.load(path)
        img = pygame.transform.scale(img, (640, 480))
        self.screen.blit(img, (0, 0))
        pygame.display.flip()

    def shoot(self):
        filename = '%s.jpg' % datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
        self.camera.start_preview()
        sleep(3)
        self.camera.capture(filename)
        self.camera.stop_preview()
        self.camera.close()
        self.display_image('/home/pi/booth/processing.png')
        sleep(1)
        self.display_image('/home/pi/booth/finished.png')
        sleep(2)
        return filename

    def tweet(self):
        filename = self.shoot()
        auth = tweepy.OAuthHandler(settings.CONSUMER_KEY, settings.CONSUMER_SECRET)
        auth.set_access_token(settings.ACCESS_TOKEN, settings.ACCESS_SECRET)
        api = tweepy.API(auth)
        api.update_with_media(filename=filename, status='New photo from #evanswedding')


booth = WeddingBooth()
booth.tweet()
