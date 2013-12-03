#src: http://aimotion.blogspot.com/2012/08/introduction-to-recommendations-with.html

''' User-based Collaborative Filtering '''

from mrjob.job import MRJob
from similarity import correlation, jaccard, cosine, regularized_correlation
from math import sqrt

try:
    from itertools import combinations
except ImportError:
    from metrics import combinations


PRIOR_COUNT = 10
PRIOR_CORRELATION = 0


class CommaValueProtocol(object):

    def write(self, key, values):
        return ','.join(str(v) for v in values)


class UserSimilarities(MRJob):

    OUTPUT_PROTOCOL = CommaValueProtocol

    def steps(self):
        return [
            self.mr(mapper=self.group_by_item_rating,
                    reducer=self.count_ratings_users_freq),
            self.mr(mapper=self.pairwise_items,
                    reducer=self.calculate_similarity),
            self.mr(mapper=self.calculate_ranking,
                    reducer=self.top_similar_users)]

    def group_by_item_rating(self, key, line):
        '''
        Emit the item_id and group by its ratings (user and rating)

        '''
        user_id, item_id, rating = line.split('\t')

        yield  item_id, (user_id, float(rating))

    def count_ratings_users_freq(self, item_id, values):
        '''
        For each item, emit a row containing their user + rating pairs
        Also emit user rating sum and count for use later steps.

        '''
        user_count = 0
        user_sum = 0
        final = []
        for user_id, rating in values:
            user_count += 1
            user_sum += rating
            final.append((user_id, rating))

        yield item_id, (user_count, user_sum, final)

    def pairwise_items(self, item_id, values):
        '''
        The output drops the item_id from the key entirely, instead it emits
        the pair of users as the key.

        This mapper finds all combinations of user1,user2 pairs for every item,
        as long as that item was rated by more than one user. The values are the 
        corresponding ratings of each user.
        '''
        user_count, user_sum, ratings = values

        for user1, user2 in combinations(ratings, 2):
            yield (user1[0], user2[0]), \
                    (user1[1], user2[1], item_id)

    def calculate_similarity(self, pair_key, lines):
        '''
        Sum components of each corating pair across all items who were rated by 
        both user x and user y, then calculate pairwise pearson similarity and
        corating counts.  The similarities are normalized to the [0,1] scale
        because we do a numerical sort.

        19,21   0.4,2
        21,19   0.4,2
        19,70   0.6,1
        70,19   0.6,1
        21,70   0.1,1
        70,21   0.1,1
        '''
        sum_xx, sum_xy, sum_yy, sum_x, sum_y, n, item_list = (0.0, 0.0, 0.0, 0.0, 0.0, 0, [])
        user_pair, co_ratings_id = pair_key, lines
        user_xname, user_yname = user_pair
        for user_x, user_y, item_id in lines:
            sum_xx += user_x * user_x
            sum_yy += user_y * user_y
            sum_xy += user_x * user_y
            sum_y += user_y
            sum_x += user_x
            n += 1
            item_list.append(item_id)

        cos_sim = cosine(sum_xy, sqrt(sum_xx), sqrt(sum_yy))

        yield (user_xname, user_yname), (cos_sim, n, item_list)

    def calculate_ranking(self, user_keys, values):
        '''
        Emit users with similarity in key for ranking:

        '''
        cos_sim, n, item_list = values
        user_x, user_y = user_keys
        if int(n) > 0:
            yield (user_x, cos_sim), \
                     (user_y, n, item_list)

    def top_similar_users(self, key_sim, similar_ns):
        '''
        For each user emit K closest users.
        '''
        user_x, cos_sim = key_sim
        for user_y, n, item_list in similar_ns:
            yield None, (user_x, user_y, cos_sim, n, item_list)


if __name__ == '__main__':
    UserSimilarities.run()
