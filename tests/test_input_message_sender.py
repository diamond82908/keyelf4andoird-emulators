import unittest
import sys
import io
from src.input_message_sender import InputMessageSender

class TestInputMessageSender(unittest.TestCase):
    sender : InputMessageSender
    virtual_adb_stdin: io.TextIOWrapper
    virtual_out: io.TextIOWrapper
    @classmethod
    def setUpClass(cls):
        cls.sender = InputMessageSender()
        cls.virtual_adb_stdin = open("temp", mode="wb")
        cls.virtual_out = open("temp", mode="r")

    @classmethod
    def tearDownClass(cls):
        cls.virtual_adb_stdin.close()
    
    def setUp(self):
        self.sender.reset()

    def test_init_and_reset(self):
        new_sender = InputMessageSender()
        self.assertIsNone(new_sender._adb_stdin)
    
    def test_bind(self):
        self.sender.bind(self.virtual_adb_stdin)
        self.assertIs(self.sender._adb_stdin, self.virtual_adb_stdin)

    def test_check_bind_exception(self):
        try:
            with self.assertRaises(Exception):
                self.sender.send_tap_message(0, 0)
        except Exception:
            pass
        try:
            with self.assertRaises(Exception):
                self.sender.send_swipe_message(0, 0, 0, 0, 0)
        except Exception:
            pass
    
    def test_bind_exception(self):
        with self.assertRaises(ValueError):
            self.sender.bind(sys.__stdin__)
    
    def test_swipe(self):
        self.sender.bind(self.virtual_adb_stdin)
        self.sender.send_swipe_message(0, 0, 0, 0, 0)
        expected_result = "input swipe 0 0 0 0 0\n"
        self.assertEqual(self.virtual_out.readline(), expected_result)

    def test_tap(self):
        self.sender.bind(self.virtual_adb_stdin)
        self.sender.send_tap_message(0, 0)
        expected_result = "input tap 0 0\n"
        self.assertEqual(self.virtual_out.readline(), expected_result)