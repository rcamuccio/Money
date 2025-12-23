import datetime
import matplotlib.pyplot as plt
import numpy as np
import os
import sys

class Money:

	@staticmethod
	def dte_to_jd(dte, fmt='%Y-%m-%d'):

		dte = datetime.datetime.strptime(dte, fmt)

		year = dte.year
		month = dte.month
		day = dte.day

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

		jd = float(B + C + D + day + 1720994.5)

		return jd

	@staticmethod
	def dte_f():

		t = datetime.datetime.today()
		y = str(t.year)
		m = str(t.month)
		d = str(t.day)
		dte = y + '-' + m + '-' + d

		return dte

	@staticmethod
	def dte_i():

		t = datetime.datetime.today()
		y = str(t.year)
		m = '01'
		d = '01'
		dte = y + '-' + m + '-' + d

		return dte

	@staticmethod
	def get_chk(nme, dte_i=None, dte_f=None):

		if dte_i == None:
			dte_i = Money.dte_i()

		if dte_f == None:
			dte_f = Money.dte_f()

		dte_i_jd = Money.dte_to_jd(dte_i)
		dte_f_jd = Money.dte_to_jd(dte_f)

		dte_list = []
		dte_jd_list = []
		chk_list = []

		f = open(nme)

		for ln in f:
			ln = ln.split()

			if ln[0] == 'Checking':
				dte = ln[1]
				dte_jd = Money.dte_to_jd(dte)
				chk = float(ln[3])

				if (dte_jd < dte_i_jd) or (dte_jd > dte_f_jd):
					pass

				else:
					dte_list.append(dte)
					dte_jd_list.append(dte_jd)
					chk_list.append(chk)

			else:
				pass

		f.close()

		return dte_list, dte_jd_list, chk_list

	@staticmethod
	def get_eod(nme, dte_i=None, dte_f=None, print_to_term=True):

		if dte_i == None:
			dte_i = Money.dte_i()

		if dte_f == None:
			dte_f = Money.dte_f()		

		dte_i_jd = Money.dte_to_jd(dte_i)
		dte_f_jd = Money.dte_to_jd(dte_f)

		dte_list = []
		dte_jd_list = []
		chk_list = []
		eod_list = []
		svg_list = []
		tot_list = []

		dte_pre = None
		eod = 0.

		f = open(nme)

		for ln in f:
			ln = ln.split()
			acc = ln[0]

			# skip header and transfers
			if (acc == 'Account') or (acc == 'Transfer'):
				pass

			else:
				dte = ln[1]
				dif = float(ln[2])
				chk = float(ln[3])
				svg = float(ln[4])
				tot = float(ln[5])
				dte_jd = Money.dte_to_jd(dte)

				# filter dates outside range
				if (dte_jd < dte_i_jd) or (dte_jd > dte_f_jd):
					pass

				else:
					# set first unique date and eod
					if dte_pre == None:
						dte_pre = dte
						dte_list.append(dte)
						dte_jd_list.append(dte_jd)
						eod = dif

					# shift unique date and reset eod
					elif dte_pre != dte:
						dte_list.append(dte)
						dte_jd_list.append(dte_jd)
						eod_list.append(eod)
						chk_list.append(chk)
						svg_list.append(svg)
						tot_list.append(tot)
						dte_pre = dte
						eod = dif

					# add to current eod
					else:
						eod += dif

		# final sum
		eod_list.append(eod)
		chk_list.append(chk)
		svg_list.append(svg)
		tot_list.append(tot)

		if print_to_term:
			cnt = 1
			for dte in dte_list:
				amt = np.around(eod_list[cnt-1], decimals=2)
				print(' ', cnt, dte, amt, 'USD')
				cnt += 1

		f.close()

		return dte_list, dte_jd_list, eod_list, chk_list, svg_list, tot_list

	@staticmethod
	def get_svg(nme, dte_i=None, dte_f=None):

		if dte_i == None:
			dte_i = Money.dte_i()

		if dte_f == None:
			dte_f = Money.dte_f()

		dte_i_jd = Money.dte_to_jd(dte_i)
		dte_f_jd = Money.dte_to_jd(dte_f)

		dte_list = []
		dte_jd_list = []
		svg_list = []

		f = open(nme)

		for ln in f:
			ln = ln.split()

			if ln[0] == 'Savings':
				dte = ln[1]
				dte_jd = Money.dte_to_jd(dte)
				svg = float(ln[4])

				if (dte_jd < dte_i_jd) or (dte_jd > dte_f_jd):
					pass

				else:
					dte_list.append(dte)
					dte_jd_list.append(dte_jd)
					svg_list.append(svg)

			else:
				pass

		f.close()

		return dte_list, dte_jd_list, svg_list

	@staticmethod
	def get_tot(nme, dte_i=None, dte_f=None):

		if dte_i == None:
			dte_i = Money.dte_i()

		if dte_f == None:
			dte_f = Money.dte_f()

		dte_i_jd = Money.dte_to_jd(dte_i)
		dte_f_jd = Money.dte_to_jd(dte_f)

		dte_list = []
		dte_jd_list = []
		chk_list = []
		svg_list = []
		tot_list = []

		f = open(nme)

		for ln in f:
			ln = ln.split()

			if (ln[0] == 'Checking') or (ln[0] == 'Savings'):
				dte = ln[1]
				dte_jd = Money.dte_to_jd(dte)
				chk = float(ln[3])
				svg = float(ln[4])
				tot = chk + svg

				if (dte_jd < dte_i_jd) or (dte_jd > dte_f_jd):
					pass

				else:
					dte_list.append(dte)
					dte_jd_list.append(dte_jd)
					tot_list.append(tot)

			else:
				pass

		return dte_list, dte_jd_list, tot_list

	@staticmethod
	def get_trf(nme, dte_i=None, dte_f=None):

		if dte_i == None:
			dte_i = Money.dte_i()

		if dte_f == None:
			dte_f = Money.dte_f()		

		dte_i_jd = Money.dte_to_jd(dte_i)
		dte_f_jd = Money.dte_to_jd(dte_f)

		dte_list = []
		dte_jd_list = []
		trf_list = []

		f = open(nme)

		for ln in f:
			ln = ln.split()

			if ln[0] == 'T':
				dte = ln[1]
				dte_jd = Money.dte_to_jd(dte)
				trf = float(ln[2])

				if (dte_jd < dte_i_jd) or (dte_jd > dte_f_jd):
					pass

				else:
					dte_list.append(dte)
					dte_jd_list.append(dte_jd)
					trf_list.append(trf)

			else:
				pass

		f.close()

		return dte_list, dte_jd_list, trf_list

	@staticmethod
	def plt_chk(year, dte_list, chk_list):

		plt.figure(figsize=(10, 10))

		plt.plot(dte_list, chk_list, color='green')

		ref_jd_list = Money.ref_jd(year)
		for date in ref_jd_list:
			plt.axvline(x=date, ymin=0, ymax=10000, linestyle='dotted', linewidth=0.5, color='gray')

		plt.title('Checking Balance (' + str(year) + ')')
		plt.xlabel('Time [JD]')
		plt.ylabel('Amount [USD]')

		plt.savefig(str(year) + '-chk.png', dpi=400)

	@staticmethod
	def plt_eod(year, dte_list, chk_list, svg_list, tot_list):

		plt.figure(figsize=(10, 10))

		plt.plot(dte_list, tot_list, color='blue', label='Total')
		plt.plot(dte_list, chk_list, color='green', label='Checking')
		plt.plot(dte_list, svg_list, color='red', label='Savings')

		ref_jd_list = Money.ref_jd(year)
		for date in ref_jd_list:
			plt.axvline(x=date, ymin=0, ymax=10000, linestyle='dotted', linewidth=0.5, color='gray')

		plt.title('EOD Balance (' + str(year) + ')')
		plt.xlabel('Time [JD]')
		plt.ylabel('Amount [USD]')
		plt.legend()

		plt.savefig(str(year) + '-eod.png', dpi=400)

	@staticmethod
	def plt_svg(year, dte_list, svg_list):

		plt.figure(figsize=(10, 10))

		plt.plot(dte_list, svg_list, color='red')

		ref_jd_list = Money.ref_jd(year)
		for date in ref_jd_list:
			plt.axvline(x=date, ymin=0, ymax=10000, linestyle='dotted', linewidth=0.5, color='gray')

		plt.title('Savings Balance (' + str(year) + ')')
		plt.xlabel('Time [JD]')
		plt.ylabel('Amount [USD]')

		plt.savefig(str(year) + '-svg.png', dpi=400)

	@staticmethod
	def plt_tot(year, dte_list, tot_list):

		plt.figure(figsize=(10, 10))

		plt.plot(dte_list, tot_list, color='blue')

		ref_jd_list = Money.ref_jd(year)
		for date in ref_jd_list:
			plt.axvline(x=date, ymin=0, ymax=10000, linestyle='dotted', linewidth=0.5, color='gray')

		plt.title('Total Balance (' + str(year) + ')')
		plt.xlabel('Time [JD]')
		plt.ylabel('Amount [USD]')

		plt.savefig(str(year) + '-tot.png', dpi=400)

	@staticmethod
	def ref_jd(year):

		dte_list = []
		for m in range(1, 13):
			dte = year + '-' + str(m) + '-1'
			dte_list.append(dte)

		jd_list = []
		for dte in dte_list:
			jd = Money.dte_to_jd(dte)
			jd_list.append(jd)

		return jd_list

if __name__ == '__main__':

	os.system('clear')

	year = '2025'
	file = 'test-data.tsv'
	dte_i = None
	dte_f = None
	print_to_term = False

	# transactions - checking, savings, total
	dte_chk_list, jd_chk_list, chk_list = Money.get_chk(file, dte_i, dte_f) 
	dte_svg_list, jd_svg_list, svg_list = Money.get_svg(file, dte_i, dte_f)
	dte_tot_list, jd_tot_list, tot_list = Money.get_tot(file, dte_i, dte_f)
	Money.plt_chk(year, jd_chk_list, chk_list)
	Money.plt_svg(year, jd_svg_list, svg_list)
	Money.plt_tot(year, jd_tot_list, tot_list)

	# transactions - EOD
	eod_dte_list, eod_dte_jd_list, eod_list, eod_chk_list, eod_svg_list, eod_tot_list = Money.get_eod(file, print_to_term=print_to_term)
	Money.plt_eod(year, eod_dte_jd_list, eod_chk_list, eod_svg_list, eod_tot_list)