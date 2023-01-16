# -*- coding: utf-8 -*-


''' --------- Imports ----------- '''

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import scipy as sp
from scipy.io import loadmat
import copy
import matplotlib.lines as mlines
from matplotlib.patches import Rectangle


''' --------- Fig. 2 ----------- '''


def plot_heatmap_noise(data,metric,vmin,vmax,title,main_title,size_titles,size_labels,size_pad,save):
	fig, (ax1,ax2,ax3,ax4) = plt.subplots(1,4,gridspec_kw={'width_ratios': [1,1,1,0.05]})
	fig.set_size_inches(35,10)
	fig.suptitle(main_title,fontsize=size_titles,fontweight='bold',y=1.05)
	heat1 = data['OU_cs'][metric]
	heat2 = data['Pink_cs'][metric]
	heat3 = data['White_cs'][metric]
	sns.heatmap(heat1,ax=ax1,vmin=vmin,vmax=vmax,cmap=sns.color_palette("Blues"),
		square=True,cbar=None)
	sns.heatmap(heat2,ax=ax2,vmin=vmin,vmax=vmax,cmap=sns.color_palette("Blues"),
		square=True,cbar=None,yticklabels=[])
	sns.heatmap(heat3,ax=ax3,vmin=vmin,vmax=vmax,cmap=sns.color_palette("Blues"),
		square=True,yticklabels=[],cbar_ax=ax4)
	cbar = ax3.collections[0].colorbar
	cbar.set_ticks(np.arange(vmin,vmax+1,0.5*(vmax-vmin)))
	ax4.tick_params('y',length=10,width=2)
	cbar.set_ticklabels(np.arange(vmin,vmax+1,0.5*(vmax-vmin)))
	cbar.ax.tick_params(labelsize=size_labels)
	cbar.ax.set_ylabel(title,fontsize=size_labels)
	ax1.set_ylabel(r'Input Contrast, c',fontsize=size_labels,labelpad=-25)
	ax1.set_yticks([0,50])
	ax1.set_yticklabels([1,0.02],fontsize=size_labels)
	contour1 = sp.ndimage.filters.gaussian_filter(heat1,sigma=1.2,mode='nearest',truncate=4)
	contour2 = sp.ndimage.filters.gaussian_filter(heat2,sigma=1.2,mode='nearest',truncate=4)
	contour3 = sp.ndimage.filters.gaussian_filter(heat3,sigma=1.2,mode='nearest',truncate=4)
	contour_list = [contour1,contour2,contour3]
	X = np.linspace(0,50,50)
	Y = np.linspace(0,50,50)
	X, Y = np.meshgrid(X,Y)
	for a,t,c in zip([ax1,ax2,ax3],
		['Ornstein-Uhlenbeck Noise','Pink Noise','Gaussian White Noise'],contour_list):
		a.set_xlabel(r'Noise Intensity, $\sigma$',fontsize=size_labels,labelpad=-10)
		a.set_xticks([0,50])
		a.set_xticklabels([0.005,0.25],fontsize=size_labels,fontdict={'horizontalalignment':'left'})
		a.tick_params(axis='x', rotation=0, pad = 10)
		a.tick_params(axis='both', length=10, width=2)
		a.set_title(t,{'fontsize':size_titles,'fontweight':'normal'},pad=size_pad)
		a.contour(X,Y,c,levels=[20,50,70],colors=['k'],linewidths=3)
	if save:
		plt.savefig(save+'.pdf',bbox_inches='tight')
	plt.show()
	return [ax1,ax2,ax3,ax4]

def plot_metrics(data,size_titles,size_labels,save):
	fig, (ax1,ax2,ax3) = plt.subplots(1,3)
	fig.set_size_inches(34.4,10)
	data_no_adap,data_div_adap,data_sub_adap=data
	difx = 0.05
	titles = {'DomDur':'Mean Percept Duration (s)','MixDur':'Mean Mixed Percept Duration (s)','CV':'Coefficient of Variation \nof Percept Durations'}
	ylims = [[0,6],[0,1.4],[0,4]]
	for metric,ax,ys in zip(['DomDur','MixDur','CV'],(ax1,ax2,ax3),ylims):
		x = np.array([1,2,3]) - difx
		for noise in ['Pink_cs','White_cs','OU_cs']:
			means = [data_no_adap[noise][metric].mean(),data_div_adap[noise][metric].mean(),data_sub_adap[noise][metric].mean()]
			stds  = [data_no_adap[noise][metric].std(),data_div_adap[noise][metric].std(),data_sub_adap[noise][metric].std()]
			ax.errorbar(x, means, yerr=stds,lw = 3,marker='o',markersize=10,capsize=6,capthick=3,elinewidth=3)
			x = x + difx
		ax.set_xlim([0.8,3.2])
		ax.set_xticks([1,2,3],fontsize=size_labels)
		ax.set_xticklabels(['No \nAdaptation','Divisive \nAdaptation','Subtractive \nAdaptation'],fontsize=size_labels)
		ax.set_ylim(ys)
		ax.tick_params(axis='y', labelsize=size_labels)
		ax.tick_params(axis='x', pad=10)
		ax.tick_params('both',length=10,width=2)
		ax.set_title(titles[metric],fontsize=size_titles,pad=25)
		ax.spines[['bottom','left','top','right']].set_linewidth(2)
		ax.spines[['bottom','left','top','right']].set_color('#c4c4c4')
	ax1.legend(['Pink Noise','Gaussian White Noise','Ornstein-Uhlenbeck Noise'],fontsize=size_labels)
	ax1.annotate('*',  xy = (1+0.5*difx,0.4),color='tab:orange',fontsize=25)
	ax1.annotate('*',  xy = (2-0.5*difx,0.28),color='tab:orange',fontsize=25)
	ax2.annotate('*',  xy = (1+0.5*difx,0.45),color='tab:orange',fontsize=25)
	ax2.annotate('*',  xy = (2-0.5*difx,0.4),color='tab:orange',fontsize=25)
	ax3.annotate('*',  xy = (1+0.5*difx,2.3),color='tab:orange',fontsize=25)
	ax3.annotate('*',  xy = (2+0.5*difx,2.5),color='tab:orange',fontsize=25)
	if save:
		plt.savefig(save+'.pdf',bbox_inches='tight')
	plt.show()
	return [ax1,ax2,ax3]

def plot_violin(data,noises,size_labels,save,max_y):
	fig, ax = plt.subplots(1,1)
	fig.set_size_inches(11.48,11.48)
	ax.spines["top"].set_visible(False)
	ax.spines["right"].set_visible(False)
	ax.spines['bottom'].set_color('#c4c4c4')
	ax.spines['left'].set_color('#c4c4c4')
	ax.spines[['bottom','left','top','right']].set_linewidth(2)
	wid_violin = 0.2
	colors = ['tab:green','tab:blue','tab:orange']
	labels = ['Ornstein-Uhlenbeck Noise','Pink Noise','Gaussian White Noise']
	for i in range(0,len(noises)):
		noise = noises[i]
		if len(noises) == 2:
			const = 0.15
			xpos = [1+(2*i-1)*const,2+(2*i-1)*const,3+(2*i-1)*const]
		else:
			const = 0.25
			xpos = [1+(i-1)*const,2+(i-1)*const,3+(i-1)*const]
		hist1 = data[noise]['DomDur']
		hist2 = data[noise]['MixDur']
		hist3 = data[noise]['CV']
		mins  = np.array([np.min(hist1),np.min(hist2),np.min(hist3)])
		maxes = np.array([np.max(hist1),np.max(hist2),np.max(hist3)])
		means = np.array([np.mean(hist1),np.mean(hist2),np.mean(hist3)])
		std   = np.array([np.std(hist1),np.std(hist2),np.std(hist3)])
		n = np.array([np.shape(hist1)[0],np.shape(hist2)[0],np.shape(hist3)[0]])
		parts = ax.violinplot([hist1,hist2,hist3],xpos,widths=wid_violin,showextrema=False)
		for pc in parts['bodies']:
			pc.set_facecolor(colors[i])
		ax.errorbar(np.array(xpos), means, [means - mins, maxes - means], fmt='.k', ecolor='darkgray', elinewidth=1)
		ax.errorbar(np.array(xpos), means, std, fmt='ok', elinewidth=4, ecolor=colors[i])
		for j in range(0,3):
			if noise=='Pink_cs' and j==1:
				ax.annotate('N='+str(n[j]),(xpos[j]-0.03,mins[j]-0.22),fontsize=size_labels-5,horizontalalignment='center')
			else:
				ax.annotate('N='+str(n[j]),(xpos[j]-0.03,mins[j]-0.13),fontsize=size_labels-5,horizontalalignment='center') 
	# formatting and labels
	ax.set_xlim([0.5,3.5])
	ax.set_xticks([1,2,3])
	ax.set_xticklabels(['Mean\n Percept\n Duration (s)','Mean Mixed\n Percept\n Duration (s)','Coefficient of\n Variation of\n Percept Durations'])
	ax.tick_params(axis='x', pad=20, labelsize=size_labels,length=10,width=2)
	ax.tick_params(axis='y',labelsize=size_labels,length=10,width=2)
	ax.set_xlabel(' ')
	ax.set_ylabel(' ')
	ax.set_ylim([0,max_y])
	ax.set_yticks(np.arange(0,max_y+1,2))
	ax.set_yticklabels(np.arange(0,max_y+1,2))
	lines = [mlines.Line2D([], [], color=c,lw=3) for c in colors]
	ax.legend(handles=lines[:len(noises)],labels=labels[:len(noises)],loc='upper center',markerscale=0,fontsize=size_labels)
	if save:
		plt.savefig(save+'.pdf',bbox_inches='tight')
	plt.show()
	return ax

def plot_histogram(data,size_labels,size_pad,save):
	fig, ax = plt.subplots(1,1)
	fig.set_size_inches(11.48,11.48)

	num_bins = 500
	ax.hist(data['White_cs']['PercTime'],bins=num_bins,range=(0,100),color='tab:orange',alpha = 0.5,cumulative=True)
	ax.hist(data['Pink_cs']['PercTime'],bins=num_bins,range=(0,100),color='tab:blue',alpha = 0.5,cumulative=True)
	ax.hist(data['OU_cs']['PercTime'],bins=num_bins,range=(0,100),color='tab:green',alpha = 0.4,cumulative=True)

	ax.legend(['Gaussian White Noise','Pink Noise','Ornstein-Uhlenbeck Noise'],fontsize=size_labels,loc='lower right')
	ax.set_xlabel(r'Dominance Time (%)',fontsize=size_labels,labelpad=size_pad)
	ax.set_xticks(np.linspace(0,100,5))
	ax.set_xticklabels(np.linspace(0,100,5,dtype=int),fontsize=size_labels)
	ax.set_xlim([0,100])
	ax.tick_params('y',labelsize=size_labels)
	ax.tick_params('both',length=10,width=2)
	ax.set_ylabel(r'Cumulative Number of Cases',fontsize=size_labels,labelpad=size_pad)
	ax.set_ylim([0,2500])
	ax.spines["top"].set_visible(False)
	ax.spines["right"].set_visible(False)
	ax.spines['bottom'].set_color('#c4c4c4')
	ax.spines['left'].set_color('#c4c4c4')
	ax.spines[['bottom','left','top','right']].set_linewidth(2)
	if save:
		plt.savefig(save+'.pdf',bbox_inches='tight')
	plt.show()
	return ax

def plot_ou_tau(data,data_sd,size_labels,main_title,adap,save):
	fig, (ax1,ax2) = plt.subplots(1,2)
	fig.set_size_inches(15,10)
	fig.suptitle(main_title,fontsize=size_labels+2,fontweight='bold',y=0.95)

	heat1 = data['OU_st']['PercTime']
	heat1sd = np.divide(data_sd['OU_st']['PercTime'],heat1)*100
	heat2 = data['OU_st']['DomDur']

	ax1 = sns.heatmap(heat1,ax=ax1,vmin=0,vmax=100,cmap=sns.color_palette("Blues"),
		square=True,cbar_kws={'use_gridspec':False,'location':'top','shrink':0.8})
	cax = ax1.figure.axes[-1]
	cax.tick_params('x',length=10,width=2)
	ax2 = sns.heatmap(heat1sd,vmin=0,vmax=180,ax=ax2,cmap=sns.color_palette("Blues"),
		square=True,cbar_kws={'use_gridspec':False,'location':'top','shrink':0.8})
	cax = ax2.figure.axes[-1]
	cax.tick_params('x',length=10,width=2)
	for ax in [ax1,ax2]:
		ax.set_xlabel(r'Noise Intensity, $\sigma$',fontsize=size_labels,labelpad=-10)
		ax.set_xticks([0,50])
		ax.set_xticklabels([0.002,0.1],fontsize=size_labels)
		ax.tick_params(axis='x', rotation=0, pad=10)
		ax.tick_params('both',length=10,width=2)

		ax.set_ylabel(r'Noise Correlation Time, $\tau$ (ms)',fontsize=size_labels,labelpad=10)

		ax.axhline(y=50, color='#dbe9f6',linewidth=3)
		ax.axhline(y=0, color='#dbe9f6',linewidth=3)
		ax.axvline(x=0, color='#dbe9f6',linewidth=3)
		ax.axvline(x=50, color='#dbe9f6',linewidth=3)

		if ax == ax1:
			if adap == False:
				ax.set_yticks([0,50])
				ax.set_yticklabels([1000,20],fontsize=size_labels)
				ax.tick_params(axis='y', rotation=0)
			else:
				ax.set_yticks([0,30,50])
				ax.set_yticklabels([1000,400,20],fontsize=size_labels)
				ax.tick_params(axis='y', rotation=0)
		else:
			ax2.set_yticks([])
			ax2.set_yticklabels([])
	# color bar configurations  
	cbar = ax1.collections[0].colorbar
	cbar.set_ticks([0,50,100])
	cbar.set_ticklabels([0,50,100])
	cbar.ax.tick_params(labelsize=size_labels)
	cbar.ax.set_xlabel('Dominance Time (%)',fontsize=size_labels,labelpad=15)
	cbar = ax2.collections[0].colorbar
	cbar.set_ticks([0,90,180])
	cbar.set_ticklabels([0,90,180])
	cbar.ax.tick_params(labelsize=size_labels)
	cbar.ax.set_xlabel('Standard Deviation of Dominance Time (%)',fontsize=size_labels,labelpad=15)   
	# contour of mean percept duration
	contour = sp.ndimage.filters.gaussian_filter(heat2,sigma=1.2,mode='nearest',truncate=4)
	X = np.linspace(0,50,50)
	Y = np.linspace(0,50,50)
	X, Y = np.meshgrid(X,Y)
	ax1.contour(X,Y,contour,levels=[1],colors=['w'],linewidths=3)
	if adap == False:
		ax1.annotate(' ',xy=(28,28),fontsize=size_labels,fontweight='bold',color='w')
	else:
		ax1.annotate(r'$\bar{D}=1$',xy=(28,28),fontsize=size_labels,fontweight='bold',color='w')
	# mark parameters used by Said and Heeger
	oriX, oriY = 24, 10
	lil_box = Rectangle((oriX, oriY), 1, 1,alpha=1,ec='tab:red',lw=3,fill=False)
	ax1.add_patch(lil_box)
	if save:
		plt.savefig(save+'.pdf',bbox_inches='tight')
	plt.show()
	ax = [ax1,ax2]
	return ax

def plot_timecourse(data,size_labels,size_titles,save):
	fig, (ax1,ax2,ax3) = plt.subplots(3,1,gridspec_kw={'height_ratios': [1,1,1]})
	fig.set_size_inches(20,15)

	ou_time,pink_time,white_time = data

	ou_time_t = ou_time['t'][0,:]
	ou_time_a = ou_time['FA'][0,:]
	ou_time_b = ou_time['FB'][0,:]

	pink_time_t = pink_time['t'][0,:]
	pink_time_a = pink_time['FA'][0,:]
	pink_time_b = pink_time['FB'][0,:]

	white_time_t = white_time['t'][0,:]
	white_time_a = white_time['FA'][0,:]
	white_time_b = white_time['FB'][0,:]

	for a in [ax1,ax2,ax3]:
		a.set_xlim(0,20000)
		a.set_ylim(0,1)
		a.set_ylabel(r'Firing Rate',fontsize=size_labels,labelpad=20)
		a.set_xticks(np.linspace(0,20000,6))
		a.set_xticklabels([])
		a.set_yticks(np.linspace(0,1,3))
		a.set_yticklabels(np.linspace(0,1,3).round(3),fontsize=size_labels)
		a.tick_params('both',length=10,width=2)
		a.spines["top"].set_visible(False)
		a.spines["right"].set_visible(False)
		a.spines['bottom'].set_color('#c4c4c4')
		a.spines['left'].set_color('#c4c4c4')
		a.spines[['bottom','left','top','right']].set_linewidth(2)

	ax1.plot(ou_time_t,ou_time_a,linewidth=3,color='tab:orange')
	ax1.plot(ou_time_t,ou_time_b,linewidth=3,color='tab:blue')
	ax1.set_title(r'Ornstein-Uhlenbeck Noise',fontsize=size_titles)
	ax1.legend(['Binocular Layer A','Binocular Layer B'],fontsize=size_labels,loc='upper right')
	ax1.fill_between(ou_time_t, ou_time_a, ou_time_b, where=(ou_time_a > ou_time_b), color='tab:orange', alpha=0.3)
	ax1.fill_between(ou_time_t, ou_time_a, ou_time_b, where=(ou_time_a < ou_time_b), color='tab:blue', alpha=0.3)

	ax2.plot(pink_time_t,pink_time_a,linewidth=3,color='tab:orange')
	ax2.plot(pink_time_t,pink_time_b,linewidth=3,color='tab:blue')
	ax2.set_title(r'Pink Noise',fontsize=size_titles)
	ax2.fill_between(pink_time_t, pink_time_a, pink_time_b, where=(pink_time_a > pink_time_b), color='tab:orange', alpha=0.3)
	ax2.fill_between(pink_time_t, pink_time_a, pink_time_b, where=(pink_time_a < pink_time_b), color='tab:blue', alpha=0.3)

	ax3.plot(white_time_t,white_time_a,linewidth=3,color='tab:orange')
	ax3.plot(white_time_t,white_time_b,linewidth=3,color='tab:blue')
	ax3.set_title(r'Gaussian White Noise',fontsize=size_titles)
	ax3.set_xlabel(r'Time (s)',fontsize=size_labels)
	ax3.set_xticklabels(np.linspace(0,20,6,dtype=int),fontsize=size_labels)
	ax3.fill_between(white_time_t, white_time_a, white_time_b, where=(white_time_a > white_time_b), color='tab:orange', alpha=0.3)
	ax3.fill_between(white_time_t, white_time_a, white_time_b, where=(white_time_a < white_time_b), color='tab:blue', alpha=0.3)

	if save:
		plt.savefig(save+'.pdf',bbox_inches='tight')
	plt.show()
	return [ax1,ax2,ax3]
