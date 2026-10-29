import unittest

from app import create_app


class AppFactoryTests(unittest.TestCase):
    def test_app_factory_creates_flask_app(self):
        app = create_app()
        rules = {str(rule) for rule in app.url_map.iter_rules()}

        self.assertEqual(app.name, "app")
        self.assertIn("/register", rules)
        self.assertIn("/login", rules)
        self.assertIn("/profile", rules)
        self.assertIn("/logout", rules)


if __name__ == "__main__":
    unittest.main()
