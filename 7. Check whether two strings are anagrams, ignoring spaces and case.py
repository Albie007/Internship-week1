str1="listen"
str2="silent"
croppdstr1=list(str1.strip().lower())
croppdstr2=list(str2.strip().lower())
croppdstr1.sort()
croppdstr2.sort()
if croppdstr1 == croppdstr2:
    print("This are anagrams ")
else:
    print("This are not anagrams ")