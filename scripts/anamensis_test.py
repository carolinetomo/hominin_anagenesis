import mandos
import sys

if len(sys.argv) != 5:
    print "python "+sys.argv[0]+" <tree> <alignment> <partitions file> <range data file>"
    sys.exit(0)

infile = sys.argv[1]
tree = mandos.tree_utils2.read_tree(infile)

seqs = mandos.tree_utils2.read_phylip_file(sys.argv[2])
parts = sys.argv[3]
sitels = mandos.tree_utils2.read_partition_file(parts)

ranges = mandos.tree_utils2.read_strat(sys.argv[4])
mandos.tree_utils2.match_strat(tree,ranges)
mandos.tree_utils2.init_heights_strat(tree)

taxa = ["Australopithecus_anamensis","Australopithecus_afarensis"]
subtree = mandos.tree_utils2.prune_SA(tree,taxa)

print "calculating AIC of bifurcating arrangement"
print subtree.get_newick_repr(True)
morpholike = mandos.tree_likelihood_calculator.calc_mk_like(sitels,subtree,seqs,True,True,numstates=5)
opt = mandos.stratoML.optim_lambda_heights(subtree,ranges,True)
print subtree.get_newick_repr(True)
strat_like = -opt[1][1]
print strat_like,morpholike
combined = strat_like + morpholike
#print subtree.nnodes("all")
print (2*(6))-(2*combined)

print "making SA and calculating AIC"
taxa = "Australopithecus_anamensis"
subtree = mandos.tree_utils2.make_ancestor(subtree,taxa)
print subtree.get_newick_repr(True)
morpholike = mandos.tree_likelihood_calculator.calc_mk_like(sitels,subtree,seqs,True,True,numstates=5)
opt = mandos.stratoML.optim_lambda_heights(subtree,ranges,True)
print subtree.get_newick_repr(True)
strat_like = -opt[1][1]
print strat_like,morpholike
combined = strat_like + morpholike

print (2*(6))-(2*combined)

"""
When combining, the number of parameters (_k_) should be
        
        num_nodes+num_tips + num_branch_lengths + morph_parameters + strat_parameters

so here:
    45+
"""
