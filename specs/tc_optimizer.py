import unittest

class TestOptimization(unittest.TestCase):

    def test_does_not_error(self):

        from FireGirlOptimizer import FireGirlPolicyOptimizer
        from FireGirlPolicy import FireGirlPolicy

        FGPO = FireGirlPolicyOptimizer()
        FGPO.createFireGirlPathways(5,5)
        b = [0,0,0,0,0,0,0,0,0,0,0]
        policy = FireGirlPolicy(b)
        FGPO.setPolicy(policy)

        self.assertIsNotNone("Hello World")

if __name__ == '__main__':
    unittest.main()
