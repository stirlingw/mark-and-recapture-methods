#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import uuid
import random
import math
from scipy import stats
import os

samples_per_file = 10000

def sample_at_idx(idx, file_prefix):
	with open(file_prefix + str(idx)) as f:
		print 'Sampling from file: ' + file_prefix + str(idx)
		u = []
		r = 0
		caught = []
		for label in f:
			caught.append(label)
			if (label in marked):
				r = r + 1
			else:
				if (label not in u):
					u.append(label) 
	return {'u': u,  'r': r, 'c': len(set(caught))}

if (len(sys.argv) > 1 and sys.argv[1] == 'populate'):
	file_prefix = sys.argv[2]
	labels_min = 1000000
	labels_max = 2000000
	uuids = []
	n_labels = int(random.uniform(labels_min, labels_max))
	print n_labels
	for x in xrange(n_labels):
		label = uuid.uuid1()
		for x in xrange(int(random.uniform(20, 200))):
			uuids.append(label)
	random.shuffle(uuids)
	idx = 0
	for label in uuids:
		if (idx % samples_per_file == 0):
			f = open(file_prefix + str(idx/samples_per_file),'w')
		f.write(str(label) + '\n');
		idx = idx + 1
	f.close();
elif (len(sys.argv) > 1 and sys.argv[1] == 'sample'):
	n_samples = int(sys.argv[2])
	file_prefix = sys.argv[3]
	num_files = len([f for f in os.listdir('.') if os.path.isfile(os.path.join('.', f)) and file_prefix in f])
	marked = []
	numerator_portion = 0
	numerator_portion_at_t_2 = 0
	denominator_portion = 0
	cum_marked_ratio = 0
	t_alpha_99 = stats.t.ppf(1-0.01, n_samples-2)
	t_alpha_95 = stats.t.ppf(1-0.05, n_samples-2)
	t_alpha_90 = stats.t.ppf(1-0.1, n_samples-2)
	for i in xrange(n_samples):
		res = sample_at_idx(i, file_prefix)
		c = res['c']
		marked = marked + res['u']      
		numerator_portion += (samples_per_file * math.pow(len(marked),2))
		if i < 2:
			numerator_portion_at_t_2 = numerator_portion 
		denominator_portion = denominator_portion + res['r']  * len(marked)
		est = int(numerator_portion/(denominator_portion+1))
		cum_marked_ratio += math.pow(res['r'],2) /(samples_per_file)
	var = ( cum_marked_ratio - math.pow(denominator_portion,2) / numerator_portion ) / (n_samples-2)
	std_err = math.sqrt(var/numerator_portion)
	print "Sample size used: {0:.2f}%".format(100.0*float(n_samples)/float(num_files+1))
	print 'Estimated Expected Value: '  + str(est)
	print 'Variance of ' + str(var) + ' (reciprocal)'
	print 'Standard Error of ' + str(std_err) + ' (reciprocal)'
	print 'Confidence Intervals:'
	print  '99%: ' + str(round(1.0/(1.0/est+(t_alpha_99*std_err)))) + " to " + str(round(1.0/(1.0/est-(t_alpha_99*std_err))))
	print  '95%: ' + str(round(1.0/(1.0/est+(t_alpha_95*std_err)))) + " to "  + str(round(1.0/(1.0/est-(t_alpha_95*std_err))))
	print  '90%: ' + str(round(1.0/(1.0/est+(t_alpha_90*std_err)))) + " to "  + str(round(1.0/(1.0/est-(t_alpha_90*std_err))))
else:
	print 'usage:\tcatchrelease.py populate sample_file_prefix'
	print '\tcatchrelease.py sample number_sample_files sample_file_prefix'
	print 'example:\n\tpython catchrelease.py sample 10 myfiles_'