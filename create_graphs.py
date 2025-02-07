import networkx as nx
import numpy as np

from utils import *
from data import *
from args import Args

def create_name(name):
    arg_temp = Args()
    arg_temp.change_dataset(name)

    return create(arg_temp)


def create_graph_class(args):
### load datasets
    graphs=[]
    # Provide Graph Labels
    labels=[]
    nums_classes = 2
    # This is default to none
    num_features = 0
    
    if args.graph_class_dataset == 'type1-v-random':
        # Create a simple binary classification
        # dataset where the model tries to distinguish
        # between type1 graphs (layer trees) and 
        # random n-regular graphs. 
        # Create the type1 graph
        # NOTE: May be hard to learn complete randomness!!
        width = 6
        branch = 3
        height = 10
        for i in range(1000):
            G = layered_tree(width, height, branch_factor=branch)
            graphs.append(G)
            labels.append(0)

        # Create the random 6-regular graphs
        degree = 6
        nodes = 60
        for i in range(1000):
            graphs.append(nx.random_regular_graph(degree, nodes))
            labels.append(1)

        args.max_prev_node = 43 # Could just set to none and let it calculate given it is a random dataset but nahhhh for now
        nums_classes = 2
    elif args.graph_class_dataset == 'type1-v-type2a':
        # Create a simple binary classification
        # dataset where the model tries to distinguish
        # between type1 graphs (layer trees) and 
        # type2a graphs. 
        # Create the type1 graph
        width = 6
        branch = 3
        height = 10
        for i in range(1000):
            G = layered_tree(width, height, branch_factor=branch)
            graphs.append(G)
            labels.append(0)


        for i in range(1000):
            # 50 nodes in all graphs
            graphs.append(ladder_extra(6, 10))
            labels.append(1)

        # Have to see what max_prev nodes is
        args.max_prev_node = 31 # Just for 6,10
        nums_classes = 2

    elif args.graph_class_dataset == 'DD':
        num_features = 89
        
        graphs, labels = Graph_load_batch_graph_class(min_num_nodes=100, max_num_nodes=500, name='DD',
                    node_attributes=False, node_labels=True, num_node_labels=num_features, node_label_shift=True)
        nums_classes = 2
        
        args.max_prev_node = 230
        
    return graphs,labels, nums_classes, num_features



def create(args):
### load datasets
    graphs=[]
    # synthetic graphs
    if args.graph_type=='ladder':
        graphs = []
        for i in range(100, 201):
            graphs.append(nx.ladder_graph(i))
        args.max_prev_node = 10
    elif args.graph_type=='ladder_small':
        graphs = []
        for i in range(2, 11):
            graphs.append(nx.ladder_graph(i))
        args.max_prev_node = 10
    elif args.graph_type == 'ladder_extra':
        graphs = []
        for i in range(1000):
            # 50 nodes in all graphs
            graphs.append(ladder_extra(6, 10))

        # Have to see what max_prev nodes is
        args.max_prev_node = 28 # Just for 6,10
        return graphs
    elif args.graph_type == 'ladder_extra_circular':
        graphs = []
        for i in range(1000):
            # 50 nodes in all graphs
            graphs.append(ladder_extra_circular(6, 10))

        # Have to see what max_prev nodes is!!
        args.max_prev_node = 28 # Just for 6,10
        return graphs
    elif args.graph_type == 'ladder_extra_full_circular':
        graphs = []
        for i in range(1000):
            # 50 nodes in all graphs
            graphs.append(ladder_extra_full_circular(6, 10))

        # Have to see what max_prev nodes is
        args.max_prev_node = 28 # Just for 6,10
        return graphs
    elif args.graph_type.startswith('layer_tree'):
        graphs = []
        width = 6
        branch = 3
        height_indx = args.graph_type.rfind('_') + 1
        height = int(args.graph_type[height_indx:])
        for i in range(1000):
            G = layered_tree(width, height, branch_factor=branch)
            graphs.append(G)

        # Max prev nodes????
        args.max_prev_node = 31 # width = 6, branch = 3
        return graphs
    elif args.graph_type.startswith('ladder_tree'):
        graphs = []
        width = 6
        branch = 2
        height_indx = args.graph_type.rfind('_') + 1
        height = int(args.graph_type[height_indx:])
        for i in range(1000):
            G = ladder_tree(width, height, branch_factor=branch)
            graphs.append(G)

        args.max_prev_node = 28 # width = 6, branch = 2
        return graphs
    elif args.graph_type.startswith('random'):
        indx_degree = int(args.graph_type.find('_')) + 1
        indx_nodes = int(args.graph_type.find('_', indx_degree))

        degree = int(args.graph_type[indx_degree: indx_nodes])
        nodes = int(args.graph_type[indx_nodes + 1: ])

        graphs = []
        for i in range(1000):
            graphs.append(nx.random_regular_graph(degree, nodes))

        # Note we are only using these for testing so shouldn't need this
        return graphs
    elif args.graph_type=='tree':
        print ('Creating tree graphs')
        graphs = []
        for i in range(2,5):
            for j in range(3,5):
                graphs.append(nx.balanced_tree(i,j))
        args.max_prev_node = 256
    elif args.graph_type=='tree_adversarial':
        graphs = []
        # Trees that have not been seen before
        # in the standard 'trees' dataset
        
        # The first set includes trees
        # that have different heights than
        # those in the training data
        heights = [2, 5, 6]
        for i in range(2, 5):
            for h in heights:
                graphs.append(nx.balanced_tree(i, h))
                
        args.max_prev_node = 256
        return graphs
    elif args.graph_type.startswith('tree_r_edge'):
        num_edges_removed = int(args.graph_type[-1])
        # Generate full balanced trees
        print('here')
        for i in range(2, 5):
            for j in range(3, 5):
                graph = nx.balanced_tree(i, j)
                # Get the edges so we can randomly 
                # remove num_edges_removed edges
                for x in range(num_edges_removed):
                    edges = graph.edges()
                    edge = np.random.randint(len(edges))
                    graph.remove_edge(edges[edge][0], edges[edge][1])

                graphs.append(graph)

        args.max_prev_node = 256
        return graphs
    elif args.graph_type.startswith('rary-tree'):
        # Generate all rary-trees for a given
        # r and height of tree.
        r = args.graph_type[-1]
        h = 4 
        graphs = []
        for n in range(1, 2 ** h):
            graphs.append(nx.full_rary_tree(r, n))

        args.max_prev_node = 256 # This doesnt super matter
        return graphs
    elif args.graph_type.startswith('tree_r_node'):
        # Remove n nodes from the graph
        n = int(args.graph_type[-1])
        graphs = []
        for i in range(2, 5):
            for j in range(3, 5):
                graph = nx.balanced_tree(i, j)

                for x in range(n):
                    nodes = graph.nodes()
                    node = np.random.randint(len(nodes))
                    graph.remove_node(nodes[node])

                graphs.append(graph)

        args.max_prev_node = 256
        return graphs
    elif args.graph_type=='caveman':
        # graphs = []
        # for i in range(5,10):
        #     for j in range(5,25):
        #         for k in range(5):
        #             graphs.append(nx.relaxed_caveman_graph(i, j, p=0.1))
        graphs = []
        for i in range(2, 3):
            for j in range(30, 81):
                for k in range(10):
                    graphs.append(caveman_special(i,j, p_edge=0.3))
        args.max_prev_node = 100
    elif args.graph_type=='caveman_small':
        # graphs = []
        # for i in range(2,5):
        #     for j in range(2,6):
        #         for k in range(10):
        #             graphs.append(nx.relaxed_caveman_graph(i, j, p=0.1))
        graphs = []
        for i in range(2, 3):
            for j in range(6, 11):
                for k in range(20):
                    graphs.append(caveman_special(i, j, p_edge=0.8)) # default 0.8
        args.max_prev_node = 20
    elif args.graph_type=='caveman_small_single':
        # graphs = []
        # for i in range(2,5):
        #     for j in range(2,6):
        #         for k in range(10):
        #             graphs.append(nx.relaxed_caveman_graph(i, j, p=0.1))
        graphs = []
        for i in range(2, 3):
            for j in range(8, 9):
                for k in range(100):
                    graphs.append(caveman_special(i, j, p_edge=0.5))
        args.max_prev_node = 20
    elif args.graph_type.startswith('community'):
        num_communities = int(args.graph_type[-1])
        print('Creating dataset with ', num_communities, ' communities')
        c_sizes = np.random.choice([12, 13, 14, 15, 16, 17], num_communities)
        #c_sizes = [15] * num_communities
        for k in range(3000):
            graphs.append(n_community(c_sizes, p_inter=0.01))
        args.max_prev_node = 80
    elif args.graph_type=='grid':
        graphs = []
        for i in range(10,20):
            for j in range(10,20):
                graphs.append(nx.grid_2d_graph(i,j))
        args.max_prev_node = 40
    elif args.graph_type=='grid_small':
        graphs = []
        for i in range(2,5):
            for j in range(2,6):
                graphs.append(nx.grid_2d_graph(i,j))
        args.max_prev_node = 15
    elif args.graph_type=='barabasi':
        graphs = []
        for i in range(100,200):
             for j in range(4,5):
                 for k in range(5):
                    graphs.append(nx.barabasi_albert_graph(i,j))
        args.max_prev_node = 130
    elif args.graph_type=='barabasi_small':
        graphs = []
        for i in range(4,21):
             for j in range(3,4):
                 for k in range(10):
                    graphs.append(nx.barabasi_albert_graph(i,j))
        args.max_prev_node = 20
    elif args.graph_type=='grid_big':
        graphs = []
        for i in range(36, 46):
            for j in range(36, 46):
                graphs.append(nx.grid_2d_graph(i, j))
        args.max_prev_node = 90

    elif 'barabasi_noise' in args.graph_type:
        graphs = []
        for i in range(100,101):
            for j in range(4,5):
                for k in range(500):
                    graphs.append(nx.barabasi_albert_graph(i,j))
        graphs = perturb_new(graphs,p=args.noise/10.0)
        args.max_prev_node = 99

    # real graphs
    elif args.graph_type == 'enzymes':
        graphs= Graph_load_batch(min_num_nodes=10, name='ENZYMES', node_attributes=True,node_labels=True)
        args.max_prev_node = 25
    elif args.graph_type == 'enzymes_small':
        graphs_raw = Graph_load_batch(min_num_nodes=10, name='ENZYMES')
        graphs = []
        for G in graphs_raw:
            if G.number_of_nodes()<=20:
                graphs.append(G)
        args.max_prev_node = 15
    elif args.graph_type.startswith('enzymes'):
        graph_label = int(args.graph_type[-1])
        graphs= Graph_load_label(min_num_nodes=10, name='ENZYMES', node_attributes=True,node_labels=True, graph_label=graph_label)
        args.max_prev_node = 25

    elif args.graph_type == 'protein':
        graphs = Graph_load_batch(min_num_nodes=20, name='PROTEINS_full')
        args.max_prev_node = 80

    elif args.graph_type == 'DD':
        graphs = Graph_load_batch(min_num_nodes=100, max_num_nodes=500, name='DD',node_attributes=False, node_labels=True)
        args.max_prev_node = 230
    elif args.graph_type.startswith('DD'):
        graph_label = int(args.graph_type[-1])
        graphs= Graph_load_label(min_num_nodes=100, max_num_nodes=500, name='DD', node_attributes=False,node_labels=True, graph_label=graph_label)
        args.max_prev_node = 230

    elif args.graph_type == 'AIDS': # Definitely check! Maybe train on inactive and test on active so train on 1!
        # Gotta calc this!
        graphs = Graph_load_batch(min_num_nodes=2, max_num_nodes=100, name='AIDS',node_attributes=False,node_labels=True)
        args.max_prev_node = 16
    elif args.graph_type.startswith('AIDS'):
        graph_label = int(args.graph_type[-1])
        graphs= Graph_load_label(min_num_nodes=2, max_num_nodes=100, name='AIDS', node_attributes=False,node_labels=True, graph_label=graph_label)
        args.max_prev_node = 16

    elif args.graph_type == 'Fingerprint': # Not so great to train on because the graph classes include several graph labels
        # Gotta calc this!
        graphs = Graph_load_batch(min_num_nodes=2, max_num_nodes=26, name='Fingerprint',node_attributes=True, node_labels=False)
        args.max_prev_node = 6
    elif args.graph_type.startswith('Fingerprint'):
        graph_label = int(args.graph_type[-1])
        graphs= Graph_load_label(min_num_nodes=2, max_num_nodes=26, name='Fingerprint', node_attributes=True,node_labels=False, graph_label=graph_label)
        args.max_prev_node = 6

    elif args.graph_type == 'COLLAB': # Interesting to try but may be quite slow
        # Gotta calc this!
        graphs = Graph_load_batch(min_num_nodes=32, max_num_nodes=492, name='COLLAB',node_attributes=False, node_labels=False)
        args.max_prev_node = 480
    elif args.graph_type.startswith('COLLAB'):
        graph_label = int(args.graph_type[-1])
        graphs= Graph_load_label(min_num_nodes=32, max_num_nodes=492, name='COLLAB', node_attributes=False,node_labels=False, graph_label=graph_label)
        args.max_prev_node = 480

    elif args.graph_type == 'IMDB-MULTI': #Definitely try!!
        # Gotta calc this!
        graphs = Graph_load_batch(min_num_nodes=7, max_num_nodes=89, name='IMDB-MULTI',node_attributes=False, node_labels=False)
        args.max_prev_node = 86
    elif args.graph_type.startswith('IMDB-MULTI'):
        graph_label = int(args.graph_type[-1])
        graphs= Graph_load_label(min_num_nodes=7, max_num_nodes=89, name='IMDB-MULTI', node_attributes=False,node_labels=False, graph_label=graph_label)
        args.max_prev_node = 86

    elif args.graph_type == 'REDDIT-MULTI-12K': # Not done yet may be too large to really try, Maybe want to limit max
        # Gotta calc this! # Try max = 500
        graphs = Graph_load_batch(min_num_nodes=2, max_num_nodes=500, name='REDDIT-MULTI-12K',node_attributes=False, node_labels=False)
        args.max_prev_node = 3061
    elif args.graph_type.startswith('REDDIT-MULTI-12K'):
        graph_label = int(args.graph_type[-1])
        graphs= Graph_load_label(min_num_nodes=2, max_num_nodes=3782, name='REDDIT-MULTI-12K', node_attributes=False,node_labels=False, graph_label=graph_label)
        args.max_prev_node = 3061

    elif args.graph_type == 'Letter-high': # Could be quite interesting to look at. For example train on low distortion and test on med/high and diff letters
        # Gotta calc this!
        graphs = Graph_load_batch(min_num_nodes=2, max_num_nodes=9, name='Letter-high',node_attributes=True, node_labels=False)
        args.max_prev_node = 6
    elif args.graph_type.startswith('Letter-high'):
        graph_label = int(args.graph_type[-1])
        graphs= Graph_load_label(min_num_nodes=2, max_num_nodes=9, name='Letter-high', node_attributes=True,node_labels=False, graph_label=graph_label)
        args.max_prev_node = 6

    elif args.graph_type == 'Letter-med': 
        # Gotta calc this!
        graphs = Graph_load_batch(min_num_nodes=2, max_num_nodes=9, name='Letter-med',node_attributes=True, node_labels=False)
        args.max_prev_node = 5
    elif args.graph_type.startswith('Letter-med'):
        graph_label = int(args.graph_type[-1])
        graphs= Graph_load_label(min_num_nodes=2, max_num_nodes=9, name='Letter-med', node_attributes=True,node_labels=False, graph_label=graph_label)
        args.max_prev_node = 5

    elif args.graph_type == 'Letter-low': # For a specific letter may want to try for example the letter N
        # Gotta calc this!
        graphs = Graph_load_batch(min_num_nodes=2, max_num_nodes=8, name='Letter-low',node_attributes=True, node_labels=False)
        args.max_prev_node = 5
    elif args.graph_type.startswith('Letter-low'):
        graph_label = int(args.graph_type[-1])
        graphs= Graph_load_label(min_num_nodes=2, max_num_nodes=8, name='Letter-low', node_attributes=True,node_labels=False, graph_label=graph_label)
        args.max_prev_node = 5

    elif args.graph_type == 'citeseer':
        _, _, G = Graph_load(dataset='citeseer')
        G = max(nx.connected_component_subgraphs(G), key=len)
        G = nx.convert_node_labels_to_integers(G)
        graphs = []
        for i in range(G.number_of_nodes()):
            G_ego = nx.ego_graph(G, i, radius=3)
            if G_ego.number_of_nodes() >= 50 and (G_ego.number_of_nodes() <= 400):
                graphs.append(G_ego)
        args.max_prev_node = 250
    elif args.graph_type == 'citeseer_small':
        _, _, G = Graph_load(dataset='citeseer')
        G = max(nx.connected_component_subgraphs(G), key=len)
        G = nx.convert_node_labels_to_integers(G)
        graphs = []
        for i in range(G.number_of_nodes()):
            G_ego = nx.ego_graph(G, i, radius=1)
            if (G_ego.number_of_nodes() >= 4) and (G_ego.number_of_nodes() <= 20):
                graphs.append(G_ego)
        shuffle(graphs)
        graphs = graphs[0:200]
        args.max_prev_node = 15

    return graphs


# Define a useful function for getting the dataset to test/analyze
def get_graph_data(dataset, isModelDataset=False):
    """
        Given a dataset name, loads in the graphs of that dataset.
        Creates a specific argument object for that dataset to allow
        for different datasets to be created.
        
        return: If isModelDataset: returns args, train, val, test split
                else: returgn args, data
    """
    args_data = Args()
    args_data.change_dataset(dataset)
    
    # Load the graph data - Consider using presaved datasets! with graph load list
    graphs = create(args_data)
    graphs_len = len(graphs)
    random.seed(123)
    shuffle(graphs)

    # Display some graph stats
    graph_node_avg = 0
    for graph in graphs:
        graph_node_avg += graph.number_of_nodes()
    graph_node_avg /= graphs_len
    print('Average num nodes', graph_node_avg)

    args_data.max_num_node = max([graphs[i].number_of_nodes() for i in range(graphs_len)])
    max_num_edge = max([graphs[i].number_of_edges() for i in range(graphs_len)])
    min_num_edge = min([graphs[i].number_of_edges() for i in range(graphs_len)])

    # show graphs statistics
    print('total graph num: {}'.format(graphs_len))
    print('max number node: {}'.format(args_data.max_num_node))
    print('max/min number edge: {}; {}'.format(max_num_edge,min_num_edge))
    print('max previous node: {}'.format(args_data.max_prev_node))
    
    if isModelDataset:
        # split datasets
        graphs_len = len(graphs)
        graphs_test = graphs[int(0.8 * graphs_len):]
        graphs_train = graphs[0:int(0.8*graphs_len)]
        graphs_validate = graphs[0:int(0.2*graphs_len)]
        return args_data, graphs_train, graphs_validate, graphs_test
    
    return args_data, graphs

def create_named(name):
### load datasets
    graphs=[]
    max_prev_node=0
    # synthetic graphs
    if name =='ladder':
        graphs = []
        for i in range(100, 201):
            graphs.append(nx.ladder_graph(i))
        max_prev_node = 10
    elif name=='ladder_small':
        graphs = []
        for i in range(2, 11):
            graphs.append(nx.ladder_graph(i))
        max_prev_node = 10
    elif name=='tree':
        print ('Creating tree graphs')
        graphs = []
        for i in range(2,5):
            for j in range(3,5):
                graphs.append(nx.balanced_tree(i,j))
        max_prev_node = 256
    elif name=='tree_adversarial':
        graphs = []
        # Trees that have not been seen before
        # in the standard 'trees' dataset
        
        # The first set includes trees
        # that have different heights than
        # those in the training data
        heights = [2, 5, 6]
        for i in range(2, 5):
            for h in heights:
                graphs.append(nx.balanced_tree(i, h))
                
        # More later! 
        
    elif name=='caveman':
        # graphs = []
        # for i in range(5,10):
        #     for j in range(5,25):
        #         for k in range(5):
        #             graphs.append(nx.relaxed_caveman_graph(i, j, p=0.1))
        graphs = []
        for i in range(2, 3):
            for j in range(30, 81):
                for k in range(10):
                    graphs.append(caveman_special(i,j, p_edge=0.3))
        max_prev_node = 100
    elif name=='caveman_small':
        # graphs = []
        # for i in range(2,5):
        #     for j in range(2,6):
        #         for k in range(10):
        #             graphs.append(nx.relaxed_caveman_graph(i, j, p=0.1))
        graphs = []
        for i in range(2, 3):
            for j in range(6, 11):
                for k in range(20):
                    graphs.append(caveman_special(i, j, p_edge=0.8)) # default 0.8
        max_prev_node = 20
    elif name=='caveman_small_single':
        # graphs = []
        # for i in range(2,5):
        #     for j in range(2,6):
        #         for k in range(10):
        #             graphs.append(nx.relaxed_caveman_graph(i, j, p=0.1))
        graphs = []
        for i in range(2, 3):
            for j in range(8, 9):
                for k in range(100):
                    graphs.append(caveman_special(i, j, p_edge=0.5))
        max_prev_node = 20
    elif name.startswith('community'):
        num_communities = int(name[-1])
        print('Creating dataset with ', num_communities, ' communities')
        c_sizes = np.random.choice([12, 13, 14, 15, 16, 17], num_communities)
        #c_sizes = [15] * num_communities
        for k in range(3000):
            graphs.append(n_community(c_sizes, p_inter=0.01))
        max_prev_node = 80
    elif name=='grid':
        graphs = []
        for i in range(10,20):
            for j in range(10,20):
                graphs.append(nx.grid_2d_graph(i,j))
        max_prev_node = 40
    elif name=='grid_small':
        graphs = []
        for i in range(2,5):
            for j in range(2,6):
                graphs.append(nx.grid_2d_graph(i,j))
        max_prev_node = 15
    elif name=='barabasi':
        graphs = []
        for i in range(100,200):
             for j in range(4,5):
                 for k in range(5):
                    graphs.append(nx.barabasi_albert_graph(i,j))
        max_prev_node = 130
    elif name=='barabasi_small':
        graphs = []
        for i in range(4,21):
             for j in range(3,4):
                 for k in range(10):
                    graphs.append(nx.barabasi_albert_graph(i,j))
        max_prev_node = 20
    elif name=='grid_big':
        graphs = []
        for i in range(36, 46):
            for j in range(36, 46):
                graphs.append(nx.grid_2d_graph(i, j))
        max_prev_node = 90

    elif 'barabasi_noise' in name:
        # Broken!
        graphs = []
        for i in range(100,101):
            for j in range(4,5):
                for k in range(500):
                    graphs.append(nx.barabasi_albert_graph(i,j))
        #graphs = perturb_new(graphs,p=args.noise/10.0)
        max_prev_node = 99

    # real graphs
    elif name == 'enzymes':
        graphs= Graph_load_batch(min_num_nodes=10, name='ENZYMES')
        max_prev_node = 25
    elif name == 'enzymes_small':
        graphs_raw = Graph_load_batch(min_num_nodes=10, name='ENZYMES')
        graphs = []
        for G in graphs_raw:
            if G.number_of_nodes()<=20:
                graphs.append(G)
        max_prev_node = 15
    elif name == 'protein':
        graphs = Graph_load_batch(min_num_nodes=20, name='PROTEINS_full')
        max_prev_node = 80
    elif name == 'DD':
        graphs = Graph_load_batch(min_num_nodes=100, max_num_nodes=500, name='DD',node_attributes=False,graph_labels=True)
        max_prev_node = 230
    elif name == 'citeseer':
        _, _, G = Graph_load(dataset='citeseer')
        G = max(nx.connected_component_subgraphs(G), key=len)
        G = nx.convert_node_labels_to_integers(G)
        graphs = []
        for i in range(G.number_of_nodes()):
            G_ego = nx.ego_graph(G, i, radius=3)
            if G_ego.number_of_nodes() >= 50 and (G_ego.number_of_nodes() <= 400):
                graphs.append(G_ego)
        max_prev_node = 250
    elif name == 'citeseer_small':
        _, _, G = Graph_load(dataset='citeseer')
        G = max(nx.connected_component_subgraphs(G), key=len)
        G = nx.convert_node_labels_to_integers(G)
        graphs = []
        for i in range(G.number_of_nodes()):
            G_ego = nx.ego_graph(G, i, radius=1)
            if (G_ego.number_of_nodes() >= 4) and (G_ego.number_of_nodes() <= 20):
                graphs.append(G_ego)
        shuffle(graphs)
        graphs = graphs[0:200]
        max_prev_node = 15

    return graphs
