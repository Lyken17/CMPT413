import perc
import sys
import optparse
import os
from include.feature_vector import FeatureVector


def retrieve_feature(output, feat_list):
    # This function returns feature vector generated by certain output
    index = 0
    for i in range(1, len(output)-1):
        (index, feats) = perc.feats_for_word(index, feat_list)
        if len(feats) == 0:
            raise ValueError("Returned empty feature")
        feat_vec = FeatureVector()
        for feat in feats:
            feat_vec[feat, output[i]] += 1
    return feat_vec


def perc_train(train_data, tagset, iterations=1):
    feat_vec = FeatureVector()
    default_tag = tagset[0]

    for iteration in range(iterations):
        # Number of Sentences
        sentence_total = len(train_data)
        sentence_count = 0

        for (labeled_list, feat_list) in train_data:
            sentence_count += 1
            print "iteration", iteration, "sentence", sentence_count, "of", sentence_total
            # Retrieve Gold Output
            gold_output = []
            gold_output.append('B_-1')
            for i in labeled_list:
                (w, t, label) = i.split()
                gold_output.append(label)
            gold_output.append('B_+1')

            # Retrieve Local Output
            local_output = perc.perc_test(feat_vec,
                                          labeled_list,
                                          feat_list,
                                          tagset,
                                          default_tag)
            local_output.insert(0, 'B_-1')
            local_output.append('B_+1')

            # When Outputs are different, update feature vector
            if local_output != gold_output:
                # Extract features from both outputs
                local_vec = retrieve_feature(local_output, feat_list)
                gold_vec = retrieve_feature(gold_output, feat_list)

                feat_vec += gold_vec - local_vec

    return feat_vec

if __name__ == '__main__':
    optparser = optparse.OptionParser()
    optparser.add_option("-t", "--tagsetfile", dest="tagsetfile", default=os.path.join("data", "tagset.txt"), help="tagset that contains all the labels produced in the output, i.e. the y in \phi(x,y)")
    optparser.add_option("-i", "--trainfile", dest="trainfile", default=os.path.join("data", "train.txt.gz"), help="input data, i.e. the x in \phi(x,y)")
    optparser.add_option("-f", "--featfile", dest="featfile", default=os.path.join("data", "train.feats.gz"), help="precomputed features for the input data, i.e. the values of \phi(x,_) without y")
    optparser.add_option("-e", "--numepochs", dest="numepochs", default=int(1), help="number of epochs of training; in each epoch we iterate over over all the training examples")
    optparser.add_option("-m", "--modelfile", dest="modelfile", default=os.path.join("data", "default.model"), help="weights for all features stored on disk")
    (opts, _) = optparser.parse_args()

    # each element in the feat_vec dictionary is:
    # key=feature_id value=weight
    feat_vec = {}
    tagset = []
    train_data = []

    tagset = perc.read_tagset(opts.tagsetfile)
    print >>sys.stderr, "reading data ..."
    train_data = perc.read_labeled_data(opts.trainfile, opts.featfile)
    print >>sys.stderr, "done."
    feat_vec = perc_train(train_data, tagset, int(opts.numepochs))
    perc.perc_write_to_file(feat_vec, opts.modelfile)
