from keywords_suif import *
from blocker_class import blocker
#from register_alloc import register_alloc
from optimization_class import optimization
from cparse import *
from copy import deepcopy

def put_equal(fil):
	for i in range(63):
		f.write("=")

if __name__ == "__main__":
	import sys
	file = open(sys.argv[1])
	lines = file.readlines()
	file.close()
	strings = ""
	for i in lines:
		strings += i
    #lex.input(strings)
	#yacc.parse(strings)
	run_parser()
	write_file()
	inter = open("inter_suif.txt")
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
	blc =  obj.get_blocks()
	edg =  obj.get_edges()
	obj2 = optimization(blc, edg, dict_var)
	f = open("inter.txt", "w")
	f_LIR = open("LIR.txt", "w")
	f_LIR.write("\n\n============Basic Blocks===============\n\n")
	f_LIR.write("----------Block " + str(0) + "----------\n");
	f_LIR.write("Prologue\n")
	
	#Writing the blocks
	for i in range(len(obj2.LIR)-1):
		f_LIR.write("\n")
		f_LIR.write("----------Block " + str(i+1) + "----------\n");
		for j in obj2.LIR[i]:
			f_LIR.write("\t".join(j[:3]))
			f_LIR.write(" ")
			f_LIR.write(" ".join(j[3:]))
			f_LIR.write('\n');
	f_LIR.write("Epilogue\n")
	f_LIR.close()

	f.write("PROCEDURE " + get_proc_name() + ":\n")
	f.write("\n\n============Basic Blocks===============\n\n")
	f.write("----------Block " + str(0) + "----------\n");
	f.write("Prologue\n")
	
	#Writing the blocks
	for i in range(len(blc)-1):
		f.write("\n")
		f.write("----------Block " + str(i+1) + "----------\n");
		for j in blc[i]:
			f.write("\t".join(j[:3]))
			f.write(" ")
			f.write(" ".join(j[3:]))
			f.write('\n');
	f.write("Epilogue\n")
	
	f.write("\nNUMBER OF NODES %d"%(len(blc)));
	cnt = 0;
	for i in range(-1,len(edg)-1):
		for j in edg[i]:
			cnt = cnt + 1;
	
	f.write("\nNUMBER OF EDGES %d"%(cnt));
		
	#writing the edges Do not forget to add one to all the edges
	f.write("\n\nEDGES:")
	
	for i in range(-1,len(edg)-1):
		for j in edg[i]:
			f.write("\n")
			f.write("%d --> %d"%(i+1, j+1));
	f.write("\n\n")
	
	# Immidiate Predecessor
	pred = obj2.reverse_edges		
	put_equal(f);
	f.write("Immediate Predecessor Set\n")
	f.write("\n\nBlocks Immediate Predecessors")
	#f.write("0\tNone");
			
	for i in range(-1,len(pred)-1):
		f.write("\n%d\t\t"%(i+1))
		if pred[i] == []:
			f.write("None")
		pred[i].sort();
		pred[i].reverse();
		for j in pred[i]:
			f.write("%d  "%(j+1));
	
	## Sucessor Set

	f.write("\n\n")
	pred = deepcopy(edg)		
	put_equal(f);
	f.write("Immediate Sucessor Set\n")
	f.write("\n\nBlocks\tImmediate Sucessors")
			
	for i in range(-1,len(pred)-1):
		f.write("\n%d\t\t"%(i+1))
		if pred[i] == []:
			f.write("None")
		pred[i].sort();
		pred[i].reverse();
		for j in pred[i]:
			f.write("%d  "%(j+1));
	
	## Domintors

	f.write("\n\n")
	pred = obj2.dominated		
	put_equal(f);
	f.write("Dominators\n")
	f.write("\n\nBlocks\tDominates")
			
	for i in range(-1,len(pred)-1):
		f.write("\n%d\t\t"%(i+1))
		if pred[i] == []:
			f.write("None")
		pred[i].sort();
		pred[i].reverse();
		for j in pred[i]:
			f.write("%d  "%(j+1));
	## Dominted

	## post dominators
	f.write("\n\n")
	pred = obj2.get_ipdom()
	put_equal(f);
	f.write("Immediate Post Dominators Set\n")
	f.write("\n\nBlocks\tImmidiate Postdominators")
			
	for i in range(-1,len(pred)-1):
		f.write("\n%d\t\t"%(i+1))
		if pred[i] == []:
			f.write("None")
		pred[i].sort();
		pred[i].reverse();
		for j in pred[i]:
			f.write("%d  "%(j+1));
	
	## Forward Edge
	flag = 0;
	f.write("\n\n")
	pred = deepcopy(obj2.forward_edges)		
	put_equal(f);
	k = 0
	f.write("Forward Edges\n")
	for i in range(-1,len(pred)-1):
		for j in pred[i]:
			flag = 1
			k = k + 1
			f.write("\n")
			f.write("%d : %d --> %d"%(k, i+1, j+1));
	if flag == 0:
		f.write("\nNone");
	
	## Back Edge
	flag = 0;
	f.write("\n\n")
	pred = deepcopy(obj2.backward_edges)		
	put_equal(f);
	k = 0
	f.write("Back Edges\n")
	for i in range(-1,len(pred)-1):
		for j in pred[i]:
			flag = 1
			k = k + 1
			f.write("\n")
			f.write("%d : %d --> %d"%(k, i+1, j+1));
	if flag == 0:
		f.write("\nNone");
	
	## cross Edge
	flag = 0
	f.write("\n\n")
	pred = deepcopy(obj2.cross_edges)		
	put_equal(f);
	k = 0
	f.write("Cross Edges\n")
	for i in range(-1,len(pred)-1):
		for j in pred[i]:
			flag = 1;
			k = k + 1;
			f.write("\n")
			f.write("%d : %d --> %d"%(k, i+1, j+1));
	if flag == 0:
		f.write("\nNone");
	
	## Loops
	flag = 0
	f.write("\n\n")
	pred = deepcopy(obj2.natural_loop)		
	put_equal(f);
	f.write("Natural Loops\n")
	for i in range(1,len(pred)+1):
		f.write("\n")
		f.write("%d :\t" %(i))
		for j in pred[i]:
			flag = 1;
			f.write("%d "%(j+1));
	if flag == 0:
		f.write("\nNone");

	f.write("\n\n")
	
