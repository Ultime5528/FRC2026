from typing import List


class LinearInterpolator:
    def __init__(self, point_x: List[float], point_y: List[float]):
        self._points_x = point_x
        self._points_y = point_y
        self._points = list(zip(point_x, point_y))

    def setPointsX(self, x_points: List[float]):
        self._points_x = x_points
        self._points = list(zip(x_points, self._points_y))

    def setPointsY(self, y_points: List[float]):
        self._points_y = y_points
        self._points = list(zip(self._points_x, y_points))

    def getPointsX(self) -> List[float]:
        return self._points_x

    def getPointsY(self) -> List[float]:
        return self._points_y

    def interpolate(self, x):
        i = 1

        if x <= self._points[0][0]:
            return self._points[0][1]

        while i < len(self._points) and x > self._points[i][0]:
            i += 1

        if i == len(self._points):
            return self._points[i - 1][1]

        return (self._points[i][1] - self._points[i - 1][1]) / (
            self._points[i][0] - self._points[i - 1][0]
        ) * (x - self._points[i - 1][0]) + self._points[i - 1][1]
