edges = []
for i in new_list:
    s = i['word']
    for k in new_list:
        t = k['word']
        for index, txt in db_data.uvod.iteritems():
            if s != t:
                if s.lower() in txt.lower() and t.lower() in txt.lower():
                    pair = {}
                    pair['source'] = s
                    pair['target'] = t
                    edges.append(pair)

dedup_edges = [dict(g) for g in set([tuple(l.items()) for l in edges])]
