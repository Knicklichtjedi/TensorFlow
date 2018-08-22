import pstats

"""
This is just a test file!
"""

p = pstats.Stats('FilterResult')

# p.strip_dirs().sort_stats(-1).print_stats()

p.sort_stats("tottime")
p.print_stats()

# CALL WITH:
# $ python -m cProfile -o FilterResult image_filter.py
