import numpy as np
from sklearn.metrics.pairwise import *
from .DBManager import *

class StatistSystem:
    @staticmethod
    def get_user_recommendations(user_id, rel_watch):
        needed = 8
        acquinted = DBManager.get_user_acquainted(user_id)
        # print('acq', acquinted)
        collaborative = StatistSystem.col_recommend(user_id)
        # print('____collaboration_____', collaborative)
        print('____collaboration_____', collaborative)
        resultative = [watch for watch in collaborative if watch not in acquinted]
        # print('____collaboration_____', resultative)
        if(len(resultative) < needed):
            contentive = StatistSystem.cont_recommend(rel_watch)
            contentive = [watch for watch in contentive if watch not in acquinted]
            # print('____content_____', contentive)
            for watch in contentive:
                if(watch not in resultative):
                    resultative.append(watch)
        resultative = resultative[:needed]
        # print('____result_____', resultative)
        recommendations = DBManager.get_watches_by_id(resultative)
        return recommendations


    @staticmethod
    def cont_recommend(watch):
        similar = DBManager.get_similar_watches(watch, 30)
        return [watch['id'] for watch in similar]

    @staticmethod
    def col_recommend(user_id):
        ratings = DBManager.get_ratings()
        rates = ratings['rates']
        user_ids = ratings['user_ids']
        watch_ids = ratings['watch_ids']
        user_index = user_ids.index(user_id)
        print(user_index)
        # print('watch_ids', watch_ids)

        user_bound = 20
        len_user, len_rate = len(rates), len(rates[user_index])
        predict = np.zeros((len_rate))
        rates_matr = np.zeros((len_user, len_rate))
        for i in range(len_user):
            for j in range(len_rate):
                rates_matr[i][j] = rates[i][j]
        if(user_bound > len_user-1):
            user_bound = len_user-1

        avg_user_rating = np.array([x for x in rates_matr[user_index] if x > 0]).mean()
        user_similarity = 1 - pairwise_distances([rates_matr[user_index]], rates_matr, metric='cosine')[0]
        print('user_simil', user_similarity)
        print('user_simil', user_ids)
        top_sim_users = (user_similarity.argsort()[::-1])[1:user_bound + 1]
        # print(top_sim_users)
        indexes = top_sim_users.astype(int)

        abs_sim = np.abs(user_similarity)
        val = user_similarity[indexes]
        # print('val', val)

        differ = rates_matr[indexes]
        for ind in range(len(differ)):
            differ[ind] -= differ[ind][differ[ind]!=0].mean()
        val = val.dot(differ)
        # print('val', val)
        predict = avg_user_rating + val / abs_sim[indexes].sum()
        print('predict', predict)
        print('ids', watch_ids)
        # print(user_similarity)
        # print(predict)

        # print(watch_ids)
        predict_ind = predict.argsort()
        # print(predict_ind)
        result = []
        for i in range(len(predict)):
            if(predict[i] >= 3):
                result.append(watch_ids[predict_ind[i]])
        print('resi', result[::-1])
        return result[::-1]



        # for i in predict_ind:
        #     if(predict[i] >= 3):
        #         # print(i, predict[i])
        #         result.append(watch_ids[i])
        # print(result)
        # return result[::-1]

    @staticmethod
    def get_watch_comparing_info(watch_ids):
        const = {
            'sales': [DBManager.stat_compare_by_sales, 'amount', 'compare_sales'],
            'rates': [DBManager.stat_compare_by_rating, 'avg_rate', 'compare_rating']
        }
        info = {}
        comparing_res = None
        if(len(watch_ids) >= 2):
            for c_type in const:    
                comparing_res = const[c_type][0](watch_ids)
                if(c_type=='sales'):
                    sales_ceil = max([item['amount'] for item in comparing_res])
                format_res = {}
                curr_watch = comparing_res[0]['model_name']
                model_curve = ()
                for item in comparing_res:
                    temp_dict = {}
                    if(item['model_name'] != curr_watch):
                        curr_watch = item['model_name']
                        model_curve = ()
                    temp_dict['date_inter'] = item['date_inter']
                    temp_dict[const[c_type][1]] = item[const[c_type][1]]
                    if((c_type=='sales') and sales_ceil > 0):
                        temp_dict['amount'] /= sales_ceil/100
                    model_curve = (*model_curve, temp_dict)
                    if item['n'] == 0:
                        format_res[item['model_name']] = model_curve
                print(format_res)
                info[const[c_type][2]] = format_res
        return info

    @staticmethod
    def get_top_catalog_info():
        info = {}
        info['sales'] = DBManager.stat_catalog_sales_info()
        info['rating'] = DBManager.stat_catalog_rating_info()
        return info

    @staticmethod
    def get_watch_addit_info(watch_id):
        info = {}
        con = connections['default']
        with con.connection.cursor(DictCursor) as cursor:
            info['cost_categ'] = DBManager.stat_cost_categ_info()
            info['rates'] = DBManager.stat_watch_rates_info(watch_id)
            sales = DBManager.stat_catalog_sales_info()
            rating = DBManager.stat_catalog_rating_info()
            for i in sales:
                if watch_id == i['id']:
                    info['sales'] = sales
                    break
            for i in rating:
                if watch_id == i['id']:
                    info['rating'] = rating
                    break

            top_local_ordered = DBManager.stat_watch_top_locals(watch_id)
            if(len(top_local_ordered) >=5):
                info['top_local'] = top_local_ordered
            
            # print(top_local_ordered)
        return info