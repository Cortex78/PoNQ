import unittest
from unittest.mock import MagicMock
import sys

# To avoid ModuleNotFoundError during import of src.utils.mesh_tools,
# we temporarily mock the missing dependencies.
_original_modules = sys.modules.copy()
_mock_modules = [
    "igl", "numpy", "trimesh", "sklearn", "sklearn.neighbors",
    "skimage", "skimage.measure", "scipy", "scipy.spatial"
]
for module in _mock_modules:
    sys.modules[module] = MagicMock()

try:
    from src.utils.mesh_tools import mesh_chamfer, mesh_hausdorff
finally:
    # Restore original sys.modules immediately after import to minimize global side-effects.
    for module in _mock_modules:
        if module in _original_modules:
            sys.modules[module] = _original_modules[module]
        else:
            del sys.modules[module]

class MockArray:
    """Simulates a numpy-like array for basic arithmetic used in mesh_tools."""
    def __init__(self, data):
        self.data = data

    def __pow__(self, other):
        return MockArray([x**other for x in self.data])

    def mean(self):
        return sum(self.data) / len(self.data) if self.data else 0.0

    def max(self):
        return max(self.data) if self.data else 0.0

class TestMeshMetrics(unittest.TestCase):
    def setUp(self):
        # Access the 'igl' mock that was used by mesh_tools
        import src.utils.mesh_tools as mesh_tools
        self.mock_igl = mesh_tools.igl

    def test_mesh_chamfer_basic(self):
        # d1 = [1.0, 2.0], d1^2 = [1.0, 4.0], mean = 2.5
        # d2 = [3.0, 4.0], d2^2 = [9.0, 16.0], mean = 12.5
        # Expected: 2.5 + 12.5 = 15.0
        d1 = MockArray([1.0, 2.0])
        d2 = MockArray([3.0, 4.0])
        self.mock_igl.signed_distance.side_effect = [(d1, None, None), (d2, None, None)]

        result = mesh_chamfer(None, None, None, None)
        self.assertEqual(result, 15.0)

    def test_mesh_chamfer_zeros(self):
        d1 = MockArray([0.0, 0.0])
        d2 = MockArray([0.0, 0.0, 0.0])
        self.mock_igl.signed_distance.side_effect = [(d1, None, None), (d2, None, None)]

        result = mesh_chamfer(None, None, None, None)
        self.assertEqual(result, 0.0)

    def test_mesh_chamfer_single_element(self):
        # d1 = [2.0], d1^2 = 4.0, mean = 4.0
        # d2 = [4.0], d2^2 = 16.0, mean = 16.0
        # Expected: 4.0 + 16.0 = 20.0
        d1 = MockArray([2.0])
        d2 = MockArray([4.0])
        self.mock_igl.signed_distance.side_effect = [(d1, None, None), (d2, None, None)]

        result = mesh_chamfer(None, None, None, None)
        self.assertEqual(result, 20.0)

    def test_mesh_hausdorff_basic(self):
        # d1 = [1.0, 5.0], max = 5.0
        # d2 = [2.0, 4.0], max = 4.0
        # Expected: max(5.0, 4.0) = 5.0
        d1 = MockArray([1.0, 5.0])
        d2 = MockArray([2.0, 4.0])
        self.mock_igl.signed_distance.side_effect = [(d1, None, None), (d2, None, None)]

        result = mesh_hausdorff(None, None, None, None)
        self.assertEqual(result, 5.0)

    def test_mesh_hausdorff_zeros(self):
        d1 = MockArray([0.0])
        d2 = MockArray([0.0])
        self.mock_igl.signed_distance.side_effect = [(d1, None, None), (d2, None, None)]

        result = mesh_hausdorff(None, None, None, None)
        self.assertEqual(result, 0.0)

if __name__ == "__main__":
    unittest.main()
