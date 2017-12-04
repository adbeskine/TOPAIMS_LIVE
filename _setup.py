from home.models import Site_info

s = Site_info(locked=True, password='firstpasswordshouldchangeeverytimesitelocks')
s.save()