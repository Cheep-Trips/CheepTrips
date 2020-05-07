import unittest

# just for testing unittest and Travis CI
class TestSum(unittest.TestCase):
    # should pass
    def test_sum(self):
		self.assertEqual(sum([1, 2, 3]), 6, “Should be 6”)

    # should fail
	def test_sum_tupple(self):
		self.assertEqual(sum([1. 2. 2]), 6, “Should be 6”)

if __name__ == “__main__”:
	unittest.main()
