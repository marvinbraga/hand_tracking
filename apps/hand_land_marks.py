# coding=utf-8
"""
Hand Land Marks Module.
"""
from enum import Enum


class HandLandMarks(Enum):
    """ Identificação de Land Marks. """
    WHIST = 0
    THUMB_CMC = 1
    THUMB_MCP = 2
    THUMB_IP = 3
    THUMB_TIP = 4
    INDEX_FINGER_MPC = 5
    INDEX_FINGER_PIP = 6
    INDEX_FINGER_DIP = 7
    INDEX_FINGER_TIP = 8
    MIDDLE_FINGER_MCP = 9
    MIDDLE_FINGER_PIP = 10
    MIDDLE_FINGER_DIP = 11
    MIDDLE_FINGER_TIP = 12
    RING_FINGER_MCP = 13
    RING_FINGER_PIP = 14
    RING_FINGER_DIP = 15
    RING_FINGER_TIP = 16
    PINK_MCP = 17
    PINK_PIP = 18
    PINK_DIP = 19
    PINK_TIP = 20

    @staticmethod
    def all():
        """ Retorna Lista com todos os atributos. """
        return [HandLandMarks(mark) for mark in range(21)]
