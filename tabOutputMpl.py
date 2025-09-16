from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib as mpl


class PlotCanvas(FigureCanvas):
    def __init__(self, parent=None):
        self.fig = Figure(figsize=(5, 4), dpi=100)
        self.ax = self.fig.add_subplot(111)
        super().__init__(self.fig)
        self.setParent(parent)
        self.fig.patch.set_alpha(0.0)
        # self.fig.tight_layout()
        self.ax.set_facecolor((0.6, 0.6, 0.6, 1))
        mpl.rcParams['text.color'] = "white"
        mpl.rcParams['axes.labelcolor'] = "white"
        mpl.rcParams['xtick.color'] = "white"
        mpl.rcParams['ytick.color'] = "white"
        for spine in self.ax.spines.values():
            spine.set_color("gray")

    def plot_I_P(self, heatfluxi, dTs, showComponents):
        self.ax.clear()
        I = heatfluxi['I']
        P_Ress = heatfluxi['P_Results']
        P_Pes = heatfluxi['P_Peltiers']
        P_J = heatfluxi['P_Joule']
        P_Ls = heatfluxi['P_HeatConducts']
        if len(dTs) == 1:
            self.ax.plot(I, P_Ress[0], label=f"$P_{{CS}}$ ($\Delta$T={dTs[0]} K)", c='green', lw=1.5)
            if showComponents:
                self.ax.plot(I, P_Pes[0], label=f"$P_{{Pe}}$ ($\Delta T=${dTs[0]} K)", c='blue', lw=1)
                self.ax.plot(I, P_J, label=f"$P_{{J}}$ ($\Delta T=${dTs[0]} K)", c='orange', lw=1)
                self.ax.plot(I, P_Ls[0], label=f"$P_{{\lambda}}$ ($\Delta T=${dTs[0]} K)", c='red', lw=1)

        elif len(dTs) == 2:
            self.ax.plot(I, P_Ress[0], label=f"$P_{{CS}}$ ($\Delta$T={dTs[0]} K)", c='green', lw=1.5)
            self.ax.plot(I, P_Ress[1], label=f"$P_{{CS}}$ ($\Delta$T={dTs[1]} K)", c='green', lw=1.5, ls='--')
            if showComponents:
                self.ax.plot(I, P_Pes[0], label=f"$P_{{Pe}}$ ($\Delta T=${dTs[0]} K)", c='blue', lw=1)
                self.ax.plot(I, P_Pes[1], label=f"$P_{{Pe}}$ ($\Delta T=${dTs[1]} K)", c='blue', lw=1, ls='--')
                self.ax.plot(I, P_J, label=f"$P_{{J}}$ ($\Delta T=${dTs[0]},{dTs[1]} K)", c='orange', lw=1)
                self.ax.plot(I, P_Ls[0], label=f"$P_{{\lambda}}$ ($\Delta T=${dTs[0]} K)", c='red', lw=1)
                self.ax.plot(I, P_Ls[1], label=f"$P_{{\lambda}}$ ($\Delta T=${dTs[1]} K)", c='red', lw=1, ls='--')

        elif len(dTs) == 3:
            self.ax.plot(I, P_Ress[0], label=f"$P_{{CS}}$ ($\Delta$T={dTs[0]} K)", c='green', lw=1.5)
            self.ax.plot(I, P_Ress[1], label=f"$P_{{CS}}$ ($\Delta$T={dTs[1]} K)", c='green', lw=1.5, ls='--')
            self.ax.plot(I, P_Ress[2], label=f"$P_{{CS}}$ ($\Delta$T={dTs[2]} K)", c='green', lw=1.5, ls=':')
            if showComponents:
                self.ax.plot(I, P_Pes[0], label=f"$P_{{Pe}}$ ($\Delta T=${dTs[0]} K)", c='blue', lw=1)
                self.ax.plot(I, P_Pes[1], label=f"$P_{{Pe}}$ ($\Delta T=${dTs[1]} K)", c='blue', lw=1, ls='--')
                self.ax.plot(I, P_Pes[2], label=f"$P_{{Pe}}$ ($\Delta T=${dTs[2]} K)", c='blue', lw=1, ls=':' )
                self.ax.plot(I, P_J, label=f"$P_{{J}}$ ($\Delta T=${dTs[0]},{dTs[1]},{dTs[2]} K)", c='orange', lw=1)
                self.ax.plot(I, P_Ls[0], label=f"$P_{{\lambda}}$ ($\Delta T=${dTs[0]} K)", c='red', lw=1)
                self.ax.plot(I, P_Ls[1], label=f"$P_{{\lambda}}$ ($\Delta T=${dTs[1]} K)", c='red', lw=1, ls='--')
                self.ax.plot(I, P_Ls[2], label=f"$P_{{\lambda}}$ ($\Delta T=${dTs[2]} K)", c='red', lw=1, ls=':' )

        elif len(dTs) == 4:
            self.ax.plot(I, P_Ress[0], label=f"$P_{{CS}}$ ($\Delta$T={dTs[0]} K)", c='green', lw=1.5)
            self.ax.plot(I, P_Ress[1], label=f"$P_{{CS}}$ ($\Delta$T={dTs[1]} K)", c='green', lw=1.5, ls='--')
            self.ax.plot(I, P_Ress[2], label=f"$P_{{CS}}$ ($\Delta$T={dTs[2]} K)", c='green', lw=1.5, ls=':' )
            self.ax.plot(I, P_Ress[3], label=f"$P_{{CS}}$ ($\Delta$T={dTs[3]} K)", c='green', lw=1.5, ls='-.')
            if showComponents:
                    self.ax.plot(I, P_Pes[0], label=f"$P_{{Pe}}$ ($\Delta T=${dTs[0]} K)", c='blue', lw=1)
                    self.ax.plot(I, P_Pes[1], label=f"$P_{{Pe}}$ ($\Delta T=${dTs[1]} K)", c='blue', lw=1, ls='--')
                    self.ax.plot(I, P_Pes[2], label=f"$P_{{Pe}}$ ($\Delta T=${dTs[2]} K)", c='blue', lw=1, ls=':' )
                    self.ax.plot(I, P_Pes[3], label=f"$P_{{Pe}}$ ($\Delta T=${dTs[3]} K)", c='blue', lw=1, ls='-.')
                    self.ax.plot(I, P_J, label=f"$P_{{J}}$ ($\Delta T=${dTs[0]},{dTs[1]},{dTs[2]},{dTs[3]} K)", c='orange', lw=1)
                    self.ax.plot(I, P_Ls[0], label=f"$P_{{\lambda}}$ ($\Delta T=${dTs[0]} K)", c='red', lw=1)
                    self.ax.plot(I, P_Ls[1], label=f"$P_{{\lambda}}$ ($\Delta T=${dTs[1]} K)", c='red', lw=1, ls='--')
                    self.ax.plot(I, P_Ls[2], label=f"$P_{{\lambda}}$ ($\Delta T=${dTs[2]} K)", c='red', lw=1, ls=':')
                    self.ax.plot(I, P_Ls[3], label=f"$P_{{\lambda}}$ ($\Delta T=${dTs[3]} K)", c='red', lw=1, ls='-.')

        self.ax.set_xlabel("I [A]")
        self.ax.set_ylabel("P [W]")
        self.ax.grid()
        self.ax.set_title("Heatfluxes")
        self.ax.legend(facecolor = (0.1, 0.1, 0.1, 1))

        self.draw()

    def plot_I_COP(self, heatfluxi, dTs):
        self.ax.clear()
        # cop = []
        linetypes = ['-', '--', ':', '-.']
        for i, res in enumerate(heatfluxi['COPs']):
            # cop.append(res/ -heatfluxi['P_Joule'])
            self.ax.plot(heatfluxi['I'], heatfluxi['COPs'][i], label=f"$\Delta$T={dTs[i]} K", c='white', lw=1.5, ls=linetypes[i])

        self.ax.set_xlabel("I [A]")
        self.ax.set_ylabel("COP")
        self.ax.grid()
        self.ax.set_ylim(0, 20)
        self.ax.set_title("Coefficient of Performance (COP)")
        self.ax.legend(facecolor = (0.1, 0.1, 0.1, 1))
        self.draw()