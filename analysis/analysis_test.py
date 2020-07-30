import unittest
import pandas as pd
import analysis_tools as analysis
import matplotlib.pyplot as plt


class TestStringMethods(unittest.TestCase):

    def setUp(self):
        xs = [10, 30, 110, -20, 50, 50, 30, 80, 99, 10]
        ys = [20, 60, 110, -40, 100, 100, 60, 160, 200, 20]
        ts = [0, 1000, 2000, 3000, 8000, 9000, 10000, 11000, 12000, 13000]
        
        self.dirty_tracking_data = pd.DataFrame({"x": xs, "y": ys, "t": ts})

    def test_cleaning(self):
        clean_tracking_data = analysis.clean_tracking_data(self.dirty_tracking_data)
        answer = self.dirty_tracking_data[[True, True, True, False, True, True, True, True, True, False]]
        self.assertTrue(all(answer == clean_tracking_data))

    def test_frac_conv(self):
        frac_coords = analysis.convert_to_frac_coords(self.dirty_tracking_data, (0, 100), (0, 200))
        self.assertEqual(frac_coords["x"][0], 0.1)
        self.assertEqual(frac_coords["y"][0], 0.1)
        self.assertEqual(frac_coords["x"][9], 0.1)

    def test_mid_splats(self):
        heatmap = analysis.calc_heatmap(pd.DataFrame([{"x": 0.5, "y": 0.5, "t": 0},
                                                      {"x": 0.4, "y": 0.4, "t": 1}]),
                                        (100, 100), (5./100., 3./100.))

    def test_lower_edge_splats(self):
        heatmap = analysis.calc_heatmap(pd.DataFrame([{"x": 0.0, "y": 0.5, "t": 0},
                                                      {"x": 0.4, "y": 0.0, "t": 1},
                                                      {"x": 0.0, "y": 0.0, "t": 2}]),
                                        (100, 100), (5./100., 3./100.))

    def test_higher_edge_splats(self):
        heatmap = analysis.calc_heatmap(pd.DataFrame([{"x": 1.0, "y": 0.5, "t": 0},
                                                      {"x": 0.4, "y": 1.0, "t": 1},
                                                      {"x": 1.0, "y": 1.0, "t": 2}]),
                                        (100, 100), (5./100., 3./100.))

    def test_negative_splats(self):
        heatmap = analysis.calc_heatmap(pd.DataFrame([{"x": -1.0, "y": 0.5, "t": 0},
                                                      {"x": 0.4, "y": -1.0, "t": 1},
                                                      {"x": -1.0, "y": 1.0, "t": 2}]),
                                        (100, 100), (5./100., 3./100.))

    def test_positive_edge_splats(self):
        heatmap = analysis.calc_heatmap(pd.DataFrame([{"x": 2.0, "y": 0.5, "t": 0},
                                                      {"x": 0.4, "y": 2.0, "t": 1},
                                                      {"x": 2.0, "y": 2.0, "t": 2}]),
                                        (100, 100), (5./100., 3./100.))


if __name__ == '__main__':
    unittest.main()