from cie1931 import cie1931_512


class RGB:
    def __init__(self):
        self.R = 0
        self.G = 0
        self.B = 0

    # def __setattr__(self, name, value):
        # super().__setattr__(self, name, cie1931_512[value])

    def copy(self, source):
        self.R = source.R
        self.G = source.G
        self.B = source.B


class HSV:
    def __init__(self, hue=0, saturation=1.0, value=1.0):
        self.Hue = hue
        self.Saturation = saturation
        self.Value = value

    def toRGB(self):
        rgb = RGB()
        # print(self.Hue, self.Saturation, self.Value)
        R, G, B = (self._hsv_to_rgb(
            self.Hue, self.Saturation, self.Value))
        rgb.R = int(cie1931_512[(round(R * 510))]/2)
        rgb.G = int(cie1931_512[(round(G * 510))]/2)
        rgb.B = int(cie1931_512[(round(B * 510))]/2)
        return rgb

    def _hsv_to_rgb(self, h, s, v):
        if s == 0.0:
            return v, v, v
        i = int(h*6.0) # XXX assume int() truncates!
        f = (h*6.0) - i
        p = v*(1.0 - s)
        q = v*(1.0 - s*f)
        t = v*(1.0 - s*(1.0-f))
        i = i%6
        if i == 0:
            return v, t, p
        if i == 1:
            return q, v, p
        if i == 2:
            return p, v, t
        if i == 3:
            return p, q, v
        if i == 4:
            return t, p, v
        if i == 5:
            return v, p, q
        # Cannot get here