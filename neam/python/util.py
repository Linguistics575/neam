import re

def multi_sub(correspondences, text):
    pattern = '({})'.format('|'.join(re.escape(key) for key in correspondences.keys()))
    return re.sub(pattern, lambda match: correspondences[match.group(0)], text)

