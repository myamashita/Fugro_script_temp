import h5py
import xarray as xr
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import datetime as dtm
import numpy as np
import pandas as pd
"""
NotImplementedError: Please use HDF reader for matlab v7.3 files, e.g. h5py
fd 1x29
spec2d 59887x29x24
td 59887x5
thetad 1x24
"""

fname = 'ww3_5118_spec.mat'

mat = h5py.File(fname, 'r')
time = np.squeeze(mat['td'][:])
# Create a DataFrame with columns for each component
df = pd.DataFrame({
    'year': time[0].astype(int),
    'month': time[1].astype(int),
    'day': time[2].astype(int),
    'hour': time[3].astype(int),
    'minute': time[4].astype(int)
})

# Create xarray.Dataset
DA = xr.Dataset({
    'spec2d': (['direction', 'frequency', 'time'], np.array(mat['spec2d']))},
    coords={'frequency': np.squeeze(mat['fd'][:]),
            'time': pd.to_datetime(df[['year', 'month', 'day', 'hour', 'minute']]),
            'direction': np.squeeze(mat['thetad'][:])})

#DA['direction']=(DA.direction+180)%360 
#DA = DA.sortby('direction', ascending=True)
sum_in_time = DA.sum(dim='time')

fig = plt.figure(facecolor=(1.0, 1.0, 1.0), figsize=(6.4, 4), dpi=300)
fig.show()
fig.canvas.draw()
ax = fig.add_subplot(1, 1, 1)
X, Y = np.meshgrid(DA.frequency, DA.direction)
Z = sum_in_time.spec2d

pc = ax.pcolormesh(
    X, Y, Z.values,
    cmap=plt.cm.plasma)
fig.colorbar(pc, ax=ax, orientation='horizontal', aspect=50,
                 label=r'Spectral Density [m$^2$/Hz]')
ax2 = ax.twiny()
ax2.xaxis.tick_top()
ax2.axes.set_xlabel('Period [s]')
ax2.set_xlim(ax.get_xlim()[0], ax.get_xlim()[1])
ax2.set_xticks([0.1, 0.2, 0.3, 0.4, 0.5])
ax2.set_xticklabels(['10', '5', '3.3', '2.5', '2'])
ax.axes.set_ylabel('Direction [FROM]')
ax.axes.set_xlabel('Frequency [Hz]')
fig.tight_layout()
fig.savefig(f'SUM_alltime_{fname[:-4]}.png', format='png')
plt.close('all')
fig.clf()

Z = DA.mean(dim='time').spec2d
fig = plt.figure(facecolor=(1.0, 1.0, 1.0), figsize=(6.4, 4), dpi=300)
fig.show()
fig.canvas.draw()
ax = fig.add_subplot(1, 1, 1)

pc = ax.pcolormesh(X, Y, Z,
                   norm=colors.LogNorm(vmin=5E-4, vmax=Z.max()),
                   cmap=plt.cm.jet)
fig.colorbar(pc, ax=ax, orientation='horizontal', aspect=50,
             label=r'Spectral Density [m$^2$/Hz]')

ax2 = ax.twiny()
ax2.xaxis.tick_top()
ax2.axes.set_xlabel('Period [s]')
ax2.set_xlim(ax.get_xlim()[0], ax.get_xlim()[1])
ax2.set_xticks([0.1, 0.2, 0.3, 0.4, 0.5])
ax2.set_xticklabels(['10', '5', '3.3', '2.5', '2'])
ax.axes.set_ylabel('Direction [FROM]')
ax.axes.set_xlabel('Frequency [Hz]')
fig.tight_layout()
fig.savefig(f'MEAN_alltime_jet_{fname[:-4]}.png', format='png')
plt.close('all')
fig.clf()

month = DA.groupby('time.month').mean(dim='time').spec2d
for i, j in enumerate(['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']):
    fig = plt.figure(facecolor=(1.0, 1.0, 1.0), figsize=(6.4, 4), dpi=300)
    fig.show()
    fig.canvas.draw()
    ax = fig.add_subplot(1, 1, 1)

    pc = ax.pcolormesh(X, Y, month.sel(month=i+1).values,
                       norm=colors.LogNorm(vmin=5E-4, vmax=Z.max()),
                       cmap=plt.cm.jet)
    fig.colorbar(pc, ax=ax, orientation='horizontal', aspect=50,
                 label=r'Spectral Density [m$^2$/Hz]')

    ax2 = ax.twiny()
    ax2.xaxis.tick_top()
    ax2.axes.set_xlabel('Period [s]')
    ax2.set_xlim(ax.get_xlim()[0], ax.get_xlim()[1])
    ax2.set_xticks([0.1, 0.2, 0.3, 0.4, 0.5])
    ax2.set_xticklabels(['10', '5', '3.3', '2.5', '2'])
    ax.axes.set_ylabel('Direction [FROM]')
    ax.axes.set_xlabel('Frequency [Hz]')
    fig.tight_layout()
    fig.savefig(f'MEAN_{j}_jet_{fname[:-4]}.png', format='png')
    plt.close('all')
    fig.clf()
