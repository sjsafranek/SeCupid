import ProgressBar2

widgets = [ProgressBar2.Bar(left='[',right=']'), ProgressBar2.Percentage(),' ', ProgressBar2.ETA()]
pbar = ProgressBar2.ProgressBar(widgets=widgets, maxval=10000000)
# maybe do something
pbar.start()
for i in range(2000000):
    # do something
    pbar.update(5*i+1)
pbar.finish()

print()