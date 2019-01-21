# Contains the information about one node in the Baysean Network encoded with the dependancies, children, and cpt.
class Node(object): 
	def __init__(self):
		self.name = None
		self.cpt = None
		self.children = None
		self.parents = None

# this stores the actual bayes net object.
class BN(object):
	def __init__(self):
		FS = Node()
		FS.name = 'FS'
		FS.values = ['fs', '~fs']
		FS.cpt = {'fs' : 0.05, '~fs' : 0.95}
		FS.children = ['FB']
		FS.parents = None

		FB = Node()
		FB.name = 'FB'
		FB.values = ['fb', '~fb']
		FB.cpt = {'fb_fs' : 0.6, 'fb_~fs': 0.1, '~fb_fs' : 0.4, '~fb_~fs' : 0.9}
		FB.children = None
		FB.parents = ['FS']


		FM = Node()
		FM.name = 'FM'
		FB.values = ['fm', '~fm']
		FM.cpt = {'fm': 0.035714286, '~fm': 0.964285714}
		FM.children = ['FH', 'NDG']
		FM.parents = None

		NA = Node()
		NA.name = 'NA'
		NA.values = ['na', '~na']
		NA.cpt = {'na': 0.3, '~na': 0.7}
		NA.children = ['NDG']
		NA.parents = None

		NDG = Node()
		NDG.name = 'NDG'
		NDG.values = ['ndg', '~ndg']
		NDG.cpt = {'ndg_fm_na': 0.8, 'ndg_fm_~na': 0.4, 'ndg_~fm_na': 0.5, 'ndg_~fm_~na': 0  , '~ndg_fm_na': 0.2, '~ndg_fm_~na': 0.6 , '~ndg_~fm_na': 0.5, '~ndg_~fm_~na': 1 }
		NDG.children = ['FH']
		NDG.parents = ['NA', 'FM']

		FH = Node()
		FH.name = 'FH'
		NDG.values = ['fh', '~fh']
		FH.cpt = {'fh_ndg_fm_fs': 0.99, 'fh_ndg_fm_~fs' : 0.65, 'fh_ndg_~fm_fs': 0.75, 'fh_ndg_~fm_~fs' : 0.2, 'fh_~ndg_fm_fs': 0.9, 'fh_~ndg_fm_~fs' : 0.4, 'fh_~ndg_~fm_fs': 0.5, 'fh_~ndg_~fm_~fs' : 0.0, 
				 '~fh_ndg_fm_fs': 0.01, '~fh_ndg_fm_~fs' : 0.35, '~fh_ndg_~fm_fs': 0.25, '~fh_ndg_~fm_~fs' : 0.8, '~fh_~ndg_fm_fs': 0.1, '~fh_~ndg_fm_~fs' : 0.6, '~fh_~ndg_~fm_fs': 0.5, '~fh_~ndg_~fm_~fs' : 1.0} 
		FH.children = None
		FH.parents = ['FS', 'FM', 'NDG']

		self.BN = [FS, FB, FM, NA, NDG, FH]


