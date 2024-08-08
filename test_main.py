import unittest
import main


class TestMain(unittest.TestCase):

    def test_check_username_validity(self):
        self.assertEqual(main.check_username_validity("armin"), False)
        self.assertEqual(main.check_username_validity("armin1234"), True)

    def test_check_number_validity(self):
        self.assertEqual(main.check_number_validity("09050793242"), False)
        self.assertEqual(main.check_number_validity("09990793242"), True)

    def test_free_times_check(self):
        self.assertEqual(main.free_times_check("25/08/2024", "20:25"), False)
        self.assertEqual(main.free_times_check("25/08/2024", "20:35"), True)

    def test_reserved_times_check(self):
        self.assertEqual(main.reserved_times_check("08/05/2024", "18:30"), False)
        self.assertEqual(main.reserved_times_check("08/05/2024", "18:32"), True)

    def test_user_login(self):
        self.assertEqual(main.user_login("armin", "1234"), True)
        self.assertEqual(main.user_login("armin", "655665"), False)


if __name__ == "__main__":
    unittest.main()
