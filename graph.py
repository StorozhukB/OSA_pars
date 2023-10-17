import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle, RegularPolygon
from matplotlib.path import Path
from matplotlib.projections.polar import PolarAxes
from matplotlib.projections import register_projection
from matplotlib.spines import Spine
from matplotlib.transforms import Affine2D

from config import radar_l,radar_p,max_mark,y_hist

mpl.use('agg')

def radar_factory(num_vars, frame='circle'):
    """Create a radar chart with `num_vars` axes.

    This function creates a RadarAxes projection and registers it.

    Parameters
    ----------
    num_vars : int
        Number of variables for radar chart.
    frame : {'circle' | 'polygon'}
        Shape of frame surrounding axes.

    """
    # calculate evenly-spaced axis angles
    theta = np.linspace(0, 2*np.pi, num_vars, endpoint=False)
    
    class RadarTransform(PolarAxes.PolarTransform):
        def transform_path_non_affine(self, path):
            # Paths with non-unit interpolation steps correspond to gridlines,
            # in which case we force interpolation (to defeat PolarTransform's
            # autoconversion to circular arcs).
            if path._interpolation_steps > 1:
                path = path.interpolated(num_vars)
            return Path(self.transform(path.vertices), path.codes)
    class RadarAxes(PolarAxes):
        name = 'radar'
        PolarTransform = RadarTransform
        def __init__(self, *args, **kwargs):
            s=super().__init__(*args, **kwargs)
            # rotate plot such that the first axis is at the top
            self.set_theta_zero_location('N')
        def fill(self, *args, closed=True, **kwargs):
            """Override fill so that line is closed by default"""
            return super().fill(closed=closed, *args, **kwargs)
        def plot(self, *args, **kwargs):
            """Override plot so that line is closed by default"""
            lines = super().plot(*args, **kwargs)
            for line in lines:
                self._close_line(line)
        def _close_line(self, line):
            x, y = line.get_data()
            # FIXME: markers at x[0], y[0] get doubled-up
            if x[0] != x[-1]:
                x = np.concatenate((x, [x[0]]))
                y = np.concatenate((y, [y[0]]))
                line.set_data(x, y)
        def set_varlabels(self, labels):
            self.set_thetagrids(np.degrees(theta), labels,y=-0.17,fontsize='small')
        def _gen_axes_patch(self):
            # The Axes patch must be centered at (0.5, 0.5) and of radius 0.5
            # in axes coordinates.
            if frame == 'circle':
                return Circle((0.5, 0.5), 0.5)
            elif frame == 'polygon':
                return RegularPolygon((0.5, 0.5), num_vars,
                                      radius=.5, edgecolor="k")
            else:
                raise ValueError("unknown value for 'frame': %s" % frame)
        def draw(self, renderer):
            """ Draw. If frame is polygon, make gridlines polygon-shaped """
            if frame == 'polygon':
                gridlines = self.yaxis.get_gridlines()
                for gl in gridlines:
                    gl.get_path()._interpolation_steps = num_vars
            super().draw(renderer)
        def _gen_axes_spines(self):
            if frame == 'circle':
                return super()._gen_axes_spines()
            elif frame == 'polygon':
                # spine_type must be 'left'/'right'/'top'/'bottom'/'circle'.
                spine = Spine(axes=self,
                              spine_type='circle',
                              path=Path.unit_regular_polygon(num_vars))
                # unit_regular_polygon gives a polygon of radius 1 centered at
                # (0, 0) but we want a polygon of radius 0.5 centered at (0.5,
                # 0.5) in axes coordinates.
                spine.set_transform(Affine2D().scale(.5).translate(.5, .5)
                                    + self.transAxes)


                return {'polar': spine}
            else:
                raise ValueError("unknown value for 'frame': %s" % frame)
    register_projection(RadarAxes)
    return theta

def create_radar(type:str,data:list,path:str,color:tuple=(0,0,1)):
    """
    Creae radar graph of given type:"l"/"p"(lector/practice)
    using given data list
    creates image .png in given path (path include name of file without .png)
    you may change color of data using color param
    """
    sign=''
    if type=="l":
        sign=radar_l
    elif type=="p":
        sign=radar_p
    if not sign:
        raise ValueError("Incorect type, use l/p to choose type of graph")
    n=len(sign)
    theta=radar_factory(n,frame='polygon')
    fig, ax = plt.subplots(figsize=(7, 6), subplot_kw=dict(projection='radar'))
    fig.subplots_adjust(right=0.9,top=0.85, bottom=0.15)
    ax.set_rgrids([1,2,3,4,5],["","","","",""])
    plt.ylim(0, 5)
    line = ax.plot(theta, data,color=color)
    ax.fill(theta, data, alpha=0.25, label='_nolegend_',color=color)
    ax.set_varlabels(['']*n)
    ax.set_varlabels(sign)
    fig.savefig(path,transparent=True)
    plt.close()

def create_hist(data:list,path:str,color:tuple=(0,0,1),hist_name:str=""):
    """
    Cheate histogram out of given data list
    creates image .png in given path (path include name of file without .png)
    you may change color of data using color param
    also name of histogram may be set by name param
    """
    plt.figure(figsize=(7,6))
    plt.bar([i+1 for i in range(max_mark)],data,color=color)
    plt.grid(alpha=0.25)
    fig=plt.gcf()
    plt.xlabel(hist_name)

    plt.ylabel(y_hist)
    plt.gca().yaxis.label.set(rotation='horizontal', ha='right');
    fig.axes[0].yaxis.set_label_coords(0,1.02)

    fig.savefig(path,transparent=True)
    plt.close()
    pass



