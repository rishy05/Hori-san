#flames
def flames_function(a_1, b_1):
  a = list(a_1)
  b = list(b_1)
  for i in a:
    for j in b:
      if i==j:
        a.remove(i)
        b.remove(j)
        break
  l=[]
  l=a+b
  n=len(l)
  l1=list('flames')
  while len(l1)>1:
      p = l1[n%len(l1)-1]
      l1 = l1[l1.index(p)+1:]+l1[:l1.index(p)+1]
      l1.remove(p)
      print(l1)
  if l1[0]=="f":
       return "Friends"
  elif l1[0]=="l":
       return "Lovers"
  elif l1[0]=="a":
       return "Affections"
  elif l1[0]=="m":
       return "Married"
  elif l1[0]=="e":
       return "Enemys"
  else:
       return "Sisters"
