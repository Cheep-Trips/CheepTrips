import unittest

# just to test unittest and Travis CI
class TestSum(unittest.TestCase):

	def test_sum(self):
		self.assertEqual(sum([1, 2, 3]), 6, "Should be 6")

	def test_sum_tuple(self):
		self.assertNotEqual(sum((1, 2, 2)), 6, "This should not be 6.")

if __name__ == '__main__':
	unittest.main()