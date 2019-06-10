from Profile import Profile


class Neuron:

    # It is important that parent may not be neuron. If neuron is in first layer than it's parent is just array
    # The same goes for outputs, in last layer (FinalNeurons) they're raw sequences
    def __init__(self, seq_size, parent):
        self.profile = Profile(seq_size)
        self.seq_size = seq_size
        self.parent = parent
        self.outputs = []

    def calculate_matching(self, sequence):
        return self.profile.calculate_matching(sequence)

    def append_sequence(self, sequence):
        self.profile.load_sequence(sequence)

    def append_output(self, neuron):
        self.outputs.append(neuron)

    def get_minimum_output(self, sequence):
        """Calculating minimal matching value in output neurons

        This function takes all of its outputs and calculates how similar the sequence is to this outputs.
        We're searching for the least matching output category. Later network based on this minimal value will
        assign new sequence to this neuron OR (if threshold value will be grater than minimal matching value) it will
        create new neuron for this sequence.

        """
        min_value = 1
        for output in self.outputs:
            match = output.calculate_matching(sequence)
            min_value = match if match < min_value else min_value
        return min_value

    # is_final_neuron is used to mark whether we're about to erase final neuron and therefore need to delete
    # it's sequences' counts from it's parents. Since FinalNeuron inherits from Neuron we are not able to do this
    # check by using isinstance()
    def leave_parent(self, is_final_neuron):
        """Removing neuron from it's parent output

        This method is necessary because when we want to get rid of neuron (because i.e. final neuron doesn't meet the
        requirements for being motif) we need to inform it's parent neuron (or array) to remove this object. The reason
        why it is method in Neuron and not in FinalNeuron is that if FinalNeuron happens to be the only output neuron
        of Neuron, then there is no point of keeping this neuron (and therefore we recursively remove neurons with
        empty outputs.
        """
        if is_final_neuron:
            self._adjust_profiles(self, self.profile.counts.copy(), self.profile.seq_amount)
        if isinstance(self.parent, Neuron):
            if self._able_to_leave(self):
                self.parent.outputs.remove(self)
            if len(self.parent.outputs) == 0:
                self.parent.leave_parent(False)
        else:
            self.parent.remove(self)

    def _able_to_leave(self, parent):
        """Method which tells us if neuron can be erased from network

        This method is needed due to the fact that network needs at least one neuron per layer and this neurons
        have to be connected. leave_parent reduces obsolete neurons from network but it may happen that none of
        final neurons will have enough sequences to be called a motif. In this scenario this method proves to be
        useful as it marks this danger and tells neuron that he cannot leave network.

        Neuron is not allowed to leave when his parent and all parents way up to first layer has only one output.
        """
        if isinstance(parent, Neuron):
            if len(parent.outputs) > 1:
                return True
            return self._able_to_leave(parent.parent)
        else:
            # This is the case when parent is not a neuron but a list. It happens when this function reaches first layer
            if len(parent) > 1:
                return True
            return False

    def _adjust_profiles(self, parent, counts, seq_amount):
        """Method which deletes outdated sequences data from profiles

        When obsolete (non-motif) neuron is deleted, it's parents still have information about it's sequences
        in their's profiles. Therefore we need to clear outdated information just by deleting counts and then
        recalculating each profiles.

        It is important to run this method only for final neuron, because it's parents my be erased also and in this
        situation we'd clear more sequences then there actually were.
        """
        if not isinstance(parent, Neuron):
            return
        parent_counts = parent.profile.counts
        for count_pos in range(self.seq_size):
            for nucleotide in range(4):
                parent_counts[count_pos][nucleotide] -= counts[count_pos][nucleotide]
        parent.profile.seq_amount -= seq_amount
        parent.profile.calculate_probabilities()
        self._adjust_profiles(parent.parent, counts, seq_amount)
