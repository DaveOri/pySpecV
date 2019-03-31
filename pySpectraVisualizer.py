import tkinter as tki  # for python2 is Tkinter
import tkinter.filedialog
import netCDF4
import matplotlib.pyplot as plt
import matplotlib.dates as md
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import pandas as pd

#dfmt = '%Y%m%d %H%m'
dfmt = '%H:%M:%S'
#xfmt = md.DateFormatter(dfmt)
xfmt = md.DateFormatter('%H')

def str2num(string):
  try:
    return float(string)
  except:
    return None

def str2dat(string):
  date = pd.to_datetime(string)
  if pd.isnull(date):
    return None
  return date

class Application(tki.Frame):
  def __init__(self):
    print(screen_width, screen_height)
    super().__init__()
    self.master.title("pySpecralVisualizer")
    self.pack(fill=tki.BOTH, expand=True)
    self.frameplots = tki.Frame(self)
    self.frameplots.pack(fill=tki.BOTH, expand=True)
    self.framelimits = tki.Frame(self)
    self.framelimits.pack(fill=tki.X)
    self.framebuttons = tki.Frame(self)
    self.framebuttons.pack(fill=tki.X)
    self.initControlFrame()
    self.initVisualFrame()

  def initControlFrame(self):
    
    self.master.bind("<Button-1>", self.leftClick)
    self.master.bind("<Button-3>", self.rightClick)

    self.button_open = tki.Button(self.framebuttons,
                                  text="Open file...",
                                  command=self.openfile)
    self.button_open.pack(side="left")

    self.frequencies = []
    self.frequency = tki.StringVar(self.master)
    self.frequency.set('frequency [GHz]')
    
    self.varnames = []
    self.xcoord = tki.StringVar(self.master)
    self.xcoord.set('X coordinates')
    
    self.y_coords = []
    self.ycoord = tki.StringVar(self.master)
    self.ycoord.set('Y coordinates')

    self.z_coords = []
    self.zcoord = tki.StringVar(self.master)
    self.zcoord.set('Z coordinates')
    
    #self.frequency.trace('w', self._print_state)


    self.menu_frequencies = tki.OptionMenu(self.framebuttons,
                                           variable=self.frequency,
                                           value='frequency [GHz]',
                                           *self.frequencies)
    self.menu_frequencies.pack(side="left")#.grid(row=0, column=0)
    # self.menu_xcoord = tki.OptionMenu(self.framebuttons,
    #                                   variable=self.xcoord,
    #                                   value='X coordinates',
    #                                   *self.varnames)
    # self.menu_xcoord.pack(side="left")#.grid(row=0, column=0)
    # self.menu_ycoord = tki.OptionMenu(self.framebuttons,
    #                                   variable=self.ycoord,
    #                                   value='Y coordinates',
    #                                   *self.varnames)
    # self.menu_ycoord.pack(side="left")#.grid(row=0, column=0)
    self.menu_zcoord = tki.OptionMenu(self.framebuttons,
                                      variable=self.zcoord,
                                      value='Z coordinates',
                                      *self.varnames)
    self.menu_zcoord.pack(side="left")#.grid(row=0, column=0)


    # self.button_print = tki.Button(self.framebuttons,
    #                                text="print frequency",
    #                                command=self._print_state)
    # self.button_print.pack(side="left")#.grid(row=0, column=0)

    self.hlimLabel = tki.Label(self.framelimits, text="height lim")
    self.hlimLabel.pack(side='left')
    self.hlim0 = tki.Entry(self.framelimits)
    self.hlim0.pack(side='left')
    self.hlim1 = tki.Entry(self.framelimits)
    self.hlim1.pack(side='left')

    self.tlimLabel = tki.Label(self.framelimits, text="time lim")
    self.tlimLabel.pack(side='left')
    self.tlim0 = tki.Entry(self.framelimits)
    self.tlim0.pack(side='left')
    self.tlim1 = tki.Entry(self.framelimits)
    self.tlim1.pack(side='left')

    self.vlimLabel = tki.Label(self.framelimits, text="value lim")
    self.vlimLabel.pack(side='left')
    self.vlim0 = tki.Entry(self.framelimits)
    self.vlim0.pack(side='left')
    self.vlim1 = tki.Entry(self.framelimits)
    self.vlim1.pack(side='left')

    self.button_draw = tki.Button(self.framebuttons,
                                  text="Draw",
                                  command=self._drawTimeHeight)
    self.button_draw.pack(side="left")#.grid(row=0, column=0)

  def initVisualFrame(self):
    self.master.update()
    dpi=100.
    fpw = self.frameplots.winfo_width()/dpi
    fph = self.frameplots.winfo_height()/dpi
    figTimeHeight = plt.figure(figsize=(fpw*0.75,fph*0.5), dpi=dpi,
                               linewidth=.01, edgecolor='k')
    self.axTH=plt.gca()
    figTimeSeries = plt.figure(figsize=(fpw*0.25,fph*0.5), dpi=dpi,
                               linewidth=.01, edgecolor='k')
    self.axTS=plt.gca()
    figProfile = plt.figure(figsize=(fpw*0.25,fph*0.5), dpi=dpi,
                            linewidth=.01, edgecolor='k')
    self.axPr=plt.gca()
    figSpectroGram = plt.figure(figsize=(fpw*0.25,fph*0.999), dpi=dpi,
                                linewidth=.01, edgecolor='k')
    self.axSG=plt.gca()
    figSpectrum = plt.figure(figsize=(fpw*0.25,fph*0.5), dpi=dpi,
                             linewidth=.01, edgecolor='k')
    self.axSp=plt.gca()

    self.canvasTH = FigureCanvasTkAgg(figTimeHeight, master=self.frameplots)
    self.canvasTS = FigureCanvasTkAgg(figTimeSeries, master=self.frameplots)
    self.canvasPr = FigureCanvasTkAgg(figProfile, master=self.frameplots)
    self.canvasSG = FigureCanvasTkAgg(figSpectroGram, master=self.frameplots)
    self.canvasSp = FigureCanvasTkAgg(figSpectrum, master=self.frameplots)

    self.canvasTH.get_tk_widget().grid(row=0, column=0, columnspan=3,
                                       sticky=tki.E+tki.W+tki.S+tki.N)
    self.canvasTS.get_tk_widget().grid(row=1, column=0,
                                       sticky=tki.E+tki.W+tki.S+tki.N)
    self.canvasPr.get_tk_widget().grid(row=1, column=1,
                                       sticky=tki.E+tki.W+tki.S+tki.N)
    self.canvasSG.get_tk_widget().grid(row=0, column=3, rowspan=2,
                                       sticky=tki.E+tki.W+tki.S+tki.N)
    self.canvasSp.get_tk_widget().grid(row=1, column=2,
                                       sticky=tki.E+tki.W+tki.S+tki.N)
    
    self.canvasTH.mpl_connect('button_press_event', self.callTH)
    self.canvasTS.mpl_connect('button_press_event', self.callTS)
    self.canvasPr.mpl_connect('button_press_event', self.callPr)
    self.canvasSG.mpl_connect('button_press_event', self.callSG)
    self.canvasSp.mpl_connect('button_press_event', self.callSp)


  def callTH(self, event):
    print('canvas TimeHeight', event.x, event.y)
    dx, dy = self.axTH.transData.inverted().transform((event.x, event.y))
    print('data TH', dx, dy)
    self._drawTimeHeight()
    self.axTH.axvline(dx)
    self.axTH.axhline(dy)
    self.canvasTH.draw()
    self._drawSpectrum(dx,dy)
    self._drawTimeSeries(dy)
    self._drawProfile(dx)
    self._drawSpectroGram(dx)

  def callTS(self, event):
    print('canvas TimeSeries', event.x, event.y)
    dx, dy = self.axTS.transData.inverted().transform((event.x, event.y))
    print('data TS', dx, dy)

  def callPr(self, event):
    print('canvas Profile', event.x, event.y)
    dx, dy = self.axPr.transData.inverted().transform((event.x, event.y))
    print('data Pr', dx, dy)

  def callSG(self, event):
    print('canvas SpectroGram', event.x, event.y)
    dx, dy = self.axSG.transData.inverted().transform((event.x, event.y))
    print('data SG', dx, dy)

  def callSp(self, event):
    print('canvas Spectrum', event.x, event.y)
    dx, dy = self.axSp.transData.inverted().transform((event.x, event.y))
    print('data Sp', dx, dy)


  def leftClick(self, event):
    print('leftclick', event.x, event.y)
    #self._draw_main()

  def middleClick(self, event):
    print('middleclick')

  def rightClick(self, event):
    print('rightclick', event.x, event.y)


  def _drawTimeHeight(self):
    xlim = (str2dat(self.tlim0.get()), str2dat(self.tlim1.get()))
    ylim = (str2num(self.hlim0.get()), str2num(self.hlim1.get()))
    vmin, vmax = str2num(self.vlim0.get()), str2num(self.vlim1.get())
    try:
      self.cbTH.remove()
    except:
      pass
    self.axTH.clear()
    fidx = np.where(self.variables['frequency'][:]==float(self.frequency.get()))
    H = self.variables['height'][0,0,:]
    tt = pd.to_datetime(self.variables['datatime'][:,0], unit='s')
    var = self.variables[self.zcoord.get()]
    X = var[:,0,:,fidx[0][0],0,0].T
    mesh = self.axTH.pcolormesh(tt,H,X, vmin=vmin, vmax=vmax)
    self.cbTH = plt.colorbar(mesh, label=var.name + ' ' + var.units,
                             ax=self.axTH, orientation='vertical')
    self.axTH.set_xlim(xlim)
    self.axTH.set_ylim(ylim)
    self.axTH.xaxis.set_major_formatter(xfmt)
    self.axTH.set_xlabel('time')
    self.axTH.set_ylabel('height   [m]')
    self.axTH.set_title('Basetime= '+tt[0].strftime('%Y-%m-%d %H:%M'))
    #plt.tight_layout()
    self.canvasTH.draw()

  def _drawTimeSeries(self, dy):
    xlim = (str2dat(self.tlim0.get()), str2dat(self.tlim1.get()))
    ylim = (str2num(self.vlim0.get()), str2num(self.vlim1.get()))
    self.axTS.clear()
    fidx = np.where(self.variables['frequency'][:]==float(self.frequency.get()))
    H = self.variables['height'][0,0,:]
    Hidx = np.argmin(np.abs(H-dy))
    tt = pd.to_datetime(self.variables['datatime'][:,0], unit='s')
    var = self.variables[self.zcoord.get()]
    X = var[:,0,Hidx,fidx[0][0],0,0]
    if X.mask.prod():
      X = X.data
    self.axTS.plot(tt, X, label='Height= '+str(dy))
    self.axTS.legend()
    self.axTS.grid()
    self.axTS.xaxis.set_major_formatter(xfmt)
    self.axTS.set_xlim(xlim)
    self.axTS.set_ylim(ylim)
    self.axTS.set_xlabel('time')
    self.axTS.set_ylabel(var.name + ' ' + var.units)
    self.axTS.set_title('Basetime= '+tt[0].strftime('%Y-%m-%d %H:%M'))
    self.canvasTS.draw()

  def _drawProfile(self, dx):
    ylim = (str2num(self.hlim0.get()), str2num(self.hlim1.get()))
    xlim = (str2num(self.vlim0.get()), str2num(self.vlim1.get()))
    self.axPr.clear()
    fidx = np.where(self.variables['frequency'][:]==float(self.frequency.get()))
    H = self.variables['height'][0,0,:]
    tt = pd.to_datetime(self.variables['datatime'][:,0], unit='s')
    Tidx = np.argmin(np.abs(tt-md.num2date(dx).replace(tzinfo=None)).to_pytimedelta())
    print(Tidx)
    var = self.variables[self.zcoord.get()]
    X = var[Tidx,0,:,fidx[0][0],0,0]
    self.axPr.plot(X, H, label='Time= '+(md.num2date(dx)).strftime(dfmt))
    self.axPr.legend()
    self.axPr.grid()
    self.axPr.set_xlim(xlim)
    self.axPr.set_ylim(ylim)
    self.axPr.set_ylabel('height   [m]')
    self.axPr.set_xlabel(var.name + ' ' + var.units)
    self.canvasPr.draw()

  def _drawSpectroGram(self, dx):
    ylim = (str2num(self.hlim0.get()), str2num(self.hlim1.get()))
    fidx = np.where(self.variables['frequency'][:]==float(self.frequency.get()))
    H = self.variables['height'][0,0,:]
    tt = pd.to_datetime(self.variables['datatime'][:,0], unit='s')
    Tidx = np.argmin(np.abs(tt-md.num2date(dx).replace(tzinfo=None)).to_pytimedelta())
    try:
      self.cbSG.remove()
    except:
      pass
    self.axSG.clear()
    if 'Radar_Spectrum' in self.variables.keys():
      Xvar = self.variables['Radar_Velocity']
      Yvar = self.variables['Radar_Spectrum']
      X = Xvar[fidx[0][0],:]
      Y = Yvar[Tidx,0,:,fidx[0][0],0,:]
      mesh = self.axSG.pcolormesh(X,H,Y, vmin=None, vmax=None)
      self.cbSG = plt.colorbar(mesh, label=Yvar.name + ' ' + Yvar.units,
                               ax=self.axSG, orientation='vertical')
      self.axSG.set_ylabel('height   [m]')
      self.axSG.set_xlabel(Xvar.name + ' ' + Xvar.units)
    self.axSG.set_ylim(ylim)
    self.canvasSG.draw()

  def _drawSpectrum(self, dx, dy):
    fidx = np.where(self.variables['frequency'][:]==float(self.frequency.get()))
    H = self.variables['height'][0,0,:]
    Hidx = np.argmin(np.abs(H-dy))
    tt = pd.to_datetime(self.variables['datatime'][:,0], unit='s')
    Tidx = np.argmin(np.abs(tt-md.num2date(dx).replace(tzinfo=None)).to_pytimedelta())
    if 'Radar_Spectrum' in self.variables.keys():
      Xvar = self.variables['Radar_Velocity']
      Yvar = self.variables['Radar_Spectrum']
      X = Xvar[fidx[0][0],:]
      Y = Yvar[Tidx,0,Hidx,fidx[0][0],0,:]
    else:
      X = 0
      Y = 0
    self.axSp.clear()
    self.axSp.plot(X,Y)
    self.axSp.set_ylabel(Yvar.name + ' ' + Yvar.units)
    self.axSp.set_xlabel(Xvar.name + ' ' + Xvar.units)
    self.canvasSp.draw()


  def openfile(self):
    filetypes = (("netCDF files","*.nc"), ("all files","*.*"))
    self.filename = tki.filedialog.askopenfilename(initialdir="./",
                                                   title="Select file",
                                                   filetypes=filetypes)
    data = netCDF4.Dataset(self.filename, 'r')
    self.variables = data.variables
    dimensions = data.dimensions
    self.frequencies = list(map(str,self.variables['frequency'][:]))
    self.menu_frequencies['menu'].delete(0,'end')
    for f in self.frequencies:
      setFrequency = lambda value=f: self.frequency.set(value)
      self.menu_frequencies.children['menu'].add_command(label=f,
                                                         command=setFrequency)
    self.frequency.set('frequency [GHz]')

    self.varnames = list(self.variables.keys())
    #self.menu_xcoord['menu'].delete(0,'end')
    #self.menu_ycoord['menu'].delete(0,'end')
    self.menu_zcoord['menu'].delete(0,'end')
    validdim = ('grid_x','grid_y','heightbins','frequency','radar_polarisation','radar_peak_number')
    for name in self.varnames:
      if self.variables[name].dimensions == validdim:
        print(name)
        # setCoord = lambda value=name: self.xcoord.set(value)
        # self.menu_xcoord.children['menu'].add_command(label=name,
        #                                               command=setCoord)
        # setCoord = lambda value=name: self.ycoord.set(value)
        # self.menu_ycoord.children['menu'].add_command(label=name,
        #                                               command=setCoord)

        setCoord = lambda value=name: self.zcoord.set(value)
        self.menu_zcoord.children['menu'].add_command(label=name,
                                                      command=setCoord)
    # self.xcoord.set('X coordinates')
    # self.ycoord.set('Y coordinates')
    self.zcoord.set('Z coordinates')


  def _print_state(self, *args):
    print('frequency ', self.frequency.get())


root = tki.Tk()
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.geometry(str(screen_width)+'x'+str(screen_height) + "+0+0")
app = Application()

def quit_root(): # This is needed because of the freaking pyplot childs
  plt.close('all')
  root.destroy()
root.protocol("WM_DELETE_WINDOW", quit_root)

root.mainloop()

#filetypes = (("jpeg files","*.jpg"),("all files","*.*"))
#root.filename = filedialog.asksaveasfilename(initialdir="./",
#                                          title = "Select file",
#                                          filetypes = filetypes)
#print (root.filename)

