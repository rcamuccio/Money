import datetime
import matplotlib.pyplot as plt
import numpy as np

class Money:

	@staticmethod
	def dte_to_jd(dte, fmt='%Y-%m-%d'):

		dt = datetime.datetime.strptime(dte, fmt)

		year = dt.year
		month = dt.month
		day = dt.day

		if (month == 1) or (month == 2):
			yearp = year - 1
			monthp = month + 12
		else:
			yearp = year
			monthp = month

		if ((year < 1582) or (year == 1582 and month < 10) or (year == 1582 and month == 10 and day < 15)):
			B = 0
		else:
			A = np.trunc(yearp / 100.)
			B = 2 - A + np.trunc(A / 4.)

		if yearp < 0:
			C = np.trunc((365.25 * yearp) - 0.75)
		else:
			C = np.trunc(365.25 * yearp)

		D = np.trunc(30.6001 * (monthp + 1))

		jd = B + C + D + day + 1720994.5

		return jd

	@staticmethod
	def get_file_size(nme):

		with open(nme) as f:
			nlines = sum(1 for _ in f)

		return nlines

	@staticmethod
	def get_ref_jd(year):

		dte_list = []
		for m in range(1, 13):
			dte = year + '-' + str(m) + '-1'
			dte_list.append(dte)

		jd_list = []

		for dte in dte_list:
			jd = Money.dte_to_jd(dte)
			jd_list.append(jd)

		return jd_list

	@staticmethod
	def get_chk(nme, fmt='%Y-%m-%d'):

		dte_list = []
		chk_list = []

		idx = 0

		f = open(nme)

		for ln in f:
			ln = ln.split()

			acc = ln[0]
			if acc == 'Checking':

				dte = ln[1]
				jd = Money.dte_to_jd(dte)
				dte_list.append(jd)

				chk = float(ln[4])
				chk_list.append(chk)

				idx += 1

		chk_mean = np.mean(chk_list)

		f.close()

		return idx, dte_list, chk_list, chk_mean

	@staticmethod
	def get_svg(nme, dte_i, dte_f, fmt='%Y-%m-%d'):

		dte_i_jd = Money.dte_to_jd(dte_i)
		dte_f_jd = Money.dte_to_jd(dte_f)

		dte_list = []
		svg_list = []

		f = open(nme)

		for ln in f:
			ln = ln.split()

			acc = ln[0]
			if acc == 'Savings':

				dte = ln[1]
				jd = Money.dte_to_jd(dte)
				dte_list.append(jd)

				svg = float(ln[5])
				svg_list.append(svg)

				idx += 1

		svg_mean = np.mean(svg_list)

		f.close()

		return idx, dte_list, svg_list, svg_mean

	@staticmethod
	def get_eod(nme, dte_i, dte_f, fmt='%Y-%m-%d'):
		''' This function reads a data file containing bank account transactions and returns a list of unique dates along with the corresponding end-of-day net, checking, savings, and total balance.

		:parameter nme [str] - The path of the data file
		:parameter dte_i [str] - The initial date in yyyy-mm-dd format
		:parameter dte_f [str] - The final date in in yyyy-mm-dd format
		:parameter fmt [str] - The format of the date supplied

		:return dte_list [list, float] - A list of unique Julian dates
		:return chk_list [list, float] - A list of checking balances
		:return svg_list [list, float] - A list of savings balances
		:return tot_list [list, float] - A list of total account balances
		'''

		dte_i_jd = Money.dte_to_jd(dte_i)
		dte_f_jd = Money.dte_to_jd(dte_f)

		dte_list = []
		chk_list = []
		svg_list = []
		tot_list = []

		f = open(nme)

		for ln in f:
			ln = ln.split()

			acc = ln[0]
			if acc == 'Transfer':
				pass

			dte = ln[1]
			dte_jd = Money.dte_to_jd(dte)
			if (dte_jd < dte_i_jd) | (dte_jd > dte_f_jd):
				pass

			eod = ln[3]
			if eod == 'n/a':
				pass

			else:
				dte_list.append(dte_jd)

				chk = float(ln[4])
				chk_list.append(chk)

				svg = float(ln[5])
				svg_list.append(svg)

				tot = float(ln[6])
				tot_list.append(tot)

		f.close()

		return dte_list, chk_list, svg_list, tot_list

	@staticmethod
	def plt_eod(year, dte_list, chk_list, svg_list, tot_list):

		plt.figure(figsize=(10,10))

		plt.plot(dte_list, tot_list, color='blue', label='Total')
		plt.plot(dte_list, chk_list, color='green', label='Checking')
		plt.plot(dte_list, svg_list, color='red', label='Savings')

		ref_jd_list = Money.get_ref_jd(year)
		for date in ref_jd_list:
			plt.axvline(x=date, ymin=0, ymax=10000, linestyle='dotted', linewidth=0.5, color='gray')

		plt.title(str(year) + ' Balance')
		plt.xlabel('Time [JD]')
		plt.ylabel('Amount [USD]')
		plt.legend()

		plt.savefig(str(year) + '.png', dpi=400)

if __name__ == '__main__':

	year = '2025'
	filename = 'data.txt'

	dte_list, chk_list, svg_list, tot_list = Money.get_eod(filename, dte_i='2025-01-01', dte_f='2025-12-31')
	
	Money.plt_eod(year, dte_list, chk_list, svg_list, tot_list)