from copy import deepcopy
import random
class optimization:
	def __init__(self, blocks, edges, dict_var):
		self.dict_var = dict_var
		self.infinity = 9999999
		self.neginfinity = -9999
		self.blocks = deepcopy(blocks)
		self.edges = deepcopy(edges)
		self.end_block  = len(edges) - 2
		self.reverse_edges = self.create_reverse_edges(self.edges)
		self.dominators, self.dominated = self.create_dominators(self.edges, self.reverse_edges, -1)
		self.postdominators, self.postdominated = self.create_dominators(self.reverse_edges, self.edges, self.end_block)
		self.ipdom = self.create_idom(self.postdominators, self.end_block)		
		self.idom = self.create_idom(self.dominators, -1)
		self.forward_edges = {}
		self.backward_edges = {}
		self.natural_loops = {}	
		self.dfs_tree = {}
		self.do_dfs()
		self.create_forward_edge()
		self.create_backward_edge()
		self.create_cross_edge()
		self.create_natural_loop()
		self.Allocate_Registers()
		
	def get_ipdom(self):
		return self.ipdom
		
	def create_reverse_edges(self, edg):
		reverse_edges = {}
		for i in edg:
			reverse_edges[i] = [];
		for i in edg:
			for j in edg[i]:
				reverse_edges[j].append(i)
		
		return reverse_edges
		#self.reverse_edges = reverse_edges
	
	def create_dominators(self, edges, reverse_edges, root):
		dominators = {}
		dominators[root] = [root];
		N = self.blocks.keys()
		N.sort()
		N2 = deepcopy(N)
		N.remove(root)
		for i in N:
			dominators[i] = N2
		
		change = 1
		while(change):
			change = 0
			for n in N:
				T = N2
				for p in reverse_edges[n]:
					T = list(set(T) & set(dominators[p]))
				D = T
				D.append(n)
				D = list(set(D))
				D.sort()
				if(D != dominators[n]):
					change = 1
					dominators[n] = D
		#Removing edges that are not connected in graph
		#self.dominators = dominators
		temp_dom = self.create_reverse_edges(dominators)	
		#self.dominated = temp_dom
		for i in temp_dom:
			temp = self.single_path_dfs(i, edges)
			temp2 = deepcopy(temp_dom[i]) 
			for j in temp2:
				if j not in temp:
					temp_dom[i].remove(j)
		
		dominators = self.create_reverse_edges(temp_dom)	
		return (dominators, temp_dom)
	
	def create_idom(self, domin, root):
		Tmp = {}
		N = self.blocks.keys()
		N.sort()
		N2 = deepcopy(N)
		N.remove(root)
		for n in N2:
			Tmp[n] = domin[n][:]
			Tmp[n].remove(n)
		
		for n in N:
			tt_Tmp = Tmp[n][:] 
			#Made a copy because Tmp will change and so the looping does not happens as wanted
			for s in tt_Tmp:
				temp_Tmp = Tmp[n][:]
				if s in temp_Tmp:
					temp_Tmp.remove(s)
				for t in temp_Tmp:
					if t in Tmp[s]:
						if t in Tmp[n]:
							Tmp[n].remove(t)
		return Tmp
		
		
	def create_forward_edge(self):
	# Creates Forward edges .. testing 	
		forward_edge = {}
		d = self.dfs_d
		f = self.dfs_f
		for u in self.edges:
			for v in self.edges[u]:
				forward_edge[u] = []
				if (d[u] + 1) < (d[v]) < (f[v] + 1) < (f[u]):
					forward_edge[u].append(v)
		
		self.forward_edges = forward_edge					
					
		
	def create_backward_edge(self):
		for i in self.edges :
			j = self.edges[i]
			self.backward_edges[i] = []
			for k in j:
				if i in self.dominated[k] :
					self.backward_edges[i].append(k)
	
	def create_cross_edge(self):
		cross_edge = {}
		d = self.dfs_d
		f = self.dfs_f
		for u in self.edges:
			for v in self.edges[u]:
				cross_edge[u] = []
				if d[v] < f[v] < d[u] < f[u]:
					cross_edge[u].append(v)
		
		self.cross_edges = cross_edge					
					
	def create_natural_loop(self):
		loop = {}
		i = 0;
		for m in self.backward_edges:
			for n in self.backward_edges[m]:
				i = i + 1;
				loop[i] = [m, n]
				loop[i] = list(set(loop[i]));
				stack = [];
				if m != n :
					stack.append(m);
				while(len(stack) != 0) :
					p = stack[-1]
					del stack[-1]
					for q in self.reverse_edges[p]:
						if q not in loop[i]:
							loop[i].append(q);
							loop[i] = list(set(loop[i]));
							stack.append(q)
		self.natural_loop = loop;
		
	def do_dfs(self):
		
		self.dfs_color = {}
		self.dfs_pi = {};
		self.dfs_d = {};
		self.dfs_f = {};
	
		for i in self.edges:
			self.dfs_color[i] = 0
			self.dfs_pi[i] = -2;
			self.dfs_d[i] = 0;
			self.dfs_f[i] = 0;
			self.time = 0
			self.forward_edges[i] = []
		
		#self.stack = []
		for i in range(-1,len(self.edges)-1):
			if self.dfs_color[i] == 0:
				self.dfs_visit(i)
	
	
	def dfs_visit(self, u):
		self.time = self.time + 1;		
		self.dfs_d[u] = self.time
		stack = []
		stack.append(u)
		
		while(len(stack) > 0) :
			u = stack[-1]
			isleaf = 1;
			temp1 = self.edges[u]
			temp1.sort()
			#temp1.reverse()
			for v in temp1:
				if self.dfs_color[v] == 0:
					self.dfs_color[v] = 1
					self.dfs_pi[v] = u
					self.time = self.time + 1;		
					self.dfs_d[v] = self.time
					stack.append(v)
					isleaf = 0;
					break
			if isleaf == 1:
				self.dfs_color[v] = 2
				self.time = self.time + 1;		
				self.dfs_f[u] = self.time
				del stack[-1]
							
		
				
	def create_dfs_tree(self, root):
		self.dfs_tree = {}
		noncolor_nodes = deepcopy(self.edges.keys())
		cross_edge = {}
		for i in self.edges:
			cross_edge[i] = []
			self.forward_edges[i] = []
		i = 0;
		while(len(noncolor_nodes) > 0) :
			stack = [root]
			temp = []
			noncolor_nodes.remove(root)
			while(len(stack) > 0):
				
				curr = stack[-1]
				temp1 = self.edges[curr]
				temp1.sort()
				temp1.reverse()
				flag = 0
				for k in temp1:
					if k in noncolor_nodes:
						flag = 1;
						break
				
				if flag == 1:						
					del stack[-1]
					temp.append(curr)
				
				for j in temp1:
					if j in noncolor_nodes:
						stack.append(j)
						noncolor_nodes.remove(j)
					else:
						if j not in self.backward_edges[curr]:
							if j not in stack:
								cross_edge[curr].append(j)
							else:
								self.forward_edges[curr].append(j)
								
			self.dfs_tree[i] = temp
			if(len(noncolor_nodes) > 0):
				root = noncolor_nodes[0]
			i = i + 1		
		
		#print self.dfs_tree	
		#print cross_edge	
		
	
	def single_path_dfs(self, root, edges):
		noncolor_nodes = deepcopy(edges.keys())
		stack = [root]
		temp = []
		noncolor_nodes.remove(root)
		while(len(stack) > 0):
			curr = stack[-1]
			del stack[-1]
			temp.append(curr)
			for j in edges[curr]:
				if j in noncolor_nodes:
					stack.append(j)
					noncolor_nodes.remove(j)
		return temp 
	
	def Allocate_Registers(self):
		from reg_parameters import __REGS
		self.final_code = {}
		self.f = open("reg_alloc.txt", "w")
		self.write_file(self.blocks, "The Starting Code")
		self.symbol_map = {}
		self.symbol_map['__first_time'] = 1
		self.reverse_symbol_map = {}
		self.interfere = {} # need to fill this with a function given by the user input
		self.LIR = deepcopy(self.blocks)
		i = 0
		self.curr_disp = 0
		k = 0
		self.looping = self.looping_est()
		self.write_loop_count()
		while 1:
			k = k+1
			while 1:
				self.create_udchains(self.LIR)
				self.make_webs(__REGS, self.LIR)
				self.build_AdjMtx()
				bool_v = 1
				if k == 1:
					bool_v = self.Coalesce_Regs()
				if not bool_v:
					self.write_file(self.LIR, "After Register Coalesce")
				if bool_v:
					break
#			for i in self.Symreg:
#				print i, self.Symreg[i]
			self.Build_AdjLsts()
			self.Compute_Spill_Costs()
			self.write_file(self.LIR, "Code For Adj List")
			self.write_adjlist("Adj List After Spill cost")
			self.Prune_Graph()
			succ = self.Assign_Regs()
			self.write_adjlist("Adj List after Graph Coloring")
			if succ:
				self.Modify_Code()
				self.write_file(self.final_code, "The Final Code")
			else:
				self.Gen_Spill_Code()
				self.write_file(self.LIR, "Code After Spilling")	

			if k == 30:
				print "Tried", k, "times .... Please increase the number of registers"
				break		
			
			if succ:
				break		
		self.invariant_removal()
			
	def create_udchains(self, blocks):
		'''Creation of UDchains'''
		definitions = {}
		defcheck = {}
		self.def_keyword = {	'load' : 1,
						'str' : 1,
						'cpy' : 1,
						'cvt' : 1,
						'ldc' : 1,
						'neg' : 1,
						'add' : 1,
						'sub' : 1,
						'mul' : 1,
						'div' : 1,
						'not' : 1,
						'and' : 1,
						'ior' : 1,
						'xor' : 1,
						'seq' : 1,
						'sne' : 1,
						'sl' : 1,
						'sle' : 1,
					#	'jmp' : 1,
					#	'btru' : 1,
					#	'bfls' : 1,
					}
		def_keyword = self.def_keyword
		for i in blocks:
			j = blocks[i]
			for k in range(0,len(j)):
				l = j[k]
				if def_keyword.has_key(l[1]):
					if(l[2][:1] == '['):
						continue
					if(definitions.has_key(l[2])):
						definitions[l[2]].append((i, k))
						defcheck[(l[2],i,k)] = 1;
					else:
						definitions[l[2]] = [(i, k)]
						defcheck[(l[2],i,k)] = 1;
	
		self.definitions = definitions
		self.duchains = {}
		self.blocks_done = {}
		for i in defcheck:
			self.blocks_done = {}
			self.duchains[i] = []
			self.recur_duchain(i, i[1], 1, def_keyword, blocks)
		
		uses = {}
		for i in blocks:
			j = blocks[i]
			for k in range(0, len(j)):
				for l1 in range(2, len(j[k])):
					l = j[k][l1]
					if l1 == 2 :
						if def_keyword.has_key(j[k][1]):
							continue
					if definitions.has_key(l):
						if(uses.has_key(l)):
							uses[l].append((i, k))
						else:
							uses[l] = [(i, k)]
			
	def recur_duchain(self,defcheck_tuple, curr_block, first_time, def_keyword, blocks):
		if(first_time == 1):
			start_index = defcheck_tuple[2] + 1	
		else:
			start_index = 0
		j = blocks[curr_block]
		for k in range(start_index, len(j)):
			for l1 in range(2, len(j[k])):
				l = j[k][l1]
				if l==defcheck_tuple[0]:
					if l1 == 2 :
						if def_keyword.has_key(j[k][1]):
							continue
				
					if(self.duchains.has_key(defcheck_tuple)):
						self.duchains[defcheck_tuple].append((curr_block, k))
					else:
						self.duchains[defcheck_tuple] = [(curr_block, k)]
			
			if len(j[k]) > 2 and j[k][2] == defcheck_tuple[0]:
				return
		
					
		for i in self.edges[curr_block]:
			if self.blocks_done.has_key(i):
				continue;
			self.blocks_done[i] = 1
			self.recur_duchain(defcheck_tuple, i, 0, def_keyword, blocks)

# Here a web is a list of tuple (symb, defs(a tuple of tuple (block, line)), uses(a tuple of all uses), spill, sreg, disp)	
# Using 0 for false and -1 for nil
	def make_webs(self, nregs, blocks):
		Webs = set()
		nwebs = nregs
		for sdu in self.duchains:
			nwebs = nwebs + 1
			Webs = Webs.union(set([(sdu[0], tuple([(sdu[1], sdu[2])]), tuple(self.duchains[sdu]), 0, -1, -1)]))
		
		while 1:
		#for k in range(1,2):
			oldwebs = nwebs
			Tmp1 = deepcopy(Webs)
			while (len(list(Tmp1)) > 0):
				web1 = Tmp1.pop()
				old_web1 = web1
				Tmp2 = deepcopy(Tmp1)
				while(len(Tmp2) > 0):
					web2 = Tmp2.pop()
					if web1[0] == web2[0] and len(list(set(web1[2]).intersection(set(web2[2])))) !=0:
						temp_web_l = list(web1)
						temp_web_l[1] = tuple(set(web1[1]).union(set(web2[1]))) 	
						temp_web_l[2] = tuple(set(web1[2]).union(set(web2[2]))) 	
						web1 = tuple(temp_web_l)
						Webs_list = list(Webs)
						if web2 in Webs_list:
							Webs_list.remove(web2)
						Webs = set(Webs_list)
						nwebs = nwebs - 1
				Webs_list = list(Webs)
				if old_web1 in Webs_list:
					Webs_list.remove(old_web1)
					Webs_list.append(web1)
				Webs = set(Webs_list)
				
			if(oldwebs == nwebs):
				break		
			
		Symreg = {}
		for i in range(0, nregs):
			Symreg[i] = ('__R' + str(i), tuple([]), tuple([]), 0, -1, -1)
		
		self.reg_to_int = {}
		i = nregs
		Webs_list = list(Webs)
		for j in range(0,len(Webs_list)):
			temp_l = list(Webs_list[j]);
			temp_l[4] = i
			Webs_list[j] = tuple(temp_l)
			Symreg[i] = Webs_list[j];
			i = i + 1;
			self.reg_to_int[Webs_list[j][0]] = i - 1

		Webs = set(Webs_list)
		
		self.Webs = Webs
		self.Symreg = Symreg
		self.nwebs = len(Symreg)
		self.nregs = nregs

		self.MIR_to_SymLIR(blocks)	
		
		
# Trying to find if the use is after the def at question for LiveAt()	
# Please set self.blocks_done to [] before the call
	def is_reachable(self, a,b, a_def, b_def):
		'''a --> b : here both a and b are tuples of (block, line number)'''
		if a[1] != -1:
			a_def.remove(a)
		flag = 1
		if a[0]==b[0]:
			if a[1] < b[1]:
				for all_a in a_def:
					if all_a[0] != a[0] and all_a[0] !=b[0]:
						continue
					if a[1] < all_a[1] and all_a[1] < b[1]:
						flag = 0
						break
				for all_b in b_def:
					if all_b[0] != b[0] and all_b[0] !=b[0]:
						continue
					if a[1] < all_b[1] and all_b[1] < b[1]:
						flag = 0
						break
				if flag:
					return 1;
				#else:
				#	return 0;
		
		for i in self.edges[a[0]]:
			if i in self.blocks_done:
				continue
			self.blocks_done.append(i)
			temp_bool = self.is_reachable((i, -1), b, a_def, b_def)
			if temp_bool == 1:
				return 1;
		return 0	
	
	def create_interference(self):
		from reg_parameters import __never_go
		from reg_parameters import __always_go
		
		for i in __never_go:
			if self.symbol_map.has_key(i):
				for j in self.symbol_map[i]:
					temp1 = __never_go[i]
					for temp in temp1:
						if temp >= self.nregs:
							continue
						self.AdjMtx[j, temp] = 1

		for i in __always_go:
			if self.symbol_map.has_key(i):
				for j in self.symbol_map[i]:
					temp1 = __always_go[i]
					for temp in temp1:
						for k in range(0,self.nregs):
							if (k == temp):
								continue
							self.AdjMtx[j, k] = 1
		
				
	def build_AdjMtx(self):
		nwebs = self.nwebs
		nregs = self.nregs
		self.AdjMtx = {}
		Symreg = self.Symreg
		for i in range(1, nwebs):
			for j in range(0, i + 1):
				self.AdjMtx[i, j] = 0
		
		for i in range(1, nregs):
			for j in range(0, i):
				self.AdjMtx[i, j] = 1
		
		self.create_interference()
		for i in range(nregs, nwebs):
#			for j in range(1, nregs):
#				if self.check_restriction(Symreg[i], j): # need to change
#					self.AdjMtx[i,j] = 1	
		
			for j in range(nregs, i):
				for Def in list(Symreg[i][1]):
					flag = 0
					for an_def in list(Symreg[j][1]):
						self.blocks_done = []
						temp_bool = self.is_reachable(an_def, Def, list(Symreg[j][1]), list(Symreg[i][1]))
						if (temp_bool):
							flag = 1
							break
					if not flag:
						continue	
#					if (self.LiveAt(Symreg[j][2], Symreg[i][0], Def)):
					for uses in list(Symreg[j][2]):
						self.blocks_done = []
						temp_bool = self.is_reachable(Def, uses, list(Symreg[i][1]), list(Symreg[j][1]))
						if (temp_bool):
							self.AdjMtx[i,j] = 1
							
			for j in range(i+1, nwebs):
				for Def in list(Symreg[i][1]):
					flag = 0
					for an_def in list(Symreg[j][1]):
						self.blocks_done = []
						temp_bool = self.is_reachable(an_def, Def, list(Symreg[j][1]), list(Symreg[i][1]))
						if (temp_bool):
							flag = 1
							break
					if not flag:
						continue	
#					if (self.LiveAt(Symreg[j][2], Symreg[i][0], Def)):
					for uses in list(Symreg[j][2]):
						self.blocks_done = []
						temp_bool = self.is_reachable(Def, uses, list(Symreg[i][1]), list(Symreg[j][1]))
						if (temp_bool):
							self.AdjMtx[j,i] = 1
			
#			for i in range(1, self.nwebs):
#				print
#				for j in range(0,i):
#					print self.AdjMtx[i,j],				
	
	def MIR_to_SymLIR(self, blocks):
		LIR = deepcopy(blocks)
		temp_sym_map = {}
		temp_r_sym_map = {}
		for i in blocks:
			j = 0
			while j < len(blocks[i]):
				inst = blocks[i][j]
				for k1 in range(0,len(inst)):
					k = inst[k1]
					if self.definitions.has_key(k):
						for l in self.Symreg:
							temp_web = self.Symreg[l]
							if k == temp_web[0]:
								for m in temp_web[1]:
									if(m[0] == i and m[1] == j):
										LIR[i][j][k1] = "_s" + str(l)
										if self.symbol_map['__first_time'] == 1:
											if (self.symbol_map.has_key(self.blocks[i][j][k1])) == 0:
												self.symbol_map[self.blocks[i][j][k1]] = []
											if l not in self.symbol_map[self.blocks[i][j][k1]]:
												self.symbol_map[self.blocks[i][j][k1]].append(l)
												self.reverse_symbol_map[l] = self.blocks[i][j][k1]
										else:
							
											temp = self.reverse_symbol_map[int(blocks[i][j][k1][2:])]
											if (temp_sym_map.has_key(temp)) == 0:
												temp_sym_map[temp] = []
											if l not in temp_sym_map[temp]:
												temp_sym_map[temp].append(l)
												temp_r_sym_map[l] = temp	
												
								for m in temp_web[2]:
									if(m[0] == i and m[1] == j):
										LIR[i][j][k1] = "_s" + str(l)
										if self.symbol_map['__first_time'] == 1:
											if  self.symbol_map.has_key(self.blocks[i][j][k1]) == 0:
												self.symbol_map[self.blocks[i][j][k1]] = []
											if l not in self.symbol_map[self.blocks[i][j][k1]]:
												self.symbol_map[self.blocks[i][j][k1]].append(l)
												self.reverse_symbol_map[l] = self.blocks[i][j][k1]
										else:
											temp = self.reverse_symbol_map[int(blocks[i][j][k1][2:])]
											if (temp_sym_map.has_key(temp)) == 0:
												temp_sym_map[temp] = []
											if l not in temp_sym_map[temp]:
												temp_sym_map[temp].append(l)
												temp_r_sym_map[l] = temp	
												
				j = j + 1
		
		if self.symbol_map['__first_time'] == 0:
			self.symbol_map = temp_sym_map
			self.reverse_symbol_map = temp_r_sym_map
		
		self.symbol_map['__first_time'] = 0
		self.LIR = LIR
		for i in self.dict_var:
			temp = self.dict_var[i]
			if self.symbol_map.has_key(temp):
				self.symbol_map[i] = self.symbol_map[temp] 
				del self.symbol_map[temp]
						
									
# An AdjLsts is a list [nints, color, disp, spcost, adjnds, rmvadj, spill]				
	def Build_AdjLsts(self):
		self.AdjLsts = {}
		for i in range(0,self.nregs):
			self.AdjLsts[i] = [0, -1, -1, self.neginfinity, [], [], 0]
		for i in range(self.nregs, self.nwebs):
			self.AdjLsts[i] = [0, -1, -1, 0.0, [], [], 0]
		
		for i in range(1, self.nwebs):
			for j in range(0, i):
				if self.AdjMtx[i,j] == 1:
					self.AdjLsts[i][4].append(j);
					self.AdjLsts[j][4].append(i);
					self.AdjLsts[i][0] = self.AdjLsts[i][0] + 1
					self.AdjLsts[j][0] = self.AdjLsts[j][0] + 1
		
			
	def Coalesce_Regs( self):
		lir_temp = deepcopy(self.LIR)
		suc = 1;
		for i in range(-1,len(lir_temp) - 1):
			for j in range(0,len(lir_temp[i])):
				if self.LIR[i][j] == []:
					continue
				inst = self.LIR[i][j]
				if (inst[1] == 'cpy'):
					if inst[2][:1] == '[' or inst[4][:1] == '[':
						continue
					if inst[2][:2] != '_s' or inst[4][:2] != '_s':
						continue
					k = int(inst[2][2:])					
					l = int(inst[4][2:])
					if(self.AdjMtx[max(k,l), min(k,l)] == 0):
						for p in range(-1,len(lir_temp) - 1):
							for q in range(0,len(lir_temp[p])):
								rm_inst = self.LIR[p][q]
								for r in range(2,len(rm_inst)):
									opp = rm_inst[r]
									if opp == inst[4]:
										self.LIR[p][q][r] = inst[2]
						#self.LIR[i].pop(j)
						self.LIR[i][j] = []
						suc = 0
						temp_s1 = tuple(set(self.Symreg[k][1]).union(set(self.Symreg[l][1])))		
						temp_s2 = tuple(set(self.Symreg[k][2]).union(set(self.Symreg[l][2])))
						Symreg_list = list(self.Symreg[k])
						Symreg_list[1] = temp_s1
						Symreg_list[2] = temp_s2
						self.Symreg[k] = tuple(Symreg_list)
						self.Symreg[l] = () # Diff from Muchnik
						
						for p in range(0, len(self.Symreg)):
							if self.AdjMtx.has_key((max(p,l), min(p,l))):
								if self.AdjMtx[max(p,l), min(p,l)] == 1:
									self.AdjMtx[max(p,k), min(p,k)] = 1
								
								self.AdjMtx[max(p,l), min(p,l)] = 3 # Diff from Muchnik
		
		for i in self.LIR:
			while [] in self.LIR[i]:
				self.LIR[i].remove([])
		
	
		return suc
	
	def looping_est(self):
		looping = {}
		for i in range(-1,len(self.blocks) -1):
			looping[i] = 1;
		for i in self.natural_loop:
			for j in self.natural_loop[i]:
				temp = random.randint(2, 50)
				looping[j] = looping[j] + temp
		
		return looping												

# Remember: I have not removed the coalesced register from Adjlist ...
# To calculate Spill Cost doing what Jose did in class ...
# Every Def costs 1 while every use costs 2
# Am not considering rematerialization of registers
# Here a web is a list of tuple (symb, defs(a tuple of tuple (block, line)), uses(a tuple of all uses), spill, sreg, disp)
				
	def Compute_Spill_Costs(self):
		looping = self.looping
		for i in self.Symreg:
			if self.Symreg[i] == ():
				continue
			if self.AdjLsts[i][3] == self.neginfinity:
				continue
			curr_cost = 0
			# All the definitions ...
			for j in self.Symreg[i][1]:
				curr_cost = curr_cost + looping[j[0]] * 1;
				#curr_cost = 1000
			for j in self.Symreg[i][2]:
				curr_cost = curr_cost + looping[j[0]] * 2;
				#curr_cost = 1000
			temp_list = list(self.Symreg[i])
			temp_list[3] = curr_cost
			self.Symreg[i] = tuple(temp_list)
			self.AdjLsts[i][3] = curr_cost
		
		for i in self.LIR:
			for j in self.LIR[i]:
				if j[1] == 'cpy':
					if j[4][:3] == '[DI':
						sym_reg = int(j[2][2:])
						self.AdjLsts[sym_reg][3] = self.neginfinity
					if j[2][:3] == '[DI':
						sym_reg = int(j[4][2:])
						self.AdjLsts[sym_reg][3] = self.neginfinity
								

# An AdjLsts is a list [nints, color, disp, spcost, adjnds, rmvadj, spill]				
# How to handle cases where the nint is already 0 ??	
	def Prune_Graph(self):
		stack = []
		nodes = self.nwebs
		for i in range(0, self.nwebs):
			temp_nint = len(self.AdjLsts[i][4]) 	
			if  temp_nint== 0:
				success = 0
				stack.append(i)
				self.Adjust_Neighbors(i)	
				nodes = nodes - 1
		while 1:
			while 1:
				success = 1;
				for i in range(0, self.nwebs):
					temp_nint = len(self.AdjLsts[i][4]) 	
					if  temp_nint == 0 and i not in stack:
						success = 0
						stack.append(i)
						self.Adjust_Neighbors(i)	
						nodes = nodes - 1
					if  temp_nint> 0 and temp_nint < self.nregs:
						success = 0
						stack.append(i)
						self.Adjust_Neighbors(i)	
						nodes = nodes - 1
				
				if success:
					break
			if nodes !=0 :
				spillcost = self.infinity + 1
				spillnode = 6
				for i in range(0, self.nwebs):
					temp_nint = len(self.AdjLsts[i][4])
					spill_cost = self.AdjLsts[i][3]
					if temp_nint > 0 and (spill_cost/temp_nint) < spillcost:
						spillnode = i
						spillcost = spill_cost/temp_nint
						
				stack.append(spillnode)
				self.Adjust_Neighbors(spillnode)
				nodes = nodes - 1;
			
			if(nodes == 0):
				break
		self.reg_stack = stack
#		random.shuffle(self.reg_stack)
	
	def Adjust_Neighbors(self, i):
		for k in self.AdjLsts[i][4]:
			if k in self.AdjLsts[i][4]:
				self.AdjLsts[k][4].remove(i)
				self.AdjLsts[k][0] = self.AdjLsts[k][0] - 1
				self.AdjLsts[k][5].append(i)
		
		self.AdjLsts[i][0] = 0
		self.AdjLsts[i][5].extend(self.AdjLsts[i][4])
		self.AdjLsts[i][4] = []
		
	def Assign_Regs(self):
		success = 1
		self.color_map = {}
		still_left = []
		for i in self.AdjLsts:
			self.color_map[i] = -1
		
		for i in self.AdjLsts:
			if self.AdjLsts[i][3] == self.neginfinity:
				c = self.Min_Color(i)
				if c >= 0:
					if i < self.nregs:
						pass
					self.AdjLsts[i][1] = c
					self.reg_stack.remove(i)
				else:
					still_left.append(i)
					self.reg_stack.remove(i)						 
		while len(self.reg_stack) > 0:
			r = self.reg_stack[-1]
			del self.reg_stack[-1]
			c = self.Min_Color(r)
			if c >= 0:
				if r < self.nregs:
					pass
				self.AdjLsts[r][1] = c
			else:
				self.AdjLsts[r][6] = 1 #Do I need a spill part in AdjLsts ?
				success = 0
	
		while len(still_left) > 0:
			r = still_left[-1]
			del still_left[-1]
			c = self.Min_Color(r)
			if c >= 0:
				if r < self.nregs:
					pass
				self.AdjLsts[r][1] = c
			else:
				self.AdjLsts[r][6] = 1 #Do I need a spill part in AdjLsts ?
				success = 0
		
		return success			
	
	def Min_Color(self, r):
		reg_list = []
		for i in range(0, self.nregs):
			reg_list.append(i)
		for i in self.AdjLsts[r][5]:
			j = self.color_map[i]
			if j == -1:
				continue;
			if j in reg_list:
				reg_list.remove(j)
		if reg_list == []:
			return -1
		else:
			self.color_map[r] = reg_list[0]	 										 
			return reg_list[0]
	
	def Modify_Code(self):
		reg_color = {}
		for i in range(0,self.nregs):
			temp = self.AdjLsts[i][1]
			reg_color[temp] = i
		
		self.final_code = deepcopy(self.LIR)
		blocks = deepcopy(self.LIR)
		for i in blocks:
			j = 0
			while j < len(blocks[i]):
				inst = blocks[i][j]
				for k1 in range(0,len(inst)):
					k = inst[k1]
					if k[:2] == "_s":
						temp = int(k[2:])
						color = self.AdjLsts[temp][1]
						reg = reg_color[color]
						self.final_code[i][j][k1] = "_R" + str(reg)
				j = j + 1						

	
	def Gen_Spill_Code(self):
		regct = 0
		old_LIR = deepcopy(self.LIR)
		for ti in self.AdjLsts:
			i = self.AdjLsts[ti]
			if i[6] == 0:
				continue
			if i[3] == self.neginfinity:
				continue	
			web = self.Symreg[ti]
			defs = web[1]
			uses = web[2]
			if i[2] == -1:
				self.AdjLsts[ti][2] = self.curr_disp
				self.curr_disp = self.curr_disp + 4
			for p in defs:
				disp = self.AdjLsts[ti][2]
				blc = p[0]
				line_temp = p[1]
				line = self.LIR[blc].index(old_LIR[blc][line_temp])
				old_blc = self.LIR[blc]
				adding_lines = ['[xx]:', 'cpy', '[DISP + ' + str(disp) + ' ]', '=', '_s' + str(ti)]
				new_blc = old_blc[:(line + 1)]
				new_blc.append(adding_lines)
				new_blc.extend(old_blc[(line + 1):])
				self.LIR[blc] = new_blc
						
			for p in uses:
				disp = self.AdjLsts[ti][2]
				blc = p[0]
				line_temp = p[1]
				line = self.LIR[blc].index(old_LIR[blc][line_temp])
				old_blc = self.LIR[blc]
				new_blc = old_blc[:line]
				adding_lines = ['[xx]:', 'cpy', '_s' + str(ti), '=', '[DISP + ' + str(disp) + ' ]']
				new_blc.append(adding_lines)
				new_blc.extend(old_blc[line:])
				self.LIR[blc] = new_blc
		
	def write_file(self, blc, string):
		self.f.write("=========================== " + string + " ===========================\n")
		self.f.write("----------Block " + str(0) + "----------\n");
		self.f.write("Prologue\n")
		
		#Writing the blocks
		for i in range(len(blc)-1):
			self.f.write("----------Block " + str(i+1) + "----------\n");
			for j in blc[i]:
				self.f.write("\t".join(j[:3]))
				self.f.write(" ")
				self.f.write(" ".join(j[3:]))
				self.f.write('\n');
		self.f.write("Epilogue\n")

# An AdjLsts is a list [nints, color, disp, spcost, adjnds, rmvadj, spill]				
	def write_adjlist(self, string):
		self.f.write("=========================== " + string + " ===========================\n")
		self.f.write("nints\tcolor\tdisp\tspcost\tadjnds\t\t\trmvadjnds\t\t\tspill\n")
		for i1 in range(0, self.nregs):
			i = self.AdjLsts[i1]
			self.f.write("R" + str(i1) + "\t")
			self.f.write("".join(str(i)))
			self.f.write("\n")
		for i1 in range(self.nregs, self.nwebs):
			i = self.AdjLsts[i1]
			self.f.write("S" + str(i1) + "\t")
			self.f.write("".join(str(i)))
			self.f.write("\n")
	
	def write_loop_count(self):
		string = "Loop Counts"
		self.f.write("=========================== " + string + " ===========================\n")
		self.f.write("Blocks\tLoop Count\n")
		for i in self.looping:
			self.f.write(str(i) + "\t" + str(self.looping[i]) + "\n")
	
	def invariant_removal(self):
		for_removal = []
		for j in self.Symreg:
			for defs in self.Symreg[j][1]:
				for i1 in self.natural_loop:
					flag = 0
					for i in self.natural_loop[i1]:
						if defs[0] == i:
							flag = 1
							break;
					if not flag:
						continue		
					flag = 1
					for uses in self.Symreg[j][2]:
						for i in self.natural_loop[i1]:
							if uses[0] == i:
								flag = 0
								break;
					if flag:
						for_removal.append(defs)			

		string = "Loop Invariant"
		self.f.write("=========================== " + string + " ===========================\n")
		
		old_LIR = deepcopy(self.final_code)
		before_LIR = {}
		if for_removal == []:
			self.f.write("Loop Invariant: None\n")
		else:
			for i in for_removal:
				if before_LIR.has_key(i[0]):
					before_LIR[i[0]].append(self.final_code[i[0]][i[1]])
				else:
					before_LIR[i[0]] = []
					before_LIR[i[0]].append(self.final_code[i[0]][i[1]])
				old_LIR[i[0]][i[1]] = []

			self.f.write("----------Block " + str(0) + "----------\n");
			self.f.write("Prologue\n")
		
			blc = old_LIR
			#Writing the blocks
			for i in range(len(blc)-1):
				if before_LIR.has_key(i):
					self.f.write("----------Block " + str(i+1 - 0.5) + "----------\n");
					for j in before_LIR[i]:
						self.f.write("\t".join(j[:3]))
						self.f.write(" ")
						self.f.write(" ".join(j[3:]))
						self.f.write('\n');
					
					
				self.f.write("----------Block " + str(i+1) + "----------\n");
				for j in blc[i]:
					self.f.write("\t".join(j[:3]))
					self.f.write(" ")
					self.f.write(" ".join(j[3:]))
					self.f.write('\n');
			self.f.write("Epilogue\n")
			
				
					
			
			
							
