# -*- coding: utf-8 -*-
import math
from abc import ABCMeta,abstractmethod
import wx


class Point:
    """基类点
    画线要有点，形状也是由点组成的。所以我们要有基础类——点。它的属性就是它的位置x,y。
    点的位置有绝对位置和相对位置，B点相对A点的位置，就是B.x-A.x，B.y-A.y。因此我们定义点的加减法来计算相对位置。
    另外我们还定义了静态函数dist来计算两个点a，b的距离。
    最后，我们在调用DrawLines函数时需要点位置的元组形式，因此我们定义了属性xy。
    """
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __sub__(self, other):
        return Point(self.x-other.x, self.y-other.y)

    def __add__(self, other):
        return Point(self.x+other.x, self.y-other.y)

    @property
    def xy(self):
        return self.x, self.y

    def __str__(self):
        return 'x={0},y={1}'.format(self.x, self.y)

    def __repr__(self):
        return str(self.xy)

    @staticmethod
    def dist(a, b):
        return math.sqrt((a.x-b.x)**2 + (a.y-b.y)**2)


class Polygon:
    """基类多边形
    形状由点组成。我们用points列表来表示这些点。
    由于我们要画它，而且DrawLines的参数是元组，因此我们用draw_points来返回所需要的参数格式。
    area用来代表形状的面积，不同形状有不同算法，因此用抽象函数实现。（这里的形状默认是凸闭合的形状）两个多边形的比较用面积来比较。
    不同形状可以用不同的颜色线来画，因此加了属性color。
    """
    __metaclass__ = ABCMeta

    def __init__(self, points_list, **kwargs):
        for point in points_list:
            assert isinstance(point, Point), "input must be Point type"
        self.points = points_list[:]
        self.points.append(points_list[0])
        self.color = kwargs.get('color', '#000000')

    def draw_points(self):
        points_xy = []
        for point in self.points:
            points_xy.append(point.xy)
        print(points_xy)
        return tuple(points_xy)

    @abstractmethod
    def area(self):
        raise Exception("not implement")

    def __lt__(self, other):
        assert isinstance(other, Polygon)
        return self.area < other.area


class RectAngle(Polygon):
    """子类矩形
    基于基类Polygon，但初始化的时候更简单，只需要指定长，宽，和起始点即可。另外要记得实现area方法。
    """
    def __init__(self, start_point, w, h, **kwargs):
        self._w = w
        self._h = h
        Polygon.__init__(self, [start_point, start_point+Point(w, 0), start_point+Point(0, h)], **kwargs)

    def area(self):
        return self._w * self._h


class TriAngle(Polygon):
    """子类三角形
    基于基类Polygon，初始化的时候指定三个点。记得判断三个点不在一条直线上。
    三点在一条直线上，报异常
    计算面积可以用海伦公式,S=√p(p-a)(p-b)(p-c), p为半周长（周长的一半）
    """
    def __init__(self, first_point, second_point, third_point, **kwargs):
        self.first_point = first_point
        self.second_point = second_point
        self.third_point = third_point
        for i in range(2):
            assert not (first_point[i] == second_point[i] and first_point[i] == third_point[i]), \
                'Three points in one line'
        Polygon.__init__(self, [first_point, second_point, third_point], **kwargs)

    def area(self):
        a = Point.dist(self.first_point, self.second_point)
        b = Point.dist(self.second_point, self.third_point)
        c = Point.dist(self.first_point, self.third_point)
        p = (a + b + c) / 2
        return math.sqrt(p * (p - a) * (p - b) * (p - c))


class Circle(Polygon):
    """子类圆形
    圆可以看作多边形，当边足够多时，就成了圆形。初始化参数可以是中心点，半径和实现的边数。
    面积pi*r^2
    点的位置可以由半径的sin，cos函数获得。
    """
    def __init__(self, start_point, r, n):
        self.start_point = start_point
        self.r = r
        self.n = n
        self.points = [start_point + Point(0, r)]
        for i in range(n):
            # TODO 将圆的360度分为n份，取每一份的点
            pass

    def area(self):
        return math.pi * self.r * self.r


class Example(wx.Frame):
    def __init__(self, title, shapes):
        super(Example, self).__init__(None, title=title, size=(600, 400))
        self.shapes = shapes

        self.Bind(wx.EVT_PAINT, self.on_paint)

        self.Center()
        self.Show()

    def on_paint(self, e):
        dc = wx.PaintDC(self)

        for shape in self.shapes:
            dc.SetPen(wx.Pen(shape.color))
            dc.DrawLines(shape.draw_points())


if __name__ == '__main__':

    prepare_draws = []

    start_p = Point(50, 60)
    a = RectAngle(start_p, 100, 80, color='#ff0000')
    prepare_draws.append(a)

    for shape in prepare_draws:
        print(shape.area())

    app = wx.App()
    Example('Shapes', prepare_draws)
    app.MainLoop()
