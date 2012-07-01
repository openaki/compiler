from keywords_suif import *
from copy import deepcopy

class blocker:
	def __init__(self, prog_list):
		self.prog = prog_list
		self.block_map = {}
		self.edge_map = {}
		self.leaders = []
		self.labels = {}
		self.label_block_map = {}
		self.make_label_map()
		self.make_leader_list()
		self.make_block_map()
		self.make_label_block_map()
		self.make_edge_map()
		self.unreachable_removal()
	
	def make_label_map(self):
		i = 0
		while (i < len(self.prog)):
			stat = self.prog[i]
			if(keywords_suif.has_key(stat[1]) == 0): # A seperate map of labels
				if(stat[1][-1] == ':'):
					temp_stat = stat[1].split(':');
				self.labels[temp_stat[0]] = i
			i = i + 1
	
	def make_leader_list(self):
		i = 0
		while (i < len(self.prog)):
			stat = self.prog[i]
	
			if(jump_suif.has_key(stat[1])) : 
				# All the jump + 1 statements are leaders and also the labels
				self.leaders.append(i+1)
				#temp_list = stat[2].split(",")
				temp_word = stat[-1];		
				# The last element for both jmp and conditional jump has label
				self.leaders.append(self.labels[temp_word])
			
			if(stat[1] == 'ret'):
				self.leaders.append(i+1)
			i = i+1
		# Removing Duplicates
		leader_map = {}.fromkeys(self.leaders)
		leader_unique = leader_map.keys()
		# Is there a need to sort ?? -- Yes
		leader_unique.sort()
		self.leaders = leader_unique
		if 0 in self.leaders:
			self.leaders.remove(0)
		
	def make_block_map(self):
		i = 0;
		j = 0;
		while(j < len(self.leaders)):
			temp_list = []
			while(i<self.leaders[j]):
				temp_list.append(self.prog[i])
				i = i+1;
			if(len(temp_list) == 0):
				break;
			self.block_map[j] = temp_list
			j = j+1;

		temp_list = []
		while(i<len(self.prog)):
			temp_list.append(self.prog[i]);
			i = i+1;
		if(len(temp_list) > 0):	
			self.block_map[j] = temp_list
			j = j + 1
		self.block_map[j] = []
		self.end = j
		self.block_map[-1] = []
		
	def make_label_block_map(self):
		for i in self.block_map:
			temp_list1 = self.block_map[i];
			if(len(temp_list1) == 0):
				continue;
			temp_list = temp_list1[0]	
			temp_list2 = temp_list[1].split(':'); 
			
			if(self.labels.has_key(temp_list2[0])):
				self.label_block_map[temp_list2[0]] = i;		
	
	def make_edge_map(self):
		j = 0
		for i in self.block_map:
			if(len(self.block_map[i]) == 0):
				continue
						
			temp_list = self.block_map[i][-1];
			temp_list2 = []
			if(jump_suif.has_key(temp_list[1])):
				if(temp_list[1] == 'jmp'):
					temp_list2.append(self.label_block_map[temp_list[-1]]);
				else:
					#temp_list3 = temp_list[2].split(",")
					temp_word = temp_list[-1];
					temp_list2.append(self.label_block_map[temp_word]);
					temp_list2.append(i+1);
			else:
				if(temp_list[1] == 'ret'):
					temp_list2.append(self.end)
				else:
					temp_list2.append(i+1); #In case no jump statements
			
			self.edge_map[i] = temp_list2
		self.edge_map[-1] = [0]
		self.edge_map[self.end] = []
			
			
	def get_blocks(self):
		return self.block_map
	
	def get_edges(self):
		return self.edge_map
	
	def unreachable_removal(self):
		temp_edge = deepcopy(self.edge_map)
		temp_blocks = deepcopy(self.block_map)
		new_blocks = {}
		new_edge = {}
		conn = self.single_path_dfs(-1, self.edge_map)
		match_map = {}
		j = -1
		for i in range(-1,len(temp_edge)-1):
			if i in conn:
				match_map[i] = j;
				j = j + 1;

		for i in range(-1, len(temp_blocks) - 1):
			 if match_map.has_key(i):
			 	new_blocks[match_map[i]] = self.block_map[i]
				new_edge[match_map[i]] = self.edge_map[i]			
		
		for i in new_edge:
			temp_edge = deepcopy(new_edge[i])
			for j in temp_edge:
				new_edge[i].remove(j)
				if(match_map.has_key(j)):
					new_edge[i].append(match_map[j])
			new_edge[i].sort()
			new_edge[i].reverse()		
		
		self.edge_map = new_edge
		self.block_map = new_blocks
			
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

if __name__ == "__main__":
	inter = open("intermidiate.txt")
	prog = []

	for i in inter.readlines():
		j_list = i[:-1].split() # removing the trailing \n
		if len(j_list) < 2:
			continue
		if len(j_list) > 3:
			pass
			#j_temp = j_list[2].split(',');
			#j_list[2] = j_temp[0];
		prog.append(j_list)
	
	obj = blocker(prog)
	
