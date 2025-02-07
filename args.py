
### program configuration
class Args():
    def __init__(self):
        ### if clean tensorboard
        self.clean_tensorboard = False
        ### Which CUDA GPU device is used for training
        #self.cuda = 2 / unused
        self.train_all = False

        ### Which GraphRNN model variant is used.
        # The simple version of Graph RNN
        # self.note = 'GraphRNN_MLP'
        # The dependent Bernoulli sequence version of GraphRNN
        self.note = 'GraphRNN_RNN'

        # Which dataset to use for graph classification
        #self.graph_class_dataset = 'type1-v-random'
        #self.graph_class_dataset = 'type1-v-type2a'
        self.graph_class_dataset = 'DD'

        # The relative weighting assigned to the generative modeling
        # objective in the graph classification combined loss
        self.gen_weight = 1 # Play with this!
        self.classification_weight = 1

        self.MLP = False
        self.dropout = False # Dropout does not work well sadly
        self.bn = False
        # If we should have a seperate linear layer 
        # just for the node features!
        self.feature_pre = True
        
        self.node_features = True
        # Specifies whether we have node features match
        # the adjacency row, or whether we lead by one node!
        # False: means we lead by one
        # True: match node features
        self.current_node_feats = False

        ## for comparison, removing the BFS compoenent
        # self.note = 'GraphRNN_MLP_nobfs'
        # self.note = 'GraphRNN_RNN_nobfs'

        ### Which dataset is used to train the model
        #self.graph_type = 'DD'
        #self.graph_type = 'DD_1'

        #self.graph_type = 'AIDS'
        #self.graph_type = 'AIDS_1'

        #self.graph_type = 'Fingerprint'
        #self.graph_type = 'Fingerprint_1'

        #self.graph_type = 'COLLAB'
        #self.graph_type = 'COLLAB_1'

        #self.graph_type = 'IMDB-MULTI'
        #self.graph_type = 'IMDB-MULTI_1'

        #self.graph_type = 'Letter-high'
        #self.graph_type = 'Letter-high_0'

        #self.graph_type = 'Letter-med'
        #self.graph_type = 'Letter-med'

        #self.graph_type = 'Letter-low'
        #self.graph_type = 'Letter-low_1' # N

        #self.graph_type = 'REDDIT-MULTI-12K'
        #self.graph_type = 'REDDIT-MULTI-12K_1'

        # self.graph_type = 'caveman'
        # self.graph_type = 'caveman_small'
        # self.graph_type = 'caveman_small_single'
        # self.graph_type = 'community4'
        #self.graph_type = 'grid'
        # self.graph_type = 'grid_small'
        #self.graph_type = 'ladder'
        self.graph_type = 'ladder_small'
        #self.graph_type = 'tree'
        #self.graph_type = 'tree_r_edge_1'
        #self.graph_type = 'layer-tree_40'

        #self.graph_type = 'ladder_tree_10'
        #self.graph_type = 'ladder_extra_full_circular'
        #self.graph_type = 'ladder_extra'

        #self.graph_type = 'enzymes'
        #self.graph_type = 'enzymes_1'
        #self.graph_type = 'enzymes_small'
        # self.graph_type = 'barabasi'
        # self.graph_type = 'barabasi_small'
        # self.graph_type = 'citeseer'
        # self.graph_type = 'citeseer_small'

        # self.graph_type = 'barabasi_noise'
        # self.noise = 10
        #
        # if self.graph_type == 'barabasi_noise':
        #     self.graph_type = self.graph_type+str(self.noise)

        # if none, then auto calculate
        self.max_num_node = None # max number of nodes in a graph
        self.max_prev_node = None # max previous node that looks back

        ### network config
        ## GraphRNN
        if 'small' in self.graph_type:
            self.parameter_shrink = 2
        else:
            self.parameter_shrink = 1
        self.hidden_size_rnn = int(128/self.parameter_shrink) # hidden size for main RNN
        self.hidden_size_rnn_output = 16 # hidden size for output RNN
        self.embedding_size_rnn = int(64/self.parameter_shrink) # the size for LSTM input
        self.embedding_size_rnn_output = 8 # the embedding size for output rnn
        self.embedding_size_output = int(64/self.parameter_shrink) # the embedding size for output (VAE/MLP)

        self.batch_size = 32 # normal: 32, and the rest should be changed accordingly
        self.test_batch_size = 32
        self.test_total_size = 1000
        self.num_layers = 4

        ### training config
        self.num_workers = 4 # num workers to load data, default 4
        self.batch_ratio = 32 # how many batches of samples per epoch, default 32, e.g., 1 epoch = 32 batches
        self.epochs = 500 #was 3000 # now one epoch means self.batch_ratio x batch_size
        self.epochs_test_start = 1 # was 100
        self.epochs_test = 1 # was 100
        self.epochs_log = 1 # was 100
        self.epochs_save = 100 # was 100

        self.lr = 0.003
        self.milestones = [100, 400] # was 400, 1000
        self.lr_rate = 0.3

        self.scheduler = 'cos'

        self.sample_time = 2 # sample time in each time step, when validating

        ### output config
        # self.dir_input = "/dfs/scratch0/jiaxuany0/"
        self.dir_input = "./"
        self.model_save_path = self.dir_input+'model_save/' # only for nll evaluation
        self.graph_save_path = self.dir_input+'graphs/'
        self.figure_save_path = self.dir_input+'figures/'
        self.timing_save_path = self.dir_input+'timing/'
        self.figure_prediction_save_path = self.dir_input+'figures_prediction/'
        self.nll_save_path = self.dir_input+'nll/'


        self.load = False # if load model, default lr is very low
        self.load_epoch = 100
        self.save = True


        ### baseline config
        # self.generator_baseline = 'Gnp'
        self.generator_baseline = 'BA'

        # self.metric_baseline = 'general'
        # self.metric_baseline = 'degree'
        self.metric_baseline = 'clustering'


        ### filenames to save intemediate and final outputs
        self.fname = self.note + '_' + self.graph_type + '_' + str(self.num_layers) + '_' + str(self.hidden_size_rnn) + '_'
        self.fname_pred = self.note+'_'+self.graph_type+'_'+str(self.num_layers)+'_'+ str(self.hidden_size_rnn)+'_pred_'
        self.fname_train = self.note+'_'+self.graph_type+'_'+str(self.num_layers)+'_'+ str(self.hidden_size_rnn)+'_train_'
        self.fname_test = self.note + '_' + self.graph_type + '_' + str(self.num_layers) + '_' + str(self.hidden_size_rnn) + '_test_'
        self.fname_baseline = self.graph_save_path + self.graph_type + self.generator_baseline+'_'+self.metric_baseline
    
    def change_dataset(self, dataset):
        self.graph_type = dataset
        
        # Re-configure the network if necessary
        if 'small' in self.graph_type:
            self.parameter_shrink = 2
        else:
            self.parameter_shrink = 1
        self.hidden_size_rnn = int(128/self.parameter_shrink) # hidden size for main RNN
        self.embedding_size_rnn = int(64/self.parameter_shrink) # the size for LSTM input
        self.embedding_size_output = int(64/self.parameter_shrink) # the embedding size for output (VAE/MLP)
        
        self.fname = self.note + '_' + self.graph_type + '_' + str(self.num_layers) + '_' + str(self.hidden_size_rnn) + '_'
        self.fname_pred = self.note+'_'+self.graph_type+'_'+str(self.num_layers)+'_'+ str(self.hidden_size_rnn)+'_pred_'
        self.fname_train = self.note+'_'+self.graph_type+'_'+str(self.num_layers)+'_'+ str(self.hidden_size_rnn)+'_train_'
        self.fname_test = self.note + '_' + self.graph_type + '_' + str(self.num_layers) + '_' + str(self.hidden_size_rnn) + '_test_'
        self.fname_baseline = self.graph_save_path + self.graph_type + self.generator_baseline+'_'+self.metric_baseline
        
