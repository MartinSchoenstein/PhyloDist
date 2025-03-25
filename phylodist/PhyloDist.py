import phylodist.distances as dst
import phylodist.pre_processing as pp
import warnings
warnings.filterwarnings('ignore')


# Main function of the library, allows access to 7 metrics for comparing phylogenetic profiles
def distance_profiles(
    method,                 #Name of the distance method to use : "Jaccard", "Hamming", "Pearson", "MI", "PCS", "Cotransition", "Svd_phy"
    x,                      #Data to use
    y=None,                 #Second date source if you want to compare the x profils to y profils and not all x profils to all x profils
    type = "matrix",        #Type of data source, classic profils matrix or transition vectors matrix
    #subset_prot=None,
    confidence=1.5,         #PCS parameter, influence the value of a double match
    penalty=0.6,            #PCS parameter, influence the value of a doouble missmatch
    truncation= 0.5,        #SVD-phy parameter, influence the data reduction
    consecutive = True,     #Cotransition score parameter, when =False only counts one transition in 2 directly consecutive ones
    tree = None,            #Newick tree to order profils for PCS or Cotransition score
    path = None             #Path to download distance dataframe
):
    if method not in ["Jaccard", 'jaccard', "Hamming", 'hamming', "Pearson", 'pearson', "MI", 'mi', "Cotransition", 'cotransition', "PCS", 'pcs', "SVD_phy", 'svd_phy']:
        raise ValueError("Method not accepted")
    if method in ["Cotransition", 'cotransition', "PCS", 'pcs'] and tree == None:
        if type not in ["Transition_vector", "Transition vector", "transition_vector", "transition vector"]:
            raise ValueError("Tree needed for this method")
    if type not in ["matrix", "Matrix", "Transition_vector", "Transition vector", "transition_vector", "transition vector"]:
        raise ValueError("type must be matrix or transition_vector")
    if method in ["SVD_phy", 'svd_phy'] and y != None:
        raise ValueError("SVD_phy only accepts 1 matrix")
    dfx, binary_x = pp.input(x)
    if y is None:
        dfy = None
        print(len(dfx), " profiles loaded into ", method, " distance.")
    else:
        dfy = pp.input(y, test_binary = False)
        print(len(dfx) + len(dfy), " profiles loaded into ", method, " distance.")
    if method in ["Jaccard", 'jaccard', "Hamming", 'hamming', "Cotransition", 'cotransition', "PCS", 'pcs'] and binary_x == False:
        dfx = pp.to_binary(dfx)
        if dfy is not None:
            dfy = pp.to_binary(dfy)
        print("Profiles were not binary, to_binary() was applied with 0.5 for threshold")
    print("Running...")
    if method == "Jaccard" or method == "jaccard":
        result = dst.jaccard(dfx, dfy)
    if method == "Hamming" or method == "hamming":
        result = dst.hamming(dfx, dfy) 
    if method == "Pearson" or method == "pearson":
        result = dst.pearson(dfx, dfy)
    if method == "MI" or method == "mi":
        result = dst.mi(dfx, dfy)
    if method == "cotransition" or method == "Cotransition":
        if type == "matrix":
            ordered_dfx = pp.order_by_tree(dfx, tree)
            tvx = pp.transition_vector(ordered_dfx, from_outside = False)
            if dfy is None :
                ordered_dfy = None
                tvy = None
            else :
                ordered_dfy = pp.order_by_tree(dfy, tree)
                tvy = pp.transition_vector(ordered_dfy, from_outside = False)
        else:
            tvx = dfx
            tvy = None
        result, p_value = dst.cotransition(tvx, tvy, consecutive)
    if method == "pcs" or method == "PCS":
        if type == "matrix":
            ordered_dfx = pp.order_by_tree(dfx, tree)
            tvx = pp.transition_vector(ordered_dfx, from_outside = False)
            if dfy is None :
                ordered_dfy = None
                tvy = None
            else :
                ordered_dfy = pp.order_by_tree(dfy, tree)
                tvy = pp.transition_vector(ordered_dfy, from_outside = False)
        else:
            tvx = dfx
            tvy = None
        result = dst.pcs(tvx, tvy, confidence, penalty)
    if method == "svd_phy" or method == "SVD_phy":
        result = dst.SVD_phy(dfx, truncation)
    if path is not None:
        if method == "cotransition" or method == "Cotransition":
            p_value.to_csv(path, index = True)
        result.to_csv(path, index=True),
    return result
